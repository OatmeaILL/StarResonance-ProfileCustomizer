# -*- coding: utf-8 -*-
"""主窗口：三 Tab GUI（查找资源 / 编辑图片 / 更换操作）"""

import os
import re
import sys
import json
import threading
import queue

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView,
    QFileDialog, QMessageBox, QProgressBar, QLabel, QPushButton,
    QGroupBox, QLineEdit, QAbstractItemView,
    QPlainTextEdit, QSlider, QSpinBox, QRadioButton, QButtonGroup,
    QSizePolicy, QTextBrowser, QDialog, QFrame,
    QComboBox, QCheckBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QRect, QPoint, QTimer
from PyQt5.QtGui import (
    QFont, QColor, QPixmap, QImage, QPainter, QPen, QTextCursor, QIcon
)
from PIL import Image

from .constants import (
    APP_VERSION,
    EXCLUDED_ASSET_NAMES, IMAGE_ICON, IMAGE_EASTEREGG,
)
from .paths import resource_path, app_dir, find_container_dir
from .debug import debug_log, is_debug_enabled
from .debug_panel import create_debug_resize_panel, apply_debug_resize
from .win32_tools import (
    find_game_window, set_game_window_resolution, is_game_running,
    user32, HAS_WIN32, WindowCapture,
)
from .unity import PkgFile
from .pkg_ops import PkgSearchThread, apply_changes
from .image_crop import (
    ImageCropWidget, ClickableLabel,
    CARD_WIDTH, CARD_HEIGHT, AVATAR_WIDTH, AVATAR_HEIGHT,
    THUMB_MIN_SIZE, THUMB_MAX_SIZE, draw_preview_border,
)
from .info_dialogs import show_tutorial_dialog, show_faq_dialog, show_about_dialog
from .i18n import (
    t, get_card_steps, get_avatar_steps,
)
from . import pkg_ops


def _btn_style(bg, hover, padding="6px 12px", font_size=None, pressed=None, disabled=False):
    """生成按钮 QSS 样式字符串，消除重复的内联样式定义"""
    parts = [f"QPushButton {{ background-color: {bg}; color: white; font-weight: bold; "
             f"padding: {padding}; border-radius: 4px;"]
    if font_size:
        parts.append(f" font-size: {font_size};")
    parts.append(" }")
    parts.append(f" QPushButton:hover {{ background-color: {hover}; }}")
    if pressed:
        parts.append(f" QPushButton:pressed {{ background-color: {pressed}; }}")
    if disabled:
        parts.append(" QPushButton:disabled { background-color: #95a5a6; }")
    return "".join(parts)


_ADJ_BTN_STYLE = (
    "QPushButton { background-color: #444; color: #ddd; font-weight: bold; "
    "padding: 1px 4px; border-radius: 2px; min-width: 16px; max-width: 20px; font-size: 11px; }"
    "QPushButton:hover { background-color: #666; }"
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        title = f"{t('app_title_prefix')}{APP_VERSION}"
        if is_debug_enabled():
            title += " [debug mode]"
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(resource_path(os.path.join('image', IMAGE_ICON))))
        self.setMinimumSize(800, 640)
        self.resize(800, 600)

        self._pkg_files = []
        self._config_path = os.path.join(app_dir(), 'config.json')
        self._app_dir = app_dir()
        self._bak_dir = os.path.join(self._app_dir, 'bak')
        self._cache_dir = os.path.join(self._app_dir, 'cache')
        self._search_thread = None
        self._search_stage = None
        self._search_candidates_count = 0
        self._apply_thread = None
        self._apply_msg_queue = None
        self._apply_poll_timer = None
        self._found_results = []
        self._card_result = None
        self._avatar_result = None
        self._card_cache_path = None
        self._avatar_cache_path = None
        self._target_pkg_info = {}
        self._last_preview_source = None

        # 交互状态
        self._current_steps = None
        self._current_step_index = 0
        self._game_hwnd = 0
        self._manual_game_hwnd = 0
        self._manual_process_name = ''
        self._manual_pid = 0
        self._manual_window_title = ''
        self._current_workflow_name = ''

        # 退出确认开关（_load_config 中会从配置读取覆盖）
        self._confirm_on_exit = True

        # 窗口捕获
        self._window_capture = WindowCapture(self)
        self._window_capture.on_captured = self._on_window_captured
        self._window_capture.on_cancel = self._on_capture_cancelled

        self._setup_ui()
        debug_log("UI初始化完成")
        self._load_config()

        self._game_check_timer = QTimer(self)
        self._game_check_timer.timeout.connect(self._check_game_process)
        self._game_check_timer.start(3000)
        debug_log("游戏进程监测定时器已启动(3秒间隔)")

    # ==================== UI 构建 ====================

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(6)

        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #555;
                border-radius: 6px;
                margin-top: 8px;
                padding-top: 14px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 6px;
            }
            QTabWidget::pane {
                border: 1px solid #555;
                border-radius: 4px;
            }
            QTabBar::tab {
                padding: 6px 16px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            QTabBar::tab:selected {
                background: #3a3a3a;
                color: #fff;
            }
            QProgressBar {
                border: 1px solid #555;
                border-radius: 4px;
                text-align: center;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2ecc71);
                border-radius: 3px;
            }
        """)

        top_layout = QHBoxLayout()
        top_layout.setSpacing(6)

        lbl_dir = QLabel(t('game_dir_label'))
        lbl_dir.setStyleSheet("font-weight: bold; font-size: 12px;")
        top_layout.addWidget(lbl_dir)
        self.game_path_edit = QLineEdit()
        self.game_path_edit.setPlaceholderText(t('placeholder_game_path'))
        self.game_path_edit.setReadOnly(True)
        self.game_path_edit.setStyleSheet("padding: 4px; border-radius: 4px;")
        top_layout.addWidget(self.game_path_edit, 1)

        btn_browse = QPushButton(t('btn_select_dir'))
        btn_browse.setStyleSheet(_btn_style("#34495e", "#2c3e50"))
        btn_browse.clicked.connect(self._browse_game_path)
        top_layout.addWidget(btn_browse)

        self.btn_restore = QPushButton(t('btn_restore'))
        self.btn_restore.setFixedWidth(70)
        self.btn_restore.setStyleSheet(_btn_style("#e74c3c", "#c0392b", font_size="13px", pressed="#a93226"))
        self.btn_restore.clicked.connect(self._restore_backup)
        top_layout.addWidget(self.btn_restore)

        btn_tutorial = QPushButton(t('btn_tutorial'))
        btn_tutorial.setFixedWidth(70)
        btn_tutorial.setStyleSheet(_btn_style("#3498db", "#2980b9", padding="6px 12px"))
        btn_tutorial.clicked.connect(lambda: show_tutorial_dialog(self))
        top_layout.addWidget(btn_tutorial)

        btn_faq = QPushButton(t('btn_faq'))
        btn_faq.setFixedWidth(70)
        btn_faq.setStyleSheet(_btn_style("#e67e22", "#d35400", padding="6px 12px"))
        btn_faq.clicked.connect(lambda: show_faq_dialog(self))
        top_layout.addWidget(btn_faq)

        btn_settings = QPushButton(t('btn_settings'))
        btn_settings.setFixedWidth(70)
        btn_settings.setStyleSheet(_btn_style("#9b59b6", "#8e44ad", padding="6px 12px"))
        btn_settings.clicked.connect(self._show_settings_dialog)
        top_layout.addWidget(btn_settings)

        main_layout.addLayout(top_layout)

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self._setup_search_tab()
        self._setup_image_edit_tab()
        self._setup_apply_tab()

        self.tabs.setTabEnabled(1, False)
        self.tabs.setTabEnabled(2, False)

        self.status_label = QLabel(t('status_ready'))
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(18)
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.progress_bar, 1)
        bottom_layout.addWidget(self.status_label, 1)
        main_layout.addLayout(bottom_layout)

    def _create_slider_row(self, label_text, val_min, val_max, default_val, val_min_width=28):
        """创建带 +/-/R 按钮的滑块行，返回 (slider, val_label, row_layout)"""
        slider = QSlider(Qt.Horizontal)
        slider.setRange(val_min, val_max)
        slider.setValue(default_val)

        # 滑块拖动时在鼠标位置显示当前值的气泡提示
        def _show_value_tooltip(value):
            from PyQt5.QtWidgets import QToolTip
            # 在滑块手柄位置显示气泡
            # slider.rect() 中心高度，水平位置按值占比估算
            slider_rect = slider.rect()
            if val_max > val_min:
                ratio = (value - val_min) / (val_max - val_min)
            else:
                ratio = 0.5
            handle_x = int(slider_rect.x() + ratio * slider_rect.width())
            handle_y = slider.rect().y() - 10
            pos = slider.mapToGlobal(QPoint(handle_x, handle_y))
            QToolTip.showText(pos, str(value), slider)

        slider.sliderMoved.connect(_show_value_tooltip)

        row = QHBoxLayout()
        row.addWidget(QLabel(label_text))
        val_label = QLabel(str(default_val))
        val_label.setMinimumWidth(val_min_width)
        row.addWidget(val_label)
        row.addStretch()

        btn_reset = QPushButton("R")
        btn_reset.setStyleSheet(_ADJ_BTN_STYLE)
        btn_reset.setToolTip(t('tooltip_reset_default'))
        btn_reset.clicked.connect(lambda: slider.setValue(default_val))
        row.addWidget(btn_reset)

        btn_minus = QPushButton("-")
        btn_minus.setStyleSheet(_ADJ_BTN_STYLE)
        btn_minus.clicked.connect(lambda: slider.setValue(slider.value() - 1))
        row.addWidget(btn_minus)

        btn_plus = QPushButton("+")
        btn_plus.setStyleSheet(_ADJ_BTN_STYLE)
        btn_plus.clicked.connect(lambda: slider.setValue(slider.value() + 1))
        row.addWidget(btn_plus)

        return slider, val_label, row

    def _setup_search_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        mode_group = QGroupBox(t('group_search_mode'))
        mode_layout = QHBoxLayout()
        self.radio_quick = QRadioButton(t('radio_quick'))
        self.radio_deep = QRadioButton(t('radio_full'))
        self.radio_quick.setChecked(True)
        mode_btn_group = QButtonGroup(self)
        mode_btn_group.addButton(self.radio_quick)
        mode_btn_group.addButton(self.radio_deep)
        mode_layout.addWidget(self.radio_quick)
        mode_layout.addWidget(self.radio_deep)
        mode_layout.addWidget(QLabel(t('label_quick_n')))
        self.quick_n_spin = QSpinBox()
        self.quick_n_spin.setRange(1, 20)
        self.quick_n_spin.setValue(2)
        mode_layout.addWidget(self.quick_n_spin)
        mode_layout.addStretch()
        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)

        btn_layout = QHBoxLayout()
        self.btn_scan = QPushButton(t('btn_scan'))
        self.btn_scan.setStyleSheet(_btn_style("#34495e", "#2c3e50", padding="6px 14px"))
        self.btn_scan.clicked.connect(self._scan_pkg_files)
        btn_layout.addWidget(self.btn_scan)
        self.btn_search = QPushButton(t('btn_search'))
        self.btn_search.setEnabled(False)
        self.btn_search.setStyleSheet(_btn_style("#27ae60", "#219a52", padding="6px 14px", disabled=True))
        self.btn_search.clicked.connect(self._do_search)
        btn_layout.addWidget(self.btn_search)
        self.btn_stop = QPushButton(t('btn_stop'))
        self.btn_stop.setEnabled(False)
        self.btn_stop.setStyleSheet(_btn_style("#e74c3c", "#c0392b", padding="6px 14px", disabled=True))
        self.btn_stop.clicked.connect(self._stop_search)
        btn_layout.addWidget(self.btn_stop)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        self.search_log = QPlainTextEdit()
        self.search_log.setReadOnly(True)
        self.search_log.setMaximumHeight(80)
        layout.addWidget(self.search_log)

        self.result_table = QTableWidget()
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels([t('col_pkg'), t('col_type'), t('col_name'), t('col_usage')])
        self.result_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.result_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.result_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.result_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(self.result_table)

        assign_layout = QHBoxLayout()
        btn_assign_card = QPushButton(t('btn_assign_card'))
        btn_assign_card.clicked.connect(self._assign_card)
        assign_layout.addWidget(btn_assign_card)
        btn_assign_avatar = QPushButton(t('btn_assign_avatar'))
        btn_assign_avatar.clicked.connect(self._assign_avatar)
        assign_layout.addWidget(btn_assign_avatar)
        self.assigned_label = QLabel(t('assigned_label').format(t('not_selected'), t('not_selected')))
        self.assigned_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        assign_layout.addWidget(self.assigned_label, 1)
        layout.addLayout(assign_layout)

        self.tabs.addTab(tab, t('tab_search'))

    def _setup_image_edit_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        import_layout = QHBoxLayout()
        self.btn_import_card = QPushButton(t('btn_import_card'))
        self.btn_import_card.setEnabled(False)
        self.btn_import_card.setStyleSheet(_btn_style("#3498db", "#2980b9", padding="8px", font_size="13px", disabled=True))
        self.btn_import_card.clicked.connect(self._import_card_image)
        import_layout.addWidget(self.btn_import_card)

        self.btn_import_avatar = QPushButton(t('btn_import_avatar'))
        self.btn_import_avatar.setEnabled(False)
        self.btn_import_avatar.setStyleSheet(_btn_style("#9b59b6", "#8e44ad", padding="8px", font_size="13px", disabled=True))
        self.btn_import_avatar.clicked.connect(self._import_avatar_image)
        import_layout.addWidget(self.btn_import_avatar)

        small_btn_style = (
            "QPushButton { background-color: #555; color: white; font-weight: bold; "
            "padding: 6px 10px; border-radius: 4px; font-size: 12px; }"
            "QPushButton:hover { background-color: #777; }"
        )
        self.btn_reset_pos = QPushButton(t('btn_reset_pos'))
        self.btn_reset_pos.setStyleSheet(small_btn_style)
        self.btn_reset_pos.clicked.connect(self._reset_position)
        import_layout.addWidget(self.btn_reset_pos)

        self.btn_reset_img = QPushButton(t('btn_reset_img'))
        self.btn_reset_img.setStyleSheet(small_btn_style)
        self.btn_reset_img.clicked.connect(self._reset_adjustments)
        import_layout.addWidget(self.btn_reset_img)

        import_layout.addStretch()
        layout.addLayout(import_layout)

        edit_layout = QHBoxLayout()
        left_panel = QVBoxLayout()
        self.crop_widget = ImageCropWidget(CARD_WIDTH, CARD_HEIGHT)
        self.crop_widget._zoom_callback = lambda z: self.zoom_slider.setValue(int(z * 100))
        self.crop_widget._preview_callback = self._update_preview
        left_panel.addWidget(self.crop_widget, 1)

        self.btn_next_step = QPushButton(t('btn_next_step'))
        self.btn_next_step.setEnabled(False)
        self.btn_next_step.setStyleSheet(_btn_style("#27ae60", "#219a52", padding="10px", font_size="14px", disabled=True))
        self.btn_next_step.setMaximumWidth(600)
        self.btn_next_step.clicked.connect(self._on_next_step)
        next_row = QHBoxLayout()
        next_row.addStretch(1)
        next_row.addWidget(self.btn_next_step, 100)
        next_row.addStretch(1)
        left_panel.addLayout(next_row)

        self.tip_label = QLabel(t('tip_must_enter_guild'))
        self.tip_label.setAlignment(Qt.AlignCenter)
        left_panel.addWidget(self.tip_label)

        edit_layout.addLayout(left_panel, 3)

        ctrl_panel = QVBoxLayout()
        self.edit_type_label = QLabel(t('edit_type_none'))
        self.edit_type_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        ctrl_panel.addWidget(self.edit_type_label)

        # 亮度
        self.brightness_slider, self.brightness_val_label, bright_row = self._create_slider_row(
            t('label_brightness'), -100, 100, 0)
        self.brightness_slider.valueChanged.connect(self._on_brightness_changed)
        ctrl_panel.addLayout(bright_row)
        ctrl_panel.addWidget(self.brightness_slider)

        # 对比度
        self.contrast_slider, self.contrast_val_label, contrast_row = self._create_slider_row(
            t('label_contrast'), -100, 100, 0)
        self.contrast_slider.valueChanged.connect(self._on_contrast_changed)
        ctrl_panel.addLayout(contrast_row)
        ctrl_panel.addWidget(self.contrast_slider)

        # 饱和度
        self.saturation_slider, self.saturation_val_label, sat_row = self._create_slider_row(
            t('label_saturation'), -100, 100, 0)
        self.saturation_slider.valueChanged.connect(self._on_saturation_changed)
        ctrl_panel.addLayout(sat_row)
        ctrl_panel.addWidget(self.saturation_slider)

        # 色温
        self.temperature_slider, self.temperature_val_label, temp_row = self._create_slider_row(
            t('label_temperature'), -100, 100, 0)
        self.temperature_slider.valueChanged.connect(self._on_temperature_changed)
        ctrl_panel.addLayout(temp_row)
        ctrl_panel.addWidget(self.temperature_slider)

        # 缩放
        self.zoom_slider, self.zoom_val_label, zoom_row = self._create_slider_row(
            t('label_zoom'), 1, 300, 100, val_min_width=36)
        self.zoom_val_label.setText("100%")
        self.zoom_slider.valueChanged.connect(self._on_zoom_changed)
        ctrl_panel.addLayout(zoom_row)
        ctrl_panel.addWidget(self.zoom_slider)

        self.btn_crop_ok = QPushButton(t('btn_crop_ok'))
        self.btn_crop_ok.setEnabled(False)
        self.btn_crop_ok.setStyleSheet(_btn_style("#27ae60", "#219a52", padding="8px", disabled=True))
        self.btn_crop_ok.clicked.connect(self._confirm_crop)
        ctrl_panel.addWidget(self.btn_crop_ok)

        self.thumb_label = ClickableLabel(t('thumb_label'))
        self.thumb_label.setAlignment(Qt.AlignCenter)
        self.thumb_label.setMinimumSize(THUMB_MIN_SIZE, THUMB_MIN_SIZE)
        self.thumb_label.setMaximumSize(THUMB_MAX_SIZE, THUMB_MAX_SIZE)
        self.thumb_label.setStyleSheet("border: 1px solid #555; background: #333;")
        self.thumb_label.setToolTip(t('tooltip_click_preview'))
        self.thumb_label.setCursor(Qt.PointingHandCursor)
        self.thumb_label.clicked.connect(self._show_preview_dialog)
        ctrl_panel.addWidget(self.thumb_label)
        ctrl_panel.addStretch()

        # 控制面板限宽：最大化时不再无限拉伸滑块和按钮，多余空间留给裁剪区
        ctrl_widget = QWidget()
        ctrl_widget.setLayout(ctrl_panel)
        ctrl_widget.setMaximumWidth(360)
        edit_layout.addWidget(ctrl_widget, 1)
        layout.addLayout(edit_layout, 1)

        self.tabs.addTab(tab, t('tab_edit'))
        self._current_edit_type = None

    def _setup_apply_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        game_status_layout = QHBoxLayout()
        self.game_status_label = QLabel(t('game_status_not_detected'))
        self.game_status_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 5px;")
        game_status_layout.addWidget(self.game_status_label)
        self.btn_capture_window = QPushButton(t('btn_capture_window'))
        self.btn_capture_window.setStyleSheet(_btn_style("#e67e22", "#d35400", padding="5px 10px", font_size="12px"))
        self.btn_capture_window.setCursor(Qt.PointingHandCursor)
        self.btn_capture_window.setToolTip(t('tooltip_capture'))
        self.btn_capture_window.clicked.connect(self._start_capture_window)
        game_status_layout.addWidget(self.btn_capture_window)
        game_status_layout.addStretch()
        layout.addLayout(game_status_layout)

        action_layout = QHBoxLayout()
        self.btn_start_card = QPushButton(t('btn_start_card'))
        self.btn_start_card.setEnabled(False)
        self.btn_start_card.setStyleSheet(_btn_style("#3498db", "#2980b9", padding="12px", font_size="14px", disabled=True))
        self.btn_start_card.setMaximumWidth(300)
        self.btn_start_card.clicked.connect(self._start_card_workflow)
        action_layout.addWidget(self.btn_start_card)

        self.btn_start_avatar = QPushButton(t('btn_start_avatar'))
        self.btn_start_avatar.setEnabled(False)
        self.btn_start_avatar.setStyleSheet(_btn_style("#9b59b6", "#8e44ad", padding="12px", font_size="14px", disabled=True))
        self.btn_start_avatar.setMaximumWidth(300)
        self.btn_start_avatar.clicked.connect(self._start_avatar_workflow)
        action_layout.addWidget(self.btn_start_avatar)

        self.btn_step_next = QPushButton(t('btn_step_next'))
        self.btn_step_next.setEnabled(False)
        self.btn_step_next.setStyleSheet(_btn_style("#27ae60", "#219a52", padding="12px 30px", font_size="14px", disabled=True))
        self.btn_step_next.setMaximumWidth(300)
        self.btn_step_next.clicked.connect(self._advance_step)
        action_layout.addWidget(self.btn_step_next)

        action_layout.addStretch()
        layout.addLayout(action_layout)

        self.step_browser = QTextBrowser()
        self.step_browser.setFont(QFont("Microsoft YaHei", 11))
        self.step_browser.setStyleSheet("padding: 10px;")
        self.step_browser.setOpenExternalLinks(False)
        # 限宽居中：最大化时教程文字保持可读行宽，不横贯整个窗口
        self.step_browser.setMaximumWidth(900)
        browser_row = QHBoxLayout()
        browser_row.addStretch(1)
        browser_row.addWidget(self.step_browser, 100)
        browser_row.addStretch(1)
        layout.addLayout(browser_row, 1)

        # ===== DEBUG: 窗口分辨率调试面板（仅 debug 模式显示） =====
        (self._debug_resize_group, self._debug_w_spin, self._debug_h_spin,
         self._debug_scale_spin, self._debug_btn) = create_debug_resize_panel(layout)
        self._debug_resize_group.setMaximumWidth(560)
        self._debug_btn.clicked.connect(self._debug_apply_resize)
        # ===== DEBUG END =====

        self.tabs.addTab(tab, t('tab_apply'))

    # ==================== 窗口捕获 ====================

    def _start_capture_window(self):
        self._window_capture.start(self.btn_capture_window)

    def _on_window_captured(self, hwnd, window_title, process_name, pid):
        debug_log(f"确认游戏窗口: title={window_title}, process={process_name}, pid={pid}, hwnd={hwnd}")
        self._manual_game_hwnd = hwnd
        self._manual_process_name = process_name
        self._manual_pid = pid
        self._manual_window_title = window_title
        self._game_hwnd = hwnd
        display_name = window_title if window_title != t('no_title') else process_name
        self.game_status_label.setText(t('game_status_connected').format(display_name))
        self.game_status_label.setStyleSheet(
            "font-size: 14px; font-weight: bold; padding: 5px; color: #27ae60;")
        self.btn_start_card.setEnabled(True)
        self.btn_start_avatar.setEnabled(True)
        self.btn_capture_window.setEnabled(True)
        self.btn_capture_window.setText(t('btn_capture_window'))

    def _on_capture_cancelled(self):
        self.btn_capture_window.setEnabled(True)
        self.btn_capture_window.setText(t('btn_capture_window'))
        self.btn_capture_window.setToolTip(t('tooltip_capture'))

    def _check_game_process(self):
        if self._manual_game_hwnd and HAS_WIN32:
            if user32.IsWindow(self._manual_game_hwnd):
                self._game_hwnd = self._manual_game_hwnd
                display_name = self._manual_window_title if self._manual_window_title != t('no_title') else self._manual_process_name
                self.game_status_label.setText(t('game_status_connected').format(display_name))
                self.game_status_label.setStyleSheet(
                    "font-size: 14px; font-weight: bold; padding: 5px; color: #27ae60;")
                self.btn_start_card.setEnabled(True)
                self.btn_start_avatar.setEnabled(True)
                return
            else:
                debug_log(f"手动捕获窗口已失效: hwnd={self._manual_game_hwnd}")
                self._manual_game_hwnd = 0
                self._manual_process_name = ''
                self._manual_pid = 0
                self._manual_window_title = ''
        hwnd, window_title = find_game_window()
        if hwnd:
            self._game_hwnd = hwnd
            display_name = window_title if window_title else t('window_title_default')
            debug_log(f"检测到游戏窗口: hwnd={hwnd}, title={window_title}")
            self.game_status_label.setText(t('game_status_connected').format(display_name))
            self.game_status_label.setStyleSheet(
                "font-size: 14px; font-weight: bold; padding: 5px; color: #27ae60;")
            self.btn_start_card.setEnabled(True)
            self.btn_start_avatar.setEnabled(True)
        else:
            self._game_hwnd = 0
            running = is_game_running()
            if running:
                debug_log(f"游戏进程运行中但未找到窗口: {running}")
                self.game_status_label.setText(t('game_status_running_no_window'))
                self.game_status_label.setStyleSheet(
                    "font-size: 14px; font-weight: bold; padding: 5px; color: #e67e22;")
            else:
                self.game_status_label.setText(t('game_status_not_detected'))
                self.game_status_label.setStyleSheet(
                    "font-size: 14px; font-weight: bold; padding: 5px; color: #e74c3c;")
            self.btn_start_card.setEnabled(False)
            self.btn_start_avatar.setEnabled(False)

    # ==================== 工作流 ====================

    def _on_next_step(self):
        if self._apply_thread and self._apply_thread.is_alive():
            debug_log("应用修改正在进行中，忽略重复点击")
            return
        debug_log("点击下一步: 开始应用PKG修改")
        self._apply_changes()

    def _start_card_workflow(self):
        self._start_workflow(get_card_steps(), t('workflow_card'))

    def _start_avatar_workflow(self):
        self._start_workflow(get_avatar_steps(), t('workflow_avatar'))

    def _start_workflow(self, steps, workflow_name):
        if not self._game_hwnd:
            debug_log(f"启动{workflow_name}工作流失败: 未检测到游戏窗口")
            QMessageBox.warning(self, t('tip'), t('msg_no_game_window'))
            return

        debug_log(f"启动{workflow_name}工作流, 共{len(steps)}步")
        self._current_steps = steps
        self._current_step_index = 0
        self._current_workflow_name = workflow_name
        self.step_browser.clear()
        title = t('workflow_card_title') if workflow_name == t('workflow_card') else t('workflow_avatar_title')
        self.step_browser.append(f"<h3>{title}</h3><hr>")

        self.btn_step_next.setEnabled(True)
        self.btn_start_card.setEnabled(False)
        self.btn_start_avatar.setEnabled(False)

        self._show_current_step()

    def _show_current_step(self):
        if self._current_steps is None or self._current_step_index >= len(self._current_steps):
            return

        step = self._current_steps[self._current_step_index]
        debug_log(f"工作流步骤 [{self._current_step_index+1}/{len(self._current_steps)}]: {step.get('text', '')[:50]}")

        action = step.get('action')
        if action and action[0] == 'resize':
            _, w, h, scale = action
            if self._game_hwnd:
                debug_log(f"  调整窗口: {w}x{h}@{scale}%")
                result = set_game_window_resolution(self._game_hwnd, w, h, scale)
                if result:
                    actual_w = int(w * scale / 100)
                    actual_h = int(h * scale / 100)
                    debug_log(f"  窗口调整成功: {actual_w}x{actual_h}")
                    self.step_browser.append(
                        f"<p style='font-size:10pt; color:#888;'>{t('window_resized').format(actual_w, actual_h)}</p>"
                    )
                else:
                    debug_log(f"  窗口调整失败")
                    self.step_browser.append(
                        f"<p style='font-size:10pt; color:#e74c3c;'>{t('window_resize_failed')}</p>"
                    )

        text = step['text']
        hint = step['hint']
        hint_color = step.get('hint_color', 'green')

        self.step_browser.append(
            f"<p style='font-size:13pt;'>{text}</p>"
            f"<p style='font-size:12pt; color:{hint_color};'><b>{hint}</b></p>"
            f"<hr>"
        )
        cursor = self.step_browser.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.step_browser.setTextCursor(cursor)

    def _advance_step(self):
        if self._current_steps is None:
            return

        self._current_step_index += 1

        if self._current_step_index >= len(self._current_steps):
            wf_name = getattr(self, '_current_workflow_name', '')
            debug_log(f"{wf_name}工作流完成")
            done_text = t('workflow_done_card') if wf_name == t('workflow_card') else t('workflow_done_avatar')
            self.step_browser.append(
                f"<p style='font-size:14pt; color:#27ae60;'><b>{done_text}</b></p>"
            )
            self._current_steps = None
            self.btn_step_next.setEnabled(False)
            if self._game_hwnd:
                self.btn_start_card.setEnabled(True)
                self.btn_start_avatar.setEnabled(True)
            return

        self._show_current_step()

    # ==================== 调试面板 ====================

    def _debug_apply_resize(self):
        w = self._debug_w_spin.value()
        h = self._debug_h_spin.value()
        scale = self._debug_scale_spin.value()
        success, actual_w, actual_h = apply_debug_resize(self._game_hwnd, w, h, scale)
        if success:
            self.step_browser.append(
                f"<p style='color:#27ae60;'>{t('debug_resize_log').format(actual_w, actual_h, w, h, scale)}</p>"
            )
        elif not self._game_hwnd:
            QMessageBox.warning(self, t('tip'), t('msg_no_game_window_debug'))
        else:
            self.step_browser.append(
                f"<p style='color:#e74c3c;'>{t('debug_resize_fail')}</p>"
            )

    # ==================== 配置读写 ====================

    def _load_config(self):
        try:
            if os.path.exists(self._config_path):
                with open(self._config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                debug_log(f"加载配置: {self._config_path}")
                game_path = config.get('game_path', '')
                target_pkg = config.get('target_pkg', {})
                if target_pkg:
                    self._target_pkg_info = target_pkg
                    debug_log(f"  target_pkg: {target_pkg}")
                quick_n = config.get('quick_n', 2)
                self.quick_n_spin.setValue(quick_n)
                card_result = config.get('card_result')
                avatar_result = config.get('avatar_result')
                if card_result:
                    self._card_result = card_result
                    debug_log(f"  card_result: {card_result}")
                if avatar_result:
                    self._avatar_result = avatar_result
                    debug_log(f"  avatar_result: {avatar_result}")
                if game_path and os.path.isdir(game_path):
                    self.game_path_edit.setText(game_path)
                    self.status_label.setText(t('status_loaded_config').format(game_path))
                    debug_log(f"  game_path: {game_path} (有效)")
                    self._scan_pkg_files()
                else:
                    debug_log(f"  game_path: '{game_path}' (无效或为空)")
                debug_enabled = bool(config.get('debug', False))
                self._debug_resize_group.setVisible(debug_enabled)
                debug_log(f"  debug={debug_enabled}, 调试面板={'显示' if debug_enabled else '隐藏'}")
                self._update_assigned_label()
                # 恢复上次窗口大小和位置
                geometry = config.get('window_geometry')
                if geometry and isinstance(geometry, list) and len(geometry) == 4:
                    x, y, w, h = geometry
                    # 确保窗口位置在可见屏幕范围内（避免恢复到已断开的显示器）
                    screens = QApplication.screens()
                    in_screen = False
                    for screen in screens:
                        geo = screen.availableGeometry()
                        if geo.contains(QPoint(x + w // 2, y + h // 2)):
                            in_screen = True
                            break
                    if in_screen:
                        self.setGeometry(x, y, w, h)
                        if config.get('window_maximized'):
                            self.showMaximized()
                        debug_log(f"  恢复窗口位置: x={x}, y={y}, w={w}, h={h}"
                                  f"{', 最大化' if config.get('window_maximized') else ''}")
                    else:
                        debug_log(f"  保存的窗口位置不在任何屏幕上，忽略: x={x}, y={y}")
                # 读取退出确认开关（默认开启）
                self._confirm_on_exit = bool(config.get('confirm_on_exit', True))
            else:
                debug_log("配置文件不存在，跳过加载")
                self._confirm_on_exit = True
        except Exception as e:
            debug_log(f"加载配置异常: {e}")
            self._confirm_on_exit = True

    def _save_config(self, target_pkg=None):
        try:
            config = {}
            if os.path.exists(self._config_path):
                try:
                    with open(self._config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                except Exception as e:
                    debug_log(f"读取已有配置失败，将创建新配置: {e}")
            game_path = self.game_path_edit.text().strip()
            if game_path:
                config['game_path'] = game_path
            if target_pkg is not None:
                config['target_pkg'] = target_pkg
            elif hasattr(self, '_target_pkg_info') and self._target_pkg_info:
                config['target_pkg'] = self._target_pkg_info
            config['quick_n'] = self.quick_n_spin.value()
            if self._card_result:
                config['card_result'] = self._card_result
            if self._avatar_result:
                config['avatar_result'] = self._avatar_result
            with open(self._config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            debug_log(f"配置已保存: {self._config_path}")
        except Exception as e:
            debug_log(f"保存配置异常: {e}")

    # ==================== PKG 扫描 / 搜索 ====================

    def _browse_game_path(self):
        d = QFileDialog.getExistingDirectory(self, t('msg_select_dir'))
        if d:
            debug_log(f"用户选择游戏目录: {d}")
            self.game_path_edit.setText(d)
            self._save_config()
            self._scan_pkg_files()

    def _scan_pkg_files(self):
        game_path = self.game_path_edit.text().strip()
        if not game_path:
            debug_log("_scan_pkg_files: game_path为空，跳过")
            return
        container_dir = find_container_dir(game_path)
        if container_dir is None:
            debug_log(f"_scan_pkg_files: 未找到container目录, game_path={game_path}")
            QMessageBox.warning(self, t('tip'),
                t('msg_no_container').format(game_path))
            return
        debug_log(f"_scan_pkg_files: container_dir={container_dir}")
        self._pkg_files = []
        skipped = 0
        skipped_meta = 0
        for f in os.listdir(container_dir):
            if f.lower().endswith('.pkg'):
                if f.lower() in PkgFile.EXCLUDED_PKGS:
                    skipped_meta += 1
                    continue
                full_path = os.path.join(container_dir, f)
                try:
                    fsize = os.path.getsize(full_path)
                    if fsize > PkgFile.MAX_PKG_SIZE:
                        skipped += 1
                        continue
                except OSError:
                    continue
                self._pkg_files.append(full_path)
        self._pkg_files.sort()
        workers = PkgSearchThread.calc_workers(self._pkg_files)
        debug_log(f"_scan_pkg_files: 找到{len(self._pkg_files)}个PKG, 跳过{skipped}个>1G, {skipped_meta}个meta, 线程数={workers}")
        self.btn_search.setEnabled(len(self._pkg_files) > 0)
        self.search_log.appendPlainText(
            t('msg_scan_done').format(len(self._pkg_files), skipped, skipped_meta, workers)
        )
        self.status_label.setText(t('status_scanned').format(len(self._pkg_files)))
        self._save_config()

    def _do_search(self):
        asset_type = "Texture2D"
        asset_name = "personalzone_player_bg"
        if not self._pkg_files:
            QMessageBox.warning(self, t('tip'), t('msg_no_pkg_scanned'))
            return
        self.result_table.setRowCount(0)
        self.search_log.clear()
        self._found_results = []
        self.progress_bar.setValue(0)
        workers = PkgSearchThread.calc_workers(self._pkg_files)
        mode_str = t('radio_quick') if self.radio_quick.isChecked() else t('radio_full')
        debug_log(f"开始PKG搜索: 模式={mode_str}, 类型={asset_type}, 名称={asset_name}, PKG数={len(self._pkg_files)}, 线程={workers}")
        self.search_log.appendPlainText(
            t('msg_search_start').format(mode_str, asset_type, asset_name, len(self._pkg_files), workers)
        )
        self.btn_search.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.btn_scan.setEnabled(False)
        self.status_label.setText(t('status_searching'))
        # 快速模式：优先尝试从上次记录的pkg路径预检测，命中则跳过全量扫描
        if self.radio_quick.isChecked():
            candidates = self._get_cached_quick_pkgs()
            if candidates:
                debug_log(f"预查找: 候选{len(candidates)}个pkg: {[os.path.basename(p) for p in candidates]}")
                self.search_log.appendPlainText(
                    t('msg_pre_search').format(len(candidates))
                )
                self._start_search_thread(candidates, asset_type, asset_name, workers, stage='pre')
                return
        self._start_search_thread(self._pkg_files, asset_type, asset_name, workers, stage='full')

    def _get_cached_quick_pkgs(self):
        """从config读取上次快速查找使用的pkg路径（去重、过滤存在的）"""
        candidates = []
        seen = set()
        try:
            if os.path.exists(self._config_path):
                with open(self._config_path, 'r', encoding='utf-8') as f:
                    cfg = json.load(f)
                for key in ('card_result', 'avatar_result'):
                    r = cfg.get(key) or {}
                    p = r.get('pkg_path', '')
                    if not p or p in seen or not os.path.isfile(p):
                        continue
                    try:
                        if os.path.getsize(p) > PkgFile.MAX_PKG_SIZE:
                            continue
                    except OSError:
                        continue
                    if os.path.basename(p).lower() in PkgFile.EXCLUDED_PKGS:
                        continue
                    candidates.append(p)
                    seen.add(p)
        except Exception as e:
            debug_log(f"读取缓存的PKG路径失败: {e}")
        return candidates

    def _start_search_thread(self, pkg_files, asset_type, asset_name, workers, stage):
        """启动PkgSearchThread，stage标记预检测/全量"""
        self._search_stage = stage
        self._search_candidates_count = len(pkg_files)
        self._search_thread = PkgSearchThread(pkg_files, asset_type, asset_name, max_workers=workers)
        self._search_thread.progress.connect(self._on_search_progress)
        self._search_thread.found.connect(self._on_search_found)
        self._search_thread.finished.connect(self._on_search_finished)
        self._search_thread.start()

    def _stop_search(self):
        if self._search_thread and self._search_thread.isRunning():
            self._search_thread.stop()
            debug_log("用户停止搜索")
            self.search_log.appendPlainText(t('msg_search_stopped'))

    def _on_search_progress(self, current, total, msg):
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)
        self.status_label.setText(t('status_searching_progress').format(current, total, msg))

    def _on_search_found(self, pkg_path, class_name, asset_name, path_id, entry_index):
        if asset_name.lower() in EXCLUDED_ASSET_NAMES:
            debug_log(f"搜索排除废弃资源: {asset_name} in {os.path.basename(pkg_path)}")
            self.search_log.appendPlainText(t('msg_search_excluded').format(asset_name, os.path.basename(pkg_path)))
            return
        debug_log(f"搜索找到: {asset_name} ({class_name}) in {os.path.basename(pkg_path)} 条目#{entry_index}")
        row = self.result_table.rowCount()
        self.result_table.setRowCount(row + 1)
        self.result_table.setItem(row, 0, QTableWidgetItem(os.path.basename(pkg_path)))
        self.result_table.setItem(row, 1, QTableWidgetItem(class_name))
        self.result_table.setItem(row, 2, QTableWidgetItem(asset_name))
        self.result_table.setItem(row, 3, QTableWidgetItem(""))
        self._found_results.append({
            'pkg_path': pkg_path, 'class_name': class_name,
            'asset_name': asset_name, 'path_id': path_id, 'entry_index': entry_index,
        })
        self.search_log.appendPlainText(
            t('msg_search_found').format(asset_name, class_name, os.path.basename(pkg_path), entry_index)
        )
        if self.radio_quick.isChecked():
            n = self.quick_n_spin.value()
            unique_pkgs = set(r['pkg_path'] for r in self._found_results)
            if len(unique_pkgs) >= n:
                if self._search_thread and self._search_thread.isRunning():
                    self._search_thread.stop()
                    debug_log(f"快速查找: 已找到{n}个数据包，停止")
                    self.search_log.appendPlainText(t('msg_quick_stop').format(n))

    def _on_search_finished(self, found_count, scanned_count):
        self.btn_search.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.btn_scan.setEnabled(True)
        self.progress_bar.setValue(0)
        actual_found = len(self._found_results)
        debug_log(f"搜索完成(stage={self._search_stage}): 扫描{scanned_count}个PKG, 找到{actual_found}个有效匹配")
        # 预查找阶段：命中目标则直接应用，否则回退全量扫描
        if self._search_stage == 'pre':
            n = self.quick_n_spin.value()
            unique_pkgs = {r['pkg_path'] for r in self._found_results}
            target = min(n, self._search_candidates_count)
            if actual_found > 0 and len(unique_pkgs) >= target:
                debug_log(f"预查找命中: unique={len(unique_pkgs)}/{target}")
                self.search_log.appendPlainText(t('msg_pre_search_hit'))
                self._apply_search_results(scanned_count, actual_found)
                return
            debug_log(f"预查找未命中(unique={len(unique_pkgs)}/{target})，回退全量")
            self.search_log.appendPlainText(t('msg_pre_search_miss'))
            self.btn_search.setEnabled(False)
            self.btn_stop.setEnabled(True)
            self.btn_scan.setEnabled(False)
            self.status_label.setText(t('status_full_searching'))
            workers = PkgSearchThread.calc_workers(self._pkg_files)
            self._start_search_thread(self._pkg_files, "Texture2D", "personalzone_player_bg", workers, stage='full')
            return
        self._apply_search_results(scanned_count, actual_found)

    def _apply_search_results(self, scanned_count, actual_found):
        """应用搜索结果：自动分配名片/头像、保存配置、提示用户"""
        self.status_label.setText(t('status_search_done').format(scanned_count, actual_found))
        if actual_found > 0:
            first_result = self._found_results[0]
            pkg_path = first_result['pkg_path']
            self._target_pkg_info = {
                'name': os.path.basename(pkg_path), 'path': pkg_path,
                'asset_name': first_result['asset_name'],
            }
            self._save_config()
            self._auto_assign()
            QMessageBox.information(self, t('tip'),
                t('msg_search_complete').format(actual_found))
            self.tabs.setCurrentIndex(1)
        else:
            self.tabs.setTabEnabled(1, False)
            self.tabs.setTabEnabled(2, False)
            QMessageBox.information(self, t('tip'),
                t('msg_search_no_result').format(scanned_count))

    def _auto_assign(self):
        if len(self._found_results) >= 1:
            self._card_result = self._found_results[0]
            self._update_table_assign(0, t('workflow_card'))
            debug_log(f"自动分配名片: {self._card_result['asset_name']}")
        if len(self._found_results) >= 2:
            self._avatar_result = self._found_results[1]
            self._update_table_assign(1, t('workflow_avatar'))
            debug_log(f"自动分配头像: {self._avatar_result['asset_name']}")
        self._update_assigned_label()
        self._save_config()
        self.btn_import_card.setEnabled(self._card_result is not None)
        self.btn_import_avatar.setEnabled(self._avatar_result is not None)
        if self._found_results:
            self.tabs.setTabEnabled(1, True)
            self.tabs.setTabEnabled(2, False)
        # 检查资源编号是否超过12，超过则提示用户
        if self._card_result:
            self._check_asset_index_hint(self._card_result['asset_name'])
        if self._avatar_result:
            self._check_asset_index_hint(self._avatar_result['asset_name'])

    def _assign_card(self):
        result = self._get_selected_result()
        if result:
            self._card_result = result
            debug_log(f"手动分配名片: {result['asset_name']}")
            self._update_table_assign(self.result_table.currentRow(), t('workflow_card'))
            self._update_assigned_label()
            self._save_config()
            self.btn_import_card.setEnabled(True)
            self._check_asset_index_hint(result['asset_name'])

    def _assign_avatar(self):
        result = self._get_selected_result()
        if result:
            self._avatar_result = result
            debug_log(f"手动分配头像: {result['asset_name']}")
            self._update_table_assign(self.result_table.currentRow(), t('workflow_avatar'))
            self._update_assigned_label()
            self._save_config()
            self.btn_import_avatar.setEnabled(True)
            self._check_asset_index_hint(result['asset_name'])

    def _update_table_assign(self, row, assign_type):
        if 0 <= row < self.result_table.rowCount():
            self.result_table.setItem(row, 3, QTableWidgetItem(assign_type))

    def _update_assigned_label(self):
        card_name = self._card_result['asset_name'] if self._card_result else t('not_selected')
        avatar_name = self._avatar_result['asset_name'] if self._avatar_result else t('not_selected')
        self.assigned_label.setText(t('assigned_label').format(card_name, avatar_name))

    def _check_asset_index_hint(self, asset_name):
        """检查资源名末尾数字是否超过12，超过则显示提示"""
        match = re.search(r'(\d+)$', asset_name)
        if match and int(match.group(1)) > 12:
            QMessageBox.information(self, t('tip'), t('msg_asset_index_high'))

    def _get_selected_result(self):
        rows = self.result_table.selectionModel().selectedRows()
        if not rows:
            QMessageBox.warning(self, t('tip'), t('msg_select_result'))
            return None
        row = rows[0].row()
        if row < len(self._found_results):
            return self._found_results[row]
        return None

    # ==================== 图片编辑 ====================

    def _import_card_image(self):
        in_path, _ = QFileDialog.getOpenFileName(
            self, t('file_select_card'), "", t('file_filter_image'))
        if in_path:
            debug_log(f"导入名片图片: {in_path}")
            self._current_edit_type = 'card'
            self._load_image_to_editor(in_path, CARD_WIDTH, CARD_HEIGHT)
            self.edit_type_label.setText(t('edit_type_card').format(CARD_WIDTH, CARD_HEIGHT))
            self.btn_crop_ok.setEnabled(True)

    def _import_avatar_image(self):
        in_path, _ = QFileDialog.getOpenFileName(
            self, t('file_select_avatar'), "", t('file_filter_image'))
        if in_path:
            debug_log(f"导入头像图片: {in_path}")
            self._current_edit_type = 'avatar'
            self._load_image_to_editor(in_path, AVATAR_WIDTH, AVATAR_HEIGHT)
            self.edit_type_label.setText(t('edit_type_avatar').format(AVATAR_WIDTH, AVATAR_HEIGHT))
            self.btn_crop_ok.setEnabled(True)

    def _load_image_to_editor(self, image_path, target_w, target_h):
        debug_log(f"加载图片到编辑器: path={image_path}, target={target_w}x{target_h}")
        try:
            pil_img = Image.open(image_path)
        except ImportError:
            debug_log(f"Image.open ImportError, 尝试BytesIO回退: {image_path}")
            try:
                from PIL import Image as _Img
                import io as _io
                with open(image_path, 'rb') as _f:
                    raw = _f.read()
                pil_img = _Img.open(_io.BytesIO(raw))
                pil_img.load()
                debug_log(f"BytesIO回退成功: {image_path}")
            except Exception as e2:
                debug_log(f"BytesIO回退也失败: {e2}")
                QMessageBox.critical(self, t('msg_image_load_title'),
                    t('msg_image_load_failed').format(image_path, e2))
                return
        except Exception as e:
            debug_log(f"图片加载失败: {e}")
            QMessageBox.critical(self, t('msg_image_load_title'),
                t('msg_image_load_failed').format(image_path, e))
            return
        try:
            debug_log(f"图片原始: size={pil_img.size}, mode={pil_img.mode}, format={pil_img.format}")
            if pil_img.mode != 'RGBA':
                pil_img = pil_img.convert('RGBA')
                debug_log(f"图片已转换为RGBA")
            data = pil_img.tobytes()
            qimg = QImage(data, pil_img.width, pil_img.height, pil_img.width * 4, QImage.Format_RGBA8888)
            pixmap = QPixmap.fromImage(qimg)
            if pixmap.isNull():
                debug_log(f"QPixmap为空，图片数据无效: {image_path}")
                QMessageBox.critical(self, t('msg_image_load_title'),
                    t('msg_image_invalid').format(image_path))
                return
            self.crop_widget.target_w = target_w
            self.crop_widget.target_h = target_h
            self.crop_widget.aspect_ratio = target_w / target_h
            self.crop_widget.set_image(pixmap)
            self.brightness_slider.setValue(0)
            self.contrast_slider.setValue(0)
            self.zoom_slider.setValue(100)
            self.brightness_val_label.setText("0")
            self.contrast_val_label.setText("0")
            self.zoom_val_label.setText("100%")
            self.tabs.setCurrentIndex(1)
            debug_log(f"图片加载到编辑器成功: {pil_img.width}x{pil_img.height}")
        except Exception as e:
            debug_log(f"图片处理失败: {e}")
            QMessageBox.critical(self, t('msg_image_process_title'),
                t('msg_image_process_failed').format(image_path, e))

    def _on_brightness_changed(self, val):
        self.brightness_val_label.setText(str(val))
        self.crop_widget.set_brightness(val)

    def _on_contrast_changed(self, val):
        self.contrast_val_label.setText(str(val))
        self.crop_widget.set_contrast(val)

    def _on_saturation_changed(self, val):
        self.saturation_val_label.setText(str(val))
        self.crop_widget.set_saturation(val)

    def _on_temperature_changed(self, val):
        self.temperature_val_label.setText(str(val))
        self.crop_widget.set_temperature(val)

    def _on_zoom_changed(self, val):
        self.zoom_val_label.setText(f"{val}%")
        self.crop_widget.set_zoom(val / 100.0)

    def _reset_position(self):
        self.crop_widget.reset_position()
        self.zoom_slider.blockSignals(True)
        self.zoom_slider.setValue(100)
        self.zoom_slider.blockSignals(False)
        self.zoom_val_label.setText("100%")

    def _reset_adjustments(self):
        self.brightness_slider.setValue(0)
        self.contrast_slider.setValue(0)
        self.saturation_slider.setValue(0)
        self.temperature_slider.setValue(0)
        self.crop_widget.reset_adjustments()

    def _update_preview(self, pixmap):
        if pixmap:
            self._last_preview_source = pixmap
            scaled = pixmap.scaled(self.thumb_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            draw_preview_border(scaled)
            self.thumb_label.setPixmap(scaled)
        self._update_preview_dialog()

    def _show_preview_dialog(self):
        if hasattr(self, '_preview_dialog') and self._preview_dialog is not None and self._preview_dialog.isVisible():
            self._preview_dialog.raise_()
            self._update_preview_dialog()
            return
        self._preview_dialog = QDialog(self, Qt.Window)
        self._preview_dialog.setWindowTitle(t('preview_title'))
        self._preview_dialog.setStyleSheet("background-color: #2B2B2B;")
        self._preview_dialog.setWindowFlags(self._preview_dialog.windowFlags() | Qt.WindowMinMaxButtonsHint)
        layout = QVBoxLayout(self._preview_dialog)
        self._preview_dialog_label = QLabel()
        self._preview_dialog_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._preview_dialog_label)
        # 彩蛋提示文本（仅在未载入图片的彩蛋状态下显示）
        self._preview_hint_label = QLabel(t('easter_egg_hint'))
        self._preview_hint_label.setAlignment(Qt.AlignCenter)
        self._preview_hint_label.setStyleSheet("color: #aaaaaa; font-size: 12px; padding: 4px;")
        self._preview_hint_label.hide()
        layout.addWidget(self._preview_hint_label)
        btn_close = QPushButton(t('close'))
        btn_close.setStyleSheet(_btn_style("#555", "#777", padding="6px 20px"))
        btn_close.clicked.connect(self._preview_dialog.close)
        layout.addWidget(btn_close, alignment=Qt.AlignCenter)
        self._preview_dialog.show()
        if self.crop_widget.has_image():
            self._update_preview_dialog()
        else:
            self._show_easter_egg()

    def _show_easter_egg(self):
        """未载入任何图片时点击预览触发的彩蛋：展示 Easteregg.jpg + 提示文本"""
        debug_log("预览彩蛋触发: 未载入任何图片")
        img_path = resource_path(os.path.join('image', IMAGE_EASTEREGG))
        if os.path.exists(img_path):
            pix = QPixmap(img_path)
            if not pix.isNull():
                # 与正常预览一致的适屏缩放（不超过图片原始尺寸）
                screen = QApplication.primaryScreen()
                if screen is not None:
                    screen_geo = screen.geometry()
                    max_w = min(pix.width(), screen_geo.width() - 100)
                    max_h = min(pix.height(), screen_geo.height() - 100)
                else:
                    # 回退：使用固定最大尺寸，避免在无屏幕环境下崩溃
                    max_w = min(pix.width(), 1600)
                    max_h = min(pix.height(), 900)
                scaled = pix.scaled(max_w, max_h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self._preview_dialog_label.setPixmap(scaled)
            else:
                debug_log(f"预览彩蛋图片无效: {img_path}")
        else:
            debug_log(f"预览彩蛋图片不存在: {img_path}")
        self._preview_hint_label.setText(t('easter_egg_hint'))
        self._preview_hint_label.show()
        self._preview_dialog.setWindowTitle(t('preview_title'))

    def _update_preview_dialog(self):
        if not hasattr(self, '_preview_dialog') or self._preview_dialog is None or not self._preview_dialog.isVisible():
            return
        cropped = self.crop_widget.get_cropped_image()
        if cropped is None:
            return
        # 有真实预览内容时隐藏彩蛋提示（彩蛋 -> 正常预览的切换）
        hint = getattr(self, '_preview_hint_label', None)
        if hint is not None:
            hint.hide()
        data = cropped.tobytes()
        w, h = cropped.width, cropped.height
        qimg = QImage(data, w, h, w * 4, QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(qimg)
        # primaryScreen() 在某些场景（远程桌面断开、无显示器等）可能返回 None
        screen = QApplication.primaryScreen()
        if screen is not None:
            screen_geo = screen.geometry()
            max_w = min(w, screen_geo.width() - 100)
            max_h = min(h, screen_geo.height() - 100)
        else:
            # 回退：使用固定最大尺寸，避免在无屏幕环境下崩溃
            max_w = min(w, 1600)
            max_h = min(h, 900)
        scaled = pixmap.scaled(max_w, max_h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        draw_preview_border(scaled)
        self._preview_dialog_label.setPixmap(scaled)
        self._preview_dialog.setWindowTitle(t('preview_title_size').format(w, h))

    def _confirm_crop(self):
        cropped = self.crop_widget.get_cropped_image()
        if cropped is None:
            debug_log("裁剪确认: 没有可裁剪的图片")
            QMessageBox.warning(self, t('tip'), t('msg_no_crop_image'))
            return
        os.makedirs(self._cache_dir, exist_ok=True)
        if self._current_edit_type == 'card':
            self._card_cache_path = os.path.join(self._cache_dir, "card_custom.png")
            cropped.save(self._card_cache_path, 'PNG')
            debug_log(f"名片裁剪结果已保存: {self._card_cache_path} ({cropped.width}x{cropped.height})")
            self.search_log.appendPlainText(t('log_card_saved'))
        elif self._current_edit_type == 'avatar':
            self._avatar_cache_path = os.path.join(self._cache_dir, "avatar_custom.png")
            cropped.save(self._avatar_cache_path, 'PNG')
            debug_log(f"头像裁剪结果已保存: {self._avatar_cache_path} ({cropped.width}x{cropped.height})")
            self.search_log.appendPlainText(t('log_avatar_saved'))
        data = cropped.tobytes()
        qimg = QImage(data, cropped.width, cropped.height, cropped.width * 4, QImage.Format_RGBA8888)
        self._update_preview(QPixmap.fromImage(qimg))
        self._update_next_button()
        type_name = t('workflow_card') if self._current_edit_type == 'card' else t('workflow_avatar')
        QMessageBox.information(self, t('tip'),
            t('msg_crop_done').format(type_name, cropped.width, cropped.height))

    def _update_next_button(self):
        has_card = bool(self._card_cache_path and os.path.exists(self._card_cache_path) and self._card_result)
        has_avatar = bool(self._avatar_cache_path and os.path.exists(self._avatar_cache_path) and self._avatar_result)
        self.btn_next_step.setEnabled(has_card or has_avatar)

    # ==================== PKG 应用 / 备份还原 / 退出 ====================

    def _apply_changes(self):
        tasks = []
        if self._card_cache_path and os.path.exists(self._card_cache_path) and self._card_result:
            tasks.append((t('workflow_card'), self._card_result, self._card_cache_path))
        if self._avatar_cache_path and os.path.exists(self._avatar_cache_path) and self._avatar_result:
            tasks.append((t('workflow_avatar'), self._avatar_result, self._avatar_cache_path))
        if not tasks:
            debug_log("应用修改: 没有可应用的任务")
            QMessageBox.warning(self, t('tip'), t('msg_no_task'))
            return

        self.status_label.setText(t('status_applying'))
        self.progress_bar.setValue(5)
        self.btn_next_step.setEnabled(False)
        self.btn_import_card.setEnabled(False)
        self.btn_import_avatar.setEnabled(False)

        self._apply_msg_queue = queue.Queue()
        self._apply_result = None
        debug_log(f"启动应用修改子线程: {len(tasks)}个任务, bak_dir={self._bak_dir}")

        def worker():
            try:
                success = apply_changes(
                    tasks,
                    progress_callback=lambda pct: self._apply_msg_queue.put(('progress', pct)),
                    log_callback=lambda msg: self._apply_msg_queue.put(('log', msg)),
                    bak_dir=self._bak_dir,
                )
            except Exception as e:
                import traceback
                debug_log(f"应用修改子线程异常: {e}")
                debug_log(traceback.format_exc())
                success = False
            self._apply_msg_queue.put(('done', success))

        self._apply_thread = threading.Thread(target=worker, daemon=True)
        self._apply_thread.start()

        self._apply_poll_timer = QTimer(self)
        self._apply_poll_timer.timeout.connect(self._poll_apply_queue)
        self._apply_poll_timer.start(50)

    def _poll_apply_queue(self):
        """主线程轮询子线程消息队列，安全更新UI"""
        drained = False
        while not drained:
            try:
                kind, payload = self._apply_msg_queue.get_nowait()
            except queue.Empty:
                drained = True
                break
            if kind == 'progress':
                self.progress_bar.setValue(payload)
            elif kind == 'log':
                self.search_log.appendPlainText(payload)
            elif kind == 'done':
                self._apply_poll_timer.stop()
                self._on_apply_done(payload)
                return

    def _on_apply_done(self, success):
        if success:
            self.progress_bar.setValue(100)
            self._save_config()
            debug_log("应用修改完成")
            QMessageBox.information(self, t('tip'), t('msg_apply_done'))
            self.progress_bar.setValue(0)
            self.status_label.setText(t('status_applied'))
            self.tabs.setTabEnabled(2, True)
            self.tabs.setCurrentIndex(2)
            debug_log("PKG修改成功，跳转到更换操作选项卡")
        else:
            QMessageBox.critical(self, t('error'), t('msg_apply_error'))
            self.status_label.setText(t('status_apply_failed'))
            self.progress_bar.setValue(0)
        self.btn_next_step.setEnabled(True)
        self._update_next_button()
        self.btn_import_card.setEnabled(self._card_result is not None)
        self.btn_import_avatar.setEnabled(self._avatar_result is not None)
        self._apply_thread = None
        debug_log("_on_apply_done: 槽函数结束")

    def _restore_backup(self):
        restored = pkg_ops.restore_backup(
            self._bak_dir, self._config_path,
            self.game_path_edit.text().strip(),
            log_callback=lambda msg: self.search_log.appendPlainText(msg),
        )
        if restored == 0:
            QMessageBox.information(self, t('tip'), t('msg_no_backup'))
        else:
            self.status_label.setText(t('status_restored').format(restored))
            QMessageBox.information(self, t('tip'),
                t('msg_restore_done').format(restored))
            self._save_config()

    def _cleanup_on_exit(self):
        pkg_ops.cleanup_on_exit(
            self._bak_dir, self._cache_dir,
            self._config_path, self.game_path_edit.text().strip(),
        )

    # ==================== 设置窗口 ====================

    def _show_settings_dialog(self):
        """显示设置对话框"""
        from .constants import IMAGE_ABOUT
        from .i18n import get_language, set_language, SUPPORTED_LANGUAGES
        from .info_dialogs import show_about_dialog
        import json

        dlg = QDialog(self)
        dlg.setWindowTitle(t('dialog_settings_title'))
        dlg.setMinimumWidth(380)
        layout = QVBoxLayout(dlg)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        # 语言设置
        lang_group = QGroupBox(t('settings_language'))
        lang_layout = QHBoxLayout(lang_group)
        lang_combo = QComboBox()
        lang_combo.addItem(t('lang_zh'), 'zh')
        lang_combo.addItem(t('lang_en'), 'en')
        lang_combo.addItem(t('lang_ja'), 'ja')
        current_lang = get_language()
        for i in range(lang_combo.count()):
            if lang_combo.itemData(i) == current_lang:
                lang_combo.setCurrentIndex(i)
                break
        lang_layout.addWidget(lang_combo)
        layout.addWidget(lang_group)

        # Debug 模式
        debug_group = QGroupBox(t('settings_debug'))
        debug_layout = QVBoxLayout(debug_group)
        debug_check = QCheckBox(t('settings_debug_hint'))
        debug_check.setChecked(is_debug_enabled())
        debug_layout.addWidget(debug_check)
        layout.addWidget(debug_group)

        # 其他设置
        other_group = QGroupBox(t('settings_other'))
        other_layout = QVBoxLayout(other_group)
        confirm_exit_check = QCheckBox(t('settings_confirm_exit_hint'))
        confirm_exit_check.setChecked(getattr(self, '_confirm_on_exit', True))
        other_layout.addWidget(confirm_exit_check)
        layout.addWidget(other_group)

        # 关于按钮
        about_layout = QHBoxLayout()
        about_layout.addStretch()
        btn_about = QPushButton(t('settings_about_btn'))
        btn_about.setStyleSheet(_btn_style("#9b59b6", "#8e44ad", padding="6px 16px"))
        btn_about.clicked.connect(lambda: show_about_dialog(dlg))
        about_layout.addWidget(btn_about)
        about_layout.addStretch()
        layout.addLayout(about_layout)

        # 提示文本
        hint_label = QLabel(t('settings_restart_hint'))
        hint_label.setStyleSheet("color: #e67e22; font-size: 11px;")
        hint_label.setWordWrap(True)
        layout.addWidget(hint_label)

        # 按钮区
        btn_layout = QHBoxLayout()
        btn_save = QPushButton(t('settings_btn_save'))
        btn_save.setStyleSheet(_btn_style("#27ae60", "#219a52", padding="8px 20px"))
        btn_close = QPushButton(t('settings_btn_close'))
        btn_close.setStyleSheet(_btn_style("#7f8c8d", "#95a5a6", padding="8px 20px"))
        btn_layout.addStretch()
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_close)
        layout.addLayout(btn_layout)

        saved = [False]

        def _save_and_restart():
            new_lang = lang_combo.currentData()
            new_debug = debug_check.isChecked()
            new_confirm_exit = confirm_exit_check.isChecked()
            config = {}
            try:
                if os.path.exists(self._config_path):
                    with open(self._config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
            except Exception as e:
                debug_log(f"读取配置用于设置合并失败: {e}")
            lang_changed = (new_lang != current_lang)
            debug_changed = (new_debug != is_debug_enabled())
            confirm_exit_changed = (new_confirm_exit != getattr(self, '_confirm_on_exit', True))
            config['language'] = new_lang
            config['debug'] = new_debug
            config['confirm_on_exit'] = new_confirm_exit
            try:
                with open(self._config_path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)
                saved[0] = True
                # 立即更新运行时开关，无需重启即可生效
                self._confirm_on_exit = new_confirm_exit
            except Exception as e:
                QMessageBox.critical(dlg, t('error'), str(e))
                return

            if lang_changed:
                reply = QMessageBox.question(
                    dlg, t('settings_restart_title'),
                    t('settings_restart_now'),
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
                )
                if reply == QMessageBox.Yes:
                    dlg.accept()
                    # 重启程序
                    # PyInstaller ONEFILE 模式下,父进程通过 _MEIPASS/_PYI* 环境变量记录解压目录,
                    # 子进程若继承该变量会复用父进程临时目录,而父进程退出时会清理该目录,
                    # 导致子进程读取文件(如 UnityPy\resources\lzma.tpk)时 FileNotFoundError。
                    # 必须清除所有 _MEI* 和 _PYI* 环境变量,强制子进程重新解压。
                    # 同时使用 close_fds=True 和 CREATE_NEW_PROCESS_GROUP 确保进程独立。
                    import subprocess
                    env = os.environ.copy()
                    for k in list(env.keys()):
                        if k.startswith('_MEI') or k.startswith('_PYI'):
                            del env[k]
                    subprocess.Popen(
                        [sys.executable] + sys.argv[1:],
                        env=env,
                        close_fds=True,
                        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                    )
                    QApplication.quit()
                else:
                    dlg.accept()
            elif debug_changed:
                QMessageBox.information(dlg, t('tip'), t('settings_debug_restarted'))
                dlg.accept()
            elif confirm_exit_changed:
                # 仅退出确认设置变化，无需重启，提示已保存
                QMessageBox.information(dlg, t('tip'), t('settings_saved'))
                dlg.accept()
            else:
                dlg.accept()

        btn_save.clicked.connect(_save_and_restart)
        btn_close.clicked.connect(dlg.reject)

        dlg.exec_()

    def resizeEvent(self, event):
        """窗口尺寸变化时让预览框适度放大并同步缩略图，保持整体比例协调"""
        super().resizeEvent(event)
        self._update_thumb_max_size()

    def _update_thumb_max_size(self):
        """窗口越宽预览框上限越大(180~280px)，并按新尺寸重渲染预览缩略图"""
        if not hasattr(self, 'thumb_label'):
            return
        grow = max(0.0, min(1.0, (self.width() - 960) / (1500 - 960)))
        size = int(THUMB_MAX_SIZE + (280 - THUMB_MAX_SIZE) * grow)
        self.thumb_label.setMaximumSize(size, size)
        src = self._last_preview_source
        if src is not None and not src.isNull():
            scaled = src.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            draw_preview_border(scaled)
            self.thumb_label.setPixmap(scaled)

    def closeEvent(self, event):
        # 应用修改进行中禁止退出：避免退出清理与写包线程竞态写坏游戏文件
        if self._apply_thread is not None and self._apply_thread.is_alive():
            QMessageBox.warning(self, t('tip'), t('msg_exit_while_applying'))
            event.ignore()
            return
        # 根据设置决定是否弹出退出确认对话框
        if self._confirm_on_exit:
            ret = QMessageBox.question(self, t('msg_confirm_exit_title'),
                t('msg_confirm_exit'),
                QMessageBox.Yes | QMessageBox.No)
            if ret != QMessageBox.Yes:
                event.ignore()
                return
        # 保存窗口大小和位置到配置文件
        # 最大化时 normalGeometry() 返回还原后的常规尺寸，并额外记录最大化状态，
        # 避免下次启动变成"准全屏大小的普通窗口"
        try:
            was_maximized = self.isMaximized()
            geo = self.normalGeometry()
            self._save_window_geometry(geo.x(), geo.y(), geo.width(), geo.height(), was_maximized)
        except Exception as e:
            debug_log(f"保存窗口位置失败: {e}")
        self._cleanup_on_exit()
        event.accept()

    def _save_window_geometry(self, x, y, w, h, maximized=False):
        """将窗口位置和大小写入 config.json 的 window_geometry 字段，同时记录最大化状态"""
        try:
            config = {}
            if os.path.exists(self._config_path):
                with open(self._config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            config['window_geometry'] = [x, y, w, h]
            config['window_maximized'] = bool(maximized)
            with open(self._config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            debug_log(f"窗口位置已保存: x={x}, y={y}, w={w}, h={h}")
        except Exception as e:
            debug_log(f"保存窗口位置异常: {e}")
