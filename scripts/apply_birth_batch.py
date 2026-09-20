# -*- coding: utf-8 -*-
"""宝宝出生批次注入（2026-09-15 出生 → 0-1 岁）

1. 修正 2026-09-11 ~ 09-30 条目的中文星期（既有批次 weekday 偏移 1 天）
2. 改写 2026-09-15 ~ 09-21 共 28 篇为「出生后 0-1 岁」口吻；dangdang-ep27 仅改阶段标签
3. 追加 2026-09-22 ~ 09-30 每日 4 篇（中/英日常 + 中/英科学）共 36 篇
4. 追加 黑猫当当历险记 ep28 / ep29
5. 四副本同步 stories.json + index.html EMBEDDED_STORIES

素材来源：scripts/rewrite_out_*.json、scripts/generate_out_*.json、scripts/generate_dangdang.json
"""
import io, json, os, re, datetime, shutil, sys

BASE = r'D:/code test/睡前故事'
SC = os.path.join(BASE, 'scripts')
LOCS = [
    r'C:/Users/Administrator/WorkBuddy/Claw/github-bedtime-stories',
    r'C:/Users/Administrator/WorkBuddy/Claw/bedtime-story-app',
    BASE,
    r'D:/code test/睡前故事/github-pages',
]
W = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
EMB_RE = re.compile(r'const EMBEDDED_STORIES = \[.*?\];', re.S)
CURLY = '“”‘’'


def fmt_date(dt):
    return f'{dt.year}年{dt.month}月{dt.day}日 · {W[dt.weekday()]}'


def fmt_short(dt):
    return f'{dt.month:02d}/{dt.day:02d}'


def load(n):
    return json.load(io.open(os.path.join(SC, n), encoding='utf-8'))


rewrites = []
for n in ['rewrite_out_a.json', 'rewrite_out_b.json', 'rewrite_out_c.json', 'rewrite_out_d.json']:
    rewrites += load(n)
news = []
for n in ['generate_out_a.json', 'generate_out_b.json', 'generate_out_c.json', 'generate_out_d.json', 'generate_out_e.json']:
    news += load(n)
dang = load('generate_dangdang.json')

print(f'载入：改写 {len(rewrites)} 篇 / 新增 {len(news)} 篇 / 当当 {len(dang)} 篇')


def audit(items, label):
    bad = []
    for it in items:
        t = it['title'] + it['preview'] + it['moral'] + ''.join(it['content'])
        for ch in CURLY:
            if ch in t:
                bad.append((it.get('id'), '弯引号'))
        if '蟹' in t:
            bad.append((it.get('id'), '蟹'))
        if len(it['content']) < 4:
            bad.append((it.get('id'), f"段落少{len(it['content'])}"))
    print(f'  {label}: {len(items)} 篇，问题 {len(bad)}')
    for b in bad[:8]:
        print('   !', b)
    return bad


allbad = audit(rewrites, '改写') + audit(news, '新增') + audit(dang, '当当')
if allbad:
    sys.exit('素材有问题，终止')

TARGET_SHORTS = {f'09/{d:02d}' for d in range(11, 31)}

for L in LOCS:
    sp = os.path.join(L, 'stories.json')
    if not os.path.isfile(sp):
        print('MISS', sp)
        continue
    shutil.copyfile(sp, sp + '.bak_birth')
    stories = json.load(io.open(sp, encoding='utf-8'))
    byid = {s['id']: s for s in stories}
    before = len(stories)

    # A. 日期星期修正（09/11 ~ 09/30）
    datefix = 0
    for s in stories:
        if s.get('dateShort') not in TARGET_SHORTS:
            continue
        m = re.match(r'^(\d{4}-\d{2}-\d{2})', s['id'])
        if not m:
            continue
        nd = fmt_date(datetime.date.fromisoformat(m.group(1)))
        if s.get('date') != nd:
            s['date'] = nd
            datefix += 1

    # B. 改写替换
    miss = [r['id'] for r in rewrites if r['id'] not in byid]
    if miss:
        sys.exit('改写目标缺失: ' + str(miss))
    for r in rewrites:
        s = byid[r['id']]
        s['title'] = r['title']
        s['preview'] = r['preview']
        s['moral'] = r['moral']
        s['content'] = r['content']
        s['ageGroup'] = '0-1'
        s['ageLabel'] = '0-1 yr' if s.get('language') == 'en' else '0-1岁'

    # ep27 仅改阶段标签
    if 'dangdang-ep27-zh' in byid:
        byid['dangdang-ep27-zh']['ageGroup'] = '0-1'
        byid['dangdang-ep27-zh']['ageLabel'] = '0-1岁'

    # C. 追加每日新故事
    added = 0
    for n in news:
        if n['id'] in byid:
            print('  DUP skip', n['id'])
            continue
        dt = datetime.date.fromisoformat(n['id'][:10])
        e = {
            'date': fmt_date(dt), 'dateShort': fmt_short(dt), 'title': n['title'],
            'language': n['language'], 'ageGroup': '0-1',
            'ageLabel': '0-1 yr' if n['language'] == 'en' else '0-1岁',
            'preview': n['preview'], 'moral': n['moral'], 'content': n['content'],
            'id': n['id'], 'category': n['category'],
        }
        if n.get('series') == 'science':
            e['series'] = 'science'
            e['seriesTitle'] = '科学故事'
            e['source'] = n.get('source', '儿童科普常识')
        stories.append(e)
        byid[n['id']] = e
        added += 1

    # D. 追加当当
    for d in dang:
        if d['id'] in byid:
            print('  DUP skip', d['id'])
            continue
        mm, dd = d['dateShort'].split('/')
        dt = datetime.date(2026, int(mm), int(dd))
        e = {
            'date': fmt_date(dt), 'dateShort': d['dateShort'], 'title': d['title'],
            'language': 'zh', 'ageGroup': '0-1', 'ageLabel': '0-1岁',
            'preview': d['preview'], 'moral': d['moral'], 'content': d['content'],
            'id': d['id'], 'series': 'dangdang', 'seriesTitle': '黑猫当当历险记',
            'episode': d['episode'],
        }
        stories.append(e)
        byid[d['id']] = e
        added += 1

    json.dump(stories, io.open(sp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

    # E. 重写 index.html 的 EMBEDDED_STORIES
    idxp = os.path.join(L, 'index.html')
    emb_ok = False
    if os.path.isfile(idxp):
        html = io.open(idxp, encoding='utf-8').read()
        line = 'const EMBEDDED_STORIES = ' + json.dumps(stories, ensure_ascii=False, separators=(',', ':')) + ';'
        if EMB_RE.search(html):
            html = EMB_RE.sub(lambda m: line, html, count=1)
            io.open(idxp, 'w', encoding='utf-8').write(html)
            emb_ok = True
    n01 = sum(1 for s in stories if s.get('ageGroup') == '0-1')
    print(f'{L}\n  {before} -> {len(stories)} (+{added}) | 星期修正 {datefix} | 0-1岁共 {n01} | embed={emb_ok}')

print('DONE')
