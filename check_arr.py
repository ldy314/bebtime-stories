import json

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

marker = 'const EMBEDDED_STORIES = ['
idx = html.index(marker)
s = idx + len(marker)

# Parse the array manually
depth = 1
in_string = False
escape = False
end = -1
for i in range(s, len(html)):
    c = html[i]
    if escape:
        escape = False
        continue
    if c == '\\' and in_string:
        escape = True
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
            end = i
            break

print(f'Array ends at char {end}')
print(f'Context around end: {repr(html[end-10:end+20])}')

# Try parsing just up to a reasonable point
arr_str = html[s:end+1]
print(f'Array string length: {len(arr_str)}')

# Try parsing
try:
    arr = json.loads(arr_str)
    print(f'SUCCESS: {len(arr)} stories')
except json.JSONDecodeError as e:
    print(f'Error: {e}')
    # Show context around error
    pos = e.pos
    print(f'At position {pos}: {repr(arr_str[pos-30:pos+30])}')
