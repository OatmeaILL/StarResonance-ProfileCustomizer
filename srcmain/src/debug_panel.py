# -*- coding: utf-8 -*-
"""调试用窗口分辨率面板（仅 debug 模式显示）"""

from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QSpinBox, QPushButton
from .debug import debug_log
from .win32_tools import set_game_window_resolution
from .i18n import t


def create_debug_resize_panel(parent_layout, apply_callback=None):
    """创建调试面板并添加到布局

    Args:
        parent_layout: 要添加到的布局
        apply_callback: 点击应用时的回调(hwnd, w, h, scale) or None

    Returns:
        (group, w_spin, h_spin, scale_spin, btn)
    """
    group = QGroupBox(t('debug_resize_title'))
    layout = QHBoxLayout(group)
    layout.addWidget(QLabel(t('debug_label_w')))
    w_spin = QSpinBox()
    w_spin.setRange(1, 100000)
    w_spin.setValue(500)
    layout.addWidget(w_spin)
    layout.addWidget(QLabel(t('debug_label_h')))
    h_spin = QSpinBox()
    h_spin.setRange(1, 100000)
    h_spin.setValue(5735)
    layout.addWidget(h_spin)
    layout.addWidget(QLabel(t('debug_label_scale')))
    scale_spin = QSpinBox()
    scale_spin.setRange(1, 100)
    scale_spin.setValue(100)
    layout.addWidget(scale_spin)
    btn = QPushButton(t('debug_btn_apply'))
    btn.setStyleSheet(
        "QPushButton { background-color: #e74c3c; color: white; font-weight: bold; "
        "padding: 6px 14px; border-radius: 4px; }"
    )
    group.setVisible(False)
    parent_layout.addWidget(group)
    return group, w_spin, h_spin, scale_spin, btn


def apply_debug_resize(game_hwnd, w, h, scale):
    """执行窗口分辨率调整

    Returns:
        (success: bool, actual_w: int, actual_h: int)
    """
    if not game_hwnd:
        return False, 0, 0
    actual_w = int(w * scale / 100)
    actual_h = int(h * scale / 100)
    result = set_game_window_resolution(game_hwnd, w, h, scale)
    if result:
        debug_log(f"[DEBUG RESIZE] {w}x{h}@{scale}% -> {actual_w}x{actual_h}")
        return True, actual_w, actual_h
    else:
        debug_log(f"[DEBUG RESIZE] 失败: {w}x{h}@{scale}%")
        return False, 0, 0
