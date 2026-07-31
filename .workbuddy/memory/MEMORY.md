# MEMORY.md — 睡前故事项目长期记忆

## Git / GitHub 推送要点（2026-07-30 确认）
- 仓库：`ldy314/bebtime-stories`。根目录 `D:\code test\睡前故事` 在 `master`；子目录 `github-pages/` 是独立仓库在 `main`（两者指向同一远端）。
- **推送必须用本地 `core.sshCommand`**：默认 git SSH 不会选用 `~/.ssh/id_ed25519`（ssh-agent 未运行），导致 `Could not read from remote repository`。已为两个仓库设置：
  `git config core.sshCommand "ssh -o StrictHostKeyChecking=no -i /c/Users/Administrator/.ssh/id_ed25519"`
- 当前沙箱到 GitHub 网络不稳：SSH 鉴权成功，但 `fetch`/`push` 大数据时偶发 `Connection reset by ... port 22`。小增量推送（如单提交）通常可成功；若失败重试即可。
- 备份分支命名约定：`backup/pre-fix-YYYYMMDD`（github-pages）与 `backup/pre-fix-YYYYMMDD-root`（根目录），避免与主分支冲突。
- 推送备用手段（绕过本地分支问题）：`git push origin <sha>:<refs/heads/backup/xxx>`。
- **发布前必须把 root 的 `series-dangdang-guide.md` / `dangdang-destinations.md` 同步进 `github-pages/`**（github-pages 才是实际部署源）。2026-07-31 踩坑：在 root/autodir/07 镜像改了 Ruddy/雪纳瑞/常州新景点，但忘了同步 github-pages/，导致 github-pages 工作树仍是旧版（含恐龙园/大麻糕、无 Ruddy）；push 前已用 root 权威版覆盖修正。
- **远程 main 可能比本地 github-pages 领先 1 个自动生成提交**（如 `eaa79cf1` Auto-generate bedtime stories 2026-07-31，含当日每日故事）。push 前应先 `git fetch origin '+refs/heads/main:refs/remotes/origin/main'`（注意 refspec 有时不自动建 origin/main），把本地 stories.json 构造成「远程 base + 本地 ep02-9」的并集再提交，避免覆盖掉线上的当日故事。

## 代码审核结论（2026-07-30）
- 真实需修项：C3（clean_stories 正则漏 science）、C1（sync_stories 路径锚定+一致性告警）、M2（re2 别名）、H1（根 scripts 硬编码路径，用 resolvePath 回退）、M1（下拉刷新 preventDefault）。
- 误报/非缺陷：C2（EMBEDDED_STORIES 实际合法）、H3（已有 -1 抛错）、M3（单弯引号已处理）、H2/H4/M4/M5（非缺陷或增强项）。
- github-pages 关键生成脚本（generate-story.js / generate-collection-html.js / prompt-builder.js）**已全程用 `__dirname` 相对路径**，无需改。

## 时间线 / 宝宝出生硬约束（2026-07-31 用户明确，已按真实创作日重排）
- **阶段由真实创作日决定**（用户原话：「故事要和目前宝宝所处的阶段一致；今天创作的所有故事都属于胎教期；9月22号之前创作的所有故事，无论多少，都属于胎教期」）。
- 宝宝预产期 **2026-09-22**；凡在 2026-09-22 **之前创作**的故事一律 **胎教期**（讲给肚里还没来的宝宝听），**绝不在出生前把宝宝写成已出生**。
- **当前全集状态**：ep01–ep19 均于 **2026-07-31** 一次性创作（早于预产期），故**全集 19 集全部胎教期**、日期统一标 2026-07-31；ep09=《茅山遇修猴子》（修猴子登场，胎教期），ep10=当当讲给肚里宝宝听的茅山复述，ep10–19 已去除「已出生宝宝」措辞。
- **出生情节留待 2026-09-22 之后**创作的集数（ep20+）；届时 `apply_series_episode.py` 的 `get_age_info` 按真实生成日期 cutoff（`CHILD_BIRTHDAY=2026-09-22`）自动判定 ageGroup 为 0-1 岁，无需手动指定。
- `dateOverride` 缺省时取「latest Saturday on/before today」；批量生成务必显式给 `dateOverride`，否则会塌到同一天。
- 重排工具（可复用）：`automation-2026-07-16-11-56-46/patch_realtime.py`、`fix_prenatal.py`、`fix_state.py`、`patch_docs.py`。

## 内容禁忌（用户明确，2026-07-31）
- **不得出现「大闸蟹 / 螃蟹」相关内容**（用户原话：「不要大闸蟹内容」）。当当系列及所有睡前故事创作时，避免以螃蟹/大闸蟹为角色、食物或情节元素；长荡湖等相关地标也不以螃蟹为卖点。
- 2026-07-31 已清理临时灵感文档 `临时/deepseek_markdown_20260731_2987a5 (1).md` 中的 11 处大闸蟹/螃蟹内容（含《当当和大闸蟹的最后一课》、长荡湖大闸蟹产区、食物故事 #232、道具符号「大闸蟹」等），替换为桂花/银鱼/芝麻糖等无蟹替代；另一副本 `69fd35` 本就是「已移除螃蟹」的 V3.0 版。
- 正式发布的 19 篇故事、大纲、指南、合集、索引均不含大闸蟹（已 grep 验证）。
