/**
 * Prompt Builder for Bedtime Story Generation
 * Contains age group calculation and prompt assembly for Chinese & English stories
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
  const d = new Date(dateStr + 'T00:00:00+08:00');
  return weekdays[d.getDay()];
}

/**
 * Format date as "YYYY年M月D日"
 */
function formatDateCn(dateStr) {
  const d = new Date(dateStr + 'T00:00:00+08:00');
  return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`;
}

/**
 * Format date short as "MM/DD"
 */
function formatDateShort(dateStr) {
  const d = new Date(dateStr + 'T00:00:00+08:00');
  const mm = String(d.getMonth() + 1).padStart(2, '0');
  const dd = String(d.getDate()).padStart(2, '0');
  return `${mm}/${dd}`;
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

// ===== Chinese author style descriptions =====
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
- 适合中低年龄的轻冒险：冒险不危险、悬念不紧张、冲突不激烈。所有"困难"最终都被善良和友谊化解，给孩子安全感。
`;

// ===== English author style descriptions =====
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

/**
 * Build the Chinese story generation prompt
 */
function buildChinesePrompt(dateStr, ageInfo) {
  const ageStyle = AGE_STYLE_CN[ageInfo.group];
  return `写一个适合儿童的中文睡前故事，语言温和易懂，阅读时长约 3-5 分钟。故事需有完整情节，结尾附上简短寓意。

当前年龄段：${ageInfo.labelCn}
年龄段风格要求：${ageStyle}

请根据当前年龄段调整故事风格和内容深度。故事标题中注明适合的年龄段。

**中文故事风格参考，融合以下六位大师的特色，加上你自己的创造力和想象力：**
${CN_STYLES}

**综合风格要求：**
- 这六种风格要自然融合，不要生硬拼接。可以以某一种或两种风格为主导，其他风格为点缀。
- 每篇故事可以侧重不同风格，保持多样性。
- 场景可以有中国特色，也可以有奇幻世界，关键是要让孩子觉得"好听、想听、听不够"。
- 适合朗读：句子有自然的停顿，家长读着顺口，孩子听着入耳。
- 不同年龄段可侧重不同作家风格：胎教期偏冰波/金波的诗意温柔，0-3岁偏张秋生/孙敬修的短小精炼，3-6岁偏汤素兰/郑渊洁的幽默想象，6岁以上可完整融合六种风格。

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
  return `Write an English children's bedtime story (not a translation, an original new story), reading time about 3-5 minutes.

Current age stage: ${ageInfo.labelEn}
Age stage style requirements: ${ageStyle}

Please adjust the story complexity based on the age stage.

**Style reference - fuse these five masters' characteristics with your own creativity and imagination:**
${EN_STYLES}

**Overall style requirements:**
- These five styles should blend naturally, not be awkwardly stitched together. One style can dominate while others accent.
- Full of imaginative settings: singing trees, cloud-dwelling animals, color-eating monsters, flying libraries, talking rafts on the Mississippi, named duck families in a New England town, etc.
- Suitable for reading aloud: sentence structures with natural pauses and breathing room for parents reading at bedtime.
- Each story can lean toward different styles for variety - one Dr. Seuss rhyme-heavy, next Twain adventure narration, next Dahl dark humor, next McCloskey warm small-town daily life.

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

module.exports = {
  getAgeInfo,
  getChineseWeekday,
  formatDateCn,
  formatDateShort,
  buildChinesePrompt,
  buildEnglishPrompt
};
