# -*- coding: utf-8 -*-
"""Unity 相关：UnityPy 兼容层 + PKG 容器解析 + 贴图替换"""

import struct

from .debug import debug_log

# ===== UnityPy 兼容层 =====

import ctypes as _ctypes

_orig_CDLL = _ctypes.CDLL


class _FmodSafeCDLL(_orig_CDLL):
    """CDLL子类，在fmod.dll加载失败时静默跳过而非报错"""
    def __init__(self, name, *args, **kwargs):
        if name and isinstance(name, str) and 'fmod' in name.lower():
            self._name = name
            self._handle = None
            return
        super().__init__(name, *args, **kwargs)


_ctypes.CDLL = _FmodSafeCDLL

import UnityPy  # noqa: E402


# ===== PKG 容器文件解析与重打包 =====

class PkgEntry:
    def __init__(self, index, offset, size):
        self.index = index
        self.offset = offset
        self.size = size


class PkgFile:
    HEADER_SIZE = 24
    FOOTER_SIZE = 8
    MAX_PKG_SIZE = 1 * 1024 * 1024 * 1024
    EXCLUDED_PKGS = {'meta.pkg'}

    def __init__(self):
        self.filepath = None
        self.header = None
        self.footer = None
        self.entries = []

    def parse(self, filepath):
        self.filepath = filepath
        self.entries = []
        debug_log(f"PkgFile.parse: {filepath}")
        with open(filepath, 'rb') as f:
            data = f.read()
        self.header = data[:self.HEADER_SIZE]
        total_len = len(data)
        positions = []
        idx = 0
        while True:
            pos = data.find(b'UnityFS', idx)
            if pos == -1:
                break
            positions.append(pos)
            idx = pos + 1
        valid_positions = []
        for i, pos in enumerate(positions):
            if data[pos:pos + 8] != b'UnityFS\x00':
                continue
            valid_positions.append(pos)
        for j, pos in enumerate(valid_positions):
            if j + 1 < len(valid_positions):
                actual_size = valid_positions[j + 1] - pos
            else:
                fs_size = struct.unpack('>Q', data[pos + 30:pos + 38])[0]
                footer_start_est = pos + fs_size
                if footer_start_est + self.FOOTER_SIZE <= total_len:
                    actual_size = fs_size
                else:
                    actual_size = total_len - self.FOOTER_SIZE - pos
            self.entries.append(PkgEntry(j + 1, pos, actual_size))
        if self.entries:
            last = self.entries[-1]
            footer_start = last.offset + last.size
            self.footer = data[footer_start:footer_start + self.FOOTER_SIZE]
            if len(self.footer) < self.FOOTER_SIZE:
                self.footer = self.footer + b'\x00' * (self.FOOTER_SIZE - len(self.footer))
        else:
            self.footer = b'\x00' * self.FOOTER_SIZE
        return len(self.entries)

    def extract_single(self, entry_index, output_path):
        debug_log(f"PkgFile.extract_single: entry={entry_index}, output={output_path}")
        with open(self.filepath, 'rb') as f:
            f.seek(self.entries[entry_index].offset)
            data = f.read(self.entries[entry_index].size)
        with open(output_path, 'wb') as f:
            f.write(data)

    @staticmethod
    def repack_from_data(header, footer, file_data_list):
        import io
        buf = io.BytesIO()
        actual_count = len(file_data_list)
        header = header[:20] + struct.pack('<I', actual_count) + header[24:]
        buf.write(header)
        for d in file_data_list:
            buf.write(d)
        buf.write(footer)
        return buf.getvalue()


# ===== Unity3D 资源编辑 =====

class Unity3DEditor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.env = None
        self.assets = []
        self.modified = False

    def load(self):
        debug_log(f"Unity3DEditor.load: {self.filepath}")
        self.env = UnityPy.load(self.filepath)
        self.assets = []
        container_map = {}
        for obj in self.env.objects:
            if obj.type.name == 'AssetBundle':
                try:
                    data = obj.read()
                    for item in data.m_Container:
                        if isinstance(item, (list, tuple)) and len(item) == 2:
                            container_path = item[0]
                            asset_info = item[1]
                            if hasattr(asset_info, 'asset') and hasattr(asset_info.asset, 'm_PathID'):
                                container_map[asset_info.asset.m_PathID] = container_path
                except Exception as e:
                    debug_log(f"读取 AssetBundle container 失败: {e}")
        for obj in self.env.objects:
            class_name = obj.type.name if hasattr(obj.type, 'name') else str(obj.type)
            name = ''
            container = ''
            try:
                data = obj.read()
                name = getattr(data, 'm_Name', '') or ''
                if not name and hasattr(data, 'name'):
                    name = data.name
                if not name and hasattr(data, 'm_PathName'):
                    name = data.m_PathName
                container = container_map.get(obj.path_id, '')
            except Exception:
                try:
                    tree = obj.read_typetree()
                    if isinstance(tree, dict):
                        name = tree.get('m_Name', '') or ''
                    elif hasattr(tree, 'm_Name'):
                        name = tree.m_Name or ''
                except Exception as e:
                    debug_log(f"read_typetree 也失败 path_id={obj.path_id}: {e}")
            if not name:
                name = f"{class_name}_{obj.path_id}"
            self.assets.append({
                'path_id': obj.path_id,
                'class_id': obj.type_id,
                'class_name': class_name,
                'container': container,
                'name': name,
            })
        return self.assets

    def get_object(self, path_id):
        for obj in self.env.objects:
            if obj.path_id == path_id:
                return obj
        return None

    def import_texture(self, path_id, input_path):
        debug_log(f"Unity3DEditor.import_texture: path_id={path_id}, input={input_path}")
        obj = self.get_object(path_id)
        if obj is None:
            raise RuntimeError("未找到对象")
        data = obj.read()
        data.set_image(input_path)
        data.save()
        self.modified = True

    def save(self, output_path=None):
        if output_path is None:
            output_path = self.filepath
        debug_log(f"Unity3DEditor.save: {output_path}")
        with open(output_path, 'wb') as f:
            f.write(self.env.file.save())
        self.modified = False
