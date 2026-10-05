# -*- coding: utf-8 -*-
"""Win32 窗口操作：查找游戏窗口、调整分辨率、检测进程、手动捕获窗口"""

import ctypes
import ctypes.wintypes

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer

from .constants import GAME_PROCESS_NAMES, GAME_WINDOW_TITLES
from .debug import debug_log
from .i18n import t

try:
    import ctypes
    import ctypes.wintypes
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False

user32 = ctypes.windll.user32 if HAS_WIN32 else None

if HAS_WIN32:
    user32.SetWindowPos.restype = ctypes.c_bool
    user32.SetWindowPos.argtypes = [
        ctypes.wintypes.HWND, ctypes.wintypes.HWND,
        ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
        ctypes.c_uint
    ]
    user32.MoveWindow.restype = ctypes.c_bool
    user32.MoveWindow.argtypes = [
        ctypes.wintypes.HWND, ctypes.c_int, ctypes.c_int,
        ctypes.c_int, ctypes.c_int, ctypes.c_bool
    ]
    user32.GetWindowLongW.restype = ctypes.c_long
    user32.GetWindowLongW.argtypes = [ctypes.wintypes.HWND, ctypes.c_int]
    user32.SetWindowLongW.restype = ctypes.c_long
    user32.SetWindowLongW.argtypes = [ctypes.wintypes.HWND, ctypes.c_int, ctypes.c_long]
    user32.ShowWindow.restype = ctypes.c_bool
    user32.ShowWindow.argtypes = [ctypes.wintypes.HWND, ctypes.c_int]
    user32.GetWindowRect.restype = ctypes.c_bool
    user32.GetWindowRect.argtypes = [ctypes.wintypes.HWND, ctypes.POINTER(ctypes.wintypes.RECT)]
    user32.GetAncestor.restype = ctypes.wintypes.HWND
    user32.GetAncestor.argtypes = [ctypes.wintypes.HWND, ctypes.c_uint]
    user32.IsWindow.restype = ctypes.c_bool
    user32.IsWindow.argtypes = [ctypes.wintypes.HWND]
    user32.WindowFromPoint.restype = ctypes.wintypes.HWND
    user32.WindowFromPoint.argtypes = [ctypes.wintypes.POINT]
    user32.GetCursorPos.restype = ctypes.c_bool
    user32.GetCursorPos.argtypes = [ctypes.POINTER(ctypes.wintypes.POINT)]
    user32.GetAsyncKeyState.restype = ctypes.c_short
    user32.GetAsyncKeyState.argtypes = [ctypes.c_int]


def find_game_window():
    """查找游戏进程的窗口句柄，优先匹配已知标题，其次按进程名匹配"""
    if not HAS_WIN32:
        return 0, ''
    result = [0, '']

    def enum_callback(hwnd, _):
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buf = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buf, length + 1)
                pid = ctypes.wintypes.DWORD()
                user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                try:
                    import psutil
                    p = psutil.Process(pid.value)
                    if p.name().lower() in GAME_PROCESS_NAMES:
                        if buf.value in GAME_WINDOW_TITLES:
                            result[0] = hwnd
                            result[1] = buf.value
                            return False
                        elif result[0] == 0:
                            result[0] = hwnd
                            result[1] = buf.value
                except Exception as e:
                    debug_log(f"枚举窗口时获取进程信息失败 pid={pid.value}: {e}")
        return True

    callback_type = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
    user32.EnumWindows(callback_type(enum_callback), 0)
    return result[0], result[1]


def set_game_window_resolution(hwnd, width, height, scale_percent=100):
    """修改游戏窗口分辨率和缩放，并移动到左上角"""
    if not HAS_WIN32:
        return False

    actual_w = int(width * scale_percent / 100)
    actual_h = int(height * scale_percent / 100)

    try:
        GWL_STYLE = -16
        WS_POPUP = 0x80000000
        WS_OVERLAPPEDWINDOW = 0x00CF0000
        WS_VISIBLE = 0x10000000

        current_style = user32.GetWindowLongW(hwnd, GWL_STYLE)

        if current_style & WS_POPUP:
            user32.SetWindowLongW(hwnd, GWL_STYLE, WS_OVERLAPPEDWINDOW | WS_VISIBLE)

        moved = user32.MoveWindow(hwnd, 0, 0, actual_w, actual_h, True)

        if not moved:
            SWP_NOZORDER = 0x0004
            SWP_FRAMECHANGED = 0x0020
            moved = user32.SetWindowPos(hwnd, 0, 0, 0, actual_w, actual_h,
                                SWP_NOZORDER | SWP_FRAMECHANGED)

        if not moved:
            debug_log(f"set_game_window_resolution: 窗口调整失败 hwnd={hwnd}, {actual_w}x{actual_h}")
            return False

        WM_SIZE = 0x0005
        SIZE_RESTORED = 0
        user32.SendMessageW(hwnd, WM_SIZE, SIZE_RESTORED, (actual_h << 16) | (actual_w & 0xFFFF))

        return True
    except Exception as e:
        debug_log(f"set_game_window_resolution 异常: {e}")
        return False


def is_game_running():
    """检查游戏进程是否在运行"""
    try:
        import psutil
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] and proc.info['name'].lower() in GAME_PROCESS_NAMES:
                return True
    except Exception as e:
        debug_log(f"检测游戏进程失败: {e}")
    return False


class WindowCapture:
    """管理手动捕获游戏窗口的交互流程

    Captured callback signature: on_captured(hwnd, window_title, process_name, pid)
    """

    def __init__(self, parent_widget):
        self._parent = parent_widget
        self._capturing = False
        self._mouse_ready = False
        self._timer = None
        self.on_captured = None
        self.on_cancel = None

    @property
    def is_capturing(self):
        return self._capturing

    def start(self, btn_capture_window):
        if not HAS_WIN32:
            QMessageBox.warning(self._parent, t('tip'), t('warning'))
            return
        debug_log("开始手动捕获游戏窗口")
        self._capturing = True
        self._mouse_ready = False
        btn_capture_window.setEnabled(False)
        btn_capture_window.setText(t('capture_prompt'))
        btn_capture_window.setToolTip(t('tooltip_capture'))
        self._parent.showMinimized()

        if self._timer is None:
            self._timer = QTimer(self._parent)
            self._timer.timeout.connect(self._poll)
        self._timer.start(100)

    def _poll(self):
        if not self._capturing:
            self.cancel()
            return
        if not HAS_WIN32:
            self.cancel()
            return

        vk_escape = 0x1B
        if user32.GetAsyncKeyState(vk_escape) & 0x8000:
            self.cancel()
            return

        vk_lbutton = 0x01
        lbutton_down = user32.GetAsyncKeyState(vk_lbutton) & 0x8000
        if not self._mouse_ready:
            if not lbutton_down:
                self._mouse_ready = True
            return

        if lbutton_down:
            self._timer.stop()
            point = ctypes.wintypes.POINT()
            user32.GetCursorPos(ctypes.byref(point))
            hwnd = user32.WindowFromPoint(point)
            if hwnd:
                GA_ROOT = 2
                root_hwnd = user32.GetAncestor(hwnd, GA_ROOT)
                if root_hwnd:
                    hwnd = root_hwnd
            if hwnd and hwnd != int(self._parent.winId()):
                self._confirm(hwnd)
            else:
                self.cancel()

    def _confirm(self, hwnd):
        self._capturing = False
        self._parent.showNormal()
        self._parent.activateWindow()
        self._parent.raise_()
        debug_log(f"捕获到窗口: hwnd={hwnd}")

        length = user32.GetWindowTextLengthW(hwnd)
        buf = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buf, length + 1)
        window_title = buf.value

        pid = ctypes.wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        process_name = ''
        try:
            import psutil
            p = psutil.Process(pid.value)
            process_name = p.name()
        except Exception:
            process_name = t('capture_pid_label').format(pid.value)

        if not window_title:
            window_title = t('no_title')

        info_text = t('capture_confirm_text').format(
            window_title, process_name, pid.value, hwnd
        )
        reply = QMessageBox.question(
            self._parent, t('capture_confirm_title'), info_text,
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            if self.on_captured:
                self.on_captured(hwnd, window_title, process_name, pid.value)
        else:
            self.cancel()

    def cancel(self):
        self._capturing = False
        if self._timer and self._timer.isActive():
            self._timer.stop()
        self._parent.showNormal()
        self._parent.activateWindow()
        self._parent.raise_()
        if self.on_cancel:
            self.on_cancel()
