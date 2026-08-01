#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 stories.json 内嵌进 index.html，保证"打开即渲染、不依赖 fetch"。
同时保留后台静默 fetch 更新（stories.json 有新增时无缝刷新）。

用法: python3 scripts/embed_stories.py [path/to/index.html] [path/to/stories.json]
默认操作当前目录下的 index.html 与 stories.json。
"""
import json
import re
import sys
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, 'index.html')
STORIES = sys.argv[2] if len(sys.argv) > 2 else os.path.join(BASE, 'stories.json')


def main():
    with open(STORIES, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open(INDEX, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1) 生成内嵌 JSON，转义 </ 防止提前闭合 script 标签
    js = json.dumps(data, ensure_ascii=False)
    js = js.replace('</', '<\\/')
    embed = '<script id="embedded-stories" type="application/json">\n' + js + '\n</script>\n'

    # 注入到主脚本之前（pinyin-pro CDN 之后）
    marker = '<script>\n// ===== 全局错误捕获'
    if marker in html:
        if 'id="embedded-stories"' not in html:
            html = html.replace(marker, embed + marker, 1)
        else:
            # 已存在则更新内容
            html = re.sub(
                r'<script id="embedded-stories" type="application/json">.*?</script>\n',
                embed, html, count=1, flags=re.DOTALL)
    else:
        raise SystemExit('未找到注入标记，index.html 结构已变')

    # 2) STORIES 声明改为从内嵌读取
    html = html.replace(
        'let STORIES = [];',
        'let STORIES = JSON.parse(document.getElementById("embedded-stories").textContent);',
        1)

    # 3) init 改为内嵌优先 + 后台静默更新
    new_init = '''// ===== 初始化 (内嵌优先，保证立即渲染，不依赖 fetch) =====
function init() {
  const container = document.getElementById('storyList');
  if (!STORIES || STORIES.length === 0) {
    if (container) container.innerHTML = '<div class="loading">😕 故事数据缺失，请刷新重试</div>';
    return;
  }
  buildSearchIndex();
  renderStoryList();

  // 后台静默更新(失败不影响已显示内容)
  (async () => {
    try {
      const res = await fetch('stories.json?t=' + Date.now());
      const latest = await res.json();
      if (Array.isArray(latest) && latest.length >= STORIES.length) {
        STORIES = latest;
        buildSearchIndex();
        renderStoryList();
      }
    } catch (e) { /* 静默 */ }
    try {
      const r2 = await fetch('storyline-data.json?t=' + Date.now());
      STORYLINE = await r2.json();
      window.STORYLINE_DATA = STORYLINE;
    } catch (e) { /* 静默 */ }
  })();
}
init();'''

    html = re.sub(r'\(async function init\(\) \{.*?\}\)\(\);', new_init, html, count=1, flags=re.DOTALL)

    with open(INDEX, 'w', encoding='utf-8') as f:
        f.write(html)

    print('OK: 已内嵌 %d 篇故事到 %s' % (len(data), os.path.basename(INDEX)))


if __name__ == '__main__':
    main()
