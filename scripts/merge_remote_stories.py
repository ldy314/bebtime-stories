# -*- coding: utf-8 -*-
"""Union-merge remote (GitHub Actions generated) stories into local H5 stories.json.

Keeps local ordering, inserts remote-only entries chronologically before the
trailing series episode. Then rebuilds index.html EMBEDDED_STORIES and collections.
"""
import io
import json
import os
import shutil
import subprocess

AUTO = r'C:/Users/Administrator/WorkBuddy/automation-2026-07-16-11-56-46'
H5 = r'C:/Users/Administrator/WorkBuddy/Claw/bedtime-story-app'
BACK = r'D:/code test/睡前故事'
REMOTE = os.path.join(AUTO, '.remote_stories.json')

local_path = os.path.join(H5, 'stories.json')
local = json.load(io.open(local_path, encoding='utf-8'))
remote = json.load(io.open(REMOTE, encoding='utf-8'))

have = {s['id'] for s in local}
missing = [s for s in remote if s['id'] not in have]
if not missing:
    print('NOTHING TO MERGE')
else:
    # insert before the trailing dangdang episode (dated later than the dailies)
    pos = len(local)
    while pos > 0 and local[pos - 1].get('series') == 'dangdang':
        pos -= 1
    for i, s in enumerate(missing):
        local.insert(pos + i, s)
    with io.open(local_path, 'w', encoding='utf-8') as f:
        json.dump(local, f, ensure_ascii=False, indent=2)
    print('MERGED', [s['id'] for s in missing], '-> total', len(local))

# rebuild EMBEDDED_STORIES
idx_path = os.path.join(H5, 'index.html')
text = io.open(idx_path, encoding='utf-8').read()
marker = 'const EMBEDDED_STORIES = '
lines = text.split('\n')
for i, line in enumerate(lines):
    if line.startswith(marker):
        lines[i] = marker + json.dumps(local, ensure_ascii=False) + ';'
        break
else:
    raise SystemExit('ERROR: EMBEDDED_STORIES not found')
io.open(idx_path, 'w', encoding='utf-8').write('\n'.join(lines))
print('UPDATED index.html EMBEDDED_STORIES')

for gen in ['generate-collection-html.js', 'generate-collection-md.js']:
    gp = os.path.join(AUTO, gen)
    if os.path.exists(gp):
        subprocess.run(['node', gp], cwd=AUTO, check=True)
        print('RAN', gen)

coll = os.path.join(AUTO, 'bedtime-story-collection.html')
if os.path.exists(coll):
    shutil.copyfile(coll, os.path.join(AUTO, 'collection-deploy', 'index.html'))
    shutil.copyfile(coll, os.path.join(BACK, 'bedtime-story-collection.html'))
md = r'C:/Users/Administrator/WorkBuddy/Claw/bedtime-story-collection.md'
if os.path.exists(md):
    shutil.copyfile(md, os.path.join(BACK, 'bedtime-story-collection.md'))
print('DONE merge')
