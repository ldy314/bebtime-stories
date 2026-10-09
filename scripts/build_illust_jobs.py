# -*- coding: utf-8 -*-
"""构建插图生成任务清单：文件名按既有约定，提示词按故事内容生成。"""
import json, io, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'D:/code test/睡前故事'
d = json.load(io.open(os.path.join(BASE, 'stories.json'), encoding='utf-8'))
match = json.load(io.open(os.path.join(BASE, 'scripts/illust_match.json'), encoding='utf-8'))
missing_ids = match['missing_ids']

ILLEGAL = r'\\/:*?"<>|'
def sanitize(name):
    for ch in ILLEGAL:
        name = name.replace(ch, '')
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def core_title(t):
    t = t.replace('🔬', '').strip()
    t = re.sub(r'[【\[]胎教期[】\]]', '', t)
    t = re.sub(r'[（(]胎教期[）)]', '', t)
    t = re.sub(r'[（(]0-1岁[）)]', '', t)
    t = re.sub(r'\(Prenatal\)', '', t, flags=re.I)
    t = re.sub(r'\(0-1\s*yr\)', '', t, flags=re.I)
    t = t.strip()
    t = re.sub(r'^科学故事[:：]?', '', t)
    t = re.sub(r'^Science Story[:：]?', '', t, flags=re.I)
    return t.strip(' :：')

def filename_for(s):
    t = s['title']
    sci = s.get('category') == 'science'
    dd = s.get('series') == 'dangdang'
    zh = s['language'] == 'zh'
    prenatal = s.get('ageGroup') == 'prenatal'
    if dd:
        return sanitize(t) + '.png'
    if sci:
        body = core_title(t)
        if zh:
            mark = '（胎教期）' if prenatal else '（0-1岁）'
            return sanitize(f'科学故事{mark}{body}') + '.png'
        mark = '(Prenatal)' if prenatal else '(0-1 yr)'
        return sanitize(f'Science Story {mark} {body}') + '.png'
    # 日常
    if zh:
        if '（胎教期）' in t or '（0-1岁）' in t:
            return sanitize(t) + '.png'
        mark = '（胎教期）' if prenatal else '（0-1岁）'
        return sanitize(t + mark) + '.png'
    return sanitize(t) + '.png'

STYLE = {
    'zh': '儿童睡前故事绘本插画，温暖柔和的水彩画风，色调温馨治愈，画面安静梦幻，竖版构图，画面中不要出现任何文字、字母或符号。',
    'en': '儿童睡前故事绘本插画，温暖柔和的水彩画风，色调温馨治愈，画面安静梦幻，竖版构图，画面中不要出现任何文字、字母或符号。',
    'sci': '儿童科普绘本插画，以可爱拟人化、温和直观的方式表现科学主题，温暖柔和色调，圆润造型，竖版构图，画面中不要出现任何文字、数字、公式或符号。',
    'baby': '婴儿绘本插画，极简构图，大面积柔和留白，圆润可爱的造型，高亮度粉彩色调，安静温柔，竖版构图，画面中不要出现任何文字。',
    'dd': '以参考图中的黑色小猫「当当」（黄色大眼睛、浅蓝色领结、白色小爪子）为主角的儿童绘本插画，扁平可爱画风，温暖柔和色调，竖版构图，画面中不要出现任何文字。',
}

def prompt_for(s):
    sci = s.get('category') == 'science'
    dd = s.get('series') == 'dangdang'
    prenatal = s.get('ageGroup') == 'prenatal'
    ct = core_title(s['title'])
    prev = re.sub(r'\s+', ' ', (s.get('preview') or '')).strip()
    if len(prev) > 110:
        prev = prev[:110]
    if dd:
        st = STYLE['dd']
    elif sci:
        st = STYLE['sci']
    elif not prenatal:
        st = STYLE['baby']
    else:
        st = STYLE['zh' if s['language'] == 'zh' else 'en']
    scene = f'故事《{ct}》的场景：{prev}' if prev else f'故事《{ct}》的场景。'
    return st + scene

jobs = []
seen_names = {}
for s in d:
    if s['id'] not in missing_ids:
        continue
    fn = filename_for(s)
    # 防重名
    if fn in seen_names:
        base, ext = os.path.splitext(fn)
        fn = f'{base}-{s["id"]}{ext}'
    seen_names[fn] = s['id']
    jobs.append({
        'id': s['id'],
        'filename': fn,
        'prompt': prompt_for(s),
        'dangdang': s.get('series') == 'dangdang',
        'title': s['title'],
    })

out = os.path.join(BASE, 'scripts/illust_jobs.json')
json.dump(jobs, io.open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('jobs:', len(jobs))
import collections
c = collections.Counter('dd' if j['dangdang'] else 'story' for j in jobs)
print(c)
# 抽查文件名
for j in jobs[:3] + jobs[-3:]:
    print(' ', j['filename'])
# 检查与现有文件冲突
exist = set(os.listdir(os.path.join(BASE, '插图')))
conf = [j['filename'] for j in jobs if j['filename'] in exist]
print('与现有文件重名:', conf[:10], '共', len(conf))
