# -*- coding: utf-8 -*-
"""PKG 操作：多线程搜索 / 应用修改 / 备份 / 还原 / 清理"""

import os
import gc
import json
import shutil
import struct
import tempfile
import threading

from PyQt5.QtCore import QThread, pyqtSignal

from .debug import debug_log
from .unity import UnityPy, PkgFile, Unity3DEditor
from .paths import find_container_dir


# ===== PKG 内存检索线程 =====

class PkgSearchThread(QThread):
    progress = pyqtSignal(int, int, str)
    found = pyqtSignal(str, str, str, str, int)
    finished = pyqtSignal(int, int)

    def __init__(self, pkg_files, asset_type, asset_name_pattern, max_workers=1):
        super().__init__()
        self.pkg_files = pkg_files
        self.asset_type = asset_type
        self.asset_name_pattern = asset_name_pattern
        self.max_workers = max(1, min(max_workers, 4))
        self._stopped = False
        self._found_count = 0
        self._scanned_count = 0
        self._lock = None

    def stop(self):
        self._stopped = True

    @staticmethod
    def calc_workers(pkg_files):
        try:
            import psutil
            cpu_count = os.cpu_count() or 2
            avail_mem_gb = psutil.virtual_memory().available / (1024 ** 3)
            usable_mem_gb = max(avail_mem_gb - 2, 1)
            mem_workers = int(usable_mem_gb / 0.15)
            return max(1, min(cpu_count, mem_workers, 4))
        except ImportError:
            return min(os.cpu_count() or 2, 2)

    def _search_single_pkg(self, pkg_path):
        results = []
        try:
            fsize = os.path.getsize(pkg_path)
            if fsize > PkgFile.MAX_PKG_SIZE:
                return results
        except OSError:
            return results
        try:
            with open(pkg_path, 'rb') as f:
                pkg_data = f.read()
        except OSError:
            return results
        positions = []
        idx = 0
        while True:
            pos = pkg_data.find(b'UnityFS', idx)
            if pos == -1:
                break
            positions.append(pos)
            idx = pos + 1
        for entry_idx, pos in enumerate(positions):
            if self._stopped:
                break
            try:
                if pkg_data[pos:pos + 8] != b'UnityFS\x00':
                    continue
                fs_size = struct.unpack('>Q', pkg_data[pos + 30:pos + 38])[0]
            except (struct.error, IndexError):
                continue
            try:
                entry_data = pkg_data[pos:pos + fs_size]
                env = UnityPy.load(entry_data)
                for obj in env.objects:
                    if self._stopped:
                        break
                    class_name = obj.type.name if hasattr(obj.type, 'name') else str(obj.type)
                    if class_name != self.asset_type:
                        continue
                    try:
                        data = obj.read()
                        name = getattr(data, 'm_Name', '') or ''
                        if not name and hasattr(data, 'name'):
                            name = data.name
                        if not name and hasattr(data, 'm_PathName'):
                            name = data.m_PathName
                    except Exception as e:
                        debug_log(f"搜索时读取对象失败 path_id={obj.path_id}: {e}")
                        continue
                    if self.asset_name_pattern.lower() in name.lower():
                        results.append((pkg_path, class_name, name, str(obj.path_id), entry_idx + 1))
            except Exception as e:
                debug_log(f"搜索PKG条目失败 entry={entry_idx}: {e}")
                continue
        del pkg_data
        return results

    def run(self):
        debug_log(f"PkgSearchThread.run: 开始搜索, {len(self.pkg_files)}个PKG, {self.max_workers}线程")
        self._lock = threading.Lock()
        self._found_count = 0
        self._scanned_count = 0
        total = len(self.pkg_files)
        pkg_index = [0]
        index_lock = threading.Lock()

        def worker(thread_id):
            while not self._stopped:
                with index_lock:
                    if pkg_index[0] >= total:
                        break
                    i = pkg_index[0]
                    pkg_index[0] += 1
                pkg_path = self.pkg_files[i]
                pkg_filename = os.path.basename(pkg_path)
                try:
                    fsize = os.path.getsize(pkg_path)
                    if fsize > PkgFile.MAX_PKG_SIZE:
                        with self._lock:
                            self._scanned_count += 1
                        self.progress.emit(self._scanned_count, total, f"[跳过>1G] {pkg_filename}")
                        continue
                except OSError:
                    with self._lock:
                        self._scanned_count += 1
                    continue
                self.progress.emit(self._scanned_count + 1, total, pkg_filename)
                results = self._search_single_pkg(pkg_path)
                with self._lock:
                    self._scanned_count += 1
                    self._found_count += len(results)
                for r in results:
                    self.found.emit(*r)
                del results
                gc.collect()

        threads = []
        for tid in range(self.max_workers):
            t = threading.Thread(target=worker, args=(tid,), daemon=True)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        gc.collect()
        debug_log(f"PkgSearchThread.run: 搜索完成, found={self._found_count}, scanned={self._scanned_count}")
        self.finished.emit(self._found_count, self._scanned_count)


# ===== 应用修改 / 备份 / 还原 / 清理 =====

def apply_changes(tasks, progress_callback=None, log_callback=None, bak_dir=None):
    """将裁剪后的图片应用到 PKG 文件

    Args:
        tasks: list of (label, result_dict, cache_path)
        progress_callback: function(current_pct) or None
        log_callback: function(text) or None
        bak_dir: 备份目录，None时回退到模块推导（打包后可能不可写）

    Returns:
        True on success, False on failure
    """
    def _log(msg):
        if log_callback:
            log_callback(msg)

    if not tasks:
        debug_log("应用修改: 没有可应用的任务")
        return False

    debug_log(f"开始应用修改: {len(tasks)}个任务, bak_dir={bak_dir}")

    if progress_callback:
        progress_callback(5)

    if not bak_dir:
        bak_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'bak')
    try:
        os.makedirs(bak_dir, exist_ok=True)
    except OSError as e:
        debug_log(f"创建备份目录失败: {bak_dir}, {e}")
        _log(f"[错误] 无法创建备份目录 {bak_dir}: {e}")
        _log("请将程序放到有写入权限的文件夹，或以管理员身份运行")
        return False
    debug_log(f"使用备份目录: {bak_dir}")

    backed_up_pkgs = []
    try:
        pkg_tasks = {}
        for label, result, cache_path in tasks:
            pkg_path = result['pkg_path']
            if pkg_path not in pkg_tasks:
                pkg_tasks[pkg_path] = []
            pkg_tasks[pkg_path].append((label, result, cache_path))

        debug_log(f"应用修改: {len(pkg_tasks)}个PKG文件需要处理")
        total_pkgs = len(pkg_tasks)

        for pkg_idx, (pkg_path, pkg_task_list) in enumerate(pkg_tasks.items()):
            debug_log(f"处理PKG [{pkg_idx+1}/{total_pkgs}]: {os.path.basename(pkg_path)}")

            bak_path = backup_pkg(pkg_path, bak_dir)
            if bak_path:
                backed_up_pkgs.append((pkg_path, bak_path))

            pkg = PkgFile()
            pkg.parse(pkg_path)
            with open(pkg_path, 'rb') as f:
                all_data = f.read()

            for label, result, cache_path in pkg_task_list:
                entry_index = result['entry_index']
                path_id_str = result['path_id']
                debug_log(f"  替换{label}: asset={result['asset_name']}, entry={entry_index}, path_id={path_id_str}")

                temp_dir = tempfile.mkdtemp(prefix="pkg_apply_")
                temp_file = os.path.join(temp_dir, f"file{entry_index}.unity3d")
                pkg.extract_single(entry_index - 1, temp_file)
                debug_log(f"  提取条目到: {temp_file}")

                editor = Unity3DEditor(temp_file)
                editor.load()
                path_id = int(path_id_str) if path_id_str.lstrip('-').isdigit() else 0
                editor.import_texture(path_id, cache_path)
                editor.save()
                debug_log(f"  纹理已导入并保存: path_id={path_id}")

                with open(temp_file, 'rb') as f:
                    new_entry_data = f.read()

                file_data_list = []
                for entry in pkg.entries:
                    if entry.index == entry_index:
                        file_data_list.append(new_entry_data)
                    else:
                        file_data_list.append(all_data[entry.offset:entry.offset + entry.size])

                new_pkg_data = PkgFile.repack_from_data(pkg.header, pkg.footer, file_data_list)
                with open(pkg_path, 'wb') as f:
                    f.write(new_pkg_data)
                debug_log(f"  PKG已重新打包写入: {os.path.basename(pkg_path)}")
                # 记录修改后签名：区分"本程序改过"（跳过备份）与"游戏更新过"（重新备份）
                record_applied_signature(pkg_path, bak_dir)

                del new_pkg_data
                del file_data_list
                shutil.rmtree(temp_dir, ignore_errors=True)

                _log(f"[替换] {label}: {result['asset_name']} <- {os.path.basename(cache_path)}")

            del all_data
            gc.collect()

            if progress_callback:
                progress_val = int((pkg_idx + 1) / total_pkgs * 90) + 5
                progress_callback(progress_val)

        if progress_callback:
            progress_callback(100)
        debug_log("应用修改完成")
        return True

    except Exception as e:
        debug_log(f"应用修改失败: {e}")
        _log(f"[错误] 应用修改失败: {e}")
        if backed_up_pkgs:
            debug_log(f"开始还原已备份的 {len(backed_up_pkgs)} 个PKG文件")
            _log("正在还原已修改的文件，请勿关闭程序...")
            for orig_path, bak_path in backed_up_pkgs:
                try:
                    if os.path.exists(bak_path):
                        shutil.copy2(bak_path, orig_path)
                        debug_log(f"已还原: {os.path.basename(orig_path)}")
                        _log(f"[还原] {os.path.basename(orig_path)}")
                except Exception as restore_err:
                    debug_log(f"还原失败: {orig_path}, {restore_err}")
                    _log(f"[错误] 还原失败: {os.path.basename(orig_path)}，请手动从备份目录恢复")
            debug_log("还原流程结束")
        return False


BAK_MANIFEST_NAME = 'bak_manifest.json'


def _load_bak_manifest(bak_dir):
    """读取备份清单 {pkg_name: {orig_size, orig_mtime, applied_size, applied_mtime}}"""
    path = os.path.join(bak_dir, BAK_MANIFEST_NAME)
    try:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data, dict):
                return data
    except Exception as e:
        debug_log(f"读取备份清单失败: {e}")
    return {}


def _save_bak_manifest(bak_dir, manifest):
    path = os.path.join(bak_dir, BAK_MANIFEST_NAME)
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
    except Exception as e:
        debug_log(f"写入备份清单失败: {e}")


def _file_signature(path):
    """返回 (size, mtime) 签名，失败返回 None"""
    try:
        stat = os.stat(path)
        return (stat.st_size, stat.st_mtime)
    except OSError as e:
        debug_log(f"获取文件信息失败: {path}, {e}")
        return None


def _manifest_matches(record, sig):
    return (record.get('size'), record.get('mtime')) == sig


def backup_pkg(pkg_path, bak_dir):
    """备份 PKG 文件（带新鲜度校验）

    - 无备份：备份并记录原始签名
    - 已有备份且游戏文件与 orig/applied 签名一致：跳过（同会话重复应用场景，保留原始备份）
    - 已有备份但游戏文件已外部变化（如游戏更新）：重新备份覆盖，防止旧版本备份盖掉新游戏文件
    - 有备份但无清单记录（旧版本程序残留）：无法确认新鲜度，重新备份（安全方向）
    """
    os.makedirs(bak_dir, exist_ok=True)
    pkg_name = os.path.basename(pkg_path)
    bak_path = os.path.join(bak_dir, pkg_name)
    sig = _file_signature(pkg_path)
    if sig is None:
        return None
    manifest = _load_bak_manifest(bak_dir)
    if os.path.exists(bak_path):
        record = manifest.get(pkg_name)
        if record and (_manifest_matches({'size': record.get('orig_size'), 'mtime': record.get('orig_mtime')}, sig)
                       or _manifest_matches({'size': record.get('applied_size'), 'mtime': record.get('applied_mtime')}, sig)):
            debug_log(f"备份有效，跳过: {bak_path}")
            return bak_path
        debug_log(f"备份与当前游戏文件不一致，重新备份: {pkg_name}")
    shutil.copy2(pkg_path, bak_path)
    manifest[pkg_name] = {'orig_size': sig[0], 'orig_mtime': sig[1]}
    _save_bak_manifest(bak_dir, manifest)
    debug_log(f"备份: {pkg_name} -> {bak_path}")
    return bak_path


def record_applied_signature(pkg_path, bak_dir):
    """应用修改成功后记录修改后文件的签名，用于区分'本程序改过'与'游戏更新过'"""
    sig = _file_signature(pkg_path)
    if sig is None:
        return
    manifest = _load_bak_manifest(bak_dir)
    name = os.path.basename(pkg_path)
    record = manifest.get(name)
    if record:
        record['applied_size'] = sig[0]
        record['applied_mtime'] = sig[1]
        _save_bak_manifest(bak_dir, manifest)


def restore_backup(bak_dir, config_path, game_path, log_callback=None):
    """还原所有备份文件"""
    def _log(msg):
        if log_callback:
            log_callback(msg)

    if not os.path.exists(bak_dir):
        debug_log("还原备份: 备份目录不存在")
        return 0

    bak_files = [f for f in os.listdir(bak_dir) if f.endswith('.pkg')]
    if not bak_files:
        debug_log("还原备份: 没有备份文件")
        return 0

    debug_log(f"还原备份: 找到{len(bak_files)}个备份文件")
    restored = 0

    for bak_name in bak_files:
        bak_path = os.path.join(bak_dir, bak_name)
        orig_path = _find_orig_path(bak_name, config_path, game_path)

        if orig_path and os.path.exists(orig_path):
            shutil.copy2(bak_path, orig_path)
            restored += 1
            debug_log(f"还原: {bak_name} -> {orig_path}")
            _log(f"[还原] {bak_name}")
        else:
            debug_log(f"还原跳过(找不到原始路径): {bak_name}")

    debug_log(f"还原完成: {restored}个文件")
    return restored


def _find_orig_path(bak_name, config_path, game_path):
    """查找备份文件对应的原始路径"""
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            target_pkg = config.get('target_pkg', {})
            if target_pkg.get('name') == bak_name:
                return target_pkg.get('path', '')
    except Exception as e:
        debug_log(f"读取备份配置失败: {e}")

    if game_path:
        container_dir = find_container_dir(game_path)
        if container_dir:
            return os.path.join(container_dir, bak_name)
    return None


def cleanup_on_exit(bak_dir, cache_dir, config_path, game_path):
    """退出时还原备份并清理临时目录"""
    debug_log("开始退出清理")

    if os.path.exists(bak_dir):
        bak_files = [f for f in os.listdir(bak_dir) if f.endswith('.pkg')]
        debug_log(f"退出清理: 找到{len(bak_files)}个备份文件需要还原")
        for bak_name in bak_files:
            bak_path = os.path.join(bak_dir, bak_name)
            orig_path = _find_orig_path(bak_name, config_path, game_path)
            if orig_path and os.path.exists(orig_path):
                try:
                    shutil.copy2(bak_path, orig_path)
                    debug_log(f"退出还原: {bak_name} -> {orig_path}")
                except Exception as e:
                    debug_log(f"退出还原失败: {bak_name}, {e}")

    if os.path.exists(bak_dir):
        try:
            shutil.rmtree(bak_dir)
            debug_log("已删除备份目录")
        except Exception as e:
            debug_log(f"删除备份目录失败: {e}")

    if os.path.exists(cache_dir):
        try:
            shutil.rmtree(cache_dir)
            debug_log("已清理缓存目录")
        except Exception as e:
            debug_log(f"清理缓存目录失败: {e}")
    debug_log("退出清理完成")
