# -*- coding: utf-8 -*-
"""Debug 日志系统，可通过 config.json 的 debug 字段开关"""

import os
import json
import threading

from .paths import app_dir

_debug_enabled = False
_debug_log_file = None
_debug_lock = threading.Lock()


def _init_debug():
    global _debug_enabled, _debug_log_file
    config_path = os.path.join(app_dir(), 'config.json')
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                cfg = json.load(f)
            _debug_enabled = bool(cfg.get('debug', False))
    except Exception:
        pass
    if _debug_enabled:
        log_dir = os.path.join(app_dir(), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        from datetime import datetime
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_path = os.path.join(log_dir, f'debug_{ts}.log')
        try:
            _debug_log_file = open(log_path, 'w', encoding='utf-8')
        except Exception:
            _debug_log_file = None


def debug_log(msg):
    if not _debug_enabled:
        return
    from datetime import datetime
    ts = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    line = f"[{ts}] {msg}"
    with _debug_lock:
        if _debug_log_file:
            try:
                _debug_log_file.write(line + '\n')
                _debug_log_file.flush()
            except Exception:
                pass


def _close_debug():
    global _debug_log_file
    with _debug_lock:
        if _debug_log_file:
            try:
                _debug_log_file.close()
            except Exception:
                pass
            _debug_log_file = None


def is_debug_enabled():
    """返回当前是否处于 debug 模式"""
    return _debug_enabled
