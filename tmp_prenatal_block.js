// ===== 胎教期「故事孕育师」增强（参照 deepseek 故事生成思路优化指南.md） =====
// 与「黑猫当当」系列素材库完全分开（黑猫当当是独立周更系列，不混入每日胎教故事）。
// 仅作用于 prenatal 阶段（2026-09-22 之前）；不改动日期主题轮换、不引入蟹类、不把宝宝写成已出生、不用弯引号。
const PRENATAL_CAST = [
  { name: '小海螺·小旋旋', en: 'Little Conch Xuanxuan', type: '白海螺', enType: 'white conch', home: '深海海草森林', enHome: 'deep-sea seagrass forest', personality: '安静、温柔、充满好奇', enPersonality: 'quiet, gentle, full of curiosity', catchphrase: '原来是这样呀……', enCatchphrase: 'So that is how it is...' },
  { name: '月亮妈妈', en: 'Moon Mama', type: '守护者', enType: 'guardian', home: '夜空', enHome: 'the night sky', personality: '温柔、守护、充满智慧', enPersonality: 'gentle, protective, full of wisdom', catchphrase: '安心睡吧，妈妈在呢。', enCatchphrase: 'Sleep safe, Mama is here.' },
  { name: '小星星·暖暖', en: 'Little Star Nuannuan', type: '暖黄小星星', enType: 'warm-yellow little star', home: '夜空', enHome: 'the night sky', personality: '圆滚滚、爱眨眼睛、爱陪伴', enPersonality: 'round, blinking, loves to keep company', catchphrase: '我陪着你呀。', enCatchphrase: 'I am right here with you.' },
  { name: '小熊·安安', en: 'Little Bear An’an', type: '小棕熊', enType: 'little brown bear', home: '森林树洞', enHome: 'a forest hollow', personality: '软软的、慢吞吞、有安全感', enPersonality: 'soft, slow, reassuring', catchphrase: '呼……噜……', enCatchphrase: 'huff... lu...' },
  { name: '露珠邮递员·露露', en: 'Dew Postman Lulu', type: '小露珠', enType: 'little dewdrop', home: '清晨花瓣', enHome: 'a petal at dawn', personality: '活泼、爱问问题', enPersonality: 'lively, full of questions', catchphrase: '有信来啦！', enCatchphrase: 'A letter’s here!' },
  { name: '云朵精灵·朵朵', en: 'Cloud Spirit Duoduo', type: '云端小精灵', enType: 'little cloud spirit', home: '云端棉田', enHome: 'the cloud cotton field', personality: '轻盈、爱照顾人', enPersonality: 'light, caring', catchphrase: '飘呀飘，到家啦。', enCatchphrase: 'Float, float, home at last.' },
  { name: '小种子·芽芽', en: 'Little Seed Yaya', type: '小种子', enType: 'little seed', home: '妈妈的花园', enHome: 'Mama’s garden', personality: '耐心、满怀希望', enPersonality: 'patient, hopeful', catchphrase: '再等等，就快了。', enCatchphrase: 'Just a little longer.' },
  { name: '小鸟·啾啾', en: 'Bird Jiujiu', type: '小鸟', enType: 'little bird', home: '屋檐', enHome: 'the eaves', personality: '会唱摇篮曲、温柔', enPersonality: 'sings lullabies, gentle', catchphrase: '啾啾，睡吧。', enCatchphrase: 'tweet, tweet, sleep now.' },
  { name: '小闹钟·叮当', en: 'Little Alarm Dingdang', type: '小闹钟', enType: 'little alarm clock', home: '窗台', enHome: 'the windowsill', personality: '爱学唱歌、准时不闹', enPersonality: 'loves to sing, gentle with time', catchphrase: '叮咚，该睡啦。', enCatchphrase: 'ding-dong, time to sleep.' }
];

const PRENATAL_SCENES = ['海草森林', '月光海面', '云端棉田', '妈妈的花园', '星夜天台', '暖暖被窝'];
const PRENATAL_SCENES_EN = ['seagrass forest', 'moonlit sea', 'cloud cotton field', 'Mama’s garden', 'starry rooftop', 'cozy bed'];
const PRENATAL_IMAGERY = ['星星灯笼', '心跳小鼓', '梦的种子', '云朵口袋', '月光小船'];
const PRENATAL_IMAGERY_EN = ['star lantern', 'heartbeat drum', 'dream seed', 'cloud pocket', 'moonlight boat'];

const EMOTIONAL_ANCHORS = [
  '心跳/节拍：妈妈的心跳、血脉流动声、钟摆声（固定高光：让主角途经温暖水域或光晕，感知到「妈妈的心跳/微光」）。',
  '包裹/承载：柔软云墙、气泡、被水流/风轻轻托着、温暖的被窝——暗合羊水里的被包裹感。',
  '光与希望：微光、星光、萤火、黎明的金边。',
  '温度与触觉：手掌温度、温牛奶热气、阳光暖照、软软的毛茸茸。',
  '声音记忆：爸爸的笑声、妈妈的哼歌、门铃、拖鞋声。',
  '成长意象：种子发芽、小脚印、房子变大、宝宝安心长大。',
  '家庭连结：哥哥的画、奶奶的袜子、全家声景、妈妈的声音。'
];

const EMOTIONAL_ANCHORS_EN = [
  'Heartbeat / rhythm: mother’s heartbeat, blood flow, a ticking clock (fixed high point: let the protagonist sense mother’s heartbeat or a glow).',
  'Wrapping / carrying: soft cloud walls, bubbles, being held by water or wind, a warm duvet — echoing the womb’s embrace.',
  'Light & hope: a glimmer, starlight, fireflies, the golden edge of dawn.',
  'Temperature & touch: the warmth of a palm, steam from warm milk, sunny warmth, soft fur.',
  'Sound memory: dad’s laugh, mom’s humming, the doorbell, the sound of slippers.',
  'Growth imagery: a seed sprouting, little footprints, a house growing, the baby growing safe and sound.',
  'Family connection: big brother’s drawing, grandma’s socks, the whole family’s soundscape, mom’s voice.'
];

const PRENATAL_SAFETY = [
  '禁止任何危险、冲突、跌落、破碎、黑暗吞噬、分离、追赶情节。',
  '禁止否定式安慰（如「不要怕」「别哭」），只用正向温柔的安抚。',
  '禁止角色有不幸经历或负面性格；世界必须全然的善意与安全。',
  '胎教期故事讲给肚里尚未出生的宝宝听：绝不可把宝宝写成已经出生；结尾多以「等你准备好了」「安心长大就好」等温柔守候收束；可让主角途经温暖水域/光晕，感知到「妈妈的心跳」作为固定的情感高光。',
  '项目硬约束：禁止出现螃蟹 / 大闸蟹 / 任何蟹类角色、食物或情节（含长荡湖等以蟹为卖点的内容）。',
  '不使用中文弯引号「"」，用「」或单引号。'
];

const PRENATAL_SAFETY_EN = [
  'No danger, conflict, falling, breaking, dark engulfing, separation, or chasing.',
  'No negative comfort (e.g. "don’t be afraid", "don’t cry"); only gentle positive reassurance.',
  'No unfortunate backstories or negative traits; the world must be wholly kind and safe.',
  'Prenatal stories are told to the unborn baby still in mommy’s tummy: never write the baby as already born; end with tender waiting like "when you are ready" / "just grow safe and sound"; let the protagonist sense "mother’s heartbeat" as the fixed emotional high point.',
  'Hard project rule: never include crabs / hairy crabs / any crab character, food, or plot (including places marketed for crabs).',
  'Do not use Chinese curly quotes ""; use 「」 or straight single quotes.'
];

function pickProtagonist(dateStr, lang) {
  const offset = lang === 'en' ? Math.floor(PRENATAL_CAST.length / 2) : 0;
  const idx = (hashDate(dateStr + '-prot-' + lang) + offset) % PRENATAL_CAST.length;
  return PRENATAL_CAST[idx];
}

function buildPrenatalBlock(dateStr, lang) {
  const prot = pickProtagonist(dateStr, lang);
  if (lang === 'zh') {
    const scenes = PRENATAL_SCENES.join('、');
    const imagery = PRENATAL_IMAGERY.join('、');
    const anchors = EMOTIONAL_ANCHORS.map((a, i) => (i + 1) + '. ' + a).join('  ');
    const safety = PRENATAL_SAFETY.join(' ');
    return `

**胎教期增强 · 「故事孕育师」方法（请在本篇落实）**
本篇优先小主角（以其设定为基准展开，保持性格与口头禅前后一致；可让它遇见材料库里的其他伙伴，形成温柔的连续感）：
- ${prot.name}（${prot.type}｜home: ${prot.home}｜性格: ${prot.personality}｜口头禅: ${prot.catchphrase}）
常驻材料库（可顺带出现，让世界更连贯）：场景如 ${scenes}；意象如 ${imagery}。已有故事的主人公就是最珍贵的素材，可在不同故事里让它们偶尔相遇。
情感锚点（本篇必须自然嵌入至少 3 种，多选多益）：
${anchors}
安全边界（绝对遵守）：${safety}
故事骨架提示：微小主角 → 一个温柔的愿望 → 被水流/风/歌声轻轻托送（暗合羊水体验） → 遇见颜色/味道/温度/旋律的感官之美 → 途经温暖水域或光晕，感知到「妈妈的心跳」作为固定高光 → 用「小宝宝，你听到了吗？」式对话与肚里宝宝说话 → 以温柔守候收尾（如「等你准备好了，外面的世界有软软的风和圆圆的月亮等你」）。`;
  }
  const scenes = PRENATAL_SCENES_EN.join(', ');
  const imagery = PRENATAL_IMAGERY_EN.join(', ');
  const anchors = EMOTIONAL_ANCHORS_EN.map((a, i) => (i + 1) + '. ' + a).join('  ');
  const safety = PRENATAL_SAFETY_EN.join(' ');
  return `

**Prenatal enhancement · "Story-Midwife" method (apply in this story)**
Preferred little protagonist for this story (base the story on this character, keep personality & catchphrase consistent; may meet other library friends for a gentle sense of continuity):
- ${prot.name} (${prot.enType} | home: ${prot.enHome} | personality: ${prot.enPersonality} | catchphrase: ${prot.enCatchphrase})
Resident material library (may appear alongside, to make the world coherent): scenes like ${scenes}; imagery like ${imagery}. Past story protagonists are precious material — let them occasionally meet across stories.
Emotional anchors (embed at least 3 of these naturally; more is better):
${anchors}
Safety boundaries (strictly obey): ${safety}
Skeleton hint: tiny protagonist → a gentle wish → carried softly by water/wind/song (echoing the womb) → sensory beauty of colour/taste/temperature/melody → passing warm waters or a glow, sensing "mother’s heartbeat" as the fixed high point → talk to the unborn baby with "little one, can you hear?" → end with tender waiting (e.g. "when you are ready, the soft wind and round moon will be waiting").`;
}
