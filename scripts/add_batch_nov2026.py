# -*- coding: utf-8 -*-
# 10-18 ~ 11-03 批次注入：70 篇 → 四副本（stories.json + index.html EMBEDDED_STORIES）
# + 当当 state 推进到 next=35 + 重生成合集页
import json, io, re, os, sys, shutil, subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nov_data_1 import D1
from nov_data_2 import D2
from nov_data_3 import D3
from nov_data_4 import D4
from nov_data_5 import DD
from nov_data_6 import D6

ALL = D1 + D2 + D3 + D4 + DD + D6
print('待注入:', len(ALL), '篇')

EMB_RE = re.compile(r'const EMBEDDED_STORIES = \[.*?\];', re.S)
LOCS = [r'C:/Users/Administrator/WorkBuddy/Claw/github-bedtime-stories',
        r'C:/Users/Administrator/WorkBuddy/Claw/bedtime-story-app',
        r'D:/code test/睡前故事',
        r'D:/code test/睡前故事/github-pages']

# 撞 id 防护：与现有库比对，base id 已存在则改 -2
for loc in LOCS:
    sp = os.path.join(loc, 'stories.json')
    ss = json.load(io.open(sp, encoding='utf-8'))
    have = {s['id'] for s in ss}
    n_add, n_ren = 0, 0
    for s in ALL:
        sid = s['id']
        if sid in have:
            if re.match(r'^\d{4}-\d{2}-\d{2}-(cn|en)$', sid) or sid.endswith('science-cn') or sid.endswith('science-en'):
                s['id'] = sid + '-2'
                n_ren += 1
            else:
                print('跳过已存在:', sid); continue
        if s['id'] in have:
            raise SystemExit('改 -2 后仍撞: ' + s['id'])
        ss.append(dict(s)); have.add(s['id']); n_add += 1
    json.dump(ss, io.open(sp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    nid = [x['id'] for x in ss]
    assert len(nid) == len(set(nid)), 'DUP ID in ' + loc
    html = io.open(os.path.join(loc, 'index.html'), encoding='utf-8').read()
    new_line = 'const EMBEDDED_STORIES = ' + json.dumps(ss, ensure_ascii=False, separators=(',', ':')) + ';'
    io.open(os.path.join(loc, 'index.html'), 'w', encoding='utf-8').write(EMB_RE.sub(new_line, html, count=1))
    print(loc[-25:], ': +', n_add, '(改名', n_ren, ') -> 总', len(ss))

# 当当 state 推进（以 D 盘为权威）
AUTH = r'D:/code test/睡前故事/dangdang-series-state.json'
st = json.load(io.open(AUTH, encoding='utf-8'))
if st['episode'] < 35:
    st['episode'] = 35
    st['lastGeneratedDate'] = '2026-10-31'
    st['continuity'].append('第33集《当当和红气球》：红气球飘进院子，当当不用爪子改用尾巴尖压住线头护球；气球系上摇篮边，宝宝追看、当当守线；呼应ep27风筝「线的那头是家」。')
    st['continuity'].append('第34集《当当和南瓜灯》：爸爸雕南瓜、妈妈画笑脸，南瓜灯点亮时当当先跳开三步再一步步凑近；落点「看懂了的奇怪就是温暖」，南瓜灯守在宝宝小床边。')
    json.dump(st, io.open(AUTH, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    for dst in [r'C:/Users/Administrator/WorkBuddy/automation-2026-07-16-11-56-46/dangdang-series-state.json',
                r'D:/code test/睡前故事/github-pages/dangdang-series-state.json',
                r'C:/Users/Administrator/WorkBuddy/Claw/github-bedtime-stories/dangdang-series-state.json',
                r'C:/Users/Administrator/WorkBuddy/Claw/bedtime-story-app/dangdang-series-state.json']:
        shutil.copyfile(AUTH, dst)
    print('state 推进到 next=35，已同步')

# 重生成合集页
os.chdir(r'C:/Users/Administrator/WorkBuddy/automation-2026-07-16-11-56-46')
for cmd in ['node generate-collection-html.js', 'node generate-collection-md.js']:
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(cmd, '->', (r.stdout or '').strip()[-60:] or 'ok')
for loc in LOCS:
    for f in ['bedtime-story-collection.html']:
        src = f'C:/Users/Administrator/WorkBuddy/automation-2026-07-16-11-56-46/{f}'
        shutil.copyfile(src, os.path.join(loc, 'collection.html'))
        shutil.copyfile(src, os.path.join(loc, f))
    for f in ['bedtime-story-collection.md']:
        src = f'C:/Users/Administrator/WorkBuddy/{f}'
        if os.path.exists(src):
            shutil.copyfile(src, os.path.join(loc, f))
print('合集页四副本同步完成')
