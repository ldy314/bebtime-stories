import json

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

marker = 'const EMBEDDED_STORIES = ['
idx = content.find(marker)
s = idx + len(marker)

decoder = json.JSONDecoder()
obj, end = decoder.raw_decode(content[s-1:])  # s-1 to include the opening [
print(f'Total stories: {len(obj)}')
print(f'Daily: {len([x for x in obj if not x.get("series")])}')
print(f'Series: {len([x for x in obj if x.get("series")])}')
print(f'Science: {len([x for x in obj if x.get("category") == "science"])}')
print(f'First: {obj[0]["id"]} - {obj[0]["title"]}')
print(f'Last: {obj[-1]["id"]} - {obj[-1]["title"]}')
