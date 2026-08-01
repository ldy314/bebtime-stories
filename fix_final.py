#!/usr/bin/env python3
"""Final fix: replace EMBEDDED_STORIES in index.html"""
import json

# Read stories
with open('stories.json', 'r', encoding='utf-8') as f:
    stories = json.load(f)
print(f'stories.json: {len(stories)} stories')

# Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# The file has this structure:
#   ...html...</style>
#   <body>
#   ...html...
#   <script>
#   ...js...
#   const EMBEDDED_STORIES = [...];
#   ...js...
#   </script>
#   </body>
#   </html>

# Find the start of EMBEDDED_STORIES declaration
marker_start = 'const EMBEDDED_STORIES = ['
idx_start = content.find(marker_start)
if idx_start == -1:
    # Try with [[
    marker_start = 'const EMBEDDED_STORIES = [['
    idx_start = content.find(marker_start)
    if idx_start == -1:
        print('ERROR: EMBEDDED_STORIES not found')
        exit(1)

# Find end of array using character-by-character parsing
arr_content_start = idx_start + len(marker_start) - 1  # position of first [
depth = 0
in_string = False
escape_next = False
arr_end = -1

for i in range(idx_start + len(marker_start) - 1, len(content)):
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
            arr_end = i
            break

if arr_end == -1:
    print('ERROR: Array end not found')
    exit(1)

# The full declaration ends at ] + ;
decl_end = arr_end
while decl_end < len(content) and content[decl_end] in ']; \n\r':
    decl_end += 1

# But we want to keep ]; as the end
decl_end = arr_end + 2  # include ];

print(f'Array: {idx_start} -> {arr_end}')
print(f'Declaration end: {decl_end}')
print(f'Context after: {repr(content[decl_end:decl_end+10])}')

# Generate new array
new_arr = json.dumps(stories, ensure_ascii=False, indent=2)
new_declaration = f'const EMBEDDED_STORIES = {new_arr};'

# Build new content
new_content = content[:idx_start] + new_declaration + content[decl_end:]

# Write
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f'Done! File size: {len(new_content)} bytes')

# Verify by parsing
v_start = new_content.find('const EMBEDDED_STORIES = [') + 26
vd = 0
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
