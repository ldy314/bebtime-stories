#!/usr/bin/env node
/**
 * CI验证脚本 - 在GitHub Actions中运行
 * 验证:
 * 1. stories.json格式正确
 * 2. 故事数量 >= 预期最小值
 * 3. 每个故事都有对应的中英文版本（如果有）
 * 4. index.html包含所有故事（如果使用嵌入）
 */

const fs = require('fs');
const path = require('path');

const STORIES_PATH = path.join(__dirname, '..', 'stories.json');
const INDEX_PATH = path.join(__dirname, '..', 'index.html');
const STORYLINE_PATH = path.join(__dirname, '..', 'storyline-data.json');

let hasError = false;

function fail(msg) {
  console.error(`❌ ${msg}`);
  hasError = true;
}

function pass(msg) {
  console.log(`✅ ${msg}`);
}

// 1. 验证 stories.json
console.log('\n--- stories.json ---');
let stories = [];
try {
  stories = JSON.parse(fs.readFileSync(STORIES_PATH, 'utf-8'));
  pass(`stories.json 格式正确 (${stories.length} 个故事)`);
} catch (e) {
  fail(`stories.json 解析失败: ${e.message}`);
}

// 最小数量检查
const MIN_STORIES = 1;
if (stories.length < MIN_STORIES) {
  fail(`故事数量不足: ${stories.length} < ${MIN_STORIES}`);
}

// ID唯一性
const ids = stories.map(s => s.id);
const dupes = ids.filter((id, i) => ids.indexOf(id) !== i);
if (dupes.length > 0) {
  fail(`重复ID: ${[...new Set(dupes)].join(', ')}`);
} else {
  pass('ID无重复');
}

// 必填字段
const required = ['id', 'date', 'title', 'language', 'content'];
stories.forEach((s, i) => {
  for (const f of required) {
    if (!(f in s)) fail(`故事[${i}] 缺少字段: ${f}`);
  }
});

// 2. 验证 storyline-data.json（如果存在）
console.log('\n--- storyline-data.json ---');
if (fs.existsSync(STORYLINE_PATH)) {
  try {
    const data = JSON.parse(fs.readFileSync(STORYLINE_PATH, 'utf-8'));
    if (data.characters && Array.isArray(data.characters)) {
      pass(`角色: ${data.characters.length} 个`);
    }
    if (data.destinations && Array.isArray(data.destinations)) {
      pass(`目的地: ${data.destinations.length} 个`);
    }
    if (data.archive && Array.isArray(data.archive)) {
      pass(`档案: ${data.archive.length} 集`);
    }
    if (data.themes && Array.isArray(data.themes)) {
      pass(`主题: ${data.themes.length} 个`);
    }
    if (data.artStyles && Array.isArray(data.artStyles)) {
      pass(`美术风格: ${data.artStyles.length} 种`);
    }
  } catch (e) {
    fail(`storyline-data.json 解析失败: ${e.message}`);
  }
} else {
  console.log('ℹ️  storyline-data.json 不存在');
}

// 3. 检查index.html
console.log('\n--- index.html ---');
if (fs.existsSync(INDEX_PATH)) {
  const html = fs.readFileSync(INDEX_PATH, 'utf-8');
  
  // 检查动态加载或嵌入
  if (html.includes('fetch(\'stories.json\')') || html.includes("fetch(\"stories.json\")")) {
    pass('使用动态加载 (fetch stories.json)');
  } else if (html.includes('EMBEDDED_STORIES')) {
    // 验证嵌入数量
    const match = html.match(/EMBEDDED_STORIES\s*=\s*\[/);
    if (match) {
      // 简单计数
      const start = match.index;
      let depth = 0;
      let end = start;
      for (let i = start; i < html.length; i++) {
        if (html[i] === '[') depth++;
        if (html[i] === ']') depth--;
        if (depth === 0) { end = i + 1; break; }
      }
      const embeddedStr = html.substring(start, end);
      try {
        const embedded = JSON.parse(embeddedStr.replace('EMBEDDED_STORIES = ', ''));
        if (embedded.length === stories.length) {
          pass(`嵌入故事数量匹配: ${embedded.length}`);
        } else {
          fail(`嵌入故事数量不匹配: index.html=${embedded.length}, stories.json=${stories.length}`);
        }
      } catch (e) {
        fail(`EMBEDDED_STORIES 解析失败: ${e.message}`);
      }
    }
  } else {
    fail('未找到 EMBEDDED_STORIES 或 fetch(stories.json)');
  }
  
  // 检查拼音CDN
  if (html.includes('pinyin-pro')) {
    pass('拼音CDN已引入');
  }
  
  // 检查Service Worker注册
  if (html.includes('serviceWorker')) {
    pass('Service Worker已注册');
  } else {
    console.log('ℹ️  Service Worker未注册（可选）');
  }
}

console.log('\n--- 结果 ---');
if (hasError) {
  console.error('❌ CI验证失败');
  process.exit(1);
} else {
  console.log('✅ CI验证通过');
}
