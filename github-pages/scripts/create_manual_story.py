#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
create_manual_story.py — 手动创建一篇睡前故事并安全入库/发布

用途：在「允许同一天多篇故事」的规则下，手动追加一篇故事（如自动化已生成当天故事，
也可以再手动加一篇；反之亦然）。脚本会自动：
  1. 先从云端同步到本地 H5（避免覆盖云端已有的新故事）；
  2. 计算一个不与现有 id 冲突的唯一 id（同天同语言自动加 -2 / -3 …）；
  3. 写入 H5 的 stories.json 与 index.html 内嵌 EMBEDDED_STORIES；
  4. 重新生成合集 MD / HTML；
  5. 推回云端（git push）；
  6. 同步 D 盘备份并刷新单日阅读页。

用法示例：
  python scripts/create_manual_story.py --date 2026-08-05 --lang zh \
      --title "小星星的晚安歌" \
      --content "第一段。\n\n第二段。" \
      --moral "爱一直都在。" \
      --preview "小星星眨着眼睛。"

  # 从 JSON 文件读取（content 可为字符串或数组）：
  python scripts/create_manual_story.py --json story.json

  # 仅计算 id、打印将要写入的内容，不落盘：
  python scripts/create_manual_story.py --date 2026-08-05 --lang zh --title x --content "x" --dry-run

可选参数：
  --date YYYY-MM-DD        故事日期（必填，除非用 --json）
  --lang zh|en             语言（默认 zh）
  --title                  标题
  --content                正文，段落用空行(\\n\\n)分隔
  --content-file path.txt  从文件读取正文
  --moral                  寓意
  --preview                预览（默认取正文前两句）
  --category regular|science  默认 regular
  --json path.json         从一个 JSON 读取全部字段（覆盖上面的散参）
  --no-sync                跳过最初的云端同步（离线/测试时使用，谨慎）
  --no-push                不推回云端（仅本地 + 备份）
  --no-backup              不同步 D 盘备份
  --dry-run                只打印将写入的内容与 id，不落盘、不推送
"""
import json
import os
import re
import shutil
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

# ===== 路径 =====
H5 = 'C:/Users/Administrator/WorkBuddy/Claw/bedtime-story-app'
REPO = 'C:/Users/Administrator/WorkBuddy/Claw/github-bedtime-stories'
AUTO = 'C:/Users/Administrator/WorkBuddy/automation-2026-07-16-11-56-46'
DEST = 'D:/code test/睡前故事'
COLLECTION_MD = 'C:/Users/Administrator/WorkBuddy/Claw/bedtime-story-collection.md'

WEEKDAYS = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
BIRTHDAY = (2026, 9, 22)


def find_node():
    cand = [
        shutil.which('node'),
        r'C:\Users\Administrator\.workbuddy\binaries\node\versions\22.22.2\node.exe',
        r'D:\node\node.exe',
    ]
    for c in cand:
        if c and os.path.exists(c):
            return c
    return 'node'


NODE = find_node()


def run_node(script, cwd=None):
    cmd = [NODE, script]
    print(f'  $ node {os.path.basename(script)}')
    subprocess.run(cmd, cwd=cwd, check=True)


# ===== 日期/年龄辅助（与 prompt-builder.js 保持一致）=====
def format_date_cn(date_str):
    y, m, d = (int(x) for x in date_str.split('-'))
    return f'{y}年{m}月{d}日'


def format_date_short(date_str):
    _, m, d = date_str.split('-')
    return f'{m}/{d}'


def get_chinese_weekday(date_str):
    import datetime
    y, m, d = (int(x) for x in date_str.split('-'))
    # isoweekday: 周一=1..周日=7；WEEKDAYS[0]=星期日 → %7 映射一致
    return WEEKDAYS[datetime.date(y, m, d).isoweekday() % 7]


def get_age_info(date_str):
    from datetime import date
    y, m, d = (int(x) for x in date_str.split('-'))
    dd = date(y, m, d)
    if dd < date(*BIRTHDAY):
        return ('prenatal', '胎教期', 'Prenatal')
    diff = (dd - date(*BIRTHDAY)).days
    yrs = diff / 365.25
    if yrs < 1:
        return ('0-1', '0-1岁', '0-1 yr')
    if yrs < 3:
        return ('1-3', '1-3岁', '1-3 yr')
    if yrs < 6:
        return ('3-6', '3-6岁', '3-6 yr')
    return ('6+', '6岁以上', '6+ yr')


def sanitize(text):
    if not isinstance(text, str):
        return text
    return (text
            .replace('“', '「').replace('”', '」')
            .replace('‘', "'").replace('’', "'"))


def split_paras(text):
    text = (text or '').strip()
    if not text:
        return []
    parts = re.split(r'\n\s*\n', text)
    paras = [p.strip() for p in parts if p.strip()]
    if len(paras) <= 1 and '\n' in text:
        paras = [p.strip() for p in text.split('\n') if p.strip()]
    return paras


def first_sentences(text, n=2):
    sents = re.split(r'(?<=[。！？!?])', text.strip())
    sents = [s.strip() for s in sents if s.strip()]
    return ''.join(sents[:n])


def compute_unique_id(stories, date_str, lang, category):
    lang_suffix = 'cn' if lang == 'zh' else 'en'
    if category == 'science':
        base = f'{date_str}-science-{lang_suffix}'
    else:
        base = f'{date_str}-{lang_suffix}'
    if not any(s.get('id') == base for s in stories):
        return base
    n = 2
    while any(s.get('id') == f'{base}-{n}' for s in stories):
        n += 1
    return f'{base}-{n}'


def build_story(date_str, lang, title, content, moral, preview, category):
    group, label_cn, label_en = get_age_info(date_str)
    story = {
        'id': None,  # 由调用方填充
        'date': f'{format_date_cn(date_str)} · {get_chinese_weekday(date_str)}',
        'dateShort': format_date_short(date_str),
        'title': sanitize(title),
        'language': lang,
        'ageGroup': group,
        'ageLabel': label_cn if lang == 'zh' else label_en,
        'preview': sanitize(preview or ''),
        'moral': sanitize(moral or ''),
        'content': [sanitize(p) for p in content if p and p.strip()],
    }
    if category == 'science':
        story['series'] = 'science'
        story['seriesTitle'] = '科学故事'
    return story


def update_embedded_stories(index_path, stories):
    html = open(index_path, 'r', encoding='utf-8').read()
    lines = html.split('\n')
    idx = next((i for i, ln in enumerate(lines) if ln.strip().startswith('const EMBEDDED_STORIES = ')), None)
    if idx is None:
        raise RuntimeError('在 index.html 中找不到 EMBEDDED_STORIES 行')
    lines[idx] = 'const EMBEDDED_STORIES = ' + json.dumps(stories, ensure_ascii=False, separators=(',', ':')) + ';'
    open(index_path, 'w', encoding='utf-8').write('\n'.join(lines))
    print(f'  已更新 EMBEDDED_STORIES（共 {len(stories)} 篇）')


def load_args():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--date')
    ap.add_argument('--lang', default='zh')
    ap.add_argument('--title')
    ap.add_argument('--content')
    ap.add_argument('--content-file')
    ap.add_argument('--moral', default='')
    ap.add_argument('--preview')
    ap.add_argument('--category', default='regular')
    ap.add_argument('--json')
    ap.add_argument('--no-sync', action='store_true')
    ap.add_argument('--no-push', action='store_true')
    ap.add_argument('--no-backup', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    return ap.parse_args()


def main():
    args = load_args()

    # 收集字段
    if args.json:
        data = json.load(open(args.json, 'r', encoding='utf-8'))
        date_str = data['date']
        lang = data.get('lang', data.get('language', 'zh'))
        title = data['title']
        content = data.get('content', '')
        if isinstance(content, str):
            content = split_paras(content)
        moral = data.get('moral', '')
        preview = data.get('preview', '')
        category = data.get('category', 'regular')
    else:
        date_str = args.date
        lang = args.lang
        title = args.title
        if args.content_file:
            content = split_paras(open(args.content_file, 'r', encoding='utf-8').read())
        else:
            content = split_paras(args.content or '')
        moral = args.moral
        preview = args.preview or ''
        category = args.category

    if not date_str or not title:
        print('错误：必须提供 --date 与 --title（或使用 --json 提供完整字段）')
        sys.exit(2)
    if not content:
        print('错误：正文为空，请用 --content 或 --content-file 提供')
        sys.exit(2)
    if lang not in ('zh', 'en'):
        print('错误：--lang 只能是 zh 或 en')
        sys.exit(2)
    if category not in ('regular', 'science'):
        print('错误：--category 只能是 regular 或 science')
        sys.exit(2)

    # 1. 云端同步
    if not args.no_sync:
        print('[1/6] 从云端同步到本地 H5 ...')
        try:
            run_node(os.path.join(AUTO, 'sync-from-cloud.js'), cwd=AUTO)
        except Exception as e:
            print(f'  [警告] 云端同步失败，将基于当前 H5 继续：{e}')
    else:
        print('[1/6] 跳过云端同步（--no-sync）')

    h5_json = os.path.join(H5, 'stories.json')
    stories = json.load(open(h5_json, 'r', encoding='utf-8'))

    # 2. 计算唯一 id
    sid = compute_unique_id(stories, date_str, lang, category)
    print(f'[2/6] 目标 id = {sid}')

    story = build_story(date_str, lang, title, content, moral, preview, category)
    story['id'] = sid
    if not story['preview']:
        story['preview'] = first_sentences(''.join(story['content']))

    print(f'      标题：{story["title"]}  | 段落数：{len(story["content"])}  | 年龄段：{story["ageLabel"]}')

    if args.dry_run:
        print('\n[dry-run] 以下为将要写入的对象（未落盘）：')
        print(json.dumps(story, ensure_ascii=False, indent=2, ensure_ascii=False))
        print(f'[dry-run] 当前 H5 共 {len(stories)} 篇；写入后将为 {len(stories) + 1} 篇。')
        return

    # 3. 写入 H5 stories.json + index.html
    print('[3/6] 写入 H5 stories.json 与 index.html ...')
    stories.append(story)
    json.dump(stories, open(h5_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    open(h5_json, 'a', encoding='utf-8').write('\n')
    update_embedded_stories(os.path.join(H5, 'index.html'), stories)

    # 4. 重新生成合集
    print('[4/6] 重新生成合集 MD / HTML ...')
    run_node(os.path.join(AUTO, 'generate-collection-md.js'), cwd=AUTO)
    run_node(os.path.join(AUTO, 'generate-collection-html.js'), cwd=AUTO)
    try:
        shutil.copyfile(os.path.join(AUTO, 'bedtime-story-collection.html'),
                        os.path.join(AUTO, 'collection-deploy', 'index.html'))
    except Exception:
        pass

    # 5. 推回云端
    if not args.no_push:
        print('[5/6] 推回云端 ...')
        run_node(os.path.join(AUTO, 'push-to-cloud.js'), cwd=AUTO)
    else:
        print('[5/6] 跳过推送（--no-push）')

    # 6. 同步 D 盘备份
    if not args.no_backup:
        print('[6/6] 同步 D 盘备份并刷新单日页 ...')
        os.makedirs(DEST, exist_ok=True)
        shutil.copyfile(os.path.join(H5, 'index.html'), os.path.join(DEST, 'index.html'))
        shutil.copyfile(os.path.join(H5, 'stories.json'), os.path.join(DEST, 'stories.json'))
        shutil.copyfile(COLLECTION_MD, os.path.join(DEST, 'bedtime-story-collection.md'))
        shutil.copyfile(os.path.join(AUTO, 'bedtime-story-collection.html'),
                        os.path.join(DEST, 'bedtime-story-collection.html'))
        # github-pages 镜像
        gp = os.path.join(DEST, 'github-pages')
        if os.path.isdir(gp):
            try:
                shutil.copyfile(os.path.join(REPO, 'index.html'), os.path.join(gp, 'index.html'))
                shutil.copyfile(os.path.join(REPO, 'stories.json'), os.path.join(gp, 'stories.json'))
                shutil.copyfile(os.path.join(REPO, 'collection.html'), os.path.join(gp, 'collection.html'))
            except Exception as e:
                print(f'  [警告] github-pages 镜像同步失败：{e}')
        # 刷新单日页
        try:
            subprocess.run([sys.executable, os.path.join(DEST, 'scripts', 'generate_missing_pages.py')],
                           cwd=DEST, check=True)
        except Exception as e:
            print(f'  [警告] 单日页生成失败：{e}')
    else:
        print('[6/6] 跳过 D 盘备份（--no-backup）')

    print(f'\n✅ 手动故事已创建：{sid}（{story["title"]}）')


if __name__ == '__main__':
    main()
