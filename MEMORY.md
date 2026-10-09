# MEMORY.md — 睡前故事（状态快照）

> **覆盖式**更新，只写「现在是什么样」与「下一步」；追加式日志在 `.workbuddy/memory/YYYY-MM-DD.md`。
> 上限 150 行。原 `AGENTS.md`（139 行）与 `.workbuddy/memory/MEMORY.md`（13.7KB）**原文已归档**至 `docs/archive/`，有效内容已并入本文件。
> 最后更新：2026-09-26

## 一句话现状

**活跃**。云仓 GitHub Actions 每日 02:00（BJT）自动生成 + 每周六当当连载 + 每月 1 号刷新种子；
本地根目录作为完整镜像备份，`github-pages/` 为实际部署源。257 篇已覆盖至 **2026-09-30**（含提前排期）。

## 数据现状（实测 2026-09-26）

| 项 | 值 |
|---|---|
| `stories.json` | 613,406 B / **257 条** |
| 语言 | 中文 146 · 英文 111 |
| 日期范围 | 2026-07-16 ~ 2026-09-30（最新 `dangdang-ep29-zh`《当当的轻手轻脚》） |
| 年龄段 | `prenatal` **190** · `0-1` **67** |
| 分类 | `category:science` = `series:science` = **70** 篇 · `series:dangdang` = **29** 集 · 其余 `regular` 124 |
| 字段 | `id,date,dateShort,title,language,ageGroup,ageLabel,preview,moral,content` 全覆盖；`category` 194 · `series` 99 · `source` 70 · `episode` 29 |

**阶段划分（现行）**：2026-09-14 及之前 = 胎教期；**2026-09-15（出生日）及之后 = 0-1 岁**。

## 三副本 / 三入口同步现状

| 位置 | 状态 |
|---|---|
| 根目录 | 本地完整镜像。`index.html` 600,585 B（9/20 18:18）、`collection.html` 712,544 B |
| `github-pages/` | ⭐ 权威部署源。`index.html` 597,919 B（18:07）、`collection.html` 723,226 B |
| `github-pages2/` | 旧版，mtime 全冻结于 2026-08-05 —— **勿参考** |

⚠️ **根与 `github-pages/` 的 `index.html`／`collection.html` 字节不同，当前未同步**；两边提交历史分叉但同源远端。
⚠️ 根 `.git` 有 1 处未提交：`M index.html`。

## 生成器能力清单（已全部落地于云端 main）

- **胎教期「故事孕育师」材料库**：`PRENATAL_CAST`／`PRENATAL_SCENES`／`PRENATAL_IMAGERY`／`EMOTIONAL_ANCHORS`／`PRENATAL_SAFETY` + `pickProtagonist()` + `buildPrenatalBlock()`，仅在 `ageGroup==='prenatal'` 时注入。可读版 `scripts/prenatal-material-library.md`。
- **月度种子批次解锁**：`SEED_BATCHES`（12 月 ×32 种子）+ `getUnlockedSeeds()`（按当前月份解锁）+ `pickSeeds` fallback；每月 1 号由 `refresh-seeds.js --batch-only` 刷新。日志 `scripts/seed-refresh-log.json`。
- **每日情境轮换**：`OCCASIONS_CN/EN` + `pickOccasion()` —— 结尾不再局限于「晚安」（早安／白天／晚安／奇妙发现／暖心陪伴）。
- **科学故事指定来源**：素材取自 `SCIENCE_FEEDS`（环球科学／博物／Scientific American），不得编造；`moral` 为科学事实小结；fallback 标「儿童科普常识」。
- **主题池 6 类**按日期确定性轮换，同日中英文选不同题材；中文风格库 6 核心 + 6 扩展、英文 5 核心 + 6 扩展（完整定义在 `prompt-builder.js` / `STORY_STYLE_GUIDE.md`）。
- **系列划分**：科学故事 `series:'science'`（H5 有「🔬 科学」专属 tab，合集独立成章）；当当 `series:'dangdang'`；日常故事 `series` 为空。三者互不混入。

## 拼音注音现状

- 库：`pinyin-pro@3.26.0`，CDN = **jsdelivr**（`index.html:503`、`collection.html:7`）。注：`拼音功能开发记录.md` 写的 unpkg 已过时。
- 渲染：`index.html` 逐字生成 `<ruby>…<rt>…</rt></ruby>`；`collection.html` 同构。
- Toggle：`index.html` 的 `#pinyinToggle`；合集页 `onclick="togglePinyin()"`。
- **默认开启范围**：仅 `ageGroup ∈ {prenatal, 0-1, 1-3}` 自动开启；`3-6`／`6+` 默认关；英文不显示。合集页对中文卡片统一默认开。

## 内容禁忌与硬约束

- **禁用「大闸蟹／螃蟹」**（用户明确）：角色、食物、情节、地标卖点一律避免；长荡湖等不以螃蟹为卖点。2026-07-31 已清理 11 处。
- **胎教期硬约束**（编入 `PRENATAL_SAFETY`）：未出生宝宝口吻、无蟹、无弯引号、无危险或否定式安慰。
- **`stories.json` 禁中文弯引号**，用 `「」`。
- **id 约定**：自动化产出 `YYYY-MM-DD-cn`／`-en`；科学故事 `YYYY-MM-DD-science-{cn|en}`（避免被 `hasSciCn/hasSciEn` 重复生成）；手动补故事用 `-cn-2`／`-cn-3` 扩展 id。
- **星期计算坑（已修）**：`datetime.weekday()` 是 Monday=0，必须配 `['星期一',…,'星期日']`，否则整体偏移 1 天（曾致 36 条错误）。
- **`dateOverride` 缺省值** = 「latest Saturday on/before today」；批量生成务必显式给 `dateOverride`，否则塌到同一天。

## Git 推送要点

- 仓库 `ldy314/bebtime-stories`；两个仓库均须配置本地 `core.sshCommand` 指定 `~/.ssh/id_ed25519`（ssh-agent 未运行，默认不会选用该 key）。
- 数据量大时偶发 `Connection reset by ... port 22`：用 `GIT_SSH_COMMAND="ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=15 -o ServerAliveCountMax=10 -i ~/.ssh/id_ed25519"` 通常一次成功。走 `ssh.github.com:443`。
- **push 前先 `git fetch origin`**：远程 main 可能领先 1 个自动生成提交，须构造「远程 base + 本地新增」的并集再提交，避免覆盖线上故事。
- 镜像 `fetch` 后 `origin/main` 有时不更新 → 直接 `git reset --hard <commit-hash>` 更稳。
- 备份分支命名：`backup/pre-fix-YYYYMMDD`（github-pages）／`...-root`（根目录）。

## 部署

- **CloudStudio**：H5 阅读器 `https://1fed25c2ce604e02bace926e7125e05e.app.codebuddy.work` · 合集页 `https://17dbb03eb76d40a4afcb1d6900a680aa.app.codebuddy.work`（每次生成后自动重新部署）
- **GitHub Pages**：`https://ldy314.github.io/bebtime-stories/`（构建源 = `main` 根目录）

## 待办

1. 删除旧 `master` 分支（Pages 已翻到 `main`）。
2. 根与 `github-pages/` 的 `index.html`／`collection.html` **对齐同步**（当前字节不同）。
3. 将读者端「故事风格介绍」板块重新部署到云端（本地已更新）。
4. `README.md`、`拼音功能开发记录.md` 内容过时，需按现状修订（或在顶部标注过时）。

## 已失效／勿再引用

- **「已切换智谱 GLM-4V-Flash」** → **已迁回 DeepSeek**（`deepseek-chat` / `max_tokens:4096` / 单次调用）。GLM 的 `max_tokens ≤1024` 坑随之失效。
- **预产期 2026-09-22** → 实际出生日 **2026-09-15**；`CHILD_BIRTHDAY` 已全改。
- 旧路径 `C:\Users\Administrator\WorkBuddy\Claw\...`、`automation-2026-07-16-11-56-46\...` → 当前工作副本在 `D:\code test\睡前故事\`。
- README 的「23:00 生成」→ 实际 cron `0 18 * * *` UTC = 02:00 BJT。

## 本次整理（2026-09-26）

- `AGENTS.md` 由 139 行重写为受预算约束索引；**新建**本 `MEMORY.md`（原 `.workbuddy/memory/MEMORY.md` 长期笔记就地升级为项目根快照）。
- 两份原文完整归档至 `docs/archive/`：`AGENTS-full-20260926.md`、`workbuddy-memory-MEMORY-full-20260926.md`。
