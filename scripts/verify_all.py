#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify all files are valid and consistent"""
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errors = 0

def fail(msg):
    global errors
    errors += 1
    print(f"  ❌ {msg}")

def ok(msg):
    print(f"  ✅ {msg}")

# 1. stories.json
print("\n--- stories.json ---")
sp = os.path.join(BASE, "stories.json")
if not os.path.exists(sp):
    fail("stories.json 不存在")
else:
    with open(sp, 'r', encoding='utf-8') as f:
        stories = json.load(f)
    ok(f"格式正确: {len(stories)} 个故事")
    ids = [s['id'] for s in stories]
    dupes = [x for x in set(ids) if ids.count(x) > 1]
    if dupes:
        fail(f"重复ID: {dupes}")
    else:
        ok("ID无重复")

# 2. storyline-data.json
print("\n--- storyline-data.json ---")
sdp = os.path.join(BASE, "storyline-data.json")
if not os.path.exists(sdp):
    fail("storyline-data.json 不存在")
else:
    with open(sdp, 'r', encoding='utf-8') as f:
        data = json.load(f)
    ok(f"格式正确")
    ok(f"  角色: {len(data.get('characters', []))}")
    ok(f"  目的地: {len(data.get('destinations', []))}")
    archive = data.get('archive', []) or data.get('storyArchive', [])
    ok(f"  档案: {len(archive)}")
    ok(f"  主题: {len(data.get('themes', []))}")
    ok(f"  美术风格: {len(data.get('artStyles', []))}")

# 3. index.html
print("\n--- index.html ---")
ip = os.path.join(BASE, "index.html")
with open(ip, 'r', encoding='utf-8') as f:
    html = f.read()

ok(f"文件大小: {len(html)} 字符, {html.count(chr(10))} 行")

# 结构检查
for tag in ['<!DOCTYPE html>', '<html', '</html>', '<head>', '</head>', '<body>', '</body>', '</script>']:
    if tag in html:
        ok(f"包含 {tag}")
    else:
        fail(f"缺少 {tag}")

# 动态加载检查
if "fetch('stories.json" in html or 'fetch("stories.json' in html:
    ok("使用 fetch('stories.json') 动态加载")
else:
    fail("未找到 fetch('stories.json')")

if "fetch('storyline-data.json" in html or 'fetch("storyline-data.json' in html:
    ok("使用 fetch('storyline-data.json') 动态加载")
else:
    fail("未找到 fetch('storyline-data.json')")

if 'serviceWorker' in html:
    ok("Service Worker 已注册")
else:
    fail("Service Worker 未注册")

if 'EMBEDDED_STORIES' in html:
    fail("仍然包含 EMBEDDED_STORIES（应已移除）")
else:
    ok("EMBEDDED_STORIES 已移除")

# 4. sw.js
print("\n--- sw.js ---")
swp = os.path.join(BASE, "sw.js")
if os.path.exists(swp):
    ok("sw.js 存在")
else:
    fail("sw.js 不存在")

# 5. scripts
print("\n--- scripts ---")
scripts = ['validate-stories.js', 'ci-validate.js', 'rewrite_index.py', 'verify_all.py']
for s in scripts:
    sp = os.path.join(BASE, 'scripts', s)
    if os.path.exists(sp):
        ok(f"{s}")
    else:
        fail(f"{s} 不存在")

# 6. 插图脚本约束
print("\n--- 插图生成约束 ---")
igp = os.path.join(BASE, 'scripts', 'generate_illustrations.py')
if os.path.exists(igp):
    with open(igp, 'r', encoding='utf-8') as f:
        content = f.read()
    if '文字' in content and '字母' in content:
        ok("已添加文字/字母约束")
    else:
        fail("缺少文字/字母约束")

print("\n--- 结果 ---")
if errors > 0:
    print(f"❌ 有 {errors} 个问题")
    sys.exit(1)
else:
    print("✅ 所有检查通过!")
