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
- **push 断连解法（2026-08-10 验证）**：大数据 push 偶发 `Connection reset by ... port 22`，普通重试不一定成功。用 `GIT_SSH_COMMAND="ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=15 -o ServerAliveCountMax=10 -i /c/Users/Administrator/.ssh/id_ed25519" git push origin main` 通常一次成功。
- **镜像 fetch 后 ref 异常**：github-pages 镜像 `git fetch` 成功后 origin/main 有时未更新（ref 仍指旧 commit）。直接 `git reset --hard <commit-hash>` 指定 commit 而非 origin/main 可稳定对齐。

## AI 模型：已从 DeepSeek 切换智谱 GLM-4V-Flash（2026-08-10）
- 云端 github-bedtime-stories 的故事生成已切换为智谱：`generate-story.js` / `refresh-seeds.js` 均用 `ZHIPU_API_KEY` + `open.bigmodel.cn` + `/api/paas/v4/chat/completions` + `glm-4v-flash`；workflow env 为 `ZHIPU_API_KEY: ${{ secrets.ZHIPU_API_KEY }}`；README / setup-github.sh 同步更新。
- GitHub 旧 secret `DEEPSEEK_API_KEY` 仍存在（未删）；**新 secret `ZHIPU_API_KEY` 已于 2026-08-10 由用户手动在 GitHub 网页添加成功**（`gh secret list` 可见，2026-08-10T08:28:21Z）。云端 Actions 现已可用智谱 GLM-4V-Flash 生成故事。
- 智谱 API key 来自 `D:\code test\睡前故事\zp.txt`，已同时加入本地 `~/.workbuddy/models.json`（glm-5.2，智谱）。
- 本地 D 盘 `scripts/gen-today.js`（一次性测试脚本）也已改 glm-4v-flash + ZHIPU_API_KEY。
- ⚠️ **GLM-4V-Flash 的 max_tokens 上限 1024**（2026-08-12 踩坑）：原 4096/2048 会被 API 拒绝（400 `max_tokens参数非法：限制数值范围[1,1024]`），导致云端 Actions"看似成功实则零产出"（无新故事→No changes to commit）。三个脚本（generate-story.js / refresh-seeds.js / gen-today.js）均已改为 1024。排查"云端没更新"：先 `gh run view --log` 看 API 错误，再对比本地 stories.json 缺失日期。

## 代码审核结论（2026-07-30）
- 真实需修项：C3（clean_stories 正则漏 science）、C1（sync_stories 路径锚定+一致性告警）、M2（re2 别名）、H1（根 scripts 硬编码路径，用 resolvePath 回退）、M1（下拉刷新 preventDefault）。
- 误报/非缺陷：C2（EMBEDDED_STORIES 实际合法）、H3（已有 -1 抛错）、M3（单弯引号已处理）、H2/H4/M4/M5（非缺陷或增强项）。
- github-pages 关键生成脚本（generate-story.js / generate-collection-html.js / prompt-builder.js）**已全程用 `__dirname` 相对路径**，无需改。

## 时间线 / 宝宝出生硬约束（2026-09-20 重大更新：宝宝实际出生日 = 2026-09-15）
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

## 胎教期生成增强 ·「故事孕育师」材料库（2026-08-05 落地）
- 权威实现：`C:/Users/Administrator/WorkBuddy/Claw/github-bedtime-stories/scripts/prompt-builder.js` 中的 `PRENATAL_CAST` / `PRENATAL_SCENES` / `PRENATAL_IMAGERY` / `EMOTIONAL_ANCHORS` / `PRENATAL_SAFETY` + `pickProtagonist()` + `buildPrenatalBlock()`；仅在 `ageInfo.group==='prenatal'`（2026-09-22 前）注入到 4 个 prompt builder。
- 可读版：`D:/code test/睡前故事/scripts/prenatal-material-library.md`；规范镜像 `STORY_STYLE_GUIDE.md` 新增「六、胎教期增强」。
- 回归自测：`D:/code test/睡前故事/scripts/test_prenatal_render.js`（胎教期注入 / post-birth 不注入）。重放插入：`scripts/apply_prenatal_insert.py`（读 `tmp_prenatal_block.js`）。
- 硬约束已编入 `PRENATAL_SAFETY`：无蟹、未出生宝宝、无弯引号、无危险/否定式安慰。

## 月度种子批次解锁 SEED_BATCHES（2026-08-05 已部署到云端）
- 现已不是孤儿 feature：`SEED_BATCHES`(12 月×32 种子按月解锁)+`getUnlockedSeeds` 已并入云仓 `github-bedtime-stories/scripts/prompt-builder.js`（云端 main `c043af2`），`pickSeeds` fallback 调用它；`refresh-seeds.js` 已复制到云仓与镜像 `scripts/`；`generate-story.js` 加入了每月 1 号运行 `refresh-seeds.js --batch-only` 的刷新块。
- 同时修正了云仓旧逻辑：原本「整日 dayHasAny 跳过」会误伤科学故事与另一语言，已改为按语言/分类精细判断（hasCn/hasEn/hasSciCn/hasSciEn），与「同天可多篇 + 手动/自动互不覆盖」一致。
- D 盘 `scripts/` 副本与云仓、镜像已三处对齐（均以 D 副本为改全源，再整体 cp）。
- 同步工具：`scripts/apply_v2_edits.py`（情境轮换+科学来源+胎教结尾放宽+source 回退标注），`apply_prenatal_insert.py`（胎教块插入）；辅助：`tmp_prenatal_block.js`、`test_prenatal_render.js`。

## 生成器增强清单（2026-08-05 全部落地于云端 main）
- 胎教期「故事孕育师」材料库（PRENATAL_CAST/SCENES/IMAGERY/ANCHORS/SAFETY）+ 仅 prenatal 注入：见前节。
- **每日情境轮换**：`OCCASIONS_CN/EN`+`pickOccasion()`，每日故事不再局限于「晚安」，按早安/白天/晚安/奇妙发现/暖心陪伴变化结尾；胎教结尾也放宽。
- **科学故事指定来源 + 儿童可理解科普**：素材必须取自 `SCIENCE_FEEDS`（环球科学/博物/Scientific American），不得编造；要求含清楚准确的儿童科普讲解；`moral` 为科学事实小结；fallback 标注「儿童科普常识」，`generate-story.js` 保证 `story.source` 始终有值。规范镜像 `STORY_STYLE_GUIDE.md` 新增「七、每日情境轮换与科学故事来源」。

## 科学系列「单独划分」已落地（2026-08-09 确认）
- 数据层：科学故事带 `category:'science'` + `series:'science'` + `source`（来源锁定 SCIENCE_FEEDS）。`series:'science'` 是 UI 筛选的唯一依据（不是 category）。
- UI 层：H5 阅读器 `index.html` 已有「🔬 科学」专属 tab（`data-series="science"`，筛选 `s.series==='science'`）；合集页 `generate-collection-html.js` 把科学故事独立成章（封面+目录+卡片+来源徽标）。黑猫当当用 `series:'dangdang'` 独立成章；日常故事 `series` 为空。三者互不混入。
- **手动补科学故事的安全做法**：交互会话无 `DEEPSEEK_API_KEY`，无法跑 `generate-story.js` 实时生成；可直接按科学 prompt 规范撰写并入库。模板见 `D:/code test/睡前故事/scripts/add_science_stories.py`（写入 4 副本 stories.json + 重写各 index.html 的 `EMBEDDED_STORIES` 单行），新故事 id 必须形如 `{YYYY-MM-DD}-science-{cn|en}` 以免被自动化按 `hasSciCn/hasSciEn` 重复生成。
- 四副本（云仓 `github-bedtime-stories` / `bedtime-story-app` / `D:/code test/睡前故事` / `github-pages` 镜像）的 stories.json+index.html+collection.html 须保持一致；云仓 push 后，镜像 `git reset --hard origin/main` 对齐，另两处直接 cp。

## 手动/本地补故事的 id 约定（2026-08-10 踩坑后确立）
- 自动化任务每 2 小时运行，会为当天生成 `YYYY-MM-DD-cn` 与 `YYYY-MM-DD-en`（每日故事）+ 科学故事，并 push 到 origin/main。
- **本地手动补故事时，不要用当日 base id（cn/en）**，否则会与自动化产出撞 id：`git push` 会被远端「fetch first」拒绝，且即便强制也会覆盖或产生重复 id。
- 正确做法：手动/本地批量故事统一用**同日多篇扩展 id**：`YYYY-MM-DD-cn-2` / `-en-2` / `-cn-3` …（compute_unique_id 也会在 base 被占用时自动加 -2/-3，但直接指定更省事）。
- push 前务必先 `git fetch origin` 看远端是否领先；若领先（自动化已 push 新故事），先 `git reset --hard origin/main` 对齐，再把本地 4 副本统一为该基线后再叠加本地故事，最后 commit+push，避免覆盖自动化产出。
- 注入脚本模式（已验证）：`add_science_stories.py` / `add_local_ai_stories.py` 都是「读 4 副本 stories.json → 追加（按 id 去重）→ json.dump → 重写 index.html 的 EMBEDDED_STORIES 单行」；合集页用 `node scripts/generate-collection-html.js` 重生成后复制到其余 3 副本。

## 出生日变更（2026-09-20 确立，覆盖此前预产期设定）
- **宝宝实际出生日：2026-09-15**（原预产期 2026-09-22 作废）。`CHILD_BIRTHDAY`（prompt-builder.js / apply_series_episode.py / generate-dangdang.js，四副本共 10 处）已全部改为 2026-09-15。
- **切分规则**：2026-09-14 及之前 = 胎教期；**2026-09-15 及之后 = 0-1 岁**（出生后口吻：极简短句、大量重复与拟声、感官启蒙/安全感/日常认知）。
- **9/15–9/21 已发布的 28 篇已改写**为出生后口吻（素材 `scripts/rewrite_out_*.json`），dangdang-ep27 本就无胎教措辞故仅改标签。**再遇到「出生日变更」类需求，直接复用 `scripts/apply_birth_batch.py` 的「按 id 替换 + 追加」模式。**
- **9/22–9/30 每日 4 篇（中/英日常 + 中/英科学）已补齐**（素材 `scripts/generate_out_*.json`），当当 ep28/ep29 跟进「宝宝出生」单元。当前 257 篇，0-1 岁共 67 篇。
- **星期计算坑（已修）**：`datetime.weekday()` 是 Monday=0，配 `['星期日','星期一',...]` 会整体偏移 1 天（9/11–9/30 共 36 条已修正）。批量脚本务必用 `['星期一',...,'星期日']` 配 `weekday()`。
- **AI 生成方式偏好**：外部 API（智谱 glm-4-flash）试跑质量不稳（整段复读、科学故事残句），用户明确「用 WorkBuddy 自带的 DeepSeek Flash」——即由对话模型本体直接创作。备用管线脚本 `scripts/ai-0-1-pipeline.js` 保留（复用云端 prompt-builder 构建 prompt，支持 generate / rewrite）。
- **推送记录**：部署源 main = `945dff0`（github-bedtime-stories push，github-pages 随后 reset 对齐）；备份 master = `f0195ab`。
