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

## 关键目录与文件

### 1. 核心数据与页面

| 路径 | 说明 |
|------|------|
| `C:\Users\Administrator\WorkBuddy\Claw\bedtime-story-app\stories.json` | **唯一的数据库** — 全部故事 JSON 数组，25 篇（14 中文 + 11 英文） |
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

## 安全注意事项

1. **DeepSeek API Key**：仅通过环境变量 `DEEPSEEK_API_KEY` 传递，GitHub Actions 使用 Secrets。绝不硬编码或用文件存储。
2. **`.gitignore`**：已排除 `.env*`、`credentials*`、`secret*`、`*.pem`、`*.key`。
3. **XSS 防护**：H5 `index.html` 有 `escapeHtml()` 函数，所有 `innerHTML` 插值均经转义。合集 HTML 生成脚本有 `esc()` 转义。
4. **stories.json 文本约束**：不得使用中文弯引号 `""`，用 `「」` 或单引号代替，否则 JSON 解析失败。

## 后续待办

- [ ] 补全个别缺失的英文故事（当前 cn 14 / en 11，个别日期英文待云端 Actions 补齐或本地兜底）
- [ ] 删除 `master` 分支（Pages 已翻到 `main`，旧 master 可清理）
- [ ] 将读者端「故事风格介绍」板块部署到云端（已更新到本地与 D 盘，CloudStudio / GitHub Pages 待重新部署）
- [ ] 约 2026 年 9 月 22 日后，故事风格自动从胎教期切换到 0-1 岁阶段

## 当前数据统计

- 总故事数：**25 篇**（14 中文 + 11 英文）
- 覆盖日期：2026-07-16 ~ 2026-07-29
- 年龄段：全部为胎教期
- 英文个别日期待补齐（cn 14 / en 11）
- 已部署云端链接：CloudStudio 阅读器 + 合集页（2 个）+ GitHub Pages
