#!/usr/bin/env node
/**
 * sync_series_cloud.js
 * 黑猫当当系列自动化第4步调用：把本集更新后的真实数据同步到 GitHub 仓库并推送，
 * 同时镜像到 D 盘备份目录，确保云端、本地、备份三方一致。
 *
 * 复制文件：stories.json / index.html / collection.html（仓库内重生成）
 *         + 系列文件：dangdang-series-state.json / series-dangdang-guide.md
 *                      / apply_series_episode.py / sync_series_cloud.js
 */
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const REPO = 'D:/code test/睡前故事/github-pages';
const H5 = 'C:/Users/Administrator/WorkBuddy/Claw/bedtime-story-app';
const BACK = 'D:/code test/睡前故事';
const ME = __dirname; // automation 文件夹

function run(cmd) {
  try {
    execSync(cmd, { cwd: REPO, stdio: 'inherit' });
    return true;
  } catch (e) {
    console.error('[warn]', cmd, 'failed:', e.message);
    return false;
  }
}
function cp(src, dst) {
  try {
    fs.copyFileSync(src, dst);
    console.log('copied', src, '->', dst);
  } catch (e) {
    console.error('[warn] copy failed', src, e.message);
  }
}

// 1. 快进拉取，避免分叉
run('git pull --ff-only');

// 2. 镜像 H5 真实数据 -> repo
cp(path.join(H5, 'stories.json'), path.join(REPO, 'stories.json'));
cp(path.join(H5, 'index.html'), path.join(REPO, 'index.html'));

// 3. 重生成合集页（仓库自带生成器读 H5 stories.json）
run('node scripts/generate-collection-html.js');

// 4. 复制系列文件
cp(path.join(ME, 'dangdang-series-state.json'), path.join(REPO, 'dangdang-series-state.json'));
cp(path.join(ME, 'series-dangdang-guide.md'), path.join(REPO, 'series-dangdang-guide.md'));
cp(path.join(ME, 'apply_series_episode.py'), path.join(REPO, 'apply_series_episode.py'));
cp(path.join(ME, 'sync_series_cloud.js'), path.join(REPO, 'sync_series_cloud.js'));

// 5. 镜像到 D 盘备份
cp(path.join(H5, 'stories.json'), path.join(BACK, 'stories.json'));
cp(path.join(H5, 'index.html'), path.join(BACK, 'index.html'));
cp(path.join(REPO, 'bedtime-story-collection.html'), path.join(BACK, 'bedtime-story-collection.html'));
cp(path.join(REPO, 'dangdang-series-state.json'), path.join(BACK, 'dangdang-series-state.json'));
cp(path.join(REPO, 'series-dangdang-guide.md'), path.join(BACK, 'series-dangdang-guide.md'));
cp(path.join(ME, 'apply_series_episode.py'), path.join(BACK, 'scripts', 'apply_series_episode.py'));
cp(path.join(ME, 'sync_series_cloud.js'), path.join(BACK, 'scripts', 'sync_series_cloud.js'));
const mdSrc = path.join(REPO, '..', 'bedtime-story-collection.md');
if (fs.existsSync(mdSrc)) cp(mdSrc, path.join(BACK, 'bedtime-story-collection.md'));

// 6. 提交推送
run('git add -A');
run('git commit -m "series: 黑猫当当历险记 update"');
run('git push');
console.log('SERIES_PUSHED');
