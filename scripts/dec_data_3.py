# -*- coding: utf-8 -*-
# 11-13 ~ 11-17
DEC3 = []

def S(id_, date, ds, title, lang, preview, moral, content, sci=False):
    d = {'id': id_, 'date': date, 'dateShort': ds, 'title': title, 'language': lang,
         'ageGroup': '0-1', 'ageLabel': '0-1岁', 'preview': preview, 'moral': moral,
         'content': content, 'category': 'science' if sci else 'regular'}
    if sci:
        d['series'] = 'science'; d['seriesTitle'] = '科学故事'
        d['source'] = 'Children science common sense' if lang == 'en' else '儿童科普常识'
    return d

# ---------- 11-13 周五 ----------
DEC3.append(S('2026-11-13-cn', '2026年11月13日 · 星期五', '11/13',
    '落叶地毯（0-1岁）', 'zh',
    '小区里的小路铺满落叶，金黄金黄，像一块大地毯。爸爸推着小车踩过去：咔嚓咔嚓！落叶地毯会唱歌呢。',
    '秋天的落叶不是垃圾，是大自然铺的地毯。踩上去咔嚓咔嚓，是秋天最后的歌。',
    ['午后，爸爸推小车出门。','小区的小路，变样子啦！','满地落叶，金黄金黄，','风一吹，还打着旋儿飘。','像谁铺了一块大地毯。','车轮轧上去——','咔嚓，咔嚓，咔嚓！','落叶地毯会唱歌！','爸爸停车，抱宝宝下车。','小脚丫踩在叶子上。','咔嚓！','再踩——咔嚓咔嚓！','宝宝笑得眼睛弯弯。','捡起一片叶子看看：','叶脉像小小的马路。','把它放进小车网兜里，','带一片秋天回家。']))
DEC3.append(S('2026-11-13-en', 'November 13, 2026 · Friday', '11/13',
    'Crunchy Leaf Path (0-1 yr)', 'en',
    'The little path is covered with golden leaves — a big leafy carpet! The stroller rolls over it: crunch, crunch, crunch! The leaf carpet sings.',
    'Autumn leaves are not trash — they are nature\'s carpet. The crunch is autumn\'s last song.',
    ['Afternoon — stroller time!','The little path has changed!','Golden leaves everywhere,','swirling when wind blows.','Someone laid a leafy carpet!','The wheels roll over it —','crunch, crunch, crunch!','The leaf carpet sings!','Daddy stops and lifts baby out.','Little feet step on the leaves.','Crunch!','Again — crunch, crunch!','Baby smiles, eyes curved.','Pick up one leaf and look:','its veins like tiny roads.','Into the stroller basket it goes,','a piece of autumn to take home.']))
DEC3.append(S('2026-11-13-science-cn', '2026年11月13日 · 星期五', '11/13',
    '🔬 干叶子为什么踩上去脆脆响（0-1岁）', 'zh',
    '夏天的叶子软软的，踩上去没声音。秋天的叶子干干的，一踩咔嚓响。因为叶子里的水分跑掉了，变得又干又脆。',
    '新鲜叶子水分多、韧性好，弯了不断；干了以后水分没了，叶肉变脆，一踩就「咔嚓」碎裂——脆响是叶子变干的证明。',
    ['夏天的叶子，软软的。','踩上去，没声音。','秋天的叶子，干干的。','一踩——咔嚓！','为什么不一样？','秘密是水分。','夏天的叶子喝饱了水，','像湿纸巾，弯了也不破。','秋天天气干，风一吹，','叶子里的水慢慢跑掉了。','叶子变得又干又脆，','像薄薄的薯片。','轻轻一踩——','咔嚓！碎了。','脆响，是叶子变干的证据。'], sci=True))
DEC3.append(S('2026-11-13-science-en', 'November 13, 2026 · Friday', '11/13',
    '🔬 Science Story (0-1 yr): Why Dry Leaves Crunch', 'en',
    'Summer leaves are soft and make no sound. Autumn leaves are dry — crunch! Their water has gone away, leaving them crisp.',
    'Fresh leaves are full of water and bend without breaking. Dry leaves lose their moisture and turn brittle — the crunch proves it.',
    ['Summer leaves — soft and quiet.','Step on them: no sound.','Autumn leaves — dry and light.','One step — CRUNCH!','Why the difference?','The secret is water.','Summer leaves drink their fill,','like a wet wipe — bends, never breaks.','Autumn air is dry; the wind blows,','water slowly slips away.','Leaves turn dry and brittle,','like thin potato chips.','A gentle step —','crunch! They crackle.','The crunch is the proof of dryness.']))

# ---------- 11-14 周六（ep36 系列见 dd 文件） ----------
DEC3.append(S('2026-11-14-cn', '2026年11月14日 · 星期六', '11/14',
    '小手小手几根头（0-1岁）', 'zh',
    '妈妈握着宝宝的小手唱手指歌：大拇指是爸爸，食指是妈妈……唱到小拇指，宝宝咯咯笑——五根小手指，各有各的名字。',
    '手指歌让宝宝认识自己的小手。认识自己，从认识五根手指开始。',
    ['午后，宝宝躺在妈妈腿上。','妈妈握住那只小手。','大拇指弯一弯：','「大拇指是爸爸，开汽车——嘀嘀！」','食指弯一弯：','「食指是妈妈，洗衣服——哗哗！」','中指弯一弯：','「中指是哥哥，拍皮球——嘭嘭！」','无名指弯一弯：','「无名指是姐姐，弹钢琴——叮叮！」','最后是小拇指：','「小拇指是宝宝，笑一笑——嘻嘻！」','宝宝咯咯笑出声。','五根手指，轮流弯，','像五个小伙伴排队做操。','妈妈亲亲小拳头：','「小手小手真真能干！」','宝宝挥挥另一只小手：','明天再来玩手指歌呀。']))
DEC3.append(S('2026-11-14-en', 'November 14, 2026 · Saturday', '11/14',
    'Ten Little Fingers (0-1 yr)', 'en',
    'Mommy holds baby\'s hand and sings the finger song. Thumb is Daddy, pointer is Mommy... At the pinky, baby giggles — five little fingers, each with a name.',
    'Finger songs help baby know the little hand. Knowing yourself starts with five little fingers.',
    ['Afternoon — baby on Mommy\'s lap.','Mommy holds the little hand.','Thumb bends first:','"Thumb is Daddy, drives a car — beep beep!"','Pointer finger bends:','"Pointer is Mommy — swish, swish!"','Tall finger bends:','"Tall finger is brother — bounce the ball!"','Ring finger bends:','"Ring finger is sister — plink, plink!"','And the little pinky:','"Pinky is baby — hee hee hee!"','Baby laughs out loud.','Five fingers take turns bending,','like five friends doing exercises.','Mommy kisses the little fist:','"Busy little hand!"','Baby waves the other hand:','more finger songs tomorrow!']))
DEC3.append(S('2026-11-14-science-cn', '2026年11月14日 · 星期六', '11/14',
    '🔬 手指为什么有长有短（0-1岁）', 'zh',
    '伸开小手看一看：中指最高，大拇指又矮又壮。手指为什么不一样长？因为每根手指的工作不同呀。',
    '长短不一的手指配合起来才能又稳又灵活：中指长够得远，拇指壮才能对捏、握物。五根手指像一支小球队，各有各的位置。',
    ['伸开小手看一看。','中指最高，像小旗杆。','大拇指最矮，胖胖壮壮。','为什么不一样长？','因为工作不一样呀！','中指长，够得远。','食指灵活，会指东西。','大拇指壮，能对捏、能握牢。','试试不用大拇指拿摇铃？','怎么拿都拿不稳！','小指最小，','负责稳住手边的小角落。','五根手指像一支小球队，','高矮搭配，才能赢。'], sci=True))
DEC3.append(S('2026-11-14-science-en', 'November 14, 2026 · Saturday', '11/14',
    '🔬 Science Story (0-1 yr): Why Fingers Have Different Lengths', 'en',
    'Open your hand: the tall finger is tallest, the thumb is short and strong! Fingers differ because each has its own job.',
    'Different lengths work together for grip and skill: long fingers reach far, the strong thumb pinches and holds. Five fingers are a little team, each in its own position.',
    ['Open your hand and look.','The tall finger stands highest.','The thumb is shortest — strong and chubby!','Why different lengths?','Different jobs!','Long fingers reach far.','The pointer is nimble — it points.','The strong thumb pinches and grips.','Try holding a rattle without the thumb —','it just slips and slips!','The pinky is smallest,','stabilizing the hand\'s edge.','Five fingers are a little team —','tall and short together, they win!']))

# ---------- 11-15 周日 ----------
DEC3.append(S('2026-11-15-cn', '2026年11月15日 · 星期日', '11/15',
    '灯灯亮了灯灯灭了（0-1岁）', 'zh',
    '爸爸抱着宝宝站在开关旁。「啪嗒」——灯亮了！「啪嗒」——灯灭了！宝宝笑得直蹬腿。灯灯亮了，灯灯灭了，像在玩捉迷藏。',
    '开灯关灯是宝宝最爱的因果关系游戏：一个动作，一个结果，世界就是这样有规律的。',
    ['傍晚，房间暗下来了。','爸爸抱着宝宝，走到开关旁。','「啪嗒！」','灯亮了！','满屋子的光，','宝宝眼睛睁得圆圆的。','「啪嗒。」','灯灭了！','房间躲进黑黑里。','宝宝小手挥挥，蹬蹬腿。','「啪嗒！」又亮了！','「啪嗒。」又灭了！','亮——灭——亮——灭，','像在玩捉迷藏。','宝宝咯咯笑，伸手也想去按。','爸爸扶着小手指，轻轻一按——','「啪嗒！」','宝宝自己把灯点亮的！','小手指按一按，光就来报到：','世界有规律，一按就明了。']))
DEC3.append(S('2026-11-15-en', 'November 15, 2026 · Sunday', '11/15',
    'Light On, Light Off (0-1 yr)', 'en',
    'Daddy holds baby by the light switch. Click — light on! Click — light off! Baby laughs and kicks. On and off, on and off — like hide-and-seek!',
    'Switching lights is baby\'s favorite cause-and-effect game: one action, one result. The world works by such simple rules.',
    ['Evening — the room grows dim.','Daddy holds baby by the switch.','Click!','Light on!','The room fills with glow,','baby\'s eyes open wide.','Click.','Light off!','The room hides in the dark.','Baby waves and kicks.','Click! On again!','Click. Off again!','On — off — on — off,','like playing hide-and-seek.','Baby giggles, reaching for the switch.','Daddy guides the little finger — gently:','click!','Baby turned on the light all alone!','Press, and the light arrives:','the world has simple, happy rules.']))
DEC3.append(S('2026-11-15-science-cn', '2026年11月15日 · 星期日', '11/15',
    '🔬 灯为什么会亮（0-1岁）', 'zh',
    '「啪嗒」一按，灯就亮了。谁在让灯亮？是电流！它从发电厂出发，跑过长长的电线，钻进灯泡里，把灯丝烧得亮亮的。',
    '灯泡里有一根细细的灯丝，电流通过时把它烧得又红又亮，像一个小小的太阳——开关一断，电流停下，灯就灭了。',
    ['「啪嗒！」灯亮啦。','谁在让灯亮呀？','是电流小卫士！','它从发电厂出发，','跑过长长的电线，','跑啊跑，钻进灯泡里。','灯泡里有一根细灯丝，','细细的，卷成小圈。','电流一通过，','灯丝烧得又红又亮，','像一个小小的太阳！','「啪嗒」——开关断了，','电流停下来，','灯也休息了。','电宝宝真勤快，','啪嗒一声就到岗。'], sci=True))
DEC3.append(S('2026-11-15-science-en', 'November 15, 2026 · Sunday', '11/15',
    '🔬 Science Story (0-1 yr): Why Lights Turn On', 'en',
    'Click — the light is on! Who makes it shine? Electricity! It runs from the power plant through long wires into the bulb and heats the filament bright.',
    'Inside a bulb is a thin filament. When electricity flows through, it glows red-hot like a tiny sun. Break the circuit, and the light goes off.',
    ['Click! The light turns on.','Who makes it shine?','The electricity guard!','It starts at the power plant,','runs along long, long wires,','running, running, into the bulb.','Inside waits a thin filament,','curled into a tiny spring.','Electricity flows through —','the filament glows red-hot,','like a tiny little sun!','Click — the switch opens,','electricity stops,','and the light rests.','Electricity is a fast worker —','one click, and it arrives!']))

# ---------- 11-16 周一 ----------
DEC3.append(S('2026-11-16-cn', '2026年11月16日 · 星期一', '11/16',
    '毛衣上的小羊不见了（0-1岁）', 'zh',
    '今天穿的是另一件毛衣——咦，小羊呢？宝宝在毛衣上找来找去，找到了：这次是小熊！每件毛衣上，都住着一个毛线小伙伴。',
    '找一找、认一认，毛衣上的图案是宝宝的第一本图画书。',
    ['早晨穿衣服。','妈妈拿起一件新毛衣。','米色的，软软的。','宝宝低头找：小羊呢？','胸口没有小羊。','翻翻袖子——没有。','看看后背——也没有。','咦？小羊搬家了吗？','妈妈指指毛衣的正中间：','看，这里是谁？','一只小熊！','棕色的，抱着一个小蜜罐。','原来每件毛衣上，','都住着不同的毛线小伙伴。','宝宝伸手摸摸小熊。','软软的，暖暖的。','明天穿哪件呢？','不知道会遇见谁，真期待呀。']))
DEC3.append(S('2026-11-16-en', 'November 16, 2026 · Monday', '11/16',
    'Mommy\'s Big Coat (0-1 yr)', 'en',
    'A different sweater today — where is the little lamb? Baby searches... and finds a bear instead! Every sweater has its own knitted friend.',
    'Sweater patterns are baby\'s first picture book. Look and name, look and name.',
    ['Morning — dressing time.','Mommy brings another sweater.','Cream-colored, soft and snug.','Baby looks down: where is the lamb?','No lamb on the chest.','Check the sleeve — no.','Check the back — no!','Did the lamb move away?','Mommy points to the middle:','look, who is this?','A little bear!','Brown, hugging a honey pot.','Every sweater,','hosts a different knitted friend.','Baby strokes the bear.','Soft and warm.','Which sweater tomorrow?','What a nice surprise to wait for!']))
DEC3.append(S('2026-11-16-science-cn', '2026年11月16日 · 星期一', '11/16',
    '🔬 为什么爸爸的声音低低的（0-1岁）', 'zh',
    '爸爸说话「嗡嗡」的，妈妈说话清清脆脆的。都是嘴巴在说话，为什么声音不一样？因为声带不一样长。',
    '喉咙里的声带像两根小琴弦。粗厚长的琴弦（爸爸的）振得慢，声音低；细短的琴弦振得快，声音高——声音的高低是振动快慢决定的。',
    ['爸爸说话：嗡——嗡——','妈妈说话：清清脆脆。','宝宝咿呀：啊——啊——','都是嘴巴在说，','为什么不一样？','喉咙里有两根小琴弦，','叫「声带」。','爸爸的声带又长又厚，','振动得慢——','声音就低低的，嗡嗡嗡。','妈妈的声带细一些，','振得快——','声音就清清脆脆。','宝宝长大了，','声带也会慢慢变化哟。'], sci=True))
DEC3.append(S('2026-11-16-science-en', 'November 16, 2026 · Monday', '11/16',
    '🔬 Science Story (0-1 yr): Why Daddy\'s Voice Is Deep', 'en',
    'Daddy\'s voice goes hum-hum; Mommy\'s voice is clear and bright. Both are mouths talking — why so different? The vocal cords are different!',
    'Two little strings inside the throat vibrate to make voice. Thick, long strings (Daddy\'s) vibrate slowly — a deep voice. Thin, short ones vibrate fast — a high voice.',
    ['Daddy talks: hum — hum —','Mommy talks: clear and bright!','Baby babbles: ah — ah —','All from the mouth,','why do they differ?','In the throat live two tiny strings,','called vocal cords.','Daddy\'s cords are long and thick,','vibrating slowly —','a deep, humming voice.','Mommy\'s cords are thinner,','vibrating faster —','a clear, bright voice.','When baby grows up,','the cords will change too!']))

# ---------- 11-17 周二 ----------
DEC3.append(S('2026-11-17-cn', '2026年11月17日 · 星期二', '11/17',
    '会跳舞的窗帘（0-1岁）', 'zh',
    '窗户开了一条缝，风钻进来。窗帘鼓起来，飘起来，转个圈——哇，窗帘在跳舞！宝宝看得目不转睛：风先生，请您再跳一支呀。',
    '看不见的风，会借窗帘跳给我们看。世界藏着的美好，总会悄悄露出一角。',
    ['下午，妈妈把窗户开了一条缝。','呼——风钻进来。','窗帘鼓起来，圆圆的，','像一艘小帆船。','飘起来，晃起来，','又轻轻转了个圈。','宝宝躺在爬行垫上，看呆了。','窗帘在跳舞呢！','一摆，一摆，慢慢悠悠。','忽然呼——风大了，','窗帘「唰」地飘得高高的！','宝宝咯咯笑出声。','风小了，窗帘慢慢落下来，','像舞跳完了，鞠个躬。','宝宝挥挥小手：','风先生，再跳一支呀！','风先生听见了，','呼——又来了一阵。','窗帘转了个大圈。','看不见的风，借窗帘跳舞给宝宝看。']))
DEC3.append(S('2026-11-17-en', 'November 17, 2026 · Tuesday', '11/17',
    'The Dancing Curtain (0-1 yr)', 'en',
    'The window is open a crack, and wind sneaks in. The curtain puffs up, floats, and turns — look, the curtain is dancing! Baby cannot look away.',
    'Invisible wind dances through the curtain. Hidden beauty in the world always peeks out somewhere.',
    ['Afternoon — the window opens a crack.','Whoosh — wind sneaks in.','The curtain puffs up, round,','like a little sail.','It floats and sways,','and turns in a slow circle.','Baby stares from the play mat.','The curtain is dancing!','Swing, swing, slow and easy.','Suddenly — whoosh! A big gust,','the curtain flies up high!','Baby giggles out loud.','The wind softens, the curtain floats down,','like a dancer taking a bow.','Baby waves a little hand:','"Mr. Wind, one more dance!"','Mr. Wind hears,','whoosh — another gust comes.','The curtain spins a big circle.','Invisible wind, dancing through cloth.']))
DEC3.append(S('2026-11-17-science-cn', '2026年11月17日 · 星期二', '11/17',
    '🔬 窗帘为什么会飘（0-1岁）', 'zh',
    '窗户一开，窗帘就飘起来跳舞。是窗帘自己会动吗？不是，是空气在推它！风就是流动的空气，空气一动，窗帘就跟着舞。',
    '户外和屋里的空气不一样时，空气会流动来「拉平」差异——流动的空气撞上窗帘，就把它推得鼓起来、飘起来。',
    ['窗户开一条缝，','窗帘就飘起来啦。','是它会跳舞吗？','不是哦，是空气在推！','风，就是流动的空气。','窗外的凉空气，屋里的暖空气，','它们不一样，就流动起来。','空气流进屋里，','撞上窗帘——','窗帘被推得鼓鼓的。','风大，推得高高的。','风小，就慢慢悠悠地晃。','空气累了停下来，','窗帘也垂下来休息。','窗帘的舞，是空气编的舞。'], sci=True))
DEC3.append(S('2026-11-17-science-en', 'November 17, 2026 · Tuesday', '11/17',
    '🔬 Science Story (0-1 yr): Why Curtains Float', 'en',
    'Open the window a crack and the curtain starts to dance. Does it move by itself? No — air is pushing it! Wind is moving air, and moving air moves curtains.',
    'When outside and inside air differ, air flows to balance it. The flowing air bumps the curtain, puffing it up and making it sway.',
    ['The window opens a crack,','and the curtain floats up!','Does it dance by itself?','No — air pushes it!','Wind is simply moving air.','Cool air outside, warm air inside,','they differ, so air starts to flow.','The air streams into the room,','bumps the curtain —','it puffs out, round and full.','Big wind? Pushed up high!','Little wind? Gentle swaying.','When the air rests,','the curtain rests too.','The curtain\'s dance is the air\'s dance.']))
