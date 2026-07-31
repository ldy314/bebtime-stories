#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remove crab (加蟹小笼包 -> 小笼包) from published data + non-generated docs to honor 内容禁忌（禁用大闸蟹/螃蟹）。"""
import os

FILES = [
    r"D:/code test/睡前故事/stories.json",
    r"D:/code test/睡前故事/github-pages/stories.json",
    r"D:/code test/睡前故事/storyline/00-权威源文件/stories.json",
    r"C:/Users/Administrator/WorkBuddy/Claw/bedtime-story-app/stories.json",
    r"D:/code test/睡前故事/index.html",
    r"D:/code test/睡前故事/github-pages/index.html",
    r"C:/Users/Administrator/WorkBuddy/Claw/bedtime-story-app/index.html",
    r"D:/code test/睡前故事/dangdang-series-outline.md",
    r"D:/code test/睡前故事/storyline/05-故事历史档案库/分集大纲.md",
    r"D:/code test/睡前故事/storyline/00-权威源文件/dangdang-series-outline.md",
    r"D:/code test/睡前故事/storyline/03-道具与美食素材库/README.md",
    r"D:/code test/睡前故事/storyline/03-道具与美食素材库/各地特色美食.md",
    r"D:/code test/睡前故事/storyline/05-故事历史档案库/已发布故事/ep16-八百不挑食了.md",
    r"D:/code test/睡前故事/bedtime-story-collection.md",
    r"D:/code test/睡前故事/bedtime-story-collection.html",
]

OLD = "加蟹小笼包"
NEW = "小笼包"

total = 0
for f in FILES:
    if not os.path.exists(f):
        print("SKIP (missing):", f)
        continue
    try:
        data = open(f, "r", encoding="utf-8").read()
    except Exception as e:
        print("READ ERR", f, e)
        continue
    cnt = data.count(OLD)
    if cnt:
        data = data.replace(OLD, NEW)
        open(f, "w", encoding="utf-8").write(data)
        total += cnt
        print(f"FIXED {cnt}x in {f}")
    else:
        print("clean:", os.path.basename(f))

print(f"\nTotal replacements: {total}")
