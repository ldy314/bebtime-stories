# 睡前故事 (Bedtime Stories)

每日自动生成中英文双语睡前故事，通过 GitHub Actions + DeepSeek API 驱动。

## Project

- **用途**: 为未出生宝宝（预产期 2026-09-22）每日生成胎教/哄睡故事，中英文各一篇
- **栈**: Node.js (生成脚本) + Python (本地批量脚本) + 纯静态 HTML/CSS (前端)
- **仓库**: https://github.com/ldy314/bebtime-stories
- **双目录结构**: 根目录是本地工作区，`github-pages/` 是 GitHub Pages 发布目录

## Commands

- **生成缺失故事** (GitHub Actions 自动): 在 `github-pages/` 目录下运行 `node scripts/generate-story.js`
- **生成合集 HTML**: `node scripts/generate-collection-html.js` (在对应目录下)
- **手动触发**: GitHub → Actions → Generate Bedtime Stories → Run workflow
- **本地批量生成** (Python, 一次性): `python scripts/generate_stories.py` (硬编码数据，非 API)
- **补齐页面文件**: `python scripts/generate_missing_pages.py` (从 stories.json 生成缺失的 HTML 页面)

## Architecture

```
睡前故事/
├── .github/workflows/generate-stories.yml  # 自动工作流 (UTC 18:00 定时 + 手动触发)
├── github-pages/                            # GitHub Pages 发布内容
│   ├── scripts/
│   │   ├── generate-story.js                # ★ 主生成脚本 (DeepSeek API)
│   │   ├── prompt-builder.js                # 提示词构建 + 年龄分组 + 风格模板
│   │   └── generate-collection-html.js      # 合集页面生成
│   ├── stories.json                         # 所有故事数据
│   ├── index.html                           # H5 阅读器 (含 EMBEDDED_STORIES)
│   ├── collection.html                      # 故事合集页面
│   └── bedtime-story-YYYY-MM-DD.html        # 单日故事页面
├── scripts/                                 # 本地脚本
│   ├── generate_stories.py                  # 硬编码故事批量生成
│   └── generate_missing_pages.py            # 从 stories.json 补 HTML 页面
├── index.html                               # 根目录前端 (同步自 github-pages/)
├── stories.json                             # 根目录数据 (同步自 github-pages/)
└── bedtime-story-*.html                     # 根目录页面 (同步自 github-pages/)
```

**数据流**: DeepSeek API → generate-story.js → stories.json → index.html (EMBEDDED_STORIES) + collection.html + 单页 HTML

**核心常量**: `CHILD_BIRTHDAY = '2026-09-22'` (在 `prompt-builder.js` 中)。年龄分组: prenatal(胎教期), 0-1, 1-3, 3-6, 6+。

## Conventions

- **中英文各一篇**: 每天生成 `*-cn` 和 `*-en` 两篇故事
- **故事 ID 格式**: `YYYY-MM-DD-语言代码` (如 `2026-07-28-cn`)
- **JSON 字段**: `id`, `date`(含星期), `dateShort`(MM/DD), `title`, `language`, `ageGroup`, `ageLabel`, `preview`, `moral`, `content`(段落数组)
- **引号禁用**: JSON 中不使用中文弯引号 `""`，使用 `「」` 或 `''`
- **前端数据**: `index.html` 中 `const EMBEDDED_STORIES = [...]` 内嵌所有故事数据
- **同步规则**: `github-pages/` 是源，根目录是副本。workflow 运行后自动 `cp` 同步到根目录
- **DeepSeek API**: 环境变量 `DEEPSEEK_API_KEY`，模型 `deepseek-chat`，需 `response_format: { type: 'json_object' }`
- **年龄分组依据**: 以预产期 2026-09-22 为基准，按日期计算

## Notes

<!-- 快速记录区 -->
