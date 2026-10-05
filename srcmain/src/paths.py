# -*- coding: utf-8 -*-
"""资源路径与运行目录工具，兼容开发环境与 PyInstaller 打包"""

import os
import sys


def resource_path(relative_path):
    """获取资源文件的绝对路径，兼容开发环境和PyInstaller打包"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def app_dir():
    """获取程序运行目录（用于配置、缓存、备份等可写文件）"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def find_container_dir(path):
    path = os.path.normpath(path)
    if os.path.basename(path).lower() == 'container' and os.path.isdir(path):
        return path
    container_sub = os.path.join(path, 'container')
    if os.path.isdir(container_sub):
        return container_sub
    sa_container = os.path.join(path, 'Star_Data', 'StreamingAssets', 'container')
    if os.path.isdir(sa_container):
        return sa_container
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path) and item.endswith('_Data'):
            sa_c = os.path.join(item_path, 'StreamingAssets', 'container')
            if os.path.isdir(sa_c):
                return sa_c
    parent = os.path.dirname(path)
    for item in os.listdir(parent):
        item_path = os.path.join(parent, item)
        if os.path.isdir(item_path) and item.endswith('_Data'):
            sa_c = os.path.join(item_path, 'StreamingAssets', 'container')
            if os.path.isdir(sa_c):
                return sa_c
    return None
