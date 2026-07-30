#!/usr/bin/env python3
"""Sync stories data across root and github-pages directories."""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # project root (scripts/ -> parent)

def p(*parts):
    return os.path.join(ROOT, *parts)

def update_index_html(index_path, stories):
    """Update EMBEDDED_STORIES in index.html"""
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    json_str = json.dumps(stories, ensure_ascii=False)
    new_line = f'const EMBEDDED_STORIES = {json_str};'
    
    # Replace the EMBEDDED_STORIES line
    new_content = re.sub(
        r'const EMBEDDED_STORIES = .*?;',
        new_line,
        content,
        count=1,
        flags=re.DOTALL
    )
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f'  ✅ {index_path} → {len(stories)} 条故事')

def main():
    # 1. Load stories from root (source of truth)
    with open(p('stories.json'), 'r', encoding='utf-8') as f:
        root_stories = json.load(f)
    
    print(f'根目录 stories.json: {len(root_stories)} 条')
    
    # 1.5 Consistency guard: warn (non-fatal) if github-pages already diverges
    gp_path = p('github-pages', 'stories.json')
    if os.path.exists(gp_path):
        try:
            gp_stories = json.load(open(gp_path, 'r', encoding='utf-8'))
            root_ids = {s.get('id') for s in root_stories}
            gp_ids = {s.get('id') for s in gp_stories}
            if root_ids != gp_ids:
                print(f'  ⚠️ 警告: github-pages/stories.json 与根目录不一致 '
                      f'(根 {len(root_ids)} 篇 / pages {len(gp_ids)} 篇)，将以根目录为准进行同步')
        except Exception as ex:
            print(f'  ⚠️ 无法读取 github-pages/stories.json 进行对比: {ex}')
    
    # 2. Sync stories.json to github-pages/
    with open(p('github-pages', 'stories.json'), 'w', encoding='utf-8') as f:
        json.dump(root_stories, f, ensure_ascii=False, indent=2)
    print(f'  ✅ github-pages/stories.json → {len(root_stories)} 条')
    
    # 3. Update index.html in both directories
    update_index_html(p('index.html'), root_stories)
    update_index_html(p('github-pages', 'index.html'), root_stories)
    
    print(f'\n🎉 同步完成！共 {len(root_stories)} 条故事')

if __name__ == '__main__':
    main()
