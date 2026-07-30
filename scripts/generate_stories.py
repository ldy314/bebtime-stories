# -*- coding: utf-8 -*-
"""Generate 14 missing bedtime stories and update all data files."""

import json
import os
import re

STORIES_JSON = r"C:\Users\Administrator\WorkBuddy\Claw\bedtime-story-app\stories.json"
COLLECTION_MD = r"C:\Users\Administrator\WorkBuddy\Claw\bedtime-story-collection.md"
INDEX_HTML = r"C:\Users\Administrator\WorkBuddy\Claw\bedtime-story-app\index.html"

new_stories = [
    # ========== 2026-07-19 CN (冰波风格) ==========
    {
        "id": "2026-07-19-cn",
        "date": "2026年7月19日 · 星期日",
        "dateShort": "07/19",
        "title": "雨滴在云里等（胎教期）",
        "language": "zh",
        "ageGroup": "prenatal",
        "ageLabel": "胎教期",
        "preview": "云妈妈的口袋里，住着一滴小小的雨。她圆圆的，透明的，还没去过地面，也没闻过泥土的味道...",
        "moral": "等待不是空的。等待里装着所有的期盼、所有的温柔、所有还没说出口的爱。当你终于来到这个世界，你会发现——你等的人，也在等你。",
        "content": [
            "云妈妈的口袋里，住着一滴小小的雨。她圆圆的，透明的，还没去过地面，也没闻过泥土的味道。",
            "小雨滴每天趴在云的边沿上，往下看。她看见田野、河流、小房子。其中一栋小房子的窗户亮着橘黄色的灯，灯里有一位妈妈，正轻轻地拍着圆圆的肚子，嘴里哼着歌。",
            "小雨滴想下去。她想去看看那扇亮着灯的窗户。听说那肚子里住着一个还没来的小宝宝，跟小雨滴一样，也在等。",
            "云妈妈说：「再等等。雨要落下去，得等风准备好了，得等土地渴了，得等太阳把云晒得暖暖的、软软的。」",
            "小雨滴等啊等。她听云妈妈讲地面的故事——讲小草怎么从泥土里钻出来，讲小溪怎么在石头之间弹钢琴，讲花儿怎么在风里点头。",
            "「地面是什么感觉？」小雨滴问。",
            "「地面是温暖的。」云妈妈说，「像一双一直在等你的手。」",
            "有一天，风来了。风从很远的地方来，带着田野的味道，带着花香，还带着一个声音——一个妈妈在轻轻哼歌的声音。",
            "小雨滴听见了那首歌。她觉得那首歌是在叫她。也许不是叫她，但那首歌的旋律刚好跟她心里的节拍一模一样。",
            "云妈妈把口袋松了一点点。小雨滴滑到了口袋的边沿上。",
            "「准备好了吗？」云妈妈问。",
            "「准备好了。」小雨滴说。她不怕。因为她知道，下面有人在等——妈妈在等宝宝，土地在等雨，而她，正要去赴一场温暖的相遇。",
            "小雨滴落了下去。风轻轻地托着她，不急，不慌。她穿过云层，穿过风，穿过鸟的翅膀旁边，穿过树叶的缝隙。",
            "她落在了一片叶子上，嗒。又从叶子上滑到了泥土里，渗进去了。",
            "泥土很黑，但很温暖。小雨滴觉得自己被什么柔软的东西包裹住了，像被一双手轻轻捧着。",
            "泥土里，有一颗种子，也在等。种子感觉到雨来了，动了一下，好像在说：「你来了。」",
            "小雨滴和种子，在泥土里相遇了。一个从天上来的，一个在地里等的。它们谁也没说话，但都觉得——原来等了这么久，就是为了这一刻。",
            "窗户里，妈妈的歌还在轻轻地响。她不知道，她的歌叫来了一滴雨，而雨叫醒了一颗种子。",
            "每一个等待，都在等一个相遇。而每一个相遇，都让等待变得值得。"
        ]
    },
    # ========== 2026-07-19 EN (McCloskey) ==========
    {
        "id": "2026-07-19-en",
        "date": "2026年7月19日 · 星期日",
        "dateShort": "07/19",
        "title": "The Pond Sleeps Too (Prenatal)",
        "language": "en",
        "ageGroup": "prenatal",
        "ageLabel": "Prenatal",
        "preview": "The pond goes shhh-shhh when the sun goes down. The cattails go swish-swish at the edge. The old willow goes sway-sway over the water...",
        "moral": "When everything around you breathes slow and soft, you can breathe slow and soft too. The pond knows how to sleep. The moon knows how to wait. And you - you know how to be still, even if you don't know it yet.",
        "content": [
            "The pond goes shhh-shhh when the sun goes down.",
            "The cattails go swish-swish at the edge. The old willow goes sway-sway over the water.",
            "A small duck, name of Pip, floats on the pond. Pip is brown. Pip is small. Pip is doing nothing. Just floating.",
            "The bullfrog says: rummm... rummm... rummm... from the mud. Low and slow and round, like a belly full of warm soup.",
            "The fireflies come out. Blink... blink... blink... Like tiny lanterns that someone forgot to blow out.",
            "Mama Duck paddles over. Paddle, paddle, paddle. She settles next to Pip. She doesn't say anything. She just settles. The water barely moves.",
            "The moon comes up. It comes up slow, slow, slow - like it's being very careful not to wake anything up.",
            "The moon puts a silver road on the water. It goes from the edge of the pond all the way to where Pip is floating. Pip doesn't know it's there. But the road is there.",
            "Shhh-shhh says the water. Rummm-rummm says the frog. Blink-blink say the fireflies.",
            "A fish jumps - plop - and the ripples go round and round and round, getting bigger and softer, until they disappear into the dark.",
            "The old willow drops a leaf. The leaf falls slow, slow, slow - side to side, side to side - and lands on the water without a sound. It floats there, like a tiny green boat.",
            "Pip's eyes go heavy. Pip tucks his beak under his wing. Warm. Close. Mama is here.",
            "The whole pond goes still. Not dead-still - alive-still. The kind of still that means everything is breathing together. The water, the frog, the fireflies, the duck, the moon.",
            "Shhh... shhh... shhh...",
            "The pond sleeps too."
        ]
    },
    # ========== 2026-07-20 CN (张秋生风格) ==========
    {
        "id": "2026-07-20-cn",
        "date": "2026年7月20日 · 星期一",
        "dateShort": "07/20",
        "title": "月光写的一封信（胎教期）",
        "language": "zh",
        "ageGroup": "prenatal",
        "ageLabel": "胎教期",
        "preview": "月亮给一栋小房子写了一封信。信很短，只有一句话：嘘，我在。风当邮差，把信从天上送下来...",
        "moral": "有些爱，不需要语言，不需要文字。一束光，一阵风，一个小小的动作，就够了。你知道的——有人一直在你头顶亮着。",
        "content": [
            "月亮给一栋小房子写了一封信。",
            "信很短，只有一句话：嘘，我在。",
            "风当邮差，把信从天上送下来。风轻轻地，轻轻地，从窗户缝里溜进去。",
            "信落在妈妈的肚子上。",
            "妈妈没看见信，但宝宝看见了。宝宝在暖暖的羊水里，翻了个身，像在拆信。",
            "信没有字，只有月光。月光是软的，是凉的，是一根银色的线，从天上一直牵到妈妈肚子里。",
            "宝宝顺着这根线，往上摸了摸。他摸到了月亮。",
            "月亮说：我每天晚上都给你写信。",
            "宝宝不会说话，但他动了一下，像在回信。",
            "月亮笑了。月亮的笑，就是一整片亮。",
            "那天晚上，小房子里的灯灭了，月光没灭。",
            "月光从窗户缝里渗进来，铺在地板上，铺在被子上，铺在妈妈的手背上。",
            "妈妈睡得很沉。她不知道，月光在替她守着宝宝。",
            "宝宝在月光里，安安静静地浮着。他抓着那根银色的线，线的另一头，是月亮。",
            "月亮什么也没做。只是亮着。",
            "但宝宝觉得很安心。",
            "因为有些陪伴，不需要做什么。亮着，就够了。",
            "嘘，我在。",
            "每天晚上，月亮都会写这封信。信永远只有一句话，但那句话，比所有的故事都长。"
        ]
    },
    # ========== 2026-07-20 EN (Dr. Seuss) ==========
    {
        "id": "2026-07-20-en",
        "date": "2026年7月20日 · 星期一",
        "dateShort": "07/20",
        "title": "The Hush-Hush Tree (Prenatal)",
        "language": "en",
        "ageGroup": "prenatal",
        "ageLabel": "Prenatal",
        "preview": "Deep in the hush of the Whispering Wood, where the moss grows soft and the silence is good, there stood a tall tree with a curious sound - it went hush, hush, hush, all the way round...",
        "moral": "There's a hush that's not 'be quiet' - it's 'you're safe now, you can rest.' The whole world is full of that hush, if you know how to hear it. And you will.",
        "content": [
            "Deep in the hush of the Whispering Wood, where the moss grows soft and the silence is good, there stood a tall tree with a curious sound - it went hush, hush, hush, all the way round.",
            "Not a loud hush, not a scoldy-type hush. Not a 'be-quiet-you' hush or a 'hurry-up' hush. It was soft as a feather on fur on a rug. It was warm as a hug from a big fuzzy bug.",
            "The Hush-Hush Tree stood with its branches spread wide, and out of its leaves came a sound soft and slow - a sound like a shush that was saying 'it's time to let go.'",
            "Now, nobody knew where the hush-hush came from. Not the fox with his socks, not the mole with his drum, not the owl on the bough (who said 'Hoo? Hoo? Hmm?').",
            "But a small mother bird who had built her small nest right there in the Hush-Hush Tree's branches - she knew. She had five small eggs, round and warm, and she sat on them every night from dusk until dawn.",
            "And the hush-hush sound went shhhh... shhhh... shhhh... and the eggs didn't wiggle, and the eggs didn't squirm. They just sat in the nest, warm and still, like a handful of smooth round stones in the sun.",
            "The mother bird sang: 'Hush little ones, hush little ones, hush. The world is still turning, but we don't need to rush. The stars are all waking, the moon's on her way. Close your small eyes - it's the end of the day.'",
            "And the Hush-Hush Tree went shhhh... shhhh... shhhh... like it was singing along.",
            "The wind came to visit, the way that wind does. It tickled the leaves and it made the branches buzz. But even the wind, when it passed through the tree, went 'hush' instead of 'whooo' - it couldn't help but agree.",
            "The fireflies came, blink-blink-blink, one by one. The crickets came, chirp-chirp-chirp, under the moon. And each one of them, when they came to the tree, got quieter and quieter - as quiet as could be.",
            "And down in the world, past the Whispering Wood, past the meadow and stream, past the houses that stood - in one of those houses, a window glowed gold. And inside the window, a mother (I'm told) was holding her belly and humming a tune, a soft little melody, under the moon.",
            "And that melody floated right up through the air, past the chimney and rooftop, past everywhere - all the way to the Hush-Hush Tree, where it landed on a leaf like a drop of warm tea.",
            "And the tree drank it in, and the hush got softer. And the eggs in the nest got warmer and softer. And the mother bird smiled - or as much as a bird can smile - and she whispered: 'Goodnight.'",
            "Shhhh... shhhh... shhhh... went the Hush-Hush Tree.",
            "And the whole wide world went as soft as could be."
        ]
    },
    # ========== 2026-07-21 CN (金波风格) ==========
    {
        "id": "2026-07-21-cn",
        "date": "2026年7月21日 · 星期二",
        "dateShort": "07/21",
        "title": "风知道你的名字（胎教期）",
        "language": "zh",
        "ageGroup": "prenatal",
        "ageLabel": "胎教期",
        "preview": "风轻轻吹，草轻轻摇，月亮轻轻走过山岗。风从山岗上跑下来，路过一棵老槐树，路过一片芦苇荡，路过一栋亮着灯的小房子...",
        "moral": "你的名字，是这世界对你说的第一句情话。在你还没来到之前，风已经帮你传开了，水已经帮你记住了。你来了，满世界都在喊你。",
        "content": [
            "风轻轻吹，草轻轻摇，月亮轻轻走过山岗。",
            "风从山岗上跑下来，路过一棵老槐树，路过一片芦苇荡，路过一栋亮着灯的小房子。",
            "小房子的窗户开着一条缝。风从缝里溜进去，带进来桂花的香、泥土的潮，和远处小溪叮叮咚咚的声音。",
            "妈妈坐在床边，一只手拍着圆圆的肚子，另一只手放在嘴边，好像在说什么悄悄话。",
            "风竖起耳朵，听了听。",
            "妈妈在说一个名字。一遍，又一遍。轻轻的，像在念一首只有两个字的诗。",
            "风记住了那个名字。",
            "风从窗户里出来，往田野跑。它跑过小溪，小溪叮叮咚咚，风把那个名字告诉了水。水记住了，叮叮咚咚地唱着那个名字。",
            "风跑过老槐树，老槐树沙沙响，风把那个名字告诉了树叶。树叶记住了，沙沙沙沙地念着那个名字。",
            "风跑过芦苇荡，芦苇轻轻摇，风把那个名字告诉了月光。月光记住了，把那个名字写在了每一片叶子的尖尖上，亮晶晶的。",
            "风跑累了，回到小房子的屋檐上歇脚。它往下看，看见妈妈已经睡着了，手还放在肚子上。",
            "风想，宝宝还不知道，自己的名字已经被整个世界记住了。",
            "等宝宝来了，他会发现：溪水在叫他的名字，树叶在念他的名字，月光在写他的名字。",
            "他一来到这个世界，就会被叫一声。那一声，全世界一起喊。",
            "叮叮咚咚。沙沙沙沙。嘘——嘘——。",
            "都是那个名字。",
            "风轻轻地吹，草轻轻地摇。月亮轻轻地走过山岗，带着那个名字，走过每一扇亮着灯的窗。"
        ]
    },
    # ========== 2026-07-21 EN (Twain) ==========
    {
        "id": "2026-07-21-en",
        "date": "2026年7月21日 · 星期二",
        "dateShort": "07/21",
        "title": "The Old River Tells a Story (Prenatal)",
        "language": "en",
        "ageGroup": "prenatal",
        "ageLabel": "Prenatal",
        "preview": "Well now, you listen here, and I'll tell you something about the Old Muddy that most folks don't know. The river talks. Not loud - a river doesn't need to be loud...",
        "moral": "The river has been telling stories since before there were people to listen. And it's been saving one - just for you. When you're ready, go down to the water and sit. It'll tell you. It's been waiting.",
        "content": [
            "Well now, you listen here, and I'll tell you something about the Old Muddy that most folks don't know.",
            "The river talks. Not loud - a river doesn't need to be loud. It talks the way an old man talks on a porch at sundown: slow, and easy, and not in any particular hurry to get to the point.",
            "The river talks to the banks. It talks to the willows. It talks to the catfish and the turtles and the herons that stand in the shallows like they've got all the time in creation, which - being herons - they probably figure they do.",
            "But the river's best talking? That happens at night. When the steamboats have gone and the lanterns are dim and the only ones still awake are the river and the moon.",
            "That's when the river tells stories.",
            "It tells about the spring floods, when it gets up over its banks and goes roaming through the bottoms like a dog that's slipped its leash. It tells about the summer doldrums, when it gets so low and slow you could walk across it and barely wet your knees. It tells about the winter ice, when it goes hard and quiet, and you can hear it groaning in the dark, like a man turning over in bed.",
            "But there's one story the river tells that's different from the rest. It's not about floods or ice or catfish the size of dogs. It's about a sound.",
            "'There's a sound,' the river says (or the river would say, if rivers could talk, which I'm telling you they can), 'that I've been hearing for a while now. It comes from a house on my bank. It's small - smaller than a cricket, smaller than a raindrop. But it's got a rhythm to it.'",
            "The moon, who's been listening to the river's stories for as long as there've been rivers and moons, asks: 'What kind of rhythm?'",
            "'A heartbeat rhythm,' the river says. 'Thump... thump... thump. Slow and steady, like a small drum in a small room.'",
            "'Whose heartbeat?' the moon asks.",
            "The river doesn't answer right away. It gurgles over a rock - that's river for 'let me think.' Then it says: 'There's a woman in that house who's been coming down to my bank every evening. She puts her hand on her belly and she hums. And under the hum, I can hear it - thump... thump... thump. Two heartbeats. One big, one small. The small one is new.'",
            "The moon knows what that means. The moon has seen more new heartbeats than anybody. The moon says: 'That's a baby.'",
            "'I know,' says the river. 'But the baby hasn't come yet. It's still in there, still growing, still thumping away. I can hear it getting stronger every week.'",
            "'What are you going to do?' the moon asks.",
            "The river thinks about this for a long time. Water goes over rocks. A fish jumps - plop. A frog says rummm.",
            "'I'm going to keep talking,' the river says. 'I'm going to keep flowing past that house, nice and easy, so the baby can hear me. When it's born, it'll know my sound. It'll know the Old Muddy. And maybe - maybe - when it's old enough, it'll come down to the bank and sit, and listen, and the river will tell it stories.'",
            "'Like what stories?' the moon asks.",
            "'Like this one,' the river says.",
            "And the river flowed on, under the moon, past the house with the two heartbeats, carrying its story downstream - where it would be told again, and again, and again, to every child who ever sat on a riverbank and wondered what the water was saying."
        ]
    },
    # ========== 2026-07-22 CN (孙敬修风格) ==========
    {
        "id": "2026-07-22-cn",
        "date": "2026年7月22日 · 星期三",
        "dateShort": "07/22",
        "title": "小闹钟学唱歌（胎教期）",
        "language": "zh",
        "ageGroup": "prenatal",
        "ageLabel": "胎教期",
        "preview": "孩子们，你们知道吗？每个闹钟都会唱歌。可不是「叮铃铃」那种歌，是一种更轻、更慢的歌，是专门哄小宝宝睡觉的歌...",
        "moral": "声音最大的不一定最有力量。最轻的声音，反而能让人放下所有的紧张，安心入睡。你的心跳也是这样——轻轻地跳，却陪了你一辈子。",
        "content": [
            "孩子们，你们知道吗？每个闹钟都会唱歌。",
            "可不是「叮铃铃」那种歌，是一种更轻、更慢的歌，是专门哄小宝宝睡觉的歌。",
            "后来啊，有一个小闹钟，住在床头柜上，它就特别想学这首歌。",
            "小闹钟问闹钟妈妈：「妈妈妈妈，我什么时候才能学会哄觉的歌呀？」",
            "闹钟妈妈说：「你得先学会，把自己的声音调到最小。嘀嗒嘀嗒，不能再响了，得变成嘀——嗒——嘀——嗒——，慢悠悠的。」",
            "小闹钟试了试。嘀嗒嘀嗒嘀嗒。不行，太快了，像小兔子蹦。",
            "它又试了试。嘀——嗒——嘀——嗒——。嗯，好一点了，像老乌龟爬。",
            "闹钟妈妈说：「还不够。你得把声音再放轻，轻到像羽毛落在棉花上。」",
            "小闹钟使劲儿把声音调小。嘀————嗒————。这一回，声音小得几乎听不见了。",
            "可你猜怎么着？正因为太小了，你反而会竖起耳朵，认认真真地听。这可就对了。",
            "闹钟妈妈笑了：「闹钟的歌，不是为了让人听见，是为了让人安静下来。」",
            "小闹钟明白了。它开始嘀——嗒——嘀——嗒——，一声一声，不急不慌，像一只温柔的手掌，一下一下拍着后背。",
            "床头柜旁边，妈妈哄着肚子里的宝宝。宝宝的呼吸，慢慢地跟小闹钟的嘀嗒声合拍了。",
            "嘀——嗒——。宝宝的心跳。",
            "嘀——嗒——。妈妈的手掌。",
            "嘀——嗒——。小闹钟的歌。",
            "三个声音叠在一起，变成了一首只有三拍的摇篮曲。",
            "小闹钟可得意了。它想，原来闹钟不只是用来叫人起床的，闹钟也能哄人睡觉呀。",
            "嘀——嗒——。嘀——嗒——。",
            "晚安，小闹钟。晚安，小宝宝。明天早上，小闹钟会叫你们起床的。但现在，先好好睡一觉吧。"
        ]
    },
    # ========== 2026-07-22 EN (McCloskey) ==========
    {
        "id": "2026-07-22-en",
        "date": "2026年7月22日 · 星期三",
        "dateShort": "07/22",
        "title": "The Mama Robin's Counting Song (Prenatal)",
        "language": "en",
        "ageGroup": "prenatal",
        "ageLabel": "Prenatal",
        "preview": "In the old maple by the fence, there's a robin's nest. Mama Robin built it herself - twigs and mud and grass, pressed together with her chest, round and smooth and strong...",
        "moral": "Before you come into the world, someone is already counting you. Not days, not weeks - heartbeats. One, two, three, four. Each one a promise. Each one a 'you're almost here.'",
        "content": [
            "In the old maple by the fence, there's a robin's nest.",
            "Mama Robin built it herself - twigs and mud and grass, pressed together with her chest, round and smooth and strong. She built it in the fork of two branches, where the wind couldn't reach.",
            "In the nest are four eggs. Blue as a spring sky after rain. Smooth and small and warm.",
            "Every evening, when the sun goes down behind the barn and the fireflies come out, Mama Robin settles on the nest. She covers the eggs with her soft brown body, and she counts.",
            "She doesn't count out loud. She counts with her heartbeat.",
            "Thump. One egg. Thump. Two eggs. Thump. Three eggs. Thump. Four eggs.",
            "Four heartbeats back. Four tiny thumps, so small you'd need to be a bird to feel them, pulsing up through the warm blue shells.",
            "Papa Robin sits on the fence, not far away. He doesn't say anything. He just sits. Sometimes he turns his head - left, right, left - watching the yard, the barn, the lane. Keeping watch.",
            "The crickets start. Chirp, chirp, chirp - like a thousand small clocks winding themselves for the night.",
            "The old dog on the porch sighs - a big, round, contented sigh - and puts his head on his paws.",
            "The barn owl, who lives in the hole in the barn's peak, opens one yellow eye. Checks the yard. Closes it. All's well.",
            "Mama Robin shifts her weight. The eggs roll, just a tiny bit, settling deeper into the warmth.",
            "Thump. Thump. Thump. Thump. Four eggs. Four heartbeats. One nest.",
            "The moon comes up over the maple. It comes up slow and round and silver, like a dinner plate someone left in the sky.",
            "The moonlight comes through the leaves and makes dappled patterns on the ground - round, bright spots that move when the wind moves, like they're alive.",
            "Mama Robin's eyes close. Her beak tucks under her wing. But her body stays warm, and her heart keeps counting.",
            "Thump. One. Thump. Two. Thump. Three. Thump. Four.",
            "Someday soon, those four thumps will become four beaks, tapping from the inside. And the shells will crack - tik, tik, tik - and four small mouths will open, and four small voices will say, in their own way: 'I'm here. I'm here. I'm here.'",
            "But not yet. Not tonight.",
            "Tonight, it's just Mama Robin, and the eggs, and the moon, and the counting.",
            "Thump. Thump. Thump. Thump.",
            "Goodnight, maple. Goodnight, moon. Goodnight, four small hearts, beating in the dark."
        ]
    },
    # ========== 2026-07-23 CN (冰波风格) ==========
    {
        "id": "2026-07-23-cn",
        "date": "2026年7月23日 · 星期四",
        "dateShort": "07/23",
        "title": "云的口袋里装着梦（胎教期）",
        "language": "zh",
        "ageGroup": "prenatal",
        "ageLabel": "胎教期",
        "preview": "天上有一朵很软很软的云。它长得像一只懒洋洋的猫，整天在天空里慢慢地飘。云有一个口袋。口袋里装的不是雨，不是雪，是梦...",
        "moral": "有一个梦在等你，从你还没来就开始等了。它空空的，扁扁的，专门留给你。等你来了，你的第一个梦就会装进去——那个梦会是全世界最干净、最温柔的，因为你的心还什么都没碰过。",
        "content": [
            "天上有一朵很软很软的云。",
            "它长得像一只懒洋洋的猫，整天在天空里慢慢地飘。",
            "云有一个口袋。口袋里装的不是雨，不是雪，是梦。",
            "每一朵云都有一个口袋，都装着梦。梦是透明的，软软的，像棉花糖化开以后的样子。",
            "这朵云的口袋里，有一个特别小的梦。别的梦都圆滚滚的，它却扁扁的，像还没有装满。",
            "云问它：「你怎么这么小呀？」",
            "小梦说：「因为我还在等一个人。那个人的梦还没做完，我才能装满。」",
            "「等谁？」",
            "小梦不说话了。它趴在口袋边沿上，往下看。",
            "它看见了一栋小房子。窗户亮着。里面有一位妈妈，拍着圆圆的肚子，嘴里哼着歌。",
            "小梦的眼睛亮了：「就是他。」",
            "「他还没出生呢。」云说。",
            "「我知道。所以我还不能装满。我得等他来了，把他做的梦一点一点装进来。他的第一个梦，一定很小很小，小到只有一粒沙那么大。但那个梦会是最干净的，最软的，因为他的心还什么都没碰过。」",
            "云想了想，说：「那你慢慢等。我飘得慢一点。」",
            "于是云飘啊飘，飘过了山岗，飘过了河流，飘过了一片又一片田野。它飘得特别慢，慢到地上的老鹰都笑话它：「你这是什么云呐，比蜗牛还慢！」",
            "云不理它。云知道，口袋里有一个小梦在等，所以不能颠簸，不能跑太快，不然梦会洒出来的。",
            "每天晚上，云都会飘到那栋小房子的上空，停下来。小梦从口袋边沿往下看，看见妈妈在拍肚子，看见灯灭了，看见月亮升起来了。",
            "有一天，妈妈拍着拍着，肚子动了一下。",
            "小梦激动地抖了抖：「他动了！他是不是在做梦了？」",
            "云笑了：「也许吧。也许他在梦里翻了个身。」",
            "小梦等着。它知道，等那个小宝宝来到这个世界，它的第一个梦就会装进自己的身体里。到那时候，它就不扁了，它就圆了，就饱满了。",
            "而且它知道，那个梦会是全世界最温柔的梦——因为那个梦的主人，还没有见过这个世界的任何一丁点儿不好。",
            "在他看来，一切都是新的，一切都是好的，一切都值得放进梦里。",
            "小梦耐心地等着。云耐心地飘着。月亮耐心地亮着。",
            "它们都在等同一个孩子。"
        ]
    },
    # ========== 2026-07-23 EN (Sesame Street + Dr. Seuss) ==========
    {
        "id": "2026-07-23-en",
        "date": "2026年7月23日 · 星期四",
        "dateShort": "07/23",
        "title": "The Snuggle Bug Who Couldn't Sleep (Prenatal)",
        "language": "en",
        "ageGroup": "prenatal",
        "ageLabel": "Prenatal",
        "preview": "In the crumbly-crumbly corner of the Snuggle-Bug Wood, where the softest of mosses grow soft as they could, there lived a small Snuggle Bug - name of Piddle-dee-Pip - who could NOT get to sleep, not a wink, not a bit!...",
        "moral": "Sleep is shy. You can't chase it. But if you hold something soft, and listen to a hum, and stop trying so hard - it'll come. It always comes, when you stop chasing and start being.",
        "content": [
            "In the crumbly-crumbly corner of the Snuggle-Bug Wood, where the softest of mosses grow soft as they could, there lived a small Snuggle Bug - name of Piddle-dee-Pip - who could NOT get to sleep, not a wink, not a bit!",
            "'Oh BOTHER and FUSS!' said Piddle-dee-Pip. 'I've wiggled and jiggled and turned and I've flipped! I've counted the stars - I got up to eleven! I've counted the clouds - I ran out at seven! I've tried sleeping on leaves, I've tried sleeping on bark, I've tried sleeping upside down in the dark!'",
            "But nothing worked. Piddle-dee-Pip's eyes were WIDE open. Like two small round windows with nobody home in them.",
            "Along came a friend - a big fuzzy Bear - name of Humphrey-dee-Doo, with fur everywhere, and a smile like a warm honey bun, and a voice like a kettle that's just about done.",
            "'Why, Piddle-dee-Pip! You're still AWAKE?' said Humphrey-dee-Doo, with a worried sort of shake. 'The moon's been up for an HOUR at least! The fireflies have gone to their small firefly feast! The crickets have sung all their cricket-y songs! What's keeping you up when the whole world's gone wrong?'",
            "'I don't KNOW!' said Piddle, and sniffled a bit. 'I'm tired - I'm SO tired - but sleep just won't sit! It flies away! It runs away! It hides behind the tree! I chase it and chase it, but it won't come to me!'",
            "Humphrey-dee-Doo sat down with a THUMP. He folded his big fuzzy arms in a lump. He thought and he thought and he thought some more, and his thinking made the sound of a low gentle snore - which was ironic, but Piddle didn't notice, on account of being too busy being upset.",
            "'I've got it!' said Humphrey, and his eyes went all bright. 'You're chasing sleep, and sleep doesn't like to be chased!'",
            "'It doesn't?' said Piddle.",
            "'No!' said Humphrey. 'Sleep is shy. Sleep comes when you're not looking. Sleep comes when you're so busy NOT-chasing that you forget you were trying!'",
            "'But how do I NOT-chase something I'm trying to chase?' asked Piddle, who was confused, which is a perfectly reasonable way to feel when a bear tells you to stop chasing something you've been chasing all night.",
            "'Easy,' said Humphrey. 'You do something else. Something warm. Something soft. Something that has nothing to do with sleeping.'",
            "'Like what?'",
            "'Like...' Humphrey looked around. He picked up a small handful of moss. He put it in Piddle's hands. 'Feel this.'",
            "Piddle felt it. It was soft. Very, very soft. Like the top of a kitten's head, if the kitten was made of green.",
            "'Now close your eyes,' said Humphrey, 'and just feel the moss. Don't think about sleeping. Don't think about stars. Don't think about counting or clouds or anything. Just... feel.'",
            "Piddle closed his eyes. He felt the moss. It was soft. It was warm. It was there.",
            "Humphrey started to hum. Hmmmm... hmmmm... hmmmm... Not a song. Just a hum. Like a bumblebee that's too tired to buzz.",
            "Piddle felt the moss. He heard the hum. He felt the warm. He felt the close.",
            "And something happened.",
            "Sleep didn't come running. Sleep didn't come flying. Sleep just... settled. Like a leaf on still water. Like snow on a mitten. Like a small warm thing finding a warm soft place and deciding to stay.",
            "Piddle's breathing went slow. Piddle's hands went loose. The moss slipped to the ground - plop - but Piddle didn't notice.",
            "Humphrey smiled. He tucked his big fuzzy arm around Piddle, and he kept humming. Hmmmm... hmmmm... hmmmm...",
            "And the moon, who'd been watching the whole thing from up in the sky, smiled too. Because the moon knows a thing or two about patience. The moon takes all night to cross the sky, and it never hurries, and it always gets there.",
            "'Goodnight, Piddle-dee-Pip,' said Humphrey, very soft.",
            "'Goodnight, Humphrey-dee-Doo,' said the moon, even softer.",
            "And the Snuggle-Bug Wood went quiet - all except the hum."
        ]
    },
    # ========== 2026-07-24 CN (郑渊洁风格-柔和版) ==========
    {
        "id": "2026-07-24-cn",
        "date": "2026年7月24日 · 星期五",
        "dateShort": "07/24",
        "title": "梦还没来（胎教期）",
        "language": "zh",
        "ageGroup": "prenatal",
        "ageLabel": "胎教期",
        "preview": "后来啊，有一只小猫，叫兜兜。兜兜有一个特别的本事——它能看见梦。人的梦，在人的头顶上飘着，五颜六色的。小孩的梦是粉的，大人的梦是灰的，老人的梦是金的...",
        "moral": "你的第一个梦，正从天上慢慢飘来。它一路收集了风、露水、月光和鸟叫。等你来到这个世界，那个梦就到了——它是全世界最干净、最香的梦，因为它为你攒了一路的温柔。",
        "content": [
            "后来啊，有一只小猫，叫兜兜。兜兜有一个特别的本事——它能看见梦。",
            "人的梦，在人的头顶上飘着，五颜六色的。小孩的梦是粉的，大人的梦是灰的，老人的梦是金的。",
            "可兜兜发现了一件怪事。森林边上的小房子里，那位妈妈肚子里的宝宝——他的头顶上，什么也没有。",
            "兜兜歪着脑袋想了半天。别人的头顶上都有梦，怎么这个宝宝没有呢？",
            "它跑去问猫头鹰爷爷。猫头鹰爷爷整天坐在树洞里，什么都知道。",
            "「猫头鹰爷爷，那个还没出生的小宝宝，头顶上怎么没有梦呢？」",
            "猫头鹰爷爷睁开一只眼睛：「他的梦还没来呢。」",
            "「没来？梦也会迟到？」",
            "「不是迟到。」猫头鹰爷爷慢悠悠地说，「是他的梦还在路上。你看——」",
            "猫头鹰爷爷用翅膀往天上一指。兜兜抬头一看，哎呀！天上有一团特别小特别小的光，正慢慢地、慢慢地往下飘。那团光比萤火虫还小，比蒲公英的绒毛还轻。",
            "「那是他的梦。」猫头鹰爷爷说，「每个宝宝的梦都是从天上来的。梦要飘很久很久，才能飘到宝宝头顶上。」",
            "「为什么这么慢呀？」",
            "「因为梦在路上要收集东西。它要收集一阵风，收集一滴露水，收集一片月光，收集一声鸟叫。收集够了，才能变成一个完整的梦。那个梦才够香，够甜，够软。」",
            "兜兜想帮忙。它跳到屋顶上，对着天上的那团小光喊：「嘿——快点下来！宝宝快出生了！」",
            "小光没理它。它还是慢慢地飘，好像在说：急什么，好东西得慢慢来。",
            "兜兜只好等着。每天晚上，它趴在屋顶上，看着那团小光近了一点点，又近了一点点。",
            "有一天晚上，小光终于飘到了小房子的上空。它在屋顶上停了停，好像在喘口气。",
            "兜兜激动地竖起尾巴：「到了到了！」",
            "小光慢慢地从烟囱里钻进去——兜兜觉得这太冒险了，万一被烟熏黑了怎么办——不过小光没事，它是梦，不怕烟。",
            "小光飘进了卧室，飘到了妈妈的肚子上，然后轻轻一闪，不见了。",
            "兜兜趴在屋顶上，等了一会儿。",
            "然后，它看见了。妈妈的肚子上方，出现了一个很小很小的、粉色的梦。扁扁的，软软的，像一小朵棉花糖。",
            "那是宝宝的第一个梦。",
            "兜兜笑了。猫头鹰爷爷在树洞里也笑了。",
            "你猜宝宝的第一个梦是什么？兜兜看不见梦里的内容，但它看见那个梦的颜色——是全世界最浅最浅的粉，像刚出生的朝霞，像还没被碰过的花瓣。",
            "那颜色，干净得让人心里发软。"
        ]
    },
    # ========== 2026-07-24 EN (Dahl - gentle) ==========
    {
        "id": "2026-07-24-en",
        "date": "2026年7月24日 · 星期五",
        "dateShort": "07/24",
        "title": "The Toymaker's Last Song (Prenatal)",
        "language": "en",
        "ageGroup": "prenatal",
        "ageLabel": "Prenatal",
        "preview": "There was once a toymaker who lived at the end of a lane that nobody walked down anymore, in a shop that leaned slightly to the left, like a man who'd been standing for a very long time and had gotten tired...",
        "moral": "Some songs aren't written yet. They're waiting for the right person to arrive - someone who hasn't been born, maybe, but who's already listening. When you get here, there'll be a song with your name on it. You just have to be ready to hear it.",
        "content": [
            "There was once a toymaker who lived at the end of a lane that nobody walked down anymore, in a shop that leaned slightly to the left, like a man who'd been standing for a very long time and had gotten tired.",
            "His name was Mr. Coggle, and he was very old. He'd been making toys for so long that his fingers looked like the wooden dolls he made - knobbly and smooth and worn at the joints.",
            "Mr. Coggle had made every kind of toy you could think of. Clockwork trains. Spinning tops. Jack-in-the-boxes that popped with a satisfying BOING. Dolls with eyes that opened and closed. Tin soldiers that marched. A music box that played a tune so beautiful it made grown men stand still in the street with a faraway look, which was very inconvenient if they happened to be carrying groceries.",
            "But there was one toy Mr. Coggle had never made. He'd been saving the materials for it for forty years.",
            "The materials were: a piece of cedar from his grandmother's hope chest, a brass spring he'd found in a clock when he was nine, a scrap of velvet from his mother's old dress, and a single hair from the head of the woman he'd loved, who had gone away a long, long time ago and taken all the music with her.",
            "'What kind of toy is it?' asked the cat, who was orange and fat and had no business being in the shop, but was there anyway, because cats don't ask permission.",
            "'It's not a toy, exactly,' said Mr. Coggle. He was shaping the cedar with a small knife, very carefully, the way you'd shape something that mattered. 'It's more of a... a song, in a box.'",
            "'A music box?'",
            "'No. A music box plays a song that's already been written. This plays a song that hasn't been written yet. A song for someone who hasn't heard it yet.'",
            "The cat narrowed its eyes. Cats are suspicious of things they don't understand, which is most things.",
            "Mr. Coggle worked all day and all night. He carved the cedar into a small, round box, smooth as an egg. He wound the brass spring inside, but he didn't attach it to any mechanism. He lined the inside with the velvet. And he wove the single hair - which was dark and fine and still smelled faintly of lavender - around the spring, like a thread around a spindle.",
            "When he was done, the box sat on his workbench. It didn't do anything. It didn't play. It didn't open. It just sat there, looking like a small wooden egg, and doing a very good job of it.",
            "'Well?' said the cat. 'Does it work?'",
            "'It's not for me,' said Mr. Coggle. 'It's for someone who hasn't arrived yet.'",
            "'Who?'",
            "'I don't know,' said Mr. Coggle. And the strangest thing was - he smiled when he said it. A real smile, the kind that crinkles the corners of your eyes and makes you look, for a moment, like a young man instead of an old one.",
            "He put the box in the window of his shop. And there it sat.",
            "Weeks passed. Nobody came down the lane. Nobody noticed the box. The cat came and went, catching mice and making disapproving faces at things.",
            "Then one evening, a woman walked down the lane. She was round in the middle, the way women are when they're carrying something precious and heavy and almost-ready. She walked slowly, the way you walk when each step is a negotiation with gravity.",
            "She stopped at the window. She saw the box.",
            "She didn't open the door. She didn't go in. She just stood there, looking at the small wooden egg in the window, and she put her hand on her belly, and she smiled.",
            "And the box - the box that didn't play, that didn't open, that just sat there looking like a small wooden egg - hummed.",
            "Just once. A single note. Low and warm and round, like the first note of a song that's going to be very beautiful when it's finished, but isn't finished yet.",
            "The woman heard it. Or maybe she felt it. Or maybe she just knew, the way you know things that you can't explain and shouldn't try to.",
            "Mr. Coggle, inside the shop, heard it too. He closed his eyes. He was very old, and very tired, and he'd been waiting a very long time.",
            "'There you are,' he said, to nobody, or to everybody, or to the note that was hanging in the air like a held breath. 'I've been waiting for you.'",
            "The note faded. The box went quiet. The woman walked on, slowly, back up the lane, into the evening.",
            "But something had changed. The lane didn't look so forgotten. The shop didn't lean quite so far to the left. And the cat, who was sitting in the window where the box had been, was purring - though there was nobody left to hear it.",
            "Well, that's not quite true. There was somebody. Somebody very small, and very new, and very warm, who hadn't been born yet, but who had just heard the first note of a song that would last their whole life."
        ]
    },
    # ========== 2026-07-25 EN (Dr. Seuss + McCloskey) ==========
    {
        "id": "2026-07-25-en",
        "date": "2026年7月25日 · 星期六",
        "dateShort": "07/25",
        "title": "The Creek That Sang Itself to Sleep (Prenatal)",
        "language": "en",
        "ageGroup": "prenatal",
        "ageLabel": "Prenatal",
        "preview": "Down in the hollow where the ferns grow tall, where the stones are all mossy and the water's so small - there runs a creek that goes tinkle-tink-tink, and it runs all day long, and it runs all night, I think...",
        "moral": "The world is full of songs that go on without stopping - the creek, the wind, the cricket, the frog. They don't stop for night. They just get softer. And if you listen - really listen - you'll hear them singing you to sleep. They've been singing all along.",
        "content": [
            "Down in the hollow where the ferns grow tall, where the stones are all mossy and the water's so small - there runs a creek that goes tinkle-tink-tink, and it runs all day long, and it runs all night, I think.",
            "The creek goes tinkle-tink-tink over the stones. It goes shhhh-shhhh-shhh where the water hits the mud. It goes gurgle-gurgle-gurgle where it passes under the old log bridge, and it goes plip-plop-plip where it drips off the last rock at the end, into the deep pool where the big fish live (well, big for a creek - about the size of your hand).",
            "The creek has a voice. Not a loud voice. Not a show-offy voice. A working voice - the kind of voice that's always there, like the hum of a fridge, like the tick of a clock, like the breathing of someone sleeping next to you.",
            "When the sun goes down behind the ridge, the creek keeps going. Tinkle-tink-tink. It doesn't stop for night. It doesn't know what night is. It just knows: keep going, keep singing, keep moving over the stones.",
            "The fireflies come out. Blink, blink, blink. They land on the ferns by the creek. The ferns don't mind. The creek doesn't mind. Everything by the creek is the not-minding kind.",
            "A raccoon comes down to the water. Dip-dip-dip go his little hands. He's looking for crawfish. He doesn't find any. He doesn't mind. He washes his hands anyway - raccoons are like that, they'll wash their hands whether there's anything to wash them for or not.",
            "The moon comes up. Big and round and slow, like a wheel of cheese rolling across the sky. The moonlight lands on the creek, and the creek turns silver, and the tinkle-tink-tink gets a little bit softer, like even the water wants to be gentle.",
            "The crickets start. Chirp-chirp-chirp. The creek doesn't mind. It adds them to its song. Tinkle-tink-tink-chirp. Shhhh-shhhh-chirp. Gurgle-gurgle-chirp.",
            "The bullfrog says: rummm... rummm... rummm... The creek doesn't mind. It adds that too. Tinkle-tink-rummm. Shhhh-shhh-rummm.",
            "And slowly, slowly, slowly, the creek's song gets softer. And slower. And softer and slower. Until it's not really a song anymore - it's more like a breathing. In and out. Tinkle... shhhh... tinkle... shhhh...",
            "The raccoon falls asleep in the ferns, with his wet little paws tucked under his chin.",
            "The fireflies blink slower and slower and slower, until they're just tiny dots of light that might be stars, or might be reflections, or might be nothing at all.",
            "The creek keeps going. But now it's going slow. Very slow. Like it's walking on tiptoe. Like it's trying not to wake anyone up.",
            "Tinkle... tink... tink...",
            "Shhhh... shhh... shhh...",
            "The moon watches over the hollow. The ferns bend low. The creek breathes in, and breathes out, and breathes in, and breathes out.",
            "And somewhere, not far from the creek, in a house with a warm yellow window, a mother is humming. And the creek hears the humming, and adds it to its song. And the mother hears the creek, and adds it to her hum.",
            "And two songs become one song. And the one song becomes sleep."
        ]
    },
    # ========== 2026-07-26 CN (汤素兰+金波) ==========
    {
        "id": "2026-07-26-cn",
        "date": "2026年7月26日 · 星期日",
        "dateShort": "07/26",
        "title": "想睡觉的小星星（胎教期）",
        "language": "zh",
        "ageGroup": "prenatal",
        "ageLabel": "胎教期",
        "preview": "有一颗小星星，困了。它困了好久好久了。从春天困到夏天，从晚上困到天亮。可是它不能睡。因为它是一颗星星，星星的任务就是亮着...",
        "moral": "你还没来到这个世界，就已经在帮别人的忙了。你用妈妈的声音，点亮了一颗困倦的星星。这世界上的温柔，就是一个传一个——你给了别人一点暖，别人也会还你一束光。",
        "content": [
            "有一颗小星星，困了。",
            "它困了好久好久了。从春天困到夏天，从晚上困到天亮。可是它不能睡。因为它是一颗星星，星星的任务就是亮着，一直到天亮为止。",
            "「我好困呀。」小星星打了个小小的哈欠。这个哈欠很小，但在天上飘出去，变成了一阵软软的风，吹到了地面上。",
            "月亮婆婆看见了，说：「困了就睡呀。」",
            "小星星摇头：「不行。地面上有一栋小房子，窗户里有一位妈妈，她每天晚上都要看我一眼，才肯安心睡觉。我要是睡了，她看不见我，会害怕的。」",
            "月亮婆婆笑了：「那位妈妈不是怕黑。她是习惯了看看你，心里踏实。你亮着，她就觉得全世界都还好好的。」",
            "小星星想了想，更困了。它的光一点一点地暗下去，像一盏快没电的小夜灯。",
            "这时候，小房子窗户里的妈妈，抬头看了看窗外。",
            "「咦，今天那颗星星怎么不太亮了？」妈妈小声说。",
            "她摸了摸肚子，对宝宝说：「宝宝，那颗小星星好像困了。你要不要给它唱首歌？」",
            "妈妈轻轻地哼起了一首歌。那首歌很短，调子很简单，是妈妈自己编的，没有词，只有嗯嗯嗯的声音。",
            "可就是这首歌，穿过窗户，穿过夜空，飘到了小星星的耳朵旁边。",
            "小星星愣了一下。它从来没听过这么温柔的歌。那歌声软软的，暖暖的，像有人用棉花糖裹住了它。",
            "小星星觉得不那么困了。它的光亮了一点点。又亮了一点点。",
            "原来，被别人唱一首歌，比打一百个盹儿都管用。",
            "妈妈唱完了歌，摸摸肚子，轻声说：「宝宝，你看，小星星又亮了。你是不是很厉害？你还没出生呢，就帮了一颗小星星的忙。」",
            "小星星听见了，想笑，可是它已经不那么困了，就使劲儿闪了闪。",
            "那一闪，刚好被妈妈看见了。妈妈也笑了。",
            "那天晚上，小星星一直亮到天亮。不是因为不困了，是因为它的心里暖暖的，光就自然亮了。",
            "它想，原来帮助别人的人，也会被别人帮助。妈妈帮我唱了歌，我帮妈妈亮着灯。而妈妈的宝宝，他还在肚子里呢，就用妈妈的声音帮了我。",
            "这个世界上的温柔，就是这么一个传一个的。"
        ]
    }
]

# ========== Read existing stories ==========
with open(STORIES_JSON, "r", encoding="utf-8") as f:
    existing = json.load(f)

existing_ids = {s["id"] for s in existing}
to_add = [s for s in new_stories if s["id"] not in existing_ids]

print(f"Existing stories: {len(existing)}")
print(f"New stories to add: {len(to_add)}")
for s in to_add:
    print(f"  + {s['id']}: {s['title']}")

# ========== Append and write stories.json ==========
existing.extend(to_add)

with open(STORIES_JSON, "w", encoding="utf-8") as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)

print(f"\nstories.json updated: {len(existing)} total stories")

# ========== Update collection MD ==========
cn_nums = {"0": "零", "1": "一", "2": "二", "3": "三", "4": "四", "5": "五",
           "6": "六", "7": "七", "8": "八", "9": "九"}

def to_chinese_date(date_str):
    """Convert '2026年7月19日' to '二〇二六年七月十九日'"""
    m = re.match(r'(\d+)年(\d+)月(\d+)日', date_str)
    if m:
        y, mo, d = m.groups()
        y_cn = ''.join(cn_nums.get(c, c) for c in y)
        mo_cn = ''.join(cn_nums.get(c, c) for c in mo)
        # Convert day to Chinese number (handle 10-31)
        d_int = int(d)
        if d_int < 10:
            d_cn = cn_nums.get(d, d)
        elif d_int == 10:
            d_cn = "十"
        elif d_int < 20:
            d_cn = "十" + cn_nums.get(str(d_int % 10), str(d_int % 10))
        elif d_int == 20:
            d_cn = "二十"
        elif d_int < 30:
            d_cn = "二十" + cn_nums.get(str(d_int % 10), str(d_int % 10))
        elif d_int == 30:
            d_cn = "三十"
        elif d_int == 31:
            d_cn = "三十一"
        else:
            d_cn = d
        return f"{y_cn}年{mo_cn}月{d_cn}日"
    return date_str

# Read existing MD
with open(COLLECTION_MD, "r", encoding="utf-8") as f:
    md = f.read()

# Build MD entries for new stories
md_additions = []
for s in to_add:
    # Extract date parts
    date_full = s["date"]  # e.g. "2026年7月19日 · 星期日"
    # Get the date part and weekday
    parts = date_full.split(" · ")
    date_part = parts[0]  # "2026年7月19日"
    weekday = parts[1] if len(parts) > 1 else ""
    cn_date = to_chinese_date(date_part)

    # Get short date for header
    short_date_match = re.match(r'(\d+)月(\d+)日', date_part)
    if short_date_match:
        mo_str = short_date_match.group(1)
        d_str = short_date_match.group(2)
        header_date = f"{mo_str}月{d_str}日"
    else:
        header_date = date_part

    # Build story section
    title_for_header = s["title"]
    # Remove age suffix from header title if present
    title_for_header = re.sub(r'[（(].*?[）)]\s*$', '', title_for_header).strip()

    md_additions.append(f"\n## {header_date} — {title_for_header}\n")
    md_additions.append(f"**{cn_date} · {weekday}**\n")
    md_additions.append(f"*{s['title']}*（{s['ageLabel']}）\n")
    # Content paragraphs
    for para in s["content"]:
        md_additions.append(f"\n{para}\n")
    # Moral
    md_additions.append(f"\n> **✨ 故事小语**\n>\n> {s['moral']}\n")
    md_additions.append("\n---\n")

# Append to MD
if md_additions:
    # Remove trailing whitespace from existing MD
    md = md.rstrip() + "\n"
    md += "\n".join(md_additions)

    with open(COLLECTION_MD, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"\nCollection MD updated with {len(to_add)} new stories")

# ========== Update index.html EMBEDDED_STORIES ==========
with open(INDEX_HTML, "r", encoding="utf-8") as f:
    html = f.read()

# Create compressed single-line JSON
embedded_json = json.dumps(existing, ensure_ascii=False)

# Replace the EMBEDDED_STORIES line
# The pattern: const EMBEDDED_STORIES = [...]; (single line)
new_line = f"const EMBEDDED_STORIES = {embedded_json};"

# Use regex to replace the entire EMBEDDED_STORIES assignment line
html = re.sub(
    r'const EMBEDDED_STORIES\s*=\s*\[.*?\];',
    new_line,
    html,
    count=1,
    flags=re.DOTALL
)

with open(INDEX_HTML, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\nindex.html EMBEDDED_STORIES updated ({len(existing)} stories embedded)")

print("\n=== All data files updated successfully! ===")
print(f"Total stories in database: {len(existing)}")
print(f"Stories by language:")
zh_count = sum(1 for s in existing if s.get("language") == "zh")
en_count = sum(1 for s in existing if s.get("language") == "en")
print(f"  Chinese: {zh_count}")
print(f"  English: {en_count}")
