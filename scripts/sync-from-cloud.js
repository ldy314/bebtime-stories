#!/usr/bin/env node
/**
 * sync-from-cloud.js
 * 本地自动化第一步：把 GitHub 仓库（云端唯一生成源）的内容同步到本地 H5。
 * - git pull --ff-only 拉取云端生成的故事
 * - 镜像 repo 的 stories.json / index.html 到 H5 阅读器
 * - 重新生成合集 HTML 与合集 MD
 * - 复制合集 HTML 到部署目录
 * 输出：SYNC_PULLED_NEW（云端有本地没有的新故事）或 SYNC_NO_CHANGE
 */
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const REPO = 'C:/Users/Administrator/WorkBuddy/Claw/github-bedtime-stories';
const H5 = 'C:/Users/Administrator/WorkBuddy/Claw/bedtime-story-app';
const AUTO = 'C:/Users/Administrator/WorkBuddy/automation-2026-07-16-11-56-46';

function run(cmd, cwd) {
  execSync(cmd, { cwd, stdio: 'inherit' });
}
function countStories(p) {
  return JSON.parse(fs.readFileSync(p, 'utf8')).length;
}

// 1. 拉取云端（安全：仅快进，绝不合并）
const before = countStories(path.join(H5, 'stories.json'));
try {
  run('git pull --ff-only', REPO);
} catch (e) {
  console.error('[warn] git pull failed, using current repo state:', e.message);
}

// 2. 镜像 repo -> H5
fs.copyFileSync(path.join(REPO, 'stories.json'), path.join(H5, 'stories.json'));
fs.copyFileSync(path.join(REPO, 'index.html'), path.join(H5, 'index.html'));

const after = countStories(path.join(H5, 'stories.json'));
const pulledNew = after > before;

// 3. 重新生成合集 HTML（脚本读 H5 stories.json）
run(`node "${path.join(AUTO, 'generate-collection-html.js')}"`, AUTO);
fs.copyFileSync(
  path.join(AUTO, 'bedtime-story-collection.html'),
  path.join(AUTO, 'collection-deploy', 'index.html')
);

// 4. 重新生成合集 MD
run(`node "${path.join(AUTO, 'generate-collection-md.js')}"`, AUTO);

console.log(pulledNew ? 'SYNC_PULLED_NEW' : 'SYNC_NO_CHANGE');
