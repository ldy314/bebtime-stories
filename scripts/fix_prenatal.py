#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_prenatal.py
将《黑猫当当历险记》ep01-19 全部转为「胎教期」(prenatal)，并改为真实生成日期。
规则（用户 2026-07-31 明确）：
  - 故事的阶段只看【真实创作日期】，不看任何未来叙事日期。
  - 2026-09-22（预产期）之前创作的所有故事，无论多少，都属于胎教期。
  - 「宝宝出生」情节只能写在 2026-09-22 及之后。
因此：ep01-19 均创作于 2026-07-31（之前），全部 = 胎教期，且不得出现「已出生宝宝」内容。

处理：
  1) 三个 stories.json（Claw / D / github-pages）中 dangdang-ep01..19：
     - date/dateShort/ageGroup/ageLabel 统一为 2026-07-31 / 07/31 / prenatal / 胎教期
     - ep09 整篇重写为胎教期「茅山遇修猴子」（不再写出生）
     - ep10-19 做「已出生宝宝 -> 未出生（肚里等待）」措辞替换
  2) 三个 index.html 的 EMBEDDED_STORIES 单行由更新后的 stories.json 重建。
"""
import json
import os

# ---------- 路径 ----------
PAIRS = [
    ("C:/Users/Administrator/WorkBuddy/Claw/bedtime-story-app/stories.json",
     "C:/Users/Administrator/WorkBuddy/Claw/bedtime-story-app/index.html"),
    ("D:/code test/睡前故事/stories.json",
     "D:/code test/睡前故事/index.html"),
    ("D:/code test/睡前故事/github-pages/stories.json",
     "D:/code test/睡前故事/github-pages/index.html"),
    ("D:/code test/睡前故事/storyline/00-权威源文件/stories.json",
     None),  # 素材库镜像，无 index.html
]

DATE = "2026年7月31日 · 星期五"
DATE_SHORT = "07/31"
AGE_GROUP = "prenatal"
AGE_LABEL = "胎教期"

# ---------- ep09 全新胎教期内容（不再写出生） ----------
EP09 = {
    "title": "茅山遇修猴子",
    "preview": "一家人去常州近郊的仙山茅山，山顶老桃树下遇见会温和小法术的修猴子：教当当让桃叶轻轻飘、和南南开玩笑、把格格巫看呆的彩虹；结尾修猴子丢下一句『老友粉在广西等你们』，为日后的广西之旅埋下伏笔。整篇是当当讲给肚里还没来的宝宝听的冒险。",
    "moral": "奇妙的朋友要用温柔的方式相处；学到的本事要用来制造快乐，不用来捣乱。（这一程，当当都在跟肚里的小宝宝讲呢。）",
    "content": [
        "宝宝呀，你还住在妈妈肚子里，没来呢。这一周，咱们一家人去爬了茅山——那是离常州不远的一座仙山，道观藏在云雾里。",
        "山顶道观旁的老桃树下，坐着一位金红色的小猴子，身披迷你青色小道袍，腰间挂着装满鲜果的小布袋——他就是修猴子。别看他调皮，可是个会温和小法术的修道者。",
        "修猴子一见当当，眼睛亮了：小黑猫，来，我教你个好玩的！他掐了个诀，一片桃叶轻轻飘起来，在当当鼻尖打了个转，又稳稳落回手心。当当看得睁圆了金黄的眼睛，胸口那撮白毛都跟着翘了翘。修猴子说：这法术不伤人，只用来制造快乐。",
        "正说着，南南哼哧哼哧爬上山来，修猴子嘻嘻一笑，把南南的背包悄悄隐了身。南南急得满山找：我特产呢我特产呢！修猴子躲在树后偷笑，最后才把背包变回来，还附赠一颗鲜桃。南南佯装生气，实则乐呵呵：你这调皮猴子！",
        "爸爸蹲下来，让当当也试试。当当学着修猴子的样子，用小爪子轻轻一托，一片落叶真的慢慢飘了起来——虽然只飘了半寸就掉下，但全家都鼓起掌来。修猴子挠挠头：不错不错，有悟性！小不点用白毛蹭了蹭当当：弟弟，你也会魔法啦。",
        "忽然，远处的林子传来叽里咕噜的怪响——是格格巫！修猴子眉头一皱，掐诀喷出一小朵云，轻轻把格格巫的怪声音盖了过去；又变出一道小彩虹，横在格格巫面前。格格巫看呆了，忘了捣乱，尖帽子一歪坐下来看彩虹。",
        "修猴子还把一颗桃子塞给当当：常来玩，下次教你唤云朵。当当把这句话悄悄记在心里——真正的本事，不是用来吓人，而是用来让大家笑的。",
        "最妙的是，修猴子在桃树上晃着腿，远远丢下一句：老友粉在广西等你们哦！所以呀，等宝宝你来了，哥哥就带你去广西，看那位长鼻子的大象朋友。",
        "夜里，三只猫守在宝宝的小床边（床还空着，等你来）。当当把胸口白毛贴着宝宝的小床，咕噜咕噜：宝宝，今天当当学了会飘叶子的小法术，等你来了，当当飘叶子给你看。",
        "小不点用白毛蹭蹭当当：弟弟，你又交到奇妙的朋友啦。八百难得没躲，也挨过来，用壮实的身子挡在床角——守护队，连宝宝的空床也守得牢牢的。宝宝呀，山很高，朋友很多，往后的日子，还会有更多奇妙的朋友，等你，和当当，一起慢慢认识。"
    ]
}

# ---------- ep10-19 措辞替换（已出生 -> 未出生/等待） ----------
REPLACEMENTS = [
    ("三只猫挤在宝宝小床边", "三只猫守在宝宝的小床边（床还空着，等你来）"),
    ("三只猫挤在宝宝小床旁", "三只猫守在宝宝的小床边（床还空着，等你来）"),
    ("当当把胸口白毛贴着宝宝，", "当当把胸口白毛贴着宝宝的小床，"),
    ("当当把胸口白毛贴着宝宝。", "当当把胸口白毛贴着宝宝的小床。"),
    ("等你大了", "等你来了"),
    ("宝宝的笑脸就在心里", "宝宝的样子就在心里"),
    ("让宝宝贴紧", "守着还没来的宝宝"),
    # ep19 专属
    ("宝宝咯咯笑了一声（虽然还小，可好像真的被逗乐了）。",
     "宝宝在梦里弯了弯小嘴角（虽然还没来，可好像听见了）。"),
    ("逗得宝宝咯咯笑", "逗得宝宝在梦里弯了弯嘴角"),
    ("守护一个会笑的宝宝", "守护还没来的你"),
]


def fix_text(s):
    if not isinstance(s, str):
        return s
    for old, new in REPLACEMENTS:
        if old in s:
            s = s.replace(old, new)
    return s


def fix_story(st):
    ep = st.get("episode")
    if st.get("series") != "dangdang" or not isinstance(ep, int) or ep < 1 or ep > 19:
        return st
    # 元数据统一
    st["date"] = DATE
    st["dateShort"] = DATE_SHORT
    st["ageGroup"] = AGE_GROUP
    st["ageLabel"] = AGE_LABEL
    if ep == 9:
        st["title"] = EP09["title"]
        st["preview"] = EP09["preview"]
        st["moral"] = EP09["moral"]
        st["content"] = list(EP09["content"])
    elif ep >= 10:
        st["preview"] = fix_text(st.get("preview", ""))
        st["moral"] = fix_text(st.get("moral", ""))
        if isinstance(st.get("content"), list):
            st["content"] = [fix_text(p) for p in st["content"]]
        elif isinstance(st.get("content"), str):
            st["content"] = fix_text(st["content"])
    # ep01-08 仅改元数据（内容本就是胎教期），不动
    return st


def rebuild_embedded(index_path, stories):
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()
    new_line = "const EMBEDDED_STORIES = " + json.dumps(stories, ensure_ascii=False) + ";"
    lines = content.split("\n")
    replaced = False
    for i, line in enumerate(lines):
        if line.lstrip().startswith("const EMBEDDED_STORIES ="):
            lines[i] = new_line
            replaced = True
            break
    if not replaced:
        raise RuntimeError("EMBEDDED_STORIES not found in " + index_path)
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    for stories_path, index_path in PAIRS:
        if not os.path.exists(stories_path):
            print("SKIP (missing):", stories_path)
            continue
        with open(stories_path, "r", encoding="utf-8") as f:
            stories = json.load(f)
        changed = 0
        for st in stories:
            before = json.dumps(st, ensure_ascii=False)
            fix_story(st)
            after = json.dumps(st, ensure_ascii=False)
            if before != after:
                changed += 1
        with open(stories_path, "w", encoding="utf-8") as f:
            json.dump(stories, f, ensure_ascii=False, indent=2)
            f.write("\n")
        # 重建 index.html 内联数组
        if index_path and os.path.exists(index_path):
            rebuild_embedded(index_path, stories)
        print(f"OK {stories_path}  -> {changed} dangdang episodes modified; embedded rebuilt: {bool(index_path and os.path.exists(index_path))}")


if __name__ == "__main__":
    main()
