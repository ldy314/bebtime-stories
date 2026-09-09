const fs = require('fs');

const WEEK = ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'];
function weekday(y, m, d) { return WEEK[new Date(Date.UTC(y, m - 1, d)).getUTCDay()]; }

function load(p) { return JSON.parse(fs.readFileSync(p, 'utf8')); }
const news = [...load('new_part1.json'), ...load('new_part2.json')];

// 弯引号校验（合规要求：禁止中文弯引号 ""）
const BAD = /[“”]/g;
for (const s of news) {
  for (const k of ['title','preview','moral']) {
    if (BAD.test(s[k] || '')) throw new Error('弯引号违规 @ ' + s.id + ' field ' + k);
  }
  for (const para of (s.content || [])) {
    if (BAD.test(para || '')) throw new Error('弯引号违规 @ ' + s.id + ' content');
  }
}

const cur = load('stories.json');
const ids = new Set(cur.map(x => x.id));
let added = 0, skipped = 0;
for (const s of news) {
  const m = s.id.match(/(\d{4})-(\d{2})-(\d{2})-(cn|en)/);
  if (!m) throw new Error('id 格式异常: ' + s.id);
  const [, y, mo, d] = m;
  if (ids.has(s.id)) { skipped++; continue; }
  const full = {
    id: s.id,
    date: `${y}年${parseInt(mo)}月${parseInt(d)}日 · ${weekday(+y, +mo, +d)}`,
    dateShort: `${mo}/${d}`,
    title: s.title,
    language: s.language,
    ageGroup: 'prenatal',
    ageLabel: '胎教期',
    preview: s.preview,
    moral: s.moral,
    content: s.content,
    category: 'regular'
  };
  cur.push(full);
  ids.add(s.id);
  added++;
}

fs.writeFileSync('stories.json', JSON.stringify(cur, null, 2), 'utf8');
console.log(`合并完成：新增 ${added} 篇，跳过(已存在) ${skipped} 篇，当前总数 ${cur.length}`);
