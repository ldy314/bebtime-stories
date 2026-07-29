#!/usr/bin/env python3
"""Clean up stories.json - remove test data, fix date fields."""
import json
import re
from datetime import datetime, timedelta

def fix_date_field(story):
    """Fix dateShort and date based on the ID date"""
    # Extract YYYY-MM-DD from id
    m = re.match(r'(\d{4}-\d{2}-\d{2})', story['id'])
    if not m:
        return False
    
    date_str = m.group(1)
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    
    # Fix dateShort
    expected_short = f"{dt.month:02d}/{dt.day:02d}"
    story['dateShort'] = expected_short
    
    # Fix date
    weekdays_cn = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    weekday_cn = weekdays_cn[dt.weekday()]
    story['date'] = f"{dt.year}年{dt.month}月{dt.day}日 · {weekday_cn}"
    
    return True

# Load stories
with open('stories.json', 'r', encoding='utf-8') as f:
    stories = json.load(f)

print(f'原始条数: {len(stories)}')

# Keep only standard story IDs: YYYY-MM-DD-cn or YYYY-MM-DD-en
clean = []
removed = []
seen_ids = set()

for s in stories:
    sid = s['id']
    # Only keep standard format
    if re.match(r'\d{4}-\d{2}-\d{2}-(cn|en)$', sid):
        # Deduplicate (keep first occurrence of each id)
        if sid not in seen_ids:
            seen_ids.add(sid)
            fix_date_field(s)
            clean.append(s)
        else:
            removed.append(f'{sid} (重复)')
    else:
        removed.append(f'{sid} (非标准格式)')

print(f'清理后条数: {len(clean)}')
print(f'移除的条目 ({len(removed)}):')
for r in removed:
    print(f'  - {r}')

# Write cleaned stories.json
with open('stories.json', 'w', encoding='utf-8') as f:
    json.dump(clean, f, ensure_ascii=False, indent=2)

print(f'\n✅ stories.json 已清理并写入')

# Also write to github-pages
with open('github-pages/stories.json', 'w', encoding='utf-8') as f:
    json.dump(clean, f, ensure_ascii=False, indent=2)
print(f'✅ github-pages/stories.json 已同步')
