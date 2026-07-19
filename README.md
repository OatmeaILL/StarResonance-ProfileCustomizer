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
- **快速查找模式** — 优先尝试上次使用的数据包路径，命中则跳过全量扫描
- **多服务器兼容** — 支持国服、台服、港澳服、日服、国际服
- **手动窗口捕获** — 自动检测失败时可手动点击游戏窗口捕获
- **更新检测与公告** — 启动时自动检查更新，顶部公告栏轮播展示

---

## 详细使用教程

### 准备工作

1. 从 [Releases](https://github.com/OatmeaILL/StarResonance-ProfileCustomizer/releases) 下载最新版本的可执行文件（.exe）
2. 双击运行 `麦麦子名片头像修改工具 1.0.6.exe`
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

## 图片编辑器详细说明

| 功能 | 操作方法 |
|------|---------|
| 调整裁剪范围 | 拖动蓝色选框的四个角或边 |
| 平移图片 | 拖动选框外部区域 |
| 缩放 | 滑块或鼠标滚轮（1%~300%） |
| 亮度调节 | 滑块拖动，`[-]`/`[+]` 微调（步长1），`[R]` 重置 |
| 对比度调节 | 同上 |
| 饱和度调节 | 同上 |
| 色温调节 | 同上 |
| 复位图片 | 重置位置和缩放到初始状态 |
| 重置图片 | 恢复所有调节参数到默认值 |
| 大图预览 | 点击预览框弹出大图窗口，实时更新 |

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

### 1.0.6

**客户端**
- 新增「可选更新」机制：服务端发布版本时可勾选"是否可不升级此版本"，客户端首次提醒可点击"略过此次更新"，不再重复打扰
- 新增「记住窗口位置和大小」：每次启动恢复上次窗口位置和尺寸（自动校验屏幕可用性，避免恢复到已断开的显示器）
- 新增「退出确认开关」：设置窗口中可配置是否在退出时弹出确认对话框，立即生效
- 新增滑块拖动时的数值气泡提示
- 新增链接悬停手型光标和 URL 提示框
- 新增资源编号检测：当名片/头像资源编号超过 12 时，分配后提示用户在游戏中向下滚动查找
- 公告栏重构为像素级平滑滚动：先完整显示停顿，再匀速滚动，支持鼠标悬停暂停
- 兼容性修复：`QFontMetrics.horizontalAdvance` 在旧版 PyQt5 上回退到 `width`
- 兼容性修复：`primaryScreen()` 在无显示器场景下增加空指针保护
- 修复退出确认开关重启后不生效的 bug（根因：QScreen 导入异常导致配置加载中断）

**服务端**
- 发布/编辑版本对话框新增「是否可不升级此版本」复选框
- 版本检查接口响应新增 `optional` 字段
- 服务端版本号升级至 1.0.5

### 1.0.5

**客户端**
- 新增多语言支持（中文 / English / 日本語）
- 首次启动弹出语言选择对话框，支持运行时切换语言
- 新增「设置」窗口，可切换界面语言和调试模式
- 顶栏「关于」按钮移至设置窗口内
- 服务端支持按语言统计用户数据
- 修复英文版和日文版程序标题显示不正确的问题
- 修复英文和日文 FAQ 中 WeGame 平台引用的问题，改为 Steam / 游戏启动器
- 修复教程中英文和日文的路径示例，改为通用 Steam 路径
- README 和教程文本三语统一，国际化完整适配

### 1.0.4

**客户端**
- 修复修改名片后，游戏中名片最下方有几个像素宽度的异常像素区域的问题
- 异步应用修改，界面不再卡顿
- 异常自动还原：应用修改失败时自动从备份恢复已修改的游戏文件
- 预查找机制：快速查找模式优先尝试上次使用的数据包路径，命中则跳过全量扫描
- 图片编辑器新增 `[R]` 按钮（每项调节旁增加重置按钮）
- 修复首次启动未弹出教程对话框的问题
- 降低崩溃风险
- 窗口调整成功判断修正
- 客户端体积优化（约减少 10MB）
- 客户端重构，提升效率

### 1.0.3

- 修复导入部分图片时程序闪退的问题
- 修复可能闪退的兼容性问题
- 新增 debug 日志系统
- 优化图片加载，防止闪退

### 1.0.2

- 新增「手动捕获游戏窗口」功能
- 扩展游戏进程自动检测（支持台服、国际服等）
- 窗口标题多语言匹配
- 教程更新

### 1.0.1

- 图片编辑器交互优化（缩放保持选框相对位置）
- 新增图片平移功能
- 新增「复位图片」和「重置图片」按钮
- 新增饱和度、色温调节
- 新增 +/- 微调按钮（步长1）
- 新增大图预览窗口（非模态，实时更新）
- 修复选框包含图片外区域时预览异常拉伸的问题
- 修复快速拖动图片时整数溢出闪退的问题
- 编译优化，exe 体积减小

### 1.0.0

- 正式版发布
- 更新检测与公告系统
- 图片裁剪编辑器优化
- 安全修复

---

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
- **Quick Search Mode** — Tries the previously used package path first for faster searching
- **Multi-server Support** — Compatible with CN, TW, HK, JP, and international servers
- **Manual Window Capture** — Manually select the game window if auto-detection fails
- **Update Check & Announcements** — Auto-checks for updates on startup, announcement carousel bar

---

## Detailed Tutorial

### Preparation

1. Download the latest executable (.exe) from [Releases](https://github.com/OatmeaILL/StarResonance-ProfileCustomizer/releases)
2. Double-click to run `麦麦子名片头像修改工具 1.0.6.exe`
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

## Image Editor Reference

| Feature | How to Use |
|---------|-----------|
| Adjust crop area | Drag the corners or edges of the blue selection box |
| Pan image | Drag the area outside the selection box |
| Zoom | Slider or mouse wheel (1%~300%) |
| Brightness | Slider drag, `[-]`/`[+]` fine adjustment (step 1), `[R]` reset |
| Contrast | Same as above |
| Saturation | Same as above |
| Color Temperature | Same as above |
| Reset Position | Reset position and zoom to initial state |
| Reset Image | Restore all adjustment parameters to defaults |
| Large Preview | Click the preview area to open a large preview window |

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

### 1.0.6

**Client**
- New "Optional Update" mechanism: server can mark a version as skippable when publishing; clients can click "Skip This Update" on first prompt to avoid repeated notifications
- New "Remember window position and size": restores the previous window geometry on launch (with screen availability check to avoid restoring to a disconnected display)
- New "Exit confirmation toggle": configurable in Settings, takes effect immediately
- New slider value tooltip shown while dragging
- New link hover cursor (pointing hand) and URL tooltip
- New resource index detection: when card/avatar resource index exceeds 12, a hint is shown after assignment telling the user to scroll down in-game
- Announcement bar rebuilt with pixel-level smooth scrolling: displays the full text first, pauses, then scrolls linearly; mouse hover pauses scrolling
- Compatibility fix: `QFontMetrics.horizontalAdvance` now falls back to `width` on older PyQt5
- Compatibility fix: `primaryScreen()` now has a null-pointer guard for headless/disconnected-display scenarios
- Fixed exit-confirmation toggle not persisting across restarts (root cause: QScreen import error aborted config loading)

**Server**
- Added "Can skip this version" checkbox to the publish/edit version dialog
- Added `optional` field to the version check API response
- Server version bumped to 1.0.5

### 1.0.5

**Client**
- Added multilingual support (Chinese / English / Japanese)
- Language selection dialog on first launch, with runtime language switching
- Added "Settings" window for language and debug mode switching
- Moved "About" button from top bar to Settings window
- Server now tracks user data by language
- Fixed incorrect program title display for English and Japanese versions
- Replaced WeGame references in FAQ/Tutorials with Steam / game launcher for international users
- Unified tutorial and README text across all three languages

### 1.0.4

**Client**
- Fixed abnormal pixel area at the bottom of profile cards in-game
- Async modification application, no more UI freezing
- Auto-restore on failure: automatically restores backed-up files when modification fails
- Pre-search mechanism: quick search tries the last used package path first
- Added `[R]` reset buttons for all adjustment parameters
- Fixed tutorial dialog not showing on first launch
- Reduced crash risk
- Fixed window resize success detection
- Client size optimization (~10MB reduction)
- Client refactoring for improved efficiency

### 1.0.3

- Fixed crash when importing certain images
- Fixed compatibility crash issues
- Added debug logging system
- Optimized image loading to prevent crashes

### 1.0.2

- Added "Manually Capture Game Window" feature
- Extended game process auto-detection (supports TW, international servers, etc.)
- Multi-language window title matching
- Tutorial updates

### 1.0.1

- Image editor interaction optimization (zoom preserves selection box position)
- Added image panning feature
- Added "Reset Position" and "Reset Image" buttons
- Added saturation and color temperature adjustment
- Added +/- fine adjustment buttons (step 1)
- Added large preview window (non-modal, real-time updates)
- Fixed preview stretching when selection includes image outer area
- Fixed integer overflow crash during fast image dragging
- Build optimization, reduced exe size

### 1.0.0

- Official release
- Update check and announcement system
- Image editor optimization
- Security fixes

---

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
- **クイック検索モード** — 前回使用したパッケージパスを優先的に試行
- **マルチサーバー対応** — 中国サーバー、台湾、香港/澳門、日本、国際サーバーに対応
- **手動ウィンドウキャプチャ** — 自動検出に失敗した場合、ゲームウィンドウを手動で選択
- **アップデート確認＆お知らせ** — 起動時に自動アップデート確認、お知らせバー表示

---

## 詳細チュートリアル

### 準備

1. [Releases](https://github.com/OatmeaILL/StarResonance-ProfileCustomizer/releases) から最新バージョンの実行ファイル（.exe）をダウンロード
2. ダブルクリックで `麦麦子名片头像修改工具 1.0.6.exe` を実行
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

## 画像エディターリファレンス

| 機能 | 操作方法 |
|------|---------|
| 切り抜き範囲の調整 | 青色選択枠の四隅や辺をドラッグ |
| 画像の移動 | 選択枠の外側をドラッグ |
| ズーム | スライダーまたはマウスホイール（1%~300%） |
| 明るさ調整 | スライダー、`[-]`/`[+]` 微調整（ステップ1）、`[R]` リセット |
| コントラスト調整 | 同上 |
| 彩度調整 | 同上 |
| 色温度調整 | 同上 |
| 位置リセット | 位置とズームを初期状態に戻す |
| 画像リセット | 全調整パラメータをデフォルトに戻す |
| 拡大プレビュー | プレビューエリアをクリックして拡大ウィンドウ表示 |

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

### 1.0.6

**クライアント**
- 新機能「オプショナルアップデート」：サーバー側で公開時に「このバージョンのスキップを許可」を設定可能。クライアントは初回通知時に「今回の更新をスキップ」をクリックすると、以降同じバージョンの通知を停止
- 新機能「ウィンドウ位置とサイズの記憶」：起動時に前回のウィンドウ位置とサイズを復元（切断されたディスプレイへの復元を防ぐため画面可用性を自動チェック）
- 新機能「終了確認スイッチ」：設定ウィンドウで終了時の確認ダイアログ表示を切り替え可能、即時反映
- 新機能：スライダー ドラッグ中の数値バルーンチップ
- 新機能：リンクホバー時の指カーソルと URL ツールチップ
- 新機能：リソース番号検出。名刺/アバターのリソース番号が 12 を超える場合、割り当て後にゲーム内で下にスクロールするようヒントを表示
- お知らせバーをピクセルレベルのスムーズスクロールに再構築。全文表示後に一時停止し、その後線形スクロール。マウスホバーで一時停止
- 互換性修正：`QFontMetrics.horizontalAdvance` が古い PyQt5 で `width` にフォールバック
- 互換性修正：`primaryScreen()` にヘッドレス/ディスプレイ切断シナリオ用の null ポインタ保護を追加
- バグ修正：終了確認スイッチが再起動後に反映されない問題（原因：QScreen のインポートエラーにより設定読み込みが中断）

**サーバー**
- 公開/編集ダイアログに「このバージョンのスキップを許可」チェックボックスを追加
- バージョンチェック API レスポンスに `optional` フィールドを追加
- サーバーバージョンを 1.0.5 に更新

### 1.0.5

**クライアント**
- 多言語対応（中文 / English / 日本語）を追加
- 初回起動時に言語選択ダイアログを表示、実行中の言語切り替えに対応
- 「設定」ウィンドウを追加、言語とデバッグモードの切り替えが可能
- トップバーの「について」ボタンを設定ウィンドウ内に移動
- サーバーが言語別でユーザーデータを追跡
- 英語版と日本語版のプログラムタイトルの表示問題を修正
- 海外ユーザー向けに FAQ・チュートリアルの WeGame 参照を Steam/ゲームランチャーに変更
- チュートリアルと README テキストの三語統一

### 1.0.4

**クライアント**
- プロフィールカード下部の異常ピクセル領域を修正
- 非同期適用で UI フリーズを解消
- エラー時の自動復元機能を追加
- プリサーチ機構：クイック検索で前回のパッケージパスを優先
- 全調整パラメータに `[R]` リセットボタンを追加
- 初回起動時のチュートリアル表示問題を修正
- クラッシュリスクを低減
- ウィンドウリサイズ成功判定を修正
- クライアントサイズ最適化（約10MB削減）
- クライアントリファクタリング

### 1.0.3

- 特定画像インポート時のクラッシュを修正
- 互換性クラッシュ問題を修正
- デバッグログシステムを追加
- 画像読み込みを最適化

### 1.0.2

- 「ゲームウィンドウを手動キャプチャ」機能を追加
- ゲームプロセス自動検出を拡張
- ウィンドウタイトルの多言語対応
- チュートリアル更新

### 1.0.1

- 画像エディター操作最適化
- 画像移動機能を追加
- 「位置リセット」「画像リセット」ボタンを追加
- 彩度・色温度調整を追加
- +/- 微調整ボタンを追加（ステップ1）
- 拡大プレビューウィンドウを追加
- プレビュー伸縮問題を修正
- 整数オーバーフロークラッシュを修正
- ビルド最適化

### 1.0.0

- 正式リリース
- アップデート確認・お知らせシステム
- 画像エディター最適化
- セキュリティ修正

---

## 免責事項

このツールは**学習・交流目的のみ**です。**完全無料**で、転売は固く禁止します。  
ローカルゲームファイルを変更する原理により、ゲームの破損、データ異常、**アカウント停止のリスク**があります。  
**自己責任**でご使用ください。作者は一切の責任を負いません。

---

## 作者

- OatmeaILL & GLM5.2
- GitHub: [OatmeaILL](https://github.com/OatmeaILL)
- レベル 8 アクティブギルド【瑝珑】、ID: 40384