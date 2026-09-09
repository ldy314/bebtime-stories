# -*- coding: utf-8 -*-
"""注入 2026-09-11 ~ 09-21 批次：37 篇（28 每日/科学 + 8 补科学 + 1 当当 ep27）。

- 四副本 stories.json 追加（按 id 去重）
- 四副本 index.html 的 EMBEDDED_STORIES 单行重写
- dangdang-series-state.json 修正对齐（next episode -> 28）
- node 重生成 collection html/md，并复制到四副本
"""
import io, json, os, re, sys, shutil, subprocess, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batch_data_1 import NEW_RAW_1
from batch_data_2 import NEW_RAW_2
from batch_data_3 import NEW_RAW_3

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
        'ageGroup': 'prenatal',
        'ageLabel': '胎教期',
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
        base['source'] = '儿童科普常识'
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


NEW = [build_story(r) for r in (NEW_RAW_1 + NEW_RAW_2 + NEW_RAW_3)]
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

# ---- 对齐 dangdang-series-state ----
state_path = os.path.join(AUTO, 'dangdang-series-state.json')
state = json.load(io.open(state_path, encoding='utf-8'))
state['episode'] = 28
state['lastGeneratedDate'] = '2026-09-19'
state.setdefault('continuity', []).append(
    '第27集《当当和大运河的风筝》：周六全家去大运河边放燕子风筝，一阵大风把风筝吹进老柳树杈；'
    '当当想起ep26「先喊爸爸妈妈」的约定，放下爪子呼救，爸爸竹竿轻挑取回风筝、妈妈扶稳当当；'
    '呼应ep26月饼事件，落点「风筝有线牵着才不会丢——线的那头是家」。state 曾落后于实际（ep22-26 由其他通道注入），本次修正 next=28。'
)
json.dump(state, io.open(state_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('state aligned: next episode =', state['episode'])

# ---- 重生成 collection（读 H5 stories.json） ----
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
    target = os.path.join(loc, 'collection.html')
    if os.path.exists(coll_html):
        shutil.copyfile(coll_html, target)
        print('  copied collection.html ->', target)

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
