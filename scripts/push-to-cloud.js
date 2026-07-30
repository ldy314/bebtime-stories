#!/usr/bin/env node
/**
 * push-to-cloud.js
 * 本地兜底生成后调用：把 H5 中新增的故事同步回 GitHub 仓库并推送，
 * 确保云端与本地最终一致（单源记录）。
 *
 * 同步真实数据文件 stories.json 与 index.html；
 * 当 stories.json 真有变化时，额外用仓库自带脚本重生成 collection.html 一并推送，
 * 保证 GitHub Pages（合集页）与 stories.json 始终一致，避免「故事已更新但合集页陈旧」的缺口。
 */
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// 优先使用仓库内相对路径（镜像环境），缺失时回退到原 WorkBuddy 绝对路径
function resolvePath(preferred, fallback) {
  try { return fs.existsSync(preferred) ? preferred : fallback; }
  catch (e) { return fallback; }
}

const REPO = resolvePath(path.join(__dirname, '..', 'github-pages'),
                         'C:/Users/Administrator/WorkBuddy/Claw/github-bedtime-stories');
const H5 = resolvePath(path.join(__dirname, '..'),
                       'C:/Users/Administrator/WorkBuddy/Claw/bedtime-story-app');

function run(cmd, cwd, allowFail) {
  try {
    execSync(cmd, { cwd, stdio: 'inherit' });
    return true;
  } catch (e) {
    if (!allowFail) throw e;
    console.error('[warn]', cmd, 'failed:', e.message);
    return false;
  }
}

// run() returns true on exit 0, false (caught) on non-zero.
// `git diff --quiet` exits 0 when NO diff, non-zero when diff exists ⇒ hasChanges ⇔ run()===false
function hasStagedChanges(pathspec) {
  return run(`git diff --staged --quiet ${pathspec ? '-- ' + pathspec : ''}`, REPO, true) === false;
}

// 1. 先快进拉取，避免与云端新提交分叉
run('git pull --ff-only', REPO, true);

// 2. 镜像 H5 -> repo（真实数据文件）
fs.copyFileSync(path.join(H5, 'stories.json'), path.join(REPO, 'stories.json'));
fs.copyFileSync(path.join(H5, 'index.html'), path.join(REPO, 'index.html'));
run('git add stories.json index.html', REPO);

// 3. 若故事数据真有变化，重生成合集页并一起暂存
if (hasStagedChanges('stories.json')) {
  console.log('[info] stories.json changed → regenerating collection.html');
  run(`"${process.execPath}" scripts/generate-collection-html.js`, REPO);
  run('git add collection.html', REPO);
}

// 4. 仅当确有暂存改动才提交推送
if (hasStagedChanges()) {
  run('git commit -m "sync: local fallback stories merged into cloud"', REPO);
  run('git push', REPO);
  console.log('PUSHED_TO_CLOUD');
} else {
  console.log('[info] no real data change, skip push.');
  run('git reset', REPO, true);
}
