#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""一次性执行 rename + status + next，避免多命令组合。"""
import subprocess, sys, os

PY = r"C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
BASE = r"D:/code test/睡前故事"
BATCH = os.path.join(BASE, "scripts", "illust_batch.py")

n = sys.argv[1] if len(sys.argv) > 1 else "8"

r = subprocess.run([PY, BATCH, "rename"], capture_output=True, text=True, encoding="utf-8", cwd=BASE)
print(r.stdout, end="")
r = subprocess.run([PY, BATCH, "next", n], capture_output=True, text=True, encoding="utf-8", cwd=BASE)
print(r.stdout, end="")
