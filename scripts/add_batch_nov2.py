# -*- coding: utf-8 -*-
# 11-04 ~ 11-30 批次注入（幂等版：重复运行安全，已存在 id 直接跳过，不改写任何已有条目）
import json, io, re, os, sys, shutil, subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dec_data_1 import DEC1
from dec_data_2 import DEC2
from dec_data_3 import DEC3
from dec_data_4 import DEC4
from dec_data_5 import DEC5
from dec_data_6 import DEC6
from dec_dd import DD2

ALL = DEC1 + DEC2 + DEC3 + DEC4 + DEC5 + DEC6 + DD2
print('待注入:', len(ALL), '篇')

EMB_RE = re.compile(r'const EMBEDDED_STORIES = \[.*?\];', re.S)
LOCS = [r'C:/Users/Administrator/WorkBuddy/Claw/github-bedtime-stories',
        r'C:/Users/Administrator/WorkBuddy/Claw/bedtime-story-app',
        r'D:/code test/睡前故事',
        r'D:/code test/睡前故事/github-pages']

for loc in LOCS:
    sp = os.path.join(loc, 'stories.json')
    ss = json.load(io.open(sp, encoding='utf-8'))
    have = {s['id'] for s in ss}
    n_add, n_skip = 0, 0
    for s in ALL:
        if s['id'] in have:
            n_skip += 1
            continue
        ss.append(dict(s)); have.add(s['id']); n_add += 1
    json.dump(ss, io.open(sp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    nid = [x['id'] for x in ss]
    assert len(nid) == len(set(nid)), 'DUP ID in ' + loc
    html = io.open(os.path.join(loc, 'index.html'), encoding='utf-8').read()
    new_line = 'const EMBEDDED_STORIES = ' + json.dumps(ss, ensure_ascii=False, separators=(',', ':')) + ';'
    io.open(os.path.join(loc, 'index.html'), 'w', encoding='utf-8').write(EMB_RE.sub(new_line, html, count=1))
    print(loc[-25:], ': +', n_add, '(跳过', n_skip, ') -> 总', len(ss))

# 当当 state 推进（以 D 盘为权威，next=39）
AUTH = r'D:/code test/睡前故事/dangdang-series-state.json'
st = json.load(io.open(AUTH, encoding='utf-8'))
if st['episode'] < 39:
    st['episode'] = 39
    st['lastGeneratedDate'] = '2026-11-28'
    st['continuity'].append('第35集《当当和会走路的月亮》（自动化）：西太湖月亮倒影，安全主题「不往水边冲」，结尾南瓜灯仍守小床。')
    st['continuity'].append('第36集《当当和小脚印》：霜晨发现小脚印通向柴堆，当当侦探式追踪找到迷路小刺猬，不伸爪、唤爸爸帮忙，送回篱笆落叶堆冬眠；落点「小小的脚印也通向回家的路」。')
    st['continuity'].append('第37集《当当和第一场雪》：雪籽半夜转初雪，当当第一次见雪、伸爪试凉、雪地盖梅花印，爸爸堆歪雪人；当当与宝宝隔窗碰鼻尖；落点「守护一天都不会化」。')
    st['continuity'].append('第38集《当当和橘子灯》：妈妈做橘子灯（星月小孔），呼应ep34南瓜灯「光里是暖」；橘子灯与南瓜灯并排守小床，宝宝隔影够光；落点「灯在哪儿，家就在哪儿」。')
    json.dump(st, io.open(AUTH, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    for dst in [r'C:/Users/Administrator/WorkBuddy/automation-2026-07-16-11-56-46/dangdang-series-state.json',
                r'D:/code test/睡前故事/github-pages/dangdang-series-state.json',
                r'C:/Users/Administrator/WorkBuddy/Claw/github-bedtime-stories/dangdang-series-state.json',
                r'C:/Users/Administrator/WorkBuddy/Claw/bedtime-story-app/dangdang-series-state.json']:
        shutil.copyfile(AUTH, dst)
    print('state 推进到 next=39（含自动化 ep35），已同步')

# 重生成合集页
os.chdir(r'C:/Users/Administrator/WorkBuddy/automation-2026-07-16-11-56-46')
for cmd in ['node generate-collection-html.js', 'node generate-collection-md.js']:
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(cmd, '->', (r.stdout or '').strip().splitlines()[-1][:60] if (r.stdout or '').strip() else 'ok')
for loc in LOCS:
    src_h = r'C:/Users/Administrator/WorkBuddy/automation-2026-07-16-11-56-46/bedtime-story-collection.html'
    shutil.copyfile(src_h, os.path.join(loc, 'collection.html'))
    shutil.copyfile(src_h, os.path.join(loc, 'bedtime-story-collection.html'))
    src_m = r'C:/Users/Administrator/WorkBuddy/bedtime-story-collection.md'
    if os.path.exists(src_m):
        shutil.copyfile(src_m, os.path.join(loc, 'bedtime-story-collection.md'))
print('合集页四副本同步完成')
