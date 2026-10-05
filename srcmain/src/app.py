# -*- coding: utf-8 -*-
"""应用入口：语言选择、EULA 确认、QApplication 初始化、主窗口启动"""

import os
import sys
import json
import ctypes

from PyQt5.QtWidgets import (
    QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QDialog,
    QComboBox, QFormLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap

from .constants import APP_VERSION, IMAGE_ABOUT
from .i18n import (
    t, set_language, get_language, load_language_from_config,
    SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE, get_eula_html,
)
from .paths import resource_path, app_dir
from .debug import _init_debug, _close_debug, debug_log, is_debug_enabled
from .win32_tools import HAS_WIN32, user32
from .info_dialogs import show_tutorial_dialog
from .main_window import MainWindow


def _show_language_select_dialog(app):
    """首次启动显示语言选择对话框，返回选择的语言代码"""
    dlg = QDialog()
    dlg.setWindowTitle(t('lang_select_title'))
    dlg.setMinimumSize(360, 200)
    layout = QVBoxLayout(dlg)

    img_path = resource_path(os.path.join('image', IMAGE_ABOUT))
    if os.path.exists(img_path):
        lbl_img = QLabel()
        pix = QPixmap(img_path).scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        lbl_img.setPixmap(pix)
        lbl_img.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_img)

    layout.addWidget(QLabel(t('lang_select_prompt')))

    combo = QComboBox()
    combo.addItem(t('lang_zh'), 'zh')
    combo.addItem(t('lang_en'), 'en')
    combo.addItem(t('lang_ja'), 'ja')
    combo.setCurrentIndex(0)
    layout.addWidget(combo)

    btn_layout = QHBoxLayout()
    btn_ok = QPushButton(t('ok'))
    btn_ok.setStyleSheet(
        "QPushButton { background-color: #27ae60; color: white; font-weight: bold; "
        "padding: 8px 24px; border-radius: 4px; }"
    )
    btn_ok.clicked.connect(dlg.accept)
    btn_layout.addStretch()
    btn_layout.addWidget(btn_ok)
    btn_layout.addStretch()
    layout.addLayout(btn_layout)

    if dlg.exec_() == QDialog.Accepted:
        return combo.currentData()
    return DEFAULT_LANGUAGE


def _show_eula_dialog(app):
    """首次启动显示 EULA，返回是否同意"""
    eula_path = os.path.join(app_dir(), '.eula_accepted')
    is_first_launch = not os.path.exists(eula_path)
    if not is_first_launch:
        return True, False

    dlg = QDialog()
    dlg.setWindowTitle(t('eula_title'))
    dlg.setMinimumSize(420, 380)
    dlg_layout = QVBoxLayout(dlg)

    img_path = resource_path(os.path.join('image', IMAGE_ABOUT))
    if os.path.exists(img_path):
        lbl_img = QLabel()
        pix = QPixmap(img_path).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        lbl_img.setPixmap(pix)
        lbl_img.setAlignment(Qt.AlignCenter)
        dlg_layout.addWidget(lbl_img)

    dlg_layout.addWidget(QLabel(get_eula_html(APP_VERSION)))

    btn_layout = QHBoxLayout()
    btn_yes = QPushButton(t('eula_agree'))
    btn_yes.setStyleSheet(
        "QPushButton { background-color: #27ae60; color: white; font-weight: bold; "
        "padding: 8px 24px; border-radius: 4px; }"
    )
    btn_no = QPushButton(t('eula_disagree'))
    btn_no.setStyleSheet(
        "QPushButton { background-color: #e74c3c; color: white; font-weight: bold; "
        "padding: 8px 24px; border-radius: 4px; }"
    )
    btn_layout.addStretch()
    btn_layout.addWidget(btn_yes)
    btn_layout.addWidget(btn_no)
    btn_layout.addStretch()
    dlg_layout.addLayout(btn_layout)

    btn_yes.clicked.connect(dlg.accept)
    btn_no.clicked.connect(dlg.reject)

    if dlg.exec_() != QDialog.Accepted:
        return False, True

    # 写入失败（如目录只读）时不中断启动，仅下次启动会再次显示协议
    try:
        with open(eula_path, 'w') as f:
            f.write('accepted')
    except OSError as e:
        debug_log(f"写入EULA标记失败(目录可能只读): {e}")
    return True, True


def _save_language(lang):
    """保存语言选择到 config.json"""
    config_path = os.path.join(app_dir(), 'config.json')
    config = {}
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
    except Exception as e:
        debug_log(f"读取配置用于语言保存失败: {e}")
    config['language'] = lang
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except Exception as e:
        debug_log(f"保存语言设置失败: {e}")


def _is_running_as_admin():
    """检测当前是否以管理员权限运行；非 Windows 或检测失败时不提示（按已授权处理）"""
    if not HAS_WIN32:
        return True
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception as e:
        debug_log(f"检测管理员权限失败: {e}")
        return True


def _warn_if_not_admin(window):
    """未使用管理员权限时弹出提示，避免用户遇到窗口调整等失败时无从排查"""
    if _is_running_as_admin():
        return
    debug_log("未以管理员权限运行，弹出提示")
    QMessageBox.information(window, t('tip'), t('msg_not_admin'))


def run():
    """应用主入口"""
    _init_debug()
    debug_log(f"程序启动 version={APP_VERSION}")
    debug_log(f"app_dir={app_dir()} frozen={getattr(sys, 'frozen', False)}")
    debug_log(f"HAS_WIN32={HAS_WIN32}")

    config_path = os.path.join(app_dir(), 'config.json')
    load_language_from_config(config_path)
    debug_log(f"加载语言配置: language={get_language()}")

    try:
        from . import unity
        debug_log("UnityPy 预热完成（主线程初始化）")
    except Exception as e:
        debug_log(f"UnityPy 预热失败: {e}")

    if HAS_WIN32:
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:
            try:
                user32.SetProcessDPIAware()
            except Exception as e:
                debug_log(f"SetProcessDPIAware 也失败: {e}")
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                f'StarImage.MaiMai.ProfileCustomizer.{APP_VERSION}'
            )
        except Exception as e:
            debug_log(f"设置AppUserModelID失败: {e}")

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    font = QFont("Microsoft YaHei", 9)
    app.setFont(font)

    # 判断是否需要弹出语言选择窗口
    # 规则：只有当 config.json 中存在合法 language 字段时才跳过
    # 另外检测 .eula_accepted 文件是否存在，用于区分全新用户与老版本升级用户
    # （老版本用户可能有 accept 文件但 config 中无 language 字段，仍需弹窗让其选择语言）
    eula_path = os.path.join(app_dir(), '.eula_accepted')
    has_eula_accepted = os.path.exists(eula_path)
    has_valid_language = False
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                cfg = json.load(f)
            if cfg.get('language', '') in SUPPORTED_LANGUAGES:
                has_valid_language = True
    except Exception as e:
        debug_log(f"读取语言配置失败: {e}")

    need_language_select = not has_valid_language
    if need_language_select:
        if has_eula_accepted:
            debug_log("检测到已启动过（.eula_accepted 存在）但未配置语言，判定为老版本升级用户，弹出语言选择")
        else:
            debug_log("首次启动，弹出语言选择")
        selected_lang = _show_language_select_dialog(app)
        set_language(selected_lang)
        _save_language(selected_lang)
        debug_log(f"用户选择语言: {selected_lang}")

    agreed, is_first_launch = _show_eula_dialog(app)
    if not agreed:
        debug_log("用户未同意EULA，程序退出")
        sys.exit(0)

    window = MainWindow()
    window.show()
    debug_log("主窗口已创建并显示")

    if is_first_launch:
        show_tutorial_dialog(window)
        debug_log("首次启动，已弹出教程")

    _warn_if_not_admin(window)

    ret = app.exec_()
    debug_log(f"app.exec_() 返回 {ret}，程序即将退出")
    _close_debug()
    sys.exit(ret)
