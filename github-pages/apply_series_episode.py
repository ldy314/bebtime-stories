# -*- coding: utf-8 -*-
"""Apply a generated 黑猫当当历险记 episode into the bedtime-story system.

Reads an episode JSON file (authored by the AI) and:
  1. Appends the episode object to H5 stories.json (series/seriesTitle/episode fields).
  2. Updates the H5 index.html EMBEDDED_STORIES single-line array.
  3. Advances dangdang-series-state.json (episode, continuity log, arc, linkages).
  4. Regenerates collection HTML + MD via the existing node generators.
  5. Copies fresh artifacts to collection-deploy and D: backup (D drive).

Usage: python apply_series_episode.py <episode_json_path>
"""
import json
import os
import re
import sys
import shutil
import subprocess
from datetime import datetime, timedelta

AUTO = r'C:/Users/Administrator/WorkBuddy/automation-2026-07-16-11-56-46'
H5 = r'C:/Users/Administrator/WorkBuddy/Claw/bedtime-story-app'
BACK = r'D:/code test/睡前故事'
CHILD_BIRTHDAY = '2026-09-22'
WEEKDAYS = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']


def resolve_path(preferred, fallback):
    return preferred if os.path.exists(preferred) else fallback


def get_age_info(date_str):
    b = datetime.strptime(CHILD_BIRTHDAY, '%Y-%m-%d')
    c = datetime.strptime(date_str, '%Y-%m-%d')
    if c < b:
        return 'prenatal', '胎教期'
    diff = (c - b).days / 365.25
    if diff < 1:
        return '0-1', '0-1岁'
    if diff < 3:
        return '1-3', '1-3岁'
    if diff < 6:
        return '3-6', '3-6岁'
    return '6+', '6岁以上'


def latest_saturday_on_or_before(today):
    d = today
    while d.weekday() != 5:  # 5 = Saturday
        d -= timedelta(days=1)
    return d


def main():
    if len(sys.argv) < 2:
        print('USAGE: python apply_series_episode.py <episode_json>')
        sys.exit(1)

    ep_path = sys.argv[1]
    ep = json.load(open(ep_path, 'r', encoding='utf-8'))

    state_path = os.path.join(AUTO, 'dangdang-series-state.json')
    state = json.load(open(state_path, 'r', encoding='utf-8'))

    stories_path = os.path.join(H5, 'stories.json')
    stories = json.load(open(stories_path, 'r', encoding='utf-8'))

    # ---- target date (latest Saturday <= today, or override) ----
    if ep.get('dateOverride'):
        target = datetime.strptime(ep['dateOverride'], '%Y-%m-%d')
    else:
        target = latest_saturday_on_or_before(datetime.now())
    y, m, d = target.year, target.month, target.day
    date_str = f'{y}-{m:02d}-{d:02d}'
    weekday = WEEKDAYS[target.weekday()]

    episode = ep.get('episodeOverride') or state['episode']
    new_id = f'dangdang-ep{episode:02d}-zh'

    # ---- duplicate guard ----
    if any(s.get('id') == new_id for s in stories):
        print('SKIP: episode already exists ->', new_id)
        sys.exit(0)

    age_group, age_label = get_age_info(date_str)

    obj = {
        'id': new_id,
        'date': f'{y}年{m}月{d}日 · {weekday}',
        'dateShort': f'{m:02d}/{d:02d}',
        'title': ep['title'],
        'language': 'zh',
        'ageGroup': age_group,
        'ageLabel': age_label,
        'preview': ep['preview'],
        'moral': ep['moral'],
        'content': ep['content'],
        'series': 'dangdang',
        'seriesTitle': '黑猫当当历险记',
        'episode': episode,
    }
    stories.append(obj)
    json.dump(stories, open(stories_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('APPENDED', new_id, '-> stories.json (total', len(stories), ')')

    # ---- update EMBEDDED_STORIES (single line) ----
    idx_path = os.path.join(H5, 'index.html')
    text = open(idx_path, 'r', encoding='utf-8').read()
    marker = 'const EMBEDDED_STORIES = '
    lines = text.split('\n')
    replaced = False
    for i, line in enumerate(lines):
        if line.startswith(marker):
            lines[i] = marker + json.dumps(stories, ensure_ascii=False) + ';'
            replaced = True
            break
    if not replaced:
        print('ERROR: EMBEDDED_STORIES line not found')
        sys.exit(1)
    open(idx_path, 'w', encoding='utf-8').write('\n'.join(lines))
    print('UPDATED index.html EMBEDDED_STORIES')

    # ---- advance state ----
    state['episode'] = episode + 1
    state['lastGeneratedDate'] = date_str
    meta = ep.get('meta') or {}
    note = meta.get('continuityNote') or f'第{episode}集《{ep["title"]}》'
    state.setdefault('continuity', []).append(note)
    if meta.get('arc'):
        state['arc'] = {'current': meta['arc'], 'startedEpisode': episode, 'description': meta.get('arcDesc', '')}
    if meta.get('linkageNote'):
        state.setdefault('linkages', []).append(meta['linkageNote'])
    json.dump(state, open(state_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('UPDATED state -> next episode', state['episode'])

    # ---- regenerate collection ----
    for gen in ['generate-collection-html.js', 'generate-collection-md.js']:
        gp = os.path.join(AUTO, gen)
        if os.path.exists(gp):
            try:
                subprocess.run(['node', gp], cwd=AUTO, check=True)
                print('RAN', gen)
            except Exception as e:
                print('WARN: failed', gen, e)

    # ---- copy artifacts to deploy + backup ----
    coll_html = os.path.join(AUTO, 'bedtime-story-collection.html')
    if os.path.exists(coll_html):
        shutil.copyfile(coll_html, os.path.join(AUTO, 'collection-deploy', 'index.html'))
        shutil.copyfile(coll_html, os.path.join(BACK, 'bedtime-story-collection.html'))
    md_src = resolve_path(os.path.join(AUTO, '..', 'bedtime-story-collection.md'),
                          r'C:/Users/Administrator/WorkBuddy/Claw/bedtime-story-collection.md')
    if os.path.exists(md_src):
        shutil.copyfile(md_src, os.path.join(BACK, 'bedtime-story-collection.md'))

    print('DONE episode', episode, 'dated', date_str)


if __name__ == '__main__':
    main()
