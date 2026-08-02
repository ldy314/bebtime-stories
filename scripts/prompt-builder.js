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
 */

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
  { name: '爱与善良', desc: '温暖人心——流浪猫的新家、给老人的椅子、分享的午餐、雨中的伞、最后的晚安、帮妈妈捶背。' }
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
  'The stray cat\'s new home', 'The seat for the old lady', 'The shared lunch', 'The umbrella in the rain', 'The final goodnight',   'Rubbing Mom\'s back'
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

/**
 * Pick the broad theme direction for a date (rotates across the full 26-theme pool).
 */
function pickTheme(dateStr, lang) {
  const pool = lang === 'zh' ? THEME_POOL_ALL_CN : THEME_POOL_ALL_EN;
  // Offset EN by half the pool so CN and EN differ on the same day.
  const offset = lang === 'en' ? Math.floor(pool.length / 2) : 0;
  const idx = (hashDate(dateStr) + offset) % pool.length;
  return pool[idx];
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
  // Fallback for the 6 original broad themes: 4 distinct global seeds.
  const seeds = lang === 'zh' ? CONCRETE_SEEDS_CN : CONCRETE_SEEDS_EN;
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
  return `写一个适合儿童的中文睡前故事，语言温和易懂，阅读时长约 3-5 分钟。故事需有完整情节，结尾附上简短寓意。

当前年龄段：${ageInfo.labelCn}
年龄段风格要求：${ageStyle}

**本篇建议侧重的题材方向：「${theme.name}」**
${theme.desc}
（请从上述题材中选出合适的方向发挥，并与当前年龄段匹配；保持多样性，避免连续多日同题材同风格。）

**本篇灵感选题库（任选其一或受其启发展开，避免与已写过的故事重复）：**
${pickSeeds(dateStr, 'zh').map(s => '- ' + s).join('\n')}

请根据当前年龄段调整故事风格和内容深度。故事标题中注明适合的年龄段。

**中文故事风格参考，融合以下大师的特色，加上你自己的创造力和想象力：**
${CN_STYLES}
${CN_STYLES_EXTRA}

**综合风格要求：**
- 所有风格要自然融合，不要生硬拼接。可以以某一种或两种风格为主导，其他风格为点缀。
- 每篇故事可以侧重不同风格，保持多样性——这一篇偏孙敬修温柔民间故事风，下一篇偏郑渊洁天马行空想象风，再下一篇偏冰波诗意奇幻、张秋生小巴掌精炼、金波抒情诗性、汤素兰呆萌幽默，或上述扩展风格中的任意一种。
- 场景可以有中国特色，也可以有奇幻世界，关键是要让孩子觉得"好听、想听、听不够"。
- 适合朗读：句子有自然的停顿，家长读着顺口，孩子听着入耳。
- 不同年龄段可侧重不同作家风格：胎教期偏冰波/金波的诗意温柔，0-3岁偏张秋生/孙敬修的短小精炼，3-6岁偏汤素兰/郑渊洁的幽默想象与轻松冒险，6岁以上可完整融合多种风格。
- 形式可创新：可加入互动式提问（"你猜接下来呢？"）、系列化固定小主角连载（如"小云朵朵"系列）、关键段落标注可吟唱旋律提示。大龄故事可尝试中英双语对照段落。

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
  return `Write an English children's bedtime story (not a translation, an original new story), reading time about 3-5 minutes.

Current age stage: ${ageInfo.labelEn}
Age stage style requirements: ${ageStyle}

**Suggested theme direction for this story: "${theme.name}"**
${theme.desc}
(Pick a direction from the theme above that fits the age stage; keep variety, avoid the same theme/styles on consecutive days.)

**Inspiration seed library for this story (pick one or be inspired by it; avoid repeating stories already written):**
${pickSeeds(dateStr, 'en').map(s => '- ' + s).join('\n')}

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
  const seed = article
    ? `本月《${article.source}》真实科普报道：《${article.title}》。报道摘要：${article.summary}`
    : `一个科普主题：「${scienceFallbackTopic(dateStr, 'zh')}」`;
  const hint = article
    ? `（灵感真实来自《${article.source}》，请保留其中的科学内核，但用孩子能懂的温柔语言重述，不要照抄专业术语）`
    : '（未能抓取到当期杂志内容，请围绕这个科普主题创作）';
  return `写一个适合儿童的中文睡前科学故事，语言温和易懂，阅读时长约 3-5 分钟。${hint}

当前年龄段：${ageInfo.labelCn}
年龄段风格要求：${ageStyle}

本期科学素材：${seed}

要求：
- 把真实科学内容改编成孩子爱听的故事，保留科学内核（如现象、原理的童趣化解释），但用拟声词、温柔节奏和"守护/好奇/惊喜"的情绪包装。
- 适合胎教/哄睡朗读，句子有自然停顿，家长读着顺口。
- 故事标题必须以「🔬科学故事」开头，并注明适合的年龄段。
- 结尾用一两句话点出这个科学小知识，让孩子带着好奇入睡。

中文故事风格参考（融合大师特色 + 你的创造力）：
${CN_STYLES}
${CN_STYLES_EXTRA}

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
  const seed = article
    ? `A real popular-science article from this month's ${article.source}: "${article.title}". Summary: ${article.summary}`
    : `a science topic: "${scienceFallbackTopic(dateStr, 'en')}"`;
  const hint = article
    ? `(Inspired by real ${article.source} content — keep the genuine science kernel but retell it in gentle, child-friendly language; don't copy jargon.)`
    : '(Could not fetch the magazine; please write about this science topic.)';
  return `Write an English children's bedtime science story (original, not a translation), reading time about 3-5 minutes. ${hint}

Current age stage: ${ageInfo.labelEn}
Age stage style requirements: ${ageStyle}

This story's science seed: ${seed}

Requirements:
- Adapt the real science into a story kids love: keep the science kernel but wrap it in onomatopoeia, a soft rhythm, and feelings of wonder, safety and curiosity.
- Suitable for prenatal/soothing read-aloud; natural pauses; parent-friendly.
- Title must start with "🔬 Science Story" and note the age range.
- End with one or two lines revealing the little science fact, so the child falls asleep curious.

Style reference (fuse these masters + your creativity):
${EN_STYLES}
${EN_STYLES_EXTRA}

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

module.exports = {
  getAgeInfo,
  getChineseWeekday,
  formatDateCn,
  formatDateShort,
  buildChinesePrompt,
  buildEnglishPrompt,
  isScienceDay,
  fetchScienceArticle,
  buildScienceChinesePrompt,
  buildScienceEnglishPrompt
};
