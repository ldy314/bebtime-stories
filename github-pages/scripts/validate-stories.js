#!/usr/bin/env node
/**
 * stories.json Schema验证 + 自动同步到index.html
 * 用法: node scripts/validate-stories.js [--sync]
 * 
 * 验证规则:
 * 1. 每个故事必须包含 id, date, title, language, content 字段
 * 2. id 格式: YYYY-MM-DD-{lang}
 * 3. language 必须是 'zh' 或 'en'
 * 4. content 必须是非空字符串数组
 * 5. 无重复 id
 * 6. 可选字段类型检查
 */

const fs = require('fs');
const path = require('path');

const STORIES_PATH = path.join(__dirname, '..', 'stories.json');
const INDEX_PATH = path.join(__dirname, '..', 'index.html');

// ============ Schema验证 ============

function validateStory(story, index) {
  const errors = [];
  const prefix = `故事[${index}]`;

  // 必填字段
  const required = ['id', 'date', 'title', 'language', 'content'];
  for (const field of required) {
    if (!(field in story)) {
      errors.push(`${prefix}: 缺少必填字段 "${field}"`);
    }
  }

  if (errors.length) return errors;

  // id 格式验证
  if (!/^\d{4}-\d{2}-\d{2}-(zh|en)$/.test(story.id)) {
    errors.push(`${prefix}: id格式错误 "${story.id}" (应为 YYYY-MM-DD-{zh|en})`);
  }

  // language 验证
  if (!['zh', 'en'].includes(story.language)) {
    errors.push(`${prefix}: language "${story.language}" 无效 (应为 zh 或 en)`);
  }

  // content 验证
  if (!Array.isArray(story.content) || story.content.length === 0) {
    errors.push(`${prefix}: content 必须是非空数组`);
  } else {
    const invalidIdx = story.content.findIndex(p => typeof p !== 'string' || !p.trim());
    if (invalidIdx >= 0) {
      errors.push(`${prefix}: content[${invalidIdx}] 无效 (空字符串或非字符串)`);
    }
  }

  // 可选字段类型检查
  if (story.moral !== undefined && typeof story.moral !== 'string') {
    errors.push(`${prefix}: moral 必须是字符串`);
  }
  if (story.preview !== undefined && typeof story.preview !== 'string') {
    errors.push(`${prefix}: preview 必须是字符串`);
  }
  if (story.dateShort !== undefined && typeof story.dateShort !== 'string') {
    errors.push(`${prefix}: dateShort 必须是字符串`);
  }

  return errors;
}

function validateStories() {
  console.log('📖 验证 stories.json...');

  if (!fs.existsSync(STORIES_PATH)) {
    console.error('❌ stories.json 不存在');
    process.exit(1);
  }

  let stories;
  try {
    const raw = fs.readFileSync(STORIES_PATH, 'utf-8');
    stories = JSON.parse(raw);
  } catch (e) {
    console.error(`❌ JSON解析失败: ${e.message}`);
    process.exit(1);
  }

  if (!Array.isArray(stories)) {
    console.error('❌ stories.json 必须是数组');
    process.exit(1);
  }

  const allErrors = [];
  const idSet = new Set();

  stories.forEach((story, i) => {
    const errs = validateStory(story, i);
    allErrors.push(...errs);

    if (idSet.has(story.id)) {
      allErrors.push(`重复id: "${story.id}"`);
    }
    idSet.add(story.id);
  });

  if (allErrors.length > 0) {
    console.error(`\n❌ 发现 ${allErrors.length} 个错误:`);
    allErrors.forEach(e => console.error(`   - ${e}`));
    process.exit(1);
  }

  // 统计
  const zhCount = stories.filter(s => s.language === 'zh').length;
  const enCount = stories.filter(s => s.language === 'en').length;
  const ageGroups = {};
  stories.forEach(s => {
    const g = s.ageGroup || 'unknown';
    ageGroups[g] = (ageGroups[g] || 0) + 1;
  });

  console.log(`✅ 验证通过! 共 ${stories.length} 个故事`);
  console.log(`   中文: ${zhCount} | 英文: ${enCount}`);
  console.log(`   年龄组: ${Object.entries(ageGroups).map(([g, c]) => `${g}=${c}`).join(', ')}`);

  return stories;
}

// ============ 同步到index.html ============

function syncToIndex(stories) {
  console.log('\n🔄 同步到 index.html...');

  if (!fs.existsSync(INDEX_PATH)) {
    console.error('❌ index.html 不存在');
    process.exit(1);
  }

  let html = fs.readFileSync(INDEX_PATH, 'utf-8');

  // 检查是否使用动态加载
  if (html.includes('fetch(\'stories.json\')') || html.includes("fetch(\"stories.json\")")) {
    console.log('ℹ️  index.html 已使用动态加载，跳过同步');
    return;
  }

  // 替换 EMBEDDED_STORIES
  const storiesJson = JSON.stringify(stories, null, 0);
  
  // 匹配 const EMBEDDED_STORIES = [...];
  const embeddedRegex = /const EMBEDDED_STORIES\s*=\s*\[[\s\S]*?\];/;
  
  if (!embeddedRegex.test(html)) {
    console.error('❌ 未找到 EMBEDDED_STORIES 定义');
    process.exit(1);
  }

  const replacement = `const EMBEDDED_STORIES = ${storiesJson};`;
  html = html.replace(embeddedRegex, replacement);

  fs.writeFileSync(INDEX_PATH, html, 'utf-8');
  console.log('✅ 同步完成');
}

// ============ 主入口 ============

const args = process.argv.slice(2);
const shouldSync = args.includes('--sync');

const stories = validateStories();

if (shouldSync) {
  syncToIndex(stories);
}
