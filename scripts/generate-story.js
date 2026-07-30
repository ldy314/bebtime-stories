#!/usr/bin/env node
/**
 * Bedtime Story Generator
 * 
 * Calls DeepSeek API to generate Chinese and English bedtime stories.
 * Checks for missing stories (today + last 7 days), generates them,
 * and updates stories.json, index.html (EMBEDDED_STORIES), and collection.html.
 * 
 * Environment variables:
 *   DEEPSEEK_API_KEY - API key for DeepSeek (required)
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
  buildEnglishPrompt
} = require('./prompt-builder');

// ===== Configuration =====
const API_KEY = process.env.DEEPSEEK_API_KEY;
const API_HOST = 'api.deepseek.com';
const API_PATH = '/v1/chat/completions';
const MODEL = 'deepseek-chat';
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
function callDeepSeekAPI(userPrompt) {
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
      max_tokens: 4096
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
      const result = await callDeepSeekAPI(prompt);
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
function buildStoryObj(raw, dateStr, language, ageInfo) {
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

  return {
    id: `${dateStr}-${language === 'zh' ? 'cn' : 'en'}`,
    date: `${dateCn} · ${weekday}`,
    dateShort,
    title,
    language,
    ageGroup: ageInfo.group,
    ageLabel: language === 'zh' ? ageInfo.labelCn : ageInfo.labelEn,
    preview,
    moral,
    content
  };
}

// ===== Main =====

async function main() {
  if (!API_KEY) {
    console.error('ERROR: DEEPSEEK_API_KEY environment variable is not set.');
    console.error('Please set it as a GitHub repository secret.');
    process.exit(1);
  }

  console.log('=== Bedtime Story Generator ===');
  console.log(`Beijing time: ${getBeijingDateStr()} ${new Date().toUTCString()}`);

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
  for (const { dateStr, language } of missingStories) {
    const ageInfo = getAgeInfo(dateStr);
    console.log(`\nGenerating ${language.toUpperCase()} story for ${dateStr} (${ageInfo.labelCn || ageInfo.labelEn})...`);

    try {
      const prompt = language === 'zh'
        ? buildChinesePrompt(dateStr, ageInfo)
        : buildEnglishPrompt(dateStr, ageInfo);

      const raw = await callAPIWithRetry(prompt, `${dateStr}-${language}`);
      const story = buildStoryObj(raw, dateStr, language, ageInfo);

      // Validate required fields
      if (!story.title || !story.content || story.content.length === 0) {
        console.error(`  WARNING: Story for ${dateStr}-${language} has missing fields, skipping.`);
        continue;
      }

      newStories.push(story);
      console.log(`  Title: ${story.title}`);
      console.log(`  Paragraphs: ${story.content.length}`);
    } catch (err) {
      console.error(`  ERROR generating ${dateStr}-${language}: ${err.message}`);
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
