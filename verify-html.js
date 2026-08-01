const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const start = html.indexOf('const EMBEDDED_STORIES = [');
const arrStart = start + 26;
let depth = 0, end = arrStart;
for (let i = arrStart; i < html.length; i++) {
  if (html[i] === '[') depth++;
  if (html[i] === ']') { depth--; if (depth === 0) { end = i; break; } }
}
const substr = html.substring(arrStart, end);
try {
  const stories = JSON.parse(substr);
  console.log('EMBEDDED_STORIES 故事数:', stories.length);
  console.log('每日故事:', stories.filter(s => !s.series).length);
  console.log('系列故事:', stories.filter(s => s.series).length);
  console.log('科学故事:', stories.filter(s => s.category === 'science').length);
} catch(e) {
  console.log('Parse error:', e.message);
  const match = e.message.match(/position (\d+)/);
  if (match) {
    const pos = parseInt(match[1]);
    console.log('Around error:', JSON.stringify(substr.substring(Math.max(0,pos-30), pos+30)));
  }
}
