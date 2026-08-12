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
  buildContinuationPrompt,
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
 * Clean continuation paragraphs: strip any "续写第N段"/"Continuation paragraph N:"/numbered prefixes
 * that the model may add, so the story body stays clean.
 */
function cleanContinuationParagraphs(paras) {
  return (paras || []).map(p => String(p)
    .replace(/^\s*(续写第?\s*\d+\s*段\s*[：:、.．]\s*)/, '')
    .replace(/^\s*(第\s*\d+\s*段\s*[：:、.．]\s*)/, '')
    .replace(/^\s*(段落\s*\d+\s*[：:、.．]\s*)/, '')
    .replace(/^\s*(Continuation\s+paragraph\s*\d+\s*[:\-.]\s*)/i, '')
    .replace(/^\s*(Para(?:graph)?\s*\d+\s*[:\-.]\s*)/i, '')
    .replace(/^\s*(接着写[：:]?\s*|继续写[：:]?\s*|Next[:\-]?\s*|Continue[:\-]?\s*)/i, '')
    .trim()
  ).filter(p => p && p.trim());
}

/**
 * Character-level Jaccard similarity between two strings (0..1)
 */
function charJaccard(a, b) {
  const clean = s => new Set(String(s).replace(/[，。！？、：；\s]/g, '').split(''));
  const sa = clean(a), sb = clean(b);
  if (!sa.size || !sb.size) return 0;
  let inter = 0;
  sa.forEach(c => { if (sb.has(c)) inter++; });
  return inter / (new Set([...sa, ...sb]).size);
}

/**
 * Deduplicate near-identical paragraphs (code-level safety net).
 * Compares each paragraph against ALL previously kept paragraphs; if char-level
 * Jaccard similarity with ANY previous paragraph > 0.6, drop it. Catches both
 * adjacent and alternating (A-B-A-C-A) loop patterns.
 */
function dedupeAdjacentParagraphs(paras) {
  const out = [];
  for (const p of paras || []) {
    const dup = out.find(prev => charJaccard(prev, p) > 0.6);
    if (dup) {
      console.log(`  [dedupe] 移除与前面某段重复的段落 (sim=${charJaccard(dup, p).toFixed(2)}): ${String(p).slice(0, 30)}...`);
      continue;
    }
    out.push(p);
  }
  return out;
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

// ===== 胎教期风格自检与定向修复（"最终组合"的 AI 修复层） =====
// 生成后检测胎教故事是否具备关键风格要素（拟声词/妈妈心跳/对肚里宝宝说话/无弯引号），
// 缺失项调用 buildFixPrompt 携全文上下文定向补写，最多补 2 轮、每轮只补缺失项。
function styleGaps(story, language) {
  const text = (story.content || []).join(' ');
  const gaps = [];
  if (language === 'zh') {
    if (!/(呼呼|哗啦|咕嘟|咚咚|扑通|叮咚|沙沙|滴答|摇啊摇|晃呀晃|飘呀飘|啾啾|蛐蛐|滴滴|嗒嗒|咕噜)/.test(text)) {
      gaps.push({ key: 'onomatopoeia', label: '故事缺少拟声词', fix: '在合适位置自然地加入 2-3 处拟声词（如呼呼、哗啦、咕嘟、咚咚、摇啊摇），让声音参与叙事' });
    }
    if (!/心跳|咚咚|扑通/.test(text)) {
      gaps.push({ key: 'heartbeat', label: '缺少「妈妈的心跳」高光', fix: '加入一处妈妈心跳高光：写「咚咚、咚咚，那是妈妈的心跳」并用「你听见了吗？」与肚里宝宝对话' });
    }
    if (!/肚子里|还没出生|肚里|还没来/.test(text)) {
      gaps.push({ key: 'unborn', label: '缺少未出生宝宝视角', fix: '把「还在肚子里的小宝宝」作为倾听者，用「小宝宝，你听到了吗？」式对话呼应' });
    }
    if (/[\u201c\u201d]/.test(JSON.stringify(story))) {
      gaps.push({ key: 'curlyquote', label: '存在中文弯引号""', fix: '把所有中文弯引号替换为「」或单引号' });
    }
  } else {
    if (!/(whoosh|patter|gurgle|thump|tweet|swish|drip|rustle|huff|plop|splash|tinkle)/i.test(text)) {
      gaps.push({ key: 'onomatopoeia', label: 'missing onomatopoeia', fix: 'naturally weave in 2-3 onomatopoeia words (whoosh, patter, gurgle, thump, swish, drip)' });
    }
    if (!/(heartbeat|thump|drum)/i.test(text)) {
      gaps.push({ key: 'heartbeat', label: 'missing "mother\'s heartbeat" highlight', fix: 'add a mother-heartbeat highlight: "thump, thump, that is Mama\'s heartbeat" and speak to the baby with "little one, can you hear it?"' });
    }
    if (!/(in mama'?s belly|unborn|not yet born|little one|tiny one)/i.test(text)) {
      gaps.push({ key: 'unborn', label: 'missing unborn-baby perspective', fix: 'address the baby in Mama\'s belly directly with "little one, can you hear?" style lines' });
    }
  }
  return gaps;
}

async function ensurePrenatalStyle(story, ageInfo, dateStr, tag) {
  if (story.ageGroup !== 'prenatal') return story;
  const lang = story.language;
  for (let round = 1; round <= 2; round++) {
    const gaps = styleGaps(story, lang);
    if (gaps.length === 0) break;
    console.log(`  [style] ${tag} 第${round}轮修复 ${gaps.length} 项: ${gaps.map(g => g.label).join(' / ')}`);
    // 一次调用让模型按所有缺口补写：传全文 + 缺口清单，返回修正后的完整 content
    const fixPrompt = buildStyleFixPrompt(lang, ageInfo, story, gaps);
    try {
      const fixed = await callAPIWithRetry(fixPrompt, tag + '-style' + round);
      const newContent = Array.isArray(fixed.content)
        ? cleanContinuationParagraphs(fixed.content)
        : [];
      if (newContent.length >= story.content.length) {
        story.content = newContent;
        story.preview = sanitizeText(fixed.preview || story.preview);
        story.moral = sanitizeText(fixed.moral || story.moral);
        if (fixed.title) story.title = sanitizeText(fixed.title);
        console.log(`  [style] ${tag} 第${round}轮修复完成 (${newContent.length} 段)`);
      } else {
        console.log(`  [style] ${tag} 修复返回段数不足(${newContent.length}<${story.content.length})，保留原文`);
        break;
      }
    } catch (e) {
      console.error(`  [style] ${tag} 修复失败: ${e.message}`);
      break;
    }
  }
  return story;
}

// 风格修复 prompt：携全文 + 缺口清单，返回补全后的完整故事（分段落）
function buildStyleFixPrompt(language, ageInfo, story, gaps) {
  const paras = (story.content || []).map((p, i) => `[第${i + 1}段] ${p}`).join('\n');
  if (language === 'zh') {
    return `你是一位儿童睡前故事编辑。下面是${ageInfo.labelCn}故事《${story.title}》，请在【不改变主旨、不删减段落、不重写无关内容】的前提下，针对以下缺口做最小修改（在合适的段落中自然融入），并输出修补后的完整段落数组。

**当前故事全文（段落带序号）：**
${paras}

**需要修补的缺口：**
${gaps.map(g => '- ' + g.label + '：' + g.fix).join('\n')}

**要求：**
- 在保持情节与风格一致的前提下自然修补；不要为了补而破坏节奏。
- 弯引号缺口：把中文弯引号全部换成「」或单引号。
- 每个段落保持 80-120 字左右；段落数不变。
- 不得使用中文弯引号""，用「」或单引号。
- 保持${ageInfo.labelCn}风格：温柔、缓慢、拟声词、等待/爱/守护。

输出严格 JSON：
{
  "title": "故事标题",
  "preview": "前两句预览",
  "moral": "故事寓意",
  "content": ["第1段...", "第2段...", "第3段..."]
}`;
  }
  return `You are a children's bedtime story editor. The ${ageInfo.labelEn} story "${story.title}" below needs MINIMAL targeted fixes for the gaps listed (weave them naturally into suitable paragraphs; do NOT change the plot, do NOT delete paragraphs, do NOT rewrite unrelated content). Output the full corrected paragraph array.

**Current full story (paragraphs numbered):**
${paras}

**Gaps to fix:**
${gaps.map(g => '- ' + g.label + ': ' + g.fix).join('\n')}

**Requirements:**
- Weave fixes in naturally while keeping plot and style consistent.
- Keep each paragraph ~80-120 characters; keep the same paragraph count.
- Keep ${ageInfo.labelEn} style: gentle, slow, onomatopoeia, waiting/love/guardianship.

Output strict JSON:
{
  "title": "story title",
  "preview": "first two sentences",
  "moral": "the lesson",
  "content": ["paragraph 1...", "paragraph 2...", "paragraph 3..."]
}`;
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
        const halfPrompt = language === 'zh'
          ? buildChinesePrompt(dateStr, ageInfo) + '\n\n**重要：本次只写故事前半部分（4-6 段，每段 80-120 字）。必须停在一个让人好奇的悬念或正在进行的情节处，绝不要写出结局、收束、总结或祝福类句子（如"它完成了心愿""故事到此结束"）。让故事停留在"接下来会发生什么"的悬念上。**'
          : buildEnglishPrompt(dateStr, ageInfo) + '\n\n**IMPORTANT: For this request, write ONLY the first half of the story (4-6 paragraphs, each 80-120 characters). You MUST stop at a suspenseful moment or an ongoing plot point — do NOT write any ending, wrap-up, summary, or blessing sentences (e.g. "he completed his wish", "the end"). Leave the story hanging on "what happens next?".**';
        const firstRaw = await callAPIWithRetry(halfPrompt, tag + '-part1');

        // 第二段：续写后半部分并收尾，拼接成完整故事
        const contRaw = await callAPIWithRetry(
          buildContinuationPrompt(language, ageInfo, firstRaw.title, firstRaw.content, dateStr),
          tag + '-part2'
        );
        const contContent = Array.isArray(contRaw.content)
          ? cleanContinuationParagraphs(contRaw.content)
          : [];
        let merged = [...(Array.isArray(firstRaw.content) ? firstRaw.content : []), ...contContent];
        // 代码级自检：中文去全历史重复段（兜底，避免续写循环复读）；英文字符集小易误伤，仅靠 prompt 约束
        if (language === 'zh') {
          merged = dedupeAdjacentParagraphs(merged);
        }
        raw = { ...firstRaw, content: merged };
      }

      const story = buildStoryObj(raw, dateStr, language, ageInfo, category || 'regular');

      // 胎教期风格自检 + AI 定向修复（拟声词/妈妈心跳/未出生视角/弯引号）
      if (story.ageGroup === 'prenatal') {
        await ensurePrenatalStyle(story, ageInfo, dateStr, tag);
      }

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
