# 04 · 插画美术风格库

> 本库定义系列插图的美术规范。**重要：插图为可选独立模块，仅本地保存到 `插图\`，不接入任何网页展示**（H5 阅读器/合集页均不含插图）。

## 文件
| 文件 | 内容 |
|------|------|
| `风格规范与目录.md` | 内置 11 种暖色儿童绘本风（STYLE_CATALOG）、4 张 PINNED 几米风、风格轮转策略、运行方式、统一美术方向 |
| `插图任务清单说明.md` | `illustration_jobs.json` / `illustration_assignments.json` 结构说明与消费方式 |

## 11 种绘本风速览
几米梦境水彩 · 宫西达也大胆可爱 · Beatrix Potter 温馨细腻 · 长新太·佐野洋子轻柔诗意 · 艾瑞克·卡尔拼贴活泼 · 五味太郎极简暖色 · Briony May Smith 温暖童话水彩 · Robert McCloskey 经典美式绘本 · Dr. Seuss 俏皮奇想 · 莫奈暖光印象 · 梵高暖夜星辉

## 概念美术方向（与 11 风互补）
圆角平涂绘本风（正文主风格）· 民间年画简化风（当当主视觉/封面）· 淡彩水彩治愈风（旅行篇章）· Q版大头卡通风（头像卡）· 新国风水墨卡通风（民俗古镇）· 黏土3D立体风（海报）

## 运行（脚本在 `scripts/generate_illustrations.py`）
- `python scripts/generate_illustrations.py` → 重建 `illustration_jobs.json` 与 `illustration_assignments.json`，按文件存在标 `done`。
- 出图：`--generate --backend workbuddy` 写队列交 image-creator 用 ImageGen(HY-Image-V3.0)；或 openai/stability/local-sd。
- 限流：逐张串行 + 间隔 120–180s。

## 权威源
`AGENTS.md` 插图生成功能章节（STYLE_CATALOG）
