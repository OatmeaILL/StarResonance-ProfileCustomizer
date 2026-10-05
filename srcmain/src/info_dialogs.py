# -*- coding: utf-8 -*-
"""信息对话框：教程 / FAQ / 关于"""

import os

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTextBrowser, QPushButton,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from .constants import IMAGE_ABOUT, IMAGE_FAQ, IMAGE_TUTORIAL
from .i18n import t, get_tutorial_html, get_faq_html, get_about_html
from .paths import resource_path


def _build_info_dialog(parent, title, html_text, image_name, min_size,
                      btn_color, modal=True):
    """构建带图标的信息对话框"""
    dlg = QDialog(parent, Qt.Window)
    dlg.setWindowTitle(title)
    dlg.setMinimumSize(*min_size)
    layout = QVBoxLayout(dlg)

    img_path = resource_path(os.path.join('image', image_name))
    if os.path.exists(img_path):
        lbl_img = QLabel()
        pix = QPixmap(img_path).scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        lbl_img.setPixmap(pix)
        lbl_img.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_img)

    text = QTextBrowser()
    text.setOpenExternalLinks(False)
    text.setHtml(html_text)
    layout.addWidget(text, 1)

    btn_ok = QPushButton(t('ok'))
    btn_ok.setStyleSheet(
        f"QPushButton {{ background-color: {btn_color}; color: white; font-weight: bold; "
        f"padding: 8px 30px; border-radius: 4px; }}"
    )
    btn_ok.clicked.connect(dlg.close if not modal else dlg.accept)
    layout.addWidget(btn_ok, alignment=Qt.AlignCenter)
    return dlg


def show_tutorial_dialog(parent):
    """显示使用教程对话框（非模态）"""
    dlg = _build_info_dialog(
        parent, t('dialog_tutorial_title'), get_tutorial_html(), IMAGE_TUTORIAL,
        (500, 500), "#3498db", modal=False,
    )
    dlg.show()
    return dlg


def show_faq_dialog(parent):
    """显示常见问题对话框（非模态）"""
    dlg = _build_info_dialog(
        parent, t('dialog_faq_title'), get_faq_html(), IMAGE_FAQ,
        (500, 550), "#e67e22", modal=False,
    )
    dlg.show()
    return dlg


def show_about_dialog(parent):
    """显示关于对话框（模态）"""
    dlg = _build_info_dialog(
        parent, t('dialog_about_title'), get_about_html(), IMAGE_ABOUT,
        (450, 450), "#9b59b6", modal=True,
    )
    dlg.exec_()
    return dlg
