const fs = require('fs');
const s = JSON.parse(fs.readFileSync('stories.json', 'utf8'));
let h = fs.readFileSync('index.html', 'utf8');
const L = h.split('\n');
let done = false;
for (let i = 0; i < L.length; i++) {
  if (L[i].trimStart().startsWith('const EMBEDDED_STORIES =')) {
    L[i] = 'const EMBEDDED_STORIES = ' + JSON.stringify(s) + ';';
    done = true;
    break;
  }
}
if (!done) throw new Error('未找到 EMBEDDED_STORIES 赋值行');
fs.writeFileSync('index.html', L.join('\n'), 'utf8');
console.log('已嵌入', s.length, '篇故事到 index.html');
