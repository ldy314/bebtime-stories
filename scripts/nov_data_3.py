# -*- coding: utf-8 -*-
# 10-26 ~ 10-29 每日中英 + 中英科学
D3 = []

def S(id_, date, ds, title, lang, preview, moral, content, sci=False):
    d = {'id': id_, 'date': date, 'dateShort': ds, 'title': title, 'language': lang,
         'ageGroup': '0-1', 'ageLabel': '0-1岁', 'preview': preview, 'moral': moral,
         'content': content, 'category': 'science' if sci else 'regular'}
    if sci:
        d['series'] = 'science'; d['seriesTitle'] = '科学故事'
        d['source'] = 'Children science common sense' if lang == 'en' else '儿童科普常识'
    return d

# ---------- 10-26 周一 ----------
D3.append(S('2026-10-26-cn', '2026年10月26日 · 星期一', '10/26',
    '小猫走路静悄悄（0-1岁）', 'zh',
    '小猫走路，静悄悄。肉垫踩地板，一点声音都没有。它踮着脚，轻轻路过宝宝身边。',
    '小猫的肉垫是自带的小鞋子，软软的、悄悄的。轻轻走路，也是一种温柔。',
    ['小猫，来啦。','走路，静悄悄。','肉垫踩地板，没有声。','一步，两步，踮着脚。','路过宝宝身边。','尾巴弯弯，问声好。','宝宝眨眨眼：咦？','小猫已坐到窗台上。','悄悄的猫，悄悄的陪伴。']))
D3.append(S('2026-10-26-en', 'October 26, 2026 · Monday', '10/26',
    'Quiet Little Cat (0-1 yr)', 'en',
    'The little cat walks so quietly. Soft paws make no sound at all. Tip-toe, tip-toe, past the baby.',
    'A cat\'s soft pads are little built-in shoes. Walking gently is a kind of tenderness.',
    ['Here comes the cat.','Walking, so quiet.','Soft paws make no sound.','Step, step, on tip-toe.','Past the little baby.','The tail curves: hello!','Baby blinks — where did it go?','The cat sits on the windowsill.','A quiet cat, a quiet friend.']))
D3.append(S('2026-10-26-science-cn', '2026年10月26日 · 星期一', '10/26',
    '🔬 猫走路为什么没声音（0-1岁）', 'zh',
    '猫的脚底下有软软的肉垫，像穿了毛绒小鞋子，把脚步声都吃掉了。',
    '肉垫又软又厚，能吸掉走路的声音——猫是悄悄靠近猎物的捕猎小能手，肉垫就是它的消音器。',
    ['猫走路，没声音。','狗走路，嗒嗒响。','猫有什么秘密？','看它的脚底。','软软的肉垫，粉粉的。','像毛绒小鞋子。','脚步声，被它吃掉啦。','猫是悄悄的小猎手。','肉垫，就是消音小神器。'], sci=True))
D3.append(S('2026-10-26-science-en', 'October 26, 2026 · Monday', '10/26',
    '🔬 Science Story (0-1 yr): Why Cats Walk Silently', 'en',
    'The cat makes no sound when it walks. Its secret: soft squishy pads under its paws!',
    'The thick, soft pads swallow footsteps — like fuzzy little shoes. They help the cat sneak quietly.',
    ['The cat walks without sound.','The dog goes tap, tap.','What is the cat\'s secret?','Look under its paws.','Soft pink pads, so squishy.','Like fuzzy little shoes.','They swallow every footstep.','Cats are sneaky little hunters.','Soft pads are nature\'s muffler!'], sci=True))

# ---------- 10-27 周二 ----------
D3.append(S('2026-10-27-cn', '2026年10月27日 · 星期二', '10/27',
    '圆圆的球（0-1岁）', 'zh',
    '红皮球，圆圆的。推一推，咕噜噜。滚到东，滚到西，滚回来，撞到宝宝的小脚丫。',
    '圆圆的东西会滚。推一推、追一追，宝宝在游戏里认识了「圆」。',
    ['红皮球，圆圆的。','摸一摸，弹弹的。','小手推一推。','咕噜噜，滚走啦。','滚到东，滚到西。','咕噜噜，滚回来。','碰碰小脚丫，痒痒的。','宝宝咯咯笑。','圆圆的球，滚来滚去真好玩。']))
D3.append(S('2026-10-27-en', 'October 27, 2026 · Tuesday', '10/27',
    'The Round Red Ball (0-1 yr)', 'en',
    'A round red ball. Push it — roll, roll, roll! It rolls away and rolls back, bumping baby\'s toes.',
    'Round things roll! Pushing and chasing the ball is how baby discovers "round."',
    ['A ball, round and red.','Touch it — boing, boing!','Little hands push.','Roll, roll, roll away!','East and west it goes.','Roll, roll, roll back!','Boop — hello, little toes!','Baby laughs, hee hee hee.','Round ball, round fun.']))
D3.append(S('2026-10-27-science-cn', '2026年10月27日 · 星期二', '10/27',
    '🔬 球为什么会滚（0-1岁）', 'zh',
    '方方的积木推一下，停住了。圆圆的球推一下，滚好远。因为球身上处处是圆弧，一碰就能转。',
    '圆的东西没有角，接触地面只有一个小点，轻轻一碰就滚动——所以车轮都是圆圆的。',
    ['积木，方方的。','推一下，停住啦。','皮球，圆圆的。','推一下，滚好远。','为什么呀？','球身上全是圆弧。','没有角，没有棱。','碰地面只有一个小点。','轻轻一碰就滚动——车轮也是圆圆的哟。'], sci=True))
D3.append(S('2026-10-27-science-en', 'October 27, 2026 · Tuesday', '10/27',
    '🔬 Science Story (0-1 yr): Why Balls Roll', 'en',
    'Push a block — it stops. Push a ball — it rolls far away! The ball is round all over.',
    'Round things have no corners. They touch the ground at just one tiny point, so a small push makes them roll — that is why wheels are round!',
    ['The block is square.','Push it — it stops.','The ball is round.','Push it — it rolls!','Why, oh why?','The ball is curved all over.','No corners, no edges.','It touches the ground at one tiny point.','A little push — off it rolls! Wheels are round too.'], sci=True))

# ---------- 10-28 周三 ----------
D3.append(S('2026-10-28-cn', '2026年10月28日 · 星期三', '10/28',
    '妈妈的围巾（0-1岁）', 'zh',
    '风好大。妈妈把围巾解开，长长的一头，轻轻搭在宝宝脖子上。软软的，香香的，暖暖的。',
    '围巾把风挡在外面，把温暖围在里面。 sharing 一条围巾，就是 sharing 一份温暖。',
    ['呼呼呼，风好大。','树叶全在跳舞。','妈妈解开围巾。','长长的，软软的。','一头围妈妈，','一头围宝宝。','香香的，暖暖的。','风吹不到，冷进不来。','共享一条围巾，共享一份暖。']))
D3.append(S('2026-10-28-en', 'October 28, 2026 · Wednesday', '10/28',
    'Mommy\'s Scarf (0-1 yr)', 'en',
    'The wind is big today. Mommy unwinds her long scarf and wraps one end around baby. Soft, sweet, warm.',
    'A scarf keeps the wind out and the warmth in. Sharing a scarf is sharing warmth.',
    ['Whoosh, whoosh — big wind!','The leaves dance around.','Mommy unwinds her scarf.','Long and soft.','One end around Mommy,','one end around baby.','Sweet-smelling and warm.','The wind cannot get in.','One scarf, two warm hearts.']))
D3.append(S('2026-10-28-science-cn', '2026年10月28日 · 星期三', '10/28',
    '🔬 为什么闻得到香味（0-1岁）', 'zh',
    '妈妈身上的奶香味，宝宝隔着围巾也闻得到。因为香味的小颗粒会飞到空气里，钻进小鼻子。',
    '气味会随着空气到处旅行，鼻子里有小小的「侦察兵」接住它们——香味是会飞的信使。',
    ['妈妈抱抱，香香的。','隔着一层围巾，','小鼻子还是闻到啦。','为什么呀？','香味变成小小的颗粒。','它们飞进空气里。','飘呀飘，钻呀钻。','鼻子里的小侦察兵接住了它们。','报告！是妈妈的香味！'], sci=True))
D3.append(S('2026-10-28-science-en', 'October 28, 2026 · Wednesday', '10/28',
    '🔬 Science Story (0-1 yr): How We Smell Sweet Scents', 'en',
    'Even through the scarf, baby smells Mommy\'s sweet scent. Tiny scent bits travel through the air!',
    'Scents ride on the air and float everywhere. Little smell-catchers inside the nose catch them — scents are flying messengers.',
    ['Mommy smells so sweet.','Even through the scarf,','baby\'s nose finds it.','How does that work?','Scents turn into tiny bits.','The bits fly into the air.','Floating, floating, floating.','Little catchers in the nose grab them.','Report! It is Mommy\'s scent!'], sci=True))

# ---------- 10-29 周四 ----------
D3.append(S('2026-10-29-cn', '2026年10月29日 · 星期四', '10/29',
    '小星星眨眼睛（0-1岁）', 'zh',
    '夜空里有小星星，一颗，两颗，亮晶晶。它们朝宝宝眨眼睛：宝宝快睡吧，我们陪着你。',
    '星星是夜空的温柔陪伴。抬头看星星的孩子，梦里也会有光。',
    ['夜晚，安静了。','天上，小星星。','一颗，两颗，三颗。','亮晶晶，闪呀闪。','星星朝宝宝眨眼睛。','一闪，一闪。','它说：睡吧睡吧。','我在天上陪着你。','宝宝闭上眼，星星进梦里。']))
D3.append(S('2026-10-29-en', 'October 29, 2026 · Thursday', '10/29',
    'Twinkle, Little Stars (0-1 yr)', 'en',
    'In the night sky, little stars twinkle. One, two, shiny and bright. They wink at baby: sleep now, we will watch over you.',
    'Stars are the night sky\'s gentle companions. Children who look at stars dream in light.',
    ['The night is quiet.','Up in the sky — stars!','One, two, three.','Twinkle, twinkle, so bright.','A star winks at baby.','Blink, blink.','It says: sleep, sleep.','I am watching from above.','Baby closes her eyes — stars enter the dream.']))
D3.append(S('2026-10-29-science-cn', '2026年10月29日 · 星期四', '10/29',
    '🔬 星星为什么会「眨眼」（0-1岁）', 'zh',
    '星星其实不会眨眼。是地球外面的空气在动，星光穿过时被晃得一闪一闪，像在眨眼睛。',
    '空气的流动让星光摇摇晃晃，这就是「星星眨眼」——其实是大气在做游戏。',
    ['星星，一闪一闪。','它在眨眼睛吗？','其实星星不会眨。','是空气在捣乱。','地球外面裹着厚厚的空气。','空气一直在轻轻流动。','星光穿过时被晃来晃去。','一闪，一闪，像眨眼。','原来是大气在做游戏呀。'], sci=True))
D3.append(S('2026-10-29-science-en', 'October 29, 2026 · Thursday', '10/29',
    '🔬 Science Story (0-1 yr): Why Stars Twinkle', 'en',
    'Stars seem to wink and blink. But stars do not really blink — it is the air playing games with starlight!',
    'Moving air bends the starlight this way and that, making it flicker. That is why stars twinkle.',
    ['Stars twinkle, twinkle.','Are they winking at us?','Stars cannot really blink.','It is the air\'s doing.','The Earth wears a thick coat of air.','The air is always moving.','Starlight wiggles as it passes through.','Blink, blink — like winking!','It is the sky\'s little game.'], sci=True))
