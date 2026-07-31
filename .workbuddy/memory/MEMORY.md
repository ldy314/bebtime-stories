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
