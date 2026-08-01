# -*- coding: utf-8 -*-
"""
generate_illustrations.py — 睡前故事「插图生成」功能模块（可移植版本）

把一个"为每篇睡前故事生成一张暖色绘本风插图"的完整逻辑保存为**单一可移植文件**：

  1. 读取 stories.json
  2. 为每篇故事分配一种插画风格（风格库见 STYLE_CATALOG，丰富多样、全部暖色）
  3. 构建绘图提示词（中文，模型无关，任何图像模型都能直接吃）
  4. 把插图保存到 插图/ 目录，文件名 = 故事标题
  5. 输出 illustration_jobs.json 任务清单；可选 --generate 直接调用图像后端出图

────────────────────────────────────────────────────────────────────────────
可移植性（PORTABILITY）
────────────────────────────────────────────────────────────────────────────
本文件的「风格库 / 提示词构建 / 任务编排」全部是纯 Python、零第三方依赖，
可以原样复制到任何环境。真正"调哪个模型出图"被抽象成 ImageBackend 接口：

  - WorkBuddyBackend : 当前环境——交给 image-creator 智能体用 ImageGen(HY-Image-V3.0) 出图
  - OpenAIBackend    : 移植到 OpenAI(gpt-image-1 / dall-e-3)，设 OPENAI_API_KEY 即用
  - StabilityBackend : 移植到 Stability AI，设 STABILITY_API_KEY
  - LocalSDBackend   : 移植到本地 Stable Diffusion / ComfyUI（示例，按本机改写）

切换目标模型 = 实现 / 选择一个 ImageBackend.generate()，无需改动风格库与提示词。

设计原则：
  - 本功能【只】生成并保存静态插图文件，【不】修改 index.html / 合集 等任何网页文件。
  - 手动触发、不进每日自动化；对已有插图幂等（按文件名 done 跳过），可随时重跑补生成。
"""

import json
import os
import argparse
from collections import Counter

# ----------------------------------------------------------------------------
# 路径配置（相对本脚本定位到项目根目录）
# ----------------------------------------------------------------------------
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORIES_JSON = os.path.join(BASE, "stories.json")
OUT_DIR = os.path.join(BASE, "插图")
MANIFEST = os.path.join(BASE, "illustration_jobs.json")
ASSIGNMENTS = os.path.join(BASE, "illustration_assignments.json")   # 风格分配持久化
QUEUE = os.path.join(BASE, "illustration_generation_queue.jsonl")   # WorkBuddy 后端给智能体的任务规格

# ----------------------------------------------------------------------------
# 暖色绘本插画风格库（丰富多样，全部以暖色调为主）
# 每种风格：key / name / prompt（中文，描述视觉处理与暖色走向，模型无关）
# 新增风格只需往这里加一项，并（可选）写进 PINNED / 旋转池。
# ----------------------------------------------------------------------------
STYLE_CATALOG = [
    {"key": "jimmy", "name": "几米（Jimmy Liao）梦境水彩",
     "prompt": "几米（Jimmy Liao）风格：梦境般的水彩质感，柔和晕染，细线条勾勒；"
               "小小角色置身辽阔安静的氛围空间里，温柔治愈，带着淡淡的思念与诗意"},
    {"key": "miyanishi", "name": "宫西达也 大胆可爱",
     "prompt": "宫西达也（Tatsuya Miyanishi）风格：大胆可爱的圆润造型，饱满粗放的线条，"
               "暖红橙主调，童趣温馨，角色表情生动憨厚，画面充满被爱包围的暖意"},
    {"key": "potter", "name": "欧美经典绘本（Beatrix Potter）温馨细腻",
     "prompt": "欧美经典绘本（Beatrix Potter / 彼得兔）风格：细腻写实的暖色描绘，"
               "柔和米色与大地色交织，复古治愈，细节丰富如旧时光里的插画，恬静温柔"},
    {"key": "nagata", "name": "长新太 / 佐野洋子 轻柔诗意",
     "prompt": "长新太 / 佐野洋子风格：轻柔诗意，淡彩与大量留白，温暖中带一点俏皮的荒诞感，"
               "构图舒缓，笔触松弛，像一首温柔的睡前童谣"},
    {"key": "carle", "name": "艾瑞克·卡尔（Eric Carle）拼贴活泼",
     "prompt": "艾瑞克·卡尔（Eric Carle）风格：手工拼贴质感，鲜艳的暖色块"
               "（橙、暖黄、珊瑚红、暖绿），纸张肌理明显，活泼童真，充满发现的惊喜"},
    {"key": "goto", "name": "五味太郎 极简暖色",
     "prompt": "五味太郎风格：极简明快的造型，平涂暖色块，童稚线条，干净幽默，"
               "信息清晰，留白充足，像孩子信手画出的温暖小世界"},
    {"key": "briony", "name": "Briony May Smith 温暖童话水彩",
     "prompt": "Briony May Smith 风格：细腻温暖的水彩，柔和光感与微妙纹理，"
               "常带一点童话与民间故事的魔法气息；角色置身开满花草的温柔自然里，"
               "暖金色夕照、柔润笔触，治愈又有故事感"},
    {"key": "mccloskey", "name": "Robert McCloskey 经典美式绘本",
     "prompt": "Robert McCloskey（罗伯特·麦克洛斯基）风格：经典美式绘本，"
               "钢笔线条加柔和淡彩，朴素温润的乡村与生活气息，笔触沉稳可爱；"
               "暖褐、奶白与柔蓝交织的怀旧暖调，安静恬淡"},
    {"key": "seuss", "name": "Dr. Seuss 俏皮奇想",
     "prompt": "Dr. Seuss（苏斯博士）风格：俏皮夸张的线条与天马行空的奇想角色，"
               "活泼跳脱的构图与童趣想象力；以暖奶油底色搭配柔和的红、橘、暖黄，"
               "让画面既 playful 又温暖，适合睡前"},
    {"key": "monet", "name": "莫奈（Claude Monet）暖光印象",
     "prompt": "克劳德·莫奈（Claude Monet）印象派风格：柔光晕染与松散的笔触，"
               "捕捉清晨与黄昏的暖色光线；朦胧的暖金、蜜橘、淡粉与奶白交织，"
               "水汽与花影轻轻荡漾，宁静梦幻，像被温柔光包裹的睡前一幕"},
    {"key": "vangogh", "name": "梵高（Vincent van Gogh）暖夜星辉",
     "prompt": "文森特·梵高（Vincent van Gogh）风格：标志性的旋动笔触与厚重油彩质感，"
               "以温暖的星夜金、琥珀、蜜橘与柔蓝取代冷调，画面涌动着温柔的光与爱；"
               "宁静的村庄、暖灯与夜空星辰，治愈而有力量，适合睡前"},
]

# 4 张确认样张固定几米风；其余在旋转池（排除几米，含莫奈/梵高等）均衡轮转
PINNED = {
    "小星星的暖暖": "jimmy",
    "小种子的春天": "jimmy",
    "月光小船（胎教期）": "jimmy",
    "当当来我家": "jimmy",
}
_ROTATION = [s for s in STYLE_CATALOG if s["key"] != "jimmy"]
_BY_KEY = {s["key"]: s for s in STYLE_CATALOG}


# ----------------------------------------------------------------------------
# 文件名安全清洗（去掉 emoji / Windows 非法字符，保留中文与常用标点）
# ----------------------------------------------------------------------------
def safe_filename(title):
    out = []
    for ch in title:
        o = ord(ch)
        if o > 0xFFFF:          # 丢弃 emoji / 非 BMP 字符（如 🔬）
            continue
        if ch in '/\\:*?"<>|':   # Windows 非法字符
            continue
        out.append(ch)
    name = "".join(out).strip()
    return name or "story"


# ----------------------------------------------------------------------------
# 风格分配（带持久化：catalog 改动不会影响已生成图的风格标注）
# ----------------------------------------------------------------------------
def load_assignments():
    """读取已持久化的 标题→风格key 映射；首次引入时从现有清单播种，保持 35 张不变。"""
    if os.path.exists(ASSIGNMENTS):
        try:
            return json.load(open(ASSIGNMENTS, encoding="utf-8"))
        except Exception:
            pass
    if os.path.exists(MANIFEST):
        try:
            m = json.load(open(MANIFEST, encoding="utf-8"))
            return {j["title"]: j["style_key"] for j in m.get("jobs", [])}
        except Exception:
            pass
    return {}


def save_assignments(assign):
    with open(ASSIGNMENTS, "w", encoding="utf-8") as f:
        json.dump(assign, f, ensure_ascii=False, indent=2)


def assign_style(title, counter, assign):
    if title in PINNED:
        return PINNED[title]
    if title in assign:
        return assign[title]
    style = _ROTATION[counter % len(_ROTATION)]
    return style["key"]


# ----------------------------------------------------------------------------
# 提示词构建（模型无关，纯文本；任何图像模型都能直接吃）
# ----------------------------------------------------------------------------
def build_prompt(story, style_key):
    style = _BY_KEY[style_key]
    scene = "画面主题：{title}。{preview}".format(
        title=story.get("title", ""),
        preview=(story.get("preview") or "")[:60],
    )
    return (
        f"{scene}。"
        f"{style['prompt']}。"
        "整体为儿童绘本插图质感，3:4 竖版构图，暖色调为主"
        "（暖黄、奶油、柔粉、蜜橘、淡金、暖米），治愈温暖，"
        "细腻笔触，留白呼吸感，非常适合睡前故事。"
        "【重要约束】：画面中不得出现任何文字、字母、数字、"
        "拼音、符号或水印。纯插图，无任何文本元素。"
    )


# ----------------------------------------------------------------------------
# 构建任务清单
# ----------------------------------------------------------------------------
def build_jobs(reset=False):
    """读取 stories.json，构建全部插图任务（含风格分配与提示词）。"""
    with open(STORIES_JSON, encoding="utf-8") as f:
        stories = json.load(f)

    assign = load_assignments()
    if reset:
        # 仅保留「已固定样张」与「已生成文件」的分配，其余清空 → 重新轮转（含新风格）
        keep = {}
        for t, k in assign.items():
            if t in PINNED or os.path.exists(os.path.join(OUT_DIR, safe_filename(t) + ".png")):
                keep[t] = k
        assign = keep

    jobs = []
    counter = 0
    for story in stories:
        title = story.get("title", "")
        key = assign_style(title, counter, assign)
        if title not in PINNED and title not in assign:
            assign[title] = key
            counter += 1
        fname = safe_filename(title) + ".png"
        out_path = os.path.join(OUT_DIR, fname)
        jobs.append({
            "title": title,
            "language": story.get("language", ""),
            "ageLabel": story.get("ageLabel", ""),
            "style_key": key,
            "style_name": _BY_KEY[key]["name"],
            "prompt": build_prompt(story, key),
            "out_path": out_path,
            "done": os.path.exists(out_path),
        })
    save_assignments(assign)
    return jobs


def write_manifest(jobs):
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump({
            "out_dir": OUT_DIR,
            "note": "本清单由 generate_illustrations.py 生成；done=true 表示插图已存在，可跳过。",
            "jobs": jobs,
        }, f, ensure_ascii=False, indent=2)


def print_summary(jobs):
    done = sum(1 for j in jobs if j["done"])
    print("=" * 78)
    print(f"插图任务总数：{len(jobs)}  |  已完成（文件存在）：{done}  |  待生成：{len(jobs) - done}")
    print(f"输出目录：{OUT_DIR}")
    print("-" * 78)
    cnt = Counter(j["style_name"] for j in jobs)
    print("风格分布：")
    for name, n in cnt.items():
        print(f"  - {name}: {n} 张")
    print("-" * 78)
    print("逐篇分配：")
    for i, j in enumerate(jobs, 1):
        flag = "✓" if j["done"] else " "
        print(f"  [{flag}] {i:2d}. 《{j['title']}》 → {j['style_name']}")


# ----------------------------------------------------------------------------
# 后端抽象（可移植核心）：实现一个 ImageBackend.generate() 即可换模型
# ----------------------------------------------------------------------------
class ImageBackend:
    """图像生成后端接口。移植到新模型 / 软件时，只需实现 generate()。"""
    name = "base"

    def generate(self, prompt, out_path, size=(1024, 1536), **kwargs):
        raise NotImplementedError


class WorkBuddyBackend(ImageBackend):
    """
    当前环境后端：本环境 Python 不能直接调用 ImageGen，
    因此 generate() 把 (提示词 + 输出路径 + 尺寸) 写成任务规格，追加到 QUEUE 文件，
    由 image-creator 智能体读取并用 ImageGen (HY-Image-V3.0) 出图。
    """
    name = "workbuddy"

    def __init__(self, queue_path=QUEUE):
        self.queue_path = queue_path
        open(self.queue_path, "w", encoding="utf-8").close()  # 清空旧队列

    def generate(self, prompt, out_path, size=(1024, 1536), **kwargs):
        spec = {"prompt": prompt, "out_path": out_path,
                "size": list(size), "quality": "high"}
        with open(self.queue_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(spec, ensure_ascii=False) + "\n")
        return True


class OpenAIBackend(ImageBackend):
    """移植示例：OpenAI 图像 API。设 OPENAI_API_KEY 后可直接出图。"""
    name = "openai"

    def __init__(self, model="gpt-image-1", size="1024x1536", quality="high"):
        from openai import OpenAI
        self.client = OpenAI()
        self.model = model
        self.size = size
        self.quality = quality

    def generate(self, prompt, out_path, size=(1024, 1536), **kwargs):
        sz = f"{size[0]}x{size[1]}"
        resp = self.client.images.generate(
            model=self.model, prompt=prompt, size=sz, quality=self.quality)
        import base64
        b64 = resp.data[0].b64_json          # gpt-image-1 返回 b64
        with open(out_path, "wb") as f:
            f.write(base64.b64decode(b64))
        return True


class StabilityBackend(ImageBackend):
    """移植示例：Stability AI。设 STABILITY_API_KEY 后按官方 REST API 改写 generate()。"""
    name = "stability"

    def __init__(self, model="stable-diffusion-xl-1024-1024"):
        self.model = model

    def generate(self, prompt, out_path, size=(1024, 1536), **kwargs):
        # TODO: 按 Stability AI 文档实现（multipart 上传 prompt → 下载图片到 out_path）
        raise NotImplementedError("请按 Stability AI 文档实现 generate()")


class LocalSDBackend(ImageBackend):
    """移植示例：本地 Stable Diffusion / ComfyUI。按本机推理脚本改写 generate()。"""
    name = "local-sd"

    def generate(self, prompt, out_path, size=(1024, 1536), **kwargs):
        # TODO: 调用本机 SD / ComfyUI（如 subprocess 调 cli，或 POST 到本地 API）
        raise NotImplementedError("请按本机 SD / ComfyUI 调用方式实现 generate()")


def get_backend(name, **cfg):
    name = (name or "workbuddy").lower()
    if name == "workbuddy":
        return WorkBuddyBackend(**cfg)
    if name == "openai":
        return OpenAIBackend(**cfg)
    if name == "stability":
        return StabilityBackend(**cfg)
    if name == "local-sd":
        return LocalSDBackend(**cfg)
    raise ValueError(f"未知后端: {name}")


# ----------------------------------------------------------------------------
# 生成驱动
# ----------------------------------------------------------------------------
def run_generation(backend_name, limit=None, start=0):
    jobs = json.load(open(MANIFEST, encoding="utf-8"))["jobs"]
    pending = [j for j in jobs if not j["done"]]
    batch = pending[start:start + (limit or len(pending))]
    be = get_backend(backend_name)
    print(f"使用后端 [{be.name}]，本次处理 {len(batch)} 张")
    for j in batch:
        ok = be.generate(j["prompt"], j["out_path"])
        print(f"  {'✓' if ok else '✗'} {j['title']}")
    if backend_name == "workbuddy":
        print(f"任务规格已写入：{QUEUE}（交给 image-creator 智能体执行出图）")


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------
def main():
    p = argparse.ArgumentParser(description="睡前故事插图生成（可移植版）")
    p.add_argument("--build", action="store_true",
                   help="重建 illustration_jobs.json（默认行为）")
    p.add_argument("--reset-assignments", action="store_true",
                   help="清空非固定/未生成图的风格分配，使其重新轮转（含新风格）")
    p.add_argument("--generate", action="store_true",
                   help="调用图像后端出图")
    p.add_argument("--backend", default="workbuddy",
                   help="后端：workbuddy / openai / stability / local-sd")
    p.add_argument("--limit", type=int, default=None,
                   help="--generate 时本批最大张数")
    p.add_argument("--from", type=int, default=0, dest="start",
                   help="--generate 起始偏移")
    args = p.parse_args()

    if args.generate:
        run_generation(args.backend, limit=args.limit, start=args.start)
        return

    jobs = build_jobs(reset=args.reset_assignments)
    write_manifest(jobs)
    print_summary(jobs)
    print(f"\n任务清单已写入：{MANIFEST}")
    print("（默认仅产出清单；出图请用 --generate --backend <name>，"
          "或在 WorkBuddy 中把清单交给 image-creator 智能体读取执行。）")


if __name__ == "__main__":
    main()
