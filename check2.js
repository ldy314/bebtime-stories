const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const m = 'const EMBEDDED_STORIES = [';
const i = html.indexOf(m);
const s = i + m.length;
let d = 1, is = false, es = false, ei = -1;
for (let j = s; j < html.length; j++) {
  const c = html[j];
  if (es) { es = false; continue; }
  if (c === '\\' && is) { es = true; continue; }
  if (c === '"') { is = !is; continue; }
  if (is) continue;
  if (c === '[') d++;
  if (c === ']') { d--; if (d === 0) { ei = j; break; } }
}
const arr = JSON.parse(html.substring(s, ei + 1));
console.log('Total:', arr.length);
console.log('Daily:', arr.filter(x => !x.series).length);
console.log('Series:', arr.filter(x => x.series).length);
console.log('Science:', arr.filter(x => x.category === 'science').length);
console.log('First:', arr[0].id, arr[0].title);
console.log('Last:', arr[arr.length-1].id, arr[arr.length-1].title);
