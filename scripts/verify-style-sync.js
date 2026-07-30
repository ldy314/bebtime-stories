/**
 * verify-style-sync.js
 * Drift guard: ensure STORY_STYLE_GUIDE.md (local generation spec) stays
 * consistent with the enriched style definitions in GitHub's prompt-builder.js.
 *
 * Reads prompt-builder.js as TEXT (no export required), extracts the theme
 * pool names and core author-style markers, then asserts every one of them
 * appears in STORY_STYLE_GUIDE.md.
 *
 * Exit code: 0 = in sync (prints STYLE_SYNC_OK); 1 = drift detected.
 */

const fs = require('fs');
const path = require('path');

// 优先使用仓库内相对路径（镜像环境），缺失时回退到原 WorkBuddy 绝对路径
function resolvePath(preferred, fallback) {
  try { return fs.existsSync(preferred) ? preferred : fallback; }
  catch (e) { return fallback; }
}

const REPO_PB = resolvePath(path.join(__dirname, '..', 'github-pages', 'scripts', 'prompt-builder.js'),
                            'C:/Users/Administrator/WorkBuddy/Claw/github-bedtime-stories/scripts/prompt-builder.js');
const GUIDE = resolvePath(path.join(__dirname, 'STORY_STYLE_GUIDE.md'),
                          'C:/Users/Administrator/WorkBuddy/automation-2026-07-16-11-56-46/STORY_STYLE_GUIDE.md');

function fail(msg) {
  console.error(msg);
  process.exit(1);
}

if (!fs.existsSync(REPO_PB)) fail('STYLE_CHECK_SKIP: prompt-builder.js not found at ' + REPO_PB + ' (run sync-from-cloud first)');
if (!fs.existsSync(GUIDE)) fail('STYLE_CHECK_SKIP: STORY_STYLE_GUIDE.md not found at ' + GUIDE);

const pb = fs.readFileSync(REPO_PB, 'utf8');
const guide = fs.readFileSync(GUIDE, 'utf8');

function extractThemeNames(blockName) {
  const block = pb.match(new RegExp(blockName + '\\s*=\\s*\\[([\\s\\S]*?)\\];'));
  if (!block) return [];
  return [...block[1].matchAll(/name:\s*'([^']+)'/g)].map((m) => m[1]);
}

const cnThemes = extractThemeNames('THEME_POOL_CN');
const enThemes = extractThemeNames('THEME_POOL_EN');

// Core author-style markers (stable across edits). If a style is renamed in
// prompt-builder.js this list should be updated too — but the theme check
// above catches removed/renamed themes automatically.
const styleMarkers = [
  '孙敬修', '郑渊洁', '冰波', '张秋生', '金波', '汤素兰',
  '绘本大师风', '北欧童话风', '日本童话风', '童谣', '科普叙事风', '轻松冒险风',
  'Dr. Seuss', 'Sesame Street', 'Roald Dahl', 'Mark Twain', 'Robert McCloskey',
  'Julia Donaldson', 'Oliver Jeffers', 'Mem Fox', 'A.A. Milne', 'Beatrix Potter', 'Light adventure',
];

const missing = [];
for (const t of cnThemes) if (!guide.includes(t)) missing.push('CN theme: ' + t);
for (const t of enThemes) if (!guide.includes(t)) missing.push('EN theme: ' + t);
for (const m of styleMarkers) if (!guide.includes(m)) missing.push('style marker: ' + m);

if (missing.length) {
  console.log('STYLE_DRIFT_DETECTED');
  missing.forEach((x) => console.log('  - ' + x));
  console.log('ACTION: align STORY_STYLE_GUIDE.md with github-bedtime-stories/scripts/prompt-builder.js');
  process.exit(1);
}

console.log('STYLE_SYNC_OK cnThemes=' + cnThemes.length + ' enThemes=' + enThemes.length + ' markers=' + styleMarkers.length);
process.exit(0);
