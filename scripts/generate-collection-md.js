#!/usr/bin/env node
/**
 * generate-collection-md.js
 * 从 H5 的 stories.json 全量重新生成 bedtime-story-collection.md（保持表头）。
 * 这样合集档案永远与 stories.json 一致，避免追加导致的重复/漂移。
 */
const fs = require('fs');
const path = require('path');

const H5 = 'C:/Users/Administrator/WorkBuddy/Claw/bedtime-story-app';
const MD_PATH = 'C:/Users/Administrator/WorkBuddy/Claw/bedtime-story-collection.md';

const stories = JSON.parse(fs.readFileSync(path.join(H5, 'stories.json'), 'utf8'));

// 按日期排序（早->晚），同日 cn 在前
stories.sort((a, b) => {
  if (a.id.slice(0, 10) !== b.id.slice(0, 10)) return a.id.slice(0, 10).localeCompare(b.id.slice(0, 10));
  return a.language === 'en' ? 1 : -1;
});

function headingOf(s) {
  const m = s.date.match(/(\d+)月(\d+)日/);
  const md = m ? `${m[1]}月${m[2]}日` : s.dateShort;
  return `${md} — ${s.title}`;
}
function anchorOf(heading) {
  return heading.replace(' — ', '--');
}

const HEADER = `# 🌛 睡前故事合集

> 适合胎教与儿童睡前阅读 · 语言温和易懂 · 每篇约3-5分钟

---

## 目录

`;

const toc = stories.map((s, i) => `${i + 1}. [${headingOf(s)}](#${anchorOf(headingOf(s))})`).join('\n');

const body = stories.map(s => {
  const h = headingOf(s);
  const paras = (s.content || []).join('\n\n');
  const moral = s.moral ? `\n**寓意：** ${s.moral}` : '';
  return `## ${h}\n\n**${s.date}**\n\n${paras}${moral}`;
}).join('\n\n---\n\n');

const out = HEADER + toc + '\n\n---\n\n' + body + '\n';
fs.writeFileSync(MD_PATH, out, 'utf8');
console.log(`Generated collection.md with ${stories.length} stories.`);
