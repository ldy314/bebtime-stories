#!/usr/bin/env python3
"""Generate missing bedtime story HTML pages from stories.json"""

import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

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
    # Year: each digit
    year_cn = ''.join(chinese_number(int(c)) for c in str(y))
    month_cn = chinese_number(m)
    day_cn = chinese_number(d)
    return f'{year_cn}年{month_cn}月{day_cn}日'

def get_weekday(date_str):
    """Get Chinese weekday from date string"""
    from datetime import datetime
    weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    return weekdays[dt.weekday()]

def generate_html(date_str, story, output_dir='.'):
    """Generate a bedtime story HTML page"""
    title = story['title']
    content_paragraphs = story['content']
    moral = story.get('moral', '')
    
    date_cn = format_date_cn(date_str)
    weekday = get_weekday(date_str)
    
    # Build content HTML
    content_html = ''
    for i, p in enumerate(content_paragraphs):
        if p.strip():
            cls = 'first' if i == 0 else ''
            content_html += f'    <p class="{cls}">{p.strip()}</p>\n\n'
    
    # Build moral HTML
    moral_html = ''
    if moral:
        # Split moral by \n if multiline
        moral_lines = moral.strip().split('\n')
        moral_text = '<br>\n'.join(moral_lines)
        moral_html = f'''  <div class="moral">
    <div class="moral-title">✨ 故事小语</div>
    <div class="moral-text">
      {moral_text}
    </div>
  </div>
'''
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>每日儿童睡前故事 — {date_cn}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    min-height: 100vh;
    display: flex; justify-content: center; align-items: center;
    font-family: "PingFang SC", "Microsoft YaHei", "Noto Serif SC", serif;
    padding: 20px;
  }}
  .card {{
    max-width: 680px; width: 100%;
    background: #fef9f0;
    border-radius: 24px;
    padding: 48px 40px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
    position: relative;
    overflow: hidden;
  }}
  .card::before {{
    content: ""; position: absolute; top: 0; left: 0; right: 0; height: 6px;
    background: linear-gradient(90deg, #a8d8ea, #ffb347, #ffcc33);
  }}
  .stars {{
    position: absolute; top: 20px; right: 30px;
    font-size: 24px; opacity: 0.4;
  }}
  .moon {{
    position: absolute; top: 16px; right: 70px;
    font-size: 28px; opacity: 0.3;
  }}
  .date {{
    font-size: 13px; color: #b0a08a; text-align: center; margin-bottom: 8px;
    letter-spacing: 2px;
  }}
  h1 {{
    text-align: center; color: #5c4d3c;
    font-size: 26px; font-weight: 600;
    margin-bottom: 6px; letter-spacing: 2px;
  }}
  .divider {{
    text-align: center; color: #d4c5a9; font-size: 14px;
    margin-bottom: 28px; letter-spacing: 4px;
  }}
  .story {{
    font-size: 18px; line-height: 2; color: #5a4535;
    text-align: justify; text-indent: 2em;
  }}
  .story p {{ margin-bottom: 16px; }}
  .story .first::first-letter {{
    font-size: 32px; font-weight: bold; color: #e8963b;
  }}
  .moral {{
    margin-top: 36px; padding: 20px 24px;
    background: linear-gradient(135deg, #fff8e7, #fef3d6);
    border-radius: 16px; border-left: 4px solid #f0b850;
  }}
  .moral-title {{
    font-size: 15px; color: #c8923a; font-weight: 600;
    margin-bottom: 8px; letter-spacing: 2px;
  }}
  .moral-text {{
    font-size: 16px; line-height: 1.8; color: #7a6550;
  }}
  .footer {{
    text-align: center; margin-top: 32px;
    font-size: 13px; color: #c4b49a;
  }}
  .footer span {{ margin: 0 6px; }}
</style>
</head>
<body>
<div class="card">
  <div class="stars">✦ ✦ ✦</div>
  <div class="moon">🌙</div>
  <div class="date">{date_cn} · {weekday}</div>
  <h1>🌛 睡前故事</h1>
  <div class="divider">— ✿ —</div>

  <div class="story">
{content_html}  </div>

{moral_html}
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
    print(f'  ✅ {filename}')
    return filepath

def main():
    stories = load_stories()
    
    # Group by date, get Chinese stories
    cn_stories = {}
    for s in stories:
        if s['language'] == 'zh':
            date_id = s['id']  # e.g., '2026-07-28-cn'
            # Extract YYYY-MM-DD from the start of the ID
            m = re.match(r'(\d{4}-\d{2}-\d{2})', date_id)
            if m:
                date_str = m.group(1)
                # Only keep the first story for each date
                if date_str not in cn_stories:
                    cn_stories[date_str] = s
    
    # Find existing HTML files
    existing = set()
    for f in os.listdir('.'):
        m = re.match(r'bedtime-story-(\d{4}-\d{2}-\d{2})\.html', f)
        if m:
            existing.add(m.group(1))
    
    print(f'已有页面: {len(existing)} 个')
    print(f'故事数据: {len(cn_stories)} 天')
    
    missing_dates = sorted(set(cn_stories.keys()) - existing)
    print(f'缺失页面: {len(missing_dates)} 个: {missing_dates}')
    
    for date_str in missing_dates:
        generate_html(date_str, cn_stories[date_str])
    
    print(f'\n✅ 共生成 {len(missing_dates)} 个缺失页面')

if __name__ == '__main__':
    main()
