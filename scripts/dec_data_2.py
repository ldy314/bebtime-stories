# -*- coding: utf-8 -*-
# 11-08 ~ 11-12（11-08/09/10 撞 base id → cn/en 用 -2）
DEC2 = []

def S(id_, date, ds, title, lang, preview, moral, content, sci=False):
    d = {'id': id_, 'date': date, 'dateShort': ds, 'title': title, 'language': lang,
         'ageGroup': '0-1', 'ageLabel': '0-1岁', 'preview': preview, 'moral': moral,
         'content': content, 'category': 'science' if sci else 'regular'}
    if sci:
        d['series'] = 'science'; d['seriesTitle'] = '科学故事'
        d['source'] = 'Children science common sense' if lang == 'en' else '儿童科普常识'
    return d

# ---------- 11-08 周日 ----------
DEC2.append(S('2026-11-08-cn-2', '2026年11月8日 · 星期日', '11/08',
    '谁在敲门（0-1岁）', 'zh',
    '咚咚咚！有人敲门。咚咚咚！还在敲。妈妈抱着宝宝去开门——哇，是外公！外公从老远老远的地方来看宝宝啦。',
    '咚咚的敲门声背后，常常藏着想念你的人。开门的瞬间，是最快乐的时刻。',
    ['吃过早饭，阳光爬上窗台。','咚咚咚！有人在敲门。','宝宝的小脑袋转向大门。','咚咚咚！还在敲。','是谁呀？声音这么响。','妈妈抱起宝宝：走，看看去。','脚步哒哒哒，心跳咚咚咚。','妈妈转动门把手——','哇！是外公！','外公的眉毛上还带着路上的风霜，','手里拎着一大袋家乡的土产。','外公张开手臂：我的小宝贝！','宝宝看着外公，眼睛睁得圆圆的。','这个声音有点耳熟——是视频里天天见的那个声音呀！','外公亲亲宝宝的小额头。','咚咚的敲门声背后，是想念宝宝的人。']))
DEC2.append(S('2026-11-08-en-2', 'November 8, 2026 · Sunday', '11/08',
    'Knock, Knock, Who Is It? (0-1 yr)', 'en',
    'Knock knock! Someone is at the door. Knock knock! Again. Mommy opens it — it is Grandpa! He came from far, far away to see baby.',
    'Behind a knocking door is often someone who misses you. Opening the door is the happiest moment.',
    ['Breakfast done, sun on the sill.','Knock knock! Someone is there.','Baby\'s head turns to the door.','Knock knock! Again!','Who can it be?','Mommy lifts baby: let\'s see!','Steps go tap-tap, heart goes thump-thump.','Mommy turns the handle —','it is Grandpa!','Frost of the road on his eyebrows,','a big bag of hometown treats in his arms.','Grandpa opens his arms: my little one!','Baby stares, big round eyes.','That voice — the one from video calls every day!','Grandpa kisses baby\'s forehead.']))
DEC2.append(S('2026-11-08-science-cn', '2026年11月8日 · 星期日', '11/08',
    '🔬 门铃为什么会唱歌（0-1岁）', 'zh',
    '手指按一下小按钮，「叮咚——」门铃就唱歌。门铃里藏着什么小秘密？原来按钮连着一根看不见的电线。',
    '按下按钮，电流就顺着电线跑起来，让门铃里的小铃铛（或小喇叭）振动发声。手指一松，电流断掉，歌声就停——按钮是歌声的开关。',
    ['「叮咚——」门铃唱歌啦。','谁在让它唱呀？','是一个小按钮。','手指按下去——叮咚！','松开来——歌声停了。','按钮里有什么魔法？','没有魔法，有电宝宝！','按钮连着一根看不见的电线。','一按，电宝宝就跑起来，','跑过电线，敲响小铃铛。','铃铛一振动，叮咚——','一松手，电宝宝回家休息，','歌声也休息啦。'], sci=True))
DEC2.append(S('2026-11-08-science-en', 'November 8, 2026 · Sunday', '11/08',
    '🔬 Science Story (0-1 yr): Why the Doorbell Sings', 'en',
    'Press the little button — ding-dong! The doorbell sings. What is the secret? A button, a wire, and invisible electricity!',
    'Pressing the button lets electricity run along the wire and shake the little bell. Let go, the flow stops, the song stops. The button is the song\'s switch.',
    ['Ding-dong! The doorbell sings.','Who is making it sing?','A little button.','Press it — ding-dong!','Let go — the song stops.','Is there magic inside?','No magic — electricity!','The button connects to a hidden wire.','Press, and electricity runs,','along the wire, ringing the bell.','The bell vibrates — ding-dong!','Let go, electricity rests,','and so does the song.']))

# ---------- 11-09 周一 ----------
DEC2.append(S('2026-11-09-cn-2', '2026年11月9日 · 星期一', '11/09',
    '小镜子不见了（0-1岁）', 'zh',
    '宝宝最爱的小镜子不见了！昨天还挂在摇篮边。找呀找——原来被晾起来的小毛巾盖住了。掀开毛巾，镜子里立刻出现一个宝宝：你也在这里找镜子吗？',
    '东西「不见了」，常常只是被藏起来了。掀开谜底的一刻，多像变魔术呀。',
    ['早上醒来，宝宝想照镜子。','咦？摇篮边空空的。','小镜子去哪儿了？','宝宝伸长脖子看——没有。','小手抓抓床单——没有。','妈妈走来：找什么呢？','哦——妈妈知道了。','昨晚洗好的小毛巾，','正好晾在镜子前面。','妈妈轻轻掀开毛巾——','镜子里立刻出现一个宝宝！','宝宝笑了：你也在这里找镜子吗？','两个宝宝，一起笑。','原来小镜子没有走，','只是跟毛巾玩了一晚上捉迷藏。']))
DEC2.append(S('2026-11-09-en-2', 'November 9, 2026 · Monday', '11/09',
    'Peek-a-Boo Towel (0-1 yr)', 'en',
    'Baby\'s favorite mirror is gone! It hung by the crib yesterday. Where is it? Look — a fresh towel is covering it! Lift the towel: hello, mirror baby!',
    'Things that "disappear" are often just hidden. Lifting the mystery away feels like magic.',
    ['Morning — baby wants the mirror.','Huh? The spot by the crib is empty.','Where did the mirror go?','Stretch the neck — not there.','Grab the sheet — not there.','Mommy comes: what are you looking for?','Oh — now she knows.','Last night\'s clean little towel,','hung right in front of the mirror.','Mommy lifts it gently —','a baby appears in the mirror at once!','Baby laughs: are you looking too?','Two babies laughing together.','The mirror never left —','it played hide-and-seek all night.']))
DEC2.append(S('2026-11-09-science-cn', '2026年11月9日 · 星期一', '11/09',
    '🔬 为什么看不见风（0-1岁）', 'zh',
    '风呼呼地吹，可是伸出手，什么都抓不到。风明明在，为什么看不见？因为风是流动的空气，空气是透明的。',
    '空气没有颜色，所以眼睛看不见它。但树叶摇晃、旗帜飘动、头发飞起来，都是风在告诉大家：我在这儿！',
    ['窗外，呼——呼——','风来啦。','伸出手抓一抓。','咦？什么也没抓到。','风明明在吹呀！','为什么看不见它？','因为风是流动的空气，','空气是透明的，','像一层看不见的玻璃。','可是树叶在摇——那是风。','旗帜在飘——那是风。','头发飞起来——也是风。','眼睛看不见风，','但风会用它的办法打招呼。'], sci=True))
DEC2.append(S('2026-11-09-science-en', 'November 9, 2026 · Monday', '11/09',
    '🔬 Science Story (0-1 yr): Why We Cannot See Wind', 'en',
    'Whoosh — the wind blows! Stretch out your hand... nothing to grab. Wind is there, but why can\'t we see it? Wind is moving air, and air is transparent.',
    'Air has no color, so eyes cannot catch it. But swaying leaves, flying flags, and floating hair all shout: wind is here!',
    ['Whoosh — whoosh — outside!','The wind is here.','Grab it with your hand...','nothing there!','But the wind IS blowing!','Why can\'t we see it?','Wind is moving air,','and air is transparent —','like invisible glass.','But the leaves are swaying — that is wind.','The flag is flying — that is wind.','Baby\'s hair floats up — wind again!','Eyes cannot see wind,','but wind says hello its own way.']))

# ---------- 11-10 周二 ----------
DEC2.append(S('2026-11-10-cn-2', '2026年11月10日 · 星期二', '11/10',
    '毛衣上的小羊（0-1岁）', 'zh',
    '天冷了，妈妈给宝宝穿上厚毛衣。毛衣上绣着一只卷卷毛的小羊。宝宝摸一摸：软软的。小羊住在毛衣上，暖暖地陪着宝宝过冬。',
    '毛衣是小羊的毛织成的——穿在身上的，是羊毛送来的冬天的礼物。',
    ['呼呼，天冷了。','妈妈拿来厚毛衣。','蓝色的，软软的，','胸口绣着一只小羊。','白白卷卷，像个云朵球。','宝宝伸手摸一摸。','咦，软软的，暖暖的。','妈妈把宝宝的小手放进袖子里。','暖流顺着袖子爬上来。','妈妈说：这只小羊，','住在一座山坡上，','它的毛卷卷的，冬天也不怕冷。','剪下羊毛，纺成毛线，','织呀织，织成宝宝的毛衣。','所以毛衣这么暖呀——','是小羊把它的暖，送给了宝宝。','宝宝摸摸小羊：谢谢你呀。']))
DEC2.append(S('2026-11-10-en-2', 'November 10, 2026 · Tuesday', '11/10',
    'The Little Lamb on the Sweater (0-1 yr)', 'en',
    'It is cold. Mommy puts a thick sweater on baby. A curly little lamb is knitted on the front. Touch it — so soft. The lamb will keep baby warm all winter.',
    'Sweaters are made of sheep\'s wool — winter\'s gift from the sheep, worn on the body.',
    ['Whoosh — it is getting cold.','Mommy brings the thick sweater.','Blue and soft,','with a little lamb on the chest.','White and curly, like a cloud ball.','Baby reaches out to touch.','Soft... and warm.','Little hand slides into the sleeve.','Warmth climbs up the arm.','Mommy says: this lamb,','lives on a green hillside.','Its wool is curly — it never fears winter.','Wool is cut and spun into yarn,','knit and knit — a sweater for baby!','That is why sweaters are so warm —','the lamb gave its warmth to you.','Baby pats the lamb: thank you!']))
DEC2.append(S('2026-11-10-science-cn', '2026年11月10日 · 星期二', '11/10',
    '🔬 水壶为什么会呜呜叫（0-1岁）', 'zh',
    '炉子上的水壶烧着烧着，呜——呜——叫起来了。水又没有嘴巴，是谁在唱歌？是水蒸气从壶嘴的小口里冲出来！',
    '水烧开后变成水蒸气，水蒸气从壶嘴的小口用力挤出去，振动得很快很快，就发出呜呜的哨音——壶盖还会被顶得一跳一跳。',
    ['炉子上，大水壶。','火苗舔着壶底。','咕嘟，咕嘟，水里冒泡。','呜——呜——','水壶叫起来啦！','水又没有嘴巴，','是谁在唱歌？','是水蒸气呀！','水烧开了，变成水蒸气。','水蒸气从壶嘴的小口往外挤。','口子小，力气大，','抖得飞快飞快——','呜——哨音就出来了。','壶盖也被顶得一跳一跳。','快来看，水开了！'], sci=True))
DEC2.append(S('2026-11-10-science-en', 'November 10, 2026 · Tuesday', '11/10',
    '🔬 Science Story (0-1 yr): Why the Kettle Whistles', 'en',
    'The kettle on the stove goes woo — woo —! Water has no mouth, so who is singing? It is the steam squeezing out of the tiny spout!',
    'Boiling water turns into steam. Steam forces through the small spout and vibrates very fast — that makes the whistle. The lid dances too!',
    ['On the stove sits the kettle.','Flames lick its bottom.','Glug, glug — bubbles inside.','Woo — woo —','the kettle sings!','Water has no mouth,','so who is the singer?','It is the steam!','Boiling water becomes steam.','Steam squeezes out of the tiny spout.','Small hole, strong push,','vibrating very, very fast —','woo! The whistle sounds.','The lid hops up and down.','Quick — the water is boiling!']))

# ---------- 11-11 周三 ----------
DEC2.append(S('2026-11-11-cn', '2026年11月11日 · 星期三', '11/11',
    '咕噜噜肚子叫（0-1岁）', 'zh',
    '玩着玩着，宝宝的小肚子「咕噜噜」叫了。咦，是谁在肚子里说话？原来是肚子在提醒：该喝奶啦！',
    '咕噜噜是小肚子的语言。听懂身体的声音，就知道什么时候该吃饭、该睡觉了。',
    ['宝宝趴在垫子上玩摇铃。','玩着玩着——','咕噜噜，咕噜噜。','咦？什么声音？','宝宝停下来，眨眨眼。','小手拍拍肚子。','咕噜噜，又叫了。','是谁在肚子里说话呀？','妈妈笑着走过来：','是肚子在说话呢！','它说：宝宝玩饿了，','该喝奶啦，该喝奶啦。','妈妈抱起宝宝，冲好温温的奶。','咕嘟咕嘟，咕嘟咕嘟。','小肚子不叫了，','暖暖的，饱饱的。','咕噜噜是小肚子的语言，','听懂它，就是好宝宝。']))
DEC2.append(S('2026-11-11-en', 'November 11, 2026 · Wednesday', '11/11',
    'Tummy Says Growl (0-1 yr)', 'en',
    'Playing, playing — and then: gurgle, gurgle! Who is talking inside the tummy? The tummy is reminding: time for milk!',
    'Gurgle-gurgle is the tummy\'s language. Understanding your body\'s sounds tells you when to eat and when to sleep.',
    ['Baby plays with the rattle.','Playing, playing —','gurgle, gurgle!','Huh? What was that?','Baby stops and blinks.','Pats the little tummy.','Gurgle — again!','Who is talking in there?','Mommy comes over, smiling:','that is your tummy talking!','It says: baby is hungry,','time for milk, time for milk!','Mommy hugs baby, warm milk ready.','Glug, glug, glug.','The tummy stops growling,','warm and full.','Gurgle is the tummy\'s language,','and baby understands!']))
DEC2.append(S('2026-11-11-science-cn', '2026年11月11日 · 星期三', '11/11',
    '🔬 肚子为什么会咕噜叫（0-1岁）', 'zh',
    '肚子饿的时候，咕噜噜、咕噜噜。其实不是肚子在喊饿，是肚子里的小肠在蠕动——工作时推来推去，把气体和液体挤得咕噜响。',
    '肠胃一直在慢慢蠕动帮食物往前走。饿的时候里面只剩气体和液体，蠕动一挤，就发出咕噜噜的声音——是肠胃在工作呢。',
    ['肚子饿的时候，','咕噜噜，咕噜噜。','是肚子在喊「饿」吗？','不是哦。','肚子里有一根长长的小肠，','它一直在慢慢蠕动，','把食物一点点往前推。','吃饱时，里面满满的，','声音小小的。','饿的时候，里面只剩气体和水，','一挤——咕噜噜！','响亮的大合唱！','原来咕噜声，','是肠胃工作的声音呀。'], sci=True))
DEC2.append(S('2026-11-11-science-en', 'November 11, 2026 · Wednesday', '11/11',
    '🔬 Science Story (0-1 yr): Why Tummies Growl', 'en',
    'When baby is hungry: gurgle, gurgle! It is not the tummy shouting — it is the long small intestine squeezing gas and liquid as it works.',
    'Guts always wiggle slowly to push food along. When empty, only gas and liquid are inside — squeezing them makes the loud growl.',
    ['When the tummy is hungry,','gurgle, gurgle, gurgle!','Is the tummy shouting "food"?','Not really.','Inside lives a long small intestine,','always wiggling slowly,','pushing food little by little.','When full, everything is packed,','so the sound is small.','When empty, only gas and liquid remain,','one squeeze — GURGLE!','A loud little chorus!','Growls are just the guts at work.']))

# ---------- 11-12 周四 ----------
DEC2.append(S('2026-11-12-cn', '2026年11月12日 · 星期四', '11/12',
    '窗台上的麻雀（0-1岁）', 'zh',
    '窗外的小麻雀蹦蹦跳跳，啄一啄，跳一跳，又一啄。它从来不迈步走，只会两脚一起蹦。宝宝趴在窗台边看呆了：小麻雀，你为什么不用走路呀？',
    '麻雀双脚齐蹦，是它独特的移动方式。世界上每个小家伙，都有自己的办法。',
    ['上午的窗台，热闹了。','一只小麻雀跳上来。','褐色的羽毛，圆滚滚的身子。','它啄一啄面包屑。','跳一跳，再啄一啄。','咦？宝宝趴在窗边看呆了。','小麻雀不会走路呀！','它总是两脚一起蹦：','蹦——啄，蹦——啄。','像个小皮球，一弹一弹。','一只鸽子慢悠悠走过，一步，一步。','小麻雀还是蹦蹦跳跳。','蹦，蹦，蹦，','小脑袋一点一点的，','像在给音乐打拍子。','面包屑吃完，扑棱棱飞走啦。','再见，蹦蹦跳跳的小麻雀。']))
DEC2.append(S('2026-11-12-en', 'November 12, 2026 · Thursday', '11/12',
    'Little Sparrow, Hop Hop (0-1 yr)', 'en',
    'A little sparrow lands outside the window. Peck, hop, peck! It never walks — it always hops with both feet together. Baby watches, amazed.',
    'Sparrows hop instead of walk — their own special way to move. Every little creature has its own way.',
    ['Morning — the windowsill is busy.','A little sparrow hops up.','Brown feathers, round little body.','Peck at the bread crumbs.','Hop, peck! Hop, peck!','Baby stares from the window.','The sparrow never walks!','Both feet jump together:','hop — peck, hop — peck.','Like a tiny ball, bounce and bounce.','A pigeon strolls by, step... step...','The sparrow just keeps hopping.','Hop, hop, hop,','head bobbing like a little beat,','drumming to its own music.','Crumbs all gone — away it flies!','Bye-bye, hopping sparrow.']))
DEC2.append(S('2026-11-12-science-cn', '2026年11月12日 · 星期四', '11/12',
    '🔬 麻雀为什么蹦着走（0-1岁）', 'zh',
    '鸽子迈着步子走，麻雀却两脚一起蹦。不是麻雀不会走，是它的小短腿蹦起来更快、更省力。',
    '麻雀的腿短，迈步走路又慢又费劲；双脚同时蹬地跳，又快又灵活，还方便随时起飞——蹦跳是短腿小鸟的聪明选择。',
    ['鸽子走路：一步，一步。','麻雀走路：蹦！蹦！','两脚一起跳，不迈步。','是它不会走吗？','不是哦。','麻雀的小腿短短的。','迈步走，又慢又费劲。','双脚一起蹬地蹦，','又快又灵活！','蹦一下，就前进一小段。','遇到危险？','再蹦一下，扑棱——飞啦！','蹦跳，是短腿小鸟的聪明办法。'], sci=True))
DEC2.append(S('2026-11-12-science-en', 'November 12, 2026 · Thursday', '11/12',
    '🔬 Science Story (0-1 yr): Why Sparrows Hop', 'en',
    'Pigeons walk step by step, but sparrows hop with both feet! Not because they cannot walk — short legs hop faster and save energy.',
    'Sparrows have short legs; walking is slow and tiring for them. Hopping with both feet is quick, nimble, and ready for takeoff anytime.',
    ['Pigeons walk: step... step...','Sparrows go: hop! hop!','Both feet jump together.','Can\'t sparrows walk?','They can!','But sparrow legs are short.','Walking is slow and tiring.','Hopping with both feet,','is fast and nimble!','One hop — a little leap forward.','Danger?','Another hop — flap — fly away!','Hopping is the short-legged bird\'s smart trick.']))
