# AGENTS.md — 睡前故事项目全貌

> 写给任何接手这个项目的人（包括未来的自己）。读完这篇，你应该知道所有东西在哪、怎么跑、为什么这样设计。

---

## 项目目标

为即将出生的孩子（预产期 **2026年9月22日**）每天自动生成中英文睡前故事各一篇。故事风格随孩子年龄分阶段自动调整。

## 架构总览：三重保障系统

```
优先级 1 ── 本地 WorkBuddy 自动化（主力）
优先级 2 ── 手机一键触发 GitHub Action（备用）
优先级 3 ── GitHub Actions 定时 + GitHub Pages（永久在线）
```

## 系列素材库（黑猫当当）— 集中索引

系列「黑猫当当历险记」的全部角色设定、目的地风物、主题库、美术风格、分集大纲等细节，已分类整理到：

```
D:\code test\睡前故事\storyline\
```

由 `storyline\分类依据.md` 作为**唯一分类索引与权威说明**。写系列故事时，本文件不再重复角色/目的地/主题/风格等细节，直接查阅该索引与对应分类文件夹即可（索引手册第九节专门说明本文件与它的分工）。

> 冲突处理：索引手册若与任何旧模板冲突，以 `storyline\00-权威源文件` 中的现有内容为准（如：安徽定远白猫定名「卡莎」、故事发生地=江苏常州、目的地 22 个含 Ruddy 一家带来的 6 个跨国连线目的地、插图 11 种绘本风）。

## 关键目录与文件

### 1. 核心数据与页面

| 路径 | 说明 |
|------|------|
| `C:\Users\Administrator\WorkBuddy\Claw\bedtime-story-app\stories.json` | **唯一的数据库** — 全部故事 JSON 数组，35 篇（22 中文 + 13 英文，会随自动化动态增长） |
| `C:\Users\Administrator\WorkBuddy\Claw\bedtime-story-app\index.html` | **H5 阅读器** — 内嵌 EMBEDDED_STORIES 变量，不依赖外部 JSON 加载 |
| `C:\Users\Administrator\WorkBuddy\Claw\bedtime-story-collection.md` | **合集 Markdown** — 所有故事的可读文本合集 |
| `C:\Users\Administrator\WorkBuddy\automation-2026-07-16-11-56-46\bedtime-story-collection.html` | **合集 HTML** — 由 `generate-collection-html.js` 从 stories.json 生成 |

### 2. GitHub Pages 项目

| 路径 | 说明 |
|------|------|
| `C:\Users\Administrator\WorkBuddy\Claw\github-bedtime-stories\` | GitHub Pages 项目完整源码 |
| 内含：`index.html`、`collection.html`、`stories.json`、`scripts/`（JS 生成脚本）、`.github/workflows/generate-stories.yml` |
| 仓库地址：`https://github.com/ldy314/bebtime-stories` |
| **状态：已推送至 `main` 分支（commit `5aa00d9`，GitHub Pages 由该分支构建）** |

### 3. 自动化脚本

| 路径 | 说明 |
|------|------|
| `C:\Users\Administrator\WorkBuddy\automation-2026-07-16-11-56-46\generate_stories.py` | **补跑脚本** — 包含 14 篇胎教期故事全文，一次性批量补生成 |
| `C:\Users\Administrator\WorkBuddy\automation-2026-07-16-11-56-46\generate-collection-html.js` | **合集生成器** — 读取 stories.json，渲染完整的合集 HTML |

### 4. 备份目录

| 路径 | 说明 |
|------|------|
| `D:\code test\睡前故事\` | **完整项目镜像** |
| 根目录：`index.html`、`stories.json`、合集 MD、合集 HTML |
| `github-pages\`：GitHub Pages 全部源码 |
| `scripts\`：自动化脚本副本 |
| `插图\`：每篇故事一张暖色绘本风插图（PNG，按标题命名）；**仅本地保存，不进网页** |
| `illustration_jobs.json`：插图任务清单（由 `scripts/generate_illustrations.py` 生成，标记每篇 done 状态） |

### 5. 自动化任务

| ID | 名称 | 频率 | 作用 |
|----|------|------|------|
| `automation-1784174206957` | 睡前故事小程序（含备份同步） | 每 2 小时 | 检查遗漏 → 生成故事 → 更新源文件 → 部署云端 → 无条件同步备份到 `D:\code test\睡前故事\`（18 个文件），默认模型 Hy3 |

> 2026-07-29 合并：原独立任务「睡前故事备份同步」（automation-1785075365533，每 1 小时）已删除，其全部同步步骤并入主任务的"第五部分"，每次运行无条件执行。

## 故事数据格式

### stories.json 每个条目

```json
{
  "id": "YYYY-MM-DD-cn",        // 唯一标识，cn/en 区分语言
  "date": "YYYY年M月D日 · 星期X",
  "dateShort": "MM/DD",
  "title": "故事标题",
  "language": "zh",             // zh / en
  "ageGroup": "prenatal",       // prenatal / 0-1 / 1-3 / 3-6 / 6+
  "ageLabel": "胎教期",
  "preview": "故事前两句话...",
  "moral": "故事寓意",
  "content": ["段落1", "段落2"]  // 字符串数组
}
```

## 年龄阶段与风格

> **风格单一事实来源**：实际生成用的完整定义（题材池 + 中英文大师风格 + 题材轮换规则）在 `STORY_STYLE_GUIDE.md`（本地镜像）与 GitHub 仓库 `scripts/prompt-builder.js`（权威源）中，二者必须保持一致（自动化每次同步后用 `verify-style-sync.js` 校验）。下表为各阶段**风格重点方向**概览，完整风格库见上述文件。

| 阶段 | 时间 | 中文风格重点 | 英文风格重点 |
|------|------|-------------|-------------|
| **胎教期** | ~2026.9.22 | 冰波/金波诗意温柔、拟声词、等待/爱/守护 | Dr. Seuss 韵律 + McCloskey 自然拟声 + Mem Fox |
| **0-1 岁** | 2026.9~2027.9 | 张秋生/孙敬修、极简句、感官启蒙、童谣风 | 极简词汇、重复拟声、McCloskey + Mem Fox 动物日常 |
| **1-3 岁** | 2027.9~2029.9 | 汤素兰/孙敬修、生活习惯/情绪认知、绘本大师风 | 重复句型、Seuss + 芝麻街 + McCloskey + Donaldson |
| **3-6 岁** | 2029.9~2032.9 | 郑渊洁/汤素兰、轻松冒险、幽默想象、科普叙事 | Dahl 转折幽默 + McCloskey 小镇冒险 + Donaldson 反转 |
| **6 岁+** | 2032.9+ | 全部风格完整融合、深层寓意、双语对照 | Twain 冒险 + Dahl 黑色幽默 + 全部风格完整融合 |

> **题材池（6 类，每篇选一；按日期确定性轮换，同日中英文选不同题材）：**
> 自然与科学启蒙（二十四节气/星空宇宙/微观世界/海洋雨林）· 中国文化与传统（节日传说/神话新编/古诗词意境/十二生肖）· 情感与心理（情绪小怪兽/安全感/家庭与爱/自我接纳）· 想象与奇幻（梦境探险/物品有灵/反向世界）· 生活与认知（职业初识/好习惯/食物旅行）· **轻松愉快的冒险**（寻宝/迷路回家/帮朋友/森林小任务，温和不刺激，以温暖回家收尾）。

> **中文风格库（6 核心 + 6 扩展）**：核心 — 孙敬修、郑渊洁、冰波、张秋生、金波、汤素兰；扩展 — 绘本大师风（几米/五味太郎/松居直）、北欧童话风（安徒生/林格伦）、日本童话风（宫泽贤治/新美南吉）、童谣民歌风、科普叙事风（斯凯瑞式）、轻松冒险风。
> **英文风格库（5 核心 + 6 扩展）**：核心 — Dr. Seuss、Sesame Street、Roald Dahl、Mark Twain、Robert McCloskey；扩展 — Julia Donaldson、Oliver Jeffers、Mem Fox / Bill Martin Jr、A.A. Milne、Beatrix Potter、Light adventure。
> **形式创新：** 互动式提问、系列化固定小主角连载、可吟唱旋律提示、大龄中英双语对照。

## 部署

### 两个云链接（CloudStudio）

- **H5 阅读器**：`https://9579701995034ab0af6d08e3b2292da7.app.codebuddy.work`
- **合集页面**：`https://268b20b7b5cb4295a01a09e5af8bf7ac.app.codebuddy.work`

每次生成新故事后，自动化任务会自动重新部署这两个链接。

**管理已发布的应用**：设置 → 数据管理 → 我发布的应用

### GitHub Pages（已上线）

- 目标链接：`https://ldy314.github.io/bebtime-stories/`
- 构建源：`main` 分支根目录（2026-07-29 已从 master 翻到 main，Pages 指向 main）

## 插图生成功能（Illustration Generator）

为每篇睡前故事生成一张「暖色儿童绘本风」插图，作为程序的**独立功能模块**。**仅本地保存到 `插图\`，不接入任何网页展示**（H5 阅读器 / 合集页均不含插图，符合最初需求）。

> **触发方式（重要）**：本功能**不接入每日自动化**（「睡前故事小程序」自动化只负责故事文本生成 / 部署 / 备份，绝不触发插图生成）。插图只在**用户手动调用**时生成——运行脚本产出 `illustration_jobs.json` 后，由用户 / 专家读取清单调用图像工具出图。脚本对已有插图是幂等的（按文件名 `done` 跳过），可随时手动重跑补生成。

### 模块与产物

| 路径 | 说明 |
|------|------|
| `scripts/generate_illustrations.py` | **功能模块（可移植单文件）** — 读取 stories.json，为每篇分配插画风格、构建中文绘图提示词、生成任务清单；并把"调哪个模型出图"抽象为 `ImageBackend` 接口（WorkBuddy / OpenAI / Stability / 本地SD 示例） |
| `插图\` | 输出目录，每篇一张 PNG，文件名 = 故事标题（如 `当当来我家.png`）；用 `safe_filename()` 清洗 emoji / Windows 非法字符 |
| `illustration_jobs.json` | 任务清单（含 `title` / `style_key` / `style_name` / `prompt` / `out_path` / `done`），供专家 / 自动化消费 |
| `illustration_assignments.json` | 风格分配持久化（标题→风格key）；catalog 改动不会破坏已生成图的风格标注，且新故事自动纳入新风格轮转 |
| `illustration_generation_queue.jsonl` | `--generate --backend workbuddy` 时产出的任务规格队列，交给 image-creator 智能体用 ImageGen 出图 |

### 风格策略（多风格轮转，丰富不单一）

内置 11 种暖色儿童绘本风（`STYLE_CATALOG`）：`几米梦境水彩` / `宫西达也大胆可爱` / `欧美经典绘本(Beatrix Potter)温馨细腻` / `长新太·佐野洋子轻柔诗意` / `艾瑞克·卡尔拼贴活泼` / `五味太郎极简暖色` / `Briony May Smith 温暖童话水彩` / `Robert McCloskey 经典美式绘本` / `Dr. Seuss 俏皮奇想` / `莫奈(Claude Monet)暖光印象` / `梵高(Vincent van Gogh)暖夜星辉`（后两者已引导向暖金、蜜橘、淡粉等暖调，保留印象派/后印象派笔触特征又契合睡前暖意）。新增风格只需往 `STYLE_CATALOG` 加一项即可。

- **4 张确认样张固定几米风**（`PINNED`）：小星星的暖暖、小种子的春天、月光小船（胎教期）、当当来我家。
- **其余篇在另外 10 种风格（含莫奈 / 梵高）间均衡轮转**（分配时排除几米，避免占比过高），整体风格更丰富多样；新增故事会自动纳入新风格轮转（见 `illustration_assignments.json` 持久化）。

### 运行方式

- `python scripts/generate_illustrations.py`（默认）：重建 `illustration_jobs.json` 与 `illustration_assignments.json`，按 `os.path.exists(out_path)` 标记 `done`，打印总数 / 风格分布 / 逐篇分配。风格分配持久化，重复运行不会打乱已生成图。
- **可移植出图**：`python scripts/generate_illustrations.py --generate --backend <name>`
  - `--backend workbuddy`：把待生成任务的 (prompt / out_path / size) 写入 `illustration_generation_queue.jsonl`，由 image-creator 智能体读取并用 ImageGen (HY-Image-V3.0) 出图（当前环境 Python 不能直接调 ImageGen）。
  - `--backend openai`：设 `OPENAI_API_KEY` 后直接调用 OpenAI 图像 API 出图（脚本已内置 `OpenAIBackend` 示例实现）。
  - `--backend stability` / `--backend local-sd`：按本机/本账号改写 `StabilityBackend` / `LocalSDBackend` 的 `generate()` 即可。
  - 追加 `--limit N --from M` 可分批出图（如 `--limit 8 --from 0`）。
  - 重置非固定/未生成图的风格分配（使其重新轮转、纳入莫奈/梵高）：`--reset-assignments`。
- **可移植性要点**：风格库 `STYLE_CATALOG` 与提示词构建 `build_prompt()` 是零依赖纯函数，可原样复制到任何环境；"换模型"=实现/选择 `ImageBackend.generate()`，无需改动风格与提示词。
- **限流约束**（WorkBuddy 直连 ImageGen 时）：账号级图像任务上限 150、同时间戳会撞名覆盖 → 出图需**逐张串行 + 生成即重命名 + 间隔 120–180s**。

## 安全注意事项

1. **DeepSeek API Key**：仅通过环境变量 `DEEPSEEK_API_KEY` 传递，GitHub Actions 使用 Secrets。绝不硬编码或用文件存储。
2. **`.gitignore`**：已排除 `.env*`、`credentials*`、`secret*`、`*.pem`、`*.key`。
3. **XSS 防护**：H5 `index.html` 有 `escapeHtml()` 函数，所有 `innerHTML` 插值均经转义。合集 HTML 生成脚本有 `esc()` 转义。
4. **stories.json 文本约束**：不得使用中文弯引号 `""`，用 `「」` 或单引号代替，否则 JSON 解析失败。

## 后续待办

- [ ] 复核故事完整性（当前 22 中文 + 13 英文，共 35 篇；会随睡前故事自动化动态增长，插图清单需随之重建）
- [ ] 删除 `master` 分支（Pages 已翻到 `main`，旧 master 可清理）
- [ ] 将读者端「故事风格介绍」板块部署到云端（已更新到本地与 D 盘，CloudStudio / GitHub Pages 待重新部署）
- [ ] 约 2026 年 9 月 22 日后，故事风格自动从胎教期切换到 0-1 岁阶段

## 当前数据统计

- 总故事数：**35 篇**（22 中文 + 13 英文，动态增长中）
- 覆盖日期：2026-07-16 ~ 2026-07-29
- 年龄段：全部为胎教期
- 中文 22 篇 / 英文 13 篇，共 35 篇（会随自动化动态增长）
- 已部署云端链接：CloudStudio 阅读器 + 合集页（2 个）+ GitHub Pages
