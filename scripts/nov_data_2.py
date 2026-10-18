# -*- coding: utf-8 -*-
# 10-22 ~ 10-25 每日中英 + 中英科学
D2 = []

def S(id_, date, ds, title, lang, preview, moral, content, sci=False):
    d = {'id': id_, 'date': date, 'dateShort': ds, 'title': title, 'language': lang,
         'ageGroup': '0-1', 'ageLabel': '0-1岁', 'preview': preview, 'moral': moral,
         'content': content, 'category': 'science' if sci else 'regular'}
    if sci:
        d['series'] = 'science'; d['seriesTitle'] = '科学故事'
        d['source'] = 'Children science common sense' if lang == 'en' else '儿童科普常识'
    return d

# ---------- 10-22 周四 ----------
D2.append(S('2026-10-22-cn', '2026年10月22日 · 星期四', '10/22',
    '浴室的小鸭子（0-1岁）', 'zh',
    '洗澡啦！小黄鸭浮在水上，捏一捏，吱吱叫。它摇摇摆摆游过来，撞到宝宝的小肚肚。',
    '小鸭子会浮起来，是因为水把它轻轻托住了。洗澡时间，是玩水的好时光。',
    ['哗啦哗啦，洗澡啦。','小黄鸭，下水啦。','浮在水上，摇呀摇。','捏一捏——吱吱！','再捏——吱吱吱！','小鸭子游过来。','轻轻碰碰小肚肚。','泡泡飞起来，亮晶晶。','洗香香，抱出来，真舒服。']))
D2.append(S('2026-10-22-en', 'October 22, 2026 · Thursday', '10/22',
    'Splash Splash, Bath Time (0-1 yr)', 'en',
    'Bath time! Little duck floats on the water. Squeeze — squeak! It swims over and bumps baby gently.',
    'Water lifts the duck up gently. Bath time is splash-and-play time.',
    ['Splash, splash, bath time!','Little yellow duck floats.','Bob, bob, on the water.','Squeeze it — squeak!','Squeeze again — squeak, squeak!','The duck swims over.','Boop! It touches baby.','Bubbles fly up, shiny.','Clean and cozy, all done!']))
D2.append(S('2026-10-22-science-cn', '2026年10月22日 · 星期四', '10/22',
    '🔬 小鸭子为什么浮在水上（0-1岁）', 'zh',
    '小黄鸭躺水上，怎么按也不沉。因为鸭肚子里藏着空气，水在下面轻轻托着它。',
    '水有一种向上托的力量叫浮力。空心、轻轻的东西，水就把它托在水面上。',
    ['小鸭子，浮浮的。','按一按，又弹上来。','为什么不沉呢？','鸭子肚里有空气。','像只小小的空盒子。','水有向上的力气，叫浮力。','浮力轻轻托着它。','轻轻的东西，水托得住。','石头重重的，扑通就沉啦。'], sci=True))
D2.append(S('2026-10-22-science-en', 'October 22, 2026 · Thursday', '10/22',
    '🔬 Science Story (0-1 yr): Why the Duck Floats', 'en',
    'The little duck floats and floats. Push it down — it pops back up! Air hides inside its tummy.',
    'Water pushes things up. That push is called buoyancy. Light, hollow things float on the water.',
    ['The duck floats, floats.','Push it — it pops back!','Why does it not sink?','Air hides in its tummy.','Like a tiny empty box.','Water pushes up — that is buoyancy.','Buoyancy holds the duck gently.','Light things float.','Heavy things go plop and sink!'], sci=True))

# ---------- 10-23 周五 ----------
D2.append(S('2026-10-23-cn', '2026年10月23日 · 星期五', '10/23',
    '秋叶飘呀飘（0-1岁）', 'zh',
    '一片黄叶子，从树上飘下来。飘呀飘，转呀转，像小蝴蝶。落在宝宝的小车车上。',
    '秋天的叶子慢慢落下，是大树在换新衣裳。每一片落叶都是一封秋天的信。',
    ['树上，一片黄叶子。','风轻轻一吹。','飘——呀——飘。','转个圈，转个圈。','像一只小蝴蝶。','飘到宝宝的车车上。','宝宝伸手，抓一抓。','叶子脆脆的，沙沙响。','大树说：换季啦，明年再见。']))
D2.append(S('2026-10-23-en', 'October 23, 2026 · Friday', '10/23',
    'Leaves Fall Softly (0-1 yr)', 'en',
    'A yellow leaf falls from the tree. Down, down, spinning like a little butterfly. It lands on baby\'s stroller.',
    'Falling leaves mean autumn is dressing the trees in new colors. Every leaf is a letter from fall.',
    ['A yellow leaf on the tree.','The wind blows softly.','Down, down it floats.','Spin, spin, spin.','Like a little butterfly.','It lands on the stroller.','Baby reaches out.','The leaf goes crunch, crunch.','The tree says: see you next year!']))
D2.append(S('2026-10-23-science-cn', '2026年10月23日 · 星期五', '10/23',
    '🔬 叶子为什么变黄（0-1岁）', 'zh',
    '夏天的叶子绿绿的，秋天就变黄了。因为叶子里藏着黄色的小色素，夏天被绿色盖住，秋天绿色退场，黄色就露出来啦。',
    '叶子里的绿色怕冷，天一凉就慢慢退去，藏了一路的黄色和红色就显出来了。',
    ['叶子，夏天绿绿的。','秋天，变黄啦。','为什么呀？','叶子里藏着小色素。','绿色站岗，黄色睡觉。','天一凉，绿色怕冷。','绿色悄悄退场了。','黄色伸个懒腰：到我来啦！','于是满树都是金黄色。'], sci=True))
D2.append(S('2026-10-23-science-en', 'October 23, 2026 · Friday', '10/23',
    '🔬 Science Story (0-1 yr): Why Leaves Turn Yellow', 'en',
    'Leaves are green in summer, yellow in autumn. Yellow was hiding inside all along!',
    'Cold weather makes the green fade away, and the yellow and red that were hiding come out to play.',
    ['Leaves are green in summer.','In autumn they turn yellow.','Why?','Yellow colors hide inside.','Green stands in front.','When it gets cold...','Green fades away.','Yellow stretches: my turn!','The whole tree turns gold!'], sci=True))

# ---------- 10-24 周六（系列由 ep33 占位，不在此文件） ----------
# ---------- 10-25 周日 ----------
D2.append(S('2026-10-25-cn', '2026年10月25日 · 星期日', '10/25',
    '小雨点滴滴答（0-1岁）', 'zh',
    '下雨啦。小雨点落在窗玻璃上，滴滴答，滴滴答。宝宝趴在妈妈肩上，听雨唱歌。',
    '小雨点敲窗户，是天空在演奏音乐。听，每一种声音都有自己的节奏。',
    ['外面，下雨啦。','小雨点，排着队。','滴滴答，滴滴答。','落在窗玻璃上。','敲敲窗：咚咚。','落在树叶上：沙沙。','宝宝趴在妈妈肩上。','眼睛亮亮，听雨唱歌。','雨停了，天边一道小彩虹。']))
D2.append(S('2026-10-25-en', 'October 25, 2026 · Sunday', '10/25',
    'Raindrops Go Pit-pat (0-1 yr)', 'en',
    'It is raining! Little raindrops tap the window. Pit-pat, pit-pat. Baby listens to the rain song.',
    'Raindrops tap-tapping is the sky making music. Listen — every sound has its own rhythm.',
    ['Rain is falling outside.','Little raindrops, in a line.','Pit-pat, pit-pat.','Tap-tap on the window.','On the leaves — swish.','On the roof — pitter patter!','Baby rests on Mommy\'s shoulder.','Bright eyes listen to the rain song.','The rain stops — hello, little rainbow!']))
D2.append(S('2026-10-25-science-cn', '2026年10月25日 · 星期日', '10/25',
    '🔬 雨点从哪里来（0-1岁）', 'zh',
    '云朵里住着许多小水珠。小水珠越抱越多，云朵抱不动了，就变成雨点落下来。',
    '水汽升上天空变成云，云里的小水珠聚在一起变重了，重得云朵托不住，就落下来成为雨。',
    ['天上的云，白白的。','云里住着小水珠。','一颗，两颗，好多颗。','小水珠抱在一起。','抱得越来越多。','云朵抱不动啦。','哗啦啦，掉下来。','小水珠变成小雨点。','落进泥土，浇灌小花。'], sci=True))
D2.append(S('2026-10-25-science-en', 'October 25, 2026 · Sunday', '10/25',
    '🔬 Science Story (0-1 yr): Where Rain Comes From', 'en',
    'Little water drops live inside clouds. When they hug together too tight, down comes the rain!',
    'Water vapor rises to make clouds. Drops gather until they are too heavy — then they fall as rain.',
    ['The cloud is white and soft.','Tiny water drops live inside.','One, two, so many!','The drops hug each other.','More and more drops hug.','The cloud cannot hold them.','Pitter-patter, down they fall!','Drops become raindrops.','Rain waters the flowers below.'], sci=True))
