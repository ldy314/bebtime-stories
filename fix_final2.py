#!/usr/bin/env python3
"""Fix EMBEDDED_STORIES by parsing file structure directly"""
import json

# Read stories.json
with open('stories.json', 'r', encoding='utf-8') as f:
    stories = json.load(f)
print(f'stories.json: {len(stories)} stories')

# Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find line numbers
start_line = -1
end_line = -1
for i, line in enumerate(lines):
    if 'const EMBEDDED_STORIES' in line and start_line == -1:
        start_line = i
    if start_line >= 0 and end_line == -1:
        # Check if this line has ]; that closes the array
        # But we need to handle multiline - the array spans many lines
        # Count open [ and close ] from start_line onward
        pass

# Better approach: join all text and find positions
content = ''.join(lines)

# Find const EMBEDDED_STORIES
marker = 'const EMBEDDED_STORIES'
start_idx = content.find(marker)
if start_idx == -1:
    print('ERROR: marker not found')
    exit(1)

# Find the closing ]; after the marker
# We need to find the ]; that's followed by either \n\n or \n;// or similar
search_from = start_idx + len(marker)
# Find ]; that's not inside a string
in_string = False
escape_next = False
depth = 0
end_idx = -1

for i in range(search_from, len(content)):
    c = content[i]
    if escape_next:
        escape_next = False
        continue
    if c == '\\' and in_string:
        escape_next = True
        continue
    if c == '"':
        in_string = not in_string
        continue
    if in_string:
        continue
    if c == '[':
        depth += 1
    elif c == ']':
        depth -= 1
        if depth == 0:
            # Found closing ], now include ;
            end_idx = i + 1
            if end_idx < len(content) and content[end_idx] == ';':
                end_idx += 1
            break

if end_idx == -1:
    print('ERROR: end not found')
    exit(1)

print(f'Start: {start_idx}, End: {end_idx}')
print(f'Before: {repr(content[start_idx:start_idx+40])}')
print(f'After: {repr(content[end_idx:end_idx+20])}')

# Generate new array
new_arr = json.dumps(stories, ensure_ascii=False, indent=2)
new_declaration = f'const EMBEDDED_STORIES = {new_arr};\n'

# Replace
new_content = content[:start_idx] + new_declaration + content[end_idx:]

# Write
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f'File size: {len(new_content)} bytes')

# Verify
v_marker = 'const EMBEDDED_STORIES = ['
v_start = new_content.find(v_marker) + len(v_marker)
vd = 1
vis = False
ves = False
vei = -1
for i in range(v_start, len(new_content)):
    c = new_content[i]
    if ves:
        ves = False
        continue
    if c == '\\' and vis:
        ves = True
        continue
    if c == '"':
        vis = not vis
        continue
    if vis:
        continue
    if c == '[':
        vd += 1
    elif c == ']':
        vd -= 1
        if vd == 0:
            vei = i
            break

varr = json.loads(new_content[v_start:vei+1])
print(f'Verified: {len(varr)} stories')
print(f'Daily: {len([x for x in varr if not x.get("series")])}')
print(f'Series: {len([x for x in varr if x.get("series")])}')
print(f'Science: {len([x for x in varr if x.get("category") == "science"])}')
