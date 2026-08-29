# StarResonance-ProfileCustomizer

<img src="./xmp.png" width="50%">

星痕共鸣（Blue Protocol: Star Resonance / BPSR）名片/头像自定义修改工具  
Profile & Avatar Customization Tool for Blue Protocol: Star Resonance (BPSR)

[中文](#中文) | [English](#english) | [日本語](#日本語)

---

# 中文

## 简介

**麦麦子名片头像修改工具** 是一款用于修改《星痕共鸣》（Blue Protocol: Star Resonance / BPSR）游戏内名片和头像的 PC 桌面工具。  
通过替换本地游戏文件的方式，将你喜欢的图片设置为游戏中的名片或头像。

> ⚠ **本工具仅供交流与学习使用，完全免费，禁止倒卖。修改本地文件可能导致封号风险，请自行决定是否使用。**

---

## 功能一览

- **自动检索** — 自动扫描游戏数据包（.pkg），搜索名片和头像相关的 Texture2D 资源
- **图片编辑** — 内置图片编辑器：选框裁剪、亮度/对比度/饱和度/色温调节、缩放、图片平移
- **一键替换** — 异步执行，进度条实时显示，不卡界面
- **交互式更换流程** — 自动调整游戏窗口分辨率，分步引导完成拍照
- **备份还原** — 修改前自动备份原始文件，异常时自动还原，退出程序自动还原
- **多服务器兼容** — 支持国服、台服、港澳服、日服、国际服
- **手动窗口捕获** — 自动检测失败时可手动点击游戏窗口捕获

---

## 详细使用教程

### 准备工作

1. 从 [Releases](https://github.com/OatmeaILL/StarResonance-ProfileCustomizer/releases) 下载最新版本的可执行文件（.exe）
2. 双击运行 `麦麦子名片头像修改工具 1.0.7.exe`
3. 首次启动需阅读并同意**用户协议**
4. 同意后会弹出**使用教程**对话框，你可以随时点击主窗口的「教程」按钮再次查看

### 第一步：选择游戏目录

1. 点击主窗口顶部的 **「选择目录」** 按钮
2. 在弹出的文件选择对话框中，找到星痕共鸣的安装文件夹
3. 通常路径类似：`D:\WeGameApps\rail_apps\STAR RESONANSE(2001991)\`
4. 程序会自动识别数据包所在位置（`Star_Data/StreamingAssets/container` 目录）
5. 选择成功后，输入框会显示游戏路径

> **提示**：如果选择目录后提示找不到数据包，请手动确认游戏目录下存在 `Star_Data/StreamingAssets/container` 文件夹。

### 第二步：查找资源

1. 点击 **「扫描数据包」** 按钮，程序会扫描游戏目录下的所有 `.pkg` 文件
2. 扫描完成后，选择查找方式：
   - **快速查找**（推荐）：优先尝试上次使用的数据包路径，命中则跳过全量扫描，速度极快
   - **完整查找**：扫描所有数据包中的每个资源，耗时较长但更彻底
3. 点击 **「开始查找」** 按钮
4. 程序会在后台搜索名片和头像相关的 Texture2D 资源，进度条会实时显示进度
5. 查找完成后，表格中会列出找到的资源，并自动分配为名片和头像
6. 如果找到多个资源，你可以手动在表格中选择不同的资源进行替换

> **关于速度**：查找速度取决于 CPU、内存和磁盘性能。完整查找可能耗时较长，但游戏更新后仍可正常使用，且兼容所有服务器版本。

### 第三步：编辑图片

> **重要**：请务必先打开游戏并进入协会场景，再执行此步骤，否则后续操作会卡死。

1. 切换到 **「编辑图片」** 选项卡
2. 点击 **「选择名片图片」** 或 **「选择头像图片」** 按钮，选择你想要的图片文件（支持 PNG、JPG、BMP 等格式）
3. 在左侧预览区，你会看到加载的图片和一个**蓝色选框**
4. 编辑图片：
   - **调整裁剪范围**：拖动蓝色选框的四个角或边，调整裁剪区域
   - **平移图片**：拖动选框**外部**的区域，可以平移图片，选框保持不动
   - **缩放**：使用滑块或鼠标滚轮，支持 1%~300% 缩放
   - **亮度**：拖动滑块调节（-100 ~ +100），点击 `[R]` 重置，点击 `[-]`/`[+]` 微调
   - **对比度**：同上
   - **饱和度**：控制颜色鲜艳程度，同上
   - **色温**：暖色（偏黄）/ 冷色（偏蓝）偏移，同上
5. 点击 **「复位图片」** 可重置图片位置和缩放
6. 点击 **「重置图片」** 可恢复所有调节参数到默认值
7. 点击预览框可弹出**大图预览窗口**（非模态，可同时操作编辑器并实时更新）
8. 调整满意后，点击 **「确认裁剪」** 保存裁剪结果
9. 点击 **「下一步」** 进入更换操作

### 第四步：更换操作（名片）

> **重要**：请先将游戏从全屏切换为窗口化模式！

1. 切换到 **「更换操作」** 选项卡
2. 确保游戏已启动，且程序检测到游戏窗口（显示绿色"已连接"）
   - 如果未自动检测到，点击 **「手动捕获游戏窗口」**，然后点击游戏窗口
   - 如果手动捕获仍无效，请尝试**以管理员权限运行本程序**
3. 点击 **「开始更换名片」**
4. 按照程序提示逐步操作：

   **步骤 1**：进入协会，站在拍照点位 → 点击「下一步」
   
   **步骤 2**：选中"拍名片"后按 F 进入界面，选择「坐下」动作后点击暂停动作，在背景中选择要自定义的图片 → 点击「下一步」
   > 程序会自动调整窗口大小为细长条状
   
   **步骤 3**：回到游戏，将橙色摄像框**向上拖动到最顶端** → 点击「下一步」
   > 程序会进一步调整窗口分辨率
   
   **步骤 4**：**手动上下拖动一下橙色摄像框**（必须操作，否则名片会显示异常），然后按 V 键拍照 → 点击「下一步」
   > ⚠ 这一步非常重要，不拖动摄像框会拍出灰色照片
   
   **步骤 5**：名片已更改完毕，点击「确认上传」完成流程
   > 程序会自动恢复窗口分辨率

### 第四步：更换操作（头像）

1. 切换到 **「更换操作」** 选项卡
2. 确保游戏窗口已连接
3. 点击 **「开始更换头像」**
4. 按照程序提示逐步操作：

   **步骤 1**：进入协会，站在拍照点位 → 点击「下一步」
   
   **步骤 2**：选中"拍头像"后按 F 进入界面，选择「坐下」动作后点击暂停动作，在背景中选择要自定义的图片 → 点击「下一步」
   > 程序会自动调整窗口大小
   
   **步骤 3**：拖动橙色摄像框到合适位置，按 V 键拍照 → 点击「下一步」
   
   **步骤 4**：头像已更改完毕，点击「确认上传」完成流程

### 还原与备份

- 在更换过程中，程序会自动备份被修改的原始文件
- 任何步骤出现异常，程序会自动从备份还原已修改的文件
- 你也可以随时点击主窗口的 **「还原」** 按钮手动恢复原始文件
- **退出程序时也会自动还原备份**

---

## 常见问题

<details>
<summary>点击展开</summary>

**Q. 为什么图片能选择的位置那么小？**  
A. 因为要适配星痕共鸣的名片大小（468×774 像素）。请选一张基础分辨率不要太大的图片进行替换。

**Q. 为什么查找的进度条这么慢？**  
A. 使用的是自搜索方法，优点是游戏更新也不影响使用，且兼容国际服、港澳台服等。缺点是依赖 CPU、内存、磁盘性能。

**Q. 为什么替换时窗口分辨率没有改变？**  
A. 请确保在开始前已将游戏从全屏切换为窗口化。如果仍然无效，请尝试以管理员权限运行本程序。

**Q. 为什么进度条卡在 45%？**  
A. 请不要替换文件之后再启动游戏或切换场景。请先进入协会场景，再进行文件替换。

**Q. 游戏出问题了！闪退/建模消失等异常现象？**  
A. 点击「还原」按钮可恢复原始文件。如果还原功能也失效，请在 WeGame 手动点击修复游戏。

**Q. 为什么替换出来的名片拍出来是灰色的？**  
A. 未在向上拖动完橙色摄像框后的下一步再次上下拖动摄像框，请严格按照提示操作第 4 步。

**Q. 国际服、港澳台服、日服可以使用吗？**  
A. 可以。程序已支持台服（StarTW.exe）、港澳服（StarHK.exe）、日服（StarJP.exe / BPSRJP.exe）、国际服（BPSR.exe）等进程名的自动检测。如果未检测到，可点击「手动捕获游戏窗口」手动选择。

**Q. 为什么应用修改时进度条不动然后闪退？**  
A. 1.0.4 版本已修复此问题（改为异步子线程执行 + 主线程轮询更新进度）。如仍遇到，请开启 Debug 模式后提交 Issue。

</details>

---

## Debug 模式

如需排查问题，可开启 debug 日志：

1. 点击主窗口顶栏的「设置」按钮
2. 在设置窗口中勾选「调试模式 (Debug)」
3. 点击「保存并重启」，程序将重新启动
4. 日志文件将自动生成在 `logs/` 目录下
5. 排查完毕后建议回到设置窗口取消勾选

---

## 提交 Issue

遇到问题时，请按以下步骤操作：

1. 开启 Debug 模式（见上方说明）
2. 复现问题
3. 在 [Issues](https://github.com/OatmeaILL/StarResonance-ProfileCustomizer/issues) 页面提交
4. 附上 `logs/` 目录下时间最近的日志文件，以便快速定位问题

---

## 更新日志

### 1.0.7

**客户端**
- 预览框与大图预览窗口新增蓝色虚线边框：深色/偏色图片也能看清裁剪边界（仅显示用，不会写入导出的图片）
- 新增预览彩蛋：未载入图片时点击预览框，弹出彩蛋图片与三语提示
- 最大化窗口布局优化：裁剪区、表格等工作区自适应放大，控制面板与按钮限宽不再拉伸变形，预览框随窗口适度变大
- 导入图片后预览框立即刷新，无需先拖动图片
- 新增非管理员权限启动提示
- 修复：程序目录只读时首次启动可能闪退的问题
- 修复：应用修改过程中关闭程序可能导致游戏文件损坏的问题（处理期间禁止退出）
- 修复：最大化状态下关闭程序后，下次启动窗口尺寸异常的问题
- 修复：异常退出残留的旧备份可能在游戏更新后覆盖新游戏文件的问题（备份新鲜度校验）
- 新增 WebP / GIF 图片格式导入支持

> 更早版本的更新记录见 [GitHub Releases](https://github.com/OatmeaILL/StarResonance-ProfileCustomizer/releases)。

## 免责声明

本工具仅供交流与学习使用，**完全免费**，禁止任何形式的倒卖。  
原理为修改本地游戏文件，可能导致游戏损坏、数据异常，并存在**封号风险**。  
请自行决定是否使用，作者不对任何后果负责。

---

## 作者

- 麦片 & GLM5.2
- GitHub: [OatmeaILL](https://github.com/OatmeaILL)
- 8 级活跃协会【瑝珑】，编号 40384

---

# English

## Introduction

**Maimai BPSR Profile & Avatar Customizer** is a PC desktop tool for modifying in-game profile cards (business cards) and avatars in **Blue Protocol: Star Resonance** (BPSR / 星痕共鸣).  
It replaces local game files to set your own images as in-game profile cards or avatars.

> ⚠ **This tool is for learning and communication purposes only. It is completely free. Reselling is strictly prohibited. Modifying local game files may result in account suspension. Use at your own risk.**

---

## Features

- **Auto-search** — Scans game data packages (.pkg) to find Texture2D resources for profile cards and avatars
- **Image Editor** — Built-in editor with crop selection, brightness/contrast/saturation/color temperature adjustment, zoom, and pan
- **One-click Replace** — Async execution with real-time progress bar, no UI freezing
- **Interactive Workflow** — Automatically adjusts game window resolution, step-by-step photo-taking guidance
- **Backup & Restore** — Automatically backs up original files before modification; auto-restore on errors or program exit
- **Multi-server Support** — Compatible with CN, TW, HK, JP, and international servers
- **Manual Window Capture** — Manually select the game window if auto-detection fails

---

## Detailed Tutorial

### Preparation

1. Download the latest executable (.exe) from [Releases](https://github.com/OatmeaILL/StarResonance-ProfileCustomizer/releases)
2. Double-click to run `麦麦子名片头像修改工具 1.0.7.exe`
3. On first launch, read and accept the **User Agreement**
4. A **Tutorial** dialog will appear automatically. You can also click the "Tutorial" button on the main window to view it again

### Step 1: Select Game Directory

1. Click the **"Select Directory"** button at the top of the main window
2. In the file dialog, locate the Blue Protocol: Star Resonance installation folder
3. Typical path: `...\Steam\steamapps\common\Star Resonance\` or your game launcher's install folder
4. The program will automatically detect the data package location (`Star_Data/StreamingAssets/container` folder)
5. Once successful, the game path will be displayed in the input field

> **Tip**: If the program cannot find the data package, manually verify that the `Star_Data/StreamingAssets/container` folder exists in your game directory.

### Step 2: Find Resources

1. Click **"Scan Packages"** to scan all `.pkg` files in the game directory
2. After scanning, choose a search mode:
   - **Quick Search** (recommended): Tries the previously used package path first; skips full scan if found
   - **Full Search**: Scans every resource in all packages; slower but more thorough
3. Click **"Start Search"**
4. The program searches for Texture2D resources related to profile cards and avatars in the background
5. When complete, the results are listed in a table, automatically assigned as card and avatar
6. If multiple resources are found, you can manually select different ones in the table

> **About Speed**: Search speed depends on CPU, memory, and disk performance. Full search may take longer, but it still works after game updates and is compatible with all server versions.

### Step 3: Edit Image

> **Important**: Make sure to launch the game and enter the guild (association) scene **before** this step, or the subsequent operations will freeze.

1. Switch to the **"Edit Image"** tab
2. Click **"Select Card Image"** or **"Select Avatar Image"** to choose your image file (supports PNG, JPG, BMP, etc.)
3. In the left preview area, you'll see the loaded image with a **blue selection box**
4. Edit the image:
   - **Adjust crop area**: Drag the corners or edges of the blue selection box
   - **Pan image**: Drag the area **outside** the selection box to move the image (the selection box stays fixed)
   - **Zoom**: Use the slider or mouse wheel (1%~300%)
   - **Brightness**: Drag the slider (-100 ~ +100), click `[R]` to reset, click `[-]`/`[+]` for fine adjustment
   - **Contrast**: Same as above
   - **Saturation**: Controls color intensity, same as above
   - **Color Temperature**: Warm (yellowish) / Cool (bluish) shift, same as above
5. Click **"Reset Position"** to reset image position and zoom
6. Click **"Reset Image"** to restore all adjustment parameters to defaults
7. Click the preview area to open a **large preview window** (non-modal, real-time updates while editing)
8. When satisfied, click **"Confirm Crop"** to save
9. Click **"Next"** to proceed to the replacement workflow

### Step 4: Apply Changes (Profile Card)

> **Important**: Switch the game from fullscreen to windowed mode before starting!

1. Switch to the **"Apply Changes"** tab
2. Ensure the game is running and the program detects the game window (shows green "Connected")
   - If not detected, click **"Manually Capture Game Window"** and then click on the game window
   - If still not working, try running the program **as administrator**
3. Click **"Replace Profile Card"**
4. Follow the on-screen prompts step by step:

   **Step 1**: Enter the guild (association) and stand at the photo spot → Click "Next"
   
   **Step 2**: Select "Take Profile Card", press F to enter the interface, choose the "Sit" pose and pause it, then select the background image you want to customize → Click "Next"
   > The program will automatically resize the window to a tall, narrow shape
   
   **Step 3**: Go back to the game and **drag the orange camera frame all the way to the top** → Click "Next"
   > The program will further adjust the window resolution
   
   **Step 4**: **Manually drag the orange camera frame up and down a bit** (mandatory, otherwise the card will display incorrectly), then press the V key to take a photo → Click "Next"
   > ⚠ This step is very important! Skipping it will result in a gray photo
   
   **Step 5**: The card has been changed. Click "Confirm Upload" to complete the process
   > The program will automatically restore the window resolution

### Step 4: Apply Changes (Avatar)

1. Switch to the **"Apply Changes"** tab
2. Ensure the game window is connected
3. Click **"Replace Avatar"**
4. Follow the on-screen prompts:

   **Step 1**: Enter the guild and stand at the photo spot → Click "Next"
   
   **Step 2**: Select "Take Avatar", press F to enter the interface, choose the "Sit" pose and pause it, then select the background image → Click "Next"
   > The program will automatically resize the window
   
   **Step 3**: Drag the orange camera frame to the desired position, press V to take a photo → Click "Next"
   
   **Step 4**: The avatar has been changed. Click "Confirm Upload" to complete

### Restore & Backup

- The program automatically backs up original files during modification
- If any step fails, the program will automatically restore modified files from backup
- You can also click the **"Restore"** button on the main window at any time
- **Backups are automatically restored when the program exits**

---

## FAQ

<details>
<summary>Click to expand</summary>

**Q. Why is the image selection area so small?**  
A. It must fit the BPSR card size (468×774 pixels). Choose an image that is not too large in resolution.

**Q. Why is the search progress bar so slow?**  
A. The program uses a self-search method that works even after game updates and is compatible with all server versions. Speed depends on CPU, memory, and disk performance.

**Q. Why doesn't the window resolution change during replacement?**  
A. Make sure to switch the game from fullscreen to windowed mode before starting. If it still doesn't work, try running the program as administrator.

**Q. Why is the progress bar stuck at 45%?**  
A. Do not launch the game or switch scenes after replacing the files. Enter the guild scene first, then replace the files.

**Q. The game is broken! Crashes or missing models?**  
A. Click the "Restore" button to recover original files. If that doesn't work, manually repair the game through Steam or your game launcher.

**Q. Why is the card photo gray?**  
A. You did not drag the orange camera frame up and down in Step 4. Follow the on-screen instructions carefully.

**Q. Can I use this on international servers, Taiwan, Hong Kong/Macau, or Japan servers?**  
A. Yes. The program supports StarTW.exe (Taiwan), StarHK.exe (HK/Macau), StarJP.exe / BPSRJP.exe (Japan), and BPSR.exe (International). If not detected, use "Manually Capture Game Window".

**Q. Why does the progress bar freeze and the program crash during modification?**  
A. Version 1.0.4 fixed this issue (using async sub-thread execution + main thread polling). If it still occurs, enable Debug mode and submit an Issue.

</details>

---

## Debug Mode

To troubleshoot issues, enable debug logging:

1. Click the "Settings" button in the main window top bar
2. Check "Debug Mode" in the Settings window
3. Click "Save & Restart" to restart the program
4. Log files will be generated in the `logs/` directory
5. After troubleshooting, uncheck it in the Settings window

---

## Submitting Issues

1. Enable Debug mode (see above)
2. Reproduce the problem
3. Submit on the [Issues](https://github.com/OatmeaILL/StarResonance-ProfileCustomizer/issues) page
4. Attach the most recent log file from the `logs/` directory

---

## Changelog

### 1.0.7

**Client**
- Preview box and large preview window now draw a dashed blue border: dark or off-color images show their crop boundaries clearly (display only, never saved into exported images)
- New easter egg: clicking the preview box without a loaded image shows an easter egg picture with a trilingual hint
- Maximized window layout improvements: workspace areas (crop view, tables) expand while control panels and buttons stay width-capped; the preview box grows moderately with the window
- Preview thumbnail now refreshes immediately after importing an image
- New notice when the program is not running with administrator privileges
- Fixed a possible crash on first launch when the program folder is read-only
- Fixed possible game file corruption when closing the program while changes are being applied (exit is blocked during processing)
- Fixed abnormal window size on next launch after closing the program while maximized
- Fixed stale leftover backups possibly overwriting newer game files after a game update (backup freshness check)
- Added WebP / GIF image import support

> For older release notes, see [GitHub Releases](https://github.com/OatmeaILL/StarResonance-ProfileCustomizer/releases).

## Disclaimer

This tool is for **learning and communication purposes only**. It is **completely free**. Reselling is strictly prohibited.  
It works by modifying local game files, which may cause game corruption, data anomalies, and **account suspension risk**.  
Use at your own risk. The author assumes no responsibility for any consequences.

---

## Author

- OatmeaILL & GLM5.2
- GitHub: [OatmeaILL](https://github.com/OatmeaILL)
- Level 8 active guild【瑝珑】, ID: 40384

---

# 日本語

## 概要

**麦麦子 BPSR 名刺・アバター変更ツール** は、**星痕共鳴（Blue Protocol: Star Resonance / BPSR）** のゲーム内プロフィールカード（名刺）とアバターを変更するための PC デスクトップツールです。  
ローカルのゲームファイルを置き換えることで、好きな画像をゲーム内のプロフィールカードやアバターとして設定できます。

> ⚠ **このツールは学習・交流目的のみです。完全無料で、転売は固く禁止します。ローカルファイルの変更によりアカウント停止のリスクがあります。自己責任でご使用ください。**

---

## 機能一覧

- **自動検索** — ゲームデータパッケージ（.pkg）をスキャンし、プロフィールカードとアバター用の Texture2D リソースを検索
- **画像エディター** — 内蔵エディター：切り抜き選択、明るさ/コントラスト/彩度/色温度調整、ズーム、画像移動
- **ワンクリック置換** — 非同期実行、リアルタイム進行状況バー表示、UI のフリーズなし
- **対話型ワークフロー** — ゲームウィンドウの解像度を自動調整、段階的に写真撮影をガイド
- **バックアップ＆復元** — 変更前に自動バックアップ、エラー時や終了時に自動復元
- **マルチサーバー対応** — 中国サーバー、台湾、香港/澳門、日本、国際サーバーに対応
- **手動ウィンドウキャプチャ** — 自動検出に失敗した場合、ゲームウィンドウを手動で選択

---

## 詳細チュートリアル

### 準備

1. [Releases](https://github.com/OatmeaILL/StarResonance-ProfileCustomizer/releases) から最新バージョンの実行ファイル（.exe）をダウンロード
2. ダブルクリックで `麦麦子名片头像修改工具 1.0.7.exe` を実行
3. 初回起動時に**利用規約**を読み、同意してください
4. 同意後、**チュートリアル**ダイアログが自動表示されます。メインウィンドウの「チュートリアル」ボタンからも再表示可能

### ステップ 1：ゲームディレクトリの選択

1. メインウィンドウ上部の **「ディレクトリを選択」** ボタンをクリック
2. ファイル選択ダイアログで、星痕共鳴のインストールフォルダを選択
3. 一般的なパス：`...\Steam\steamapps\common\Star Resonance\` またはゲームランチャーのインストールフォルダ
4. プログラムが自動的にデータパッケージの場所を検出します（`Star_Data/StreamingAssets/container` フォルダ）
5. 成功すると、入力フィールドにゲームパスが表示されます

> **ヒント**：データパッケージが見つからない場合は、ゲームディレクトリに `Star_Data/StreamingAssets/container` フォルダが存在するか確認してください。

### ステップ 2：リソースの検索

1. **「パッケージをスキャン」** をクリックし、ゲームディレクトリ内のすべての `.pkg` ファイルをスキャン
2. スキャン完了後、検索モードを選択：
   - **クイック検索**（推奨）：前回使用したパッケージパスを優先的に試行、見つかれば全スキャンをスキップ
   - **完全検索**：すべてのパッケージ内の全リソースをスキャン、時間はかかるがより徹底的
3. **「検索開始」** をクリック
4. バックグラウンドでプロフィールカードとアバターに関連する Texture2D リソースを検索
5. 完了すると、結果がテーブルに表示され、自動的にカードとアバターに割り当てられます
6. 複数のリソースが見つかった場合、テーブルから手動で選択できます

> **速度について**：検索速度は CPU、メモリ、ディスク性能に依存します。完全検索は時間がかかる場合がありますが、ゲームアップデート後も使用可能で、すべてのサーバーバージョンに対応しています。

### ステップ 3：画像の編集

> **重要**：このステップの前に、必ずゲームを起動してギルド（協会）シーンに入ってください。そうしないと後続の操作がフリーズします。

1. **「画像編集」** タブに切り替え
2. **「カード画像を選択」** または **「アバター画像を選択」** をクリックし、画像ファイルを選択（PNG、JPG、BMP などに対応）
3. 左側のプレビューエリアに、読み込まれた画像と**青色の選択枠**が表示されます
4. 画像を編集：
   - **切り抜き範囲の調整**：青色の選択枠の四隅や辺をドラッグ
   - **画像の移動**：選択枠の**外側**をドラッグして画像を移動（選択枠は固定）
   - **ズーム**：スライダーまたはマウスホイール（1%~300%）
   - **明るさ**：スライダーをドラッグ（-100 ~ +100）、`[R]` でリセット、`[-]`/`[+]` で微調整
   - **コントラスト**：同上
   - **彩度**：色の鮮やかさを調整、同上
   - **色温度**：暖色（黄色寄り）/ 寒色（青寄り）にシフト、同上
5. **「位置リセット」** で画像の位置とズームを初期状態に戻す
6. **「画像リセット」** で全ての調整パラメータをデフォルトに戻す
7. プレビューエリアをクリックすると**拡大プレビューウィンドウ**を表示（非モーダル、編集と同時にリアルタイム更新）
8. 満足したら **「切り抜き確定」** をクリックして保存
9. **「次へ」** をクリックして交換作業に進む

### ステップ 4：交換作業（プロフィールカード）

> **重要**：開始前にゲームをフルスクリーンからウィンドウモードに切り替えてください！

1. **「交換作業」** タブに切り替え
2. ゲームが起動しており、プログラムがゲームウィンドウを検出していることを確認（緑色の「接続済み」表示）
   - 検出されない場合、**「ゲームウィンドウを手動キャプチャ」** をクリックし、ゲームウィンドウをクリック
   - それでも無効な場合、**管理者として実行** してみてください
3. **「プロフィールカードを交換」** をクリック
4. 画面の指示に従って操作：

   **ステップ 1**：ギルド（協会）に入り、撮影スポットに立つ → 「次へ」をクリック
   
   **ステップ 2**：「プロフィールカード撮影」を選択し、F キーでインターフェースに入り、「座る」ポーズを選択して一時停止、カスタマイズしたい背景画像を選択 → 「次へ」をクリック
   > プログラムが自動的にウィンドウを細長い形状にリサイズ
   
   **ステップ 3**：ゲームに戻り、**オレンジ色の撮影フレームを一番上までドラッグ** → 「次へ」をクリック
   > プログラムがさらにウィンドウ解像度を調整
   
   **ステップ 4**：**オレンジ色の撮影フレームを上下に少しドラッグ**（必須。これを行わないとカードが正しく表示されません）、その後 V キーで写真を撮影 → 「次へ」をクリック
   > ⚠ この手順は非常に重要です！スキップするとグレーの写真になります
   
   **ステップ 5**：カードの変更が完了しました。「アップロード確定」をクリックして完了
   > プログラムが自動的にウィンドウ解像度を復元

### ステップ 4：交換作業（アバター）

1. **「交換作業」** タブに切り替え
2. ゲームウィンドウが接続されていることを確認
3. **「アバターを交換」** をクリック
4. 画面の指示に従って操作：

   **ステップ 1**：ギルドに入り、撮影スポットに立つ → 「次へ」をクリック
   
   **ステップ 2**：「アバター撮影」を選択し、F キーでインターフェースに入り、「座る」ポーズを選択して一時停止、背景画像を選択 → 「次へ」をクリック
   > プログラムが自動的にウィンドウをリサイズ
   
   **ステップ 3**：オレンジ色の撮影フレームを適切な位置にドラッグし、V キーで撮影 → 「次へ」をクリック
   
   **ステップ 4**：アバターの変更が完了しました。「アップロード確定」をクリックして完了

### 復元とバックアップ

- 交換処理中、プログラムは自動的に変更前のファイルをバックアップ
- エラーが発生した場合、自動的にバックアップからファイルを復元
- メインウィンドウの **「復元」** ボタンからいつでも手動復元可能
- **プログラム終了時にも自動的にバックアップを復元**

---

## よくある質問

<details>
<summary>クリックして展開</summary>

**Q. 画像の選択範囲がとても小さいのはなぜ？**  
A. 星痕共鳴のカードサイズ（468×774 ピクセル）に合わせる必要があるためです。解像度が大きすぎない画像を選んでください。

**Q. 検索の進行状況がとても遅いのはなぜ？**  
A. ゲームアップデート後も使用可能で、全サーバーバージョンに対応した自己検索方式を使用しています。速度は CPU、メモリ、ディスク性能に依存します。

**Q. 交換時にウィンドウ解像度が変わらないのはなぜ？**  
A. 開始前にゲームをフルスクリーンからウィンドウモードに切り替えてください。それでも無効な場合、管理者として実行してみてください。

**Q. 進行状況バーが 45% で止まるのはなぜ？**  
A. ファイルを置換した後にゲームを起動したりシーンを切り替えたりしないでください。先にギルドシーンに入ってからファイルを置換してください。

**Q. ゲームが壊れた！クラッシュやモデル消失が発生？**  
A. 「復元」ボタンをクリックして元のファイルを復元してください。復元が効かない場合は、Steam やゲームランチャーで手動修復を実行してください。

**Q. 交換したカード写真がグレーになるのはなぜ？**  
A. ステップ 4 でオレンジ色の撮影フレームを上下にドラッグしていません。画面の指示に従ってください。

**Q. 国際サーバー、台湾、香港/澳門、日本サーバーでも使えますか？**  
A. はい。StarTW.exe（台湾）、StarHK.exe（香港/澳門）、StarJP.exe / BPSRJP.exe（日本）、BPSR.exe（国際）に対応しています。自動検出されない場合は「ゲームウィンドウを手動キャプチャ」をお試しください。

**Q. 修正中に進行状況バーが止まってプログラムがクラッシュするのはなぜ？**  
A. バージョン 1.0.4 でこの問題を修正しました（非同期サブスレッド実行 + メインスレッドポーリング）。まだ発生する場合は、デバッグモードを有効にして Issue を送信してください。

</details>

---

## デバッグモード

問題を調査するには、デバッグログを有効にします：

1. メインウィンドウ上部の「設定」ボタンをクリック
2. 設定ウィンドウで「デバッグモード」をチェック
3. 「保存して再起動」をクリックしてプログラムを再起動
4. ログファイルが `logs/` ディレクトリに生成されます
5. 調査後は設定ウィンドウでチェックを外してください

---

## Issue の送信

1. デバッグモードを有効にする（上記参照）
2. 問題を再現する
3. [Issues](https://github.com/OatmeaILL/StarResonance-ProfileCustomizer/issues) ページで送信
4. `logs/` ディレクトリの最新ログファイルを添付

---

## 更新履歴

### 1.0.7

**クライアント**
- プレビュー枠と拡大プレビューウィンドウに青い破線ボーダーを追加：暗い色や被った色の画像でも切り抜き範囲を確認しやすくなりました（表示のみで、書き出し画像には含まれません）
- イースターエッグを追加：画像未選択の状態でプレビュー枠をクリックすると、彩蛋画像と三言語のヒントを表示
- 最大化レイアウトの改善：切り抜きビューなどの作業領域は拡大し、コントロールパネルやボタンは幅制限で引き伸ばされなくなりました。プレビュー枠もウィンドウに合わせて適度に拡大
- 画像インポート後、プレビューが即座に更新されるように
- 管理者権限で実行していない場合の注意表示を追加
- 修正：プログラムフォルダが読み取り専用の場合、初回起動時にクラッシュする可能性がある問題
- 修正：変更適用中にプログラムを終了するとゲームファイルが破損する可能性がある問題（適用中は終了をブロック）
- 修正：最大化状態で終了した後、次回起動時のウィンドウサイズが異常になる問題
- 修正：異常終了で残った古いバックアップが、ゲーム更新後に新しいゲームファイルを上書きする可能性がある問題（バックアップ新鮮度チェック）
- WebP / GIF 画像形式のインポートに対応

> それ以前の更新履歴は [GitHub Releases](https://github.com/OatmeaILL/StarResonance-ProfileCustomizer/releases) をご覧ください。

## 免責事項

このツールは**学習・交流目的のみ**です。**完全無料**で、転売は固く禁止します。  
ローカルゲームファイルを変更する原理により、ゲームの破損、データ異常、**アカウント停止のリスク**があります。  
**自己責任**でご使用ください。作者は一切の責任を負いません。

---

## 作者

- OatmeaILL & GLM5.2
- GitHub: [OatmeaILL](https://github.com/OatmeaILL)
- レベル 8 アクティブギルド【瑝珑】、ID: 40384