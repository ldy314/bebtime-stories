#!/usr/bin/env node
/**
 * generate-collection-md.js
 * 从 H5 的 stories.json 全量重新生成 bedtime-story-collection.md（保持表头）。
 * 每日故事与「黑猫当当历险记」系列分开成两个板块。
 */
const fs = require('fs');
const path = require('path');

const STORIES_PATH = path.join(process.cwd(), 'stories.json');
const MD_PATH = path.join(process.cwd(), 'bedtime-story-collection.md');

const stories = JSON.parse(fs.readFileSync(STORIES_PATH, 'utf8'));

// 每日故事 + 科学故事（科学故事带 series:'science'，需一并纳入合集，保持与 stories.json 一致）
const daily = stories.filter(s => !s.series || s.series === 'science');
const series = stories.filter(s => s.series === 'dangdang');

// 按日期排序（早->晚），同日 cn 在前
daily.sort((a, b) => {
  if (a.id.slice(0, 10) !== b.id.slice(0, 10)) return a.id.slice(0, 10).localeCompare(b.id.slice(0, 10));
  return a.language === 'en' ? 1 : -1;
});
// 系列按集数排序
series.sort((a, b) => (a.episode || 0) - (b.episode || 0));

function headingOf(s) {
  const m = s.date.match(/(\d+)月(\d+)日/);
  const md = m ? `${m[1]}月${m[2]}日` : s.dateShort;
  const sci = (s.series === 'science') ? '🔬 ' : '';
  return `${sci}${md} — ${s.title}`;
}
function anchorOf(heading) {
  return heading.replace(' — ', '--');
}

const HEADER = `# 🌛 睡前故事合集

> 适合胎教与儿童睡前阅读 · 语言温和易懂 · 每篇约3-5分钟
> 另有连载系列《黑猫当当历险记》（每周一集），见文末专属板块。

---

## 目录

`;

const toc = daily.map((s, i) => `${i + 1}. [${headingOf(s)}](#${anchorOf(headingOf(s))})`).join('\n');

const body = daily.map(s => {
  const h = headingOf(s);
  const paras = (s.content || []).join('\n\n');
  const moral = s.moral ? `\n**寓意：** ${s.moral}` : '';
  return `## ${h}\n\n**${s.date}**\n\n${paras}${moral}`;
}).join('\n\n---\n\n');

// 系列板块
let seriesSection = '';
if (series.length) {
  const sToc = series.map((s, i) => `${i + 1}. [${headingOf(s)}](#${anchorOf(headingOf(s))})`).join('\n');
  const sBody = series.map(s => {
    const h = headingOf(s);
    const paras = (s.content || []).join('\n\n');
    const moral = s.moral ? `\n**故事小语：** ${s.moral}` : '';
    const src = s.source ? `\n\n> 📚 灵感来源：${s.source}` : '';
    return `## ${h}\n\n**${s.date}** · 🐱 黑猫当当历险记${src}\n\n${paras}${moral}`;
  }).join('\n\n---\n\n');
  seriesSection = `\n\n---\n\n## 🐱 黑猫当当历险记（系列连载）\n\n> 一只调皮的小黑猫当当，和姐姐白猫小不点、哥哥狸花猫八百，在爸爸妈妈的家里上演一集又一集温柔又好玩的冒险。每集都悄悄告诉孩子：要听爸爸妈妈的话。\n\n### 系列目录\n\n${sToc}\n\n---\n\n${sBody}`;
}

const out = HEADER + toc + '\n\n---\n\n' + body + seriesSection + '\n';
fs.writeFileSync(MD_PATH, out, 'utf8');
console.log(`Generated collection.md with ${daily.length} daily + ${series.length} series stories.`);
