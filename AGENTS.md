# AGENTS.md — 睡前故事

> 为宝宝每天自动生成中英文睡前故事各一篇（含科学系列、黑猫当当连载），风格随年龄阶段自动切换；
> 产出经 CloudStudio H5 阅读器 + GitHub Pages 双通道发布。
> **历史日志**：`.workbuddy/memory/YYYY-MM-DD.md` —— **本目录是项目标准配置，必须存在**（一天一文件，只追加）。**格式规范**见工作区根 `AGENTS.md`「日志规范」。**三种 AI 都能读写** —— WorkBuddy 自动识别；opencode／Reasonix 需按本行**主动读**。**默认读本目录 `MEMORY.md`（现状快照）；追溯过程时才读日志，且只读最近 1–3 份（禁全量）**。
> **交接文档（handoff）**：接手会话／换 AI／换 harness 时，先读 **`.handoff/LATEST.txt` 第 1 行**（最新交接件的相对路径；**该文件不存在＝尚无交接件**）—— 本目录有读本目录，无则读工作区根。产出由 skill `handoff` 写入 `.handoff/`（**双写** OS temp ＋ 项目根）；该目录属**运行产物**，清旧件**不算**「整理」。规范见工作区根 `AGENTS.md`「交接文档（handoff）」。

**本文件是索引**（≤60 行）。**完整原档**见 `docs/archive/AGENTS-full-20260926.md`；状态快照见 `MEMORY.md`（已并入原 `.workbuddy/memory/MEMORY.md` 的有效内容）。

## 项目事实

| 项 | 值 |
|---|---|
| 数据 | `stories.json` 613KB / **257 篇**（146 中 + 111 英），覆盖 2026-07-16 ~ 09-30 |
| 分类 | 胎教期 190 篇 · 0-1 岁 67 篇 · 科学 70 篇 · 黑猫当当 29 集 |
| 关键日期 | 宝宝**实际出生日 2026-09-15**（原预产期 09-22 已作废）→ 之前 = 胎教期，之后 = 0-1 岁 |
| 生成模型 | **DeepSeek**（`deepseek-chat`，`max_tokens: 4096`，**单次调用、不再分段续写**） |
| 仓库 | `ldy314/bebtime-stories` —— 根目录在 `master`、`github-pages/` 在 `main`，同源远端 |

## 三套入口（谁是谁，别搞混）

| 入口 | 角色 |
|---|---|
| 根目录 | 本地**完整镜像／备份**（有独立 `.git`） |
| `github-pages/` | ⭐ **当前权威部署源**（push 目标；GitHub Pages 构建源） |
| `github-pages2/` | **旧版快照**（全部文件 mtime 冻结于 2026-08-05；`prompt-builder.js` 仅为权威版的 46%）—— **勿作参考** |

## 生成与发布链

```
prompt-builder.js  →  generate-story.js  →  stories.json  →  embed_stories.py
  (风格唯一权威源)     (DeepSeek 调用)       (唯一数据库)    (重写 index.html 的 EMBEDDED_STORIES)
      →  generate-collection-html.js  →  collection.html  →  push-to-cloud.js  →  云端 + GitHub Pages
```

**Cloud workflows**（`.github/workflows/`）：`generate-stories.yml` 每日 `0 18 * * *`（= 02:00 北京时间）；
`refresh-seeds.yml` 每月 1 号（种子批次刷新）；`generate-dangdang.yml` 每周六（当当连载）。

## 不可违反的约束

1. **`stories.json` 禁用中文弯引号**（`“”`），必须用 `「」` 或单引号 —— 否则 JSON 解析失败。
2. **不得出现「大闸蟹／螃蟹」**相关内容（用户明确禁忌）—— 角色、食物、情节、地标卖点一律避免。
3. **阶段由创作日决定**：出生日之前的创作**绝不把宝宝写成已出生**。改 `CHILD_BIRTHDAY` 须四副本同步。
4. **`prompt-builder.js` 是风格唯一权威**；`STORY_STYLE_GUIDE.md` 是其镜像，**二者必须完全一致**（用 `verify-style-sync.js` 校验）。
5. **手动补故事禁用当日 base id**（`YYYY-MM-DD-cn`）—— 会与自动化撞 id 导致 push 被拒；须用 `YYYY-MM-DD-cn-2` 扩展 id。
6. **四副本同步**：云仓 / `github-bedtime-stories` / 本目录根 / `github-pages` 的 `stories.json` + `index.html` + `collection.html` 必须保持一致。
7. **API Key 仅走环境变量与 GitHub Secrets**，绝不硬编码或用文件存储。
8. **发布前必须把 root 的 `series-dangdang-guide.md`／`dangdang-destinations.md` 同步进 `github-pages/`** —— 那才是实际部署源。

## 已知坑

- 脚本硬编码 `C:/Users/Administrator/WorkBuddy/...` 绝对路径（`push-to-cloud.js`、`sync-from-cloud.js`、`verify-style-sync.js`），D 盘环境运行可能失败。
- 根 `index.html`／`collection.html` 与 `github-pages/` 版本**字节不同、未同步** —— push 前须核对。
- 根与 `github-pages` 提交历史分叉却同源远端 → 易相互覆盖；push 前先 `git fetch` 看远端是否领先（远程可能有自动生成的当日提交）。
- 推送偶发 `Connection reset by ... port 22` → 用 `GIT_SSH_COMMAND` 带 `ServerAliveInterval=15 -o StrictHostKeyChecking=no -i ~/.ssh/id_ed25519` 重试（仍走 `ssh.github.com:443`）。
- `README.md` 与 `拼音功能开发记录.md` **内容已过时**（写智谱 GLM、23:00 生成、unpkg CDN），勿据此判断现状。

## 部署

- **CloudStudio**：H5 阅读器 + 合集页各一个链接，每次生成后自动重新部署（链接见 `MEMORY.md`）。
- **GitHub Pages**：`https://ldy314.github.io/bebtime-stories/`，构建源 = `main` 分支根目录。
