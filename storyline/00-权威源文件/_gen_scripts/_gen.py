# -*- coding: utf-8 -*-
import json, os, re

BASE = r"D:\code test\睡前故事\storyline"
SRC = os.path.join(BASE, "00-权威源文件")

def w(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("wrote", path)

# ---------- 1) 已发布故事（来自 stories.json, series=dangdang） ----------
data = json.load(open(os.path.join(SRC, "stories.json"), encoding="utf-8"))
dn = sorted([s for s in data if s.get("series") == "dangdang"], key=lambda x: x.get("episode", 0))
ep_archive_dir = os.path.join(BASE, "05-故事历史档案库", "已发布故事")
rows = []
for s in dn:
    ep = s.get("episode")
    title = s.get("title", "")
    fname = f"ep{ep:02d}-{title}.md"
    body = []
    body.append(f"# 第{ep}集 · 《{title}》")
    body.append("")
    body.append(f"- **id**：{s.get('id')}")
    body.append(f"- **日期**：{s.get('date')}")
    body.append(f"- **年龄段**：{s.get('ageLabel')}（{s.get('ageGroup')}）")
    body.append(f"- **教育点**：{s.get('moral')}")
    body.append(f"- **导语**：{s.get('preview')}")
    body.append("")
    body.append("## 正文")
    body.append("")
    for i, para in enumerate(s.get("content", []), 1):
        body.append(f"{i}. {para}")
    body.append("")
    w(os.path.join(ep_archive_dir, fname), "\n".join(body))
    rows.append((ep, s.get("id"), title, s.get("date"), s.get("ageLabel"), s.get("moral")))

# ---------- 2) 全局检索索引（来自 state.json + stories.json） ----------
state = json.load(open(os.path.join(SRC, "dangdang-series-state.json"), encoding="utf-8"))
idx = []
idx.append("# 黑猫当当历险记 · 全局故事检索索引")
idx.append("")
idx.append("> 自动生成自 `dangdang-series-state.json` 与 `stories.json`，供创作者快速检索定位。")
idx.append("")
idx.append(f"- **系列名**：{state.get('seriesTitle')}")
idx.append(f"- **下一集编号（episode）**：{state.get('episode')}")
idx.append(f"- **最近生成日期**：{state.get('lastGeneratedDate')}")
arc = state.get("arc", {})
idx.append(f"- **当前故事线（arc）**：{arc.get('current')}（自第{arc.get('startedEpisode')}集开启）")
idx.append(f"  - 说明：{arc.get('description')}")
idx.append(f"- **文档创建于**：{state.get('createdAt')}")
idx.append("")
idx.append("## 一、连续性日志（continuity）")
idx.append("")
for c in state.get("continuity", []):
    idx.append(f"- {c}")
idx.append("")
idx.append("## 二、已发布分集检索表")
idx.append("")
idx.append("| 集 | id | 标题 | 日期 | 年龄段 | 教育点 |")
idx.append("|----|----|------|------|--------|--------|")
for ep, sid, title, date, age, moral in rows:
    idx.append(f"| {ep} | {sid} | 《{title}》 | {date} | {age} | {moral} |")
idx.append("")
idx.append("## 三、跨集关联（linkages）")
idx.append("")
lk = state.get("linkages", [])
idx.append("（暂无，或由自动化后续补充）" if not lk else "\n".join(f"- {x}" for x in lk))
idx.append("")
w(os.path.join(BASE, "05-故事历史档案库", "全局检索索引.md"), "\n".join(idx))

# ---------- 3) 分集大纲（直接归档 outline） ----------
import shutil
shutil.copy(os.path.join(SRC, "dangdang-series-outline.md"),
            os.path.join(BASE, "05-故事历史档案库", "分集大纲.md"))

# ---------- 4) 目的地 → 场景 / 美食 / 灵感 解析 ----------
dest_text = open(os.path.join(SRC, "dangdang-destinations.md"), encoding="utf-8").read()
# 按二级标题切分目的地块（遇到一级标题“# 目的地 × 月度微博 feed”停止）
lines = dest_text.splitlines()
blocks = {}  # name -> {meta, 文化, 民俗, 美食, 景点, 自然景观}
cur = None
section = None
buf = {}
meta_lines = []
for ln in lines:
    if ln.startswith("# 目的地 × 月度微博 feed"):
        break
    if ln.startswith("## "):
        # 保存上一个
        if cur is not None:
            blocks[cur] = {"meta": meta_lines, "sections": buf}
        cur = ln[3:].strip()
        buf = {}
        meta_lines = []
        section = None
        continue
    if ln.startswith("### "):
        section = ln[4:].strip()
        buf[section] = []
        continue
    if cur is None:
        continue
    if section is None:
        if ln.strip():
            meta_lines.append(ln.strip())
    else:
        buf[section].append(ln)
# 最后一个
if cur is not None:
    blocks[cur] = {"meta": meta_lines, "sections": buf}

SCENE_DIR = os.path.join(BASE, "02-场景背景素材库", "地域专属户外场景")
FOOD_DIR = os.path.join(BASE, "03-道具与美食素材库")
INSPIRE_DIR = os.path.join(BASE, "06-创作灵感素材库")

# 4a) 每个目的地一个场景文件
food_all = ["# 各地特色美食（按目的地归档）\n",
            "\n> 来源：`dangdang-destinations.md`，写作旅游单元直接取用。\n"]
inspire_all = ["# 场景奇遇灵感（场景 + 事件绑定）\n",
               "\n> 把「目的地景点 + 自然景观」整理为可入戏的奇遇场景。来源：`dangdang-destinations.md`。\n"]
for name, b in blocks.items():
    meta = "\n".join(b["meta"])
    sec = b["sections"]
    # 场景文件
    sc = [f"# 场景 · {name}", "", f"> {meta}", ""]
    for key in ["文化", "民俗", "景点", "自然景观"]:
        if key in sec:
            txt = "\n".join(sec[key]).strip()
            if txt:
                sc.append(f"## {key}")
                sc.append("")
                sc.append(txt)
                sc.append("")
    w(os.path.join(SCENE_DIR, f"{name}.md"), "\n".join(sc))
    # 美食汇总
    if "美食" in sec:
        ftxt = "\n".join(sec["美食"]).strip()
        if ftxt:
            food_all.append(f"## {name}")
            food_all.append("")
            food_all.append(ftxt)
            food_all.append("")
    # 灵感汇总
    ins = []
    if "景点" in sec:
        ins.append("\n".join(sec["景点"]).strip())
    if "自然景观" in sec:
        ins.append("\n".join(sec["自然景观"]).strip())
    ins_txt = "\n".join([x for x in ins if x])
    if ins_txt:
        inspire_all.append(f"## {name}")
        inspire_all.append("")
        inspire_all.append(ins_txt)
        inspire_all.append("")

w(os.path.join(FOOD_DIR, "各地特色美食.md"), "\n".join(food_all))
w(os.path.join(INSPIRE_DIR, "场景奇遇灵感.md"), "\n".join(inspire_all))

print("destinations parsed:", len(blocks))
print("done")
