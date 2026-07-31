# -*- coding: utf-8 -*-
"""
QA 校验脚本：黑猫当当历险记 ep01~ep06 集成质量校验
Author: Edward (QA Engineer)
Usage: python qa_verify_dangdang.py
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

APP = r"C:\Users\Administrator\WorkBuddy\Claw\bedtime-story-app"
SJ = r"D:\code test\睡前故事"
GP = r"D:\code test\睡前故事\github-pages"
STATE_AUTO = r"C:\Users\Administrator\WorkBuddy\automation-2026-07-16-11-56-46\dangdang-series-state.json"

STORIES = {
    "app/stories.json": os.path.join(APP, "stories.json"),
    "睡前故事/stories.json": os.path.join(SJ, "stories.json"),
    "github-pages/stories.json": os.path.join(GP, "stories.json"),
}
INDEXES = {
    "app/index.html": os.path.join(APP, "index.html"),
    "睡前故事/index.html": os.path.join(SJ, "index.html"),
    "github-pages/index.html": os.path.join(GP, "index.html"),
}
COLLECTIONS = {
    "bedtime-story-collection.html": os.path.join(SJ, "bedtime-story-collection.html"),
    "github-pages/collection.html": os.path.join(GP, "collection.html"),
    "bedtime-story-collection.md": os.path.join(SJ, "bedtime-story-collection.md"),
}
STATES = {
    "automation/dangdang-series-state.json": STATE_AUTO,
    "睡前故事/dangdang-series-state.json": os.path.join(SJ, "dangdang-series-state.json"),
    "github-pages/dangdang-series-state.json": os.path.join(GP, "dangdang-series-state.json"),
}

EP_IDS = [f"dangdang-ep{i:02d}-zh" for i in range(1, 7)]
EP_TITLES = {
    2: "当当大战一只耳",
    3: "爬山看星星",
    4: "老钟楼的秘密",
    5: "龙宫的珍珠",
    6: "智斗格格巫",
}
BANNED = ["博物", "环球科学", "国家地理", "据《", "杂志"]
CURLY = ["\u201c", "\u201d"]
RULE_SENTENCE = (
    "爸爸妈妈立下了几条家规：听见名字要答应、要回家；出门要牵好小绳绳；"
    "不可以抓沙发；还要一起保护好宝宝——宝宝是家里最小、最宝贝的小成员，三只猫都要当他的小守护。"
)
OLD_TAIL = "来保护他的家人啦。"

results = {}   # name -> (bool, [evidence lines])


def record(key, ok, lines):
    results[key] = (ok, lines)


def read(path):
    with io.open(path, encoding="utf-8") as f:
        return f.read()


def load_json(path):
    return json.loads(read(path))


def extract_embedded(path):
    """从 index.html 中提取 EMBEDDED_STORIES 数组并解析。"""
    txt = read(path)
    m = re.search(r"const\s+EMBEDDED_STORIES\s*=\s*(\[)", txt)
    if not m:
        raise ValueError("未找到 EMBEDDED_STORIES 定义")
    start = m.start(1)
    depth, in_str, esc = 0, False, False
    for i in range(start, len(txt)):
        c = txt[i]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
            continue
        if c == '"':
            in_str = True
        elif c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                return json.loads(txt[start:i + 1])
    raise ValueError("EMBEDDED_STORIES 数组未闭合")


def series_of(arr):
    return {s["id"]: s for s in arr if str(s.get("id", "")).startswith("dangdang-ep")}


def core(s):
    """用于跨副本比对的核心字段快照。"""
    return {k: s.get(k) for k in
            ("id", "title", "content", "series", "seriesTitle", "episode",
             "preview", "moral", "date", "language")}


# ---------------- 1. JSON 合法性 ----------------
parsed, ev, ok1 = {}, [], True
for name, p in STORIES.items():
    try:
        arr = load_json(p)
        parsed[name] = arr
        ser = series_of(arr)
        missing = [i for i in EP_IDS if i not in ser]
        flag = (not missing) and len(ser) == 6
        ok1 &= flag
        ev.append(f"{'OK ' if flag else 'NG '} {name}: 解析成功, 总条数={len(arr)}, "
                  f"系列条数={len(ser)}, 缺失={missing or '无'}")
    except Exception as e:
        ok1 = False
        ev.append(f"NG  {name}: 解析失败 -> {e!r}")
totals = {n: len(a) for n, a in parsed.items()}
same_total = len(set(totals.values())) == 1
ok1 &= same_total
ev.append(f"{'OK ' if same_total else 'NG '} 三处总条数一致: {totals}")
record("1. JSON合法性&6条系列条目", ok1, ev)

# ---------------- 2. 三处 stories.json 一致 ----------------
ev, ok2 = [], True
names = list(parsed.keys())
if len(names) == 3:
    base = names[0]
    base_ser = {i: core(series_of(parsed[base])[i]) for i in EP_IDS if i in series_of(parsed[base])}
    for other in names[1:]:
        oser = series_of(parsed[other])
        for eid in EP_IDS:
            a, b = base_ser.get(eid), core(oser[eid]) if eid in oser else None
            if a != b:
                ok2 = False
                diff = [k for k in a if b is None or a.get(k) != b.get(k)] if a else ["<缺失>"]
                ev.append(f"NG  {other} 的 {eid} 与 {base} 不一致, 差异字段={diff}")
    # 整库对象级比对
    for other in names[1:]:
        same_all = parsed[base] == parsed[other]
        ev.append(f"{'OK ' if same_all else 'NG '} 整库对象级比对 {base} vs {other}: "
                  f"{'完全一致' if same_all else '存在差异'}")
        ok2 &= same_all
    if ok2:
        ev.append("OK  ep01~ep06 的 title/content/series/seriesTitle/episode 三处完全一致")
else:
    ok2 = False
    ev.append("NG  可解析副本数不足 3")
record("2. 三处stories.json一致", ok2, ev)

# ---------------- 3. 三处 index.html EMBEDDED_STORIES 一致 ----------------
ev, ok3, emb = [], True, {}
for name, p in INDEXES.items():
    try:
        arr = extract_embedded(p)
        emb[name] = arr
        ser = series_of(arr)
        missing = [i for i in EP_IDS if i not in ser]
        flag = not missing
        ok3 &= flag
        ev.append(f"{'OK ' if flag else 'NG '} {name}: 解析成功, 总条数={len(arr)}, "
                  f"系列条数={len(ser)}, 缺失={missing or '无'}")
    except Exception as e:
        ok3 = False
        ev.append(f"NG  {name}: 提取/解析失败 -> {e!r}")
if len(emb) == 3:
    en = list(emb.keys())
    for other in en[1:]:
        same = emb[en[0]] == emb[other]
        ok3 &= same
        ev.append(f"{'OK ' if same else 'NG '} EMBEDDED_STORIES 比对 {en[0]} vs {other}: "
                  f"{'完全一致' if same else '存在差异'}")
    # 与 stories.json 交叉比对
    if parsed:
        cross = emb[en[0]] == parsed[names[0]]
        ev.append(f"{'OK ' if cross else '!! '} 交叉比对 index.html 与 stories.json: "
                  f"{'一致' if cross else '不一致(参考项)'}")
record("3. 三处EMBEDDED_STORIES一致", ok3, ev)

# ---------------- 后续检查基于基准副本 ----------------
BASE = series_of(parsed[names[0]]) if parsed else {}

# ---------------- 4. 系列字段正确 ----------------
ev, ok4 = [], True
for n, eid in enumerate(EP_IDS, start=1):
    s = BASE.get(eid)
    if not s:
        ok4 = False
        ev.append(f"NG  {eid}: 缺失")
        continue
    c1 = s.get("series") == "dangdang"
    c2 = s.get("seriesTitle") == "黑猫当当历险记"
    c3 = isinstance(s.get("episode"), int) and not isinstance(s.get("episode"), bool) \
        and s.get("episode") == n
    good = c1 and c2 and c3
    ok4 &= good
    ev.append(f"{'OK ' if good else 'NG '} {eid}: series={s.get('series')!r} "
              f"seriesTitle={s.get('seriesTitle')!r} episode={s.get('episode')!r}"
              f"({type(s.get('episode')).__name__})")
record("4. 系列字段正确", ok4, ev)

# ---------------- 5. ep01 家规「保护宝宝」 ----------------
ev, ok5 = [], True
ep1 = BASE.get("dangdang-ep01-zh")
if not ep1:
    ok5 = False
    ev.append("NG  ep01 缺失")
else:
    c = ep1["content"]
    idx3 = c[3] if len(c) > 3 else ""
    has_full = RULE_SENTENCE in idx3
    has_key = "还要一起保护好宝宝" in idx3
    ok5 &= has_full and has_key
    ev.append(f"{'OK ' if has_full else 'NG '} content[3] 含完整新家规原句: {has_full}")
    ev.append(f"{'OK ' if has_key else 'NG '} content[3] 含「还要一起保护好宝宝」: {has_key}")
    hits = []
    for name, p in list(STORIES.items()) + list(COLLECTIONS.items()):
        t = read(p)
        if OLD_TAIL in t:
            hits.append(f"{name}(x{t.count(OLD_TAIL)})")
    no_old = not hits
    ok5 &= no_old
    ev.append(f"{'OK ' if no_old else 'NG '} 旧结尾「{OLD_TAIL}」残留: "
              f"{'无' if no_old else hits}")
    ev.append(f"    ep01 结尾实际为: ...{c[-1][-30:]}")
record("5. ep01家规保护宝宝完好", ok5, ev)

# ---------------- 6. 无杂志名 ----------------
ev, ok6 = [], True
for eid in EP_IDS:
    s = BASE.get(eid, {})
    text = "".join(s.get("content", [])) + s.get("title", "") + \
        s.get("preview", "") + s.get("moral", "")
    hit = {w: text.count(w) for w in BANNED if w in text}
    if hit:
        ok6 = False
        ev.append(f"NG  {eid} 系列正文命中: {hit}")
for name, p in COLLECTIONS.items():
    t = read(p)
    hit = {w: t.count(w) for w in BANNED if w in t}
    if hit:
        ok6 = False
        ev.append(f"NG  {name} 命中: {hit}")
        for w in hit:
            for m in list(re.finditer(re.escape(w), t))[:3]:
                seg = t[max(0, m.start() - 45):m.start() + 45].replace("\n", " ")
                ev.append(f"      [{w}] ...{seg}...")
    else:
        ev.append(f"OK  {name}: 0 命中")
if all("系列正文命中" not in x for x in ev):
    ev.insert(0, "OK  6 集系列 content/title/preview/moral: 0 命中")
record("6. 无杂志名", ok6, ev)

# ---------------- 7. 弯引号合规 ----------------
ev, ok7 = [], True
for eid in EP_IDS:
    s = BASE.get(eid, {})
    for i, para in enumerate(s.get("content", [])):
        for ch in CURLY:
            if ch in para:
                ok7 = False
                pos = para.index(ch)
                ev.append(f"NG  {eid} content[{i}] 含 U+{ord(ch):04X}: "
                          f"...{para[max(0,pos-20):pos+20]}...")
if ok7:
    ev.append("OK  6 集 content 中未发现中文弯引号 U+201C / U+201D")
# 附加：三处 stories.json 全局弯引号统计（参考）
for name, p in STORIES.items():
    t = read(p)
    ev.append(f"    [参考] {name} 全库弯引号计数: "
              f"U+201C={t.count(CURLY[0])}, U+201D={t.count(CURLY[1])}")
record("7. 弯引号合规", ok7, ev)

# ---------------- 8. 胸口白毛设定 ----------------
ev, ok8 = [], True
for eid in ("dangdang-ep01-zh", "dangdang-ep06-zh"):
    s = BASE.get(eid, {})
    text = "".join(s.get("content", [])) + s.get("preview", "")
    chest = [m.group(0) for m in re.finditer(r"胸口[^，。；！？]{0,12}白毛", text)]
    tail_fur = [m.group(0) for m in re.finditer(r"尾巴尖[^，。；！？]{0,10}白毛", text)]
    good = bool(chest) and not tail_fur
    ok8 &= good
    ev.append(f"{'OK ' if good else 'NG '} {eid}: 胸口白毛表述={chest}, "
              f"尾巴尖白毛误写={tail_fur or '无'}")
# 全系列扫描白毛描述
allhits = []
for eid in EP_IDS:
    s = BASE.get(eid, {})
    for m in re.finditer(r"[^，。；！？]{0,10}白毛", "".join(s.get("content", []))):
        allhits.append(f"{eid}: {m.group(0)}")
ev.append("    全系列「白毛」描述: " + " | ".join(allhits))
record("8. 胸口白毛设定", ok8, ev)

# ---------------- 9. 教育点融入 ----------------
ev, ok9 = [], True
KEYS = ["听爸爸妈妈的话", "听爸爸的话", "爸爸妈妈的话", "家规", "保护宝宝",
        "保护好宝宝", "保护家人", "保护他的家人", "守护", "跟紧", "不跟陌生人走"]
for eid in EP_IDS:
    s = BASE.get(eid, {})
    moral = s.get("moral", "")
    content = "".join(s.get("content", []))
    mk = [k for k in KEYS if k in moral]
    ck = [k for k in KEYS if k in content]
    good = bool(mk or ck)
    ok9 &= good
    ev.append(f"{'OK ' if good else 'NG '} {eid} ep{s.get('episode')}: "
              f"moral命中={mk or '无'}; content命中={ck[:5] or '无'}")
record("9. 教育点融入", ok9, ev)

# ---------------- 10. 合集含新 5 集 ----------------
# 说明(QA Round2 修正): html 合集使用「第N集」标签, md 合集使用
# 「### 系列目录 + 1. [日期 — 标题]」编号目录约定, 二者均为合法表达。
# 原断言仅接受「第N集」字面量, 属测试用例缺陷, 现按文件类型分别断言。
ev, ok10 = [], True
EP_DATES = {2: "8月1日", 3: "8月8日", 4: "8月15日", 5: "8月22日", 6: "8月29日"}
for name, p in COLLECTIONS.items():
    t = read(p)
    miss = []
    is_md = name.endswith(".md")
    for n in range(2, 7):
        title = EP_TITLES[n]
        if title not in t:
            miss.append(f"第{n}集标题《{title}》")
            continue
        if is_md:
            # md 约定: 目录项「N. [日期 — 标题]」且存在正文小节「## 日期 — 标题」
            toc = re.search(rf"{n}\.\s*\[{EP_DATES[n]}\s*—\s*{re.escape(title)}\]", t)
            body = re.search(rf"##\s*{EP_DATES[n]}\s*—\s*{re.escape(title)}", t)
            if not toc:
                miss.append(f"第{n}集目录项")
            if not body:
                miss.append(f"第{n}集正文小节")
        else:
            if f"第{n}集" not in t:
                miss.append(f"第{n}集(标签)")
    if is_md:
        if "黑猫当当历险记（系列连载）" not in t:
            miss.append("系列区块标题")
        if "### 系列目录" not in t:
            miss.append("系列目录区块")
    good = not miss
    ok10 &= good
    conv = "md编号目录约定" if is_md else "html第N集约定"
    ev.append(f"{'OK ' if good else 'NG '} {name} [{conv}]: "
              f"{'第2~6集及标题齐全' if good else '缺失=' + str(miss)}")
    if good:
        if is_md:
            ev.append("      " + " / ".join(
                f"{n}.[{EP_DATES[n]} — {EP_TITLES[n]}]" for n in range(2, 7)))
        else:
            ev.append("      " + " / ".join(
                f"第{n}集《{EP_TITLES[n]}》" for n in range(2, 7)))
record("10. 合集含新5集", ok10, ev)

# ---------------- 11. 状态文件一致 ----------------
ev, ok11, sdata = [], True, {}
for name, p in STATES.items():
    if not os.path.exists(p):
        ok11 = False
        ev.append(f"NG  {name}: 文件不存在 ({p})")
        continue
    try:
        d = load_json(p)
        sdata[name] = d
        epi = d.get("episode", d.get("nextEpisode"))
        cont = d.get("continuity", d.get("continuityNotes", []))
        ncont = len(cont) if isinstance(cont, (list, dict)) else "N/A"
        arcs = d.get("arc", d.get("arcs", []))
        last_arc = ""
        if isinstance(arcs, list) and arcs:
            la = arcs[-1]
            last_arc = la if isinstance(la, str) else json.dumps(la, ensure_ascii=False)
        elif isinstance(arcs, str):
            last_arc = arcs
        c1 = epi == 7
        c2 = ncont == 6
        c3 = "守护宝宝" in json.dumps(d, ensure_ascii=False)
        good = c1 and c2 and c3
        ok11 &= good
        ev.append(f"{'OK ' if good else 'NG '} {name}: episode={epi}(需7) "
                  f"continuity={ncont}条(需6) 含「守护宝宝」={c3}")
        ev.append(f"      arc尾项: {last_arc[:80]}")
    except Exception as e:
        ok11 = False
        ev.append(f"NG  {name}: 解析失败 -> {e!r}")
if len(sdata) == 3:
    sn = list(sdata.keys())
    for o in sn[1:]:
        same = sdata[sn[0]] == sdata[o]
        ok11 &= same
        ev.append(f"{'OK ' if same else 'NG '} 状态文件比对 {sn[0]} vs {o}: "
                  f"{'一致' if same else '存在差异'}")
record("11. 状态文件一致", ok11, ev)

# ---------------- 输出 ----------------
print("=" * 78)
print("黑猫当当历险记 ep01~ep06 集成质量校验报告")
print("=" * 78)
for k in results:
    okv, lines = results[k]
    print(f"\n【{k}】 -> {'PASS' if okv else 'FAIL'}")
    for l in lines:
        print("   " + l)

print("\n" + "=" * 78)
print("汇总")
print("=" * 78)
for k in results:
    print(f"{'PASS' if results[k][0] else 'FAIL'}  {k}")
failed = [k for k in results if not results[k][0]]
print(f"\n总计 {len(results)} 项, 通过 {len(results)-len(failed)}, 失败 {len(failed)}")
if failed:
    print("失败项: " + ", ".join(failed))
