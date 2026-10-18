# -*- coding: utf-8 -*-
# 补 10-24（周六）每日中英 + 中英科学
D6 = []

def S(id_, date, ds, title, lang, preview, moral, content, sci=False):
    d = {'id': id_, 'date': date, 'dateShort': ds, 'title': title, 'language': lang,
         'ageGroup': '0-1', 'ageLabel': '0-1岁', 'preview': preview, 'moral': moral,
         'content': content, 'category': 'science' if sci else 'regular'}
    if sci:
        d['series'] = 'science'; d['seriesTitle'] = '科学故事'
        d['source'] = 'Children science common sense' if lang == 'en' else '儿童科普常识'
    return d

D6.append(S('2026-10-24-cn', '2026年10月24日 · 星期六', '10/24',
    '暖暖的秋阳（0-1岁）', 'zh',
    '秋天的太阳照在阳台上，暖暖的，不烫。宝宝躺在小垫子上晒太阳，光落在小脚丫上，像盖了一层金被子。',
    '秋天的阳光温柔不刺眼，是宝宝最舒服的自然浴。暖暖的光，会变成小小的能量和好心情。',
    ['秋天的太阳，照阳台。','暖暖的，柔柔的。','小垫子，铺开来。','宝宝躺上去，晒太阳。','光落在小脚丫上。','光落在小手手上。','像盖了层金被子。','眯眯眼，笑一笑。','暖暖的太阳，暖暖的宝宝。']))
D6.append(S('2026-10-24-en', 'October 24, 2026 · Saturday', '10/24',
    'Bubbles Float High (0-1 yr)', 'en',
    'Daddy blows bubbles — round and shiny! One, two, three. They float up slowly and pop, pop, pop!',
    'Bubbles are little balls of air. Chasing them is a happy first game.',
    ['Daddy blows bubbles!','Round and shiny,','up they float, so slow.','One, two, three!','Baby watches, eyes so big.','A bubble lands — pop!','Another one — pop, pop!','Baby kicks, kick, kick!','Bubbles are tiny balls of fun.']))
D6.append(S('2026-10-24-science-cn', '2026年10月24日 · 星期六', '10/24',
    '🔬 秋天的太阳为什么不烫（0-1岁）', 'zh',
    '夏天的太阳晒得皮肤疼，秋天的太阳却暖暖的。因为秋天太阳升得低低的，光是斜斜地照过来，力量散开了。',
    '太阳斜着照，同样的光摊在更大的地方，每小块分到的热就少——所以秋阳暖暖不烫人。',
    ['夏天的太阳，晒得疼。','秋天的太阳，暖暖的。','同一个太阳呀？','对呀，但位置变了。','夏天太阳升得高高的。','光直直地照下来。','秋天太阳升得低低的。','光斜斜地照过来，散开了。','力量摊薄了，就变得温柔啦。'], sci=True))
D6.append(S('2026-10-24-science-en', 'October 24, 2026 · Saturday', '10/24',
    '🔬 Science Story (0-1 yr): Why the Autumn Sun Feels Gentle', 'en',
    'The summer sun burns, but the autumn sun feels soft and warm. Same sun — different angle!',
    'In autumn the sun sits lower, so its light comes in slanted and spreads out. Less heat in each spot — a gentle sun.',
    ['The summer sun is hot, hot!','The autumn sun is warm and soft.','Is it a different sun?','No — the sun just sits lower!','Summer: sun high, light straight down.','Autumn: sun low, light slanted.','The light spreads out wide.','Less heat for every little spot.','That is why autumn feels gentle.'], sci=True))
