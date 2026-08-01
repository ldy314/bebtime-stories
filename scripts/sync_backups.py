#!/usr/bin/env python3
"""Sync all updated files to backup locations"""
import os
import shutil
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Files to sync (relative to project root)
SYNC_FILES = [
    'index.html',
    'stories.json',
    'sw.js',
    'storyline-data.json',
    'scripts/validate-stories.js',
    'scripts/ci-validate.js',
    'scripts/verify_all.py',
    'scripts/generate_illustrations.py',
]

BACKUPS = [
    os.path.expanduser('~/WorkBuddy/Claw/bedtime-story-app'),
    os.path.expanduser('~/WorkBuddy/automation-2026-07-16-11-56-46'),
    os.path.expanduser('~/WorkBuddy/Claw/github-bedtime-stories'),
]

def sync_file(rel_path, backup_dir):
    src = os.path.join(BASE, rel_path)
    dst = os.path.join(backup_dir, rel_path)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
    print(f"  → {dst}")

def main():
    print("📂 同步文件到备份位置...")
    
    for backup in BACKUPS:
        if not os.path.isdir(backup):
            print(f"⚠️  跳过 {backup} (不存在)")
            continue
        print(f"\n📁 {backup}")
        for rel_path in SYNC_FILES:
            try:
                sync_file(rel_path, backup)
            except Exception as e:
                print(f"  ❌ {rel_path}: {e}")

    print("\n✅ 同步完成!")

if __name__ == '__main__':
    main()
