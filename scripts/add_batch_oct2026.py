# -*- coding: utf-8 -*-
"""注入 2026-10-01 ~ 10-17 批次：71 篇（每日中英 34 + 科学 34 + 当当 ep30-32）。

- 四副本 stories.json 追加（按 id 去重）
- 四副本 index.html EMBEDDED_STORIES 单行重写
- dangdang-series-state.json: next -> 33，continuity 追加 ep30/31/32
- collection html/md 重生成并复制到四副本
"""
import io, json, os, re, sys, shutil, subprocess, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from oct_data_1 import RAW_OCT_1
from oct_data_2 import RAW_OCT_2
from oct_data_3 import RAW_OCT_3
from oct_data_4 import RAW_OCT_4

AUTO = r'C:/Users/Administrator/WorkBuddy/automation-2026-07-16-11-56-46'
LOCS = [
    r'C:/Users/Administrator/WorkBuddy/Claw/github-bedtime-stories',
    r'C:/Users/Administrator/WorkBuddy/Claw/bedtime-story-app',
    r'D:/code test/睡前故事',
    r'D:/code test/睡前故事/github-pages',
]
WEEKDAYS = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
EMB_RE = re.compile(r'const EMBEDDED_STORIES = \[.*?\];', re.S)


def fmt_date(d):
    return f'{d.year}年{d.month}月{d.day}日 · {WEEKDAYS[d.weekday()]}'


def fmt_short(d):
    return f'{d.month:02d}/{d.day:02d}'


def build_story(raw):
    d = datetime.date.fromisoformat(raw['dateStr'])
    base = {
        'date': fmt_date(d),
        'dateShort': fmt_short(d),
        'title': raw['title'],
        'language': raw.get('language', 'zh'),
        'ageGroup': '0-1',
        'ageLabel': '0-1岁',
        'preview': raw['preview'],
        'moral': raw['moral'],
        'content': raw['content'],
    }
    kind = raw['kind']
    if kind == 'dangdang':
        ep = raw['episode']
        base['id'] = f'dangdang-ep{ep:02d}-zh'
        base['series'] = 'dangdang'
        base['seriesTitle'] = '黑猫当当历险记'
        base['episode'] = ep
    elif kind == 'science':
        suffix = 'cn' if raw['language'] == 'zh' else 'en'
        base['id'] = f"{raw['dateStr']}-science-{suffix}"
        base['category'] = 'science'
        base['series'] = 'science'
        base['seriesTitle'] = '科学故事'
        base['source'] = '儿童科普常识' if raw['language'] == 'zh' else 'Children science common sense'
    else:
        suffix = 'cn' if raw['language'] == 'zh' else 'en'
        base['id'] = f"{raw['dateStr']}-{suffix}"
        base['category'] = 'regular'
    return base


def check_curly(articles):
    bad = []
    for a in articles:
        text = a['title'] + a['preview'] + a['moral'] + ''.join(a['content'])
        for ch in '“”‘’':
            if ch in text:
                bad.append((a['id'], ch))
    return bad


NEW = [build_story(r) for r in (RAW_OCT_1 + RAW_OCT_2 + RAW_OCT_3 + RAW_OCT_4)]
bad = check_curly(NEW)
if bad:
    print('ERROR: curly quotes found:', bad)
    sys.exit(1)
print(f'built {len(NEW)} stories, no curly quotes')

for loc in LOCS:
    sp = os.path.join(loc, 'stories.json')
    stories = json.load(io.open(sp, encoding='utf-8'))
    existing = {s.get('id') for s in stories}
    added = 0
    for nw in NEW:
        if nw['id'] in existing:
            print('  DUP skip:', nw['id'])
            continue
        stories.append(nw)
        added += 1
        existing.add(nw['id'])
    json.dump(stories, io.open(sp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    idxp = os.path.join(loc, 'index.html')
    if os.path.isfile(idxp):
        html = io.open(idxp, encoding='utf-8').read()
        new_line = 'const EMBEDDED_STORIES = ' + json.dumps(stories, ensure_ascii=False, separators=(',', ':')) + ';'
        if EMB_RE.search(html):
            html = EMB_RE.sub(new_line, html, count=1)
            io.open(idxp, 'w', encoding='utf-8').write(html)
        else:
            print('  WARN: EMBEDDED_STORIES not found in', idxp)
    print(f'  {loc}: +{added} 篇，总计 {len(stories)} 篇')

# ---- series state 对齐 ----
state_path = os.path.join(AUTO, 'dangdang-series-state.json')
state = json.load(io.open(state_path, encoding='utf-8'))
if state.get('episode') != 30:
    print('WARN: state next episode =', state.get('episode'), '(expect 30)')
state['episode'] = 33
state['lastGeneratedDate'] = '2026-10-17'
state['continuity'].append(
    '第30集《当当和小手》：宝宝醒着挥小手，小手抓住当当的尾巴尖，当当选了「不动」，把尾巴借作宝宝的第一个玩具；'
    '妈妈见证，落点「轻轻的相遇用轻轻的回应」。'
)
state['continuity'].append(
    '第31集《当当听宝宝咿呀》：宝宝开始咿咿呀呀发声，当当竖耳回应一声「喵」，一来一往完成「第一段对话」，'
    '爸爸悄悄录下；落点「认真的听众是最好的回应」。'
)
state['continuity'].append(
    '第32集《当当和第一次出门》：秋日全家带宝宝第一次下楼晒太阳，当当不前不后护送，提醒大金毛放轻脚步；'
    '落叶落在盖被上宝宝梦中笑；归途当当认路领航；落点「世界很大慢慢认识，家的方向永远记得」。'
)
json.dump(state, io.open(state_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('state aligned: next episode =', state['episode'])

for dst in [r'D:/code test/睡前故事/dangdang-series-state.json',
            r'D:/code test/睡前故事/github-pages/dangdang-series-state.json']:
    shutil.copyfile(state_path, dst)
    print('  state synced ->', dst)

# ---- 重生成 collection ----
for gen in ['generate-collection-html.js', 'generate-collection-md.js']:
    gp = os.path.join(AUTO, gen)
    if os.path.exists(gp):
        try:
            subprocess.run(['node', gp], cwd=AUTO, check=True)
            print('RAN', gen)
        except Exception as e:
            print('WARN: failed', gen, e)

coll_html = os.path.join(AUTO, 'bedtime-story-collection.html')
for loc in LOCS:
    for name in ['collection.html', 'bedtime-story-collection.html']:
        if os.path.exists(coll_html):
            shutil.copyfile(coll_html, os.path.join(loc, name))

md_candidates = [
    os.path.join(AUTO, '..', 'bedtime-story-collection.md'),
    r'C:/Users/Administrator/WorkBuddy/Claw/bedtime-story-collection.md',
]
md_src = next((p for p in md_candidates if os.path.exists(p)), None)
if md_src:
    for dst in [r'D:/code test/睡前故事/bedtime-story-collection.md',
                r'D:/code test/睡前故事/github-pages/bedtime-story-collection.md']:
        shutil.copyfile(md_src, dst)
        print('  copied collection md ->', dst)

print('DONE')
