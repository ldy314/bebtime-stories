# -*- coding: utf-8 -*-
"""本地 AI 撰写 5 篇「题材多样化」胎教期故事并同步全部四个副本。
遵循：
- 胎教期材料库（常驻角色 + 场景/意象库 + 情感锚点 + 安全边界）
- 题材多样：颜色与画 / 声音与音乐 / 味道与温暖食物 / 动物朋友 / 四季与天气
- 硬约束：无蟹、未出生宝宝、无弯引号(用「」)、安全边界、妈妈的心跳固定高光
- 全部 prenatal（2026-08-10 < 预产期 2026-09-22）
"""
import io, json, os, re, datetime

def fmt_date(d):
    wd = ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'][d.weekday()]
    return f"{d.year}年{d.month}月{d.day}日 · {wd}"

def fmt_short(d):
    return f"{d.month:02d}/{d.day:02d}"

# 5 篇本地 AI 撰写故事（dateStr 统一 2026-08-10，用后缀区分同天多篇）
NEW_RAW = [
    {
        "dateStr": "2026-08-10", "language": "zh",
        "title": "「小小画家的星星调色盘」（胎教期）",
        "preview": "暖暖在彩色蜡笔山坡上捡到一个小调色盘，她想把夜晚画得暖暖的。",
        "moral": "每一种颜色都是一种温柔；而妈妈的心跳，是夜里最暖的那一笔。",
        "content": [
            "傍晚，小星星·暖暖提着小小的灯笼，慢慢飘到彩色蜡笔山坡。山坡上的草尖沾着夕阳剩下的橘色，风一吹，像有人在轻轻涂颜色。暖暖低头，忽然看见泥地里躺着一个巴掌大的小调色盘，里面盛着金、粉、蓝、绿四种温柔的颜料。",
            "暖暖用手指蘸了一点金色，在夜空的画布上轻轻一抹——星星们亮了起来，像撒了一把会发光的小糖。她又蘸了粉色，把云朵涂成软软的棉花糖；蘸了蓝色，把远处的小河染成安静的梦。山坡上的小花们都仰起脸，等着属于自己的颜色。",
            "这时，一阵细细的「咚、咚、咚」从很远的地方传来，像画布背面有人在轻轻敲。暖暖把耳朵贴在夜空上，听见那是妈妈的心跳——平稳、温暖，一下一下，像在给这幅画打拍子。原来，所有的颜色加起来，都比不上这一声心跳让人安心。",
            "暖暖忽然明白了：妈妈的心跳，就是夜里最暖的那一笔颜色。它不在调色盘里，却把整个世界都涂得软软的、香香的。她把剩下的绿色轻轻点在自己的小灯笼上，让光也带一点草地的味道。",
            "宝宝，你也在妈妈肚子里，听着这一声「咚、咚、咚」慢慢长大呀。等你会画画的那一天，记得先给妈妈画一颗小小的、暖暖的心。晚安，小画家；晚安，小宝宝。",
        ],
    },
    {
        "dateStr": "2026-08-10", "language": "en",
        "title": "The Little Bird Who Learned a Lullaby (Prenatal)",
        "preview": "Jiujiu the little bird wanted to sing the softest song, until the wind taught him a secret.",
        "moral": "The gentlest sound in the world is a mother's heartbeat, keeping time for every lullaby.",
        "content": [
            "High on a soft cloud-meadow, a small bird named Jiujiu practiced his songs. He could tweet bright and loud, but tonight he wanted to sing something softer — a song to help a sleepy little one far below. He flapped to the old Wind and asked, \"Wind, how do I sing a lullaby?\"",
            "The Wind smiled and spun slowly around him. \"Listen,\" the Wind whispered. \"The trees whisper, the brook babbles, the stars hum their quiet tune. Mix a little of each, and you have music.\" Jiujiu listened: the leaves went sh-sh-sh, the brook went bub-bub, the stars went mmm-mmm. He tried, and a gentle melody floated into the night.",
            "Then, from deep inside the sleeping world, came a sound so soft he almost missed it: a steady \"lum... lum... lum.\" Jiujiu pressed his feathery cheek to the cloud and heard it clearly — a mother's heartbeat, calm and warm, keeping time beneath everything. It was the quiet drum that all lullabies leaned on.",
            "Jiujiu understood. No tweet, no whisper, no hum was as gentle as that heartbeat. So he shaped his song around it, letting the \"lum... lum... lum\" be the calm center, and his own soft \"jiu... jiu...\" float like a blanket on top. The little one below wriggled happily, lulled by both.",
            "And you, small sleeper in your mama's warm tide, are already hearing that same drum. One day Jiujiu will sing for you too. Good night, little bird; good night, small one.",
        ],
    },
    {
        "dateStr": "2026-08-10", "language": "zh",
        "title": "「云朵厨房的甜味信封」（胎教期）",
        "preview": "朵朵在暖暖厨房窗台烤了一块会发光的云朵小饼干，香香的味道飘向了远方。",
        "moral": "厨房里甜甜的味道，是爱慢慢烤出来的；妈妈的心跳，就是那炉火轻轻的呼吸。",
        "content": [
            "云朵精灵·朵朵推开暖暖厨房的窗，把一小团白云放进小烤箱。她撒进月光粉、星星糖，还有一勺「等一等就会甜」的耐心。烤箱呼呼地唱起歌，热气像软软的围巾，绕着朵朵转了一圈又一圈。",
            "不一会儿，一块小小的云朵饼干烤好了，浑身透着暖黄色的光，香香的味道顺着窗缝飘了出去，飘过海草森林，飘过月光海面，一直飘到很远很远的地方。朵朵把饼干装进一个画着小太阳的信封，贴上「给正在长大的你」的标签。",
            "忽然，信封轻轻跳了一下——里面传出了「咚、咚、咚」的声音。朵朵把耳朵贴上去，笑了：那是妈妈的心跳呀，原来这甜甜的味道，一直都连着妈妈肚子里那炉小小的火。每一口香气，都是妈妈在轻轻说「我在呢」。",
            "朵朵明白了：厨房里暖暖的味道，不是凭空来的，是爱一点一点烤出来的；而妈妈的心跳，就是那炉火轻轻的呼吸，不急不慢，永远都在。她把信封轻轻放在宝宝的梦里，让香味陪着他慢慢长大。",
            "宝宝，等你来到这个世界，闻到厨房里甜甜的香气时，就想一想今天这块云朵小饼干吧。晚安，朵朵；晚安，小宝宝。",
        ],
    },
    {
        "dateStr": "2026-08-10", "language": "en",
        "title": "The Sleepy Rabbit and the Moonlight Letter (Prenatal)",
        "preview": "An'an the little bear met a timid rabbit, and together they read a letter written in moonlight.",
        "moral": "A friend's warm paw, and a mother's steady heartbeat, are two ways the world says \"you are safe.\"",
        "content": [
            "In Mama's quiet garden, Little Bear An'an was fluffing his soft pillow when a tiny rabbit peeped from behind the roses. The rabbit's ears trembled. \"I can't sleep,\" she whispered. \"The night feels too big.\" An'an patted the ground beside him. \"Sit with me. We'll read the moonlight letter together.\"",
            "The moon had spilled silver light across a broad leaf, and on it were gentle shapes: a hill, a stream, a small curled-up cub. \"That's you, learning the world,\" An'an said. The rabbit traced the shapes with a shy paw. \"And that,\" An'an pointed, \"is the whole garden, keeping us warm.\" The big night suddenly felt like a cozy room.",
            "From somewhere deep and close came a calm \"thump-thump, thump-thump.\" The rabbit stilled. \"What is that?\" she breathed. An'an smiled. \"That is a mother's heartbeat — the safest drum in the world. It says: you are held, even when the night is big.\" The rabbit laid a paw on her own chest and felt her own small heartbeat answer it.",
            "They stayed like that, two small friends under one moon, the letter of light unfolded between them. The rabbit's ears stopped trembling. \"I think I can sleep now,\" she yawned. An'an tucked the leaf like a blanket over them both.",
            "And you, little one growing in your mama's tide, have that same drum beneath you. When the world feels big, remember: a friend's warm paw, and a mother's steady heartbeat, are two ways the world says you are safe. Good night, small friends; good night, small one.",
        ],
    },
    {
        "dateStr": "2026-08-10", "language": "zh",
        "title": "「小雨滴的四季旅行」（胎教期）",
        "preview": "露露骑着一滴小雨，从春天出发，经过了夏、秋、冬，最后听见了最安稳的鼓声。",
        "moral": "四季会轮流转，可妈妈的心跳一直都在，像雨的节奏，陪着你慢慢长大。",
        "content": [
            "露珠邮递员·露露接到了一封信，要送给「正在长大的小宝宝」。她跳上一滴亮晶晶的小雨，从绵绵小雨花园出发了。第一站是春天：小雨落在嫩芽上，芽芽伸了个懒腰，说「再等等，就快了」。",
            "小雨飘呀飘，到了夏天。荷叶撑起绿伞，青蛙打起小鼓，热乎乎的风里全是青草的味道。露露把信贴在胸口，怕它被太阳晒皱。又飘到秋天：果子红了，叶子金了，风变得轻轻的、凉凉的，像一条软毯子裹住大地。",
            "最后是冬天。小雨变成了小雪花，安安静静地落。世界白白的、暖暖的（因为雪把声音都抱住了）。露露有点累，把耳朵贴在小雪花上——却听见「咚、咚、咚」，一下一下，从很远很近的地方传来。",
            "那是妈妈的心跳呀。原来不管春天、夏天、秋天还是冬天，这声音一直都在，像雨的节奏，不快不慢，陪着肚里的小宝宝慢慢长大。露露忽然不累了：信不用急着送，因为收信的人，正被这声音稳稳地抱着。",
            "宝宝，四季会一轮一轮地转，你也会一天一天地长。可妈妈的心跳，永远是你最安稳的鼓声。晚安，露露；晚安，小宝宝。",
        ],
    },
]

# 显式 id：避开远端已自动生成的 2026-08-10-cn/en（每日故事），
# 5 篇统一作为同日多篇的扩展 id，自然且不冲突。
EXPLICIT_IDS = [
    "2026-08-10-cn-2",
    "2026-08-10-en-2",
    "2026-08-10-cn-3",
    "2026-08-10-en-3",
    "2026-08-10-cn-4",
]

def build_story(raw, sid):
    d = datetime.date.fromisoformat(raw["dateStr"])
    lang = raw["language"]
    return {
        "id": sid,
        "date": fmt_date(d),
        "dateShort": fmt_short(d),
        "title": raw["title"],
        "language": lang,
        "ageGroup": "prenatal",
        "ageLabel": "胎教期",
        "preview": raw["preview"],
        "moral": raw["moral"],
        "content": raw["content"],
    }

assert len(NEW_RAW) == len(EXPLICIT_IDS), "raw/id 数量不一致"
NEW = [build_story(r, sid) for r, sid in zip(NEW_RAW, EXPLICIT_IDS)]

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
    idxp = os.path.join(loc, 'index.html')
    if os.path.isfile(idxp):
        html = io.open(idxp, encoding='utf-8').read()
        new_line = 'const EMBEDDED_STORIES = ' + json.dumps(stories, ensure_ascii=False, separators=(',', ':')) + ';'
        if EMB_RE.search(html):
            html = EMB_RE.sub(new_line, html, count=1)
            io.open(idxp, 'w', encoding='utf-8').write(html)
        else:
            print("  WARN: EMBEDDED_STORIES not found in", idxp)
    print(f"  {loc}: +{added} 篇，总计 {len(stories)} 篇")
print("DONE")
