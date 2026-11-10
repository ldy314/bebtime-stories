# -*- coding: utf-8 -*-
# 11-27 ~ 11-30
DEC6 = []

def S(id_, date, ds, title, lang, preview, moral, content, sci=False):
    d = {'id': id_, 'date': date, 'dateShort': ds, 'title': title, 'language': lang,
         'ageGroup': '0-1', 'ageLabel': '0-1岁', 'preview': preview, 'moral': moral,
         'content': content, 'category': 'science' if sci else 'regular'}
    if sci:
        d['series'] = 'science'; d['seriesTitle'] = '科学故事'
        d['source'] = 'Children science common sense' if lang == 'en' else '儿童科普常识'
    return d

# ---------- 11-27 周五 ----------
DEC6.append(S('2026-11-27-cn', '2026年11月27日 · 星期五', '11/27',
    '爸爸的低音歌（0-1岁）', 'zh',
    '晚上哄睡，爸爸唱起低低的摇篮曲。嗡——嗡——像大提琴，像远处的轮船。妈妈的歌像小鸟，爸爸的歌像大船，宝宝的眼睛，在大船的摇晃里慢慢闭上。',
    '每个人的声音都不一样，每一样都好听。低低的爸爸歌，有大大安心的力量。',
    ['晚上，房间暗下来。','宝宝揉眼睛，还不肯睡。','爸爸说：我来唱首歌。','他清清嗓子，','唱起低低的摇篮曲。','嗡——嗡——嗡——','声音沉沉的，缓缓的，','像大提琴在轻轻说话。','像远处的轮船，','载着宝宝，慢慢航行。','妈妈的歌像小鸟，','飞在高高的天上。','爸爸的歌像大船，','稳稳地浮在海面上。','宝宝靠在爸爸胸口，','能听见歌声和心跳，','一下，一下，一下。','眼皮越来越重，越来越重……','大船摇啊摇，','宝宝睡着啦。','爸爸的声音放得更轻，','把最后一个音符，','轻轻放进宝宝的梦里。']))
DEC6.append(S('2026-11-27-en', 'November 27, 2026 · Friday', '11/27',
    'Daddy\'s Deep Song (0-1 yr)', 'en',
    'Bedtime. Daddy sings a deep, low lullaby. Hum — hum — like a big cello, like a distant ship. Mommy\'s song is a bird; Daddy\'s is a big boat. Baby\'s eyes close on the gentle waves.',
    'Every voice is different, and every one is lovely. Daddy\'s deep song carries a big, safe feeling.',
    ['Evening — the room dims.','Baby rubs her eyes, not sleeping yet.','Daddy says: my turn to sing.','He clears his throat,','and hums a deep lullaby.','Hum — hum — hum —','The sound is low and slow,','like a cello speaking softly.','Like a distant ship,','carrying baby on a gentle voyage.','Mommy\'s song is a little bird,','flying high in the sky.','Daddy\'s song is a big ship,','steady on the sea.','Baby rests on Daddy\'s chest,','hearing song and heartbeat,','thump... thump... thump...','Eyelids grow heavier, heavier...','The big ship rocks, rocks,','and baby falls asleep.','Daddy\'s voice goes softer still,','laying the last note','gently into baby\'s dream.']))
DEC6.append(S('2026-11-27-science-cn', '2026年11月27日 · 星期五', '11/27',
    '🔬 歌声为什么有高有低（0-1岁）', 'zh',
    '妈妈的歌高高的，爸爸的歌低低的。声音的高低，是振动快慢定的：振得快，声音高；振得慢，声音低。',
    '声带（或琴弦）每秒振动的次数叫频率。频率高，声音就高；频率低，声音就低。爸爸声带长而厚，振动慢，所以声音低沉。',
    ['妈妈的歌：啦——啦——高高的。','爸爸的歌：嗡——嗡——低低的。','谁定的调子？','振动的快慢！','喉咙里的声带在振动。','振得快，像小蜜蜂扇翅膀，','声音就高高的。','振得慢，像大船慢慢摇，','声音就低低的。','爸爸的声带又长又厚，','振得慢，','所以唱歌嗡嗡的。','妈妈的声带细一些，','振得快，','歌声就清亮亮的。','高低音一起，才像一支乐队。'], sci=True))
DEC6.append(S('2026-11-27-science-en', 'November 27, 2026 · Friday', '11/27',
    '🔬 Science Story (0-1 yr): Why Songs Are High and Low', 'en',
    'Mommy\'s song is high; Daddy\'s song is low. The pitch depends on vibration speed: fast vibration — high sound; slow vibration — low sound.',
    'How many times per second the cords vibrate is called frequency. High frequency makes high notes, low frequency makes low notes. Daddy\'s long, thick cords vibrate slowly — a deep voice.',
    ['Mommy\'s song: la — la — so high!','Daddy\'s song: hum — hum — so low!','Who sets the tune?','The speed of vibration!','Vocal cords in the throat vibrate.','Fast, like bee wings flapping,','the sound is high.','Slow, like a big ship rocking,','the sound is low.','Daddy\'s cords are long and thick,','vibrating slowly —','that is why he hums.','Mommy\'s cords are thinner,','vibrating fast —','her song rings bright.','High notes plus low notes — one happy band!']))

# ---------- 11-28 周六（ep38 见 dd 文件） ----------
DEC6.append(S('2026-11-28-cn', '2026年11月28日 · 星期六', '11/28',
    '橘子香香（0-1岁）', 'zh',
    '妈妈剥橘子，皮一掰开，「咝」的一声，香气喷出来！满屋子都是橘子香。宝宝闻一闻，眼睛眯成月牙：这是冬天最好闻的味道。',
    '橘子皮里的小油囊一破，香气就蹦出来。美好的气味，是冬天的礼物。',
    ['下午，妈妈端来一盘橘子。','橙橙的，圆圆的，','顶上带着一小片绿叶。','妈妈拿起一个，用拇指掰皮。','「咝——」','皮一裂开，香气喷出来！','一屋子的橘子香，','清新清新的，甜甜的。','宝宝的鼻子动了动。','妈妈把橘子凑近：闻一闻？','宝宝深深吸一口气。','香！眼睛眯成了月牙。','妈妈剥下一小瓣，','挤出一点点汁，','给宝宝抿一抿——','酸酸甜甜，小脸皱成一团，','又马上笑了：还要！','橘子皮放进盘子里，','香气还在飘。','冬天的屋子里，','有暖气的暖，有窗户的水珠，','还有一整盘橘子香。','冬天的味道，是甜甜的。']))
DEC6.append(S('2026-11-28-en', 'November 28, 2026 · Saturday', '11/28',
    'Smell the Sweet Orange (0-1 yr)', 'en',
    'Mommy peels an orange — sss! The skin cracks open and fragrance bursts out! The whole room smells of orange. Baby takes a deep breath, eyes curving into crescents.',
    'Tiny oil pockets in orange skin burst and set the scent free. Beautiful smells are winter\'s gift.',
    ['Afternoon — Mommy brings oranges.','Orange and round,','with a tiny green leaf on top.','Mommy opens the peel with her thumb.','Sss —','the skin cracks, fragrance bursts out!','The whole room fills with orange scent,','fresh and sweet.','Baby\'s little nose twitches.','Mommy brings it close: smell this?','Baby takes a deep breath.','So fragrant! Eyes curve into crescents.','Mommy peels one little segment,','squeezes out a tiny drop of juice,','and lets baby taste —','sour and sweet! The face scrunches up,','then smiles at once: more!','The peel rests on the plate,','still sending out scent.','The winter room now has:','a warm radiator, window droplets,','and a whole plate of orange fragrance.','Winter tastes sweet.']))
DEC6.append(S('2026-11-28-science-cn', '2026年11月28日 · 星期六', '11/28',
    '🔬 橘子皮为什么香香的（0-1岁）', 'zh',
    '剥橘子时「咝」的一声，喷出一股香气。因为橘子皮上布满了小小的油囊，里面装着香香的精油，皮一破，精油就变成小雾滴喷出来。',
    '柑橘皮的油囊里存着柠檬烯等芳香物质，破裂时迅速挥发成香气微粒，飘进鼻子。轻轻挤橘子皮，对着火柴会喷出小「火花」，就是精油在起作用。',
    ['妈妈剥橘子。','「咝——」香气喷出来！','香味藏在哪儿？','橘子皮上，布满小油囊。','一个个小小鼓包，','像装满香水的小气球。','皮一掰破，','精油变成小雾滴，「咝」地喷出。','小雾滴飘进空气，','再飘进小鼻子——','闻到啦，好香！','柠檬皮、柚子皮也一样，','都藏着芳香小油囊。','所以剥橘子时，','总是香香的。'], sci=True))
DEC6.append(S('2026-11-28-science-en', 'November 28, 2026 · Saturday', '11/28',
    '🔬 Science Story (0-1 yr): Why Orange Peel Smells Sweet', 'en',
    'When the peel cracks — sss! — a burst of fragrance! Orange skin is covered with tiny oil pockets full of sweet essential oils; when broken, they spray out as a fine mist.',
    'Citrus peels store aromatic oils (like limonene) in little pockets. Broken, the oils evaporate into scent bits that float to your nose.',
    ['Mommy peels the orange.','Sss — fragrance bursts out!','Where does the scent hide?','All over the peel: tiny oil pockets.','Little bumps here and there,','like balloons of perfume.','The peel cracks open,','the oil sprays out as a fine mist.','Mist bits float into the air,','then into the little nose —','smell it! So sweet!','Lemon peel, pomelo peel too,','all hide their aromatic pockets.','That is why peeling citrus','always smells wonderful.']))

# ---------- 11-29 周日 ----------
DEC6.append(S('2026-11-29-cn', '2026年11月29日 · 星期日', '11/29',
    '被窝里的小隧道（0-1岁）', 'zh',
    '午睡时间，妈妈把被子搭成一个小隧道。宝宝爬进去——里面暖暖的、暗暗的，像自己的小山洞。妈妈在外面喊：小隧道里的宝宝在哪儿呀？',
    '小小的空间让宝宝特别有安全感。被窝隧道里，藏着笑声和暖暖的爱。',
    ['午睡时间到啦。','妈妈今天不直接盖被子，','她把被子架起来，','搭成一个鼓鼓的小隧道。','妈妈拍拍隧道口：','小家伙，钻进去看看？','宝宝手脚并用爬进去——','里面暖暖的、暗暗的，','像一个小小的山洞，','光从被子缝里漏进来，','一点一点的。','妈妈在外面喊：','「咦？小隧道里的宝宝在哪儿呀？」','被子里传出咯咯的笑声。','妈妈假装找：','「在被子里？不在！」','「在枕头下？不在！」','「啊——在这里！」','被子一掀，宝宝笑成一朵花。','再钻一次！再找一次！','玩累了，宝宝缩进被窝，','妈妈掖好被角。','小隧道变成小被窝，','暖暖的，睡吧。']))
DEC6.append(S('2026-11-29-en', 'November 29, 2026 · Sunday', '11/29',
    'The Blanket Tunnel (0-1 yr)', 'en',
    'Nap time. Mommy props the blanket into a little tunnel. Baby crawls in — warm and dim inside, like a tiny cave. Mommy calls from outside: where is the baby in the tunnel?',
    'Small cozy spaces make baby feel safe. Inside the blanket tunnel live laughter and warm love.',
    ['Nap time is here!','Today Mommy does not just cover baby up.','She props the blanket up,','making a puffy little tunnel.','Mommy pats the entrance:','want to crawl in, little one?','Baby crawls in, hands and feet —','warm and dim inside,','like a tiny cave,','light leaking through the seams,','just a little at a time.','Mommy calls from outside:','"Hmm? Where is the baby in the tunnel?"','Giggles float from under the blanket.','Mommy pretends to search:','"Under the blanket? No!"','"Under the pillow? No!"','"Ah — HERE you are!"','The blanket lifts — baby blooms into a flower of laughter.','Again! Crawl in again!','All played out, baby curls into the covers,','Mommy tucks the corners in.','The tunnel becomes a cozy nest —','warm now. Sleep.']))
DEC6.append(S('2026-11-29-science-cn', '2026年11月29日 · 星期日', '11/29',
    '🔬 被窝为什么越睡越暖（0-1岁）', 'zh',
    '刚钻进被窝，凉凉的；睡一会儿，暖暖的。被子自己不会发热——是宝宝的身体把被窝里的空气焐热了，被子再把暖空气锁住不让跑。',
    '被子是「空气保温层」：身体不断散发热量，被子里那层薄空气吸收热量后不再流动，像盖了层看不见的暖气——所以越睡越暖。',
    ['刚钻进被窝，','凉凉的，缩一缩。','睡一会儿，','暖暖的，舒展开。','奇怪，被子会发热吗？','不会哦。','发热的是宝宝的身体！','身体一直散着热气，','被窝里那层薄空气，','把热气接住，存起来。','被子把暖空气锁在里面，','不让它跑掉。','暖暖的空气围着宝宝，','越积越暖，','就越来越舒服啦。','早上掀开被子，热气跑了，','被窝又变回凉凉的。'], sci=True))
DEC6.append(S('2026-11-29-science-en', 'November 29, 2026 · Sunday', '11/29',
    '🔬 Science Story (0-1 yr): Why Beds Get Warmer as You Sleep', 'en',
    'Slip into bed: cool at first. Sleep a while: warm! The blanket cannot make heat — your body warms the air inside, and the blanket locks the warm air in.',
    'A blanket is an "air insulation layer": your body keeps giving off heat, the thin air layer absorbs it and stops moving, like an invisible heater — warmer and warmer.',
    ['Slip into the covers —','cool! Shiver a little.','Sleep a while —','warm! Stretch out happily.','Strange — does the blanket make heat?','No, it does not!','The heater is your own body!','Your body always gives off warmth,','and the thin air layer inside,','catches it and stores it.','The blanket locks the warm air in,','never letting it sneak away.','Warm air surrounds baby,','piling up warmth,','cozier and cozier.','In the morning the blanket lifts,','the heat escapes,','and the bed turns cool again.']))

# ---------- 11-30 周一 ----------
DEC6.append(S('2026-11-30-cn', '2026年11月30日 · 星期一', '11/30',
    '再见，十一月（0-1岁）', 'zh',
    '今天是十一月最后一天。睡前，妈妈翻着这一个月的照片：落叶的小路、外公的手表、雪籽敲窗、橘子香香……十一月要下班了，十二月排着队来了。',
    '跟一个月说再见，记住它送来的每个小美好。时间宝宝会自己长大，记忆会替我们收藏。',
    ['晚上，睡前抱抱时间。','妈妈翻着手机里的照片，','一张一张给宝宝看。','这张，是落叶的小路，','咔嚓咔嚓的落叶地毯。','这张，是外公的手表，','嘀嗒嘀嗒的时间脚步。','这张，是窗上的雪籽，','沙沙沙敲玻璃的小信使。','这张，是剥开的橘子，','咝——喷出来的香气。','还有会跳舞的窗帘，','咕嘟咕嘟的暖气片，','低低的爸爸摇篮曲……','宝宝看得眼睛亮亮的。','妈妈说：今天是十一月，','最后的一天啦。','十一月要下班了，','它把冬天交给了十二月。','十二月会带来什么？','可能是第一场真正的雪，','可能是宝宝的新本领。','妈妈亲亲宝宝：','晚安，十一月。','你好呀，十二月。']))
DEC6.append(S('2026-11-30-en', 'November 30, 2026 · Monday', '11/30',
    'Goodbye, November (0-1 yr)', 'en',
    'The last day of November. Before bed, Mommy shows baby the month\'s photos: the leafy path, Grandpa\'s watch, sleet on the window, orange fragrance... November clocks out, and December is lining up.',
    'Say goodbye to a month by remembering its little gifts. Time grows on its own; memories keep our treasures.',
    ['Evening — bedtime cuddle time.','Mommy flips through the month\'s photos,','one by one for baby.','This one: the leafy path,','the crunch-crunch leaf carpet.','This one: Grandpa\'s watch,','tick-tock footsteps of time.','This one: sleet on the window,','the tap-tap little messenger.','This one: the peeled orange,','the sss — burst of fragrance.','The dancing curtain too,','the glug-glug radiator,','Daddy\'s deep lullaby...','Baby watches with bright eyes.','Mommy says: today is November\'s,','very last day.','November clocks out tonight,','handing winter to December.','What will December bring?','Maybe the first real snow,','maybe baby\'s new little skills.','Mommy kisses baby:','Goodnight, November.','Hello, December!']))
DEC6.append(S('2026-11-30-science-cn', '2026年11月30日 · 星期一', '11/30',
    '🔬 冬天为什么天黑得早（0-1岁）', 'zh',
    '夏天七八点天还亮着，冬天四五点就黑了。因为冬天太阳升得低、走得短：它斜斜地爬上天，早早地就落山了。',
    '地轴是歪的。冬天我们这边歪离太阳，太阳在天上走的弧线又低又短，照亮白天的时刻就少——天亮得晚，黑得早。',
    ['夏天的傍晚，七八点，','天还亮亮的。','冬天的下午，四五点，','天就黑啦。','同一个太阳，为什么？','因为冬天太阳偷懒啦？','不是哦，它走的路短了。','冬天，太阳升得低低的，','在天上画一道短短的弧线，','早早地就落山。','照亮白天的时间，','就变得短短的。','天亮得晚，黑得早，','所以冬天总像傍晚。','等冬天过去，','太阳会重新走长长的路。'], sci=True))
DEC6.append(S('2026-11-30-science-en', 'November 30, 2026 · Monday', '11/30',
    '🔬 Science Story (0-1 yr): Why Winter Days End Early', 'en',
    'In summer the sky stays bright at eight; in winter it is dark by five. The sun rises low and walks a short path in winter — up slanting, down early.',
    'The Earth leans. In winter our side tips away from the sun, so the sun\'s arc is low and short — fewer bright hours. Late sunrise, early sunset.',
    ['Summer evenings, eight o\'clock,','the sky still bright.','Winter afternoons, five o\'clock,','dark already!','Same sun — why?','Is the sun feeling lazy?','No — its path is just shorter.','In winter the sun rises low,','draws a short arc across the sky,','and sets early.','The hours of daylight,','grow short and short.','Late sunrise, early sunset,','winter always feels like evening.','When winter passes,','the sun will walk its long road again.']))
