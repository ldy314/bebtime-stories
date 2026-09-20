# -*- coding: utf-8 -*-
"""把出生日期切分点从预产期 2026-09-22 更新为实际出生日 2026-09-15。

宝宝 2026-09-15 出生，故 2026-09-15 及之后的故事属于 0-1 岁阶段。
覆盖活跃四副本中所有含 CHILD_BIRTHDAY / 硬编码出生日期的脚本。
"""
import io, os

TARGETS = [
    r'D:/code test/睡前故事/scripts/prompt-builder.js',
    r'D:/code test/睡前故事/scripts/apply_series_episode.py',
    r'D:/code test/睡前故事/scripts/generate-dangdang.js',
    r'D:/code test/睡前故事/apply_series_episode.py',
    r'D:/code test/睡前故事/github-pages/scripts/prompt-builder.js',
    r'D:/code test/睡前故事/github-pages/scripts/generate-dangdang.js',
    r'D:/code test/睡前故事/github-pages/apply_series_episode.py',
    r'C:/Users/Administrator/WorkBuddy/Claw/github-bedtime-stories/scripts/prompt-builder.js',
    r'C:/Users/Administrator/WorkBuddy/Claw/github-bedtime-stories/scripts/generate-dangdang.js',
    r'C:/Users/Administrator/WorkBuddy/Claw/github-bedtime-stories/apply_series_episode.py',
]

OLD = '2026-09-22'
NEW = '2026-09-15'

for p in TARGETS:
    if not os.path.isfile(p):
        print('MISS', p)
        continue
    s = io.open(p, encoding='utf-8').read()
    n = s.count(OLD)
    if n == 0:
        print('SKIP (no match)', p)
        continue
    s2 = s.replace(OLD, NEW)
    io.open(p, 'w', encoding='utf-8').write(s2)
    print(f'OK  {n} 处  {p}')
print('DONE')
