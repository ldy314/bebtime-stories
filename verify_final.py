import json

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

marker = 'const EMBEDDED_STORIES = ['
idx = html.index(marker)
s = idx + len(marker)

# Parse the array
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

arr_str = html[s:end+1]
arr = json.loads(arr_str)
print(f'Total stories: {len(arr)}')
print(f'Daily: {len([x for x in arr if not x.get("series")])}')
print(f'Series: {len([x for x in arr if x.get("series")])}')
print(f'Science: {len([x for x in arr if x.get("category") == "science"])}')
print(f'First: {arr[0]["id"]} - {arr[0]["title"]}')
print(f'Last: {arr[-1]["id"]} - {arr[-1]["title"]}')
