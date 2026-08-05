#!/usr/bin/env python3
"""Generate missing bedtime story HTML pages from stories.json

支持「同一天多篇故事」：每个日期生成一页 bedtime-story-YYYY-MM-DD.html，
页内包含该日期的全部故事（中文、英文及其他手动创作），按语言分组、中文在前。
- 若某日期已有页面但故事数量较上次增加（例如手动新增了同天故事），会重新生成该页以包含全部故事。
- 用 .page_story_counts.json 记录每个日期的故事数，避免无谓重生成。
- 忽略黑猫当当系列（dangdang-epNN-zh）。
"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

MANIFEST = '.page_story_counts.json'


def load_stories(path='stories.json'):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def chinese_number(n):
    """Convert a number to Chinese numeral (for date display)"""
    cn = ['〇', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
    if n <= 10:
        return cn[n]
    if n < 20:
        return '十' + (cn[n % 10] if n % 10 else '')
    if n < 100:
        t = n // 10
        return cn[t] + '十' + (cn[n % 10] if n % 10 else '')
    return str(n)


def format_date_cn(date_str):
    """Format YYYY-MM-DD to Chinese date like '二〇二六年七月二十五日'"""
    parts = date_str.split('-')
    y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
    return f'{chinese_number(y)}年{chinese_number(m)}月{chinese_number(d)}日'


def get_weekday(date_str):
    """Get Chinese weekday from date string"""
    from datetime import datetime
    weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    return weekdays[dt.weekday()]


def esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def body_to_html(paras):
    out = ''
    if isinstance(paras, str):
        paras = [paras]
    for i, p in enumerate(paras):
        if p and p.strip():
            cls = 'first' if i == 0 else ''
            out += f'    <p class="{cls}">{esc(p.strip())}</p>\n\n'
    return out


def lang_label(lang):
    return '🇬🇧 EN' if lang == 'en' else '🇨🇳 中文'


def generate_html(date_str, story_list, output_dir='.'):
    """Generate a single-day page containing ALL stories of that date."""
    date_cn = format_date_cn(date_str)
    weekday = get_weekday(date_str)
    # 中文在前，英文在后；同日多篇保持数组原序
    ordered = sorted(story_list, key=lambda s: 0 if s.get('language', 'zh') != 'en' else 1)

    sections = ''
    for s in ordered:
        content = s.get('content') or []
        moral = s.get('moral', '') or ''
        title = s.get('title', '') or ''
        badge = lang_label(s.get('language', 'zh'))
        sci = '🔬 ' if s.get('series') == 'science' else ''
        body = body_to_html(content)
        moral_html = ''
        if moral:
            moral_html = f'''  <div class="moral">
    <div class="moral-title">✨ 故事小语</div>
    <div class="moral-text">
      {esc(moral).replace(chr(10), '<br>')}
    </div>
  </div>
'''
        sections += f'''  <div class="story-block">
    <div class="story-lang">{badge}</div>
    <h2>{sci}{esc(title)}</h2>
    <div class="story-body">
{body}  </div>
{moral_html}  </div>
'''

    multi = f'（共 {len(story_list)} 篇）' if len(story_list) > 1 else ''
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>每日儿童睡前故事{multi} — {date_cn}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); min-height: 100vh; display: flex; justify-content: center; align-items: flex-start; font-family: "PingFang SC", "Microsoft YaHei", "Noto Serif SC", serif; padding: 20px; }}
  .card {{ max-width: 680px; width: 100%; background: #fef9f0; border-radius: 24px; padding: 48px 40px; box-shadow: 0 20px 60px rgba(0,0,0,0.4); position: relative; overflow: hidden; margin-top: 20px; }}
  .card::before {{ content: ""; position: absolute; top: 0; left: 0; right: 0; height: 6px; background: linear-gradient(90deg, #a8d8ea, #ffb347, #ffcc33); }}
  .stars {{ position: absolute; top: 20px; right: 30px; font-size: 24px; opacity: 0.4; }}
  .moon {{ position: absolute; top: 16px; right: 70px; font-size: 28px; opacity: 0.3; }}
  .date {{ font-size: 13px; color: #b0a08a; text-align: center; margin-bottom: 8px; letter-spacing: 2px; }}
  h1 {{ text-align: center; color: #5c4d3c; font-size: 26px; font-weight: 600; margin-bottom: 6px; letter-spacing: 2px; }}
  .divider {{ text-align: center; color: #d4c5a9; font-size: 14px; margin-bottom: 28px; letter-spacing: 4px; }}
  .story-block {{ margin-bottom: 32px; padding-bottom: 24px; border-bottom: 1px dashed #e8dcc4; }}
  .story-block:last-child {{ border-bottom: none; margin-bottom: 0; padding-bottom: 0; }}
  .story-lang {{ text-align: center; font-size: 12px; color: #b0a08a; margin-bottom: 4px; }}
  .story-block h2 {{ text-align: center; color: #5c4d3c; font-size: 22px; font-weight: 600; margin-bottom: 14px; letter-spacing: 1px; }}
  .story-body {{ font-size: 18px; line-height: 2; color: #5a4535; text-align: justify; text-indent: 2em; }}
  .story-body p {{ margin-bottom: 16px; }}
  .story-body .first::first-letter {{ font-size: 32px; font-weight: bold; color: #e8963b; }}
  .moral {{ margin-top: 24px; padding: 18px 22px; background: linear-gradient(135deg, #fff8e7, #fef3d6); border-radius: 16px; border-left: 4px solid #f0b850; }}
  .moral-title {{ font-size: 15px; color: #c8923a; font-weight: 600; margin-bottom: 8px; letter-spacing: 2px; }}
  .moral-text {{ font-size: 16px; line-height: 1.8; color: #7a6550; }}
  .footer {{ text-align: center; margin-top: 32px; font-size: 13px; color: #c4b49a; }}
  .footer span {{ margin: 0 6px; }}
</style>
</head>
<body>
<div class="card">
  <div class="stars">✦ ✦ ✦</div>
  <div class="moon">🌙</div>
  <div class="date">{date_cn} · {weekday}{multi}</div>
  <h1>🌛 睡前故事</h1>
  <div class="divider">— ✿ —</div>
{sections}
  <div class="footer">
    <span>🌙</span> 晚安，好梦 <span>🌙</span>
  </div>
</div>
</body>
</html>
'''
    filename = f'bedtime-story-{date_str}.html'
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  ✅ {filename} ({len(story_list)} 篇)')
    return filepath


def load_manifest(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def save_manifest(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    stories = load_stories()

    # Group by date, ignoring the 黑猫当当 series
    by_date = {}
    for s in stories:
        if s.get('series') == 'dangdang':
            continue
        m = re.match(r'(\d{4}-\d{2}-\d{2})', s.get('id', ''))
        if not m:
            continue
        by_date.setdefault(m.group(1), []).append(s)

    existing = set()
    for f in os.listdir('.'):
        m = re.match(r'bedtime-story-(\d{4}-\d{2}-\d{2})\.html', f)
        if m:
            existing.add(m.group(1))

    manifest = load_manifest(MANIFEST)

    todo = []
    for date_str, slist in by_date.items():
        cnt = len(slist)
        if date_str not in existing:
            todo.append(date_str)          # 缺页
        elif manifest.get(date_str) != cnt:
            todo.append(date_str)          # 故事数变化（如手动新增同天故事）→ 重生成
    todo.sort()

    print(f'已有页面: {len(existing)} 个')
    print(f'故事数据: {len(by_date)} 天')
    print(f'需生成/更新: {len(todo)} 个: {todo}')

    for date_str in todo:
        generate_html(date_str, by_date[date_str])
        manifest[date_str] = len(by_date[date_str])

    save_manifest(MANIFEST, manifest)
    print(f'\n✅ 共处理 {len(todo)} 个日期页面')


if __name__ == '__main__':
    main()
