#!/usr/bin/env node
/**
 * Generate collection HTML from stories.json
 * Creates a single-page HTML with all stories listed.
 * 
 * Usage: node scripts/generate-collection-html.js
 */

const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.join(__dirname, '..');
const STORIES_PATH = path.join(ROOT_DIR, 'stories.json');
const OUTPUT_PATH = path.join(ROOT_DIR, 'collection.html');

// Read stories.json
const stories = JSON.parse(fs.readFileSync(STORIES_PATH, 'utf8'));

// Split daily stories vs 黑猫当当 series
const daily = stories.filter(s => !s.series);
const series = stories.filter(s => s.series === 'dangdang');

// 去掉标题里可能带的前缀「第N集 ·」，避免与生成器添加的序号重复
const cleanTitle = t => String(t).replace(/^第\d+集\s*[·・\-]?\s*/, '');

// HTML escape helper
function esc(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

// Convert story body paragraphs to HTML
function bodyToHtml(body, isFirst) {
  let paras;
  if (Array.isArray(body)) {
    paras = body.filter(p => p && p.trim());
  } else if (typeof body === 'string') {
    paras = body.split(/\n\n+/).filter(p => p.trim());
  } else {
    paras = [];
  }
  return paras.map((p, i) => {
    const cls = (i === 0) ? ' class="first"' : '';
    return `    <p${cls}>${esc(p).replace(/\n/g, '<br>')}</p>`;
  }).join('\n\n');
}

// Convert moral to HTML
function moralToHtml(moral) {
  return esc(moral).replace(/\n+/g, '<br>');
}

// Get short date for TOC
function shortDate(dateStr) {
  const m = dateStr.match(/(\d+)\u6708(\d+)\u65e5/);
  if (m) return `${m[1]}\u6708${m[2]}\u65e5`;
  return dateStr;
}

// Get language label
function langLabel(lang) {
  return lang === 'en' ? '\uD83C\uDDEC\uD83C\uDDE7 EN' : '\uD83C\uDDE8\uD83C\uDDE9 \u4E2D\u6587';
}

// Build TOC entries
const tocEntries = daily.map((s, i) => {
  const num = String(i + 1).padStart(2, '0');
  return `      <li><a href="#story-${i+1}"><span class="toc-num">${num}</span> ${esc(s.title)} <span class="toc-date">${shortDate(s.date)}</span></a></li>`;
}).join('\n');

// Build story cards
const storyCards = daily.map((s, i) => {
  const moralText = s.moral || '';
  const moralTitle = s.language === 'en' ? 'Story Lesson' : '\u6545\u4E8B\u5C0F\u8BED';
  const moralIcon = '\u2728';

  return `<!-- ===== ${langLabel(s.language)} Story ${i+1} ===== -->
<div class="story-card" id="story-${i+1}">
  <div class="moon">\uD83C\uDF19</div>
  <div class="stars">\u2726 \u2726 \u2726</div>
  <div class="story-date">${esc(s.date)}</div>
  <div class="story-title">${esc(s.title)}</div>
  <div class="story-lang-badge">${langLabel(s.language)}</div>
  ${s.category === 'science' ? `<div class="story-lang-badge" style="color:#2a9d8f;font-weight:600;margin-top:2px;">🔬 科学故事 · ${esc(s.source || '科学杂志')}</div>` : ''}
  <div class="story-divider">\u2014 \u273F \u2014</div>

  <div class="story-body">
${bodyToHtml(s.content, i === 0)}
  </div>

  <div class="moral">
    <div class="moral-title">${moralIcon} ${moralTitle}</div>
    <div class="moral-text">
      ${moralToHtml(moralText)}
    </div>
  </div>

  <div class="story-back"><a href="#">\u2191 \u56DE\u5230\u76EE\u5F55</a></div>
</div>`;
}).join('\n\n');

// Series section (黑猫当当历险记)
const seriesTocEntries = series.map((s, i) => {
  const num = String(i + 1).padStart(2, '0');
  const ep = (s.episode != null) ? `第${s.episode}集 · ` : '';
  return `      <li><a href="#series-${i+1}"><span class="toc-num">${num}</span> ${ep}${esc(cleanTitle(s.title))} <span class="toc-date">${shortDate(s.date)}</span></a></li>`;
}).join('\n');

const seriesCards = series.map((s, i) => {
  const ep = (s.episode != null) ? `第${s.episode}集` : '';
  const epBadge = ep ? `<span class="story-lang-badge" style="color:#6b4ea0;font-weight:600;margin-top:2px;">🐱 ${ep} · 黑猫当当历险记</span>` : '';
  return `<!-- ===== 黑猫当当历险记 Story ${i+1} ===== -->
<div class="story-card" id="series-${i+1}">
  <div class="moon">🐱</div>
  <div class="stars">✦ ✦ ✦</div>
  <div class="story-date">${esc(s.date)}</div>
  <div class="story-title">${esc(cleanTitle(s.title))}</div>
  ${epBadge}
  <div class="story-divider">— ✿ —</div>

  <div class="story-body">
${bodyToHtml(s.content, i === 0)}
  </div>

  <div class="moral">
    <div class="moral-title">✨ 故事小语</div>
    <div class="moral-text">
      ${moralToHtml(s.moral || '')}
    </div>
  </div>

  <div class="story-back"><a href="#">↑ 回到目录</a></div>
</div>`;
}).join('\n\n');

let seriesBlock = '';
if (series.length) {
  seriesBlock = `
<!-- ===== 黑猫当当历险记 系列 ===== -->
<div class="cover">
  <div class="cover-moon">🐱</div>
  <div class="cover-stars">✦ ✦ ✦</div>
  <div class="cover-emoji">🐱</div>
  <div class="series-section-title">🐱 黑猫当当历险记 · 每周系列</div>
  <p class="series-section-note">每周六更新一集，不占用每日故事名额。点开听听调皮小黑猫当当的冒险吧～</p>
  <h1>黑猫当当历险记</h1>
  <div class="subtitle">每周一集 · 温暖连载</div>
  <p class="intro">一只调皮的小黑猫当当，和姐姐白猫小不点、哥哥狸花猫八百，在爸爸妈妈的家里上演一集又一集温柔又好玩的冒险。每集都悄悄告诉孩子：要听爸爸妈妈的话。</p>
  <div class="toc">
    <div class="toc-title">📖 系列目录</div>
    <ul class="toc-list">
${seriesTocEntries}
    </ul>
  </div>
</div>

${seriesCards}`;
}

// Full HTML
const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>\u7761\u524D\u6545\u4E8B\u5408\u96C6 \xB7 \u661F\u5149\u4E0B\u7684\u6E29\u67D4</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    min-height: 100vh;
    font-family: "PingFang SC", "Microsoft YaHei", "Noto Serif SC", serif;
    padding: 20px;
  }

  /* ===== Cover ===== */
  .cover {
    max-width: 680px; width: 100%; margin: 0 auto 32px;
    background: linear-gradient(135deg, #fef9f0 0%, #fff3d6 100%);
    border-radius: 24px;
    padding: 64px 40px 48px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
    position: relative;
    overflow: hidden;
    text-align: center;
  }
  .cover::before {
    content: ""; position: absolute; top: 0; left: 0; right: 0; height: 6px;
    background: linear-gradient(90deg, #a8d8ea, #ffb347, #ffcc33, #ffe082, #a8d8ea);
  }
  .cover-stars {
    position: absolute; top: 20px; right: 30px; font-size: 24px; opacity: 0.3;
  }
  .cover-moon {
    position: absolute; top: 16px; left: 30px; font-size: 32px; opacity: 0.25;
  }
  .cover-emoji { font-size: 48px; margin-bottom: 16px; }
  .cover h1 {
    font-size: 30px; color: #5c4d3c; font-weight: 700;
    letter-spacing: 4px; margin-bottom: 8px;
  }
  .cover .subtitle {
    font-size: 15px; color: #b0a08a; letter-spacing: 3px; margin-bottom: 32px;
  }
  .cover .intro {
    font-size: 15px; line-height: 2; color: #7a6550;
    max-width: 440px; margin: 0 auto 32px;
  }
  .cover .stats {
    display: flex; justify-content: center; gap: 24px; margin-bottom: 24px;
  }
  .cover .stat {
    text-align: center;
  }
  .cover .stat-num {
    font-size: 28px; font-weight: 700; color: #e8963b;
  }
  .cover .stat-label {
    font-size: 12px; color: #b0a08a; letter-spacing: 1px;
  }

  /* ===== TOC ===== */
  .toc {
    background: rgba(255,255,255,0.5);
    border-radius: 16px;
    padding: 24px;
    text-align: left;
  }
  .toc-title {
    font-size: 14px; color: #c8923a; font-weight: 600;
    letter-spacing: 2px; margin-bottom: 16px; text-align: center;
  }
  .toc-list { list-style: none; }
  .toc-list li {
    margin-bottom: 10px;
  }
  .toc-list a {
    display: flex; align-items: center; gap: 12px;
    text-decoration: none;
    padding: 10px 16px;
    border-radius: 12px;
    transition: background 0.2s;
    font-size: 15px; color: #5a4535;
  }
  .toc-list a:hover { background: rgba(255,179,71,0.15); }
  .toc-list .toc-num {
    font-size: 13px; color: #e8963b; font-weight: 700;
    min-width: 24px;
  }
  .toc-list .toc-date {
    font-size: 12px; color: #b0a08a; margin-left: auto;
  }

  /* ===== Story cards ===== */
  .story-card {
    max-width: 680px; width: 100%; margin: 0 auto 32px;
    background: #fef9f0;
    border-radius: 24px;
    padding: 48px 40px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
    position: relative;
    overflow: hidden;
  }
  .story-card::before {
    content: ""; position: absolute; top: 0; left: 0; right: 0; height: 6px;
    background: linear-gradient(90deg, #ffb347, #ffcc33, #ffe082);
  }
  .story-card .stars {
    position: absolute; top: 20px; right: 30px; font-size: 24px; opacity: 0.35;
  }
  .story-card .moon {
    position: absolute; top: 16px; left: 30px; font-size: 24px; opacity: 0.25;
  }
  .story-date {
    font-size: 13px; color: #b0a08a; text-align: center; margin-bottom: 8px;
    letter-spacing: 2px;
  }
  .story-title {
    text-align: center; color: #5c4d3c;
    font-size: 24px; font-weight: 600;
    margin-bottom: 6px; letter-spacing: 2px;
  }
  .story-lang-badge {
    text-align: center; margin-bottom: 6px;
  }
  .story-lang-badge {
    font-size: 12px; color: #b0a08a;
  }
  .story-divider {
    text-align: center; color: #d4c5a9; font-size: 14px;
    margin-bottom: 28px; letter-spacing: 4px;
  }
  .story-body {
    font-size: 17px; line-height: 2; color: #5a4535;
    text-align: justify; text-indent: 2em;
  }
  .story-body p { margin-bottom: 14px; }
  .story-body .first::first-letter {
    font-size: 30px; font-weight: bold; color: #e8963b;
  }
  .moral {
    margin-top: 32px; padding: 20px 24px;
    background: linear-gradient(135deg, #fff8e7, #fef3d6);
    border-radius: 16px; border-left: 4px solid #f0b850;
  }
  .moral-title {
    font-size: 15px; color: #c8923a; font-weight: 600;
    margin-bottom: 8px; letter-spacing: 2px;
  }
  .moral-text {
    font-size: 15px; line-height: 1.8; color: #7a6550;
  }
  .story-back {
    text-align: center; margin-top: 24px;
  }
  .story-back a {
    font-size: 13px; color: #c4b49a; text-decoration: none;
    letter-spacing: 1px;
  }
  .story-back a:hover { color: #e8963b; }

  /* ===== Footer ===== */
  .footer {
    max-width: 680px; margin: 0 auto;
    text-align: center; padding: 32px 0;
    font-size: 13px; color: rgba(255,255,255,0.4);
    letter-spacing: 2px;
  }

  @media (max-width: 600px) {
    .cover, .story-card { padding: 36px 24px; }
    .cover h1 { font-size: 24px; }
    .story-body { font-size: 16px; }
    .toc-list a { font-size: 14px; }
  }

  /* ===== Style intro ===== */
  .style-intro {
    max-width: 680px; width: 100%; margin: 0 auto 32px;
    background: #fef9f0; border-radius: 24px; padding: 40px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4); position: relative; overflow: hidden;
  }
  .style-intro::before {
    content: ""; position: absolute; top: 0; left: 0; right: 0; height: 6px;
    background: linear-gradient(90deg, #a8d8ea, #ffb347, #ffcc33);
  }
  .style-intro h2 { text-align: center; color: #5c4d3c; font-size: 22px; font-weight: 600; margin-bottom: 18px; letter-spacing: 2px; }
  .style-intro h4 { font-size: 15px; color: #c8923a; margin: 18px 0 8px; letter-spacing: 1px; }
  .style-intro h4:first-of-type { margin-top: 4px; }
  .style-intro p { font-size: 15px; line-height: 1.9; color: #5a4535; }
  .style-intro ul { margin: 0 0 8px; padding-left: 20px; }
  .style-intro li { font-size: 15px; line-height: 1.9; color: #5a4535; margin-bottom: 6px; }
  .style-intro b { color: #e8963b; }
  .style-intro .si-note { margin-top: 16px; padding-top: 14px; border-top: 1px dashed #e8dcc4; font-size: 14px; color: #7a6550; font-style: italic; text-align: center; }
  @media (max-width: 600px) { .style-intro { padding: 32px 24px; } .style-intro p, .style-intro li { font-size: 14px; } }

  /* ===== 系列分区标题 ===== */
  .series-section-title {
    max-width: 680px; width: 100%; margin: 0 auto 16px;
    text-align: center;
    font-size: 26px; font-weight: 700; letter-spacing: 3px;
    color: #6b4ea0;
    padding: 18px 0;
  }
  .series-section-note {
    max-width: 680px; width: 100%; margin: 0 auto 32px;
    text-align: center; font-size: 14px; line-height: 1.8;
    color: #8a7ba8;
  }
</style>
</head>
<body>

<!-- ===== Cover ===== -->
<div class="cover">
  <div class="cover-moon">\uD83C\uDF19</div>
  <div class="cover-stars">\u2726 \u2726 \u2726</div>
  <div class="cover-emoji">\uD83C\uDF1A</div>
  <h1>\u661F\u5149\u4E0B\u7684\u6E29\u67D4</h1>
  <div class="subtitle">\u7761\u524D\u6545\u4E8B\u5408\u96C6 \xB7 \u4E2D\u82F1\u53CC\u8BED</div>
  <p class="intro">
    \u8FD9\u662F\u4E00\u672C\u4E3A\u5373\u5C06\u5230\u6765\u7684\u5B9D\u5B9D\u51C6\u5907\u7684\u7761\u524D\u6545\u4E8B\u96C6\u3002<br>
    \u4E2D\u6587\u6545\u4E8B\u878D\u5408\u5B59\u656C\u4FEE\u3001\u90D1\u6E0A\u6D01\u3001\u51B0\u6CE2\u3001\u5F20\u79CB\u751F\u3001\u91D1\u6CE2\u3001\u6C64\u7D20\u5170\u516D\u4F4D\u5927\u5E08\u98CE\u683C\uFF1B<br>
    \u82F1\u6587\u6545\u4E8B\u878D\u5408Dr. Seuss\u3001\u829D\u9EBB\u8857\u3001Roald Dahl\u3001Mark Twain\u3001Robert McCloskey\u4E94\u4F4D\u5927\u5E08\u98CE\u683C\u3002<br>
    \u613F\u8FD9\u4E9B\u6E29\u67D4\u7684\u6587\u5B57\uFF0C\u5316\u4F5C\u661F\u5149\uFF0C<br>
    \u8F7B\u8F7B\u843D\u5728\u5B9D\u5B9D\u7684\u5FC3\u4E0A\u3002
  </p>
  <div class="stats">
    <div class="stat">
      <div class="stat-num">${daily.length}</div>
      <div class="stat-label">\u7BC7\u6545\u4E8B</div>
    </div>
    <div class="stat">
      <div class="stat-num">${daily.filter(s => s.language === 'zh').length}</div>
      <div class="stat-label">\u4E2D\u6587</div>
    </div>
    <div class="stat">
      <div class="stat-num">${daily.filter(s => s.language === 'en').length}</div>
      <div class="stat-label">English</div>
  </div>
  <div class="stat">
    <div class="stat-num">${series.length}</div>
    <div class="stat-label">系列集数</div>
  </div>
  </div>

  <div class="toc">
    <div class="toc-title">\uD83D\uDCD6 \u76EE \u5F55</div>
    <ul class="toc-list">
${tocEntries}
    </ul>
  </div>
</div>

<!-- ===== Style intro ===== -->
<div class="style-intro">
  <h2>\u2728 \u6545\u4E8B\u98CE\u683C\u4ECB\u7ECD</h2>
  <p>\u8FD9\u4E9B\u7761\u524D\u6545\u4E8B\uFF0C\u662F\u5199\u7ED9\u6B63\u5728\u5988\u5988\u809A\u5B50\u91CC\u3001\u4E00\u5929\u5929\u957F\u5927\u7684\u5C0F\u5B9D\u8D1D\u7684\u3002\u968F\u7740\u5B9D\u5B9D\u6162\u6162\u957F\u5927\uFF0C\u6545\u4E8B\u7684\u8BED\u6C14\u3001\u9898\u6750\u548C\u98CE\u683C\u4F1A\u6084\u6084\u53D8\u5316\u2014\u2014\u50CF\u56DB\u5B63\u4E00\u6837\uFF0C\u6BCF\u4E2A\u9636\u6BB5\u90FD\u6709\u5C5E\u4E8E\u81EA\u5DF1\u7684\u6E29\u5EA6\u3002</p>
  <h4>\uD83D\uDCC5 \u6309\u5E74\u9F84\uFF0C\u6545\u4E8B\u4F1A\u8FD9\u6837\u53D8</h4>
  <ul>
    <li><b>\u80CE\u6559\u671F\uFF08\u51FA\u751F\u524D\uFF09</b>\uFF1A\u6781\u6E29\u67D4\u7F13\u6162\uFF0C\u591A\u7528\u62DF\u58F0\u8BCD\u4E0E\u8282\u594F\u611F\uFF0C\u8BB2\u7B49\u5F85\u3001\u7231\u3001\u5B88\u62A4\u4E0E\u5988\u5988\u7684\u58F0\u97F3\u3002</li>
    <li><b>0-1 \u5C81</b>\uFF1A\u6781\u7B80\u77ED\u53E5\uFF0C\u5927\u91CF\u91CD\u590D\u4E0E\u62DF\u58F0\uFF08\u52A8\u7269\u53EB\u3001\u81EA\u7136\u58F0\uFF09\uFF0C\u966A\u5B9D\u5B9D\u8BA4\u8BC6\u611F\u5B98\u4E0E\u4E16\u754C\u3002</li>
    <li><b>1-3 \u5C81</b>\uFF1A\u7B80\u5355\u60C5\u8282\uFF0C\u5C0F\u52A8\u7269\u6216\u65E5\u5E38\u7269\u54C1\u5F53\u4E3B\u89D2\uFF0C\u804A\u751F\u6D3B\u4E60\u60EF\u3001\u60C5\u7EEA\u548C\u53CB\u8C0A\u3002</li>
    <li><b>3-6 \u5C81</b>\uFF1A\u5B8C\u6574\u5C0F\u6545\u4E8B\uFF0C\u52A0\u5165\u5BF9\u8BDD\u4E0E\u8F7B\u677E\u5192\u9669\uFF0C\u8BB2\u52C7\u6C14\u3001\u5206\u4EAB\u3001\u8BDA\u5B9E\u4E0E\u597D\u5947\u5FC3\u3002</li>
    <li><b>6 \u5C81\u4EE5\u4E0A</b>\uFF1A\u66F4\u957F\u66F4\u6DF1\uFF0C\u5E26\u6BD4\u55BB\u548C\u5BD3\u610F\uFF0C\u804A\u6210\u957F\u3001\u8D23\u4EFB\u3001\u5584\u826F\u4E0E\u68A6\u60F3\u3002</li>
  </ul>
  <h4>\uD83C\uDFA8 \u6545\u4E8B\u90FD\u6709\u54EA\u4E9B\u9898\u6750\uFF1F</h4>
  <p>\u81EA\u7136\u4E0E\u79D1\u5B66\u542F\u8499 \xB7 \u4E2D\u56FD\u6587\u5316\u4E0E\u4F20\u7EDF \xB7 \u60C5\u611F\u4E0E\u5FC3\u7406 \xB7 \u60F3\u8C61\u4E0E\u5947\u5E7B \xB7 \u751F\u6D3B\u4E0E\u8BA4\u77E5 \xB7 \u8F7B\u677E\u6109\u5FEB\u7684\u5192\u9669</p>
  <h4>\u270D\uFE0F \u6587\u5B57\u91CC\u6709\u8C01\u7684\u5473\u9053\uFF1F</h4>
  <p>\u4E2D\u6587\u6545\u4E8B\u878D\u5408\u5B59\u656C\u4FEE\u3001\u51B0\u6CE2\u3001\u91D1\u6CE2\u3001\u5F20\u79CB\u751F\u3001\u90D1\u6E0A\u6D01\u3001\u6C64\u7D20\u5170\u7B49\u5927\u5E08\u7684\u6E29\u67D4\u7B14\u89E6\uFF1B\u82F1\u6587\u6545\u4E8B\u5E26\u7740 Dr. Seuss \u7684\u97F5\u5F8B\u3001McCloskey \u7684\u81EA\u7136\u3001Dahl \u7684\u5E7D\u9ED8\u4E0E Sesame Street \u7684\u6696\u610F\u3002\u6BCF\u5929\u4E2D\u82F1\u5404\u4E00\u7BC7\uFF0C\u966A\u5B9D\u5B9D\u7528\u4E24\u79CD\u8BED\u8A00\u8BF4\u665A\u5B89\u3002</p>
  <p class="si-note">\u6BCF\u4E00\u7BC7\u90FD\u6807\u6CE8\u4E86\u9002\u5408\u7684\u5E74\u9F84\u6BB5\u3002\u613F\u8FD9\u4E9B\u6E29\u67D4\u7684\u58F0\u97F3\uFF0C\u6210\u4E3A\u5B9D\u5B9D\u6765\u5230\u4E16\u754C\u524D\uFF0C\u6700\u65E9\u542C\u5230\u7684\u7231\u3002</p>
</div>

${seriesBlock}

${storyCards}

<!-- ===== Footer ===== -->
<div class="footer">
  \uD83C\uDF19 \u661F\u5149\u4E0B\u7684\u6E29\u67D4 \xB7 \u7761\u524D\u6545\u4E8B\u5408\u96C6 \xB7 \u6BCF\u65E5\u66F4\u65B0\u4E2D \uD83C\uDF19<br>
  <span style="font-size:11px;opacity:0.6">\u6700\u540E\u66F4\u65B0\uFF1A${new Date().toISOString()}</span>
</div>

</body>
</html>`;

// Write output
fs.writeFileSync(OUTPUT_PATH, html, 'utf8');
console.log('Generated collection.html with', stories.length, 'stories');
console.log('ZH stories:', stories.filter(s => s.language === 'zh').length);
console.log('EN stories:', stories.filter(s => s.language === 'en').length);
