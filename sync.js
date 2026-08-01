const fs = require('fs');
const path = require('path');

const STORIES_FILE = path.join(__dirname, 'stories.json');
const HTML_FILE = path.join(__dirname, 'index.html');

// Read stories.json - 49 stories
const stories = JSON.parse(fs.readFileSync(STORIES_FILE, 'utf8'));
console.log('stories.json:', stories.length, 'stories');

// Read index.html
let html = fs.readFileSync(HTML_FILE, 'utf8');

// Find EMBEDDED_STORIES = [
const marker = 'const EMBEDDED_STORIES = [';
let startIdx = html.indexOf(marker);

// If not found with single [, try [[ (from previous bad edit)
if (startIdx === -1) {
  const doubleMarker = 'const EMBEDDED_STORIES = [[';
  if (html.includes(doubleMarker)) {
    console.log('Found double bracket, fixing...');
    html = html.replace(doubleMarker, marker);
    startIdx = html.indexOf(marker);
  }
}

if (startIdx === -1) {
  console.error('ERROR: EMBEDDED_STORIES not found');
  process.exit(1);
}

// Find end of array - the ]; that closes the outer array
// We need to handle strings with brackets inside them
let depth = 1;
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
  console.error('ERROR: End of array not found');
  process.exit(1);
}

// The end ]; might have extra chars like ];\n;\n - find the actual ];
while (html[endIdx + 1] === ';' || html[endIdx + 1] === '\n' || html[endIdx + 1] === '\r') {
  endIdx++;
}

console.log('Range:', startIdx, '->', endIdx);
console.log('After end:', JSON.stringify(html.substring(endIdx, endIdx + 10)));

// Generate new array string
const newArrStr = JSON.stringify(stories, null, 2);

// Replace
const before = html.substring(0, startIdx);
const after = html.substring(endIdx + 1);
html = before + marker + newArrStr + ';\n\n' + after;

// Write
fs.writeFileSync(HTML_FILE, html, 'utf8');
console.log('Synced! File size:', html.length, 'bytes');

// Verify
const checkMarker = 'const EMBEDDED_STORIES = [';
const checkStart = html.indexOf(checkMarker) + checkMarker.length;
let cd = 1, cis = false, ces = false, cei = -1;
for (let i = checkStart; i < html.length; i++) {
  const c = html[i];
  if (ces) { ces = false; continue; }
  if (c === '\\' && cis) { ces = true; continue; }
  if (c === '"') { cis = !cis; continue; }
  if (cis) continue;
  if (c === '[') cd++;
  if (c === ']') { cd--; if (cd === 0) { cei = i; break; } }
}
const arr = JSON.parse(html.substring(checkStart, cei + 1));
console.log('Verified:', arr.length, 'stories');
console.log('Daily:', arr.filter(x => !x.series).length);
console.log('Series:', arr.filter(x => x.series).length);
