# -*- coding: utf-8 -*-
# 11-04 ~ 11-07（11-04/05/07 撞自动化 base id → cn/en 用 -2；11-06 科学也撞 → -2）
DEC1 = []

def S(id_, date, ds, title, lang, preview, moral, content, sci=False):
    d = {'id': id_, 'date': date, 'dateShort': ds, 'title': title, 'language': lang,
         'ageGroup': '0-1', 'ageLabel': '0-1岁', 'preview': preview, 'moral': moral,
         'content': content, 'category': 'science' if sci else 'regular'}
    if sci:
        d['series'] = 'science'; d['seriesTitle'] = '科学故事'
        d['source'] = 'Children science common sense' if lang == 'en' else '儿童科普常识'
    return d

# ---------- 11-04 周三 ----------
DEC1.append(S('2026-11-04-cn-2', '2026年11月4日 · 星期三', '11/04',
    '小袜子去哪儿了（0-1岁）', 'zh',
    '换尿布的时候，妈妈发现少了一只小袜子。找呀找，床底下没有，摇篮底下也没有。咦，小熊的耳朵上，怎么有点点蓝？',
    '找不到东西不着急，慢慢找、仔细看，它就在不远处等着你呢。',
    ['换尿布的时间到啦。','妈妈拿起小袜子，一只，两只……','咦？怎么只有一只？','另一只小袜子去哪儿了？','妈妈掀开小被子——没有。','妈妈看看摇篮底下——没有。','宝宝躺在旁边，眼睛跟着妈妈转。','找呀找，找呀找。','咦？小熊的耳朵上，怎么有点点蓝？','妈妈凑近一看，笑出了声。','原来小袜子套在了小熊耳朵上！','昨天玩游戏的时候，它悄悄躲上去的。','妈妈把小袜子取下来，亲亲宝宝的脚丫。','小袜子找到啦，小脚丫暖乎乎。']))
DEC1.append(S('2026-11-04-en-2', 'November 4, 2026 · Wednesday', '11/04',
    'Where Is My Sock? (0-1 yr)', 'en',
    'Mommy finds only ONE little sock. Where is the other one? Under the bed — no. Under the crib — no. Look! Something blue on the teddy\'s ear!',
    'Do not rush when things are lost. Look slowly and carefully — they are waiting nearby.',
    ['Diaper time, sock time.','One little sock... two?','Only one! Where is the other?','Under the bed — no.','Under the crib — no.','Baby watches Mommy search.','Look! On the teddy\'s ear,','something small and blue!','Mommy laughs out loud.','The sock played hide-and-seek!','Off it comes, gently.','Warm little toes again!']))
DEC1.append(S('2026-11-04-science-cn', '2026年11月4日 · 星期三', '11/04',
    '🔬 为什么会打嗝（0-1岁）', 'zh',
    '宝宝喝着喝着奶，忽然 hic！hic！打起嗝来。小肚子一跳一跳的，真好玩。这是横膈膜在锻炼身体呢。',
    '打嗝是横膈膜（胸腔下的大肌肉）突然抽动引起的。它一抽，气就快速冲出来，发出 hic 的声音——多数时候是吃得急了或吸了点空气。',
    ['喝奶喝得好开心。','咦？hic！','又来，hic！','小肚子一跳一跳。','为什么打嗝呀？','胸腔下面有块大肌肉，','叫横膈膜，管呼吸的。','它忽然抽了一下，','气就冲出来——hic！','吃得急了，它会这样。','拍拍背，慢慢就好啦。','打嗝不可怕，是身体在练习呢。'], sci=True))
DEC1.append(S('2026-11-04-science-en', 'November 4, 2026 · Wednesday', '11/04',
    '🔬 Science Story (0-1 yr): Why Do We Hiccup?', 'en',
    'Baby is drinking milk when — hic! hic! The tummy jumps a little. Fun! The big breathing muscle is just exercising.',
    'Hiccups happen when the diaphragm — the big muscle under your lungs — twitches suddenly. Air rushes out and goes hic!',
    ['Drinking milk, so happy.','Hic!','Hic again!','The tummy jumps and jumps.','Why do we hiccup?','Under your lungs lives a big muscle.','It is called the diaphragm.','It helps you breathe.','Sometimes it twitches — hic!','Air rushes out fast.','Pat, pat the back.','Hiccups are just practice!'], sci=True))

# ---------- 11-05 周四 ----------
DEC1.append(S('2026-11-05-cn-2', '2026年11月5日 · 星期四', '11/05',
    '声音躲猫猫（0-1岁）', 'zh',
    '「叮咚——」门铃响了。宝宝的小脑袋「唰」地转向门口。声音在跟宝宝玩躲猫猫：找找我在哪儿？',
    '宝宝会循声转头了！小脑袋转向哪里，注意力就长在哪里——这是听觉和眼睛一起做的游戏。',
    ['宝宝躺在爬行垫上。','「叮咚——」门铃响了！','小脑袋，唰地转向门口。','咦，声音从那边来的？','「叮铃铃——」电话响了。','小脑袋，又转向电话。','「哗啦啦——」爸爸在厨房倒水。','小脑袋，再转过去。','声音真调皮，','一会儿在这边，一会儿在那边。','宝宝的小脑袋，转呀转。','找到啦，找到啦！','声音躲猫猫，宝宝每次都赢。']))
DEC1.append(S('2026-11-05-en-2', 'November 5, 2026 · Thursday', '11/05',
    'What Was That Sound? (0-1 yr)', 'en',
    'Ding-dong! The doorbell rings. Baby\'s head turns — whoosh! Sounds love to play hide-and-seek with baby.',
    'Turning toward a sound is how baby\'s ears and eyes play together. Every turn is a little win.',
    ['Baby lies on the play mat.','Ding-dong! The doorbell!','Whoosh — the head turns to the door.','Where did that come from?','Ring-ring! The telephone!','The head turns again.','Glug-glug — Daddy pours water.','The head turns once more.','Sounds are playful,','here and there and everywhere.','Baby\'s little head goes round.','Found it! Found it!','Baby wins every time!']))
DEC1.append(S('2026-11-05-science-cn', '2026年11月5日 · 星期四', '11/05',
    '🔬 声音怎么传到耳朵里（0-1岁）', 'zh',
    '门铃在门口响，宝宝在房间里却听得见。因为声音会坐着「空气波浪」旅行：一圈一圈，从门口荡到宝宝耳朵里。',
    '发声的东西会让空气一圈圈振动（像水面涟漪），振动传进耳朵，耳朵里的小鼓膜跟着抖，我们就听见声音了。',
    ['门铃在门口唱歌。','宝宝在房间，也听见了。','声音是怎么来的呀？','它坐上「空气波浪」。','一圈，一圈，又一圈。','像小石子掉进水里，','水面上荡开一圈圈涟漪。','空气的涟漪飘进耳朵。','耳朵里有面小鼓膜，','跟着一抖一抖。','咚咚咚——听见啦！','原来声音会旅行呀。'], sci=True))
DEC1.append(S('2026-11-05-science-en', 'November 5, 2026 · Thursday', '11/05',
    '🔬 Science Story (0-1 yr): How Sound Travels', 'en',
    'The doorbell sings at the door, but baby hears it in the room. Sound rides on invisible air waves — round and round they travel!',
    'Things that make sound shake the air in little waves, like ripples on water. The waves reach your eardrum and wiggle it — that is hearing!',
    ['The doorbell sings at the door.','Baby hears it far away.','How does sound travel?','It rides on air waves!','Round, round, round they go.','Like a pebble dropped in water,','ripples spread out in circles.','The air ripples float to the ear.','Inside, a tiny eardrum waits.','Wiggle, wiggle — we hear it!','Sound is a little traveler.'], sci=True))

# ---------- 11-06 周五 ----------
DEC1.append(S('2026-11-06-cn-2', '2026年11月6日 · 星期五', '11/06',
    '小手抓抓抓（0-1岁）', 'zh',
    '妈妈把摇铃放到宝宝手边。小手张开，够呀够——碰到了！手指一根一根收拢，握住啦！摇铃沙沙响，宝宝的第一个「抓住」。',
    '从碰到握住，小手练习了成百上千次。每一次抓握，都是宝宝向世界伸出的一个小小的「你好」。',
    ['摇铃，躺在宝宝手边。','红红的，带一圈小珠子。','小手张开来。','够呀，够呀。','指尖碰到了！','又滑掉了……','再来。小手，张开。','一根手指，两根手指，','三根、四根、五根——','慢慢地，收拢，握住！','小手晃一晃，沙沙沙！','珠子唱歌啦！','宝宝举着自己的小手，','好像在说：我抓住啦！','第一个「抓住」，真了不起。']))
DEC1.append(S('2026-11-06-en-2', 'November 6, 2026 · Friday', '11/06',
    'Grab the Rattle! (0-1 yr)', 'en',
    'Mommy puts the rattle near baby\'s hand. Little fingers open, reach... touch! They close — got it! The rattle sings: sha-sha-sha!',
    'From touching to holding takes many tries. Every grasp is baby\'s little "hello" to the world.',
    ['The rattle waits by baby\'s hand.','Red and shiny, with little beads.','The little hand opens.','Reach, reach, reach...','Fingertips touch it!','Oops — it slips away.','Try again. Open wide.','One finger, two fingers,','three, four, five —','slowly close... Got it!','Shake, shake — sha-sha-sha!','The beads are singing!','Baby lifts the little fist:','I did it!']))
DEC1.append(S('2026-11-06-science-cn-2', '2026年11月6日 · 星期五', '11/06',
    '🔬 小手为什么能抓住东西（0-1岁）', 'zh',
    '小手能张开、能握拢，还能捏起小小的珠子——因为手上有很多很多小肌肉，每根手指都听大脑的指挥。',
    '手是全身骨头最集中的地方之一：27 块小骨头配许多小肌肉。大脑发令，肌肉拉动骨头，手指就弯起来——抓住东西是手、眼、脑一起完成的 teamwork。',
    ['小手，张一张，握一握。','还能捏起小珠子呢。','为什么这么灵巧？','手上住着好多小肌肉。','每根手指都听大脑的话。','大脑说：弯！手指就弯。','大脑说：松！手指就张开。','手心里还有 27 块小骨头，','像 27 个小零件，配合得可好了。','眼睛看到摇铃，','大脑发命令，小手去抓。','抓住东西，是三个小伙伴一起干的活儿。'], sci=True))
DEC1.append(S('2026-11-06-science-en-2', 'November 6, 2026 · Friday', '11/06',
    '🔬 Science Story (0-1 yr): How Hands Grab Things', 'en',
    'Little hands can open, close, and even pinch a tiny bead! Many small muscles live inside, and every finger listens to the brain.',
    'Each hand has 27 tiny bones and lots of little muscles. Brain gives the order, muscles pull, fingers bend — grabbing is teamwork of hand, eye, and brain.',
    ['Open, close — little hand!','It can even pinch a bead!','Why so clever?','Many small muscles live inside.','Every finger obeys the brain.','Brain says bend — fingers bend.','Brain says open — fingers open.','Inside the palm: 27 tiny bones,','27 little parts working together.','Eyes spot the rattle,','the brain sends the order,','the hand reaches out. Teamwork!']))
DEC1.append(S('2026-11-06-science-cn', '2026年11月6日 · 星期五', '11/06',
    '🔬 冬天的风为什么冷（0-1岁）', 'zh',
    '夏天吹来的风暖暖的，冬天吹来的风凉凉的。风还是风，为什么温度不一样？因为它带来的空气老家不同。',
    '冬天风从很冷的北方吹来，夏天风从温热的南方吹来——风像邮递员，送来的「空气包裹」产地不一样，摸起来就不一样。',
    ['夏天的风，暖暖的。','冬天的风，凉凉的。','都是风，不一样吗？','看它从哪里来呀。','冬天的风，从北方的冰雪国来。','一路上，空气变得冷冷的。','它跑过来，蹭蹭小脸——','好凉呀，缩缩脖子。','夏天的风从温热的南方来，','暖乎乎的。','风是空气邮递员，','包裹的产地不同，温度也不同。'], sci=True))
DEC1.append(S('2026-11-06-science-en', 'November 6, 2026 · Friday', '11/06',
    '🔬 Science Story (0-1 yr): Why Winter Wind Is Cold', 'en',
    'Summer wind feels warm; winter wind feels cold. Wind is wind — why different? It depends on where the wind comes from!',
    'Winter wind travels from the icy north, summer wind from the warm south. Wind is an air postman — the parcel\'s hometown sets the temperature.',
    ['Summer wind — warm and soft.','Winter wind — cold and crisp!','Same wind, different feel?','Look where it comes from.','Winter wind starts in the icy north.','On the way, air turns cold.','It rushes here and taps your cheek —','brr! Tuck in your chin.','Summer wind comes from the warm south.','Warm as a hug.','Wind is an air postman —','the hometown decides the temperature!']))

# ---------- 11-07 周六 ----------
DEC1.append(S('2026-11-07-cn-2', '2026年11月7日 · 星期六', '11/07',
    '会唱歌的澡盆（0-1岁）', 'zh',
    '爸爸拿来小水瓢。舀一瓢水，浇在宝宝的小脚丫上——哗啦啦！澡盆唱歌了。宝宝蹬蹬腿，水花跳起舞，澡盆唱得更欢。',
    '洗澡不只是洗澡，是水和声音的游戏。笑声加水声，是澡盆里最好听的二重唱。',
    ['傍晚，澡盆装满了温水。','小黄鸭先下水，摇摇晃晃。','爸爸拿来小水瓢。','舀一瓢水，举高高。','哗啦啦——浇在小脚丫上！','澡盆唱歌了！','宝宝咯咯笑，蹬蹬腿。','水花跳起来，噼里啪啦。','再舀一瓢，哗啦啦——','这次浇在小肚肚上。','澡盆唱得更欢了。','小黄鸭被水波推得转圈圈。','爸爸唱：哗啦哗啦洗澡歌。','宝宝跟着「啊——啊——」和声。','笑声加水声，澡盆二重唱！']))
DEC1.append(S('2026-11-07-en-2', 'November 7, 2026 · Saturday', '11/07',
    'Splish Splash Song (0-1 yr)', 'en',
    'Daddy lifts a little cup of water. Splish-splash — onto baby\'s toes! The bathtub starts singing. Baby kicks, and the song gets louder!',
    'Bath time is water-and-sound play. Laughter plus splashes — the bathtub\'s favorite duet.',
    ['Evening — the tub is warm.','Little duck floats, bob, bob.','Daddy takes a little cup.','Scoops some water, up it goes.','Splish-splash — on the toes!','The bathtub sings!','Baby giggles and kicks.','Splashes jump — pit-a-pat!','One more cup, splish-splash —','this time on the little tummy.','The song grows louder.','Duck spins in the waves.','Daddy sings the splash song,','baby joins: ah — ah —!','Bath time duet!']))
DEC1.append(S('2026-11-07-science-cn', '2026年11月7日 · 星期六', '11/07',
    '🔬 浇水时为什么咕嘟咕嘟冒泡（0-1岁）', 'zh',
    '把水瓢倒扣进澡盆，咕嘟、咕嘟，水下冒出一串泡泡。那是被困住的空气在急着逃出来呢！',
    '水瓢扣下去时兜住了空气，水从四面八方围过来挤它，空气就变成一串泡泡钻出水面——咕嘟咕嘟，是空气的逃跑声。',
    ['小水瓢，扣进水里。','咕嘟，咕嘟，咕嘟！','水下冒泡泡啦。','泡泡是什么呀？','是被水抓住的空气！','水瓢扣下去，兜住一包空气。','水从四面八方围过来。','空气着急了：放我出去！','它变成一串小泡泡，','咕嘟咕嘟往上钻。','啵！啵！冲出水面。','原来泡泡是空气在逃跑呀。'], sci=True))
DEC1.append(S('2026-11-07-science-en', 'November 7, 2026 · Saturday', '11/07',
    '🔬 Science Story (0-1 yr): Why Bubbles Gurgle Up', 'en',
    'Press the cup into the water — glug, glug, glug! Bubbles rush up. That is trapped air escaping in a hurry!',
    'The cup traps air underwater. Water squeezes it from all sides, so the air turns into bubbles and zooms to the surface.',
    ['The cup goes into the water.','Glug, glug, glug!','Bubbles rise below!','What are bubbles?','Air caught by the water!','The cup trapped a pocket of air.','Water closes in from all sides.','The air shouts: let me out!','It becomes a chain of bubbles,','zooming up, up, up.','Pop! Pop! Out of the water.','Bubbles are escaping air!'], sci=True))
