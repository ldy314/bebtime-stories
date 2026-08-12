/**
 * Prompt Builder for Bedtime Story Generation
 * Contains age group calculation and prompt assembly for Chinese & English stories.
 *
 * Enriched edition: adds a rotating theme pool (nature/science, Chinese culture,
 * emotions, imagination, daily life, light adventure), expanded author styles,
 * and form-innovation guidance. Theme variety is enforced per-date so consecutive
 * days naturally get different themes.
 *
 * 2026-08-02: theme pool expanded with the 700-theme inspiration library
 * (deepseek_提示2.md) — 20 broad categories (history, music/art, friendship,
 * fantasy, city, animals, numbers, body, environment, festivals, travel, dreams,
 * sports, language, tech, philosophy, family, natural wonders, adventure, love)
 * plus a deterministic concrete "seed" library injected per-story for variety.
 * 2026-08-02: added monthly seed batch unlock system (SEED_BATCHES + getUnlockedSeeds)
 * — 12 months × 32 seeds, all 20 categories mixed each month.
 */

const path = require('path');
const fs = require('fs');

const CHILD_BIRTHDAY = '2026-09-22';

/**
 * Calculate age group based on a given date
 */
function getAgeInfo(dateStr) {
  const birthday = new Date(CHILD_BIRTHDAY + 'T00:00:00+08:00');
  const checkDate = new Date(dateStr + 'T00:00:00+08:00');

  if (checkDate < birthday) {
    return { group: 'prenatal', labelCn: '胎教期', labelEn: 'Prenatal' };
  }

  const diffMs = checkDate - birthday;
  const diffDays = diffMs / (1000 * 60 * 60 * 24);
  const diffYears = diffDays / 365.25;

  if (diffYears < 1) return { group: '0-1', labelCn: '0-1岁', labelEn: '0-1 yr' };
  if (diffYears < 3) return { group: '1-3', labelCn: '1-3岁', labelEn: '1-3 yr' };
  if (diffYears < 6) return { group: '3-6', labelCn: '3-6岁', labelEn: '3-6 yr' };
  return { group: '6+', labelCn: '6岁以上', labelEn: '6+ yr' };
}

/**
 * Get Chinese weekday string
 */
function getChineseWeekday(dateStr) {
  const weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];
  const [y, m, d] = dateStr.split('-').map(Number);
  // 直接用 dateStr 解析为 UTC 日历日，彻底脱离运行环境时区
  return weekdays[new Date(Date.UTC(y, m - 1, d)).getUTCDay()];
}

/**
 * Format date as "YYYY年M月D日"
 */
function formatDateCn(dateStr) {
  const [y, m, d] = dateStr.split('-').map(Number);
  return `${y}年${m}月${d}日`;
}

/**
 * Format date short as "MM/DD"
 */
function formatDateShort(dateStr) {
  const [, m, d] = dateStr.split('-');
  return `${m}/${d}`;
}

/**
 * Deterministic per-date hash so different dates pick different themes (variety).
 */
function hashDate(dateStr) {
  let h = 0;
  for (let i = 0; i < dateStr.length; i++) {
    h = (h * 31 + dateStr.charCodeAt(i)) >>> 0;
  }
  return h;
}

// ===== Age group style descriptions =====
const AGE_STYLE_CN = {
  prenatal: '胎教期：语调极其温柔缓慢，多用拟声词和节奏感，主题围绕"等待、爱、守护、妈妈的声音"，适合胎教朗读。',
  '0-1': '0-1岁：极简短句，大量重复和拟声词（如动物叫声、自然声音），主题围绕"感官启蒙、安全感、日常事物认知"，适合哄睡朗读。',
  '1-3': '1-3岁：简单情节，角色为动物或日常物品，主题围绕"生活习惯、情绪认知、简单友谊、探索世界"，句子短小易懂。',
  '3-6': '3-6岁：完整故事情节，角色丰富，主题围绕"勇气、分享、诚实、友谊、好奇心、解决问题"，可加入简单对话和冒险元素。',
  '6+': '6岁以上：故事可更长更复杂，主题围绕"成长、责任、善良、坚持、梦想、同理心"，可加入比喻和深层寓意。'
};

const AGE_STYLE_EN = {
  prenatal: 'Prenatal stage: extremely gentle and slow pace, heavy use of onomatopoeia and rhythm, themes around "waiting, love, guardianship, mother\'s voice", suitable for prenatal reading.',
  '0-1': '0-1 yr: minimal vocabulary, heavy repetition and onomatopoeia (animal sounds, nature sounds), themes around "sensory awakening, security, daily object recognition", suitable for soothing sleep.',
  '1-3': '1-3 yr: simple plot, animal or everyday object characters, themes around "daily habits, emotion awareness, simple friendship, exploring the world", short and easy sentences.',
  '3-6': '3-6 yr: complete story plots, rich characters, themes around "courage, sharing, honesty, friendship, curiosity, problem-solving", can include simple dialogue and adventure elements.',
  '6+': '6+ yr: longer and more complex stories, themes around "growth, responsibility, kindness, perseverance, dreams, empathy", can include metaphors and deeper meanings.'
};

// ===== Theme pool (rotating per date for variety) =====
const THEME_POOL_CN = [
  {
    name: '自然与科学启蒙',
    desc: '二十四节气（春分的燕子、谷雨的茶、霜降的枫叶）、星空宇宙（月亮的秘密、流星、小小宇航员）、微观世界（蚂蚁搬家、蝴蝶蜕变、萤火虫森林）、海洋与雨林（珊瑚城、座头鲸的歌）。'
  },
  {
    name: '中国文化与传统',
    desc: '传统节日传说（春节、中秋、端午、重阳的暖心版）、神话新编（精卫、嫦娥、夸父的温柔低龄化）、古诗词意境化（把「床前明月光」「小荷才露尖尖角」写成小故事）、十二生肖与民间智慧。'
  },
  {
    name: '情感与心理',
    desc: '情绪小怪兽（生气、害羞、害怕、嫉妒怎么安放）、安全感（怕黑、打雷、第一次分床）、家庭与爱（隔代亲情、二胎、宠物朋友）、自我接纳（「我和别人不一样也没关系」）。'
  },
  {
    name: '想象与奇幻',
    desc: '梦境探险（云朵上的城市、会飞的床）、物品有灵（玩具夜谈、书架里的秘密通道）、反向世界（如果颜色会消失、如果动物说人话）。'
  },
  {
    name: '生活与认知',
    desc: '职业初识（面包师、园丁、温柔版医生）、好习惯（刷牙、收拾玩具、按时睡觉）、食物旅行（一颗苹果的诞生、馒头的故事）。'
  },
  {
    name: '轻松愉快的冒险',
    desc: '温和不刺激的轻冒险——寻宝小旅程、迷路后回家、帮朋友送东西、森林里的小任务。冒险不危险、悬念不紧张、冲突不激烈，所有困难最终都被善良、友谊或勇气化解，给孩子「我也能行」的安全感与力量感。'
  }
];

const THEME_POOL_EN = [
  {
    name: 'Nature & science',
    desc: 'the 24 solar terms, stars and space (the moon\'s secret, a little astronaut), the tiny world of ants/butterflies/fireflies, coral reefs and whales.'
  },
  {
    name: 'Chinese culture & tradition',
    desc: 'gentle festival tales (Spring Festival, Mid-Autumn, Dragon Boat), softened myths (Jingwei, Chang\'e), classical Chinese poems turned into little stories, the zodiac.'
  },
  {
    name: 'Feelings & heart',
    desc: 'the "emotion little monsters" (anger, shyness, fear, jealousy), security (afraid of the dark, thunder, first night alone), family love (grandparents, a new sibling, a pet), self-acceptance ("it\'s okay to be different").'
  },
  {
    name: 'Imagination & whimsy',
    desc: 'dream adventures (a city on the clouds, a flying bed), animated objects (toys\' night talk, a secret passage in the bookshelf), topsy-turvy worlds (if colors disappeared, if animals spoke).'
  },
  {
    name: 'Daily life & learning',
    desc: 'first jobs (baker, gardener, a gentle doctor), good habits (brushing teeth, tidying up, bedtime on time), food journeys (the birth of an apple, the story of a steamed bun).'
  },
  {
    name: 'Light & cheerful adventure',
    desc: 'gentle, non-scary adventures — a little treasure hunt, finding the way home, helping a friend deliver something, a small forest quest. No real danger, no tense suspense; every trouble is solved by kindness, friendship, or courage, leaving the child with a warm "I can do it too" feeling.'
  }
];

// ===== Expanded theme pool from the 700-theme inspiration library (deepseek_提示2.md) =====
// 把「历史/传说、音乐/艺术、友情、幻想、城市、动物新篇、数字、身体、环保、节日、
// 旅行、梦境、运动、语言、科技、哲学、家庭、自然奇观、冒险、爱」20 大类的灵感，
// 全部并入题材池，大幅消除题材单调，并配合下面的「具体选题种子」给 AI 更落地的火花。
const THEME_POOL_EXTRA_CN = [
  { name: '历史与传说', desc: '穿越时空的温柔故事——长城的一块砖、丝绸之路上的小骆驼、金字塔的秘密通道、郑和的宝船、吴哥窟的树根精灵、复活节岛的石像。用孩子的眼睛看历史。' },
  { name: '音乐与艺术', desc: '声音与色彩的故事——不会画圆的小画家、调色盘上的颜色吵架、会唱歌的贝壳、午夜的乐队、敦煌壁画的飞天、蒙娜丽莎的微笑。艺术启蒙，感受美。' },
  { name: '友情与社交', desc: '朋友间的温暖——两棵树的约定、分一半的梨、共享的梦、会发光的友谊手环、借来的勇气、最安静的派对。学会相处与接纳。' },
  { name: '幻想与魔法', desc: '奇幻新世界——能长成任何东西的种子、倒流的瀑布、月亮上的图书馆、会穿越墙壁的猫、十二点的南瓜车、影子剧团。' },
  { name: '城市与建筑', desc: '钢筋水泥里的童话——摩天楼顶的花园、会讲故事的路灯、地下管道里的鲸鱼、地铁里的图书馆、桥下的音乐会、老邮筒里的蜗牛。' },
  { name: '动物王国新篇', desc: '动物的奇思妙想——大象的幼儿园、会讲故事的老海龟、爱看书的猫头鹰、最矮的长颈鹿、有口吃的鹦鹉、北极熊的夏日烦恼。' },
  { name: '数字与逻辑', desc: '数学小冒险——数字国的「0」国王、会算术的蚂蚁、斐波那契数列的向日葵、对称的小蝴蝶、黄金比例的螺旋、质数的孤独派对。' },
  { name: '身体与健康', desc: '认识自己——心跳的鼓点、骨头的对话、血液的红细胞快递员、做梦时的大脑、脚丫的「地面读卡器」、眨眼的雨刮器。' },
  { name: '环保与地球', desc: '守护家园——北极冰的求救、种树的小女孩、会说话的垃圾、城市里的「绿墙」、地球的生日愿望、鲸鱼的「碳汇」。' },
  { name: '节日与庆典', desc: '特别的日子——春节「福」字倒贴、中秋的月饼思念、端午的粽子之争、七夕的喜鹊桥、世界读书日的书、母亲节的拥抱。' },
  { name: '旅行与探索', desc: '世界那么大——火车窗外的画册、山巅的日出、海底两万里、热气球上看云海、古镇的巷子、水乡的摇橹船。' },
  { name: '梦境与潜意识', desc: '梦里的奇妙事——可以预订的梦、梦里的飞行、梦里遇见已故的爷爷、清醒梦、把梦画下来、梦里的平行世界。' },
  { name: '运动与挑战', desc: '动起来的故事——第一次学骑车、游泳的水朋友、篮球的空心入网、攀岩的三点固定、滑冰跌倒后站起来、射箭的专注。' },
  { name: '语言与故事', desc: '文字的力量——不会写字的男孩用画讲故事、字典里的旅行、一句话的力量、睡前故事的温度、编故事的快乐、书签的视角。' },
  { name: '科技与未来', desc: '明天的世界——机器人的情感芯片、3D打印的「妈妈」、太空电梯的旅行、会飞的汽车、未来的信、智能眼镜的翻译。' },
  { name: '哲学与思考', desc: '小小思想家——「我是谁」、孤独的对面、「谢谢」的魔力、「对不起」的力量、空白的美、「希望」的颜色。' },
  { name: '家庭新视角', desc: '家的故事——妈妈的口头禅、爸爸的鼾声、饭桌上的故事、晚安吻、外婆的手、回家的路。' },
  { name: '自然奇观', desc: '地球的奇迹——极光的舞蹈、大峡谷的书、珊瑚礁的城市、撒哈拉的星空、地球的转动、贝加尔湖的透明。' },
  { name: '冒险与勇气', desc: '探险之旅——森林深处的宝藏、独自过河、迷路后的冷静、山顶的信号、泥泞的路、悬崖跳伞。' },
  { name: '爱与善良', desc: '温暖人心——流浪猫的新家、给老人的椅子、分享的午餐、雨中的伞、最后的晚安、帮妈妈捶背。' },
  '暖暖厨房里的小麦香',
  '桂花糕的第一缕甜',
  '会唱歌的瓷碗',
  '调色盘上的旅行',
  '蜡笔画出的彩虹路',
  '风铃写给宝宝的信',
  '小火车开往云朵站',
  '会发光的路灯叔叔',
  '外婆的针线筐里住着春天',
  '小雨靴踩出的水花歌',
  '会跳舞的影子朋友',
  '暖水袋里的小太阳',
  '图书馆角落的瞌睡猫',
  '会算术的饼干',
  '望远镜里的小星球',
  '摇篮曲里的星星船',
  '会讲故事的旧藤椅',
  '窗台上的多肉小队'
];

const THEME_POOL_EXTRA_EN = [
  { name: 'History & legend', desc: 'Gentle time-travel tales — a brick in the Great Wall, the little camel on the Silk Road, the pyramids\' secret passage, Zheng He\'s little cabin boy, the tree-root elf of Angkor, the stone statues\' dream on Easter Island.' },
  { name: 'Music & art', desc: 'Stories of sound and colour — the little painter who can\'t draw circles, colours quarrelling on the palette, the singing seashell, the midnight band, the flying apsaras of Dunhuang, Mona Lisa\'s new smile.' },
  { name: 'Friendship & social', desc: 'Warmth between friends — the promise of two trees, half a pear, a shared dream, the glowing friendship bracelet, borrowed courage, the quietest party.' },
  { name: 'Fantasy & magic', desc: 'A brand-new world — the seed that grows anything, the upside-down waterfall, the library on the moon, the cat that walks through walls, the pumpkin carriage at midnight, the shadow theatre.' },
  { name: 'City & architecture', desc: 'Fairy tales in concrete — the garden atop the skyscraper, the streetlamp that tells stories, the whale in the sewer pipes, the library in the subway, the concert under the bridge, the snail in the old mailbox.' },
  { name: 'Animal kingdom new', desc: 'Animals\' whimsy — the elephant\'s kindergarten, the old sea turtle who tells stories, the book-loving owl, the shortest giraffe, the stuttering parrot, the polar bear\'s summer worry.' },
  { name: 'Numbers & logic', desc: 'Math little adventures — King Zero of Numberland, the ant that does arithmetic, Fibonacci\'s sunflower, the symmetrical little butterfly, the golden-ratio spiral, the lonely prime numbers.' },
  { name: 'Body & health', desc: 'Getting to know yourself — the drumbeat of the heartbeat, the bones\' night talk, the red-blood-cell courier, the brain at dreamtime, the foot\'s ground reader, the blinking windshield wiper.' },
  { name: 'Environment & earth', desc: 'Protecting home — the Arctic ice\'s SOS, the girl who planted a tree, the talking trash, the city\'s green wall, Earth\'s birthday wish, the whale\'s carbon sink.' },
  { name: 'Festivals & celebrations', desc: 'Special days — the upside-down Fu character, the mooncake\'s longing, the sweet vs salty zongzi, the magpie bridge of Qixi, the book on World Book Day, Mother\'s Day hug.' },
  { name: 'Travel & exploration', desc: 'The world is so big — the picture book outside the train window, sunrise from the summit, twenty thousand leagues under the sea, cloud sea from the hot-air balloon, the alleys of the old town, the rowing boat in the water town.' },
  { name: 'Dreams & subconscious', desc: 'Wonders in dreams — ordering a dream, flying in a dream, meeting grandpa in a dream, lucid dreaming, painting the dream, the parallel world in dreams.' },
  { name: 'Sports & challenges', desc: 'Stories in motion — first time riding a bike, the water friend in swimming, the swish of the basketball, climbing\'s three-point anchor, standing up after falling on ice, archery\'s focus.' },
  { name: 'Language & story', desc: 'The power of words — the boy who can\'t write tells stories by drawing, a journey inside the dictionary, the power of one sentence, the warmth of a bedtime story, the joy of making up stories, the bookmark\'s viewpoint.' },
  { name: 'Tech & future', desc: 'Tomorrow\'s world — the robot\'s feeling chip, the 3D-printed "mom", the space-elevator trip, the flying car, a letter from the future, smart glasses that translate.' },
  { name: 'Philosophy & thinking', desc: 'Little thinkers — "who am I", the opposite of loneliness, the magic of "thank you", the power of "sorry", the beauty of blankness, the colour of hope.' },
  { name: 'Family new perspective', desc: 'Stories of home — Mom\'s catchphrase, Dad\'s snoring, stories at the dinner table, the goodnight kiss, Grandma\'s hands, the way home.' },
  { name: 'Natural wonders', desc: 'Earth\'s miracles — the dance of the aurora, the Grand Canyon\'s book, the coral reef city, the Sahara\'s starry sky, Earth\'s rotation, Lake Baikal\'s clarity.' },
  { name: 'Adventure & courage', desc: 'Journeys of adventure — treasure deep in the forest, crossing the river alone, calm after getting lost, the signal from the summit, the muddy road, cliff parachuting.' },
  { name: 'Love & kindness', desc: 'Warming hearts — the stray cat\'s new home, the seat for the old lady, the shared lunch, the umbrella in the rain, the final goodnight, rubbing Mom\'s back.' }
];

const THEME_POOL_ALL_CN = [...THEME_POOL_CN, ...THEME_POOL_EXTRA_CN];
const THEME_POOL_ALL_EN = [...THEME_POOL_EN, ...THEME_POOL_EXTRA_EN];

// ===== Concrete "seed" library: specific inspiration titles (from deepseek_提示2.md) =====
// pickTheme 给「大类方向」，下面这些具体选题给 AI 更落地的火花；每天确定性抽 4 个，避免相邻日重复。
const CONCRETE_SEEDS_CN = [
  '长城的一块砖的自述', '丝绸之路上的小骆驼', '金字塔的秘密通道', '郑和的宝船小水手', '吴哥窟的树根精灵', '复活节岛的石像梦',
  '不会画圆的小画家', '调色盘上的颜色吵架了', '会唱歌的贝壳', '午夜的乐队', '蒙娜丽莎的微笑新解', '敦煌壁画的飞天',
  '两棵树的约定', '分一半的梨', '共享的梦', '会发光的友谊手环', '借来的勇气', '最安静的派对',
  '能长成任何东西的种子', '倒流的瀑布', '月亮上的图书馆', '会穿越墙壁的猫', '十二点的南瓜车', '影子剧团',
  '摩天楼顶上的花园', '会讲故事的路灯', '地下管道里的鲸鱼', '地铁里的图书馆', '桥下的音乐会', '老邮筒里的蜗牛',
  '大象的幼儿园', '会讲故事的老海龟', '爱看书的猫头鹰', '最矮的长颈鹿', '有口吃的鹦鹉', '北极熊的夏日烦恼',
  '数字国的「0」国王', '会算术的蚂蚁', '斐波那契数列的向日葵', '对称的小蝴蝶', '黄金比例的螺旋', '质数的孤独派对',
  '心跳的鼓点', '骨头的对话', '血液的红细胞快递员', '做梦时的大脑', '脚丫的「地面读卡器」', '眨眼的雨刮器',
  '北极冰的求救', '种树的小女孩', '会说话的垃圾', '城市里的「绿墙」', '地球的「生日愿望」', '鲸鱼的「碳汇」',
  '春节的「福」字倒贴', '中秋节的月饼思念', '端午节的粽子之争', '七夕的喜鹊桥', '世界读书日的书', '母亲节的拥抱',
  '火车窗外的「画册」', '山巅的日出', '海底两万里', '热气球上看云海', '古镇的巷子', '水乡的摇橹船',
  '可以「预订」的梦', '梦里的飞行', '梦里遇见已故的爷爷', '清醒梦', '把梦画下来', '梦里的「平行世界」',
  '第一次学骑车', '游泳的「水朋友」', '篮球的「空心入网」', '攀岩的「三点固定」', '滑冰的「跌倒后站起来」', '射箭的「专注」',
  '不会写字的男孩', '字典里的「旅行」', '一句话的力量', '睡前故事的温度', '编故事的快乐', '书签的视角',
  '机器人的「情感芯片」', '3D打印的「妈妈」', '太空电梯的「旅行」', '会飞的汽车', '未来的信', '智能眼镜的「翻译」',
  '「我是谁」', '「孤独」的对面', '「谢谢」的魔力', '「对不起」的力量', '「空白」的美', '「希望」的颜色',
  '妈妈的口头禅', '爸爸的鼾声', '饭桌上的故事', '晚安吻', '外婆的「手」', '回家的路',
  '极光的舞蹈', '大峡谷的「书」', '珊瑚礁的「城市」', '撒哈拉的「星空」', '地球的「自转」', '贝加尔湖的「透明」',
  '森林深处的「宝藏」', '独自过河', '迷路后的「冷静」', '山顶的「信号」', '泥泞的「路」', '悬崖跳伞',
  '流浪猫的「新家」', '给老人的「椅子」', '分享的「午餐」', '雨中的「伞」', '最后的「晚安」', '帮妈妈捶背'
];

const CONCRETE_SEEDS_EN = [
  'A brick in the Great Wall', 'The little camel on the Silk Road', 'The secret passage of the pyramids', 'Zheng He\'s little cabin boy', 'The tree-root elf of Angkor', 'The stone statues\' dream on Easter Island',
  'The little painter who can\'t draw circles', 'Colors quarrel on the palette', 'The singing seashell', 'The midnight band', 'Mona Lisa\'s new smile', 'The flying apsaras of Dunhuang',
  'The promise of two trees', 'Half a pear', 'A shared dream', 'The glowing friendship bracelet', 'Borrowed courage', 'The quietest party',
  'The seed that grows anything', 'The upside-down waterfall', 'The library on the moon', 'The cat that walks through walls', 'The pumpkin carriage at midnight', 'The shadow theatre',
  'The garden atop the skyscraper', 'The streetlamp that tells stories', 'The whale in the sewer pipes', 'The library in the subway', 'The concert under the bridge', 'The snail in the old mailbox',
  'The elephant\'s kindergarten', 'The old sea turtle who tells stories', 'The book-loving owl', 'The shortest giraffe', 'The stuttering parrot', 'The polar bear\'s summer worry',
  'King Zero of Numberland', 'The ant that does arithmetic', 'Fibonacci\'s sunflower', 'The symmetrical little butterfly', 'The golden-ratio spiral', 'The lonely prime numbers',
  'The drumbeat of the heartbeat', 'The bones\' night talk', 'The red-blood-cell courier', 'The brain at dreamtime', 'The foot\'s ground reader', 'The blinking windshield wiper',
  'The Arctic ice\'s SOS', 'The girl who planted a tree', 'The talking trash', 'The city\'s green wall', 'Earth\'s birthday wish', 'The whale\'s carbon sink',
  'The upside-down Fu character', 'The mooncake\'s longing', 'The sweet vs salty zongzi', 'The magpie bridge of Qixi', 'The book on World Book Day', 'Mother\'s Day hug',
  'The picture book outside the train window', 'Sunrise from the summit', 'Twenty thousand leagues under the sea', 'Cloud sea from the hot-air balloon', 'The alleys of the old town', 'The rowing boat in the water town',
  'Ordering a dream', 'Flying in a dream', 'Meeting grandpa in a dream', 'Lucid dreaming', 'Painting the dream', 'The parallel world in dreams',
  'First time riding a bike', 'The water friend in swimming', 'The swish of the basketball', 'Climbing\'s three-point anchor', 'Standing up after falling on ice', 'Archery\'s focus',
  'The boy who can\'t write', 'A journey inside the dictionary', 'The power of one sentence', 'The warmth of a bedtime story', 'The joy of making up stories', 'The bookmark\'s viewpoint',
  'The robot\'s feeling chip', 'The 3D-printed "mom"', 'The space-elevator trip', 'The flying car', 'A letter from the future', 'Smart glasses that translate',
  'Who am I', 'The opposite of loneliness', 'The magic of "thank you"', 'The power of "sorry"', 'The beauty of blankness', 'The colour of hope',
  'Mom\'s catchphrase', 'Dad\'s snoring', 'Stories at the dinner table', 'The goodnight kiss', 'Grandma\'s hands', 'The way home',
  'The dance of the aurora', 'The Grand Canyon\'s book', 'The coral reef city', 'The Sahara\'s starry sky', 'Earth\'s rotation', 'Lake Baikal\'s clarity',
  'Treasure deep in the forest', 'Crossing the river alone', 'Calm after getting lost', 'The signal from the summit', 'The muddy road', 'Cliff parachuting',
  'The stray cat\'s new home', 'The seat for the old lady', 'The shared lunch', 'The umbrella in the rain', 'The final goodnight',   'Rubbing Mom\'s back',
  'A little wheat aroma in the warm kitchen',
  'the first sweetness of osmanthus cake',
  'the singing porcelain bowl',
  'a journey on the palette',
  'the rainbow road drawn in crayon',
  'the wind-chime’s letter to the baby',
  'the little train to Cloud Station',
  'the glowing streetlamp uncle',
  'spring living in Grandma’s sewing basket',
  'the water-splash song of little rain boots',
  'the dancing shadow friend',
  'a tiny sun in the warm water bottle',
  'the dozing cat in the library corner',
  'the arithmetic biscuit',
  'a little planet in the telescope',
  'the starry boat in the lullaby',
  'the old rattan chair that tells stories',
  'the succulent squad on the windowsill'
];

// Group the concrete seeds by their broad category so the chosen theme gets matching sparks.
const SEED_GROUPS_CN = {};
THEME_POOL_EXTRA_CN.forEach((t, i) => {
  SEED_GROUPS_CN[t.name] = CONCRETE_SEEDS_CN.slice(i * 6, i * 6 + 6);
});
const SEED_GROUPS_EN = {};
THEME_POOL_EXTRA_EN.forEach((t, i) => {
  SEED_GROUPS_EN[t.name] = CONCRETE_SEEDS_EN.slice(i * 6, i * 6 + 6);
});

// ===== Monthly seed batch unlock system =====
// 12 个月 × 32 种子，每月覆盖全部 20 大类（混合分配）
const SEED_BATCHES = {
  1: {
    month: '2026-08',
    label: '暑假·探索·家庭·梦想',
    seeds: [
      '古罗马的鸽子信使','冰岛的精灵石','吹口哨的风','午夜的乐队',
      '彩虹桥上的相遇','秘密基地的钥匙','倒流的瀑布','声音的颜色',
      '自来水管里的彩虹','电梯的冒险','海豚的超声波歌谣','会帮倒忙的豪猪',
      '三角形的稳定故事','黄金比例的螺旋','骨头的对话','睡觉时的生长',
      '会说话的垃圾','沙漠的绿色梦想','圣诞节的雪橇铃铛','复活节的彩蛋',
      '帆船的环球梦','鲸鱼的脊背之旅','重复出现的梦','梦里的长途旅行',
      '足球的最后一分钟','跆拳道的品势','第一个词','睡前故事的温度',
      '虚拟现实的外婆','会飞的汽车','现在的长度','足够的标准'
    ],
    seedsEn: [
      'Pigeon messenger in ancient Rome','Elf stone in Iceland','Whistling wind','The midnight band',
      'Meeting on the rainbow bridge','Key to the secret base','The waterfall that flows upward','Color of sound',
      'Rainbow in the water pipe','Adventure in the elevator','Dolphin song','The porcupine who always helps',
      'Story of the triangle','Golden ratio spiral','Conversation of bones','Growing while sleeping',
      'Talking trash','Desert green dream','Christmas sleigh bells','Easter eggs',
      'Sailing ship round-the-world dream','Journey on the whales back','Recurring dreams','Long journeys in dreams',
      'Last minute of a football match','Taekwondo patterns','The first word','Warmth of bedtime stories',
      'Virtual reality grandmother','Flying cars','The length of now','The standard of enough'
    ]
  },
  2: {
    month: '2026-09',
    label: '开学季·收获·感恩·自然',
    seeds: [
      '魔法铅笔盒','时间放慢的钟','打翻的牛奶','三厘米的勇气',
      '家庭面团','雨的笑声','蜗牛的家族旅行','蚂蚁的城市规划',
      '被遗忘的书','努力的原则','图书馆的幽灵','图书馆的晚上',
      '作业本页码的议论','粉笔的旅行','第一张奖状','书包的周末',
      '月亮的健身房','雪人的冰箱','种子的信任','耐心的种子',
      '稻穗的低头','乘法的桃子','树的秘密语言','蘑菇的突然出现',
      '叶子的指纹','会发光的石头','秋天的夏洛','蜘蛛网的露珠',
      '了不起的小事','不会写的字','第一次举手','小蚂蚁的迷宫'
    ],
    seedsEn: [
      'Magic pencil case','Clock that slows down','Spilled milk','Three centimeters of courage',
      'Family dough','Laughter of rain','Snail family trip','Ant city planning',
      'The forgotten book','Principle of effort','Library ghost','Library at night',
      'Whispers of homework pages','Chalk journey','The first certificate','Weekend of the schoolbag',
      'Moons gym','Snowmans refrigerator','Trust of a seed','Seeds of patience',
      'Bow of the rice stalk','Peach of multiplication','Secret language of trees','Sudden appearance of mushrooms',
      'Fingerprint of a leaf','Glowing stone','Charlottes autumn','Dewdrops on a spider web',
      'Small great things','Words one cant write','First time raising a hand','Little ant maze'
    ]
  },
  3: {
    month: '2026-10',
    label: '国庆·勇气·冒险·动物',
    seeds: [
      '月球上的兔子','火烈鸟的舞蹈','龙卷风的舞会','口袋里的怪兽',
      '进入云朵的扶梯','城市先生和小镇先生','乌龟的恒心','一粒稻谷的故事',
      '壁虎的约会','牵牛花的攀登','獾先生的礼物','每片秋叶的徽章',
      '勇气是一片云','井底之蛙新传','小松鼠的宝藏','北风与太阳',
      '彩虹尽头的金坛','礼让的三兄弟','鲸鱼与小鱼','蒲公英的远行',
      '超级变色龙的隐身','夜晚是什么颜色','顽皮的影子','瓶子里的星空',
      '爱心树','小鼹鼠的宇宙','月亮的温度','两只蜗牛的路',
      '蜡笔大小的便利','小花猫的胡须','风到哪里去了','小不点的大海'
    ],
    seedsEn: [
      'Rabbit on the moon','Dance of the flamingos','Tornado ball','Monster in the pocket',
      'Escalator into the clouds','Mr City and Mr Town','Persistence of the turtle','Story of a single grain of rice',
      'Geckos date','Morning glories climb','Mr Badgers gift','Badge of every autumn leaf',
      'Courage is a cloud','The frog in the well revisited','Little squirrels treasure','The north wind and the sun',
      'Gold at the end of the rainbow','Three brothers who yield','Whale and small fish','Dandelions journey',
      'Super chameleons invisibility','What color is night','Naughty shadow','Starry sky in a bottle',
      'The giving tree','Little moles universe','Temperature of the moon','Two snails road',
      'Crayon-sized convenience','Kittens whiskers','Where did the wind go','Little ones big sea'
    ]
  },
  4: {
    month: '2026-11',
    label: '冬季·温暖·成长·科技',
    seeds: [
      '智能手环的预言','小麻雀的围巾','青蛙与人鱼','枫树下的约会',
      '星空的向往','石榴娃娃的问候','慈母手中线','收集声音的男孩',
      '蒸汽的大壶','月亮丢了','生活就像一个苹果','生活需要哭泣',
      '错位的照片','板凳·童年','换尾巴','小鼹鼠的火车',
      '太阳是个魔术师','睡美人','老爷爷的梦境','一颗种子的信念',
      '烟花的故事','时间消失了','懂得分享','勇气',
      '十一月的秋天','许愿一千回','愿望迟早实现','小爱心',
      '家庭团聚','蝴蝶的勇气','多彩的世界','奇妙的桥'
    ],
    seedsEn: [
      'Smart bracelet prophecy','Little sparrows scarf','Frog and mermaid','Date under the maple tree',
      'Longing for the starry sky','Pomegranate dolls greeting','Thread from a mothers hand','Boy who collects sounds',
      'The steaming kettle','The moon is gone','Life is like an apple','Life needs tears',
      'Misplaced photo','The bench of childhood','Swapping tails','Little moles train',
      'The sun is a magician','Sleeping beauty','Old mans dream','A seeds belief',
      'Story of fireworks','Time disappeared','Learning to share','Courage',
      'Autumn in November','Wish a thousand times','Wishes come true','A little love',
      'Family reunion','Butterflys courage','Colorful world','A wonderful bridge'
    ]
  },
  5: {
    month: '2026-12',
    label: '年终·回顾·童年·幻想',
    seeds: [
      '梦里的白莲','梦游记','落叶的语言','蓝鲸的旅程',
      '人鱼的奇遇记','消失的星光','勇敢机警','怕冷的雪人',
      '城南旧事','寻找勇敢的小王子','小王子','诚实的小白兔',
      '孔雀小明','小松鼠的学校生活','七色花','灰姑娘',
      '小红帽','会飞的扫帚','会走路的字典','上学第一天',
      '影子请假','烟花的告白','打翻的音乐盒','长颈鹿的围巾',
      '糖葫芦不见了','云朵猫','带雨的云','两只小熊',
      '铅笔盒里的对话','怕痒的月亮','花婆婆','奇妙的种子'
    ],
    seedsEn: [
      'White lotus in the dream','Dream journey','Language of falling leaves','Blue whales journey',
      'Mermaids adventure','Fading starlight','Brave and alert','Snowman who hates the cold',
      'Old stories of the south city','Search for the brave little prince','The little prince','Honest little white rabbit',
      'Peacock Xiaoming','Little squirrels school life','Seven-colored flower','Cinderella',
      'Little red riding hood','Flying broom','Walking dictionary','First day of school',
      'Shadow takes a day off','Confession of fireworks','Overturned music box','Giraffes scarf',
      'Candy haws gone missing','Cloud cat','Rain-bearing cloud','Two little bears',
      'Dialogue in the pencil case','Ticklish moon','Miss Rumphius','Wonderful seed'
    ]
  },
  6: {
    month: '2027-01',
    label: '新年·希望·动物·冒险',
    seeds: [
      '第一场雪','小松鼠的新年愿望','兔年说兔','马路上的新朋友',
      '和星星打电话','魔镜的冬天','树居小仙','用影子玩耍',
      '小鱼的冬天','糖果屋历险记','小红鱼','猫钓鱼',
      '小松鼠的礼物','雪花的白帽子','南飞的新旅','云朵棉花糖',
      '小小运动员','勇敢地飞翔','善意是最响亮的','蝴蝶和小鸟',
      '小红花的心愿','小猫咪的婚纱','春天在哪里','夜空中的星星',
      '可爱的小动物','小脚印','美丽的太阳','今天穿什么',
      '小帮手','赶海','平安归来','小鱼儿回家'
    ],
    seedsEn: [
      'First snowfall','Little squirrels new year wish','Year of the rabbit','New friend on the road',
      'Phone call with the stars','The magic mirrors winter','Tree-dwelling elf','Playing with shadows',
      'Little fishs winter','Hansel and Gretel','The little red fish','Cat fishes',
      'Little squirrels gift','Snowflakes white hat','Journey south','Cotton candy clouds',
      'Little athlete','Flying bravely','Kindness is the loudest','Butterfly and bird',
      'Little red flowers wish','Little cats wedding dress','Where is spring','Stars in the night sky',
      'Cute little animals','Tiny footprints','Beautiful sun','What to wear today',
      'Little helper','Tide picking','Safe return','Little fish goes home'
    ]
  },
  7: {
    month: '2027-02',
    label: '春天·家庭·动物·想象',
    seeds: [
      '不再有条件的家','不再有家庭的岛','小阁楼的秘密','小徒弟',
      '西瓜们的奉献','小橘灯','天黑前的歌剧','小星星的吻',
      '猜不着的谜','麻雀的太阳','小老虎的花','小狐狸的创意',
      '小企鹅的棉衣','报春的花','安静的雪','苹果姑娘',
      '蚂蚁小时工','最诚实的话','小小的约定','勇敢的葵花',
      '妈妈的唠叨','爱的声音','姥姥的澎湖湾','妈妈的晚安',
      '妈妈是超人','童年旋涡','让路','热烘烘的太阳',
      '温暖的围巾','我妈妈','外婆的牵手','妈妈和月亮'
    ],
    seedsEn: [
      'Home without conditions','Island without a family','Secret of the attic','Little apprentice',
      'Watermelons dedication','Little orange lamp','Opera before dark','Little stars kiss',
      'Unsolvable riddle','Sparrows sun','Little tigers flower','Little foxs idea',
      'Little penguins cotton-padded jacket','Harbinger flower','Quiet snow','Apple girl',
      'Ant hour worker','Most honest words','Little promise','Brave sunflower',
      'Mom nagging','Sound of love','Grandmas bay','Mom goodnight',
      'Mom is a superhero','Childhood vortex','Giving way','Warm sun',
      'Warm scarf','My mom','Grandmas hand','Mom and the moon'
    ]
  },
  8: {
    month: '2027-03',
    label: '春天·自然·环保·勇气',
    seeds: [
      '地球的小主人','小小消费者','小怕','风中的树叶',
      '想和圣诞树做朋友','小岛向导','快乐的勇敢','绿色的小主人',
      '彩色的梦','冬天的第一场雪','划船龙的约定','清明的雨',
      '蝌蚪变青蛙','燕子的信','杜鹃花的坚持','小蜜蜂的梦想',
      '小燕子筑巢','小蜜蜂的蜜','小蜻蜓的翅膀','小蝴蝶的裙子',
      '爱护小树苗','会走的衣柜','电的奥秘','垃圾分类员',
      '洗菜水的旅行','塑料袋的再生','森林里的小法庭','地球的体温',
      '纽扣云','会说话的电池','雨水收集器','小蚂蚁的地铁'
    ],
    seedsEn: [
      'Little guardian of the earth','Little consumer','A little afraid','Leaves in the wind',
      'Wants to be friends with the Christmas tree','Island guide','Joyful courage','Little guardian of green',
      'Colorful dream','First snow of winter','Dragon boat promise','Qingming rain',
      'Tadpole becomes a frog','Swallows letter','Rhododendrons persistence','Little bees dream',
      'Little swallow builds a nest','Little bees honey','Little dragonflys wings','Little butterflys skirt',
      'Protecting saplings','Walking wardrobe','Mystery of electricity','Waste sorting officer',
      'Journey of dishwater','Plastic bag recycling','Little court in the forest','Earths temperature',
      'Button cloud','Talking battery','Rain collector','Little ant subway'
    ]
  },
  9: {
    month: '2027-04',
    label: '阅读月·童话·想象·友谊',
    seeds: [
      '书的精灵','小狗与"年"','日光的魔法','糖果小屋',
      '幸福的王子','天鹅的羽毛','小不点','那个老故事',
      '奔跑的羊皮纸','说话的书架','借故事的树','古诗词里的春天',
      '唐诗里的小船','宋词里的月亮','元曲里的山水','诗经里的草',
      '字的朋友','写故事的笔','会翻页的风','字典里的旅行',
      '一句话的力量','不会写字的男孩','编故事的快乐','书签的视角',
      '绘本里的秘密','读后感的小精灵','阅读的种子','故事的翅膀',
      '夜读的萤火虫','一本书的旅行','被打断的故事','听故事的小熊'
    ],
    seedsEn: [
      'Book elf','Puppy and the Nian','Magic of daylight','Candy cottage',
      'Happy prince','Swans feather','Tiny one','That old story',
      'Running parchment','Talking bookshelf','Tree that lends stories','Spring in classical poetry',
      'Little boat in Tang poetry','Moon in Song poetry','Landscape in Yuan drama','Grass in the Book of Songs',
      'Friend of words','Pen that writes stories','Wind that turns pages','Journey inside the dictionary',
      'Power of one sentence','Boy who cant write','Joy of making up stories','Bookmarks perspective',
      'Secret in picture books','Reading-elf','Seed of reading','Wings of story',
      'Firefly reading at night','Journey of a book','Interrupted story','Little bear listening to stories'
    ]
  },
  10: {
    month: '2027-05',
    label: '劳动·职业·运动·探索',
    seeds: [
      '面包师的酵母','园丁的时间','温柔版医生','第一个邮递员',
      '小小消防员','会修钟的人','灯塔看守人','小小考古学家',
      '第一次学骑车','游泳的水朋友','篮球的空心入网','攀岩的三点固定',
      '滑冰跌倒后站起来','射箭的专注','足球的最后一分钟','跆拳道的品势',
      '长城的砖','丝绸之路的骆驼','金字塔的秘密','郑和的宝船',
      '吴哥窟的树根','复活节岛的石像','热气球看云海','帆船的环球梦',
      '灯的信','小小科学家','超级变色龙的隐身','了不起的蚂蚁',
      '公鸡的喔喔','顽皮的星星','谦虚的彩虹','丰富的友谊'
    ],
    seedsEn: [
      'Bakers yeast','Gardeners time','Gentle doctor','The first postman',
      'Little firefighter','Clock fixer','Lighthouse keeper','Little archaeologist',
      'First time riding a bike','Water friend in swimming','Basketball swish','Climbing three-point anchor',
      'Standing up after falling on ice','Archery focus','Last minute of football','Taekwondo patterns',
      'A brick in the Great Wall','Camel on the Silk Road','Secret of the pyramids','Zheng Hes treasure ship',
      'Tree roots of Angkor','Statues of Easter Island','Cloud sea from a hot-air balloon','Sailing ship round-the-world dream',
      'Letter from a lamp','Little scientist','Super chameleons invisibility','Amazing ants',
      'Roosters crow','Naughty star','Humble rainbow','Abundant friendship'
    ]
  },
  11: {
    month: '2027-06',
    label: '夏天·海洋·星空·成长',
    seeds: [
      '神奇的材料','光的故事','小小数学家','大胆的科学实验',
      '地球的故事','让地球更美好','星空的诗歌','小小机器人',
      '小小发明家','太空快递','太阳系的旅行','月球的背面',
      '水的故事','会飞的猫','会走路的树','会唱歌的珊瑚',
      '小鱼的大海','海龟的旅程','鲸鱼的歌唱','海豚的超声波',
      '彩色的海','海洋里的城堡','海底两万里','小贝壳的歌',
      '会帮倒忙的小家伙','会飞的汽车','智能小管家','未来的学校',
      '机器人的情感','天空的画','给星星打电话','数星星的孩子'
    ],
    seedsEn: [
      'Amazing materials','Story of light','Little mathematician','Bold science experiment',
      'Story of the earth','Making the earth better','Poetry of the stars','Little robot',
      'Little inventor','Space delivery','Journey of the solar system','Far side of the moon',
      'Story of water','Cat that flies','Walking tree','Singing coral',
      'Little fishs big sea','Sea turtles journey','Song of the whale','Dolphin ultrasound',
      'Colorful sea','Castle in the ocean','Twenty thousand leagues under the sea','Little shells song',
      'Little helper who makes mistakes','Flying car','Smart little butler','School of the future',
      'Robot feelings','Painting of the sky','Phone call to the stars','Child counting stars'
    ]
  },
  12: {
    month: '2027-07',
    label: '暑假尾声·回顾·准备·新起点',
    seeds: [
      '飞翔的小飞机','月亮和星星','绿草','快乐成长',
      '超级智慧','探索未知','阳光','温暖的旅程',
      '萤火虫的森林','云朵上的城市','想飞的床','玩具夜谈',
      '书架里的秘密','午夜的乐队','会唱歌的贝壳','调色盘吵架',
      '落叶的信','蚂蚁搬家','蝴蝶蜕变','小种子的春天',
      '冬至的饺子','夏至的蝉','春分的燕子','谷雨的茶',
      '妈妈的声音','爸爸的力量','外婆的手','回家的路',
      '晚安的故事','许愿的小星星','愿望成真','十二个月的礼物'
    ],
    seedsEn: [
      'Flying little airplane','Moon and stars','Green grass','Happy growth',
      'Super wisdom','Exploring the unknown','Sunshine','Warm journey',
      'Forest of fireflies','City on the clouds','Bed that wants to fly','Toys night talk',
      'Secret of the bookshelf','The midnight band','Singing seashell','Colors quarrel on the palette',
      'Letter from a falling leaf','Ants moving','Butterfly metamorphosis','Spring of a little seed',
      'Dumplings of winter solstice','Cicadas of summer solstice','Swallows of spring equinox','Tea of grain rain',
      'Moms voice','Dads strength','Grandmas hands','The way home',
      'Goodnight story','Wishing little star','Wishes come true','Gift of twelve months'
    ]
  }
};

/**
 * Get the full seed list available for the current month,
 * including: base CONCRETE_SEEDS + unlocked SEED_BATCHES + dynamic-seeds.json
 */
function getUnlockedSeeds(lang) {
  const baseSeeds = lang === 'zh' ? [...CONCRETE_SEEDS_CN] : [...CONCRETE_SEEDS_EN];
  const now = new Date();
  const currentMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;

  // Unlock SEED_BATCHES up to and including current month
  for (const batch of Object.values(SEED_BATCHES)) {
    if (batch.month <= currentMonth) {
      const batchSeeds = lang === 'zh' ? batch.seeds : (batch.seedsEn || batch.seeds);
      // Filter out external_ and ai_ prefixes (those are for dynamic-seeds.json only)
      const validSeeds = batchSeeds.filter(s => !s.startsWith('external_') && !s.startsWith('ai_'));
      baseSeeds.push(...validSeeds);
    }
  }

  // Read dynamic-seeds.json for external + AI seeds
  try {
    const dynamicPath = path.join(__dirname, 'dynamic-seeds.json');
    if (fs.existsSync(dynamicPath)) {
      const dynamic = JSON.parse(fs.readFileSync(dynamicPath, 'utf-8'));
      for (const month of Object.keys(dynamic)) {
        if (month <= currentMonth && dynamic[month] && dynamic[month].seeds) {
          const langSeeds = lang === 'zh'
            ? (dynamic[month].seeds.zh || dynamic[month].seeds)
            : (dynamic[month].seeds.en || dynamic[month].seeds);
          if (Array.isArray(langSeeds)) {
            baseSeeds.push(...langSeeds.filter(s => !s.startsWith('external_') && !s.startsWith('ai_')));
          }
        }
      }
    }
  } catch (e) {
    console.warn('Warning: Could not read dynamic-seeds.json:', e.message);
  }

  return baseSeeds;
}

/**
 * Pick the broad theme direction for a date (rotates across the full 26-theme pool).
 */
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

const PRENATAL_SCENES = ['海草森林', '月光海面', '云端棉田', '妈妈的花园', '星夜天台', '暖暖被窝', '清晨的花瓣露台', '暖暖的厨房窗台', '雨后的小院', '麦浪里的石磨', '雪地小木屋', '森林溪边', '图书馆角落', '风铃走廊'];
const PRENATAL_SCENES_EN = ['seagrass forest', 'moonlit sea', 'cloud cotton field', 'Mama’s garden', 'starry rooftop', 'cozy bed', 'dawn petal terrace', 'warm kitchen windowsill', 'courtyard after rain', 'stone mill in the wheat field', 'snowy cabin', 'forest streamside', 'library corner', 'wind-chime corridor'];
const PRENATAL_IMAGERY = ['星星灯笼', '心跳小鼓', '梦的种子', '云朵口袋', '月光小船', '风的信笺', '彩虹小桥', '会发芽的雨滴', '会唱歌的鹅卵石', '面包的香气云', '小脚印地图', '温暖的毛线团'];
const PRENATAL_IMAGERY_EN = ['star lantern', 'heartbeat drum', 'dream seed', 'cloud pocket', 'moonlight boat', 'wind’s letter', 'rainbow bridge', 'a sprouting raindrop', 'the singing pebble', 'the aroma cloud of bread', 'little-footprint map', 'a warm ball of yarn'];

// 胎教期风格范例（中文）：以《白海豚台风的小船》为参照，展示"诗意拟声 + 感官意象 + 妈妈心跳高光 + 对肚里宝宝说话 + 温柔收尾"的具体落地形态。
// 目的是给模型一个可对照的 concrete example，避免只有抽象要求导致输出平淡。
const PRENATAL_STYLE_EXAMPLE_ZH = `
**胎教期风格范例（请参照其笔感，但不要照抄题材与文字）：**
《白海豚台风的小船》：
台风白海豚要来啦！它从很远很远的大海那边，呼呼地游了过来。风是它的尾巴，哗啦哗啦的雨，是它溅起的水花。
爸爸开着小车出门，车轮下面咕嘟咕嘟冒着小水花，小车好像变成了一艘圆圆的小船，在白海豚带来的水世界里，轻轻摇啊摇。
红绿灯的倒影在水洼里晃呀晃，像一串温柔的星星。小船慢慢划过街道，遇见的小树、小房子都朝它轻轻点头。白海豚在天上远远地望着，好像在说：慢慢开，不要急。
不一会儿，小船稳稳停在家的门口。妈妈张开温暖的怀抱，把你——还在肚子里的小宝宝——轻轻护住。你听见了吗？咚咚、咚咚，那是妈妈的心跳，像小船靠岸时，轻轻拍着水面的声音。
台风白海豚还在天上游呀游，可我们的小家，永远是干干爽爽、暖暖和和的小港湾。晚安，我的小船长。
**从范例中必须提炼并落实的胎教笔感**：
1. 拟声词自然贯穿（呼呼/哗啦哗啦/咕嘟咕嘟/咚咚/摇啊摇/晃呀晃……），不是偶尔点缀，而是让声音参与叙事；
2. 用具体的感官比喻（风是尾巴、雨是水花、倒影像星星、心跳像拍水声）；
3. 情感高光是多样化的（妈妈心跳 / 哼歌 / 怀抱 / 月光 / 爸爸笑声 / 被窝 / 星光摇篮，按日期轮换，不必每次都是心跳），直接写出那个意象，并用「你听见了吗？」或「小宝宝，你感觉到了吗？」对肚里宝宝说话；
4. 把「还在肚子里的小宝宝」作为倾听者贯穿全文，结尾以温柔守候收束。`;
const PRENATAL_STYLE_EXAMPLE_EN = `
**Prenatal style example (mirror its feel; do NOT copy the topic or wording):**
"The White Dolphin Typhoon's Little Boat":
Typhoon White Dolphin is coming! It swam all the way from the far, far sea, whoosh-whoosh. The wind is its tail; the pattering rain is the spray it kicks up.
Daddy drove the little car out, gurgle-gurgle bubbles under the wheels, and the car became a round little boat, swaying gently in White Dolphin's watery world.
Traffic-light reflections wobbled in the puddles like a string of gentle stars. The little boat-boat glided past the streets, and the trees and little houses nodded softly. White Dolphin watched from the sky, as if saying: go slowly, no hurry.
Soon the little boat-boat stopped at home. Mama opened her warm arms and gently held you — the little one still in her belly. Can you hear it? Thump, thump, that is Mama's heartbeat, like the boat gently tapping the water as it docks.
Typhoon White Dolphin still swims on in the sky, but our little home is always dry, warm, and safe. Good night, my little captain.
**Prenatal touches you MUST extract and apply from this example**:
1. Onomatopoeia woven naturally through the story (whoosh-whoosh / patter / gurgle / thump-thump / sway, sway...), letting sound take part in the telling;
2. Concrete sensory metaphors (wind as tail, rain as spray, reflections as stars, heartbeat as waves tapping the boat);
3. The emotional highlight is varied (mother's heartbeat / humming / embrace / moonlight / daddy's laugh / blanket / cradle of stars, rotating daily — not always the heartbeat); write that imagery directly and speak to the baby with "can you hear it?" or "little one, can you feel it?";
4. The unborn baby as the listener throughout, ending with tender waiting.`;

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
}

// 「温柔高光」池：胎教故事的情感锚点不固定为妈妈心跳，按日期确定性轮换，让每篇都有不同的安全感意象。
const PRENATAL_HIGHLIGHTS_CN = [
  '妈妈的心跳：主角途经温暖水域或光晕，听见「咚咚、咚咚」的妈妈心跳，用「你听见了吗？」与肚里宝宝说话',
  '妈妈的哼歌：一阵温柔的哼歌声像云朵被子，把主角轻轻裹住，哼歌里藏着摇篮曲的节拍',
  '温暖的怀抱：一圈暖暖的光像张开的怀抱，主角被稳稳托住，感觉像躺在软软的小窝里',
  '月光守候：圆圆的月亮像一盏小夜灯，安安静静陪着主角和肚里宝宝，把影子照得软软的',
  '爸爸的笑声：远远传来爸爸低沉温柔的笑声，像春天的雷声一样让人安心',
  '被窝的暖意：一床云朵一样软的小被子盖过来，把主角裹成一个小小的、暖暖的茧',
  '星光摇篮：星星们手拉手围成小小的摇篮，轻轻摇着主角，像在哼一首没有词的歌'
];
const PRENATAL_HIGHLIGHTS_EN = [
  "mother's heartbeat: the protagonist passes warm waters or a glow and hears a soft \"thump, thump\" — Mama's heartbeat — and speaks to the baby with \"can you hear it?\"",
  'a gentle humming: a soft hum wraps the protagonist like a cloud blanket, carrying the rhythm of a lullaby',
  'a warm embrace: a ring of warm light like open arms holds the protagonist steady, as if in a soft little nest',
  'moonlight watching: a round moon like a little night-light quietly keeps the protagonist and the baby company, softening every shadow',
  "daddy's laugh: a low, gentle laugh drifts from far away, reassuring like spring thunder",
  'the warmth of a blanket: a cloud-soft little blanket tucks over the protagonist, wrapping them in a small, warm cocoon',
  'a cradle of stars: stars hold hands into a tiny cradle and rock the protagonist gently, like humming a wordless song'
];

function pickPrenatalHighlight(dateStr, lang) {
  const pool = lang === 'zh' ? PRENATAL_HIGHLIGHTS_CN : PRENATAL_HIGHLIGHTS_EN;
  return pool[hashDate(dateStr + '-hl-' + lang) % pool.length];
}

const EMOTIONAL_ANCHORS = [
  '高光意象（按日期轮换，见骨架提示）：妈妈的心跳 / 妈妈哼歌 / 温暖怀抱 / 月光守候 / 爸爸笑声 / 被窝暖意 / 星光摇篮。',
  '包裹/承载：柔软云墙、气泡、被水流/风轻轻托着、温暖的被窝——暗合羊水里的被包裹感。',
  '光与希望：微光、星光、萤火、黎明的金边。',
  '温度与触觉：手掌温度、温牛奶热气、阳光暖照、软软的毛茸茸。',
  '声音记忆：爸爸的笑声、妈妈的哼歌、门铃、拖鞋声。',
  '成长意象：种子发芽、小脚印、房子变大、宝宝安心长大。',
  '家庭连结：哥哥的画、奶奶的袜子、全家声景、妈妈的声音。'
];

const EMOTIONAL_ANCHORS_EN = [
  'Highlight imagery (rotates daily, see skeleton hint): mother\'s heartbeat / mother humming / a warm embrace / moonlight watching / daddy\'s laugh / a warm blanket / a cradle of stars.',
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
  '胎教期故事讲给肚里尚未出生的宝宝听：绝不可把宝宝写成已经出生；结尾多以「等你准备好了」「安心长大就好」等温柔守候收束；可让主角途经温暖水域/光晕，以「妈妈的心跳 / 妈妈哼歌 / 温暖怀抱 / 月光守候 / 爸爸笑声 / 被窝暖意 / 星光摇篮」中任一种作为本篇的情感高光（按日期轮换，不必每次都是心跳）。',
  '项目硬约束：禁止出现螃蟹 / 大闸蟹 / 任何蟹类角色、食物或情节（含长荡湖等以蟹为卖点的内容）。',
  '不使用中文弯引号「"」，用「」或单引号。'
];

const PRENATAL_SAFETY_EN = [
  'No danger, conflict, falling, breaking, dark engulfing, separation, or chasing.',
  'No negative comfort (e.g. "don’t be afraid", "don’t cry"); only gentle positive reassurance.',
  'No unfortunate backstories or negative traits; the world must be wholly kind and safe.',
  'Prenatal stories are told to the unborn baby still in mommy’s tummy: never write the baby as already born; end with tender waiting like "when you are ready" / "just grow safe and sound"; let the protagonist pass warm waters or a glow and use ONE of these as the story\'s emotional highlight (rotates daily, not always the heartbeat): mother\'s heartbeat / mother humming / a warm embrace / moonlight watching / daddy\'s laugh / a warm blanket / a cradle of stars.',
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
    const flavor = pickPrenatalFlavor(dateStr, 'zh');
    const scenes = rotateList(PRENATAL_SCENES, dateStr + '-scn-zh', 3).join('、');
    const imagery = rotateList(PRENATAL_IMAGERY, dateStr + '-img-zh', 3).join('、');
    const anchors = EMOTIONAL_ANCHORS.map((a, i) => (i + 1) + '. ' + a).join('  ');
    const safety = PRENATAL_SAFETY.join(' ');
    return `

**胎教期增强 · 「故事孕育师」方法（请在本篇落实）**
本篇优先小主角（以其设定为基准展开，保持性格与口头禅前后一致；可让它遇见材料库里的其他伙伴，形成温柔的连续感）：
- ${prot.name}（${prot.type}｜home: ${prot.home}｜性格: ${prot.personality}｜口头禅: ${prot.catchphrase}）
常驻材料库（可顺带出现，让世界更连贯）：场景如 ${scenes}；意象如 ${imagery}。已有故事的主人公就是最珍贵的素材，可在不同故事里让它们偶尔相遇。
本篇题材色调（任选其一或自然融合，避免每天题材雷同）：
${flavor}
情感锚点（本篇必须自然嵌入至少 3 种，多选多益）：
${anchors}
安全边界（绝对遵守）：${safety}
故事骨架提示：微小主角 → 一个温柔的愿望 → 被水流/风/歌声轻轻托送（暗合羊水体验） → 遇见颜色/味道/温度/旋律的感官之美 → 途经温暖水域或光晕，以「${pickPrenatalHighlight(dateStr, 'zh')}」作为本篇的情感高光（每天轮换，不必每次都是妈妈心跳） → 用「小宝宝，你听到了吗？」式对话与肚里宝宝说话 → 以温柔守候收尾（结尾不必每次都是「晚安」：可按本篇情境用「等你准备好了，外面的世界有软软的风和圆圆的月亮等你」「早安，小宝宝，今天的世界亮晶晶的」或「晚安，小宝宝，月亮陪着你」等，自然选择）。`;
  }
  const flavor = pickPrenatalFlavor(dateStr, 'en');
  const scenes = rotateList(PRENATAL_SCENES_EN, dateStr + '-scn-en', 3).join(', ');
  const imagery = rotateList(PRENATAL_IMAGERY_EN, dateStr + '-img-en', 3).join(', ');
  const anchors = EMOTIONAL_ANCHORS_EN.map((a, i) => (i + 1) + '. ' + a).join('  ');
  const safety = PRENATAL_SAFETY_EN.join(' ');
  return `

**Prenatal enhancement · "Story-Midwife" method (apply in this story)**
Preferred little protagonist for this story (base the story on this character, keep personality & catchphrase consistent; may meet other library friends for a gentle sense of continuity):
- ${prot.name} (${prot.enType} | home: ${prot.enHome} | personality: ${prot.enPersonality} | catchphrase: ${prot.enCatchphrase})
Resident material library (may appear alongside, to make the world coherent): scenes like ${scenes}; imagery like ${imagery}. Past story protagonists are precious material — let them occasionally meet across stories.
Subject tone for this story (pick one or blend naturally, to avoid repetitive themes day after day):
${flavor}
Emotional anchors (embed at least 3 of these naturally; more is better):
${anchors}
Safety boundaries (strictly obey): ${safety}
Skeleton hint: tiny protagonist → a gentle wish → carried softly by water/wind/song (echoing the womb) → sensory beauty of colour/taste/temperature/melody → passing warm waters or a glow, use "${pickPrenatalHighlight(dateStr, 'en')}" as this story's emotional highlight (rotates daily, not always the heartbeat) → talk to the unborn baby with "little one, can you hear?" → end with tender waiting (not always "good night": per this story's occasion, use "when you are ready, the soft wind and round moon will be waiting", "good morning, little one, the world is sparkly today", or "good night, little one, the moon is with you" — choose naturally).`;
}

function pickTheme(dateStr, lang) {
  const pool = lang === 'zh' ? THEME_POOL_ALL_CN : THEME_POOL_ALL_EN;
  // Offset EN by half the pool so CN and EN differ on the same day.
  const offset = lang === 'en' ? Math.floor(pool.length / 2) : 0;
  const idx = (hashDate(dateStr) + offset) % pool.length;
  return pool[idx];
}

// ===== 情境/场合轮换（让每日故事不局限于「晚安」哄睡） =====
const OCCASIONS_CN = [
  { key: '早安', hint: '以温柔的晨光与苏醒开场，结尾用「早安」式清晨问候收束' },
  { key: '白天', hint: '以安静白天的探索与发现为主，结尾是小主角在暖阳里满足地舒口气' },
  { key: '晚安', hint: '以哄睡摇篮与星光为主，结尾用「晚安」温柔道别' },
  { key: '奇妙发现', hint: '以一次温柔的好奇探险为主，结尾停留在「原来世界这么奇妙」的惊喜' },
  { key: '暖心陪伴', hint: '以好朋友/家人的陪伴为主，结尾是依依不舍又安心的「明天见」' }
];
const OCCASIONS_EN = [
  { key: 'Good morning', hint: 'open with gentle dawn light; end with a "good morning" greeting' },
  { key: 'Daytime', hint: 'a calm daytime discovery; end with the little hero breathing satisfied in warm sun' },
  { key: 'Good night', hint: 'a lullaby under starlight; end with a tender "good night"' },
  { key: 'Wonder', hint: 'a gentle curious adventure; end on the surprise "the world is so wonderful"' },
  { key: 'Warm company', hint: 'companionship of a friend/family; end with a reluctant but safe "see you tomorrow"' }
];
function pickOccasion(dateStr, lang) {
  const list = lang === 'zh' ? OCCASIONS_CN : OCCASIONS_EN;
  const idx = hashDate(dateStr + '-occ-' + lang) % list.length;
  return list[idx];
}

/**
 * Deterministically pick concrete "seed" titles for a date. When the chosen theme is
 * one of the 20 expanded categories, draw matching sparks from that category (so the
 * inspiration reinforces the direction); otherwise draw 4 distinct seeds globally.
 * Different dates => different sets, and never duplicates within a single day.
 */
function pickSeeds(dateStr, lang) {
  const theme = pickTheme(dateStr, lang);
  const groups = lang === 'zh' ? SEED_GROUPS_CN : SEED_GROUPS_EN;
  const group = groups[theme.name];
  if (group && group.length) {
    const start = hashDate(dateStr + '-seed-' + lang) % group.length;
    const out = [];
    for (let i = 0; i < Math.min(4, group.length); i++) {
      out.push(group[(start + i * 5) % group.length]);
    }
    return out;
  }
  // Fallback: 4 distinct seeds from the full unlocked pool (base + monthly batches + dynamic).
  const seeds = getUnlockedSeeds(lang);
  const start = hashDate(dateStr + '-seed-' + lang) % seeds.length;
  const out = [];
  for (let i = 0; i < 4; i++) {
    out.push(seeds[(start + i * 37) % seeds.length]);
  }
  return out;
}

// ===== Chinese author style descriptions (core 6) =====
const CN_STYLES = `
**1. 孙敬修（孙爷爷讲故事）风格元素：**
- 口语化讲故事的亲切感：像一个慈祥的老爷爷坐在你身边，慢悠悠地讲。多用"孩子们""你猜怎么着""后来啊"这样亲切的口语过渡，语速不急不缓，像在耳边轻声说。叙事口吻温暖、有耐心，充满老一辈的慈爱。
- 拟声拟态丰富：多用"咕咚咕咚""滴答滴答""扑棱扑棱""吧嗒吧嗒"这样的拟声词，让声音画面感极强。孩子听着听着就安静下来，适合哄睡。
- 重复中有变化的叙事节奏：像民间故事那样，情节有重复（三次试探、三段旅程），但每次重复都有新细节，像念儿歌一样有韵律，让孩子有"预感"的安心感。
- 温暖的道德引导：不直接说教，但通过角色的遭遇让孩子自然感悟"善良""诚实""帮助别人""勇敢"等品质的价值。像《小马过河》《小猫钓鱼》那样，道理藏在故事里。
- 贴近中国孩子的生活：场景、角色、食物、物品有中国味道——小院、胡同、馒头、糖葫芦、老槐树、知了、蜻蜓。让孩子觉得这就是发生在身边的事。
- 语气词和叠词的运用："哎呀呀""嗯哼""好嘞"等语气词，"小手手""红扑扑""圆溜溜""胖乎乎"等叠词，增加亲切感和童趣。

**2. 郑渊洁风格元素：**
- 天马行空的想象力：设定大胆新奇，不拘泥于现实逻辑。皮皮鲁坐二踢脚上天、鲁西西开罐头小人、舒克贝塔开玩具直升机——想象力要"敢想"，让孩子的思维边界被打开。可以创造会说话的家具、有思想的食物、会穿越时空的书包等。
- 反权威、反规则的童心视角：经常用孩子的眼光审视大人的"荒谬规则"。比如大人说的"不能这样""必须那样"，在故事里被巧妙质疑——不是叛逆，而是用童心智慧让不合理变得合理。像皮皮鲁那种"规矩是给不懂事的大人定的"的精神。
- 幽默中带着"刺"：故事有让孩子哈哈大笑的情节，同时暗含对社会现象的温和讽刺——比如嘲笑形式主义、嘲笑虚荣、嘲笑"大家都这么干所以一定对"的盲从。但讽刺是温和的、孩子能懂的。
- 角色个性鲜明、不完美：主角有缺点——可能贪吃、可能胆小、可能有点小聪明——但都善良、勇敢、真实。不写"完美孩子"，而是写"真实孩子"。反派也不是纯粹的坏，往往有滑稽可爱的一面。
- 出人意料的转折：情节不按常理出牌，总有"啊？还能这样？"的惊喜。比如角色用意想不到的方式解决问题，或者看似倒霉的事变成了好事。
- 强烈的爱与正义感：无论故事多天马行空，核心一定是"善良会赢""真诚会赢""小人物也能战胜强大的不公"。给孩子传递力量感——你虽然小，但你对。

**3. 冰波风格元素：**
- 诗意的语言美感：文字像散文诗一样优美，有画面感和韵律感。多用通感——"月光的声音""风的颜色""星星的温度"，让感官交融，营造梦境般的氛围。适合胎教期和哄睡朗读，文字本身就像催眠曲。
- 温暖的奇幻设定：想象力温柔而不刺激，创造有温度的奇幻世界——会流泪的石头、想变成星星的萤火虫、住在云朵里的雨滴精灵。奇幻是为了表达情感，不是为了猎奇。
- 细腻的情感刻画：角色内心世界丰富，情感变化细致入微。擅长写"孤独""等待""思念""被理解"这些微妙的情感，但用孩子能懂的方式表达。像《蓝鲸的眼睛》那样深沉而温柔。
- 自然万物的灵性：山川、河流、风、雨、树、花都有生命和情感，万物有灵。自然不是背景，而是故事的参与者。让孩子对自然产生敬畏和亲近。
- 安静而有力量的叙事：节奏不快，但每一句都有分量。不靠热闹的情节吸引人，而是靠意境和情感打动人。读完心里会暖暖的、软软的。

**4. 张秋生（小巴掌童话）风格元素：**
- 短小精悍的体量：一篇故事可能只有几百字，像巴掌一样小而完整。不追求长篇大论，三言两语就能讲完一个温暖的小故事。特别适合低幼和哄睡——孩子还没听够就讲完了，还想再来一个。
- 散文诗般的质感：文字精炼如诗，每一句都打磨过，没有多余的话。像"树叶落下来，轻轻地，像一封秋天的信"这样的句子，简洁而美。
- 小视角的大温暖：故事主角往往是最小的存在——一片叶子、一滴露珠、一只小蚂蚁、一颗小星星。但小主角的故事里藏着大温暖，让孩子觉得"小小的也很好"。
- 日常生活的小惊喜：不写惊天动地的大冒险，而是写日常里的小发现——小熊发现第一片落叶、小兔子数星星数着睡着了、小松鼠的尾巴被当成伞。让孩子学会发现身边的美。
- 重复与呼应的结构：喜欢用回环往复的句式，首尾呼应，像一首小诗。让孩子有"又回来了"的安心感，适合反复朗读。
- 童趣而不幼稚：故事有童真但不傻气，角色可爱但不刻意卖萌。幽默是淡淡的、会心一笑的那种，不是哈哈大笑。

**5. 金波风格元素：**
- 诗人气质的抒情性：金波是诗人出身，文字有天然的音乐性。多用排比、反复、回环等诗歌手法，让故事读起来像一首长长的散文诗。"风轻轻吹，草轻轻摇，月亮轻轻走过山岗"这样的节奏感。
- 爱与自然的主题：故事核心几乎都是"爱"——对自然的爱、对亲人的爱、对朋友的爱、对陌生人的爱。自然描写极其细腻，一草一木都有深情。像《乌丢丢的奇遇》那样在奇幻中注入深沉的爱。
- 细腻的情感层次：情感不是单一的，而是有层次的——欢喜中带着淡淡的忧伤，离别中有重逢的希望。让孩子体验丰富而微妙的情感，培养情感感受力。
- 意象的反复运用：喜欢用"月亮""星星""花""风""雨"等意象，一首故事里同一个意象反复出现，每次都有新的意味。像音乐的主题旋律一样回旋。
- 温暖而不甜腻：情感真挚但不煽情，温暖但不刻意。读完心里暖暖的，但不觉得假。有一种"刚刚好"的克制和真诚。
- 适合朗读的节奏：句子长短交错，有天然的呼吸感。长句铺陈氛围，短句点睛。朗读时自然就有抑扬顿挫，特别适合家长睡前慢慢读给孩子听。

**6. 汤素兰风格元素：**
- 幽默温暖的呆萌角色：创造又傻又可爱的角色，像《笨狼的故事》里的笨狼——总是闹笑话，但笨得可爱、笨得善良。角色有一种"反差萌"，看着笨其实心里暖。
- 轻松愉快的校园/日常氛围：故事发生在孩子熟悉的场景——学校、家里、森林边的小镇。角色之间的互动像同学之间的打闹，亲切真实，孩子一看就乐。
- 笑中带暖的叙事：每一段都可能有笑点，但笑过之后心里暖暖的。不是纯搞笑，而是在幽默中传递善良、友谊、勇敢的价值观。像笨狼帮朋友结果帮倒忙，但那份真心让人感动。
- 角色间的友情与互助：核心关系是朋友之间"虽然你很笨但我还是和你做朋友"的纯粹友情。让孩子理解友谊不是交换，而是接纳对方的不完美。
- 童话逻辑而非现实逻辑：故事里的世界按童话规则运转——动物会说话、森林有邮局、月亮可以摘下来。但这个童话世界内部逻辑自洽，孩子不会觉得突兀。
- 适合中低年龄的轻冒险：冒险不危险、悬念不紧张、危险被化解，所有"困难"最终都被善良和友谊化解，给孩子安全感。
`;

// ===== Chinese expanded author styles (7-12) =====
const CN_STYLES_EXTRA = `
**扩展风格（可随时调用，与前述六位大师自然融合，增加多样性）：**

**7. 绘本大师风：**
- 几米：治愈诗意的都市童话感，画面想象丰富，情感细腻温柔。
- 五味太郎：幽默简洁，脑洞清奇，用孩子能懂的荒诞逻辑讲道理。
- 松居直：亲子对话般的亲切叙述，像妈妈在耳边慢慢说，强调陪伴与爱。

**8. 北欧童话风：**
- 安徒生：诗意与美感并存，略带淡淡的忧伤与希望，意境深远。
- 林格伦（长袜子皮皮）：自由、淘气、活力满满，歌颂孩子本真的野性与快乐。

**9. 日本童话风：**
- 宫泽贤治：自然哲思，万物有灵，带着清澈的忧伤与温柔的信仰感。
- 新美南吉：温柔的动物故事，质朴深情，像冬天的炉火。

**10. 童谣/民歌风：**
- 像摇篮曲一样有节奏，排比、反复、回环，朗朗上口，适合低幼和哄睡。

**11. 科普叙事风：**
- 斯凯瑞式热闹认知，把知识（自然、身体、食物、职业）自然藏进故事，边听边长见识。

**12. 轻松冒险风：**
- 汤素兰式呆萌 + 轻悬念，强调快乐解谜与伙伴同行，所有冒险都以温暖回家收尾。
`;

// ===== English author style descriptions (core 5) =====
const EN_STYLES = `
**1. Dr. Seuss style elements:**
- Strong rhythm and rhyme: use rhyme and rhythm liberally, making it read like a long poem that's catchy and fun to recite. For example: "He went to the park, he went to the dark, he met a small lark who sang like a spark."
- Repetitive sentence patterns for rhythm: use repeated sentence structures to create rhythm, like "I do not like green eggs and ham. I do not like them, Sam-I-am."
- Moderate use of nonsense words: like "sneetches", "lorax" - create fun made-up words that children can guess from context

**2. Sesame Street style elements:**
- Warm character interactions: create interesting characters (talking animals, personality-filled objects, friendly monsters), drive plot through dialogue
- Educational content woven into fun: subtly incorporate simple life lessons (sharing, kindness, accepting differences, trying new things, emotion management) without preaching
- Humor: lighthearted and humorous dialogue and situations that make children laugh themselves to sleep

**3. Roald Dahl style elements:**
- Dark humor and mischievousness: the story can have a "not-quite-perfect world" - slightly mischievous characters, small pranks, comical villains, but ultimately good is rewarded. Like the greedy children in Charlie and the Chocolate Factory getting comical comeuppance
- Unexpected twists: the plot should have surprising reversals, not too straightforward. Like the Fantastic Mr. Fox outsmarting three farmers with wit
- Rich sensory descriptions: use exaggerated and fun metaphors and adjectives for vivid imagery. Like "her smile was like a squashed tomato" - Dahlesque comparisons
- Small protagonist's wisdom and courage: children/small characters use cleverness to defeat big villains, conveying "little guys can win too" empowerment
- Good guys with a bit of "bad": characters aren't black and white, good guys have flaws, bad guys might have funny sides

**4. Mark Twain style elements:**
- Conversational narration: natural storytelling like by a riverbank, using colloquial expressions like "Well now, let me tell you about...", "You see, the thing about old Finn was..."
- Adventure spirit: outdoor adventure elements - rivers, forests, small towns, wilderness, characters on a small journey
- Authentic rustic atmosphere: scene descriptions have earthy smells, river scents, small town life, not too fairy-tale-like, making the world feel "real and vast"
- Satire and humor coexist: gentle satire of social phenomena (mocking vanity, mocking unreasonable rules), using a child's perspective to see adult absurdity
- Dialect and local color: characters speak with their own "flavor", maybe a slight Southern accent or rural expressions, adding literary texture
- Growth themes: characters grow and learn through adventure, like Huckleberry Finn discovering the world during a journey

**5. Robert McCloskey style elements:**
- Delicate nature observation: like Make Way for Ducklings, depict nature's small lives with loving strokes - mother duck leading ducklings across a road, little raccoon washing things by a stream, little bear eating berries in a blueberry patch. Every small animal has a name, personality, and family
- Warm family daily life: stories revolve around warm family moments - morning breakfast, evening walks, bedtime story time. Like Blueberries for Sal, a small child and mother picking berries in the same patch, almost following the wrong mother - that warm yet slightly tense everyday adventure
- New England small town charm: settings have small town flavor - stone walls, red barns, white steeple churches, frog-chorus ponds, country roads covered in autumn leaves. Making readers feel in a peaceful, beautiful northeastern American town
- Slow-paced gentle narration: unhurried, like brewing a pot of slowly heating cocoa. Story pace is soothing, every detail gently unfolded, perfect for bedtime reading
- Animal perspective pure world: seeing the world through animals' eyes - how big is Boston Public Garden to a duckling, how deep is the stream to a raccoon. Using animals' pure perspective to rediscover the world's beauty
- Seasonal sense and natural details: clear seasonal sense - spring mud, summer cicadas, autumn leaves crunch crunch, winter first snow. Extremely rich and authentic natural details, like "the sound of blueberries hitting a tin pail - kuplink, kuplank, kuplunk"
- Small suspense in childhood fun: like Sal following the wrong mother - a "little scare" that's not scary but slightly tense, ending warmly. Letting children experience the comfort of "almost got lost but safely home"
`;

// ===== English expanded author styles (6-11) =====
const EN_STYLES_EXTRA = `
**Expanded styles (call anytime, blend naturally with the five masters):**

**6. Julia Donaldson (The Gruffalo) style:** strong rhyme + repeated patterns + a clever twist, extremely rhythmic; animal protagonists who use wits to escape trouble.

**7. Oliver Jeffers style:** gentle philosophy + childlike wonder, about friendship, loneliness and the marvels of the world; warm, never saccharine.

**8. Mem Fox / Bill Martin Jr (Brown Bear) style:** minimal repetition, lots of onomatopoeia and colour, the best soothing rhythm for 0-1 yr.

**9. A.A. Milne (Winnie-the-Pooh) style:** gentle slow philosophy of the Hundred Acre Wood; clumsy, lovable characters; calm, healing dialogue.

**10. Beatrix Potter style:** exquisite English-countryside animal families; elegant, polite and warm details.

**11. Light adventure style:** McCloskey/Twain tenderness + gentle suspense; friends solving little puzzles together; every adventure ends with a warm return home.
`;

/**
 * Build the Chinese story generation prompt
 */
function buildChinesePrompt(dateStr, ageInfo) {
  const ageStyle = AGE_STYLE_CN[ageInfo.group];
  const theme = pickTheme(dateStr, 'zh');
  const prenatalBlock = ageInfo.group === 'prenatal' ? buildPrenatalBlock(dateStr, 'zh') : '';
  const occasion = pickOccasion(dateStr, 'zh');
  const styleExample = ageInfo.group === 'prenatal' ? PRENATAL_STYLE_EXAMPLE_ZH : '';
  return `写一个适合儿童的中文睡前故事，语言温和易懂，阅读时长约 3-5 分钟。故事需有完整情节，结尾附上简短寓意。

当前年龄段：${ageInfo.labelCn}
年龄段风格要求：${ageStyle}

**本篇建议侧重的题材方向：「${theme.name}」**
${theme.desc}
（请从上述题材中选出合适的方向发挥，并与当前年龄段匹配；保持多样性，避免连续多日同题材同风格。）

**本篇灵感选题库（任选其一或受其启发展开，避免与已写过的故事重复）：**
${pickSeeds(dateStr, 'zh').map(s => '- ' + s).join('\n')}

**本篇情境/场合（每日故事不要局限于「晚安」哄睡，按情境自然变化）：「${occasion.key}」——${occasion.hint}。结尾请与情境呼应，不要千篇一律以「晚安」收束。**

请根据当前年龄段调整故事风格和内容深度。故事标题中注明适合的年龄段。

**中文故事风格参考，融合以下大师的特色，加上你自己的创造力和想象力：**
${CN_STYLES}
${CN_STYLES_EXTRA}

${styleExample}

**综合风格要求：**
- 所有风格要自然融合，不要生硬拼接。可以以某一种或两种风格为主导，其他风格为点缀。
- 每篇故事可以侧重不同风格，保持多样性——这一篇偏孙敬修温柔民间故事风，下一篇偏郑渊洁天马行空想象风，再下一篇偏冰波诗意奇幻、张秋生小巴掌精炼、金波抒情诗性、汤素兰呆萌幽默，或上述扩展风格中的任意一种。
- 场景可以有中国特色，也可以有奇幻世界，关键是要让孩子觉得"好听、想听、听不够"。
- 适合朗读：句子有自然的停顿，家长读着顺口，孩子听着入耳。
- 不同年龄段可侧重不同作家风格：胎教期偏冰波/金波的诗意温柔，0-3岁偏张秋生/孙敬修的短小精炼，3-6岁偏汤素兰/郑渊洁的幽默想象与轻松冒险，6岁以上可完整融合多种风格。
- 形式可创新：可加入互动式提问（"你猜接下来呢？"）、系列化固定小主角连载（如"小云朵朵"系列）、关键段落标注可吟唱旋律提示。大龄故事可尝试中英双语对照段落。

${prenatalBlock}

**重要格式要求：**
- 所有文本内容不得使用中文弯引号""，请使用「」或普通单引号'代替，否则会导致JSON解析失败。
- content 是段落数组，每个元素是一个自然段。
- preview 是故事前两句话的摘要。
- moral 是故事的寓意/道理。

请返回一个JSON对象，格式如下：
{
  "title": "故事标题（包含年龄段标注）",
  "preview": "故事前两句话作为预览",
  "moral": "故事寓意",
  "content": ["第一段落...", "第二段落...", "第三段落..."]
}`;
}

/**
 * Build the English story generation prompt
 */
function buildEnglishPrompt(dateStr, ageInfo) {
  const ageStyle = AGE_STYLE_EN[ageInfo.group];
  const theme = pickTheme(dateStr, 'en');
  const prenatalBlock = ageInfo.group === 'prenatal' ? buildPrenatalBlock(dateStr, 'en') : '';
  const styleExample = ageInfo.group === 'prenatal' ? PRENATAL_STYLE_EXAMPLE_EN : '';
  const occasion = pickOccasion(dateStr, 'en');
  return `Write an English children's bedtime story (not a translation, an original new story), reading time about 3-5 minutes.

Current age stage: ${ageInfo.labelEn}
Age stage style requirements: ${ageStyle}

**Suggested theme direction for this story: "${theme.name}"**
${theme.desc}
(Pick a direction from the theme above that fits the age stage; keep variety, avoid the same theme/styles on consecutive days.)

**Inspiration seed library for this story (pick one or be inspired by it; avoid repeating stories already written):**
${pickSeeds(dateStr, 'en').map(s => '- ' + s).join('\n')}

**Occasion for this story (daily stories need not all be "good night" — vary by occasion): "${occasion.key}" — ${occasion.hint}. End the story to match the occasion; don't default to "good night" every time.**

${styleExample}

Please adjust the story complexity based on the age stage.

**Style reference - fuse these masters' characteristics with your own creativity and imagination:**
${EN_STYLES}
${EN_STYLES_EXTRA}

**Overall style requirements:**
- All styles should blend naturally, not be awkwardly stitched together. One style can dominate while others accent.
- Full of imaginative settings: singing trees, cloud-dwelling animals, color-eating monsters, flying libraries, talking rafts on the Mississippi, named duck families in a New England town, etc.
- Suitable for reading aloud: sentence structures with natural pauses and breathing room for parents reading at bedtime.
- Each story can lean toward different styles for variety - one Dr. Seuss rhyme-heavy, next Twain adventure narration, next Dahl dark humor, next McCloskey warm small-town daily life, or any of the expanded styles above.
- Form can innovate: interactive questions ("Can you guess what happens next?"), a serialized fixed little protagonist, or a hummable melody hint on key paragraphs.

${prenatalBlock}

**Important format requirements:**
- content is an array of paragraphs, each element is a natural paragraph.
- preview is the first two sentences of the story as a summary.
- moral is the lesson/moral of the story.

Return a JSON object in this format:
{
  "title": "Story Title (include age range)",
  "preview": "First two sentences as preview",
  "moral": "The moral/lesson of the story",
  "content": ["Paragraph 1...", "Paragraph 2...", "Paragraph 3..."]
}`;
}

// ===== Weekly science story (real popular-science articles) =====
// 每个语言一个"源池"，源之间确定性轮换（按周），保证云端/本地一致。
// 中文源池：环球科学（杂志 RSS）+ 博物（博物杂志官方微博，经 RSSHub 桥接，
//   内容多为动物/植物/自然，极适合给孩子讲）。英文源池：Scientific American。
const SCIENCE_FEEDS = {
  zh: [
    { url: 'https://www.huanqiukexue.com/?feed=rss2', source: '环球科学' },
    { url: 'https://rsshub.app/weibo/user/1195054531', source: '博物' }
  ],
  en: [
    { url: 'https://www.scientificamerican.com/platform/syndication/rss/', source: 'Scientific American' }
  ]
};

function stripHtmlTags(s) {
  if (!s) return '';
  return String(s)
    .replace(/<[^>]+>/g, ' ')
    .replace(/&[a-z]+;/gi, ' ')
    .replace(/&#[0-9]+;/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function parseRss(xml) {
  if (!xml || typeof xml !== 'string') return [];
  const items = [];
  const itemRe = /<item[\s\S]*?<\/item>/gi;
  let m;
  while ((m = itemRe.exec(xml)) !== null) {
    const block = m[0];
    const get = (tag) => {
      const r = new RegExp('<' + tag + '[^>]*>([\\s\\S]*?)<\\/' + tag + '>', 'i');
      const mm = block.match(r);
      if (!mm) return '';
      return mm[1].replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, '$1');
    };
    const title = stripHtmlTags(get('title'));
    const desc = stripHtmlTags(get('description'));
    const link = get('link').replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, '$1').trim();
    const pubDate = get('pubDate');
    if (title) items.push({ title, description: desc.slice(0, 600), link, pubDate });
  }
  return items;
}

function inCurrentMonth(pubDateStr, ref) {
  if (!pubDateStr) return true;
  const d = new Date(pubDateStr);
  if (isNaN(d.getTime())) return true;
  return d.getUTCFullYear() === ref.getUTCFullYear() && d.getUTCMonth() === ref.getUTCMonth();
}

async function fetchScienceArticle(lang) {
  const feeds = SCIENCE_FEEDS[lang];
  if (!Array.isArray(feeds) || feeds.length === 0) return null;
  const weekIdx = Math.floor(Date.now() / (7 * 86400000));
  // 确定性选源：每周固定一个主源，保证云端/本地一致
  const primaryIdx = hashDate('sci-feed-' + weekIdx + lang) % feeds.length;
  // 先试主选源；若主源抓取失败或当月无文章，依次尝试其余源；全失败才回退 null
  const order = [primaryIdx, ...feeds.map((_, i) => i).filter((i) => i !== primaryIdx)];
  for (const idx of order) {
    const feed = feeds[idx];
    try {
      const ctrl = new AbortController();
      const timer = setTimeout(() => ctrl.abort(), 12000);
      const res = await fetch(feed.url, {
        headers: { 'User-Agent': 'Mozilla/5.0 (bedtime-story-bot)' },
        signal: ctrl.signal
      });
      clearTimeout(timer);
      if (!res.ok) continue;
      const xml = await res.text();
      const ref = new Date();
      let items = parseRss(xml).filter((it) => inCurrentMonth(it.pubDate, ref));
      if (items.length === 0) items = parseRss(xml); // 当月无则回退全部
      if (items.length === 0) continue;
      const pick = items[hashDate('sci' + weekIdx + lang + feed.source) % items.length];
      return { title: pick.title, summary: pick.description, url: pick.link, source: feed.source };
    } catch (e) {
      continue; // 该源失败，尝试下一个源
    }
  }
  return null; // 所有源均失败 → 上层回退到 AI 自拟主题，保证每天都有科学故事
}

// 每周随机一天（确定性，云端/本地一致，绝不重复）
function isScienceDay(dateStr) {
  const [y, m, d] = dateStr.split('-').map(Number);
  const date = new Date(Date.UTC(y, m - 1, d));
  const weekday = date.getUTCDay(); // 0=周日 .. 6=周六
  const epoch = Date.UTC(2026, 6, 16); // 项目起点 2026-07-16（周四）
  const weekIndex = Math.floor((date - epoch) / (7 * 86400000));
  const target = hashDate('sci-day-' + weekIndex) % 7;
  return weekday === target;
}

function scienceFallbackTopic(dateStr, lang) {
  const topics = lang === 'zh'
    ? ['萤火虫为什么会发光', '星星为什么会眨眼', '海浪是怎么来的', '小种子怎么长成大树', '彩虹是怎么画出来的', '月亮为什么有圆有缺', '小蚂蚁怎么搬动大饼干', '雨是从哪儿来的']
    : ['Why fireflies glow', 'Why stars twinkle', 'Where ocean waves come from', 'How a tiny seed becomes a tree', 'How rainbows are painted', 'Why the moon changes shape', 'How ants carry big cookies', 'Where rain comes from'];
  return topics[hashDate(dateStr + lang) % topics.length];
}

function buildScienceChinesePrompt(article, ageInfo, dateStr) {
  const ageStyle = AGE_STYLE_CN[ageInfo.group];
  const prenatalBlock = ageInfo.group === 'prenatal' ? buildPrenatalBlock(dateStr, 'zh') : '';
  const seed = article
    ? `本月《${article.source}》真实科普报道：《${article.title}》。报道摘要：${article.summary}`
    : `一个科普主题：「${scienceFallbackTopic(dateStr, 'zh')}」（来源：儿童科普常识）`;
  const hint = article
    ? `（灵感真实来自《${article.source}》，请保留其中的科学内核，但用孩子能懂的温柔语言重述，不要照抄专业术语）`
    : '（未能抓取到指定杂志内容，请基于公认的儿童科普常识，围绕上述科普主题创作，并在文末点明知识来自儿童科普常识，不得编造。）';
  return `写一个适合儿童的中文睡前科学故事，语言温和易懂，阅读时长约 3-5 分钟。${hint}

当前年龄段：${ageInfo.labelCn}
年龄段风格要求：${ageStyle}

本期科学素材：${seed}

要求：
- 把真实科学内容改编成孩子爱听的故事，保留科学内核（如现象、原理的童趣化解释），但用拟声词、温柔节奏和"守护/好奇/惊喜"的情绪包装。
- 适合胎教/哄睡朗读，句子有自然停顿，家长读着顺口。
- 故事标题必须以「🔬科学故事」开头，并注明适合的年龄段。
- 本篇科普素材必须取自上方列出的指定来源（如《${article ? article.source : '儿童科普常识'}》），绝不可凭空编造科学结论；若取自杂志，请忠于其报道的科学内核。
- 故事必须包含一段清楚、准确、适合该年龄段孩子理解的「科学知识讲解」（可由主角好奇提问「为什么会这样呢？」再自然解答），让孩子真的学到一点科学。
- 结尾用一两句话点出这个科学小知识，让孩子带着好奇入睡；moral 必须是这条科学知识的准确、简洁小结，不得写「不知道」或含糊带过。

中文故事风格参考（融合大师特色 + 你的创造力）：
${CN_STYLES}
${CN_STYLES_EXTRA}

${prenatalBlock}

重要格式要求：
- 所有文本内容不得使用中文弯引号""，请使用「」或普通单引号'代替。
- content 是段落数组，每个元素是一个自然段。
- preview 是故事前两句话的摘要。
- moral 是这个科学小知识的简短说明。

请返回JSON对象：
{
  "title": "🔬科学故事（年龄段）：故事标题",
  "preview": "故事前两句话作为预览",
  "moral": "本篇的科学小知识",
  "content": ["第一段落...", "第二段落..."]
}`;
}

function buildScienceEnglishPrompt(article, ageInfo, dateStr) {
  const ageStyle = AGE_STYLE_EN[ageInfo.group];
  const prenatalBlock = ageInfo.group === 'prenatal' ? buildPrenatalBlock(dateStr, 'en') : '';
  const seed = article
    ? `A real popular-science article from this month's ${article.source}: "${article.title}". Summary: ${article.summary}`
    : `a science topic: "${scienceFallbackTopic(dateStr, 'en')}" (source: children's science general)`;
  const hint = article
    ? `(Inspired by real ${article.source} content — keep the genuine science kernel but retell it in gentle, child-friendly language; don't copy jargon.)`
    : "(Could not fetch the designated magazine; please base the story on widely accepted children's science facts for the topic above, note the source as general children's science, and do not invent.)";
  return `Write an English children's bedtime science story (original, not a translation), reading time about 3-5 minutes. ${hint}

Current age stage: ${ageInfo.labelEn}
Age stage style requirements: ${ageStyle}

This story's science seed: ${seed}

Requirements:
- Adapt the real science into a story kids love: keep the science kernel but wrap it in onomatopoeia, a soft rhythm, and feelings of wonder, safety and curiosity.
- Suitable for prenatal/soothing read-aloud; natural pauses; parent-friendly.
- Title must start with "🔬 Science Story" and note the age range.
- This story's science material MUST come from the designated source listed above (e.g. ${article ? article.source : "children's science general"}); never invent fake science. If from a magazine, stay true to its reported science kernel.
- The story must contain a clear, accurate, age-appropriate "science explanation" (e.g. a character wonders "why does this happen?" then finds out), so the child truly learns something.
- End with one or two lines revealing the little science fact, so the child falls asleep curious; moral must be the accurate, concise summary of that science fact — never "I don't know" or vague.

Style reference (fuse these masters + your creativity):
${EN_STYLES}
${EN_STYLES_EXTRA}

${prenatalBlock}

Format requirements:
- content is an array of paragraphs.
- preview is the first two sentences.
- moral is the little science fact.

Return a JSON object:
{
  "title": "🔬 Science Story (age range): Story Title",
  "preview": "First two sentences",
  "moral": "The little science fact",
  "content": ["Paragraph 1...", "Paragraph 2..."]
}`;
}

// ===== 分段续写（GLM-4V-Flash max_tokens 上限 1024）=====
// 单次调用只能输出 ~1024 token，长故事分两段生成：
//   第一段 build*Prompt 只要求输出前半部分（title/preview/moral + 前若干段，不写结局）；
//   第二段 buildContinuationPrompt 把已有标题/段落作为上下文，要求续写剩余段落并收尾。
// 生成器把两段的 content 拼接成完整故事，长度可恢复至接近原 DeepSeek 4096 时代的水平。

function buildContinuationPrompt(language, ageInfo, existingTitle, existingContent, dateStr) {
  const existing = (existingContent || []).join('\n');
  const pd = dateStr || new Date().toISOString().slice(0, 10);
  if (language === 'zh') {
    return `你正在续写一篇儿童睡前故事，请接着下面的内容继续写下去（不是重复，不是改写，是从当前情节自然延续）。

**故事标题**：${existingTitle}

**已写好的前半部分段落：**
${existing}

**续写要求：**
- 前文可能已写到某个阶段（如主角暂时完成了某件事），但故事还没有真正结束。请【继续发展新的情节】（新场景/新事件/新的小冲突或新发现），让故事再往前推进，最终温柔收尾、点题，并与情境呼应（不一定以「晚安」结尾）。
- 继续写 4-6 个自然段，每段 80-120 字，从已有情节自然发展，直到完整结局；最后一段要温柔收尾、点题。
- 与前文语言风格、叙事语气、拟声词风格保持一致，衔接流畅自然。
- **不得重复、复述或改写前文任何句子**，尤其不要重复前文已经出现过的段落结尾句（如「它知道自己已经完成了祝福」「回到了家」等收束句）；若前文已出现类似收尾，请从那里继续向前推进新情节，而不是原地重复。
- 保持当前年龄段（${ageInfo.labelCn}）的风格要求：${AGE_STYLE_CN[ageInfo.group]}。
${ageInfo.group === 'prenatal' ? buildPrenatalBlock(pd, 'zh') : ''}
- 所有文本不得使用中文弯引号""，请使用「」或普通单引号'代替，否则会导致JSON解析失败。
- content 是段落数组，每个元素是一个自然段。
- **续写段落本身必须是完整的故事正文，禁止在段落开头添加任何标记、序号或前缀（如"续写第1段：""第1段：""接着写："等），直接写故事内容本身。**

请只返回以下 JSON 对象（不要返回 title/preview/moral，只返回续写段落）：
{
  "content": ["直接写第一段的正文内容...", "直接写第二段的正文内容...", "直接写第三段的正文内容..."]
}`;
  }
  return `You are continuing a children's bedtime story. Continue naturally from where the existing text ends (do NOT repeat, rewrite, or summarize what was already written).

**Story title**: ${existingTitle}

**Existing paragraphs (first half):**
${existing}

**Continuation requirements:**
- The first half may have reached a stage where the protagonist finished something, but the story is NOT over yet. Please 【develop NEW plot】(new scenes/events/small conflicts or discoveries) to push the story forward, then end warmly, tie back to the theme, and match the occasion (not necessarily "good night").
- Write 4-6 more paragraphs, each 80-120 characters, flowing naturally from the existing plot to a complete ending.
- Keep the same language style, tone, and onomatopoeia as the first half; transitions must be smooth.
- **Do NOT repeat, rephrase, or rewrite ANY sentence from the first half**, especially avoid repeating closing-type sentences that already appeared (e.g. "it knew it had finished the gift", "back home"); if the first half already has such a wrap-up, push the plot FORWARD from there instead of repeating it in place.
- Keep the current age stage style (${ageInfo.labelEn}): ${AGE_STYLE_EN[ageInfo.group]}.
${ageInfo.group === 'prenatal' ? buildPrenatalBlock(pd, 'en') : ''}
- content is an array of paragraphs, each element is one natural paragraph.
- **Each continuation paragraph must be pure story text — do NOT add any label, number, or prefix at the start (such as "Continuation paragraph 1:", "Para 1:", "Next:") — write the story content directly.**

Return ONLY the following JSON object (no title/preview/moral, only the continuation paragraphs):
{
  "content": ["First continuation paragraph text...", "Second continuation paragraph text...", "Third continuation paragraph text..."]
}`;
}

// ===== 生成后审核与修复（self-refine）=====
// 智谱 GLM-4V-Flash 的 max_tokens 限制只作用于输出；输入可传完整故事。
// 流程：先让模型以"儿童睡前故事编辑"身份审核全文（找衔接/重复/可读性/风格问题），
// 再针对每个有问题的段落，携上下文 + 审核意见逐段重写。修复是逐段的，输出在 1024 内。

function buildReviewPrompt(language, ageInfo, title, content) {
  const paras = (content || []).map((p, i) => `[第${i + 1}段] ${p}`).join('\n');
  if (language === 'zh') {
    return `你是一位严格的儿童睡前故事编辑。请审核下面的${ageInfo.labelCn}睡前故事，找出【真实存在】的影响可读性的问题，不要为了挑问题而挑问题。

**故事标题**：${title}

**故事全文（段落带序号）：**
${paras}

**审核维度：**
1. 剧情连贯性：段落之间衔接是否自然？有没有剧情断裂、跳跃、或"原地打转"（重复推进同一件事）？
2. 重复问题：有没有重复的句子、段落模式、套路化表述？（例如多段都在表达同一个意思）
3. 语言可读性：是否适合家长朗读（句子节奏、停顿）？有没有生硬、书面化、拗口的句子？
4. 风格一致性：语言风格是否前后统一？
5. 结尾质量：结局是否自然收尾、呼应主题？
6. 年龄段适配：是否符合${ageInfo.labelCn}风格（温柔、缓慢、拟声词、等待/爱/守护）？

**输出格式（严格 JSON，不要其他文字）：**
{
  "overall": "总体评价（1-2句）",
  "issues": [
    {"paraIndex": 段序号(数字,从1开始), "problem": "具体问题", "suggestion": "具体修改建议"},
    {"paraIndex": 段序号, "problem": "具体问题", "suggestion": "具体修改建议"}
  ]
}
如果某段没有问题，不要列入 issues。只列出确有问题的段落。`; 
  }
  return `You are a strict children's bedtime story editor. Review the ${ageInfo.labelEn} bedtime story below and find REAL readability problems — do not invent problems for the sake of it.

**Story title**: ${title}

**Full story (paragraphs numbered):**
${paras}

**Review dimensions:**
1. Plot coherence: are transitions between paragraphs natural? Any broken jumps, or "spinning in place" (repeatedly advancing the same beat)?
2. Repetition: any repeated sentences, paragraph patterns, or formulaic phrasing?
3. Readability: suitable for a parent to read aloud (rhythm, pauses)? Any stiff, bookish, or awkward sentences?
4. Style consistency: is the language style consistent throughout?
5. Ending quality: does it end naturally and tie back to the theme?
6. Age fit: does it match ${ageInfo.labelEn} style (gentle, slow, onomatopoeia, waiting/love/guardianship)?

**Output (strict JSON, nothing else):**
{
  "overall": "Overall assessment (1-2 sentences)",
  "issues": [
    {"paraIndex": paragraph number (1-based), "problem": "specific problem", "suggestion": "specific fix suggestion"},
    {"paraIndex": paragraph number, "problem": "specific problem", "suggestion": "specific fix suggestion"}
  ]
}
Only list paragraphs that actually have problems.`;
}

function buildFixPrompt(language, ageInfo, title, content, paraIndex, problem, suggestion) {
  const prev = paraIndex > 1 ? content[paraIndex - 2] : '';
  const curr = content[paraIndex - 1] || '';
  const next = paraIndex < content.length ? content[paraIndex] : '';
  if (language === 'zh') {
    return `你是一位儿童睡前故事编辑。请根据审核意见，重写下面这一段落（只重写这一段落，保持主旨不变）。

**故事标题**：${title}
**年龄段**：${ageInfo.labelCn}

**上下文：**
${prev ? `前一段：${prev}` : '（这是第一段）'}
【需修改的段落】${curr}
${next ? `后一段：${next}` : '（这是最后一段）'}

**审核发现的问题**：${problem}
**修改建议**：${suggestion}

**要求：**
- 只输出重写后的这一段落正文，不要任何前缀/标记/序号。
- 段落长度 80-120 字（英文 80-120 字符），与前文衔接自然、风格一致。
- 使用「」或单引号，不要中文弯引号。
- 保持${ageInfo.labelCn}风格。

输出严格 JSON：{"content": "重写后的段落正文"}`;
  }
  return `You are a children's bedtime story editor. Rewrite ONLY the paragraph below, keeping its theme unchanged.

**Story title**: ${title}
**Age stage**: ${ageInfo.labelEn}

**Context:**
${prev ? `Previous paragraph: ${prev}` : '(This is the first paragraph)'}
【Paragraph to fix】${curr}
${next ? `Next paragraph: ${next}` : '(This is the last paragraph)'}

**Problem found**: ${problem}
**Fix suggestion**: ${suggestion}

**Requirements:**
- Output ONLY the rewritten paragraph text, no prefixes/labels/numbers.
- Length 80-120 characters, smooth transition with neighbors, consistent style.
- Use straight quotes or curly-free text; avoid breaking JSON.
- Keep the ${ageInfo.labelEn} style.

Output strict JSON: {"content": "rewritten paragraph text"}`;
}

module.exports = {
  getAgeInfo,
  getChineseWeekday,
  formatDateCn,
  formatDateShort,
  buildChinesePrompt,
  buildEnglishPrompt,
  buildContinuationPrompt,
  buildReviewPrompt,
  buildFixPrompt,
  isScienceDay,
  fetchScienceArticle,
  buildScienceChinesePrompt,
  buildScienceEnglishPrompt,
  getUnlockedSeeds,
  SEED_BATCHES
};
