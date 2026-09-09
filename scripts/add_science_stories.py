# -*- coding: utf-8 -*-
"""追加 4 篇科学故事（08-09 / 08-10 的 cn+en），并同步到全部四个副本。
科学故事严格按 prompt-builder 的科学模板撰写：
- 来源锁定 SCIENCE_FEEDS（中文=博物/环球科学，英文=Scientific American）
- 含儿童可理解的科学讲解 + moral=科学事实小结
- 胎教期安全：未出生宝宝、无蟹、无弯引号
"""
import io, json, os, re, datetime

ROOT = r"D:/code test/睡前故事/scripts"

def fmt_date(d):
    wd = ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'][d.weekday()]
    return f"{d.year}年{d.month}月{d.day}日 · {wd}"

def fmt_short(d):
    return f"{d.month:02d}/{d.day:02d}"

# 4 篇新科学故事（dateStr -> 计算 date/dateShort）
NEW_RAW = [
    {
        "dateStr": "2026-08-09", "language": "zh", "title": "🔬科学故事（胎教期）：萤火虫提着的小灯笼",
        "source": "博物",
        "preview": "夏夜的草地上，忽然亮起一盏又一盏绿色的小灯笼，一闪，一闪。那是萤火虫，在用光轻轻说话。",
        "moral": "萤火虫用身体里的荧光素和荧光酶，在氧气帮助下发出几乎不发热的「冷光」，用来在夜里寻找同伴；光，也可以是一种温柔的语言。",
        "content": [
            "夏天的夜晚，草地上忽然亮起一盏又一盏小小的绿灯笼，一闪，又一闪。它们不是童话里的小灯，而是一只只萤火虫——一种会飞的小甲虫。萤火虫的尾巴上，藏着一间小小的「发光工厂」。",
            "这间工厂用的材料，藏在萤火虫的身体里：一种叫「荧光素」的小东西，还有一种叫「荧光酶」的帮忙小工。当荧光素遇到空气里的氧气，荧光酶就帮它们轻轻一合，光就亮起来了。最奇妙的是，这种光几乎不烫手——它叫「冷光」，大部分都变成了温柔的光，只有一点点变成了热。",
            "萤火虫为什么要提着小灯笼呢？宝宝在妈妈肚子里也可以想一想：它们是想找朋友呀。雄萤火虫一闪一闪，像在说「我在这里」；雌萤火虫看见喜欢的，也回一闪，像在说「我也在这里」。它们用光悄悄聊天，在黑黑的夜里找到彼此。",
            "科学家叔叔阿姨们还发现，不同的萤火虫，闪灯的节奏不一样，有的快，有的慢，就像每个人说话的语调不同。靠着这小小的光，它们认出了自己的伙伴。原来，光也可以是一种温柔的语言。",
            "所以呀，宝宝，等你以后在夏夜的草地上看到一闪一闪的绿灯笼，你就知道：那是萤火虫在点灯，在用只有它们懂的语言，轻轻地说着「你好呀」。而你，也像一盏小小的灯，正被爸爸妈妈的爱，温柔地点亮着。"
        ],
    },
    {
        "dateStr": "2026-08-09", "language": "en", "title": "🔬 Science Story (Prenatal): Why the Sky Wears a Blue Coat",
        "source": "Scientific American",
        "preview": "The sky is not painted. It is lit from inside by tiny sun-beams playing a gentle game with the air.",
        "moral": "Sunlight is made of many colors; the tiny blue pieces scatter most in the air, so the daytime sky looks blue. Light, gently scattered, paints the world we see.",
        "content": [
            "Look up, little one, at the big soft sky. On a clear day it wears a coat of gentle blue. But the sky is not painted, and the air has no color of its own. So where does the blue come from?",
            "It comes from the sun, and from a quiet game the sunbeams play with the air. Sunlight looks white, but it is really made of many colors together — red, orange, yellow, green, blue, and violet, like a hidden rainbow. When sunlight reaches the air, it meets countless tiny invisible bits floating inside it.",
            "Here is the secret: the little blue and violet pieces of light are small and bouncy, so they bump into those tiny bits and scatter, spreading out in every direction, like soft sparks filling the whole sky. The bigger red and yellow pieces sail straight through, hardly bothered at all. So when we look up, our eyes meet mostly the scattered blue, and the sky looks blue.",
            "Why not violet, which scatters even more? Our eyes are not very good at seeing violet, and a little of the sun's violet light is absorbed high above. So blue wins, and paints the daytime for us.",
            "And when the sun sinks low, its light must travel through more air; the blue gets scattered away, and the warm reds and oranges slip through to say good evening. So the sky blushes at sunset. You, small sleeper, are wrapped in the very same light that colors the sky — quiet, vast, and kind."
        ],
    },
    {
        "dateStr": "2026-08-10", "language": "zh", "title": "🔬科学故事（胎教期）：星星为什么眨眼睛",
        "source": "环球科学",
        "preview": "夜空里，小星星一闪一闪，像在对宝宝眨眼睛。其实，那是它们在和地球的大气层玩捉迷藏。",
        "moral": "星星本身不眨眼；它们遥远的光穿过地球冷暖厚薄不一的大气层时被轻轻折射，忽明忽暗，看起来就像在眨眼睛。",
        "content": [
            "宝宝，等你将来来到这个世界，在某个安静的夜晚抬起头看夜空，会发现小星星一闪一闪的，像在对你眨眼睛。可是星星并不会真的眨眼——它们是远远的、安安静静发光的小太阳。那为什么看上去在闪呢？",
            "秘密藏在地球外面那层看不见的「被子」里。这床被子叫大气层，是由一层又一层的空气组成的。空气有时候暖，有时候凉；有时候厚，有时候薄。星星的光，要穿过这床摇摇晃晃的被子，才能来到宝宝的眼睛里。",
            "当星光穿过不同温度、不同厚薄的空气时，会像小皮球一样被轻轻拐弯——一会儿偏左，一会儿偏右。于是，到达我们眼睛的光，就一会儿多、一会儿少，星星看上去便一闪一闪，像在调皮地眨眼睛。",
            "离地平线越近的星星，要穿过的空气被子越厚，闪得也就越厉害。而头顶正上方的星星，穿过的空气薄一些，就闪得温柔一点。天文学家爷爷观察星星时，常常把望远镜架在高高的山顶，或者放进太空里，好让星光少穿一点「被子」，看得更清楚。",
            "所以呀，宝宝，星星眨眼睛，不是因为它们困了，而是地球的大气层在轻轻地跟光做游戏。等你来到这个世界，某个安静的夜晚，也可以和爸爸妈妈一起，数一数天上那些调皮眨眼的小星星。"
        ],
    },
    {
        "dateStr": "2026-08-10", "language": "en", "title": "🔬 Science Story (Prenatal): How a Tiny Seed Knows When to Wake",
        "source": "Scientific American",
        "preview": "A seed can wait for years in the dark, quiet as a stone — until one warm, wet morning tells it: now is the time.",
        "moral": "A seed waits in the dark until water and warmth wake it; its root grows down with gravity while its shoot reaches up to the light — a quiet plan held before it ever sees the sun.",
        "content": [
            "Deep under the soil, a tiny seed rests. It looks like nothing at all — a speck, a crumb, a sleepy little stone. But inside, it holds a whole secret: the plan to become a plant. The question is, how does it know when to wake?",
            "A seed is patient. It can wait through cold winters and dry summers, sometimes for many years, doing almost nothing. It waits for two gentle signals: water and warmth. When rain soaks the soil and the earth grows warm, the seed drinks, swells, and stirs — like a child stretching after a long nap.",
            "Then a small root tip peeks downward, looking for water and hold. The root knows to go down because of gravity, the quiet pull of the Earth. A tiny green shoot pushes upward instead, reaching for the light. Up and down — the little seed already knows the way, though it has never seen the sun.",
            "Later, in the green leaves, the plant will do a quiet magic called photosynthesis: it catches sunlight, drinks water from the soil, and breathes a gas from the air, turning them all into sweet food for itself. But all of that begins with one brave push toward the light.",
            "And you, small one, are a little like that seed. Right now you wait, warm and safe, gathering everything you need. One day you will push gently toward the light too — and the whole world will be glad to meet you."
        ],
    },
]

def build_story(raw):
    d = datetime.date.fromisoformat(raw["dateStr"])
    lang = raw["language"]
    suffix = "cn" if lang == "zh" else "en"
    return {
        "id": f"{raw['dateStr']}-science-{suffix}",
        "date": fmt_date(d),
        "dateShort": fmt_short(d),
        "title": raw["title"],
        "language": lang,
        "ageGroup": "prenatal",
        "ageLabel": "胎教期",
        "preview": raw["preview"],
        "moral": raw["moral"],
        "content": raw["content"],
        "category": "science",
        "source": raw["source"],
        "series": "science",
        "seriesTitle": "科学故事",
    }

NEW = [build_story(r) for r in NEW_RAW]

LOCS = [
    r"C:/Users/Administrator/WorkBuddy/Claw/github-bedtime-stories",
    r"C:/Users/Administrator/WorkBuddy/Claw/bedtime-story-app",
    r"D:/code test/睡前故事",
    r"D:/code test/睡前故事/github-pages",
]

EMB_RE = re.compile(r'const EMBEDDED_STORIES = \[.*?\];', re.S)

for loc in LOCS:
    sp = os.path.join(loc, 'stories.json')
    if not os.path.isfile(sp):
        print("SKIP (no stories.json):", loc); continue
    stories = json.load(io.open(sp, encoding='utf-8'))
    existing = {s.get('id') for s in stories}
    added = 0
    for nw in NEW:
        if nw['id'] in existing:
            print("  DUP skip:", nw['id']); continue
        stories.append(nw); added += 1; existing.add(nw['id'])
    json.dump(stories, io.open(sp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    # 更新 index.html 的 EMBEDDED_STORIES（保持单行）
    idxp = os.path.join(loc, 'index.html')
    if os.path.isfile(idxp):
        html = io.open(idxp, encoding='utf-8').read()
        new_line = 'const EMBEDDED_STORIES = ' + json.dumps(stories, ensure_ascii=False, separators=(',', ':')) + ';'
        if EMB_RE.search(html):
            html = EMB_RE.sub(new_line, html, count=1)
            io.open(idxp, 'w', encoding='utf-8').write(html)
        else:
            print("  WARN: EMBEDDED_STORIES not found in", idxp)
    print(f"  {loc}: +{added} 篇科学故事，总计 {len(stories)} 篇")
print("DONE")
