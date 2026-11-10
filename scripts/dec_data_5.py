# -*- coding: utf-8 -*-
# 11-22 ~ 11-26
DEC5 = []

def S(id_, date, ds, title, lang, preview, moral, content, sci=False):
    d = {'id': id_, 'date': date, 'dateShort': ds, 'title': title, 'language': lang,
         'ageGroup': '0-1', 'ageLabel': '0-1岁', 'preview': preview, 'moral': moral,
         'content': content, 'category': 'science' if sci else 'regular'}
    if sci:
        d['series'] = 'science'; d['seriesTitle'] = '科学故事'
        d['source'] = 'Children science common sense' if lang == 'en' else '儿童科普常识'
    return d

# ---------- 11-22 周日 ----------
DEC5.append(S('2026-11-22-cn', '2026年11月22日 · 星期日', '11/22',
    '爷爷的旧手表（0-1岁）', 'zh',
    '外公来看宝宝，手腕上戴着一块旧手表。嘀嗒，嘀嗒，指针慢慢走。宝宝把耳朵贴上去听——小手表里，住着一个不知疲倦的小闹钟。',
    '嘀嗒声是时间走路的脚步。和宝宝在一起的每一刻，都是最好听的那一秒。',
    ['外公又来看宝宝啦。','这次，他手腕上戴着','一块旧旧的银色手表。','「爷爷，这是什么呀？」','宝宝当然不会说话，','但小手已经伸过去了。','外公把手腕凑到宝宝面前。','圆圆的表盘，细细的指针，','指针慢慢慢慢走。','嘀嗒，嘀嗒，嘀嗒。','宝宝盯着指针看。','外公说：把耳朵贴上来听听。','宝宝的小耳朵，贴上表盘。','嘀嗒，嘀嗒——','好清楚呀！','像小闹钟在身边走路，','不知疲倦地，一步一步。','外公说：这是时间的脚步声。','它陪爷爷走了好多年，','现在，也陪着我们的小宝贝。']))
DEC5.append(S('2026-11-22-en', 'November 22, 2026 · Sunday', '11/22',
    'Grandpa\'s Old Watch (0-1 yr)', 'en',
    'Grandpa visits baby, wearing an old silver watch. Tick-tock, tick-tock, the hands walk slowly. Baby puts an ear to it — inside the watch lives a tireless little clock.',
    'Tick-tock is time walking. Every moment with baby is the sweetest tick of all.',
    ['Grandpa comes to see baby again!','This time he wears','an old silver watch.','Baby\'s hand reaches out at once.','Grandpa brings his wrist close.','A round face, thin hands,','walking slowly, slowly.','Tick-tock, tick-tock, tick-tock.','Baby stares at the moving hands.','Grandpa says: listen with your ear.','The little ear presses the watch.','Tick-tock, tick-tock —','so clear!','Like a little clock walking nearby,','step by step, never tired.','Grandpa says: that is time walking.','It walked with Grandpa for years,','and now, it walks with our little one.']))
DEC5.append(S('2026-11-22-science-cn', '2026年11月22日 · 星期日', '11/22',
    '🔬 冬天嘴里为什么呼白气（0-1岁）', 'zh',
    '天冷了，外公说话时，嘴边冒出一团团白气，像小云朵。哈——宝宝也试试。白气是从哪儿来的？是我们呼出的水汽变的！',
    '呼出的气里有水汽。夏天天气热，水汽藏得看不见；冬天空气冷，水汽一出来就被冻成许多小水珠——许多小水珠聚在一起，就是白气。',
    ['呼——天冷啦。','外公说话，嘴边冒白气，','一团一团，像小云朵。','宝宝也哈一口气——','呼，白气也出来了！','夏天怎么没有呀？','因为白气是水汽变的！','我们呼出的气里，藏着水汽。','夏天热，水汽躲着看不见。','冬天冷，水汽一出来，','就被冻成许多小水珠。','小水珠挨着小水珠，','聚成白白的一团——','那就是白气呀。','冬天到了，白气出来了。'], sci=True))
DEC5.append(S('2026-11-22-science-en', 'November 22, 2026 · Sunday', '11/22',
    '🔬 Science Story (0-1 yr): Why Breath Turns White in Winter', 'en',
    'It is cold! When Grandpa talks, puffs of white breath float by his mouth, like little clouds. Baby tries too — haa! Where does white breath come from?',
    'Our breath carries water vapor. In warm summer it hides invisibly; in cold winter it freezes into tiny droplets — many droplets together make the white puff.',
    ['Brr — it is cold!','Grandpa talks, white puffs appear,','cloud after cloud by his mouth.','Baby breathes out — haa!','White breath too!','Why not in summer?','White breath is made of vapor!','Our breath carries water vapor.','Summer is warm — vapor hides.','Winter is cold — vapor freezes,','into tiny, tiny droplets.','Droplet hugs droplet,','gathering into a white puff —','that is white breath!','Winter is here — puffs are out to play.']))

# ---------- 11-23 周一 ----------
DEC5.append(S('2026-11-23-cn', '2026年11月23日 · 星期一', '11/23',
    '雪籽敲窗户（0-1岁）', 'zh',
    '「沙沙，沙沙」，小石子一样的雪籽打在窗玻璃上。宝宝趴在窗边看：玻璃上蹦跳的小白粒，是冬天寄来的第一封信。',
    '雪籽是雪的小弟弟，先来探路。冬天的好消息，是一粒一粒敲窗户告诉我们的。',
    ['傍晚，天灰灰的。','忽然——沙沙，沙沙，','有什么打在窗玻璃上！','宝宝趴到窗边看。','呀，小白粒！','一颗一颗，蹦蹦跳跳，','打在玻璃上，弹起来，又落下。','像谁在窗外撒小石子。','又像小珍珠往下掉。','妈妈过来看：这是雪籽，','是雪的小弟弟！','它跑得急，圆头圆脑，','落地还会蹦一下。','明天，说不定雪姐姐就来了，','她会穿白裙子，飘飘悠悠。','雪籽还在沙沙沙地敲窗，','敲得很轻很有礼貌。','宝宝朝玻璃挥挥手：','冬天你好，欢迎你来！']))
DEC5.append(S('2026-11-23-en', 'November 23, 2026 · Monday', '11/23',
    'Is That Snow? (0-1 yr)', 'en',
    'Tap-tap-tap — tiny white grains hit the window! Baby watches from the sill: bouncing little white pearls. Winter has mailed its first letter.',
    'Sleet is snow\'s little brother, coming first to check the way. Winter\'s good news taps on windows, one grain at a time.',
    ['Evening — the sky turns gray.','Suddenly — tap, tap, tap!','Something hits the window!','Baby leans on the sill.','Look — tiny white grains!','One by one they bounce,','hitting the glass, hopping up, falling down.','Like little pebbles from the sky,','or tiny falling pearls.','Mommy comes over: that is sleet,','the snow\'s little brother!','He runs fast, round little head,','bouncing once when he lands.','Tomorrow, maybe big sister Snow will come,','wearing her white dress, floating slowly.','Sleet keeps tapping the window,','gently, politely.','Baby waves at the glass:','Hello, winter — welcome!']))
DEC5.append(S('2026-11-23-science-cn', '2026年11月23日 · 星期一', '11/23',
    '🔬 雪花为什么白白的（0-1岁）', 'zh',
    '雪籽白白的，雪花也白白的。可雪是水变的，水明明没有颜色呀！因为雪花是许多小冰晶拼成的，光在里面跳来跳去，全被反射出来——所有颜色混在一起，就成了白色。',
    '每片雪花由许多小冰晶组成，冰晶的小平面把各种颜色的光全部反射回来。红橙黄绿全都混在一起，眼睛看到的就是白色。',
    ['雪籽，白白的。','雪花，也白白的。','可雪是水变的呀，','水没有颜色呀！','秘密在冰晶里。','雪花是许多小冰晶拼成的，','每个冰晶都有小小的平面。','光跑进去，','就被平面弹来弹去，','红色弹出来，黄色弹出来，','绿色、蓝色都弹出来……','所有颜色混在一起，','就变成白色啦！','像彩虹全部叠在一起。','雪花白白，','是它在把所有的光都送给我们。'], sci=True))
DEC5.append(S('2026-11-23-science-en', 'November 23, 2026 · Monday', '11/23',
    '🔬 Science Story (0-1 yr): Why Snowflakes Are White', 'en',
    'Sleet is white, snow is white — but snow is made of water, and water has no color! The secret: snowflakes are built of many tiny ice crystals that bounce all light back out.',
    'Each crystal has tiny faces that reflect every color of light. All colors mixed together look white — like stacking the whole rainbow into one flake.',
    ['Sleet is white.','Snowflakes are white too.','But snow is made of water,','and water has no color!','The secret lives in the crystals.','A snowflake is many tiny ice crystals,','each with small shiny faces.','Light runs inside,','bouncing face to face —','red bounces out, yellow bounces out,','green and blue bounce out too...','All the colors mixed together,','turn into white!','Like stacking the whole rainbow.','Snowflakes are white,','because they gift us all the light.']))

# ---------- 11-24 周二 ----------
DEC5.append(S('2026-11-24-cn', '2026年11月24日 · 星期二', '11/24',
    '暖气片咕嘟咕嘟（0-1岁）', 'zh',
    '天冷了，家里的暖气片开始工作：咕嘟咕嘟，慢慢变热。宝宝的小手伸过去——暖暖的！整间屋子也慢慢暖起来，像住进了大棉被里。',
    '暖气片把屋子焐暖，冬天也可以暖暖和和。科技就是让人舒服的小魔法。',
    ['早上醒来，屋里凉凉的。','爸爸拧开暖气片。','咕嘟，咕嘟，咕嘟——','暖气片里面，热水开始流动。','摸一摸：温温的。','再等一会儿：热热的！','热气从暖气片上飘出来，','一点点，一点点，','爬上墙壁，散进屋子。','屋子慢慢暖起来了。','宝宝的小手伸过去，','贴一贴——暖暖的，好舒服。','妈妈把宝宝的小袜子搭在暖气片旁，','袜子也变得暖乎乎。','穿上去，脚丫暖暖的。','整间屋子，像住进大棉被里。','冬天不可怕，','因为家里有会发热的暖气片。']))
DEC5.append(S('2026-11-24-en', 'November 24, 2026 · Tuesday', '11/24',
    'The Warm Radiator (0-1 yr)', 'en',
    'It is cold. The radiator starts working: glug, glug, slowly warming up. Baby touches it — warm! The whole room grows cozy, like sleeping inside a big quilt.',
    'The radiator warms the room; winter can be cozy too. Technology is a little magic for comfort.',
    ['Morning — the room is chilly.','Daddy turns on the radiator.','Glug, glug, glug —','hot water starts flowing inside.','Touch it: lukewarm.','Wait a while: hot!','Warm air rises from the radiator,','little by little,','climbing the walls, spreading through the room.','Slowly the room turns warm.','Baby\'s hand reaches out,','rests on it — warm and cozy!','Mommy hangs baby\'s socks nearby,','they turn warm too.','On they go — warm little toes!','The whole room feels like a big quilt.','Winter is not scary,','when a warm radiator lives at home.']))
DEC5.append(S('2026-11-24-science-cn', '2026年11月24日 · 星期二', '11/24',
    '🔬 暖气为什么让整间屋子变暖（0-1岁）', 'zh',
    '暖气片只占一个小角落，怎么让整间屋子都暖起来？因为暖气片加热了身边的空气，暖空气轻，会往上飘；冷空气重，会沉下来补位——空气转着圈，把暖送到每个角落。',
    '热空气比冷空气轻，会上升；冷空气流过来填补，再被加热上升。空气不停转圈（这叫对流），屋子就都暖了。',
    ['暖气片，站在墙角，','个头小小的。','它怎么暖热整间屋子？','它先加热身边的空气。','暖空气变轻了，','像小气球，往上飘。','上面的冷空气重，','沉下来补位置。','补位的冷空气又被加热，','又变轻，又往上飘……','空气转啊转，转圈圈，','把暖带去每个角落。','地板暖了，天花板暖了，','宝宝的爬行垫也暖了。','这个转圈圈的魔法，','叫「对流」呀。'], sci=True))
DEC5.append(S('2026-11-24-science-en', 'November 24, 2026 · Tuesday', '11/24',
    '🔬 Science Story (0-1 yr): How the Radiator Warms the Room', 'en',
    'The radiator sits in one small corner — how does it warm the whole room? It heats the air nearby; warm air floats up, cool air sinks in to replace it. Air circles around, delivering warmth everywhere.',
    'Warm air is lighter than cool air, so it rises; cool air flows in, gets heated, and rises too. This circling is called convection.',
    ['The radiator stands in the corner,','small and quiet.','How does it warm everything?','It heats the air beside it first.','Warm air turns lighter,','like a balloon, floating up.','Cool air above is heavier,','sinking down to fill in.','The new air gets heated too,','turns light, floats up again...','Air keeps circling round and round,','carrying warmth to every corner.','The floor is warm, the ceiling is warm,','even baby\'s play mat is warm.','This circling magic','is called convection!']))

# ---------- 11-25 周三 ----------
DEC5.append(S('2026-11-25-cn', '2026年11月25日 · 星期三', '11/25',
    '窗户上的小水珠（0-1岁）', 'zh',
    '早上一看，窗玻璃上爬满了小水珠，一颗一颗，亮晶晶。屋外冷，屋内暖，窗户「出汗」啦。宝宝伸出小手指，画一道——哇，会画画的窗户！',
    '窗户上的小水珠是屋里暖空气遇冷变出来的。生活里藏着的小科学，一伸手就能摸到。',
    ['早晨醒来，看窗户——','呀！玻璃上爬满小水珠。','一颗，两颗，亮晶晶，','像玻璃长了小汗珠。','屋外北风呼呼吹，','屋里暖暖和和的。','暖空气撞上冰凉的玻璃，','「好冷呀！」','它带来的水汽，','一下子变成小水珠，','趴在玻璃上不走了。','宝宝伸出小手指，','在玻璃上画一道——','水珠让开，画痕出现！','再画个圆，画条弯弯的线，','窗户变成大画板！','妈妈画了一朵小花，','宝宝拍拍手。','窗户出汗不可怕，','它会变出画画的魔法。']))
DEC5.append(S('2026-11-25-en', 'November 25, 2026 · Wednesday', '11/25',
    'Little Drops on the Window (0-1 yr)', 'en',
    'In the morning, the window is covered with tiny water drops, shiny and round. Cold outside, warm inside — the window is "sweating"! Baby draws a line with a finger — wow, a window that paints!',
    'Drops on the window come from warm indoor air meeting cold glass. Little science hides in daily life, right at your fingertips.',
    ['Morning — look at the window!','Tiny water drops everywhere,','shiny, round, one by one,','like the glass is sweating.','Cold wind blows outside,','warm and cozy inside.','Warm air bumps the icy glass,','"So cold!"','The vapor it carries','turns into tiny drops at once,','resting on the glass.','Baby stretches out a finger,','draws a line — the drops step aside!','A circle, a wavy line —','the window becomes a drawing board!','Mommy draws a little flower,','baby claps happily.','A sweating window is not scary —','it hides a painting magic.']))
DEC5.append(S('2026-11-25-science-cn', '2026年11月25日 · 星期三', '11/25',
    '🔬 窗户上的小水珠是哪来的（0-1岁）', 'zh',
    '窗户不会出汗。小水珠是屋里暖空气「呼」出的水汽变的：暖空气碰到冰凉的玻璃，水汽就凝结成小水珠，趴在上面。',
    '水汽遇冷会凝结成小水珠——就像冰凉的杯子外壁也会「冒汗」一样。暖空气的水汽多，遇冷就更容易「出汗」。',
    ['窗户，真的会出汗吗？','不会哦。','小水珠是哪来的？','是屋里暖空气送的。','暖空气里藏着水汽，','就像湿湿的呼吸。','玻璃被北风吹得凉凉的，','暖空气一碰上它——','「好凉呀！」','水汽吓一跳，','变成小水珠，','一颗颗趴在玻璃上。','凉凉的杯子外壁也会这样，「冒汗」。','暖的碰上冷的，','水汽就变水珠——','这叫「凝结」。'], sci=True))
DEC5.append(S('2026-11-25-science-en', 'November 25, 2026 · Wednesday', '11/25',
    '🔬 Science Story (0-1 yr): Where Window Drops Come From', 'en',
    'Windows do not sweat! The tiny drops come from warm indoor air: when it meets the icy glass, its vapor turns into little drops that rest there.',
    'Vapor condenses into droplets when it meets something cold — like a cold glass of water "sweating" outside. Warm air holds more vapor, so it drops more easily.',
    ['Does the window really sweat?','No, it does not!','Where do the drops come from?','From the warm indoor air.','Warm air carries vapor,','like a damp little breath.','The north wind chills the glass,','warm air bumps into it —','"So cold!"','The vapor gets startled,','turning into tiny drops,','resting on the glass one by one.','A cold cup sweats the same way.','Warm meets cold,','vapor becomes droplets —','this is called condensation!']))

# ---------- 11-26 周四 ----------
DEC5.append(S('2026-11-26-cn', '2026年11月26日 · 星期四', '11/26',
    '小手套一对好朋友（0-1岁）', 'zh',
    '下雪籽啦，出门要戴手套。妈妈拿出两只小手套：一只左手，一只右手，是一对好朋友，永远手拉手（用绳子连着）不分开。',
    '小手套是一对好朋友，小手也是一对好朋友。好朋友的默契，是让彼此都暖暖的。',
    ['沙沙，雪籽又来敲窗了。','出门前，妈妈拿出小手套。','两只，粉色的小手套。','一只给左手，一只给右手。','妈妈说：它们是一对好朋友。','你看，中间有根小绳子连着，','走到哪儿都不分开。','宝宝伸出手，','左手钻进一只手套，','右手钻进另一只。','两只手套把小手包起来，','暖暖的，软软的。','出门啦！','雪花籽落在手套上，','一点，一点，又一点。','手套不怕冷，小手不怕冻。','左手拍一拍右手，','啪！两个好朋友打招呼。','回家摘下手套，','两只小手还是热乎乎的。','手套好朋友回抽屉休息，','明天再一起出门呀。']))
DEC5.append(S('2026-11-26-en', 'November 26, 2026 · Thursday', '11/26',
    'Mittens Are Friends (0-1 yr)', 'en',
    'Sleet is tapping again — time for mittens! Mommy brings two little mittens: one for the left hand, one for the right, best friends joined by a string, never apart.',
    'Mittens are a pair of friends, and so are the two little hands. Best friends keep each other warm.',
    ['Tap-tap — sleet at the window!','Before going out, mittens time.','Two little pink mittens.','One for the left, one for the right.','Mommy says: they are best friends.','See the little string between them —','never apart, wherever they go.','Baby stretches out the hands,','left hand into one mitten,','right hand into the other.','The mittens wrap the hands,','warm and soft.','Out the door we go!','Sleet lands on the mittens,','one dot, one dot, one more.','Mittens fear no cold, hands fear no frost.','Left hand pats the right —','clap! Two friends say hello.','Home again, mittens off,','both little hands still toasty.','The mitten friends rest in the drawer,','ready for tomorrow\'s walk.']))
DEC5.append(S('2026-11-26-science-cn', '2026年11月26日 · 星期四', '11/26',
    '🔬 手套为什么暖（0-1岁）', 'zh',
    '手套摸起来软软的，戴上暖暖的。和毯子一样，手套也是「锁空气小能手」：棉花和绒毛里藏着许多小空气袋，把手的温度留在里面。',
    '手套的纤维兜住一层薄薄的空气，手把空气焐热，热空气不流动，就像给手穿了件小棉袄——所以摘下手套，手还是热乎乎的。',
    ['小手套，软软的。','戴上，暖暖的。','它为什么这么暖？','和毯子一样，','手套会锁空气！','棉花和绒毛里，','藏着许多小空气袋。','小手伸进去，','把手套里的空气焐热。','热空气待在纤维里不动，','像给手穿了件小棉袄。','冷风想吹小手？','先问过空气袋再说！','摘下手套，','手还是热乎乎的——','那是空气袋留下的暖。'], sci=True))
DEC5.append(S('2026-11-26-science-en', 'November 26, 2026 · Thursday', '11/26',
    '🔬 Science Story (0-1 yr): Why Mittens Keep Hands Warm', 'en',
    'Mittens feel soft and keep hands warm. Like blankets, mittens are air-lockers: the cotton and fuzz hold tiny air pockets that keep the hand\'s warmth inside.',
    'The fibers trap a thin layer of air; the hand warms it, and still air blocks the cold — like a tiny padded coat. Take mittens off: hands stay toasty.',
    ['Little mittens, soft and light.','Put them on — warm and cozy!','Why are they so warm?','Just like blankets,','mittens lock the air!','Inside the cotton and fuzz,','hide many tiny air pockets.','The little hand slides in,','warming the trapped air.','The warm air stays still in the fibers,','like a tiny padded coat for the hand.','Cold wind wants in?','Ask the air pockets first!','Mittens off —','hands still toasty —','the air pockets left their warmth.']))
