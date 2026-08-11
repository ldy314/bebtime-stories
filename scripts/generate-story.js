#!/usr/bin/env node
/**
 * Bedtime Story Generator
 * 
 * Calls Zhipu (智谱) API to generate Chinese and English bedtime stories.
 * Checks for missing stories (today + last 7 days), generates them,
 * and updates stories.json, index.html (EMBEDDED_STORIES), and collection.html.
 * 
 * Environment variables:
 *   ZHIPU_API_KEY - API key for Zhipu/智谱 (required)
 * 
 * Usage:
 *   node scripts/generate-story.js
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const {
  getAgeInfo,
  getChineseWeekday,
  formatDateCn,
  formatDateShort,
  buildChinesePrompt,
  buildEnglishPrompt,
  isScienceDay,
  fetchScienceArticle,
  buildScienceChinesePrompt,
  buildScienceEnglishPrompt
} = require('./prompt-builder');

// ===== Configuration =====
const API_KEY = process.env.ZHIPU_API_KEY;
const API_HOST = 'open.bigmodel.cn';
const API_PATH = '/api/paas/v4/chat/completions';
const MODEL = 'glm-4v-flash';
const MAX_RETRIES = 3;
const RETRY_DELAY_MS = 5000;

const ROOT_DIR = path.join(__dirname, '..');
const STORIES_PATH = path.join(ROOT_DIR, 'stories.json');
const INDEX_PATH = path.join(ROOT_DIR, 'index.html');

// ===== Helpers =====

/**
 * Get Beijing time date string (YYYY-MM-DD) with optional day offset
 */
function getBeijingDateStr(offsetDays = 0) {
  const now = new Date();
  const beijing = new Date(now.getTime() + 8 * 60 * 60 * 1000 + offsetDays * 24 * 60 * 60 * 1000);
  const yyyy = beijing.getUTCFullYear();
  const mm = String(beijing.getUTCMonth() + 1).padStart(2, '0');
  const dd = String(beijing.getUTCDate()).padStart(2, '0');
  return `${yyyy}-${mm}-${dd}`;
}

/**
 * Call DeepSeek API with a prompt and return parsed JSON
 */
function callZhipuAPI(userPrompt) {
  return new Promise((resolve, reject) => {
    const systemPrompt = 'You are a creative children\'s bedtime story writer. You write in both Chinese and English. You always respond with valid JSON when asked.';

    const requestData = JSON.stringify({
      model: MODEL,
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: userPrompt }
      ],
      response_format: { type: 'json_object' },
      temperature: 0.85,
      max_tokens: 1024
    });

    const options = {
      hostname: API_HOST,
      path: API_PATH,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Length': Buffer.byteLength(requestData)
      }
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        if (res.statusCode !== 200) {
          reject(new Error(`API returned ${res.statusCode}: ${body.substring(0, 500)}`));
          return;
        }
        try {
          const response = JSON.parse(body);
          const content = response.choices?.[0]?.message?.content;
          if (!content) {
            reject(new Error('No content in API response'));
            return;
          }
          const parsed = JSON.parse(content);
          resolve(parsed);
        } catch (e) {
          reject(new Error(`Failed to parse API response: ${e.message}`));
        }
      });
    });

    req.on('error', reject);
    req.write(requestData);
    req.end();
  });
}

/**
 * Call API with retry logic
 */
async function callAPIWithRetry(prompt, label) {
  for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
    try {
      console.log(`  [${label}] Attempt ${attempt}/${MAX_RETRIES}...`);
      const result = await callZhipuAPI(prompt);
      console.log(`  [${label}] Success!`);
      return result;
    } catch (err) {
      console.error(`  [${label}] Attempt ${attempt} failed: ${err.message}`);
      if (attempt < MAX_RETRIES) {
        console.log(`  [${label}] Retrying in ${RETRY_DELAY_MS / 1000}s...`);
        await new Promise(r => setTimeout(r, RETRY_DELAY_MS));
      } else {
        throw err;
      }
    }
  }
}

/**
 * Update EMBEDDED_STORIES in index.html
 */
function updateEmbeddedStories(indexPath, stories) {
  let html = fs.readFileSync(indexPath, 'utf8');
  const jsonStr = JSON.stringify(stories);
  const lines = html.split('\n');
  const embeddedIndex = lines.findIndex(line => line.trim().startsWith('const EMBEDDED_STORIES = '));
  if (embeddedIndex === -1) {
    throw new Error('Could not find EMBEDDED_STORIES line in index.html');
  }
  lines[embeddedIndex] = `const EMBEDDED_STORIES = ${jsonStr};`;
  fs.writeFileSync(indexPath, lines.join('\n'), 'utf8');
  console.log(`  Updated EMBEDDED_STORIES with ${stories.length} stories`);
}

/**
 * Sanitize text - replace curly quotes that break JSON
 */
function sanitizeText(text) {
  if (typeof text !== 'string') return text;
  return text
    .replace(/\u201c/g, '\u300c')  // " -> 「
    .replace(/\u201d/g, '\u300d')  // " -> 」
    .replace(/\u2018/g, '\'')       // ' -> '
    .replace(/\u2019/g, '\'');      // ' -> '
}

/**
 * Validate and build a story object
 */
function buildStoryObj(raw, dateStr, language, ageInfo, category = 'regular') {
  const dateCn = formatDateCn(dateStr);
  const weekday = getChineseWeekday(dateStr);
  const dateShort = formatDateShort(dateStr);

  const title = sanitizeText(raw.title || 'Untitled');
  const preview = sanitizeText(raw.preview || '');
  const moral = sanitizeText(raw.moral || '');
  
  let content;
  if (Array.isArray(raw.content)) {
    content = raw.content.map(p => sanitizeText(String(p)));
  } else if (typeof raw.content === 'string') {
    content = [sanitizeText(raw.content)];
  } else {
    content = [];
  }

  // Filter out empty paragraphs
  content = content.filter(p => p && p.trim());

  const langSuffix = language === 'zh' ? 'cn' : 'en';
  const idSuffix = category === 'science' ? `science-${langSuffix}` : langSuffix;
  const obj = {
    id: `${dateStr}-${idSuffix}`,
    date: `${dateCn} · ${weekday}`,
    dateShort,
    title,
    language,
    ageGroup: ageInfo.group,
    ageLabel: language === 'zh' ? ageInfo.labelCn : ageInfo.labelEn,
    preview,
    moral,
    content,
    category
  };
  if (category === 'science') {
    obj.series = 'science';
    obj.seriesTitle = '科学故事';
    if (raw.source) obj.source = raw.source;
  }
  return obj;
}

// ===== Main =====

async function main() {
  if (!API_KEY) {
    console.error('ERROR: ZHIPU_API_KEY environment variable is not set.');
    console.error('Please set it as a GitHub repository secret.');
    process.exit(1);
  }

  console.log('=== Bedtime Story Generator ===');
  console.log(`Beijing time: ${getBeijingDateStr()} ${new Date().toUTCString()}`);

  // 每月 1 号自动运行种子刷新脚本（getUnlockedSeeds 自动解锁新批次）
  const today = new Date();
  if (today.getUTCDate() === 1) {
    console.log('\n=== Monthly Seed Refresh (1st of month) ===');
    try {
      const { execSync } = require('child_process');
      const nodeBin = process.execPath;
      const refreshScript = path.join(__dirname, 'refresh-seeds.js');
      execSync(`"${nodeBin}" "${refreshScript}" --batch-only`, { cwd: ROOT_DIR, stdio: 'inherit' });
      console.log('Monthly seed refresh completed.');
    } catch (err) {
      console.warn('Warning: Monthly seed refresh failed (non-fatal):', err.message);
    }
    console.log('');
  }

  // Read existing stories
  const stories = JSON.parse(fs.readFileSync(STORIES_PATH, 'utf8'));
  console.log(`Current stories: ${stories.length} (${stories.filter(s => s.language === 'zh').length} ZH, ${stories.filter(s => s.language === 'en').length} EN)`);

  // Check for missing stories: today + last 7 days
  const datesToCheck = [];
  for (let i = 0; i <= 7; i++) {
    datesToCheck.push(getBeijingDateStr(-i));
  }

  const missingStories = [];
  for (const dateStr of datesToCheck) {
    const hasCn = stories.some(s => s.id === `${dateStr}-cn`);
    const hasEn = stories.some(s => s.id === `${dateStr}-en`);
    if (!hasCn) missingStories.push({ dateStr, language: 'zh' });
    if (!hasEn) missingStories.push({ dateStr, language: 'en' });
    // 每周随机一天：额外生成中英双语「科学故事」（确定性，云端/本地一致）
    if (isScienceDay(dateStr)) {
      const hasSciCn = stories.some(s => s.id === `${dateStr}-science-cn`);
      const hasSciEn = stories.some(s => s.id === `${dateStr}-science-en`);
      if (!hasSciCn) missingStories.push({ dateStr, language: 'zh', category: 'science' });
      if (!hasSciEn) missingStories.push({ dateStr, language: 'en', category: 'science' });
    }
  }

  if (missingStories.length === 0) {
    console.log('\nAll stories up to date (today + last 7 days). Nothing to do.');
    return;
  }

  console.log(`\nFound ${missingStories.length} missing stories:`);
  missingStories.forEach(m => console.log(`  - ${m.dateStr} ${m.language}`));

  // Sort by date (oldest first)
  missingStories.sort((a, b) => {
    if (a.dateStr !== b.dateStr) return a.dateStr.localeCompare(b.dateStr);
    return a.language.localeCompare(b.language);
  });

  // Generate each missing story
  const newStories = [];
  for (const { dateStr, language, category } of missingStories) {
    const ageInfo = getAgeInfo(dateStr);
    const isSci = category === 'science';
    const logName = isSci ? `SCIENCE ${language.toUpperCase()}` : language.toUpperCase();
    console.log(`\nGenerating ${logName} story for ${dateStr} (${ageInfo.labelCn || ageInfo.labelEn})...`);

    try {
      let prompt, raw, tag;
      if (isSci) {
        const article = await fetchScienceArticle(language);
        tag = `${dateStr}-science-${language === 'zh' ? 'cn' : 'en'}`;
        prompt = language === 'zh'
          ? buildScienceChinesePrompt(article, ageInfo, dateStr)
          : buildScienceEnglishPrompt(article, ageInfo, dateStr);
        raw = await callAPIWithRetry(prompt, tag);
        raw.source = article ? article.source : (language === 'zh' ? '儿童科普常识' : "Children's science (general)"); // 标记来源（始终有值）
      } else {
        tag = `${dateStr}-${language}`;
        prompt = language === 'zh'
          ? buildChinesePrompt(dateStr, ageInfo)
          : buildEnglishPrompt(dateStr, ageInfo);
        raw = await callAPIWithRetry(prompt, tag);
      }

      const story = buildStoryObj(raw, dateStr, language, ageInfo, category || 'regular');

      // Validate required fields
      if (!story.title || !story.content || story.content.length === 0) {
        console.error(`  WARNING: Story for ${tag} has missing fields, skipping.`);
        continue;
      }

      newStories.push(story);
      console.log(`  Title: ${story.title}`);
      console.log(`  Paragraphs: ${story.content.length}`);
    } catch (err) {
      console.error(`  ERROR generating ${dateStr}-${language}${isSci ? ' (science)' : ''}: ${err.message}`);
      // Continue with other stories even if one fails
    }
  }

  if (newStories.length === 0) {
    console.log('\nNo stories were successfully generated. Exiting.');
    return;
  }

  // Add new stories to the array
  stories.push(...newStories);
  console.log(`\nTotal stories after update: ${stories.length}`);

  // Write stories.json
  fs.writeFileSync(STORIES_PATH, JSON.stringify(stories, null, 2) + '\n', 'utf8');
  console.log('Updated stories.json');

  // Update EMBEDDED_STORIES in index.html
  updateEmbeddedStories(INDEX_PATH, stories);

  // Generate collection HTML
  try {
    const { execSync } = require('child_process');
    const nodeBin = process.execPath;
    const collectionScript = path.join(__dirname, 'generate-collection-html.js');
    execSync(`"${nodeBin}" "${collectionScript}"`, { cwd: ROOT_DIR, stdio: 'inherit' });
  } catch (err) {
    console.error('Warning: Failed to generate collection HTML:', err.message);
  }

  console.log('\n=== Done! ===');
  console.log(`Generated ${newStories.length} new stories.`);
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
