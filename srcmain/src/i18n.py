# -*- coding: utf-8 -*-
"""国际化模块：语言管理 + 三语翻译字典（zh/en/ja）

使用方式：
    from .i18n import t, set_language, get_language, get_card_steps, get_avatar_steps
    label.setText(t('btn_select_dir'))
"""

import json
import os

SUPPORTED_LANGUAGES = ['zh', 'en', 'ja']
DEFAULT_LANGUAGE = 'zh'

_current_lang = DEFAULT_LANGUAGE


def set_language(lang):
    global _current_lang
    if lang in SUPPORTED_LANGUAGES:
        _current_lang = lang


def get_language():
    return _current_lang


def t(key):
    texts = _TRANSLATIONS.get(_current_lang, _TRANSLATIONS[DEFAULT_LANGUAGE])
    return texts.get(key, _TRANSLATIONS[DEFAULT_LANGUAGE].get(key, key))


def load_language_from_config(config_path):
    global _current_lang
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                cfg = json.load(f)
            lang = cfg.get('language', '')
            if lang in SUPPORTED_LANGUAGES:
                _current_lang = lang
    except Exception:
        pass


def get_card_steps():
    return _CARD_STEPS.get(_current_lang, _CARD_STEPS[DEFAULT_LANGUAGE])


def get_avatar_steps():
    return _AVATAR_STEPS.get(_current_lang, _AVATAR_STEPS[DEFAULT_LANGUAGE])


def get_eula_html(version):
    template = _EULA_TEMPLATES.get(_current_lang, _EULA_TEMPLATES[DEFAULT_LANGUAGE])
    return template.format(version=version)


def get_tutorial_html():
    return _TUTORIAL_HTML.get(_current_lang, _TUTORIAL_HTML[DEFAULT_LANGUAGE])


def get_faq_html():
    return _FAQ_HTML.get(_current_lang, _FAQ_HTML[DEFAULT_LANGUAGE])


def get_about_html():
    return _ABOUT_HTML.get(_current_lang, _ABOUT_HTML[DEFAULT_LANGUAGE])


# ============================================================
# 翻译文本字典
# ============================================================

_TRANSLATIONS = {
    # ==================== 中文 ====================
    'zh': {
        # 通用
        'ok': '确定',
        'cancel': '取消',
        'yes': '是',
        'no': '否',
        'close': '关闭',
        'tip': '提示',
        'warning': '警告',
        'error': '错误',
        'info': '信息',
        'preview': '预览',

        # app.py - EULA
        'eula_title': '用户协议',
        'eula_agree': '同意',
        'eula_disagree': '不同意',

        # app.py - 语言选择
        'lang_select_title': '选择语言 / Select Language / 言語を選択',
        'lang_select_prompt': '选择语言 / Select Language / 言語を選択：',
        'lang_zh': '简体中文',
        'lang_en': 'English',
        'lang_ja': '日本語',

        # 主窗口标题
        'app_title_prefix': '麦麦子名片头像修改工具 v',
        'app_title_debug': ' [debug mode]',

        # 顶栏按钮
        'game_dir_label': '游戏安装目录:',
        'btn_select_dir': '选择目录',
        'btn_restore': '还原',
        'btn_tutorial': '教程',
        'btn_faq': '常见问题',
        'btn_settings': '设置',
        'placeholder_game_path': '首次使用请选择游戏安装目录...',

        # 状态栏
        'status_ready': '就绪',
        'status_loaded_config': '已加载配置: {}',
        'status_scanned': '已扫描 {} 个数据包',
        'status_searching': '正在查找资源...',
        'status_searching_progress': '查找中 {}/{}: {}',
        'status_full_searching': '正在全量查找资源...',
        'status_search_done': '查找完成 | 扫描 {} 数据包 | 找到 {} 个有效匹配',
        'status_applying': '正在应用修改...',
        'status_applied': '修改已应用到游戏文件',
        'status_apply_failed': '应用修改失败',
        'status_restored': '已还原 {} 个文件',

        # Tab 标题
        'tab_search': '查找资源',
        'tab_edit': '编辑图片',
        'tab_apply': '更换操作',

        # 查找 Tab
        'group_search_mode': '查找方式',
        'radio_quick': '快速查找',
        'radio_full': '完整查找',
        'label_quick_n': '  找到几个数据包后停止:',
        'btn_scan': '扫描数据包',
        'btn_search': '开始查找',
        'btn_stop': '停止查找',
        'col_pkg': '数据包',
        'col_type': '类型',
        'col_name': '名称',
        'col_usage': '用途',
        'btn_assign_card': ' 设为名片',
        'btn_assign_avatar': ' 设为头像',
        'assigned_label': '名片: {} | 头像: {}',
        'not_selected': '未选择',

        # 编辑 Tab
        'btn_import_card': ' 选择名片图片',
        'btn_import_avatar': ' 选择头像图片',
        'btn_reset_pos': ' 复位图片',
        'btn_reset_img': ' 重置图片',
        'btn_next_step': ' 下一步',
        'btn_crop_ok': ' 确认裁剪',
        'tip_must_enter_guild': "<span style='color:red; font-weight:bold;'>注意：务必先进入协会，再进行下一步。</span>",
        'edit_type_none': '当前: 无',
        'edit_type_card': '当前: 名片 ({}x{})',
        'edit_type_avatar': '当前: 头像 ({}x{}, 1:1)',
        'label_brightness': '亮度:',
        'label_contrast': '对比度:',
        'label_saturation': '饱和度:',
        'label_temperature': '色温:',
        'label_zoom': '缩放:',
        'tooltip_reset_default': '重置为默认值',
        'tooltip_click_preview': '点击预览',
        'thumb_label': '预览',

        # 更换 Tab
        'game_status_not_detected': '游戏状态: 未检测到游戏',
        'game_status_connected': '游戏状态: 已连接 ({})',
        'game_status_running_no_window': '游戏状态: 游戏进程运行中 (未找到游戏窗口)',
        'btn_capture_window': '手动捕获游戏窗口',
        'tooltip_capture': '若检测不到游戏或点击游戏窗口无反应，请以管理员权限运行本程序',
        'capture_prompt': '请点击游戏窗口... (ESC取消)',
        'btn_start_card': ' 开始更换名片',
        'btn_start_avatar': ' 开始更换头像',
        'btn_step_next': ' 下一步',
        'window_title_default': '游戏窗口',
        'no_title': '(无标题)',

        # 工作流
        'workflow_card': '名片',
        'workflow_avatar': '头像',
        'workflow_card_title': '更换名片流程',
        'workflow_avatar_title': '更换头像流程',
        'workflow_done_card': '更换名片步骤完毕。',
        'workflow_done_avatar': '更换头像步骤完毕。',
        'msg_no_game_window': '未检测到游戏窗口，请先启动游戏',
        'msg_no_game_window_debug': '未检测到游戏窗口，请先启动游戏或手动捕获',
        'window_resized': '[窗口已调整为 {}x{}]',
        'window_resize_failed': '[窗口调整失败，请尝试以管理员权限运行工具后重试。]',

        # 对话框消息
        'msg_select_dir': '选择游戏安装目录',
        'msg_no_container': '未找到container目录\n路径: {}\n\n请确保路径正确，或直接选择container目录',
        'msg_scan_done': '扫描完成: {} 个数据包 (跳过{}个>1G, {}个meta), 线程数: {}',
        'msg_no_pkg_scanned': '请先扫描数据包',
        'msg_search_start': '开始查找 | 方式: {}, 类型: {}, 名称: {}, 数据包数: {}, 线程: {}',
        'msg_pre_search': '[预查找] 尝试读取上次记录的 {} 个数据包',
        'msg_pre_search_hit': '[预查找] 命中，跳过全量扫描',
        'msg_pre_search_miss': '[预查找] 未达目标，回退全量扫描',
        'msg_search_found': '[找到] {} ({}) in {} 条目#{}',
        'msg_search_excluded': '[排除废弃] {} in {}',
        'msg_quick_stop': '[快速查找] 已找到{}个数据包，停止查找',
        'msg_search_stopped': '用户已停止查找',
        'msg_search_complete': '找到 {} 个有效匹配资源\n已自动分配名片和头像资源',
        'msg_search_no_result': '在 {} 个数据包中未找到匹配资源',
        'msg_select_result': '请先选择一条搜索结果',
        'msg_no_crop_image': '没有可裁剪的图片',
        'msg_crop_done': '{}图片已保存到缓存\n分辨率: {}x{}',
        'msg_no_task': '请先选择并裁剪图片',
        'msg_apply_done': '数据包文件已修改。如遇游戏无法启动等问题，请点击「还原」按钮后重新尝试封包操作。',
        'msg_apply_error': '应用修改时出错，请查看日志',
        'msg_asset_index_high': '当前资源的编号较大（超过12），在游戏中排列位置较靠后。\n如果未在预期位置找到替换的资源，请向下滚动查找。',
        'msg_no_backup': '没有找到备份文件',
        'msg_restore_done': '已还原 {} 个备份文件。\n请重新启动游戏验证。',
        'msg_confirm_exit': '退出程序将自动还原备份并清理缓存文件。\n是否继续？',
        'msg_confirm_exit_title': '确认退出',
        'msg_exit_while_applying': '正在应用修改到游戏文件，请等待完成后再退出',
        'msg_not_admin': '程序未使用管理员权限运行，可能会导致部分功能异常。若出现功能异常，请尝试以管理员权限运行。',
        'msg_image_load_failed': '无法加载图片:\n{}\n\n错误: {}',
        'msg_image_invalid': '无法加载图片:\n{}\n\n图片数据无效',
        'msg_image_process_failed': '处理图片时出错:\n{}\n\n错误: {}',
        'msg_image_load_title': '图片加载失败',
        'msg_image_process_title': '图片处理失败',

        # 文件对话框
        'file_select_card': '选择名片图片',
        'file_select_avatar': '选择头像图片',
        'file_filter_image': '图片 (*.png *.jpg *.jpeg *.bmp);;All (*)',

        # 预览窗口
        'preview_title': '预览',
        'preview_title_size': '预览 - {}x{}',
        'easter_egg_hint': '你还没有选择图片呢！无法放大预览哦~',

        # 日志文本
        'log_card_saved': '[名片] 已保存裁剪结果到 cache/card_custom.png',
        'log_avatar_saved': '[头像] 已保存裁剪结果到 cache/avatar_custom.png',

        # 信息对话框标题
        'dialog_tutorial_title': '使用教程',
        'dialog_faq_title': '常见问题',
        'dialog_about_title': '关于',
        'dialog_settings_title': '设置',

        # 设置窗口
        'settings_language': '界面语言',
        'settings_debug': '调试模式 (Debug)',
        'settings_debug_hint': '开启后将在 logs/ 目录生成调试日志',
        'settings_confirm_exit': '退出时显示确认对话框',
        'settings_confirm_exit_hint': '退出程序时弹出还原窗口',
        'settings_other': '其他设置',
        'settings_saved': '设置已保存',
        'settings_about': '关于本工具',
        'settings_about_btn': '打开关于',
        'settings_restart_hint': '语言切换后需要重启程序才能完整生效',
        'settings_btn_save': '保存设置',
        'settings_btn_close': '关闭',
        'settings_restart_now': '语言已更改，需要重启程序才能生效。\n是否立即重启？',
        'settings_restart_title': '需要重启',
        'settings_debug_restarted': '调试模式设置已保存，重启后生效',

        # 窗口捕获确认
        'capture_confirm_title': '确认游戏窗口',
        'capture_confirm_text': '<b>窗口标题:</b> {}<br><b>进程名称:</b> {}<br><b>PID:</b> {}<br><b>窗口句柄:</b> {}<br><br>确认将此窗口作为游戏窗口吗？',
        'capture_pid_label': '(PID: {})',

        # 调试面板
        'debug_resize_title': '【调试】窗口分辨率测试',
        'debug_label_w': '宽:',
        'debug_label_h': '高:',
        'debug_label_scale': '缩放%:',
        'debug_btn_apply': '应用',
        'debug_resize_log': '[调试] 窗口已调整为 {}x{} (原始 {}x{} @ {}%)',
        'debug_resize_fail': '[调试] 窗口调整失败',
    },

    # ==================== English ====================
    'en': {
        # Common
        'ok': 'OK',
        'cancel': 'Cancel',
        'yes': 'Yes',
        'no': 'No',
        'close': 'Close',
        'tip': 'Tip',
        'warning': 'Warning',
        'error': 'Error',
        'info': 'Info',
        'preview': 'Preview',

        # app.py - EULA
        'eula_title': 'User Agreement',
        'eula_agree': 'Agree',
        'eula_disagree': 'Disagree',

        # app.py - Language selection
        'lang_select_title': 'Select Language / 选择语言 / 言語を選択',
        'lang_select_prompt': 'Please select interface language:',
        'lang_zh': '简体中文',
        'lang_en': 'English',
        'lang_ja': '日本語',

        # Main window title
        'app_title_prefix': 'Maimai BPSR Profile & Avatar Customizer v',
        'app_title_debug': ' [debug mode]',

        # Top bar
        'game_dir_label': 'Game Directory:',
        'btn_select_dir': 'Select Dir',
        'btn_restore': 'Restore',
        'btn_tutorial': 'Tutorial',
        'btn_faq': 'FAQ',
        'btn_settings': 'Settings',
        'placeholder_game_path': 'Select game installation directory on first use...',

        # Status bar
        'status_ready': 'Ready',
        'status_loaded_config': 'Config loaded: {}',
        'status_scanned': 'Scanned {} packages',
        'status_searching': 'Searching resources...',
        'status_searching_progress': 'Searching {}/{}: {}',
        'status_full_searching': 'Full searching resources...',
        'status_search_done': 'Search done | Scanned {} packages | Found {} matches',
        'status_applying': 'Applying changes...',
        'status_applied': 'Changes applied to game files',
        'status_apply_failed': 'Apply changes failed',
        'status_restored': 'Restored {} files',

        # Tabs
        'tab_search': 'Find Resources',
        'tab_edit': 'Edit Image',
        'tab_apply': 'Apply Changes',

        # Search Tab
        'group_search_mode': 'Search Mode',
        'radio_quick': 'Quick Search',
        'radio_full': 'Full Search',
        'label_quick_n': '  Stop after finding N packages:',
        'btn_scan': 'Scan Packages',
        'btn_search': 'Start Search',
        'btn_stop': 'Stop',
        'col_pkg': 'Package',
        'col_type': 'Type',
        'col_name': 'Name',
        'col_usage': 'Usage',
        'btn_assign_card': ' Set as Card',
        'btn_assign_avatar': ' Set as Avatar',
        'assigned_label': 'Card: {} | Avatar: {}',
        'not_selected': 'Not selected',

        # Edit Tab
        'btn_import_card': ' Select Card Image',
        'btn_import_avatar': ' Select Avatar Image',
        'btn_reset_pos': ' Reset Position',
        'btn_reset_img': ' Reset Image',
        'btn_next_step': ' Next',
        'btn_crop_ok': ' Confirm Crop',
        'tip_must_enter_guild': "<span style='color:red; font-weight:bold;'>Note: Make sure to enter the guild before proceeding.</span>",
        'edit_type_none': 'Current: None',
        'edit_type_card': 'Current: Card ({}x{})',
        'edit_type_avatar': 'Current: Avatar ({}x{}, 1:1)',
        'label_brightness': 'Brightness:',
        'label_contrast': 'Contrast:',
        'label_saturation': 'Saturation:',
        'label_temperature': 'Temp:',
        'label_zoom': 'Zoom:',
        'tooltip_reset_default': 'Reset to default',
        'tooltip_click_preview': 'Click to preview',
        'thumb_label': 'Preview',

        # Apply Tab
        'game_status_not_detected': 'Game Status: Not detected',
        'game_status_connected': 'Game Status: Connected ({})',
        'game_status_running_no_window': 'Game Status: Process running (window not found)',
        'btn_capture_window': 'Capture Game Window',
        'tooltip_capture': 'If the game cannot be detected, try running as administrator',
        'capture_prompt': 'Click the game window... (ESC to cancel)',
        'btn_start_card': ' Replace Card',
        'btn_start_avatar': ' Replace Avatar',
        'btn_step_next': ' Next',
        'window_title_default': 'Game Window',
        'no_title': '(No title)',

        # Workflow
        'workflow_card': 'Card',
        'workflow_avatar': 'Avatar',
        'workflow_card_title': 'Replace Card Workflow',
        'workflow_avatar_title': 'Replace Avatar Workflow',
        'workflow_done_card': 'Card replacement completed.',
        'workflow_done_avatar': 'Avatar replacement completed.',
        'msg_no_game_window': 'Game window not detected. Please launch the game first.',
        'msg_no_game_window_debug': 'Game window not detected. Please launch the game or capture manually.',
        'window_resized': '[Window resized to {}x{}]',
        'window_resize_failed': '[Window resize failed. Try running as administrator.]',

        # Dialog messages
        'msg_select_dir': 'Select Game Installation Directory',
        'msg_no_container': 'container directory not found\nPath: {}\n\nPlease verify the path or select the container directory directly',
        'msg_scan_done': 'Scan complete: {} packages (skipped {} >1G, {} meta), workers: {}',
        'msg_no_pkg_scanned': 'Please scan packages first',
        'msg_search_start': 'Search started | Mode: {}, Type: {}, Name: {}, Packages: {}, Workers: {}',
        'msg_pre_search': '[Pre-search] Trying {} cached packages',
        'msg_pre_search_hit': '[Pre-search] Hit, skipping full scan',
        'msg_pre_search_miss': '[Pre-search] Not enough, falling back to full scan',
        'msg_search_found': '[Found] {} ({}) in {} entry#{}',
        'msg_search_excluded': '[Excluded] {} in {}',
        'msg_quick_stop': '[Quick] Found {} packages, stopping',
        'msg_search_stopped': 'Search stopped by user',
        'msg_search_complete': 'Found {} valid matches\nCard and avatar resources auto-assigned',
        'msg_search_no_result': 'No matches found in {} packages',
        'msg_select_result': 'Please select a search result first',
        'msg_no_crop_image': 'No image to crop',
        'msg_crop_done': '{} image saved to cache\nResolution: {}x{}',
        'msg_no_task': 'Please select and crop an image first',
        'msg_apply_done': 'Package files modified. If the game fails to start, click "Restore" and try again.',
        'msg_apply_error': 'Error applying changes. Check the log.',
        'msg_asset_index_high': 'The current resource has a high index (over 12) and will appear in a later position in the game.\nIf you can\'t find the replacement at the expected location, scroll down to look for it.',
        'msg_no_backup': 'No backup files found',
        'msg_restore_done': 'Restored {} backup files.\nPlease restart the game to verify.',
        'msg_confirm_exit': 'Exiting will automatically restore backups and clear cache.\nContinue?',
        'msg_confirm_exit_title': 'Confirm Exit',
        'msg_exit_while_applying': 'Changes are being applied to game files. Please wait until it finishes before exiting.',
        'msg_not_admin': 'The program is not running with administrator privileges, which may cause some features to malfunction. If you encounter issues, try running as administrator.',
        'msg_image_load_failed': 'Cannot load image:\n{}\n\nError: {}',
        'msg_image_invalid': 'Cannot load image:\n{}\n\nInvalid image data',
        'msg_image_process_failed': 'Error processing image:\n{}\n\nError: {}',
        'msg_image_load_title': 'Image Load Failed',
        'msg_image_process_title': 'Image Process Failed',

        # File dialogs
        'file_select_card': 'Select Card Image',
        'file_select_avatar': 'Select Avatar Image',
        'file_filter_image': 'Images (*.png *.jpg *.jpeg *.bmp);;All (*)',

        # Preview
        'preview_title': 'Preview',
        'preview_title_size': 'Preview - {}x{}',
        'easter_egg_hint': "You haven't selected an image yet! Nothing to preview~",

        # Log
        'log_card_saved': '[Card] Crop saved to cache/card_custom.png',
        'log_avatar_saved': '[Avatar] Crop saved to cache/avatar_custom.png',

        # Info dialog titles
        'dialog_tutorial_title': 'Tutorial',
        'dialog_faq_title': 'FAQ',
        'dialog_about_title': 'About',
        'dialog_settings_title': 'Settings',

        # Settings
        'settings_language': 'Interface Language',
        'settings_debug': 'Debug Mode',
        'settings_debug_hint': 'Enable to generate debug logs in logs/ directory',
        'settings_confirm_exit': 'Show confirmation dialog on exit',
        'settings_confirm_exit_hint': 'A confirmation dialog pops up when exiting the program',
        'settings_other': 'Other Settings',
        'settings_saved': 'Settings saved',
        'settings_about': 'About This Tool',
        'settings_about_btn': 'Open About',
        'settings_restart_hint': 'Language change requires restart to take full effect',
        'settings_btn_save': 'Save',
        'settings_btn_close': 'Close',
        'settings_restart_now': 'Language has been changed. Restart is required.\nRestart now?',
        'settings_restart_title': 'Restart Required',
        'settings_debug_restarted': 'Debug mode setting saved. Restart to take effect.',

        # Window capture
        'capture_confirm_title': 'Confirm Game Window',
        'capture_confirm_text': '<b>Title:</b> {}<br><b>Process:</b> {}<br><b>PID:</b> {}<br><b>HWND:</b> {}<br><br>Use this window as the game window?',
        'capture_pid_label': '(PID: {})',

        # Debug panel
        'debug_resize_title': '[Debug] Window Resolution Test',
        'debug_label_w': 'W:',
        'debug_label_h': 'H:',
        'debug_label_scale': 'Scale%:',
        'debug_btn_apply': 'Apply',
        'debug_resize_log': '[Debug] Window resized to {}x{} (original {}x{} @ {}%)',
        'debug_resize_fail': '[Debug] Window resize failed',
    },

    # ==================== 日本語 ====================
    'ja': {
        # 共通
        'ok': 'OK',
        'cancel': 'キャンセル',
        'yes': 'はい',
        'no': 'いいえ',
        'close': '閉じる',
        'tip': 'ヒント',
        'warning': '警告',
        'error': 'エラー',
        'info': '情報',
        'preview': 'プレビュー',

        # app.py - EULA
        'eula_title': '利用規約',
        'eula_agree': '同意',
        'eula_disagree': '同意しない',

        # app.py - 言語選択
        'lang_select_title': '言語を選択 / Select Language / 选择语言',
        'lang_select_prompt': 'インターフェース言語を選択してください：',
        'lang_zh': '简体中文',
        'lang_en': 'English',
        'lang_ja': '日本語',

        # メインウィンドウタイトル
        'app_title_prefix': '麦麦子 BPSR 名刺・アバター変更ツール v',
        'app_title_debug': ' [debug mode]',

        # トップバー
        'game_dir_label': 'ゲームディレクトリ:',
        'btn_select_dir': 'ディレクトリ選択',
        'btn_restore': '復元',
        'btn_tutorial': 'チュートリアル',
        'btn_faq': 'FAQ',
        'btn_settings': '設定',
        'placeholder_game_path': '初回使用時にゲームインストールディレクトリを選択してください...',

        # ステータスバー
        'status_ready': '準備完了',
        'status_loaded_config': '設定読込完了: {}',
        'status_scanned': '{}個のパッケージをスキャン',
        'status_searching': 'リソース検索中...',
        'status_searching_progress': '検索中 {}/{}: {}',
        'status_full_searching': '全量リソース検索中...',
        'status_search_done': '検索完了 | {}パッケージスキャン | {}件一致',
        'status_applying': '変更を適用中...',
        'status_applied': '変更をゲームファイルに適用しました',
        'status_apply_failed': '変更適用失敗',
        'status_restored': '{}個のファイルを復元',

        # タブ
        'tab_search': 'リソース検索',
        'tab_edit': '画像編集',
        'tab_apply': '交換作業',

        # 検索タブ
        'group_search_mode': '検索方式',
        'radio_quick': 'クイック検索',
        'radio_full': '完全検索',
        'label_quick_n': '  N個見つかったら停止:',
        'btn_scan': 'パッケージスキャン',
        'btn_search': '検索開始',
        'btn_stop': '停止',
        'col_pkg': 'パッケージ',
        'col_type': 'タイプ',
        'col_name': '名前',
        'col_usage': '用途',
        'btn_assign_card': ' 名刺に設定',
        'btn_assign_avatar': ' アバターに設定',
        'assigned_label': '名刺: {} | アバター: {}',
        'not_selected': '未選択',

        # 編集タブ
        'btn_import_card': ' 名刺画像を選択',
        'btn_import_avatar': ' アバター画像を選択',
        'btn_reset_pos': ' 位置リセット',
        'btn_reset_img': ' 画像リセット',
        'btn_next_step': ' 次へ',
        'btn_crop_ok': ' 切り抜き確定',
        'tip_must_enter_guild': "<span style='color:red; font-weight:bold;'>注意：必ずギルドに入ってから次へ進んでください。</span>",
        'edit_type_none': '現在: なし',
        'edit_type_card': '現在: 名刺 ({}x{})',
        'edit_type_avatar': '現在: アバター ({}x{}, 1:1)',
        'label_brightness': '明るさ:',
        'label_contrast': 'コントラスト:',
        'label_saturation': '彩度:',
        'label_temperature': '色温度:',
        'label_zoom': 'ズーム:',
        'tooltip_reset_default': 'デフォルトに戻す',
        'tooltip_click_preview': 'クリックでプレビュー',
        'thumb_label': 'プレビュー',

        # 交換タブ
        'game_status_not_detected': 'ゲーム状態: 未検出',
        'game_status_connected': 'ゲーム状態: 接続済み ({})',
        'game_status_running_no_window': 'ゲーム状態: プロセス実行中 (ウィンドウ未検出)',
        'btn_capture_window': 'ゲームウィンドウをキャプチャ',
        'tooltip_capture': 'ゲームが検出できない場合、管理者として実行してください',
        'capture_prompt': 'ゲームウィンドウをクリック... (ESCでキャンセル)',
        'btn_start_card': ' 名刺を交換',
        'btn_start_avatar': ' アバターを交換',
        'btn_step_next': ' 次へ',
        'window_title_default': 'ゲームウィンドウ',
        'no_title': '(タイトルなし)',

        # ワークフロー
        'workflow_card': '名刺',
        'workflow_avatar': 'アバター',
        'workflow_card_title': '名刺交換フロー',
        'workflow_avatar_title': 'アバター交換フロー',
        'workflow_done_card': '名刺交換ステップ完了。',
        'workflow_done_avatar': 'アバター交換ステップ完了。',
        'msg_no_game_window': 'ゲームウィンドウが未検出。ゲームを起動してください。',
        'msg_no_game_window_debug': 'ゲームウィンドウが未検出。ゲームを起動するか手動キャプチャしてください。',
        'window_resized': '[ウィンドウを {}x{} にリサイズ]',
        'window_resize_failed': '[ウィンドウリサイズ失敗。管理者として実行してください。]',

        # ダイアログメッセージ
        'msg_select_dir': 'ゲームインストールディレクトリを選択',
        'msg_no_container': 'containerディレクトリが見つかりません\nパス: {}\n\nパスを確認するか、containerディレクトリを直接選択してください',
        'msg_scan_done': 'スキャン完了: {}個のパッケージ (スキップ{}個>1G, {}個meta), ワーカー: {}',
        'msg_no_pkg_scanned': '先にパッケージをスキャンしてください',
        'msg_search_start': '検索開始 | 方式: {}, タイプ: {}, 名前: {}, パッケージ: {}, ワーカー: {}',
        'msg_pre_search': '[事前検索] キャッシュされた{}個のパッケージを試行',
        'msg_pre_search_hit': '[事前検索] ヒット、全スキャンをスキップ',
        'msg_pre_search_miss': '[事前検索] 不十分、全スキャンにフォールバック',
        'msg_search_found': '[発見] {} ({}) in {} エントリ#{}',
        'msg_search_excluded': '[除外] {} in {}',
        'msg_quick_stop': '[クイック] {}個のパッケージを発見、停止',
        'msg_search_stopped': 'ユーザーが検索を停止',
        'msg_search_complete': '{}件の有効な一致を発見\n名刺とアバターリソースを自動割り当てしました',
        'msg_search_no_result': '{}個のパッケージに一致なし',
        'msg_select_result': '検索結果を先に選択してください',
        'msg_no_crop_image': '切り抜く画像がありません',
        'msg_crop_done': '{}画像をキャッシュに保存\n解像度: {}x{}',
        'msg_no_task': '先に画像を選択して切り抜いてください',
        'msg_apply_done': 'パッケージファイルを変更しました。ゲームが起動できない場合は「復元」をクリックしてください。',
        'msg_apply_error': '変更適用エラー。ログを確認してください。',
        'msg_asset_index_high': '現在のリソースは番号が大きく（12超）、ゲーム内の表示位置が後方になります。\n予期した場所に置き換えが見つからない場合は、下にスクロールして探してください。',
        'msg_no_backup': 'バックアップファイルが見つかりません',
        'msg_restore_done': '{}個のバックアップファイルを復元しました。\nゲームを再起動して確認してください。',
        'msg_confirm_exit': '終了するとバックアップを自動復元しキャッシュをクリアします。\n続行しますか？',
        'msg_confirm_exit_title': '終了確認',
        'msg_exit_while_applying': 'ゲームファイルに変更を適用中です。完了してから終了してください。',
        'msg_not_admin': 'プログラムが管理者権限で実行されていないため、一部の機能が正常に動作しない可能性があります。問題が発生した場合は、管理者としての実行をお試しください。',
        'msg_image_load_failed': '画像を読み込めません:\n{}\n\nエラー: {}',
        'msg_image_invalid': '画像を読み込めません:\n{}\n\n無効な画像データ',
        'msg_image_process_failed': '画像処理エラー:\n{}\n\nエラー: {}',
        'msg_image_load_title': '画像読込失敗',
        'msg_image_process_title': '画像処理失敗',

        # ファイルダイアログ
        'file_select_card': '名刺画像を選択',
        'file_select_avatar': 'アバター画像を選択',
        'file_filter_image': '画像 (*.png *.jpg *.jpeg *.bmp);;All (*)',

        # プレビュー
        'preview_title': 'プレビュー',
        'preview_title_size': 'プレビュー - {}x{}',
        'easter_egg_hint': 'まだ画像が選択されていません！拡大プレビューできませんよ～',

        # ログ
        'log_card_saved': '[名刺] 切り抜きを cache/card_custom.png に保存',
        'log_avatar_saved': '[アバター] 切り抜きを cache/avatar_custom.png に保存',

        # 情報ダイアログタイトル
        'dialog_tutorial_title': 'チュートリアル',
        'dialog_faq_title': 'FAQ',
        'dialog_about_title': 'について',
        'dialog_settings_title': '設定',

        # 設定
        'settings_language': 'インターフェース言語',
        'settings_debug': 'デバッグモード',
        'settings_debug_hint': '有効にすると logs/ ディレクトリにデバッグログを生成',
        'settings_confirm_exit': '終了時に確認ダイアログを表示',
        'settings_confirm_exit_hint': 'プログラム終了時に確認ダイアログが表示されます',
        'settings_other': 'その他の設定',
        'settings_saved': '設定を保存しました',
        'settings_about': 'このツールについて',
        'settings_about_btn': 'について開く',
        'settings_restart_hint': '言語変更は再起動後に完全反映されます',
        'settings_btn_save': '保存',
        'settings_btn_close': '閉じる',
        'settings_restart_now': '言語が変更されました。再起動が必要です。\n今すぐ再起動しますか？',
        'settings_restart_title': '再起動が必要',
        'settings_debug_restarted': 'デバッグモード設定を保存しました。再起動後に有効になります',

        # ウィンドウキャプチャ
        'capture_confirm_title': 'ゲームウィンドウ確認',
        'capture_confirm_text': '<b>タイトル:</b> {}<br><b>プロセス:</b> {}<br><b>PID:</b> {}<br><b>HWND:</b> {}<br><br>このウィンドウをゲームウィンドウとして使用しますか？',
        'capture_pid_label': '(PID: {})',

        # デバッグパネル
        'debug_resize_title': '【デバッグ】ウィンドウ解像度テスト',
        'debug_label_w': '幅:',
        'debug_label_h': '高:',
        'debug_label_scale': '倍率%:',
        'debug_btn_apply': '適用',
        'debug_resize_log': '[デバッグ] ウィンドウを {}x{} にリサイズ (元 {}x{} @ {}%)',
        'debug_resize_fail': '[デバッグ] ウィンドウリサイズ失敗',
    },
}


# ============================================================
# CARD_STEPS / AVATAR_STEPS 三语版本
# action 配置从 constants.py 导入，这里只提供 text/hint
# ============================================================

_CARD_STEP_ACTIONS = [
    None,
    ('resize', 500, 2000, 100),
    ('resize', 500, 5735, 20),
    ('resize', 500, 5735, 100),
    ('resize', 1600, 900, 100),
]

_AVATAR_STEP_ACTIONS = [
    None,
    ('resize', 545, 2152, 100),
    None,
    ('resize', 1600, 900, 100),
]


def _build_steps(texts, actions):
    result = []
    for text_info, action in zip(texts, actions):
        step = {
            'text': text_info['text'],
            'hint': text_info['hint'],
            'hint_color': text_info.get('hint_color', 'green'),
            'action': action,
        }
        result.append(step)
    return result


_CARD_STEPS_TEXTS = {
    'zh': [
        {'text': '1.进入协会并站在拍照点位。', 'hint': '完成后点击「下一步」进入下一步。', 'hint_color': 'green'},
        {'text': '2.选中"拍名片"后按F进入界面。在角色动作中选择「坐下」坐下后点击暂停动作。随后在背景中选中我们要自定义的图片。', 'hint': '完成后点击「下一步」进入下一步。', 'hint_color': 'green'},
        {'text': '3.游戏窗口变得更细长后，回到游戏，拖动鼠标将橙色的摄像框向上拖到最顶端。', 'hint': '完成后点击「下一步」进入下一步。', 'hint_color': 'green'},
        {'text': '4.游戏窗口分辨率发生变化后，再次手动上下随意拖动一下橙色摄像框，<span style="color:red;">否则名片会无法正常显示。</span>拖动完毕后按 V 拍照。', 'hint': '完成后点击「下一步」进入下一步。', 'hint_color': 'green'},
        {'text': '5.名片已更改完毕。点击确认上传即可。', 'hint': '完成后点击「下一步」完成流程。', 'hint_color': 'green'},
    ],
    'en': [
        {'text': '1. Enter the guild and stand at the photo spot.', 'hint': 'Click "Next" when done.', 'hint_color': 'green'},
        {'text': '2. Select "Take Profile Card", press F to enter. Choose the "Sit" pose and pause it. Then select the background image to customize.', 'hint': 'Click "Next" when done.', 'hint_color': 'green'},
        {'text': '3. After the window becomes tall and narrow, go back to the game and drag the orange camera frame to the very top.', 'hint': 'Click "Next" when done.', 'hint_color': 'green'},
        {'text': '4. After the resolution changes, <span style="color:red;">manually drag the orange camera frame up and down a bit, otherwise the card will not display correctly.</span> Then press V to take a photo.', 'hint': 'Click "Next" when done.', 'hint_color': 'green'},
        {'text': '5. Card replacement is complete. Click confirm to upload.', 'hint': 'Click "Next" to finish.', 'hint_color': 'green'},
    ],
    'ja': [
        {'text': '1. ギルドに入り、撮影スポットに立つ。', 'hint': '完了したら「次へ」をクリック。', 'hint_color': 'green'},
        {'text': '2. 「プロフィールカード撮影」を選択し、Fキーで进入。「座る」ポーズを選択して一時停止。カスタマイズしたい背景画像を選択。', 'hint': '完了したら「次へ」をクリック。', 'hint_color': 'green'},
        {'text': '3. ウィンドウが細長くなったら、ゲームに戻り、オレンジ色の撮影フレームを一番上までドラッグ。', 'hint': '完了したら「次へ」をクリック。', 'hint_color': 'green'},
        {'text': '4. 解像度が変更されたら、<span style="color:red;">オレンジ色の撮影フレームを上下にドラッグしてください。そうしないとカードが正しく表示されません。</span>その後Vキーで撮影。', 'hint': '完了したら「次へ」をクリック。', 'hint_color': 'green'},
        {'text': '5. 名刺の変更が完了しました。アップロードを確認してください。', 'hint': '「次へ」をクリックして完了。', 'hint_color': 'green'},
    ],
}

_AVATAR_STEPS_TEXTS = {
    'zh': [
        {'text': '1.进入协会并站在拍照点位。', 'hint': '完成后点击「下一步」进入下一步。', 'hint_color': 'green'},
        {'text': '2.选中"拍头像"后按F进入界面。在角色动作中选择「坐下」坐下后点击暂停动作。随后在背景中选中我们要自定义的图片。', 'hint': '完成后点击「下一步」进入下一步。', 'hint_color': 'green'},
        {'text': '3.拖动橙色摄像框到合适的位置后，按 V 拍照。', 'hint': '完成后点击「下一步」进入下一步。', 'hint_color': 'green'},
        {'text': '4.头像已更改完毕。点击确认上传即可。', 'hint': '完成后点击「下一步」完成流程。', 'hint_color': 'green'},
    ],
    'en': [
        {'text': '1. Enter the guild and stand at the photo spot.', 'hint': 'Click "Next" when done.', 'hint_color': 'green'},
        {'text': '2. Select "Take Avatar", press F to enter. Choose the "Sit" pose and pause it. Then select the background image to customize.', 'hint': 'Click "Next" when done.', 'hint_color': 'green'},
        {'text': '3. Drag the orange camera frame to the desired position, then press V to take a photo.', 'hint': 'Click "Next" when done.', 'hint_color': 'green'},
        {'text': '4. Avatar replacement is complete. Click confirm to upload.', 'hint': 'Click "Next" to finish.', 'hint_color': 'green'},
    ],
    'ja': [
        {'text': '1. ギルドに入り、撮影スポットに立つ。', 'hint': '完了したら「次へ」をクリック。', 'hint_color': 'green'},
        {'text': '2. 「アバター撮影」を選択し、Fキーで进入。「座る」ポーズを選択して一時停止。カスタマイズしたい背景画像を選択。', 'hint': '完了したら「次へ」をクリック。', 'hint_color': 'green'},
        {'text': '3. オレンジ色の撮影フレームを適切な位置にドラッグし、Vキーで撮影。', 'hint': '完了したら「次へ」をクリック。', 'hint_color': 'green'},
        {'text': '4. アバターの変更が完了しました。アップロードを確認してください。', 'hint': '「次へ」をクリックして完了。', 'hint_color': 'green'},
    ],
}


_CARD_STEPS = {
    lang: _build_steps(texts, _CARD_STEP_ACTIONS)
    for lang, texts in _CARD_STEPS_TEXTS.items()
}

_AVATAR_STEPS = {
    lang: _build_steps(texts, _AVATAR_STEP_ACTIONS)
    for lang, texts in _AVATAR_STEPS_TEXTS.items()
}


# ============================================================
# EULA / Tutorial / FAQ / About HTML 三语版本
# ============================================================

_EULA_TEMPLATES = {
    'zh': (
        "<h3>用户协议</h3><hr>"
        "<p>本工具完全免费且开源（GPL-3.0），原理为修改本地游戏文件，"
        "可能导致游戏损坏、数据异常，并存在封号风险。<br>"
        "请自行决定是否使用，作者不对任何后果负责。</p>"
        "<p style='color:red;'><b>程序版本为v{version} 可能存在漏洞，若发现漏洞可以拷打麦片。</b></p>"
    ),
    'en': (
        "<h3>User Agreement</h3><hr>"
        "<p>This tool is completely free and open source (GPL-3.0). "
        "It modifies local game files, which may cause game corruption, "
        "data anomalies, and account suspension risk.<br>"
        "Use at your own risk. The author assumes no responsibility.</p>"
        "<p style='color:red;'><b>Version v{version} may have bugs. Report any issues to the author.</b></p>"
    ),
    'ja': (
        "<h3>利用規約</h3><hr>"
        "<p>このツールは完全無料のオープンソース（GPL-3.0）です。ローカルゲームファイルを変更するため、"
        "ゲームの破損、データ異常、アカウント停止のリスクがあります。<br>"
        "自己責任でご使用ください。作者は一切の責任を負いません。</p>"
        "<p style='color:red;'><b>バージョン v{version} にはバグがある可能性があります。問題があれば報告してください。</b></p>"
    ),
}


_TUTORIAL_HTML = {
    'zh': """
<h2>使用教程</h2>
<hr>
<h3>第一步：选择游戏目录</h3>
<p>点击「选择目录」，找到星痕共鸣的安装文件夹。<br>
通常路径类似：<code>D:\\WeGameApps\\rail_apps\\STAR RESONANSE(2001991)...</code>，程序会自动识别数据包所在位置。</p>

<h3>第二步：查找资源</h3>
<p>点击「扫描数据包」后，再点击「开始查找」。<br>
程序会自动在数据包中搜索名片和头像相关的图片资源。<br>
找到后会自动分配为名片和头像，显示在下方表格中。</p>

<h3>第三步：编辑图片</h3>
<p style="color:red;"><b>注意！请务必先打开游戏进入协会，再进行下面的步骤，否则加载页面会卡死。</b></p>
<p>切换到「编辑图片」选项卡：<br>
1. 点击「选择名片图片」或「选择头像图片」，选择你想要的图片<br>
2. 在左侧预览区拖动蓝色选框，调整裁剪范围<br>
3. 拖动选框外的区域可以平移图片，选框保持不动<br>
4. 可以调节亮度、对比度、饱和度、色温来微调效果<br>
5. 每项调节旁的 +/- 按钮可微调<br>
6. 点击「复位图片」可重置位置和缩放，「重置图片」可恢复调节参数<br>
7. 点击预览框可弹出大图预览窗口，调整参数时实时更新<br>
8. 点击「确认裁剪」保存<br>
9. 裁剪完成后点击「下一步」</p>

<h3>第四步：更换操作</h3>
<p>切换到「更换操作」选项卡：<br>
1. 先启动游戏，确保程序检测到游戏窗口（显示绿色"已连接"）<br>
2. <b>如果未检测到游戏（如台服、日服、国际服等），点击「手动捕获游戏窗口」按钮，然后点击游戏窗口即可</b><br>
3. <b>若手动捕获仍无效，请尝试以管理员权限运行本程序</b><br>
4. <b>请先将游戏从全屏切换为窗口化！</b><br>
5. 进入游戏中的协会，站在拍照点位<br>
6. 点击「开始更换名片」或「开始更换头像」<br>
7. 按照提示一步步操作，每完成一步点击「下一步」<br>
8. 程序会自动调整游戏窗口大小，请按提示操作</p>

<h3>注意事项</h3>
<p>- 替换前请确保已进入协会场景<br>
- 请勿在替换过程中切换场景或关闭游戏<br>
- 如遇问题，点击「还原」按钮可恢复原始文件<br>
- 退出程序时会自动还原备份</p>
""",
    'en': """
<h2>Tutorial</h2>
<hr>
<h3>Step 1: Select Game Directory</h3>
<p>Click "Select Dir" and locate the Blue Protocol: Star Resonance installation folder.<br>
Typical path: <code>...\\Steam\\steamapps\\common\\Star Resonance</code> or your game launcher's install folder<br>
The program will automatically detect the data package location.</p>

<h3>Step 2: Find Resources</h3>
<p>Click "Scan Packages", then click "Start Search".<br>
The program will search for profile card and avatar resources in the data packages.<br>
Results are auto-assigned as card and avatar, shown in the table below.</p>

<h3>Step 3: Edit Image</h3>
<p style="color:red;"><b>Important! Launch the game and enter the guild BEFORE this step, or the loading screen will freeze.</b></p>
<p>Switch to the "Edit Image" tab:<br>
1. Click "Select Card Image" or "Select Avatar Image" to choose your image<br>
2. Drag the blue selection box in the preview area to adjust the crop range<br>
3. Drag outside the selection box to pan the image (box stays fixed)<br>
4. Adjust brightness, contrast, saturation, and color temperature<br>
5. Use +/- buttons for fine adjustment<br>
6. Click "Reset Position" to reset position/zoom, "Reset Image" to restore parameters<br>
7. Click the preview area for a large preview window (real-time updates)<br>
8. Click "Confirm Crop" to save<br>
9. After cropping, click "Next"</p>

<h3>Step 4: Apply Changes</h3>
<p>Switch to the "Apply Changes" tab:<br>
1. Launch the game and ensure it's detected (green "Connected")<br>
2. <b>If not detected (TW, JP, international servers), click "Capture Game Window" and click the game window</b><br>
3. <b>If capture fails, try running as administrator</b><br>
4. <b>Switch the game from fullscreen to windowed mode first!</b><br>
5. Enter the guild and stand at the photo spot<br>
6. Click "Replace Card" or "Replace Avatar"<br>
7. Follow the prompts step by step, clicking "Next" after each step<br>
8. The program will automatically adjust the game window size</p>

<h3>Notes</h3>
<p>- Make sure you've entered the guild before replacing<br>
- Do not switch scenes or close the game during replacement<br>
- Click "Restore" to recover original files if issues occur<br>
- Backups are automatically restored on exit</p>
""",
    'ja': """
<h2>チュートリアル</h2>
<hr>
<h3>ステップ 1：ゲームディレクトリの選択</h3>
<p>「ディレクトリ選択」をクリックし、星痕共鳴のインストールフォルダを選択。<br>
一般的なパス：<code>...\\Steam\\steamapps\\common\\Star Resonance</code> またはゲームランチャーのインストールフォルダ<br>
プログラムが自動的にデータパッケージの場所を検出します。</p>

<h3>ステップ 2：リソースの検索</h3>
<p>「パッケージスキャン」をクリック後、「検索開始」をクリック。<br>
データパッケージ内のプロフィールカードとアバターのリソースを自動検索します。<br>
結果は名刺とアバターに自動割り当てされ、下のテーブルに表示されます。</p>

<h3>ステップ 3：画像の編集</h3>
<p style="color:red;"><b>重要！先にゲームを起動してギルドに入ってからこのステップを行ってください。そうしないとロード画面がフリーズします。</b></p>
<p>「画像編集」タブに切り替え：<br>
1. 「名刺画像を選択」または「アバター画像を選択」をクリック<br>
2. プレビューエリアの青い選択枠をドラッグして切り抜き範囲を調整<br>
3. 選択枠の外側をドラッグして画像を移動（選択枠は固定）<br>
4. 明るさ、コントラスト、彩度、色温度を調整<br>
5. +/- ボタンで微調整<br>
6. 「位置リセット」で位置/ズームをリセット、「画像リセット」でパラメータを復元<br>
7. プレビューエリアをクリックで拡大プレビュー（リアルタイム更新）<br>
8. 「切り抜き確定」をクリックして保存<br>
9. 切り抜き後、「次へ」をクリック</p>

<h3>ステップ 4：交換作業</h3>
<p>「交換作業」タブに切り替え：<br>
1. ゲームを起動し、検出されていることを確認（緑色の「接続済み」）<br>
2. <b>検出されない場合（台湾、日本、国際サーバー等）、「ゲームウィンドウをキャプチャ」をクリックし、ゲームウィンドウをクリック</b><br>
3. <b>キャプチャが失敗する場合、管理者として実行してください</b><br>
4. <b>先にゲームをフルスクリーンからウィンドウモードに切り替えてください！</b><br>
5. ギルドに入り、撮影スポットに立つ<br>
6. 「名刺を交換」または「アバターを交換」をクリック<br>
7. 画面の指示に従い、各ステップ完了後に「次へ」をクリック<br>
8. プログラムが自動的にゲームウィンドウサイズを調整します</p>

<h3>注意事項</h3>
<p>- 交換前にギルドシーンに入っていることを確認<br>
- 交換中にシーンを切り替えたりゲームを閉じないでください<br>
- 問題があれば「復元」ボタンで元のファイルを復元<br>
- 終了時にバックアップを自動復元</p>
""",
}


_FAQ_HTML = {
    'zh': """
<h2>常见问题 FAQ</h2>
<hr>
<p><b>Q. 为什么图片能选择的位置那么小？</b><br>
A. 因为要适配星痕共鸣的名片大小。请你选一张基础分辨率没那么大的图片进行替换。</p>

<p><b>Q. 为什么查找的进度条这么慢？</b><br>
A. 使用的是适用性很高的自搜索方法寻找替换的文件。优点是游戏更新也不影响使用、国际服、港澳台服也适配。缺点是依赖CPU、内存、磁盘性能。</p>

<p><b>Q. 为什么替换时窗口分辨率没有改变？</b><br>
A. 请在开始前先手动将全屏的游戏窗口改为窗口化。或尝试以管理员权限启动本程序。</p>

<p><b>Q. 为什么进度条卡45%？</b><br>
A. 请不要替换文件之后再启动游戏/切换场景。请先进入协会，再进行文件的替换。</p>

<p><b>Q. 游戏出问题了！闪退/游戏内有诡异现象（如建模消失等）</b><br>
A. 可能是替换后还原功能出问题了，请在WEGAME手动点击修复游戏尝试修复。</p>

<p><b>Q. 为什么替换出来的名片拍出来是灰色的？</b><br>
A. 未在向上拖动完橙色取相框后的下一步再次上下拖动一下取相框，请认真看提示。</p>

<p><b>Q. 国服之外的比如国际服、港澳台服可以使用吗？</b><br>
A. 理论上是没问题，可以试试，有问题就找我反馈。</p>
""",
    'en': """
<h2>FAQ</h2>
<hr>
<p><b>Q. Why is the image selection area so small?</b><br>
A. It must fit the BPSR card size. Choose an image with smaller base resolution.</p>

<p><b>Q. Why is the search progress bar so slow?</b><br>
A. The program uses a self-search method that works after game updates and supports all servers. Speed depends on CPU, memory, and disk performance.</p>

<p><b>Q. Why doesn't the window resolution change during replacement?</b><br>
A. Switch the game from fullscreen to windowed mode before starting. Or try running as administrator.</p>

<p><b>Q. Why is the progress bar stuck at 45%?</b><br>
A. Do not launch the game or switch scenes after replacing files. Enter the guild first, then replace.</p>

<p><b>Q. The game is broken! Crashes or missing models?</b><br>
A. The restore function may have failed. Manually repair the game through Steam or your game launcher.</p>

<p><b>Q. Why is the card photo gray?</b><br>
A. You didn't drag the orange camera frame up and down in Step 4. Follow the instructions carefully.</p>

<p><b>Q. Can I use this on international, TW, HK/Macau servers?</b><br>
A. Theoretically yes. Try it and report any issues.</p>
""",
    'ja': """
<h2>よくある質問</h2>
<hr>
<p><b>Q. 画像の選択範囲がとても小さいのはなぜ？</b><br>
A. 星痕共鳴のカードサイズに合わせる必要があるためです。解像度が小さめの画像を選んでください。</p>

<p><b>Q. 検索の進行状況がとても遅いのはなぜ？</b><br>
A. ゲームアップデート後も使用可能で、全サーバーに対応した自己検索方式を使用しています。速度はCPU、メモリ、ディスク性能に依存します。</p>

<p><b>Q. 交換時にウィンドウ解像度が変わらないのはなぜ？</b><br>
A. 開始前にゲームをフルスクリーンからウィンドウモードに切り替えてください。または管理者として実行してください。</p>

<p><b>Q. 進行状況バーが45%で止まるのはなぜ？</b><br>
A. ファイル置換後にゲームを起動したりシーンを切り替えたりしないでください。先にギルドに入ってから置換してください。</p>

<p><b>Q. ゲームが壊れた！クラッシュやモデル消失？</b><br>
A. 復元機能に問題があった可能性があります。Steamやゲームランチャーで手動修復してください。</p>

<p><b>Q. カード写真がグレーになるのはなぜ？</b><br>
A. ステップ4でオレンジ色の撮影フレームを上下にドラッグしていません。指示に従ってください。</p>

<p><b>Q. 国際サーバーや台湾、香港/澳門サーバーでも使えますか？</b><br>
A. 理論上は可能です。試して問題があれば報告してください。</p>
""",
}


_ABOUT_HTML = {
    'zh': """
<h2>关于</h2>
<hr>
<p><b>麦麦子名片头像修改工具</b></p>
<p>作者：麦片</p>
<p>GitHub：<a href="https://github.com/OatmeaILL" style="color: #3498db;">https://github.com/OatmeaILL</a></p>
<br>
<p style="font-size: 14px; color: #e67e22;">
<b>作者本人8级活跃协会【瑝珑】，编号40384，<br>
交流群150+，收人拉！！<br>
进群咨询、获取最新版本！！！</b></p>
<hr>
<p style="font-size: 11px; color: #999;">
<b>免责声明</b><br>
本工具完全免费且开源（GPL-3.0），请勿购买任何付费副本，<br>
原理为修改本地游戏文件，可能导致游戏损坏、数据异常，并存在封号风险。<br>
请自行决定是否使用，作者不对任何后果负责。</p>
""",
    'en': """
<h2>About</h2>
<hr>
<p><b>Maimai BPSR Profile & Avatar Customizer</b></p>
<p>Author: OatmeaILL</p>
<p>GitHub: <a href="https://github.com/OatmeaILL" style="color: #3498db;">https://github.com/OatmeaILL</a></p>
<br>
<p style="font-size: 14px; color: #e67e22;">
<b>Level 8 active guild【瑝珑】, ID: 40384<br>
Join the community for support and latest versions!</b></p>
<hr>
<p style="font-size: 11px; color: #999;">
<b>Disclaimer</b><br>
This tool is completely free and open source (GPL-3.0). Please do not pay for it.<br>
It modifies local game files, which may cause<br>
game corruption, data anomalies, and account suspension risk.<br>
Use at your own risk. The author assumes no responsibility.</p>
""",
    'ja': """
<h2>について</h2>
<hr>
<p><b>麦麦子 BPSR 名刺・アバター変更ツール</b></p>
<p>作者：OatmeaILL</p>
<p>GitHub：<a href="https://github.com/OatmeaILL" style="color: #3498db;">https://github.com/OatmeaILL</a></p>
<br>
<p style="font-size: 14px; color: #e67e22;">
<b>レベル8アクティブギルド【瑝珑】、ID: 40384<br>
コミュニティに参加してサポートと最新バージョンを入手！</b></p>
<hr>
<p style="font-size: 11px; color: #999;">
<b>免責事項</b><br>
このツールは完全無料のオープンソース（GPL-3.0）です。有料の副本を購入しないでください。<br>
ローカルゲームファイルを変更するため、ゲームの破損、データ異常、<br>
アカウント停止のリスクがあります。<br>
自己責任でご使用ください。作者は一切の責任を負いません。</p>
""",
}
