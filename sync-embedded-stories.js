#!/usr/bin/env node
/**
 * sync-embedded-stories.js
 * 读取 stories.json，生成最新的 EMBEDDED_STORIES 数组，替换到 index.html 中
 * 正确处理 JavaScript 字符串中的括号
 */
const fs = require('fs');
const path = require('path');

const STORIES_JSON = path.join(__dirname, 'stories.json');
const INDEX_HTML = path.join(__dirname, 'index.html');

// 1. 读取 stories.json
console.log('📖 读取 stories.json...');
const stories = JSON.parse(fs.readFileSync(STORIES_JSON, 'utf8'));
console.log(`   找到 ${stories.length} 个故事`);

// 2. 读取 index.html
console.log('📄 读取 index.html...');
let html = fs.readFileSync(INDEX_HTML, 'utf8');

// 3. 找到 EMBEDDED_STORIES 的开始位置
const startMarker = 'const EMBEDDED_STORIES = [';
const startIdx = html.indexOf(startMarker);
if (startIdx === -1) {
  console.error('❌ 未找到 EMBEDDED_STORIES 标记');
  process.exit(1);
}

// 4. 找到对应的 ]; （正确处理字符串中的括号）
// 从 startMarker 之后开始，depth=1 对应外层数组
let depth = 1;
let inString = false;
let escapeNext = false;
let endIdx = -1;

for (let i = startIdx + startMarker.length; i < html.length; i++) {
  const ch = html[i];
  
  if (escapeNext) { escapeNext = false; continue; }
  if (ch === '\\' && inString) { escapeNext = true; continue; }
  if (ch === '"') { inString = !inString; continue; }
  if (inString) continue;
  
  if (ch === '[') depth++;
  if (ch === ']') {
    depth--;
    if (depth === 0) {
      endIdx = i + 1;
      break;
    }
  }
}

if (endIdx === -1) {
  console.error('❌ 未找到 EMBEDDED_STORIES 的结束 ];');
  process.exit(1);
}

console.log(`   当前位置: ${startIdx} - ${endIdx}`);

// 5. 生成新的 EMBEDDED_STORIES 字符串
const newArrayStr = JSON.stringify(stories, null, 2);

// 6. 替换
const before = html.substring(0, startIdx);
const after = html.substring(endIdx);
html = before + startMarker + newArrayStr + ';\n' + after;

// 7. 写回
fs.writeFileSync(INDEX_HTML, html, 'utf8');

console.log('✅ 已同步！');
console.log(`   文件大小: ${(html.length / 1024).toFixed(1)} KB`);
console.log(`   故事数量: ${stories.length} 个`);

// 统计
const daily = stories.filter(s => !s.series).length;
const series = stories.filter(s => s.series).length;
const science = stories.filter(s => s.category === 'science').length;
console.log(`   每日故事: ${daily} 个`);
console.log(`   系列故事: ${series} 个`);
console.log(`   科学故事: ${science} 个`);
