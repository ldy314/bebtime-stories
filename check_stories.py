import json

# Verify stories.json is OK
with open('stories.json', 'r', encoding='utf-8') as f:
    content = f.read()

# Try parsing
try:
    arr = json.loads(content)
    print(f'Parsed: {len(arr)} stories')
    for i, s in enumerate(arr):
        print(f'{i}: {s.get("id")} - {s.get("title", "")[:30]}')
except json.JSONDecodeError as e:
    print(f'Error: {e}')
    print(f'At pos {e.pos}: {repr(content[e.pos-30:e.pos+30])}')
