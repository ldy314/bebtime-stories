const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const i = html.indexOf('const EMBEDDED_STORIES = [');
const s = i + 26;
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
console.log('Array ends at char:', ei);
console.log('Context:', JSON.stringify(html.substring(ei-5, ei+15)));
const arr = JSON.parse(html.substring(s, ei + 1));
console.log('Count:', arr.length);
console.log('Daily:', arr.filter(x => !x.series).length);
console.log('Series:', arr.filter(x => x.series).length);
