import json

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

marker = 'const EMBEDDED_STORIES = ['
idx = content.find(marker)
s = idx + len(marker)

# Find end of array
depth = 1
in_string = False
escape_next = False
end = -1
for i in range(s, len(content)):
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
            end = i
            break

arr_str = content[s:end+1]
print(f'Array: chars {s} to {end} (len={end-s+1})')

# Try to find where the JSON breaks
# Start from the beginning and parse incrementally
decoder = json.JSONDecoder()
try:
    obj, idx = decoder.raw_decode(arr_str)
    print(f'Parsed OK: {len(obj)} items, ended at index {idx}')
except json.JSONDecodeError as e:
    print(f'Error: {e}')
    print(f'Position in array: {e.pos}')
    print(f'Context: {repr(arr_str[e.pos-40:e.pos+40])}')
