#!/usr/bin/env python3
"""Replace EMBEDDED_STORIES in index.html with all stories from stories.json"""
import json

# Read stories.json
with open('stories.json', 'r', encoding='utf-8') as f:
    stories = json.load(f)
print(f'stories.json: {len(stories)} stories')

# Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find const EMBEDDED_STORIES = [
marker = 'const EMBEDDED_STORIES = ['
start_idx = html.index(marker)
arr_start = start_idx + len(marker)

# Find the matching closing ] using depth tracking
depth = 1  # we're inside the outer [
in_string = False
escape_next = False
end_idx = -1

for i in range(arr_start, len(html)):
    ch = html[i]
    if escape_next:
        escape_next = False
        continue
    if ch == '\\' and in_string:
        escape_next = True
        continue
    if ch == '"':
        in_string = not in_string
        continue
    if in_string:
        continue
    if ch == '[':
        depth += 1
    elif ch == ']':
        depth -= 1
        if depth == 0:
            end_idx = i
            break

if end_idx == -1:
    print('ERROR: End of array not found')
    exit(1)

print(f'Array range: {start_idx} -> {end_idx}')
print(f'After end: {repr(html[end_idx:end_idx+10])}')

# Generate new array
new_arr = json.dumps(stories, ensure_ascii=False, indent=2)

# Replace
new_code = f'const EMBEDDED_STORIES = {new_arr};\n'
html = html[:start_idx] + new_code + html[end_idx + 1:]

# Write
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Done! File size: {len(html)} bytes')

# Verify
check_start = html.index(marker) + len(marker)
cd = 1
cis = False
ces = False
cei = -1
for i in range(check_start, len(html)):
    c = html[i]
    if ces:
        ces = False
        continue
    if c == '\\' and cis:
        ces = True
        continue
    if c == '"':
        cis = not cis
        continue
    if cis:
        continue
    if c == '[':
        cd += 1
    elif c == ']':
        cd -= 1
        if cd == 0:
            cei = i
            break

import json as j2
arr = j2.loads(html[check_start:cei + 1])
print(f'Verified: {len(arr)} stories')
print(f'Daily: {len([x for x in arr if not x.get("series")])}')
print(f'Series: {len([x for x in arr if x.get("series")])}')
