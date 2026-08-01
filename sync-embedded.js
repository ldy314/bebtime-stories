const fs = require('fs');
const path = require('path');

const STORIES_FILE = path.join(__dirname, 'stories.json');
const HTML_FILE = path.join(__dirname, 'index.html');

// Read stories.json
const stories = JSON.parse(fs.readFileSync(STORIES_FILE, 'utf8'));
console.log('stories.json:', stories.length, 'stories');

// Read index.html
let html = fs.readFileSync(HTML_FILE, 'utf8');

// Find EMBEDDED_STORIES = [
const marker = 'const EMBEDDED_STORIES = [';
const startIdx = html.indexOf(marker);
if (startIdx === -1) {
  console.error('ERROR: EMBEDDED_STORIES not found');
  process.exit(1);
}

// Find end of array ];  handling strings properly
let depth = 1; // we're already inside the outer [
let inStr = false;
let esc = false;
let endIdx = -1;

for (let i = startIdx + marker.length; i < html.length; i++) {
  const ch = html[i];
  if (esc) { esc = false; continue; }
  if (ch === '\\' && inStr) { esc = true; continue; }
  if (ch === '"') { inStr = !inStr; continue; }
  if (inStr) continue;
  if (ch === '[') depth++;
  if (ch === ']') {
    depth--;
    if (depth === 0) { endIdx = i; break; }
  }
}

if (endIdx === -1) {
  console.error('ERROR: End of EMBEDDED_STORIES not found');
  process.exit(1);
}

console.log('EMBEDED_STORIES range:', startIdx, '->', endIdx);
console.log('After end:', JSON.stringify(html.substring(endIdx, endIdx + 10)));

// Generate replacement
const newArr = JSON.stringify(stories, null, 2);
const before = html.substring(0, startIdx);
const after = html.substring(endIdx + 1); // skip the ]
html = before + marker + newArr + ';\n' + after;

// Write back
fs.writeFileSync(HTML_FILE, html, 'utf8');
console.log('Done! New file size:', html.length, 'bytes');
