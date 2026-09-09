#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Insert the prenatal "故事孕育师" enhancement block into prompt-builder.js
and wire it into all four prompt builders (Chinese/English x normal/science),
scoped strictly to ageInfo.group === 'prenatal'.
"""
import sys

import os
PB = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\Administrator\WorkBuddy\Claw\github-bedtime-stories\scripts\prompt-builder.js"
BLOCK = r"D:\code test\睡前故事\tmp_prenatal_block.js"
print("TARGET:", PB)

with open(PB, encoding="utf-8") as f:
    src = f.read()
with open(BLOCK, encoding="utf-8") as f:
    block = f.read().strip()

def replace_once(s, old, new, label):
    cnt = s.count(old)
    if cnt != 1:
        print(f"[FAIL] expected exactly 1 occurrence of marker for {label!r}, found {cnt}")
        print("  snippet around expected:")
        print("    " + old[:120].replace("\n", "\\n"))
        sys.exit(1)
    return s.replace(old, new, 1)

# ---- 1) Insert the prenatal block before pickTheme ----
marker = "function pickTheme(dateStr, lang) {"
assert marker in src, "pickTheme marker missing"
if "PRENATAL_CAST" in src:
    print("[SKIP] PRENATAL_CAST already present; not re-inserting block.")
else:
    idx = src.index(marker)
    src = src[:idx] + block + "\n\n" + src[idx:]

# ---- 2) buildChinesePrompt ----
old = "  const theme = pickTheme(dateStr, 'zh');\n  return `"
new = ("  const theme = pickTheme(dateStr, 'zh');\n"
       "  const prenatalBlock = ageInfo.group === 'prenatal' ? buildPrenatalBlock(dateStr, 'zh') : '';\n"
       "  return `")
src = replace_once(src, old, new, "cn: add prenatalBlock var")

old = "\n**重要格式要求：**"
new = "\n${prenatalBlock}\n\n**重要格式要求：**"
src = replace_once(src, old, new, "cn: inject prenatalBlock before format reqs")

# ---- 3) buildEnglishPrompt ----
old = "  const theme = pickTheme(dateStr, 'en');\n  return `"
new = ("  const theme = pickTheme(dateStr, 'en');\n"
       "  const prenatalBlock = ageInfo.group === 'prenatal' ? buildPrenatalBlock(dateStr, 'en') : '';\n"
       "  return `")
src = replace_once(src, old, new, "en: add prenatalBlock var")

old = "\n**Important format requirements:**"
new = "\n${prenatalBlock}\n\n**Important format requirements:**"
src = replace_once(src, old, new, "en: inject prenatalBlock before format reqs")

# ---- 4) buildScienceChinesePrompt ----
old = "  const ageStyle = AGE_STYLE_CN[ageInfo.group];\n  const seed = article"
new = ("  const ageStyle = AGE_STYLE_CN[ageInfo.group];\n"
       "  const prenatalBlock = ageInfo.group === 'prenatal' ? buildPrenatalBlock(dateStr, 'zh') : '';\n"
       "  const seed = article")
src = replace_once(src, old, new, "sci-cn: add prenatalBlock var")

old = "\n重要格式要求："
new = "\n${prenatalBlock}\n\n重要格式要求："
src = replace_once(src, old, new, "sci-cn: inject prenatalBlock before format reqs")

# ---- 5) buildScienceEnglishPrompt ----
old = "  const ageStyle = AGE_STYLE_EN[ageInfo.group];\n  const seed = article"
new = ("  const ageStyle = AGE_STYLE_EN[ageInfo.group];\n"
       "  const prenatalBlock = ageInfo.group === 'prenatal' ? buildPrenatalBlock(dateStr, 'en') : '';\n"
       "  const seed = article")
src = replace_once(src, old, new, "sci-en: add prenatalBlock var")

old = "\nFormat requirements:"
new = "\n${prenatalBlock}\n\nFormat requirements:"
src = replace_once(src, old, new, "sci-en: inject prenatalBlock before format reqs")

with open(PB, "w", encoding="utf-8") as f:
    f.write(src)

print("[OK] prompt-builder.js updated with prenatal enhancement block.")
print("PRENATAL_CAST present:", "PRENATAL_CAST" in src)
print("buildPrenatalBlock present:", "buildPrenatalBlock" in src)
print("prenatalBlock injections (cn/en/sci-cn/sci-en):",
      src.count("const prenatalBlock = ageInfo.group === 'prenatal'"))
