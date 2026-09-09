# -*- coding: utf-8 -*-
"""在 D 开发副本上扩充胎教期题材多样性：
1) 扩展 PRENATAL_SCENES / PRENATAL_IMAGERY
2) 新增 PRENATAL_THEME_FLAVORS + pickPrenatalFlavor + rotateList
3) buildPrenatalBlock 按日期确定性选色调 + 轮换场景/意象子集
4) CONCRETE_SEEDS 追加多样选题（不破坏 6 切片分组）
保留所有硬约束（无蟹/未出生/无弯引号/安全边界）。
"""
import io

PB = r"D:\code test\睡前故事\scripts\prompt-builder.js"

with io.open(PB, encoding='utf-8') as f:
    lines = f.read().split('\n')

# ---- 1) 替换场景/意象 4 行 + 追加 FLAVORS ----
new_block = """const PRENATAL_SCENES = ['海草森林', '月光海面', '云端棉田', '妈妈的花园', '星夜天台', '暖暖被窝', '清晨的花瓣露台', '暖暖的厨房窗台', '雨后的小院', '麦浪里的石磨', '雪地小木屋', '森林溪边', '图书馆角落', '风铃走廊'];
const PRENATAL_SCENES_EN = ['seagrass forest', 'moonlit sea', 'cloud cotton field', 'Mama’s garden', 'starry rooftop', 'cozy bed', 'dawn petal terrace', 'warm kitchen windowsill', 'courtyard after rain', 'stone mill in the wheat field', 'snowy cabin', 'forest streamside', 'library corner', 'wind-chime corridor'];
const PRENATAL_IMAGERY = ['星星灯笼', '心跳小鼓', '梦的种子', '云朵口袋', '月光小船', '风的信笺', '彩虹小桥', '会发芽的雨滴', '会唱歌的鹅卵石', '面包的香气云', '小脚印地图', '温暖的毛线团'];
const PRENATAL_IMAGERY_EN = ['star lantern', 'heartbeat drum', 'dream seed', 'cloud pocket', 'moonlight boat', 'wind’s letter', 'rainbow bridge', 'a sprouting raindrop', 'the singing pebble', 'the aroma cloud of bread', 'little-footprint map', 'a warm ball of yarn'];

// ===== 胎教期「题材色调」轮换（让每日题材更多样，避免雷同） =====
// 不替代常驻角色/情感锚点/安全边界，只是给本篇一个可侧重展开的题材方向。
const PRENATAL_THEME_FLAVORS_CN = [
  '声音与音乐：让故事充满温柔的声音——妈妈哼的歌、风铃轻响、小乐器叮咚、雨打叶片的节奏，用声音编织安全感。',
  '颜色与画：用颜色讲故事——晚霞的橘、麦田的金、海的蓝，主角收集颜色做成给宝宝的礼物。',
  '味道与温暖食物：温柔的食物气息——粥的甜香、苹果的脆、桂花的清甜，用味道传递爱意（绝不涉及螃蟹/大闸蟹）。',
  '四季与天气：讲讲温柔的天气——春天的第一场细雨、夏夜的萤火、冬日的暖阳、秋风里打转的叶子。',
  '动物朋友：主角遇见温柔的小动物——慢吞吞的小乌龟、爱打盹的猫、会唱歌的青蛙、绒毛蓬松的小羊。',
  '小手小脚与身体：用身体感受世界——小脚丫踩在软软的地上、小手摸光滑温润的石头、舒舒服服打个哈欠。',
  '家里的温暖物件：会发光的夜灯、软软的毛毯、滴答走的钟、窗台上的小盆栽，平凡物件里藏着爱。',
  '光的游戏：光与影的温柔游戏——晨光、烛光、透过树叶洒下的光斑、墙上跳舞的小影子。',
  '小小远行：一次轻轻的远行——顺着小溪飘、掠过金色田野、翻过温柔的小山，去看柔软的风景。',
  '梦与想象：轻轻的想象——云朵变成小羊、星星排成笑脸、风把小小的愿望寄向远方。'
];
const PRENATAL_THEME_FLAVORS_EN = [
  'Sound & music: fill the story with gentle sounds — mommy’s humming, a soft wind-chime, little instruments going ding, the rhythm of rain on leaves; weave safety through sound.',
  'Colour & painting: tell the story with colour — the orange of dusk, the gold of wheat fields, the blue of the sea; the protagonist gathers colours into a gift for the baby.',
  'Taste & warm food: tender food scents — the sweetness of congee, the crunch of an apple, the light fragrance of osmanthus; pass love through taste (never crabs / hairy crabs).',
  'Seasons & weather: gentle weather — the first spring drizzle, summer-night fireflies, winter’s warm sun, an autumn leaf spinning in the wind.',
  'Animal friends: the protagonist meets gentle little animals — a slow little turtle, a napping cat, a singing frog, a fluffy little lamb.',
  'Little hands, little feet, the body: feel the world with the body — tiny feet on soft ground, a small hand on a smooth warm stone, a comfy yawn.',
  'Cosy household objects: a glowing night-light, a soft blanket, a ticking clock, a little potted plant on the windowsill — love hidden in ordinary things.',
  'Play of light: a gentle game of light and shadow — morning light, candlelight, dappled light through leaves, a little shadow dancing on the wall.',
  'A tiny journey: a soft little trip — drift along the stream, skim the golden fields, over a gentle hill, to see soft scenery.',
  'Dreams & imagination: a light imagination — clouds turning into little sheep, stars arranging into a smiling face, the wind mailing a tiny wish far away.'
];

function pickPrenatalFlavor(dateStr, lang) {
  const pool = lang === 'zh' ? PRENATAL_THEME_FLAVORS_CN : PRENATAL_THEME_FLAVORS_EN;
  const idx = hashDate(dateStr + '-flav-' + lang) % pool.length;
  return pool[idx];
}

// 确定性轮换取 n 个元素的子集（不重复、按日期变化）
function rotateList(arr, key, n) {
  const start = hashDate(key) % arr.length;
  const out = [];
  for (let i = 0; i < n && i < arr.length; i++) out.push(arr[(start + i) % arr.length]);
  return out;
}"""

start = None
for i, ln in enumerate(lines):
    if ln.startswith('const PRENATAL_SCENES = ['):
        start = i
        break
if start is None:
    raise SystemExit('[FAIL] cannot find PRENATAL_SCENES start')
# 4 行：PRENATAL_SCENES, _EN, PRENATAL_IMAGERY, _IMAGERY_EN
end = start + 4
lines[start:end] = new_block.split('\n')

# ---- 2) buildPrenatalBlock CN 分支 ----
s = '\n'.join(lines)
old_cn = """    const scenes = PRENATAL_SCENES.join('、');
    const imagery = PRENATAL_IMAGERY.join('、');
    const anchors = EMOTIONAL_ANCHORS.map((a, i) => (i + 1) + '. ' + a).join('  ');
    const safety = PRENATAL_SAFETY.join(' ');"""
new_cn = """    const flavor = pickPrenatalFlavor(dateStr, 'zh');
    const scenes = rotateList(PRENATAL_SCENES, dateStr + '-scn-zh', 3).join('、');
    const imagery = rotateList(PRENATAL_IMAGERY, dateStr + '-img-zh', 3).join('、');
    const anchors = EMOTIONAL_ANCHORS.map((a, i) => (i + 1) + '. ' + a).join('  ');
    const safety = PRENATAL_SAFETY.join(' ');"""
if s.count(old_cn) != 1:
    raise SystemExit('[FAIL] CN branch replace count=%d' % s.count(old_cn))
s = s.replace(old_cn, new_cn, 1)

old_cn_text = "常驻材料库（可顺带出现，让世界更连贯）：场景如 ${scenes}；意象如 ${imagery}。已有故事的主人公就是最珍贵的素材，可在不同故事里让它们偶尔相遇。"
new_cn_text = old_cn_text + "\n本篇题材色调（任选其一或自然融合，避免每天题材雷同）：\n${flavor}"
if s.count(old_cn_text) != 1:
    raise SystemExit('[FAIL] CN text replace count=%d' % s.count(old_cn_text))
s = s.replace(old_cn_text, new_cn_text, 1)

# ---- 3) buildPrenatalBlock EN 分支 ----
old_en = """  const scenes = PRENATAL_SCENES_EN.join(', ');
  const imagery = PRENATAL_IMAGERY_EN.join(', ');
  const anchors = EMOTIONAL_ANCHORS_EN.map((a, i) => (i + 1) + '. ' + a).join('  ');
  const safety = PRENATAL_SAFETY_EN.join(' ');"""
new_en = """  const flavor = pickPrenatalFlavor(dateStr, 'en');
  const scenes = rotateList(PRENATAL_SCENES_EN, dateStr + '-scn-en', 3).join(', ');
  const imagery = rotateList(PRENATAL_IMAGERY_EN, dateStr + '-img-en', 3).join(', ');
  const anchors = EMOTIONAL_ANCHORS_EN.map((a, i) => (i + 1) + '. ' + a).join('  ');
  const safety = PRENATAL_SAFETY_EN.join(' ');"""
if s.count(old_en) != 1:
    raise SystemExit('[FAIL] EN branch replace count=%d' % s.count(old_en))
s = s.replace(old_en, new_en, 1)

old_en_text = "Resident material library (may appear alongside, to make the world coherent): scenes like ${scenes}; imagery like ${imagery}. Past story protagonists are precious material — let them occasionally meet across stories."
new_en_text = old_en_text + "\nSubject tone for this story (pick one or blend naturally, to avoid repetitive themes day after day):\n${flavor}"
if s.count(old_en_text) != 1:
    raise SystemExit('[FAIL] EN text replace count=%d' % s.count(old_en_text))
s = s.replace(old_en_text, new_en_text, 1)

lines = s.split('\n')

# ---- 4) CONCRETE_SEEDS_CN 追加多样选题（在 帮妈妈捶背 行之后、其 ]; 之前） ----
extra_cn = [
  '暖暖厨房里的小麦香', '桂花糕的第一缕甜', '会唱歌的瓷碗', '调色盘上的旅行', '蜡笔画出的彩虹路',
  '风铃写给宝宝的信', '小火车开往云朵站', '会发光的路灯叔叔', '外婆的针线筐里住着春天', '小雨靴踩出的水花歌',
  '会跳舞的影子朋友', '暖水袋里的小太阳', '图书馆角落的瞌睡猫', '会算术的饼干', '望远镜里的小星球',
  '摇篮曲里的星星船', '会讲故事的旧藤椅', '窗台上的多肉小队'
]
extra_en = [
  'A little wheat aroma in the warm kitchen', 'the first sweetness of osmanthus cake', 'the singing porcelain bowl',
  'a journey on the palette', 'the rainbow road drawn in crayon', 'the wind-chime’s letter to the baby',
  'the little train to Cloud Station', 'the glowing streetlamp uncle', 'spring living in Grandma’s sewing basket',
  'the water-splash song of little rain boots', 'the dancing shadow friend', 'a tiny sun in the warm water bottle',
  'the dozing cat in the library corner', 'the arithmetic biscuit', 'a little planet in the telescope',
  'the starry boat in the lullaby', 'the old rattan chair that tells stories', 'the succulent squad on the windowsill'
]
def append_seeds(lines, marker, extra):
    for i, ln in enumerate(lines):
        if marker in ln:
            # 确保标记行以逗号结尾（上一行可能无逗号）
            if not lines[i].rstrip().endswith(','):
                lines[i] = lines[i].rstrip() + ','
            # 下一行应为 ]; （该数组的结束）
            j = i + 1
            while j < len(lines) and lines[j].strip() != '];':
                j += 1
            if j >= len(lines):
                raise SystemExit('[FAIL] no ]; after ' + marker)
            indent = '  '
            new_seeds = ',\n'.join(indent + "'" + x + "'" for x in extra)
            lines.insert(j, new_seeds)
            return
    raise SystemExit('[FAIL] marker not found: ' + marker)

append_seeds(lines, '帮妈妈捶背', extra_cn)
# EN 数组结束标志： 'Rubbing Mom’s back' 行
append_seeds(lines, 'Rubbing Mom', extra_en)

with io.open(PB, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print('[OK] diversity edits applied to', PB)
print('  PRENATAL_SCENES lines expanded + FLAVORS + rotateList added')
print('  buildPrenatalBlock CN/EN use flavor + rotated scenes/imagery')
print('  CONCRETE_SEEDS appended', len(extra_cn), 'CN +', len(extra_en), 'EN diverse seeds')
