const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

// Find EMBEDDED_STORIES
const marker = 'const EMBEDDED_STORIES = [';
const startIdx = html.indexOf(marker);
const arrStart = startIdx + marker.length;

// Find closing ] with proper depth tracking (start at depth=1 for outer array)
let depth = 1;
let inString = false;
let escapeNext = false;
let endIdx = -1;

for (let i = arrStart; i < html.length; i++) {
  const ch = html[i];
  
  if (escapeNext) { escapeNext = false; continue; }
  if (ch === '\\' && inString) { escapeNext = true; continue; }
  if (ch === '"') { inString = !inString; continue; }
  if (inString) continue;
  
  if (ch === '[') depth++;
  if (ch === ']') {
    depth--;
    if (depth === 0) { endIdx = i; break; }
  }
}

console.log('Start at:', startIdx);
console.log('Array starts at:', arrStart);
console.log('Array ends at:', endIdx);
console.log('Context after end:', JSON.stringify(html.substring(endIdx, endIdx + 20)));

// Try to parse
const arrStr = html.substring(arrStart, endIdx + 1);
try {
  const stories = JSON.parse(arrStr);
  console.log('SUCCESS! Stories:', stories.length);
  console.log('Daily:', stories.filter(s => !s.series).length);
  console.log('Series:', stories.filter(s => s.series).length);
  console.log('Science:', stories.filter(s => s.category === 'science').length);
} catch(e) {
  console.log('Parse error:', e.message);
  const posMatch = e.message.match(/position (\d+)/);
  if (posMatch) {
    const pos = parseInt(posMatch[1]);
    console.log('At position:', pos);
    console.log('Context:', JSON.stringify(arrStr.substring(Math.max(0, pos-20), pos+20)));
  }
}
