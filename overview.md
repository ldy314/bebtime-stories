# 睡前故事项目 — 代码审核复核与修复概述

> 执行者：Senior Developer（高级开发工程师）｜日期：2026-07-30

## 一、备份（先于任何修改）
两个仓库均先本地提交，再推送 GitHub 备份分支（沙箱→GitHub 网络不稳，用「按哈希推送」成功）：
- `github-pages` → 本地 `3fcc387`，已推送 `backup/pre-fix-20260730`
- 根目录 `D:\code test\睡前故事` → 本地 `3345746`，已推送 `backup/pre-fix-20260730-root`
- **已核实这两个备份提交不含任何修复**（真正修复前状态），可作安全回退点。
- 回退命令：`git -C <repo> checkout 3345746`（或 `backup/pre-fix-20260730-root`）。

## 二、每问题复核结论（修复前先确认是否真实）
| 问题 | 复核 | 处置 |
|------|------|------|
| C2 index.html 截断 | **误报**（内嵌 JSON 合法，29 篇） | 跳过 |
| H3 updateEmbeddedStories | **误报**（已有 `-1` 抛错防护） | 跳过 |
| M3 单弯引号 | **误报**（sanitizeText 已处理 `\u2018/2019`） | 跳过 |
| C3 clean_stories 正则 | **真实** | 已修 |
| C1 stories.json 同步 | 当前一致，但无防护/路径未锚定 | 已加固 |
| M2 re2 别名 | **真实** | 已修 |
| H1 硬编码路径 | **部分真实**（github-pages 已相对；根脚本多为有意跨目录引用） | 安全子集已修 |
| M1 下拉刷新 | **真实**（缺 preventDefault） | 已修 |
| H2/H4/M4/M5 | 非缺陷/增强项 | 未改（严格保持功能不变） |

## 三、已实施的修复
- **C3** `scripts/clean_stories.py`：正则加 `(science-)?`，科学故事不再被误删。
- **C1** `scripts/sync_stories.py`：路径锚定到 `__file__`（不再依赖 cwd）；新增同步前一致性告警（非致命）。
- **M2** `scripts/generate_stories.py`：移除多余 `import re as re2`，改用 `re`。
- **H1（安全子集）** 根 `scripts/*.js`（generate-collection-html / generate-collection-md / push-to-cloud / sync-from-cloud / verify-style-sync）：加 `resolvePath(preferred, fallback)`，优先相对路径、回退原绝对路径——功能不变，可移植性提升。
- **M1** `index.html`：下拉刷新加 `{passive:false}` + `e.cancelable` 防护 + `scrollY<=0`，触发逻辑/阈值不变。

## 四、回归验证（全部通过，功能不变）
- 5 个 JS 文件 `node --check` 通过；3 个 Python 文件 `py_compile` 通过。
- C3 正则单测：science-cn/en 与常规 cn/en 均匹配，非法 ID 拒绝。
- 实跑 `generate-collection-html.js`（29 篇）、`generate-collection-md.js`（29 篇）、`verify-style-sync.js`（STYLE_SYNC_OK）、`sync_stories.py`（root↔github-pages 同步成功）均无错误。
- 数据校验：stories.json=29、科学故事 2 篇保留、EMBEDDED_STORIES=29、github-pages 与 root ID 完全一致。

## 五、提交状态
- 修复已本地提交（`cbc886f` 等），工作树干净。
- 修复版本**未推送** GitHub（你仅要求备份"之前版本"，且沙箱网络不稳）；备份分支已推送。修复版本可后续网络允许时推送。
