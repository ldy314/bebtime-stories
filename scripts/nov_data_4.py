# -*- coding: utf-8 -*-
# 10-30 ~ 11-03 每日中英 + 中英科学
D4 = []

def S(id_, date, ds, title, lang, preview, moral, content, sci=False):
    d = {'id': id_, 'date': date, 'dateShort': ds, 'title': title, 'language': lang,
         'ageGroup': '0-1', 'ageLabel': '0-1岁', 'preview': preview, 'moral': moral,
         'content': content, 'category': 'science' if sci else 'regular'}
    if sci:
        d['series'] = 'science'; d['seriesTitle'] = '科学故事'
        d['source'] = 'Children science common sense' if lang == 'en' else '儿童科普常识'
    return d

# ---------- 10-30 周五 ----------
D4.append(S('2026-10-30-cn', '2026年10月30日 · 星期五', '10/30',
    '小脚丫踩水洼（0-1岁）', 'zh',
    '雨停了，地上有小水洼。爸爸抱着宝宝，小脚丫轻轻点一点水洼。啪嗒！水花跳起来。',
    '啪嗒一声，是宝宝和水洼的第一次握手。小小的尝试，是探索世界的开始。',
    ['雨停了，云走了。','地上有小水洼。','圆的，亮的，像镜子。','爸爸抱着宝宝。','小脚丫，伸出来。','轻轻点一下——啪嗒！','水花跳起来，痒痒的。','再点一下——啪嗒啪嗒！','宝宝和水洼，握握手。']))
D4.append(S('2026-10-30-en', 'October 30, 2026 · Friday', '10/30',
    'The Wind Says Whoosh (0-1 yr)', 'en',
    'The wind blows today. It whooshes through the trees and tickles baby\'s hair. Whoosh, whoosh, hello wind!',
    'The wind cannot be seen, but it says hello through everything it touches.',
    ['The wind is here today.','Whoosh, whoosh, it sings.','It shakes the tree leaves.','It pushes the little flag.','It tickles baby\'s hair.','Whoosh — feel that?','Baby giggles, hee hee.','The wind says: hello, hello!','Baby waves back: hello, wind!']))
D4.append(S('2026-10-30-science-cn', '2026年10月30日 · 星期五', '10/30',
    '🔬 水洼去哪了（0-1岁）', 'zh',
    '昨天地上还有大大的水洼，今天却不见了。水洼去哪了？它变成看不见的水汽，飞上天空啦。',
    '太阳一晒，水就慢慢变成水汽升上天空。等它们在云里重新聚起来，又会变成雨落下来。',
    ['昨天，大水洼。','今天，不见了。','水洼去哪了？','太阳出来晒一晒。','水慢慢变成水汽。','水汽看不见，飞上天。','飞到云朵里住下。','等下次聚多了，又变雨点。','水呀水，是会旅行的小旅行家。'], sci=True))
D4.append(S('2026-10-30-science-en', 'October 30, 2026 · Friday', '10/30',
    '🔬 Science Story (0-1 yr): Where Puddles Go', 'en',
    'Yesterday there was a big puddle. Today it is gone! The puddle flew up to the sky as invisible vapor.',
    'Sunshine turns water into vapor that rises. Later the vapor gathers in clouds and falls again as rain.',
    ['Yesterday — a big puddle.','Today — all gone!','Where did it go?','The sun shone warmly.','The water turned into vapor.','Vapor is invisible.','It floats up, up, up.','It moves into a cloud.','Puddles are little travelers!'], sci=True))

# ---------- 10-31 周六（系列 ep34 同日发布，不冲突） ----------
D4.append(S('2026-10-31-cn', '2026年10月31日 · 星期六', '10/31',
    '圆圆的南瓜（0-1岁）', 'zh',
    '桌上有个大南瓜，圆圆的、橙橙的。宝宝拍一拍，咚咚咚。妈妈切开蒸一蒸，甜甜软软真好吃。',
    '南瓜是秋天的礼物：看着圆圆的可爱，吃着甜甜的暖心。秋天味道，甜进心里。',
    ['桌上，大南瓜。','圆圆的，橙橙的。','像个胖娃娃，笑眯眯。','宝宝拍一拍。','咚咚咚，声音闷闷的。','妈妈切开它。','橙色的瓜肉，亮亮的。','蒸一蒸，香飘满屋。','啊呜一口，甜甜软软。']))
D4.append(S('2026-10-31-en', 'October 31, 2026 · Saturday', '10/31',
    'Pumpkin Smile (0-1 yr)', 'en',
    'A big orange pumpkin sits on the table. Round and bright like a smiling sun. Baby pats it — boom, boom!',
    'The pumpkin is autumn\'s big smile: round, bright, and full of warmth.',
    ['A pumpkin on the table.','Big, round, and orange.','Like a smiling sun!','Baby pats it.','Boom, boom, boom!','Knock, knock, little pumpkin.','Mommy lifts baby up.','Baby and pumpkin, face to face.','Hello, big orange friend!']))
D4.append(S('2026-10-31-science-cn', '2026年10月31日 · 星期六', '10/31',
    '🔬 南瓜为什么是橙色的（0-1岁）', 'zh',
    '南瓜长大了就变成橙色的，因为它肚子里装满了「胡萝卜素」——一种橙色的天然色素，让它从绿宝宝长成橙娃娃。',
    '胡萝卜素藏在很多橙色蔬果里，宝宝吃了也能吸收它的营养，眼睛亮亮、身体棒棒。',
    ['小南瓜，小时是绿的。','长大后，变橙色啦。','为什么呀？','它肚里有胡萝卜素。','一种橙橙的天然色素。','藏得越来越多。','绿宝宝长成橙娃娃。','胡萝卜、橙子也有它。','宝宝吃了它，眼睛亮亮身体棒。'], sci=True))
D4.append(S('2026-10-31-science-en', 'October 31, 2026 · Saturday', '10/31',
    '🔬 Science Story (0-1 yr): Why Pumpkins Are Orange', 'en',
    'Little pumpkins start green. When they grow up, they turn orange — their tummies fill with carotene!',
    'Carotene is a natural orange color found in carrots, oranges, and pumpkins. Eating it helps eyes grow bright and strong.',
    ['Baby pumpkins start green.','They grow big and turn orange.','Why, oh why?','Carotene lives inside!','A natural orange color.','It fills up bit by bit.','Green baby becomes orange grown-up.','Carrots and oranges have it too.','Eat it — bright eyes, strong body!'], sci=True))

# ---------- 11-01 周日 ----------
D4.append(S('2026-11-01-cn', '2026年11月1日 · 星期日', '11/01',
    '小面包香喷喷（0-1岁）', 'zh',
    '面包店里飘出香气。圆圆的面包、胖胖的吐司，一个挨一个。宝宝吸吸小鼻子：好香呀。',
    '香味从烤箱里飞出来，邀请每一个路过的人。暖暖的食物，是最直接的幸福。',
    ['走过面包店。','咦，什么味道？','香喷喷，飘出来。','圆圆的面包，胖胖的吐司。','一个挨一个，排排坐。','烤箱里暖乎乎。','宝宝吸吸小鼻子。','小肚子咕噜噜。','好香呀，好香呀。']))
D4.append(S('2026-11-01-en', 'November 1, 2026 · Sunday', '11/01',
    'Yummy Apple Mash (0-1 yr)', 'en',
    'A red apple becomes sweet mash in baby\'s bowl. Spoon goes in — yum, yum! Baby eats it all up.',
    'Sweet apples make happy tummies. Yummy food is a little happiness every day.',
    ['A red, red apple.','Mommy washes it,','mashes it, mash, mash.','Into the little bowl.','Spoon comes — choo-choo train!','Open wide, here it comes!','Yum, yum, yum.','Sweet and soft and good.','All gone! More tomorrow.']))
D4.append(S('2026-11-01-science-cn', '2026年11月1日 · 星期日', '11/01',
    '🔬 面包为什么香香的（0-1岁）', 'zh',
    '面包烤一烤就变得特别香。因为烤箱的热气让面粉里的香味分子跳起舞来，一个个飞到空气里。',
    '加热会让食物释放香味——闻起来越香，说明烤得越透。香气是烤箱写给鼻子的邀请信。',
    ['面包进烤箱前，','闻起来淡淡的。','烤一烤，香喷喷！','为什么呀？','烤箱里热乎乎。','面粉里的香味分子醒啦。','它们跳起舞，飞出来。','飘到空中，钻进鼻子。','香气，是烤箱的邀请信。'], sci=True))
D4.append(S('2026-11-01-science-en', 'November 1, 2026 · Sunday', '11/01',
    '🔬 Science Story (0-1 yr): Why Bread Smells Sweet', 'en',
    'Bread smells wonderful after baking! The oven\'s heat wakes up tiny scent bits in the flour, and they dance into the air.',
    'Heat releases food\'s aromas — the sweeter the smell, the better the bake. Scent is the oven\'s invitation.',
    ['Bread before baking smells plain.','After baking — so sweet!','Why is that?','The oven is warm inside.','Tiny scent bits wake up.','They dance and fly out.','Up into the air,','right into your nose.','Scent is the oven\'s invitation!'], sci=True))

# ---------- 11-02 周一 ----------
D4.append(S('2026-11-02-cn', '2026年11月2日 · 星期一', '11/02',
    '小推车咕噜噜（0-1岁）', 'zh',
    '宝宝坐上小推车。咕噜噜，出发啦！树叶在旁边跑，小鸟在前面带路，风儿轻轻推一把。',
    '坐着小车去看世界：房子在走，树在走，天空也在走。出发，是最开心的事。',
    ['小推车，等宝宝。','坐上来，扣扣好。','咕噜噜，出发啦！','树叶在旁边跑。','小鸟在前面带路。','风儿轻轻推一把。','房子呀，往后走。','大树呀，往后走。','只有天空，一直跟着我们。']))
D4.append(S('2026-11-02-en', 'November 2, 2026 · Monday', '11/02',
    'Bye-bye, Little Bird (0-1 yr)', 'en',
    'A bird lands close, then flies away. Baby waves a tiny hand: bye-bye, birdie! See you tomorrow.',
    'Saying bye-bye is not sad — it means we will meet again.',
    ['A bird lands close to baby.','Tweet, tweet! It sings.','Baby stares, eyes wide.','The bird flaps its wings.','Up, up it flies away.','Baby waves a tiny hand.','Bye-bye, birdie!','The bird circles once more.','See you tomorrow, little friend!']))
D4.append(S('2026-11-02-science-cn', '2026年11月2日 · 星期一', '11/02',
    '🔬 车轮为什么是圆的（0-1岁）', 'zh',
    '小推车的轮子圆圆的，跑起来又快又稳。要是换成方轮子呢？咕咚、咕咚，一路颠簸，宝宝的小屁股会抗议的。',
    '圆形的车轮转起来中心不上下跳动，所以走得又稳又顺——圆形是滚动小能手。',
    ['小推车，跑得快。','咕噜噜，稳稳的。','轮子是什么形？','圆圆的！','试试方轮子？','咕咚，咕咚，颠颠的。','宝宝的小屁股会抗议。','圆轮子转起来，中心稳稳的。','所以车轮呀，都是圆圆的。'], sci=True))
D4.append(S('2026-11-02-science-en', 'November 2, 2026 · Monday', '11/02',
    '🔬 Science Story (0-1 yr): Why Wheels Are Round', 'en',
    'Stroller wheels are round, so the ride is smooth and fast. Imagine square wheels — bump, bump, bump!',
    'A rolling circle keeps its center at the same height, so it glides smoothly. That is why wheels are round.',
    ['The stroller zooms along.','Smooth and steady!','What shape are the wheels?','Round!','Try square wheels instead...','Bump, bump, bump — so bumpy!','Baby would say: no, no!','A round wheel rolls level.','That is why all wheels are round.'], sci=True))

# ---------- 11-03 周二 ----------
D4.append(S('2026-11-03-cn', '2026年11月3日 · 星期二', '11/03',
    '晚安小月亮（0-1岁）', 'zh',
    '月亮升起来了，弯弯的，像一只小船。它轻轻照进窗户，给宝宝盖上银色的光。晚安，小月亮。',
    '月亮每晚都会来道晚安。有月亮的夜晚，梦也是亮亮的。',
    ['天黑了，月亮升起来。','弯弯的，像小船。','它停在窗户外面。','轻轻照进一缕光。','银色的，柔柔的。','宝宝的小床，亮亮的。','小船月亮说：晚安。','宝宝的眼睛慢慢闭上。','月亮守着，梦甜甜的。']))
D4.append(S('2026-11-03-en', 'November 3, 2026 · Tuesday', '11/03',
    'Sleepy Time, Little Bear (0-1 yr)', 'en',
    'The little teddy bear is sleepy too. Baby hugs the bear, bear hugs the baby. Goodnight, little bear.',
    'A warm hug makes sleep sweet. Goodnight, little one.',
    ['The moon rises, high and round.','Baby\'s eyes grow heavy.','The little teddy bear yawns too.','Baby hugs the bear.','Bear hugs the baby.','So warm, so snug.','Mommy tucks them in.','Goodnight, little bear.','Goodnight, little one.']))
D4.append(S('2026-11-03-science-cn', '2026年11月3日 · 星期二', '11/03',
    '🔬 为什么晚上要睡觉（0-1岁）', 'zh',
    '晚上，眼睛要休息，身体也要休息。睡觉的时候，宝宝的身体在悄悄长个子，小脑袋在整理白天学到的新本领。',
    '睡觉不是浪费时间——深睡时生长激素最活跃，白天看到、听到的一切也被大脑悄悄归档。睡得好，长得快。',
    ['天黑了，要睡觉。','眼睛累了，想休息。','身体累了，想休息。','可是睡觉的时候，','身体可没闲着。','它在悄悄长个子。','小脑袋在整理白天的新本领。','像把玩具一件件收好。','睡得香，长得快——晚安，宝宝。'], sci=True))
D4.append(S('2026-11-03-science-en', 'November 3, 2026 · Tuesday', '11/03',
    '🔬 Science Story (0-1 yr): Why We Sleep at Night', 'en',
    'At night, eyes rest and bodies rest. But while baby sleeps, the body is busy growing tall and smart!',
    'Deep sleep is when the body grows fastest and the brain files away everything learned in the day. Good sleep makes you grow.',
    ['Night comes — time to sleep.','Eyes are tired.','The body is tired.','But sleep is busy time!','The body grows taller.','The little brain sorts the day\'s learning.','Like tidying toys into boxes.','Good sleep, good growth.','Goodnight, little one!'], sci=True))
