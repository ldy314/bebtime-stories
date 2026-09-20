#!/usr/bin/env node
/**
 * 0-1 岁故事管线（宝宝 2026-09-15 出生）
 *
 * 用法：
 *   node scripts/ai-0-1-pipeline.js test            单篇试跑（打印，不落盘）
 *   node scripts/ai-0-1-pipeline.js generate        生成 2026-09-22 ~ 09-30 每日 4 篇 -> data_0922_0930.json
 *   node scripts/ai-0-1-pipeline.js rewrite         改写 2026-09-15 ~ 09-21 已发故事 -> data_rewrite_0915_0921.json
 *
 * 直接复用 scripts/prompt-builder.js（云端风格权威源），保证与自动化一致。
 */
const fs = require('fs');
const path = require('path');
const https = require('https');
const PB = require('./prompt-builder');

const ROOT = path.join(__dirname, '..');
const KEY = fs.readFileSync(path.join(ROOT, 'zp.txt'), 'utf8').trim();
const MODEL = process.env.STORY_MODEL || 'glm-4-flash';
const HOST = 'open.bigmodel.cn';
const API_PATH = '/api/paas/v4/chat/completions';

const WEEKDAYS = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];

function fmtDate(s) {
  const [y, m, d] = s.split('-').map(Number);
  const dt = new Date(Date.UTC(y, m - 1, d));
  return `${y}年${m}月${d}日 · ${WEEKDAYS[dt.getUTCDay()]}`;
}
function fmtShort(s) {
  const [, m, d] = s.split('-').map(Number);
  return `${String(m).padStart(2, '0')}/${String(d).padStart(2, '0')}`;
}

function callAPI(userPrompt, { retries = 3, maxTokens = 2600 } = {}) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      model: MODEL,
      messages: [
        { role: 'system', content: "You are a warm children's bedtime story writer for babies aged 0-1. You always reply with valid JSON only." },
        { role: 'user', content: userPrompt }
      ],
      response_format: { type: 'json_object' },
      temperature: 0.88,
      max_tokens: maxTokens
    });
    const req = https.request({
      hostname: HOST, path: API_PATH, method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + KEY, 'Content-Length': Buffer.byteLength(body) }
    }, res => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try {
          const j = JSON.parse(data);
          if (j.error) throw new Error(JSON.stringify(j.error));
          const raw = j.choices[0].message.content;
          resolve(JSON.parse(raw));
        } catch (e) {
          const err = new Error('API/parse fail: ' + e.message + ' | ' + data.slice(0, 200));
          if (retries > 0) setTimeout(() => callAPI(userPrompt, { retries: retries - 1, maxTokens }).then(resolve, reject), 4000);
          else reject(err);
        }
      });
    });
    req.setTimeout(180000, () => req.destroy(new Error('timeout')));
    req.on('error', e => {
      if (retries > 0) setTimeout(() => callAPI(userPrompt, { retries: retries - 1, maxTokens }).then(resolve, reject), 4000);
      else reject(e);
    });
    req.write(body); req.end();
  });
}

const CURLY = /[\u201c\u201d\u2018\u2019]/g;
function fix(t) {
  return typeof t === 'string' ? t.replace(CURLY, m => ({ '\u201c': '\u300c', '\u201d': '\u300d', '\u2018': "'", '\u2019': "'" }[m])) : t;
}
function clean(o) {
  const seen = new Set();
  const paras = [];
  for (let p of (o.content || [])) {
    p = fix(String(p)).trim();
    if (!p) continue;
    const key = p.replace(/[，。！？、,.!?\s]/g, '');
    if (seen.has(key)) continue;   // 去掉整段复读
    seen.add(key);
    paras.push(p);
  }
  return {
    title: fix(o.title || '').trim(),
    preview: fix(o.preview || '').trim(),
    moral: fix(o.moral || '').trim(),
    content: paras
  };
}

function dupRate(paras) {
  const norm = paras.map(p => p.replace(/[，。！？、,.!?\s]/g, ''));
  const uniq = new Set(norm);
  return norm.length ? 1 - uniq.size / norm.length : 0;
}

function validate(o, lang = 'zh') {
  const probs = [];
  if (!o.title || !o.preview || !o.moral || !o.content.length) probs.push('字段缺失');
  if (o.content.length < 3) probs.push('段落过少:' + o.content.length);
  if (dupRate(o.content) > 0.2) probs.push('段落重复率过高');
  const minLen = lang === 'en' ? 30 : 12;
  const short = o.content.filter(p => p.replace(/[\s，。！？、,.!?]/g, '').length < minLen).length;
  if (short > 0) probs.push(`过短段落:${short}`);
  const last = (o.content[o.content.length - 1] || '').trim();
  if (!/[。！？.!?"'\u300d]$/.test(last)) probs.push('末段未收尾(疑似截断)');
  const all = o.title + o.preview + o.moral + o.content.join('');
  if (/[\u201c\u201d\u2018\u2019]/.test(all)) probs.push('含弯引号');
  if (/蟹/.test(all)) probs.push('含蟹');
  if (/等(你|宝宝)(出生|出来|长大一点)/.test(all)) probs.push('残留胎教等待措辞');
  if (/肚子里(的|还没)/.test(all)) probs.push('残留腹中措辞');
  if (/不要怕|别哭|别害怕/.test(all)) probs.push('否定式安慰');
  const total = o.content.join('').length;
  if (lang === 'en' ? total < 400 : total < 240) probs.push('总字数不足:' + total);
  return probs;
}

const ADDENDUM_CN = `

**本条追加硬性要求（优先级最高，务必遵守）：**
- content 只输出 4-6 个自然段，**每一段的内容必须彼此不同**：严禁把同一段复读两遍或多遍，严禁整段照抄前面的句子。
- 每个自然段 2-4 句，每句 5-14 个字。
- 全文自然融入 3-5 个**不同**的拟声词，让声音参与叙事（不要只用一个反复到底）。
- 故事要有微小的推进：小主角出现 → 一件温柔的小事发生 → 温柔收尾，不要原地打转。
- 标题末尾注明「（0-1岁）」。`;

const ADDENDUM_EN = `

**Extra hard requirements for this story (highest priority):**
- Output 4-6 paragraphs in "content", and **every paragraph must be different**. Never repeat or copy an entire paragraph.
- 2-4 short sentences per paragraph, each 4-12 words.
- Weave in 3-5 DIFFERENT onomatopoeia words so sound joins the telling.
- Include a tiny forward movement: little hero appears -> one gentle thing happens -> a tender ending. Do not go in circles.
- End the title with "(0-1 yr)".`;

const SCI_ADDENDUM_CN = `

**科学故事特别要求（优先级最高）：**
- 必须用完整的句子讲故事，**不要写成分行诗歌、断句列表或半句话**；每个自然段都是通顺的散文。
- 文中必须有一段明确、完整的科学讲解：让小主角好奇地问「为什么会这样呢？」，然后用两三句准确、孩子能听懂的话解答清楚。
- content 输出 4-5 个自然段，总字数 300-500 字；每一段内容必须彼此不同。
- 全文自然融入 3-5 个不同的拟声词。
- 标题以「🔬科学故事（0-1岁）：」开头。`;

const SCI_ADDENDUM_EN = `

**Extra hard requirements for this science story (highest priority):**
- Tell the story in complete prose sentences — **no line-broken poems, no fragment lists, no half sentences**.
- Include one clear, complete science explanation: the little hero asks "But why?" and then two or three accurate, baby-friendly sentences explain it.
- Output 4-5 paragraphs, total 350-600 characters; every paragraph must be different.
- Weave in 3-5 different onomatopoeia words.
- Start the title with "🔬 Science Story (0-1 yr):".`;

// ===== 生成 =====
async function genOne(dateStr, kind) {
  const age = PB.getAgeInfo(dateStr);
  let prompt, meta;
  if (kind === 'cn') {
    prompt = PB.buildChinesePrompt(dateStr, age) + ADDENDUM_CN;
    meta = { language: 'zh', category: 'regular' };
  } else if (kind === 'en') {
    prompt = PB.buildEnglishPrompt(dateStr, age) + ADDENDUM_EN;
    meta = { language: 'en', category: 'regular' };
  } else if (kind === 'sci-cn') {
    prompt = PB.buildScienceChinesePrompt(null, age, dateStr) + ADDENDUM_CN + SCI_ADDENDUM_CN;
    meta = { language: 'zh', category: 'science', series: 'science', source: '儿童科普常识' };
  } else {
    prompt = PB.buildScienceEnglishPrompt(null, age, dateStr) + ADDENDUM_EN + SCI_ADDENDUM_EN;
    meta = { language: 'en', category: 'science', series: 'science', source: 'Children science common sense' };
  }
  const lang = meta.language;
  let best = null, bestProbs = null;
  for (let attempt = 0; attempt < 3; attempt++) {
    let out;
    try { out = clean(await callAPI(prompt)); } catch (e) { if (attempt === 2) throw e; continue; }
    const probs = validate(out, lang);
    if (!best || probs.length < bestProbs.length) { best = out; bestProbs = probs; }
    if (probs.length === 0) break;
  }
  return { dateStr, kind, meta, ...best, _problems: bestProbs };
}

const sleep = ms => new Promise(r => setTimeout(r, ms));

async function runGenerate() {
  const dates = [];
  for (let d = 22; d <= 30; d++) dates.push(`2026-09-${String(d).padStart(2, '0')}`);
  const jobs = [];
  for (const dt of dates) for (const k of ['cn', 'en', 'sci-cn', 'sci-en']) jobs.push({ dt, k });

  const out = [];
  const CONC = 4;
  for (let i = 0; i < jobs.length; i += CONC) {
    const batch = jobs.slice(i, i + CONC);
    const res = await Promise.allSettled(batch.map(j => genOne(j.dt, j.k)));
    res.forEach((r, idx) => {
      const j = batch[idx];
      if (r.status === 'fulfilled') {
        const probs = r.value._problems || [];
        out.push(r.value);
        console.log(`${probs.length ? 'WARN' : 'OK  '} ${j.dt} ${j.k} | ${r.value.title}${probs.length ? ' | ' + probs.join(',') : ''}`);
      } else {
        console.log(`FAIL ${j.dt} ${j.k} | ${r.reason.message.slice(0, 120)}`);
      }
    });
    await sleep(600);
  }
  fs.writeFileSync(path.join(__dirname, 'data_0922_0930.json'), JSON.stringify(out, null, 2), 'utf8');
  console.log(`\nDONE generate: ${out.length}/${jobs.length} -> scripts/data_0922_0930.json`);
}

// ===== 改写（胎教期 -> 出生后 0-1 岁） =====
const REWRITE_SYS = `下面是一篇已经发布过的胎教期睡前故事（原本是讲给还在妈妈肚子里的小宝宝听的）。宝宝的出生日期是 2026-09-15，现在已经出生了。请把这篇故事改写为讲给「已经出生的小宝宝」听的 0-1 岁故事。

改写要求（严格执行）：
1. 保留原故事的主体情节、小主角、场景与转折，不要换故事、不要新增情节线。
2. 把所有「等待出生」类措辞改写掉：例如「等你出生」「等你准备好了」「等你长大」「你在妈妈肚子里」「肚里的宝宝」「外面的世界」等，改成对已经出生的小宝宝说话的方式（如「小宝宝，你听」「我们来看看」「你瞧」），或直接用温柔讲述口吻。
3. 语言向 0-1 岁靠拢：句子适度改短（多数 6-16 字），适当增加重复句式与拟声词（如「呼——呼——」「滴答，滴答」「咕噜，咕噜」），读起来更舒缓、有节奏，适合哄睡朗读。
4. 语气温暖、被守护；不出现危险、冲突、跌落、黑暗吞噬、分离、追赶情节；不用否定式安慰（如「不要怕」「别哭」）。
5. 结尾按原故事情境自然收束（不一定是「晚安」）。
6. 不使用中文弯引号，请用「」或普通单引号。
7. 禁止出现螃蟹、大闸蟹或任何蟹类角色/食物/情节。
8. 段落数保持与原故事相近（4-6 段），每篇总字数 300-600 字。
9. 每一段的内容必须彼此不同，严禁整段复读或照抄前面的段落。

请返回 JSON：{"title":"...","preview":"故事前两句","moral":"寓意（40字内，温柔不说教）","content":["段1","段2",...]}
中文标题请把「（胎教期）」改成「（0-1岁）」；英文标题请把 (Prenatal) 改成 (0-1 yr)。`;

async function runRewrite() {
  const src = JSON.parse(fs.readFileSync(path.join(ROOT, 'stories.json'), 'utf8'));
  const targets = src.filter(s => {
    const ds = s.dateShort || '';
    return ['09/15', '09/16', '09/17', '09/18', '09/19', '09/20', '09/21'].includes(ds);
  });
  console.log('待改写:', targets.length, '篇');
  const out = [];
  const CONC = 4;
  for (let i = 0; i < targets.length; i += CONC) {
    const batch = targets.slice(i, i + CONC);
    const res = await Promise.allSettled(batch.map(s => {
      const payload = { title: s.title, preview: s.preview, moral: s.moral, content: s.content };
      const prompt = REWRITE_SYS + '\n\n原文（JSON）：\n' + JSON.stringify(payload, null, 2);
      return callAPI(prompt, { maxTokens: 2600 });
    }));
    res.forEach((r, idx) => {
      const s = batch[idx];
      if (r.status === 'fulfilled') {
        const c = clean(r.value);
        const probs = validate(c, s.language === 'en' ? 'en' : 'zh');
        out.push({ id: s.id, dateStr: s.id.slice(0, 10), oldTitle: s.title, ...c, _problems: probs });
        console.log(`${probs.length ? 'WARN' : 'OK  '} ${s.id} | ${s.title} -> ${c.title}${probs.length ? ' | ' + probs.join(',') : ''}`);
      } else {
        console.log(`FAIL ${s.id} | ${r.reason.message.slice(0, 120)}`);
      }
    });
    await sleep(600);
  }
  fs.writeFileSync(path.join(__dirname, 'data_rewrite_0915_0921.json'), JSON.stringify(out, null, 2), 'utf8');
  console.log(`\nDONE rewrite: ${out.length}/${targets.length} -> scripts/data_rewrite_0915_0921.json`);
}

const mode = process.argv[2] || 'test';
if (mode === 'test') {
  (async () => {
    for (const k of ['cn', 'en', 'sci-cn', 'sci-en']) {
      const r = await genOne('2026-09-22', k);
      console.log('===== ' + k + ' =====');
      console.log(JSON.stringify(r, null, 2));
    }
  })().catch(e => { console.error('ERR', e.message); process.exit(1); });
} else if (mode === 'generate') {
  runGenerate().catch(e => { console.error(e); process.exit(1); });
} else if (mode === 'rewrite') {
  runRewrite().catch(e => { console.error(e); process.exit(1); });
}
