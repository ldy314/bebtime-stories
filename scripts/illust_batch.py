# -*- coding: utf-8 -*-
"""插图批处理循环工具。
用法:
  python illust_batch.py rename   # 把 _new 里的图按标题匹配重命名到 插图/ 并更新进度
  python illust_batch.py next N   # 打印接下来 N 个待生成任务(JSON 行: idx/id/filename/dangdang/prompt)
  python illust_batch.py status   # 打印进度统计
"""
import json, io, os, re, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'D:/code test/睡前故事'
NEW = os.path.join(BASE, '插图', '_new')
DST = os.path.join(BASE, '插图')
JOBS = os.path.join(BASE, 'scripts/illust_jobs.json')
PROG = os.path.join(BASE, 'scripts/illust_progress.json')

jobs = json.load(io.open(JOBS, encoding='utf-8'))
prog = json.load(io.open(PROG, encoding='utf-8')) if os.path.isfile(PROG) else {}

def core(job):
    m = re.search(r'《(.+?)》', job['prompt'])
    t = m.group(1) if m else job['title']
    return t

def norm(s):
    return re.sub(r'[\s_《》「」\[\]()（）:：,，.。\-\'"!?！？·]', '', s).lower()

def save():
    json.dump(prog, io.open(PROG, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

cmd = sys.argv[1] if len(sys.argv) > 1 else 'status'

if cmd == 'rename':
    files = [f for f in os.listdir(NEW) if f.lower().endswith('.png')]
    moved, orphan = [], []
    used = set()
def lcp(a, b):
    n = 0
    for x, y in zip(a, b):
        if x != y:
            break
        n += 1
    return n

def cmd_rename():
    files = [f for f in os.listdir(NEW) if f.lower().endswith('.png')]
    moved, orphan = [], []
    used = set()
    for f in files:
        nf = norm(f)
        hit = None
        for job in jobs:
            if job['id'] in prog or job['id'] in used:
                continue
            c = norm(core(job))
            # c 完整包含于 nf（正常），或 nf 与 c 的最长公共前缀足够长（自动文件名被截断）
            if c and (c in nf or lcp(nf, c) >= min(len(c), 10)):
                hit = job
                break
        if hit:
            shutil.move(os.path.join(NEW, f), os.path.join(DST, hit['filename']))
            prog[hit['id']] = hit['filename']
            used.add(hit['id'])
            moved.append(hit['filename'])
        else:
            orphan.append(f)
    save()
    print('moved:', len(moved))
    for m_ in moved:
        print('  OK', m_)
    if orphan:
        print('orphan(未匹配, 留在_new):')
        for o in orphan:
            print('  ??', o)

if cmd == 'rename':
    cmd_rename()
elif cmd == 'next':
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    pend = [j for j in jobs if j['id'] not in prog][:n]
    out = [{'idx': jobs.index(j), 'id': j['id'], 'filename': j['filename'],
            'dangdang': j['dangdang'], 'prompt': j['prompt']} for j in pend]
    print(json.dumps(out, ensure_ascii=False, indent=1))
elif cmd == 'status':
    print('total:', len(jobs), ' done:', len(prog), ' remaining:', len(jobs) - len(prog))
    newfiles = [f for f in os.listdir(NEW) if f.lower().endswith('.png')] if os.path.isdir(NEW) else []
    print('in _new:', len(newfiles))
