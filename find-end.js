const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const idx = html.indexOf('const EMBEDDED_STORIES');
let depth = 0, inStr = false, esc = false;
for (let i = idx + 26; i < html.length; i++) {
  const c = html[i];
  if (esc) { esc = false; continue; }
  if (c === '\\' && inStr) { esc = true; continue; }
  if (c === '"') { inStr = !inStr; continue; }
  if (inStr) continue;
  if (c === '[') depth++;
  if (c === ']') {
    depth--;
    if (depth === 0) {
      console.log('Found ] at', i, 'followed by:', JSON.stringify(html.substring(i, i + 10)));
      break;
    }
  }
}
