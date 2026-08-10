#!/usr/bin/env node
// scripts/refresh-seeds.js — 月度素材扩充脚本（方案A+B+C）
//
// 方案A：预留池解锁（由 getUnlockedSeeds 自动处理，此处仅日志）
// 方案B：外部RSS抓取当月热门话题，提取关键词/主题
// 方案C：AI分析近期故事，生成补充种子列表
//
// 用法：
//   node scripts/refresh-seeds.js --all             # 执行全部方案
//   node scripts/refresh-seeds.js --fetch-external  # 仅外部抓取（方案B）
//   node scripts/refresh-seeds.js --ai-analyze      # 仅AI分析（方案C）
//   node scripts/refresh-seeds.js --batch-only      # 仅方案A（预留池解锁）

const fs = require('fs');
const path = require('path');
const https = require('https');

const ROOT_DIR = path.join(__dirname, '..');
const DYNAMIC_SEEDS_PATH = path.join(__dirname, 'dynamic-seeds.json');
const LOG_PATH = path.join(__dirname, 'seed-refresh-log.json');
const STORIES_PATH = path.join(ROOT_DIR, 'stories.json');

// ===== 基础工具函数 =====

/**
 * 安全读取 JSON 文件，不存在或解析失败时返回默认值
 */
function readJsonSafe(p, def) {
  try {
    if (!fs.existsSync(p)) return def;
    return JSON.parse(fs.readFileSync(p, 'utf-8'));
  } catch (e) {
    console.warn(`  警告：读取 ${path.basename(p)} 失败：${e.message}`);
    return def;
  }
}

/**
 * 写入 JSON 文件（带换行结尾）
 */
function writeJson(p, obj) {
  fs.writeFileSync(p, JSON.stringify(obj, null, 2) + '\n', 'utf-8');
}

/**
 * 获取当前月份字符串（YYYY-MM）
 */
function getCurrentMonth() {
  const now = new Date();
  return `${now.getUTCFullYear()}-${String(now.getUTCMonth() + 1).padStart(2, '0')}`;
}

/**
 * 去重：从 incoming 中过滤掉 existing 已存在的项（trim 后比较）
 * @returns {string[]} 去重后的新增项
 */
function dedupe(existing, incoming) {
  const seen = new Set(existing.map(s => String(s).trim()).filter(Boolean));
  const result = [];
  for (const s of incoming) {
    const trimmed = String(s).trim();
    if (!trimmed) continue;
    if (seen.has(trimmed)) continue;
    seen.add(trimmed);
    result.push(trimmed);
  }
  return result;
}

// ===== RSS 解析（复用 prompt-builder.js 逻辑） =====

/**
 * 移除 HTML 标签和实体
 */
function stripHtmlTags(s) {
  if (!s) return '';
  return String(s)
    .replace(/<[^>]+>/g, ' ')
    .replace(/&[a-z]+;/gi, ' ')
    .replace(/&#[0-9]+;/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

/**
 * 解析 RSS XML 为文章列表
 */
function parseRss(xml) {
  if (!xml || typeof xml !== 'string') return [];
  const items = [];
  const itemRe = /<item[\s\S]*?<\/item>/gi;
  let m;
  while ((m = itemRe.exec(xml)) !== null) {
    const block = m[0];
    const get = (tag) => {
      const r = new RegExp('<' + tag + '[^>]*>([\\s\\S]*?)<\\/' + tag + '>', 'i');
      const mm = block.match(r);
      if (!mm) return '';
      return mm[1].replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, '$1');
    };
    const title = stripHtmlTags(get('title'));
    const desc = stripHtmlTags(get('description'));
    const link = get('link').replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, '$1').trim();
    const pubDate = get('pubDate');
    if (title) items.push({ title, description: desc.slice(0, 600), link, pubDate });
  }
  return items;
}

/**
 * 简易 HTTPS GET（Promise 封装）
 */
function fetchUrl(url) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error('请求超时')), 15000);
    https.get(url, {
      headers: { 'User-Agent': 'Mozilla/5.0 (bedtime-story-bot)' }
    }, (res) => {
      if (res.statusCode !== 200) {
        clearTimeout(timer);
        reject(new Error(`HTTP ${res.statusCode}`));
        return;
      }
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        clearTimeout(timer);
        resolve(body);
      });
    }).on('error', (e) => {
      clearTimeout(timer);
      reject(e);
    });
  });
}

// ===== RSS 源配置 =====

const RSS_FEEDS = {
  zh: [
    { url: 'https://www.huanqiukexue.com/?feed=rss2', source: '环球科学' },
    { url: 'https://rsshub.app/weibo/user/1195054531', source: '博物' }
  ],
  en: [
    { url: 'https://www.scientificamerican.com/platform/syndication/rss/', source: 'Scientific American' }
  ]
};

// ===== 文本清洗 =====

/**
 * 清洗 RSS 标题，使其适合作为种子选题
 */
function cleanSeedText(text) {
  if (!text) return '';
  return String(text)
    .replace(/[\-\|｜].*$/, '')   // 移除 " - 环球科学" 等后缀
    .replace(/_.*$/, '')
    .replace(/［.*?］/g, '')
    .replace(/【.*?】/g, '')
    .replace(/\|.*$/, '')
    .replace(/^[\s,，。！？；]+/, '')
    .replace(/[\s,，。！？；]+$/, '')
    .trim();
}

// ===== 方案A：预留池解锁 =====

async function planA_batchUnlock() {
  console.log('\n=== 方案A：预留池解锁 ===');
  console.log('SEED_BATCHES 由 getUnlockedSeeds() 按当前月份自动解锁，无需额外操作。');
  const currentMonth = getCurrentMonth();
  console.log(`当前月份：${currentMonth}`);
  return { plan: 'A', added: 0, note: 'auto-unlocked at runtime' };
}

// ===== 方案B：外部 RSS 抓取 =====

async function planBFetchExternal() {
  console.log('\n=== 方案B：外部RSS抓取 ===');
  const currentMonth = getCurrentMonth();
  const dynamic = readJsonSafe(DYNAMIC_SEEDS_PATH, {});

  // 初始化当月条目
  if (!dynamic[currentMonth]) {
    dynamic[currentMonth] = {
      seeds: { zh: [], en: [] },
      sources: [],
      updatedAt: new Date().toISOString()
    };
  }

  const newSeeds = { zh: [], en: [] };
  const sources = new Set(dynamic[currentMonth].sources || []);

  for (const lang of ['zh', 'en']) {
    const feeds = RSS_FEEDS[lang] || [];
    for (const feed of feeds) {
      try {
        console.log(`  抓取 ${feed.source}...`);
        const xml = await fetchUrl(feed.url);
        const items = parseRss(xml);
        sources.add(feed.source);
        console.log(`    获取 ${items.length} 篇文章`);

        for (const item of items) {
          // 从标题提取种子
          const cleanTitle = cleanSeedText(item.title);
          if (cleanTitle && cleanTitle.length >= 4 && cleanTitle.length <= 20) {
            newSeeds[lang].push(cleanTitle);
          }
          // 从描述提取关键词组
          if (item.description) {
            const phrases = item.description
              .split(/[,，。！？；]/)
              .slice(0, 4)
              .map(p => cleanSeedText(p))
              .filter(p => p.length >= 4 && p.length <= 15);
            newSeeds[lang].push(...phrases);
          }
        }
      } catch (e) {
        console.warn(`    警告：${feed.source} 抓取失败：${e.message}`);
      }
    }
  }

  // 去重
  const existingZh = dynamic[currentMonth]?.seeds?.zh || [];
  const existingEn = dynamic[currentMonth]?.seeds?.en || [];
  const uniqueZh = dedupe(existingZh, newSeeds.zh).slice(0, 16);
  const uniqueEn = dedupe(existingEn, newSeeds.en).slice(0, 16);

  // 写入 dynamic-seeds.json
  dynamic[currentMonth].seeds.zh = [...existingZh, ...uniqueZh];
  dynamic[currentMonth].seeds.en = [...existingEn, ...uniqueEn];
  dynamic[currentMonth].sources = [...new Set([...sources])];
  dynamic[currentMonth].updatedAt = new Date().toISOString();

  writeJson(DYNAMIC_SEEDS_PATH, dynamic);
  console.log(`  新增中文种子：${uniqueZh.length} 个，英文种子：${uniqueEn.length} 个`);

  return { plan: 'B', added: uniqueZh.length + uniqueEn.length, sources: [...sources] };
}

// ===== 方案C：AI 分析近期故事 =====

async function planCAnalyzeRecentStories() {
  console.log('\n=== 方案C：AI分析近期故事 ===');

  if (!process.env.ZHIPU_API_KEY) {
    console.warn('  警告：ZHIPU_API_KEY 未设置，跳过方案C。');
    return { plan: 'C', added: 0, error: 'ZHIPU_API_KEY not set' };
  }

  const stories = readJsonSafe(STORIES_PATH, []);
  if (!Array.isArray(stories) || stories.length === 0) {
    console.log('  stories.json 为空，跳过分析。');
    return { plan: 'C', added: 0 };
  }

  // 取最近 30 天的故事
  const now = new Date();
  const thirtyDaysAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
  const recentStories = stories.filter(s => {
    if (!s.id) return false;
    const datePart = String(s.id).split('-').slice(0, 3).join('-');
    const d = new Date(datePart + 'T00:00:00Z');
    return d >= thirtyDaysAgo && d <= now;
  });

  console.log(`  最近 30 天故事数：${recentStories.length}`);
  if (recentStories.length < 3) {
    console.log('  故事数量不足（<3），跳过分析。');
    return { plan: 'C', added: 0 };
  }

  // 提取近期故事标题和题材方向
  const recentTitles = recentStories.map(s => s.title).filter(Boolean).slice(-20);
  const recentCategories = [...new Set(recentStories.map(s => s.category).filter(Boolean))];

  const analysisPrompt = `你是一个儿童睡前故事选题专家。请分析以下近期故事标题，找出未被充分覆盖的题材方向，并生成 12 个新的中文选题种子和 12 个英文选题种子。

近期故事标题：
${recentTitles.map(t => '- ' + t).join('\n')}

已覆盖的题材方向：${recentCategories.length > 0 ? recentCategories.join('、') : '暂无'}

要求：
1. 新选题应覆盖不同的题材方向，避免与已有故事重复
2. 中文种子适合儿童，长度 4-15 字，温馨有趣，风格多样
3. 英文种子适合儿童，长度 2-6 个单词
4. 不得出现螃蟹、大闸蟹、蜘蛛等儿童可能害怕的内容
5. 涵盖多种主题：自然、科学、文化、情感、想象、冒险、家庭、艺术等

请严格按照以下 JSON 格式返回（不要包含其他文字）：
{
  "zh": ["种子1", "种子2", "种子3", "种子4", "种子5", "种子6", "种子7", "种子8", "种子9", "种子10", "种子11", "种子12"],
  "en": ["seed 1", "seed 2", "seed 3", "seed 4", "seed 5", "seed 6", "seed 7", "seed 8", "seed 9", "seed 10", "seed 11", "seed 12"]
}`;

  try {
    const requestData = JSON.stringify({
      model: 'glm-4v-flash',
      messages: [
        {
          role: 'system',
          content: 'You are a children\'s story theme expert. Analyze themes and generate new story seed ideas. Always respond with valid JSON only.'
        },
        { role: 'user', content: analysisPrompt }
      ],
      response_format: { type: 'json_object' },
      temperature: 0.9,
      max_tokens: 2048
    });

    const apiResult = await new Promise((resolve, reject) => {
      const req = https.request({
        hostname: 'open.bigmodel.cn',
        path: '/api/paas/v4/chat/completions',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${process.env.ZHIPU_API_KEY}`,
          'Content-Length': Buffer.byteLength(requestData)
        }
      }, (res) => {
        let body = '';
        res.on('data', chunk => body += chunk);
        res.on('end', () => {
          if (res.statusCode !== 200) {
            reject(new Error(`API 返回 ${res.statusCode}: ${body.substring(0, 200)}`));
            return;
          }
          try {
            const response = JSON.parse(body);
            const content = response.choices?.[0]?.message?.content;
            if (!content) {
              reject(new Error('API 响应无内容'));
              return;
            }
            resolve(JSON.parse(content));
          } catch (e) {
            reject(new Error(`解析 API 响应失败：${e.message}`));
          }
        });
      });
      req.on('error', reject);
      req.write(requestData);
      req.end();
    });

    const currentMonth = getCurrentMonth();
    const dynamic = readJsonSafe(DYNAMIC_SEEDS_PATH, {});

    if (!dynamic[currentMonth]) {
      dynamic[currentMonth] = {
        seeds: { zh: [], en: [] },
        sources: [],
        updatedAt: new Date().toISOString()
      };
    }

    const existingZh = dynamic[currentMonth]?.seeds?.zh || [];
    const existingEn = dynamic[currentMonth]?.seeds?.en || [];

    const newZh = dedupe(existingZh, Array.isArray(apiResult.zh) ? apiResult.zh : []);
    const newEn = dedupe(existingEn, Array.isArray(apiResult.en) ? apiResult.en : []);

    const finalZh = newZh.slice(0, 16);
    const finalEn = newEn.slice(0, 16);

    dynamic[currentMonth].seeds.zh = [...existingZh, ...finalZh];
    dynamic[currentMonth].seeds.en = [...existingEn, ...finalEn];

    if (!dynamic[currentMonth].sources) dynamic[currentMonth].sources = [];
    if (!dynamic[currentMonth].sources.includes('Zhipu AI 分析')) {
      dynamic[currentMonth].sources.push('Zhipu AI 分析');
    }
    dynamic[currentMonth].updatedAt = new Date().toISOString();

    writeJson(DYNAMIC_SEEDS_PATH, dynamic);
    console.log(`  AI 分析新增中文种子：${finalZh.length} 个，英文种子：${finalEn.length} 个`);

    return { plan: 'C', added: finalZh.length + finalEn.length };
  } catch (e) {
    console.error(`  错误：AI 分析失败：${e.message}`);
    return { plan: 'C', added: 0, error: e.message };
  }
}

// ===== 主入口 =====

async function main() {
  const args = process.argv.slice(2);
  const mode = args[0] || '--all';

  console.log('=== 月度素材扩充脚本 ===');
  console.log(`运行时间：${new Date().toISOString()}`);
  console.log(`当前月份：${getCurrentMonth()}`);
  console.log(`模式：${mode}`);

  const results = [];

  if (mode === '--all' || mode === '--batch-only') {
    results.push(await planA_batchUnlock());
  }

  if (mode === '--all' || mode === '--fetch-external') {
    results.push(await planBFetchExternal());
  }

  if (mode === '--all' || mode === '--ai-analyze') {
    results.push(await planCAnalyzeRecentStories());
  }

  // 更新日志
  const log = readJsonSafe(LOG_PATH, []);
  log.push({
    timestamp: new Date().toISOString(),
    mode,
    results,
    totalAdded: results.reduce((sum, r) => sum + (r.added || 0), 0)
  });
  writeJson(LOG_PATH, log);

  console.log('\n=== 执行完毕 ===');
  console.log(`模式：${mode}`);
  console.log(`新增种子总数：${results.reduce((sum, r) => sum + (r.added || 0), 0)}`);
}

main().catch(err => {
  console.error('致命错误：', err);
  process.exit(1);
});
