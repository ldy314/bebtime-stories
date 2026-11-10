# -*- coding: utf-8 -*-
# 11-18 ~ 11-22
DEC4 = []

def S(id_, date, ds, title, lang, preview, moral, content, sci=False):
    d = {'id': id_, 'date': date, 'dateShort': ds, 'title': title, 'language': lang,
         'ageGroup': '0-1', 'ageLabel': '0-1岁', 'preview': preview, 'moral': moral,
         'content': content, 'category': 'science' if sci else 'regular'}
    if sci:
        d['series'] = 'science'; d['seriesTitle'] = '科学故事'
        d['source'] = 'Children science common sense' if lang == 'en' else '儿童科普常识'
    return d

# ---------- 11-18 周三 ----------
DEC4.append(S('2026-11-18-cn', '2026年11月18日 · 星期三', '11/18',
    '热毛巾小脸擦擦（0-1岁）', 'zh',
    '早上洗脸时间。妈妈拧好热毛巾，轻轻盖在宝宝小脸上——暖暖的！再轻轻一擦：小鼻子、小脸蛋、小耳朵，都干干净净了。',
    '洗脸是每天的小仪式。暖暖的毛巾里，装着妈妈细心的爱。',
    ['早晨，阳光爬上窗台。','洗脸时间到啦。','妈妈把小毛巾泡进温水里。','捞出来，拧一拧，','热气腾腾，暖暖的。','轻轻盖在宝宝脸上——','哇，暖暖的，像小被子。','毛巾下面，宝宝呼一口气。','妈妈数一二三，掀开！','开始擦啦。','小鼻子，擦一擦，哼哼。','小脸蛋，擦一擦，滑滑。','小额头，擦一擦，亮亮。','小耳朵，擦一擦，痒痒——','宝宝躲了一下，咯咯笑。','最后擦擦小下巴。','好啦！小脸干干净净，','香喷喷，亮闪闪。','新的一天，从暖暖的毛巾开始。']))
DEC4.append(S('2026-11-18-en', 'November 18, 2026 · Wednesday', '11/18',
    'Warm Towel, Clean Face (0-1 yr)', 'en',
    'Morning face-washing time. Mommy wrings out a warm towel and covers baby\'s face gently — so warm! One soft wipe: nose, cheeks, and ears, all clean.',
    'Face washing is a daily little ritual. Inside the warm towel lives Mommy\'s careful love.',
    ['Morning — sun climbs the window.','Face-washing time!','Mommy dips the towel in warm water.','Lifts it out, wrings it,','steaming and warm.','She covers baby\'s face gently —','so warm, like a tiny blanket.','Baby breathes out under the towel.','Mommy counts one-two-three, lifts!','Now the wiping begins.','Little nose — wipe, wipe.','Little cheeks — wipe, smooth.','Little forehead — wipe, shiny.','Little ears — wipe, tickly!','Baby dodges, giggling.','Last, the little chin.','All done! Face fresh and clean,','sweet-smelling and bright.','A new day starts with a warm towel.']))
DEC4.append(S('2026-11-18-science-cn', '2026年11月18日 · 星期三', '11/18',
    '🔬 热毛巾为什么暖乎乎（0-1岁）', 'zh',
    '毛巾泡进热水里再拿出来，就变得暖乎乎的。热气是会「搬家」的：从热的水里，搬进毛巾里，再从毛巾搬到宝宝脸上。',
    '热量总是从热的地方往凉的地方流动。热水把热传给毛巾（这叫热传导），毛巾再暖暖地传给脸——热量像温柔的小搬运工。',
    ['小毛巾，泡进热水里。','捞出来——暖乎乎！','热气是从哪儿来的？','热气会搬家呀。','热的地方和凉的地方，','像两个温度不同的房间。','热量总是从热的房间，','流进凉的房间。','热水很热，毛巾凉，','热就搬进毛巾里。','毛巾暖暖了，脸凉凉的，','热又搬到了小脸上。','搬家的热气，', '叫「热传导」。', '热气是小搬运工，', '把温暖搬来搬去。']))
DEC4.append(S('2026-11-18-science-en', 'November 18, 2026 · Wednesday', '11/18',
    '🔬 Science Story (0-1 yr): Why Warm Towels Stay Warm', 'en',
    'Dip the towel in hot water, lift it out — warm! Heat loves to "move house": from the water into the towel, then onto baby\'s face.',
    'Heat always flows from hot places to cool ones. Hot water warms the towel (called conduction), and the towel warms the face — heat is a gentle little mover.',
    ['The towel dips into hot water.','Out it comes — warm and toasty!','Where does the warmth come from?','Warmth moves house!','A hot place and a cool place,','are like two rooms.','Heat always flows','from the hot room to the cool one.','Hot water, cool towel —','warmth moves into the towel.','Now the towel is warm, the face is cool,','warmth moves onto the face.','This moving warmth,','is called conduction.','Heat is a tiny mover,','carrying warmth here and there.']))

# ---------- 11-19 周四 ----------
DEC4.append(S('2026-11-19-cn', '2026年11月19日 · 星期四', '11/19',
    '纸巾盒拉不完（0-1岁）', 'zh',
    '宝宝够到纸巾盒，小手一拉——抽出一张！再一拉——又一张！咦，怎么拉也拉不完？纸巾盒像有魔法，宝宝玩得停不下来。',
    '纸巾一张张交叠排列，抽出一张就带出下一张。游戏里藏着巧妙的排列智慧。',
    ['爬行垫上，放着一个纸巾盒。','宝宝爬过去，小手搭上去。','拉——抽出一张纸巾！','软软的，飘飘的。','再拉——又一张！','咦？怎么拉也拉不完？','宝宝越拉越起劲。','一张，两张，三张……','纸巾飘了一地，','像下了一场小雪。','妈妈过来了：小家伙，','你知道为什么拉不完吗？','纸巾们排好队，','一张叠着一张，','每张都轻轻搭在前一张身上。','抽出一张，就带出下一张，','像小伙伴手拉手。','妈妈把纸巾一张张叠回去：','排好队，下次再玩呀。']))
DEC4.append(S('2026-11-19-en', 'November 19, 2026 · Thursday', '11/19',
    'Pull, Pull, Tissue Box (0-1 yr)', 'en',
    'Baby reaches the tissue box. One pull — out comes a tissue! Another pull — another one! It never ends! The tissue box must have magic.',
    'Tissues are folded one over another; pulling one brings the next. Clever arrangement hides inside the game.',
    ['On the play mat sits a tissue box.','Baby crawls over, little hand on top.','Pull — one tissue comes out!','Soft and floaty.','Pull again — another one!','How does it never end?','Baby pulls harder and harder.','One, two, three...','Tissues flutter everywhere,','like a little snowfall.','Mommy comes over: little one,','do you know why it never ends?','The tissues stand in a line,','one folded over another,','each resting on the one before.','Pull one out, the next comes too,','like friends holding hands.','Mommy folds them back one by one:','line up — play again tomorrow!']))
DEC4.append(S('2026-11-19-science-cn', '2026年11月19日 · 星期四', '11/19',
    '🔬 纸巾为什么一张张抽（0-1岁）', 'zh',
    '纸巾盒里的纸巾，抽一张带出一张，从来不乱。因为工厂把它们设计成交叠排列：每张折叠的一半搭在下一张上。',
    '交叠排列像多米诺骨牌：抽第一张时，张力把下一张带到开口处，正好接着抽。这是人类巧妙的设计智慧。',
    ['纸巾盒，藏着一支小队伍。','纸巾们怎么排队的？','一张叠一张，','每张的一半搭在下一张上。','像下楼梯，一层接一层。','抽出第一张——','第二张被带到洞口。','抽出第二张——','第三张又冒出来。','一张接一张，', '像小伙伴手拉手。', '这是设计师叔叔的妙主意，', '让纸巾又好抽又不乱。', '一个小盒子，', '藏着排队的大学问。'], sci=True))
DEC4.append(S('2026-11-19-science-en', 'November 19, 2026 · Thursday', '11/19',
    '🔬 Science Story (0-1 yr): Why Tissues Come One by One', 'en',
    'Tissues in the box come out one after another, never tangled. The factory folds them in an overlapping line: half of each tissue rests on the next.',
    'Overlapping works like dominoes: pulling the first brings the next to the opening, ready to pull. A clever human design!',
    ['Inside the box hides a little line of tissues.','How do they stand in line?','One folded over another,','half of each on the next.','Like stairs, step by step.','Pull the first one out —','the second arrives at the hole.','Pull the second —','the third pops up.','One after another,','like friends holding hands.','A designer\'s clever idea,','keeping tissues neat and easy.','A little box,','holding a big lesson in lining up.']))

# ---------- 11-20 周五 ----------
DEC4.append(S('2026-11-20-cn', '2026年11月20日 · 星期五', '11/20',
    '小乌龟慢慢爬（0-1岁）', 'zh',
    '小乌龟玩具在垫子上慢慢爬。宝宝的手快，一把就要抓住——咦，小乌龟不动了，头和脚都缩进壳里。等一等，它又悄悄探出头来。',
    '慢慢来的小乌龟教宝宝：等待也是一种本领。不着急，美好的事会再来。',
    ['爬行垫上，来了个新朋友——','绿色的小乌龟玩具。','背上有花纹的壳，','四条小短腿。','小乌龟慢慢爬，','一步，一步，又一步。','宝宝的手快，「唰」地伸过去——','要抓到啦！','咦？小乌龟停住了。','头缩进壳里，脚也缩进去，','变成一块「小石头」。','宝宝等呀等。','一秒，两秒，三秒……','悄悄地，小脑袋探出来了。','又悄悄地，小脚也出来了。','继续慢慢爬，一步，一步。','宝宝这次等它爬了一会儿，','才轻轻碰碰它的壳。','小乌龟不害怕了，','驮着小房子继续散步。','慢慢来，没关系，','等待也是一种温柔。']))
DEC4.append(S('2026-11-20-en', 'November 20, 2026 · Friday', '11/20',
    'Slow, Slow Turtle (0-1 yr)', 'en',
    'A new friend crawls slowly on the mat — the little turtle! Baby\'s quick hand swoops... but the turtle stops and hides in its shell. Wait a while — out it peeks again.',
    'The slow turtle teaches baby: waiting is a skill. No rush — good things come back.',
    ['On the play mat, a new friend —','the little green turtle toy!','Patterned shell on its back,','four short little legs.','The turtle crawls slowly,','one step, one step, one more.','Baby\'s hand is quick — swoosh!','Almost got it!','Huh? The turtle stops.','Head in the shell, legs in too,','turning into a "little stone."','Baby waits and waits.','One second, two, three...','Quietly, the head peeks out.','Quietly, the legs come out too.','Crawling on, slow and steady.','This time baby lets it crawl a while,','then taps the shell gently.','The turtle is not scared now,','walking its little house on a stroll.','Slow is okay —','waiting is a gentle skill.']))
DEC4.append(S('2026-11-20-science-cn', '2026年11月20日 · 星期五', '11/20',
    '🔬 乌龟为什么慢慢爬（0-1岁）', 'zh',
    '小兔子跑得快，小乌龟爬得慢。因为乌龟背着壳，四条小短腿驮着「小房子」走路，每一步都要用大力气。',
    '龟壳是乌龟的移动堡垒，能保护它但也很重；腿短力气有限，所以走得慢。慢有慢的好处：省力气，活得久。',
    ['小兔子，蹦蹦跳，跑得快。','小乌龟，慢吞吞，爬得慢。','为什么这么慢呀？','看它背上的壳！','那是它的小房子，','硬硬的，保护它的。','小房子可不轻，','四条小短腿驮着走，','每一步都要用力气。','腿短，壳重，','就只好慢慢爬啦。','慢也有慢的好处：','不累，省力气，','还能活好长好长时间。','不着急，慢慢走，','稳稳当当最重要。'], sci=True))
DEC4.append(S('2026-11-20-science-en', 'November 20, 2026 · Friday', '11/20',
    '🔬 Science Story (0-1 yr): Why Turtles Crawl Slowly', 'en',
    'Bunnies run fast; turtles crawl slowly. The turtle carries its shell — a little house on four short legs, every step takes big effort.',
    'The shell is a moving fortress: protective but heavy. Short legs with limited strength mean slow walking. Slow has its perks: saving energy and living long.',
    ['Bunny hops — fast and light.','Turtle crawls — slow and steady.','Why so slow?','Look at the shell on its back!','It is the turtle\'s little house,','hard and protective.','The house is not light at all,','four short legs carry it,','every step takes strength.','Short legs, heavy shell —','slow crawling it is!','Slow has its own gifts:','less tired, saving energy,','and living a long, long time.','No rush — walk slowly,','steady and safe matters most.']))

# ---------- 11-21 周六（ep37 见 dd 文件） ----------
DEC4.append(S('2026-11-21-cn', '2026年11月21日 · 星期六', '11/21',
    '小猪玩偶呼噜噜（0-1岁）', 'zh',
    '新来的小猪玩偶圆圆胖胖。捏一捏，会「哼哼」叫！宝宝抱住它，小猪哼哼，宝宝咯咯，一对好朋友，抱在一起滚来滚去。',
    '会发声的玩偶让宝宝发现：按一按，就有回应。世界就是这样有来有往。',
    ['箱子里，钻出个新朋友。','圆圆的身子，胖胖的，','粉色的小猪玩偶！','鼻子翘翘，尾巴卷卷。','宝宝伸手一捏——','哼哼！小猪叫了！','再捏——哼哼，哼哼！','宝宝愣了一下，咯咯笑起来。','又捏一下，小猪又哼哼。','按一按，就有回应，','像在说悄悄话。','宝宝抱住小猪，','小猪胖胖的，软软的，','抱着特别安心。','抱着小猪滚一滚，','小猪哼哼，宝宝咯咯，','一对好朋友，','在垫子上滚来滚去。','玩累了，宝宝靠在小猪身上，','呼——小猪呼噜噜，','宝宝也呼噜噜。']))
DEC4.append(S('2026-11-21-en', 'November 21, 2026 · Saturday', '11/21',
    'Oink Oink Little Pig (0-1 yr)', 'en',
    'A new friend arrives: a round, chubby pig toy! Squeeze it — oink! Baby hugs the pig, the pig oinks, baby giggles — two friends rolling around together.',
    'Sound toys teach baby: press, and the world answers back. Everything has its echo.',
    ['Out of the box comes a new friend.','Round body, chubby cheeks,','a pink little pig toy!','Upturned nose, curly tail.','Baby squeezes —','oink! The pig squeaks!','Squeeze again — oink, oink!','Baby blinks, then bursts into giggles.','Press once more — oink again!','Press, and it answers,','like a little chat.','Baby hugs the pig,','chubby and soft,','so comforting to hold.','Rolling around with the pig,','the pig oinks, baby giggles,','two good friends,','rolling on the mat.','Play time over, baby leans on the pig.','Oink — the pig snores softly,','and so does baby.']))
DEC4.append(S('2026-11-21-science-cn', '2026年11月21日 · 星期六', '11/21',
    '🔬 毛绒玩具为什么软软的（0-1岁）', 'zh',
    '小猪玩偶抱起来软软的。因为它外面裹着一层毛绒绒的长毛，肚子里塞满了蓬蓬的棉花。',
    '毛绒外面蓬松、棉花里面多孔，都能兜住很多空气——空气软软的，所以玩偶摸上去像云朵。捏下去，空气被挤走，松手又弹回来。',
    ['小猪玩偶，抱一抱。','软软的，像朵小云。','为什么这么软呀？','看它的外面：','一层毛绒绒的长毛，','蓬蓬松松。','再看它的肚子里：','塞满了白色的棉花，','棉花里藏着好多小空气。','空气最软和啦，','空气多，就软乎乎。','捏下去，空气被挤走，','松开手，空气又回来，','玩偶就弹回来啦。','所以抱玩偶，','像抱着一朵会唱歌的云。'], sci=True))
DEC4.append(S('2026-11-21-science-en', 'November 21, 2026 · Saturday', '11/21',
    '🔬 Science Story (0-1 yr): Why Plush Toys Are Soft', 'en',
    'The pig toy feels so soft to hug! Outside it wears fluffy fur; inside its tummy is stuffed full of puffy cotton.',
    'Fluffy fur outside and porous cotton inside both trap lots of air — air is soft, so the toy feels like a cloud. Squeeze it and air escapes; let go, it bounces back.',
    ['Hug the little pig toy.','Soft as a little cloud.','Why is it so soft?','Look outside first:','a layer of fluffy fur,','puffy and loose.','Now look inside its tummy:','stuffed with white cotton,','hiding lots of tiny air pockets.','Air is the softest thing,','more air — more puffiness.','Squeeze, the air slips out;','let go, the air comes back,','and the toy bounces up!','So hugging a plush toy','is hugging a singing cloud.']))
