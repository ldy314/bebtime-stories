const fs = require('fs');
const path = require('path');

// 优先使用仓库内相对路径（镜像环境），缺失时回退到原 WorkBuddy 绝对路径
function resolvePath(preferred, fallback) {
  try { return fs.existsSync(preferred) ? preferred : fallback; }
  catch (e) { return fallback; }
}

// Read stories.json
const stories = JSON.parse(fs.readFileSync(
  resolvePath(path.join(__dirname, '..', 'stories.json'),
              'C:/Users/Administrator/WorkBuddy/Claw/bedtime-story-app/stories.json'), 'utf8'));

// HTML escape helper
function esc(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

// Convert story body paragraphs to HTML
// content can be a string or an array of paragraph strings
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

// Convert moral to HTML (split lines with <br>)
function moralToHtml(moral) {
  return esc(moral).replace(/\n+/g, '<br>');
}

// Get short date for TOC
function shortDate(dateStr) {
  // dateStr like "2026年7月16日 · 星期四"
  const m = dateStr.match(/(\d+)月(\d+)日/);
  if (m) return `${m[1]}月${m[2]}日`;
  return dateStr;
}

// Get language label
function langLabel(lang) {
  return lang === 'en' ? '🇬🇧 EN' : '🇨🇳 中文';
}

// Build TOC entries
const tocEntries = stories.map((s, i) => {
  const num = String(i + 1).padStart(2, '0');
  return `      <li><a href="#story-${i+1}"><span class="toc-num">${num}</span> ${esc(s.title)} <span class="toc-date">${shortDate(s.date)}</span></a></li>`;
}).join('\n');

// Build story cards
const storyCards = stories.map((s, i) => {
  const moralText = s.moral || '';
  const moralTitle = s.language === 'en' ? 'Story Lesson' : '故事小语';
  const moralIcon = '✨';
  
  return `<!-- ===== ${langLabel(s.language)} Story ${i+1} ===== -->
<div class="story-card" id="story-${i+1}">
  <div class="moon">🌙</div>
  <div class="stars">✦ ✦ ✦</div>
  <div class="story-date">${esc(s.date)}</div>
  <div class="story-title">${esc(s.title)}</div>
  <div class="story-lang-badge">${langLabel(s.language)}</div>
  ${s.category === 'science' ? `<div class="story-lang-badge" style="color:#2a9d8f;font-weight:600;margin-top:2px;">🔬 科学故事 · ${esc(s.source || '科学杂志')}</div>` : ''}
  <div class="story-divider">— ✿ —</div>

  <div class="story-body">
${bodyToHtml(s.content, i === 0)}
  </div>

  <div class="moral">
    <div class="moral-title">${moralIcon} ${moralTitle}</div>
    <div class="moral-text">
      ${moralToHtml(moralText)}
    </div>
  </div>

  <div class="story-back"><a href="#">↑ 回到目录</a></div>
</div>`;
}).join('\n\n');

// Full HTML
const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>睡前故事合集 · 星光下的温柔</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    min-height: 100vh;
    font-family: "PingFang SC", "Microsoft YaHei", "Noto Serif SC", serif;
    padding: 20px;
  }

  /* ===== 封面 ===== */
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

  /* ===== 目录 ===== */
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

  /* ===== 故事卡片 ===== */
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

  /* ===== 页脚 ===== */
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
  /* ===== 故事风格介绍 ===== */
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
</style>
</head>
<body>

<!-- ===== 封面 ===== -->
<div class="cover">
  <div class="cover-moon">🌙</div>
  <div class="cover-stars">✦ ✦ ✦</div>
  <div class="cover-emoji">🌛</div>
  <h1>星光下的温柔</h1>
  <div class="subtitle">睡前故事合集 · 中英双语</div>
  <p class="intro">
    这是一本为即将到来的宝宝准备的睡前故事集。<br>
    中文故事融合孙敬修、郑渊洁、冰波、张秋生、金波、汤素兰六位大师风格；<br>
    英文故事融合Dr. Seuss、芝麻街、Roald Dahl、Mark Twain、Robert McCloskey五位大师风格。<br>
    愿这些温柔的文字，化作星光，<br>
    轻轻落在宝宝的心上。
  </p>
  <div class="stats">
    <div class="stat">
      <div class="stat-num">${stories.length}</div>
      <div class="stat-label">篇故事</div>
    </div>
    <div class="stat">
      <div class="stat-num">${stories.filter(s => s.language === 'zh').length}</div>
      <div class="stat-label">中文</div>
    </div>
    <div class="stat">
      <div class="stat-num">${stories.filter(s => s.language === 'en').length}</div>
      <div class="stat-label">English</div>
    </div>
  </div>

  <div class="toc">
    <div class="toc-title">📖 目 录</div>
    <ul class="toc-list">
${tocEntries}
    </ul>
  </div>
</div>

<!-- ===== 故事风格介绍 ===== -->
<div class="style-intro">
  <h2>✨ 故事风格介绍</h2>
  <p>这些睡前故事，是写给正在妈妈肚子里、一天天长大的小宝贝的。随着宝宝慢慢长大，故事的语气、题材和风格会悄悄变化——像四季一样，每个阶段都有属于自己的温度。</p>
  <h4>📅 按年龄，故事会这样变</h4>
  <ul>
    <li><b>胎教期（出生前）</b>：极温柔缓慢，多用拟声词与节奏感，讲等待、爱、守护与妈妈的声音。</li>
    <li><b>0-1 岁</b>：极简短句，大量重复与拟声（动物叫、自然声），陪宝宝认识感官与世界。</li>
    <li><b>1-3 岁</b>：简单情节，小动物或日常物品当主角，聊生活习惯、情绪和友谊。</li>
    <li><b>3-6 岁</b>：完整小故事，加入对话与轻松冒险，讲勇气、分享、诚实与好奇心。</li>
    <li><b>6 岁以上</b>：更长更深，带比喻和寓意，聊成长、责任、善良与梦想。</li>
  </ul>
  <h4>🎨 故事都有哪些题材？</h4>
  <p>自然与科学启蒙 · 中国文化与传统 · 情感与心理 · 想象与奇幻 · 生活与认知 · 轻松愉快的冒险</p>
  <h4>✍️ 文字里有谁的味道？</h4>
  <p>中文故事融合孙敬修、冰波、金波、张秋生、郑渊洁、汤素兰等大师的温柔笔触；英文故事带着 Dr. Seuss 的韵律、McCloskey 的自然、Dahl 的幽默与 Sesame Street 的暖意。每天中英各一篇，陪宝宝用两种语言说晚安。</p>
  <p class="si-note">每一篇都标注了适合的年龄段。愿这些温柔的声音，成为宝宝来到世界前，最早听到的爱。</p>
</div>

${storyCards}

<!-- ===== 页脚 ===== -->
<div class="footer">
  🌙 星光下的温柔 · 睡前故事合集 · 每日更新中 🌙<br>
  <span style="font-size:11px;opacity:0.6">最后更新：${new Date().toLocaleString('zh-CN', {timeZone: 'Asia/Shanghai'})}</span>
</div>

</body>
</html>`;

// Write output
fs.writeFileSync(path.join(__dirname, 'bedtime-story-collection.html'), html, 'utf8');
console.log('Generated bedtime-story-collection.html with', stories.length, 'stories');
console.log('ZH stories:', stories.filter(s => s.language === 'zh').length);
console.log('EN stories:', stories.filter(s => s.language === 'en').length);
