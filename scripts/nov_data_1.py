# -*- coding: utf-8 -*-
# 10-18 ~ 10-21 每日中英 + 中英科学（10-18 cn/en 用 -2 扩展 id，避开自动化）
D1 = []

def S(id_, date, ds, title, lang, preview, moral, content, sci=False):
    d = {'id': id_, 'date': date, 'dateShort': ds, 'title': title, 'language': lang,
         'ageGroup': '0-1', 'ageLabel': '0-1岁', 'preview': preview, 'moral': moral,
         'content': content, 'category': 'science' if sci else 'regular'}
    if sci:
        d['series'] = 'science'; d['seriesTitle'] = '科学故事'
        d['source'] = 'Children science common sense' if lang == 'en' else '儿童科普常识'
    return d

# ---------- 10-18 周日 ----------
D1.append(S('2026-10-18-cn-2', '2026年10月18日 · 星期日', '10/18',
    '小手拍拍（0-1岁）', 'zh',
    '小手拍拍，小手拍拍。拍一拍，响一声。宝宝咯咯笑，拍得真开心。',
    '拍拍手，宝宝发现自己能发出声音——小身体里藏着大大的本领。',
    ['小手，举起来。','拍一拍，拍一拍。','啪，啪。','小手碰小手，响一声。','宝宝听见了，咯咯笑。','再拍一次，啪。','咦，声音又来了。','小手真听话，一拍就响。','拍累了，小手放下来，休息一下。']))
D1.append(S('2026-10-18-en-2', 'October 18, 2026 · Sunday', '10/18',
    'Peek-a-Boo, Hello! (0-1 yr)', 'en',
    'Mommy hides behind her hands. Where is Mommy? Peek-a-boo! There she is!',
    'Peek-a-boo teaches baby that things come back — Mommy is always near.',
    ['Mommy hides her face.','Where is Mommy?','Baby waits, eyes wide.','Peek-a-boo!','There she is!','Baby laughs a big laugh.','Again! Again!','Peek-a-boo! Hello!','Mommy was always there.']))
D1.append(S('2026-10-18-science-cn', '2026年10月18日 · 星期日', '10/18',
    '🔬 镜子里的宝宝（0-1岁）', 'zh',
    '镜子里有一个宝宝，笑一笑，他也笑。伸手摸一摸——凉凉的，硬硬的。那是谁呀？',
    '镜子会反光，把宝宝的样子送回来。镜子里的宝宝就是宝宝自己——这是宝宝认识自己的第一步。',
    ['镜子亮亮的。','镜子里有个宝宝。','宝宝笑，他也笑。','宝宝伸手，他也伸手。','摸一摸，凉凉的。','哦，那是玻璃。','玻璃会反光，像一张会动的照片。','镜子里的宝宝，就是宝宝自己。','你好呀，镜子里的小宝宝。'], sci=True))
D1.append(S('2026-10-18-science-en', 'October 18, 2026 · Sunday', '10/18',
    '🔬 Science Story (0-1 yr): Baby in the Mirror', 'en',
    'There is a baby in the mirror. Baby smiles — the mirror baby smiles too. Who is that?',
    'A mirror bounces light back, so it shows your own face. The baby in the mirror is you!',
    ['The mirror is shiny.','A baby lives in the mirror?','Baby smiles — it smiles too.','Baby waves — it waves too.','Touch it — cool and smooth.','It is just glass.','Glass bounces light back, like a picture that moves.','The mirror baby is you!','Hello, little you!'], sci=True))

# ---------- 10-19 周一 ----------
D1.append(S('2026-10-19-cn', '2026年10月19日 · 星期一', '10/19',
    '奶瓶的小肚肚（0-1岁）', 'zh',
    '奶瓶有个圆肚肚，里面装着温温的奶。咕嘟，咕嘟，宝宝喝饱饱，打个小小的奶嗝。',
    '吃饱饱的宝宝最安心。温温的奶，是妈妈准备好的小小的爱。',
    ['奶瓶，圆肚肚。','肚肚里，温温的奶。','妈妈抱着宝宝。','小嘴凑上去。','咕嘟，咕嘟。','奶宝宝跑进小肚子。','小肚子，鼓鼓的。','喝饱了，打个奶嗝。','嗝——好舒服呀。']))
D1.append(S('2026-10-19-en', 'October 19, 2026 · Monday', '10/19',
    'The Sleepy Kitten (0-1 yr)', 'en',
    'A little kitten curls up like a ball. Shhh... The kitten is sleeping. Soft and warm.',
    'Even little kittens need naps. Sleep makes everyone grow strong and sweet.',
    ['A little kitten.','Soft as a cloud.','It curls up, round and round.','Shhh...','The kitten is sleeping.','Its tail covers its nose.','Purr... purr...','Sweet dreams, little cat.','Baby sleeps too. Shhh...']))
D1.append(S('2026-10-19-science-cn', '2026年10月19日 · 星期一', '10/19',
    '🔬 奶为什么是温温的（0-1岁）', 'zh',
    '宝宝的奶是温温的，不烫也不凉。为什么呀？因为妈妈用手腕试过温度啦。',
    '太烫会伤到小嘴巴，太凉小肚子会不舒服。温温的温度刚刚好——大约和妈妈的体温一样。',
    ['奶瓶里，温温的奶。','不烫，也不凉。','为什么呀？','妈妈调好温度啦。','太烫，小嘴会疼。','太凉，小肚会闹。','温温的，刚刚好。','像妈妈怀抱的温度。','温温的奶，暖暖的爱。'], sci=True))
D1.append(S('2026-10-19-science-en', 'October 19, 2026 · Monday', '10/19',
    '🔬 Science Story (0-1 yr): Why Milk Is Warm', 'en',
    'Baby milk is warm, not hot and not cold. Why? Mommy tested it first!',
    'Milk that is too hot can hurt, and cold milk upsets little tummies. Warm — about body temperature — is just right.',
    ['The milk is warm.','Not hot. Not cold.','Why is it just right?','Mommy tested it first.','Too hot — ouch, little mouth!','Too cold — brr, little tummy!','Warm is perfect.','Warm like a hug.','Warm milk, warm love.'], sci=True))

# ---------- 10-20 周二 ----------
D1.append(S('2026-10-20-cn', '2026年10月20日 · 星期二', '10/20',
    '窗外的鸽子（0-1岁）', 'zh',
    '窗台上飞来小鸽子，咕咕咕，咕咕咕。脖子亮晶晶，一歪头看一看。宝宝学它：咕咕咕。',
    '小鸽子用咕咕声打招呼。世界上的问候有千百种，每一种都很好听。',
    ['窗台上，谁来啦？','小鸽子，胖乎乎。','咕咕咕，咕咕咕。','脖子亮晶晶，绿的紫的。','歪着头，看宝宝。','宝宝也歪着头。','咕咕咕，学一学。','小鸽子扑棱棱，飞走啦。','明天再来玩呀，咕咕咕。']))
D1.append(S('2026-10-20-en', 'October 20, 2026 · Tuesday', '10/20',
    'Hello, Little Bird (0-1 yr)', 'en',
    'A little bird lands by the window. Tweet, tweet! It hops, it looks, it sings hello.',
    'A bird song is a hello from the sky. Every hello makes the day brighter.',
    ['Look! A little bird.','It hops, hop, hop.','Tweet, tweet, tweet!','It sings to the morning.','It tilts its head.','Hello, baby!','Baby kicks, kick, kick.','The bird flies away.','Bye-bye, little bird!']))
D1.append(S('2026-10-20-science-cn', '2026年10月20日 · 星期二', '10/20',
    '🔬 鸽子为什么咕咕叫（0-1岁）', 'zh',
    '鸽子不会唱歌，却会咕咕咕。原来它肚子里有个小气囊，气一鼓一鼓，就发出咕咕声。',
    '鸽子用气囊发声，就像吹响了身体里的小气球。这是它打招呼和说话的方式。',
    ['鸽子，咕咕咕。','它不会像小鸟那样唱。','它的秘密在肚子里。','有个小小的气囊。','气囊一鼓——咕！','一鼓——咕咕！','像身体里的小气球。','咕咕声是它的话：','你好呀，你好呀。'], sci=True))
D1.append(S('2026-10-20-science-en', 'October 20, 2026 · Tuesday', '10/20',
    '🔬 Science Story (0-1 yr): Why Doves Coo', 'en',
    'Doves do not sing like songbirds. They say coo, coo! A little air bag inside helps them talk.',
    'A dove puffs up an air sac in its chest — like a tiny balloon — and the air makes the coo-coo sound.',
    ['A dove says coo, coo.','Not a song like other birds.','Its secret is inside.','A little air bag.','Air puffs in — coo!','Air puffs out — coo!','Like a tiny balloon.','Coo-coo means hello.','Hello, hello!'], sci=True))

# ---------- 10-21 周三 ----------
D1.append(S('2026-10-21-cn', '2026年10月21日 · 星期三', '10/21',
    '小毯子软软（0-1岁）', 'zh',
    '小毯子，软软的。盖在身上，像一朵云。小脚丫藏起来，小手手藏起来。暖暖的，真安心。',
    '软软的毯子留住暖和的空气，像妈妈的怀抱一样，把温暖轻轻围起来。',
    ['小毯子，软软的。','盖上来，轻飘飘。','像一朵云，落身上。','小脚丫，藏起来。','小手手，藏起来。','只露出小脸蛋。','风来啦，吹不到。','暖暖的，痒痒的。','盖着云朵，做甜甜的梦。']))
D1.append(S('2026-10-21-en', 'October 21, 2026 · Wednesday', '10/21',
    'The Cozy Blanket (0-1 yr)', 'en',
    'The blanket is soft. It covers baby like a little cloud. Toes hide, fingers hide. Warm and snug.',
    'A soft blanket keeps the warm air close, wrapping baby in a gentle hug.',
    ['The blanket is soft.','So soft, so light.','It floats down like a cloud.','Toes hide inside.','Fingers hide inside.','Only the little face peeks out.','The wind cannot find baby.','Warm... warm...','Sleep under the cloud.']))
D1.append(S('2026-10-21-science-cn', '2026年10月21日 · 星期三', '10/21',
    '🔬 毯子为什么暖和（0-1岁）', 'zh',
    '小毯子不会生火，为什么会暖和？原来它锁住了宝宝身上的热气，不让暖空气溜走。',
    '毯子的纤维里藏着许多小空气袋，把身体的热气留在里面——毯子是温暖的守护者。',
    ['毯子会变暖吗？','毯子不会生火呀。','它的本事是——锁住热气。','宝宝的身体暖暖的。','热气想溜走。','毯子说：不许跑！','毛毛里有许多小空气袋。','把暖空气围起来。','热气留下来，宝宝暖乎乎。'], sci=True))
D1.append(S('2026-10-21-science-en', 'October 21, 2026 · Wednesday', '10/21',
    '🔬 Science Story (0-1 yr): Why Blankets Keep You Warm', 'en',
    'A blanket cannot make fire. How does it keep you warm? It traps the warm air from your body!',
    'The tiny fibers hold little pockets of air and stop body heat from escaping — a blanket is a warmth keeper.',
    ['Is a blanket warm?','It cannot make fire.','Its trick is — trapping heat!','Your body makes warmth.','The warmth wants to sneak away.','The blanket says: no, no!','Soft fibers hold tiny air pockets.','They hug the warm air in.','Heat stays. Baby stays cozy.'], sci=True))
