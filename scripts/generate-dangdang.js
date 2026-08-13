#!/usr/bin/env node
/**
 * generate-dangdang.js
 * 黑猫当当历险记 · 每周一集自动生成（云端 GitHub Actions 调用）
 *
 * 流程：
 *   1. 读 dangdang-series-state.json（下一集编号 / 前情 continuity / 当前 arc）
 *   2. 读 series-dangdang-guide.md（系列圣经：角色 / 写作规则 / 主题库 / 灵感池）
 *   3. 判断是否该生成：距 lastGeneratedDate >= 7 天（补生成最近一个周六）
 *   4. 用 DeepSeek 生成下一集 JSON（title/preview/moral/content + meta.continuityNote）
 *   5. 入库：追加 stories.json → 重写 index.html EMBEDDED_STORIES → 更新 state → 重建 collection.html
 *   6. 由 workflow 的 commit+push 步骤推送
 *
 * 不占用每日故事名额（条目带 series:'dangdang'）。
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const ROOT = path.join(__dirname, '..');
const STATE_PATH = path.join(ROOT, 'dangdang-series-state.json');
const GUIDE_PATH = path.join(ROOT, 'series-dangdang-guide.md');
const STORIES_PATH = path.join(ROOT, 'stories.json');
const INDEX_PATH = path.join(ROOT, 'index.html');

const API_KEY = process.env.DEEPSEEK_API_KEY;
const API_HOST = 'api.deepseek.com';
const API_PATH = '/v1/chat/completions';
const MODEL = 'deepseek-chat';
const MAX_TOKENS = 4096;

// getUTCDay() 返回 0=周日 … 6=周六，数组顺序须对齐
const WEEKDAYS = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];

// ===== 工具 =====
function callAPI(userPrompt, systemPrompt) {
  return new Promise((resolve, reject) => {
    const requestData = JSON.stringify({
      model: MODEL,
      messages: [
        { role: 'system', content: systemPrompt || 'You are a creative children\'s serialized story writer. You always respond with valid JSON.' },
        { role: 'user', content: userPrompt }
      ],
      response_format: { type: 'json_object' },
      temperature: 0.85,
      max_tokens: MAX_TOKENS
    });
    const options = {
      hostname: API_HOST, path: API_PATH, method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Length': Buffer.byteLength(requestData)
      }
    };
    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', c => body += c);
      res.on('end', () => {
        if (res.statusCode !== 200) { reject(new Error(`API ${res.statusCode}: ${body.substring(0, 400)}`)); return; }
        try {
          const content = JSON.parse(body).choices?.[0]?.message?.content;
          resolve(JSON.parse(content));
        } catch (e) { reject(new Error('parse: ' + e.message)); }
      });
    });
    req.on('error', reject);
    req.write(requestData);
    req.end();
  });
}

async function callAPIWithRetry(prompt, label, systemPrompt) {
  for (let i = 1; i <= 3; i++) {
    try { return await callAPI(prompt, systemPrompt); }
    catch (e) {
      console.log(`  [retry ${i}/3] ${label}: ${e.message}`);
      if (i === 3) throw e;
      await new Promise(r => setTimeout(r, 5000));
    }
  }
}

function beijingDateStr(offsetDays = 0) {
  const d = new Date(Date.now() + 8 * 3600 * 1000 + offsetDays * 86400 * 1000);
  return d.toISOString().slice(0, 10);
}

function latestSaturdayOnOrBefore(dateStr) {
  // 用 UTC 午夜构造，避免时区导致 getUTCDay 偏移一天（北京日期=UTC 日期部分）
  const d = new Date(dateStr + 'T00:00:00Z');
  while (d.getUTCDay() !== 6) { d.setUTCDate(d.getUTCDate() - 1); }
  return d.toISOString().slice(0, 10);
}

function sanitizeText(t) {
  if (typeof t !== 'string') return t;
  return t.replace(/\u201c/g, '\u300c').replace(/\u201d/g, '\u300d').replace(/\u2018/g, "'").replace(/\u2019/g, "'");
}

function getAgeInfo(dateStr) {
  const b = new Date('2026-09-22T00:00:00+08:00');
  const c = new Date(dateStr + 'T00:00:00+08:00');
  if (c < b) return { group: 'prenatal', label: '胎教期' };
  const diff = (c - b) / 86400000 / 365.25;
  if (diff < 1) return { group: '0-1', label: '0-1岁' };
  if (diff < 3) return { group: '1-3', label: '1-3岁' };
  if (diff < 6) return { group: '3-6', label: '3-6岁' };
  return { group: '6+', label: '6岁以上' };
}

// ===== 主流程 =====
async function main() {
  if (!API_KEY) {
    console.error('ERROR: DEEPSEEK_API_KEY not set.');
    process.exit(1);
  }

  console.log('=== 黑猫当当历险记 · 每周生成 ===');

  const state = JSON.parse(fs.readFileSync(STATE_PATH, 'utf8'));
  const guide = fs.readFileSync(GUIDE_PATH, 'utf8');
  const stories = JSON.parse(fs.readFileSync(STORIES_PATH, 'utf8'));

  // 目标日：最近一个周六
  const targetDate = latestSaturdayOnOrBefore(beijingDateStr());
  const episode = state.episode;
  const newId = `dangdang-ep${String(episode).padStart(2, '0')}-zh`;

  // 判断是否该生成：距上次 >= 7 天，且该集不存在
  const lastGen = state.lastGeneratedDate || '1970-01-01';
  const daysSince = Math.floor((new Date(targetDate + 'T00:00:00Z') - new Date(lastGen + 'T00:00:00Z')) / 86400000);
  const alreadyExists = stories.some(s => s.id === newId);
  if (alreadyExists) {
    console.log(`SKIP: ${newId} 已存在，无需生成。`);
    return;
  }
  if (daysSince < 7) {
    console.log(`SKIP: 距上次生成仅 ${daysSince} 天（<7），本周已生成过（目标日 ${targetDate}）。`);
    return;
  }

  console.log(`准备生成 ${newId}，目标日 ${targetDate}（距上次 ${daysSince} 天）`);

  // 前情（最近 3 条 + 当前 arc）
  const recentContinuity = (state.continuity || []).slice(-3).join('\n');
  const arcInfo = state.arc ? `当前故事线：${state.arc.current}（自第${state.arc.startedEpisode}集起）：${state.arc.description || ''}` : '';

  const y = targetDate.slice(0, 4);
  const m = targetDate.slice(5, 7);
  const d = targetDate.slice(8, 10);
  const weekday = WEEKDAYS[new Date(targetDate + 'T00:00:00Z').getUTCDay()];
  const age = getAgeInfo(targetDate);

  const prompt = `请为「黑猫当当历险记」系列创作第 ${episode} 集（中文，连载轻冒险）。这是每周一集的固定连载，与每日睡前故事无关。

【系列创作指南（务必遵守）】
${guide}

【当前系列状态】
- 下一集编号：ep${episode}
- 本集日期：${y}年${m}月${d}日 ${weekday}（年龄阶段：${age.label}）
- ${arcInfo}
- 最近几集前情（承接用，开头可用一两句上集回顾）：
${recentContinuity}

【本集任务】
1. 从指南「待写集数灵感池」（🟢常州本地优先）或「主题库」中选一个方向，注意避免与最近几集主题重复。
2. 若延续当前故事线（${state.arc ? state.arc.current : '无'}），要自然推进；若要收束并开启新线，要交代清楚。
3. 遵守指南的全部硬约束：主角当当每集必出、落点回「听爸爸妈妈的话」或「保护宝宝」、无暴力、无蟹、不用中文弯引号、结尾回到宝宝身边收束。

【输出格式（严格 JSON，不要其他文字）】
{
  "title": "故事名（不含「第N集」）",
  "preview": "前两句话（可含上集回顾承接）",
  "moral": "当集教育点（自然点出听爸爸妈妈的话或相关品质）",
  "content": ["段落1", "段落2", "段落3", "段落4", "段落5", "段落6"],
  "meta": {
    "continuityNote": "第${episode}集《故事名》：一句话剧情日志（含延续/收束的故事线 + 落点教育点）"
  }
}

要求：content 数组 5-8 段，每段 80-150 字，总阅读时长 3-6 分钟；语言温暖幽默、多拟声词（当当真声音）；胎教期（若当前）用第三人称温柔叙事讲给肚里宝宝听。`;

  console.log('调用 DeepSeek 生成...');
  const ep = await callAPIWithRetry(prompt, `dangdang-ep${episode}`, 'You are a warm, humorous Chinese children\'s serialized story writer. You write 黑猫当当历险记 episodes. Always respond with valid JSON.');

  // 净化 + 校验
  ep.title = sanitizeText(ep.title);
  ep.preview = sanitizeText(ep.preview);
  ep.moral = sanitizeText(ep.moral);
  ep.content = (Array.isArray(ep.content) ? ep.content : []).map(p => sanitizeText(String(p))).filter(p => p && p.trim());

  if (!ep.title || !ep.content || ep.content.length < 3) {
    console.error('ERROR: 生成结果不完整，跳过。', JSON.stringify(ep).slice(0, 200));
    process.exit(1);
  }

  console.log(`生成完成：《${ep.title}》 ${ep.content.length} 段 ${ep.content.join('').length} 字`);

  // 入库
  const obj = {
    id: newId,
    date: `${y}年${m}月${d}日 · ${weekday}`,
    dateShort: `${m}/${d}`,
    title: ep.title,
    language: 'zh',
    ageGroup: age.group,
    ageLabel: age.label,
    preview: ep.preview,
    moral: ep.moral,
    content: ep.content,
    series: 'dangdang',
    seriesTitle: '黑猫当当历险记',
    episode
  };
  stories.push(obj);
  fs.writeFileSync(STORIES_PATH, JSON.stringify(stories, null, 2), 'utf8');
  console.log(`APPENDED ${newId} -> stories.json (total ${stories.length})`);

  // 更新 index.html EMBEDDED_STORIES
  const html = fs.readFileSync(INDEX_PATH, 'utf8');
  const lines = html.split('\n');
  const idx = lines.findIndex(l => l.trim().startsWith('const EMBEDDED_STORIES = '));
  if (idx === -1) { console.error('ERROR: EMBEDDED_STORIES line not found'); process.exit(1); }
  lines[idx] = 'const EMBEDDED_STORIES = ' + JSON.stringify(stories) + ';';
  fs.writeFileSync(INDEX_PATH, lines.join('\n'), 'utf8');
  console.log('UPDATED index.html EMBEDDED_STORIES');

  // 更新 state
  state.episode = episode + 1;
  state.lastGeneratedDate = targetDate;
  const meta = ep.meta || {};
  const note = meta.continuityNote || `第${episode}集《${ep.title}》`;
  state.continuity = state.continuity || [];
  state.continuity.push(note);
  if (meta.arc) {
    state.arc = { current: meta.arc, startedEpisode: episode, description: meta.arcDesc || '' };
  }
  if (meta.linkageNote) {
    state.linkages = state.linkages || [];
    state.linkages.push(meta.linkageNote);
  }
  fs.writeFileSync(STATE_PATH, JSON.stringify(state, null, 2), 'utf8');
  console.log(`UPDATED state -> next episode ${state.episode}`);

  // 重建合集
  const { execSync } = require('child_process');
  try {
    execSync('node scripts/generate-collection-html.js', { cwd: ROOT, stdio: 'inherit' });
    console.log('REGENERATED collection.html');
  } catch (e) {
    console.error('WARN: generate-collection-html.js failed:', e.message);
  }

  console.log(`DONE episode ${episode}《${ep.title}》 dated ${targetDate}`);
}

main().catch(e => { console.error('FAIL:', e.message); process.exit(1); });
