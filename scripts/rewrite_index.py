# -*- coding: utf-8 -*-
"""Replace the entire script section of index.html with optimized version"""
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(BASE, 'index.html')

with open(INDEX, 'r', encoding='utf-8') as f:
    content = f.read()

# Find script section (from first <script> to last </script>)
first_script = content.find('<script>')
last_script_end = content.rfind('</script>') + len('</script>')

# Find the actual start of our app script (skip the CDN script)
app_script_start = content.find('<script>\n// =====')
if app_script_start == -1:
    app_script_start = first_script

new_script = r'''<script>
// ===== Service Worker 注册 =====
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('sw.js').catch(() => {});
  });
}

// ===== 数据加载（动态fetch） =====
let STORIES = [];
let STORYLINE = {};
let searchIndex = {};

async function loadStories() {
  try {
    const res = await fetch('stories.json?t=' + Date.now());
    STORIES = await res.json();
    buildSearchIndex();
  } catch (e) {
    console.error('加载stories.json失败:', e);
  }
}

async function loadStoryline() {
  try {
    const res = await fetch('storyline-data.json?t=' + Date.now());
    STORYLINE = await res.json();
  } catch (e) {
    console.warn('加载storyline-data.json失败:', e);
  }
}

// ===== 倒排索引 =====
function buildSearchIndex() {
  searchIndex = {};
  STORIES.forEach(s => {
    const text = [
      s.title || '',
      s.moral || '',
      s.preview || '',
      Array.isArray(s.content) ? s.content.join(' ') : ''
    ].join(' ');
    const words = text.toLowerCase().match(/[一-鿿]+|[a-z]+/g) || [];
    words.forEach(w => {
      if (!searchIndex[w]) searchIndex[w] = [];
      searchIndex[w].push(s.id);
    });
  });
}

// ===== 初始化 =====
(async function init() {
  await Promise.all([loadStories(), loadStoryline()]);
  window.STORYLINE_DATA = STORYLINE;
  renderStoryList();
})();

// ===== 渲染故事列表 =====
function renderStoryList() {
  const container = document.getElementById('storyList');
  const emptyEl = document.getElementById('emptyState');
  if (!container) return;
  const filtered = getFilteredStories();
  if (filtered.length === 0) {
    container.innerHTML = '';
    if (emptyEl) emptyEl.style.display = 'block';
    return;
  }
  if (emptyEl) emptyEl.style.display = 'none';
  container.innerHTML = filtered.map(s => `
    <div class="story-card fade-in" onclick="openStory('${s.id}')">
      <div class="story-card-header">
        <div class="story-card-title">${esc(s.title)}</div>
        <div class="story-card-date">${esc(s.dateShort || '')}</div>
      </div>
      <div class="story-card-preview">${esc(s.preview || '')}</div>
      <div class="story-card-footer">
        <span class="age-tag">${esc(s.ageLabel || '')}</span>
        <span class="lang-tag ${s.language}">${s.language === 'zh' ? '中文' : 'EN'}</span>
      </div>
    </div>
  `).join('');
}

function getFilteredStories() {
  let result = [...STORIES];
  const ageFilter = document.querySelector('.tab.active')?.getAttribute('data-age');
  if (ageFilter && ageFilter !== 'all') {
    result = result.filter(s => s.ageGroup === ageFilter);
  }
  const seriesFilter = document.querySelector('.tab.active')?.getAttribute('data-series');
  if (seriesFilter === 'dangdang') {
    result = result.filter(s => s.id?.startsWith('dangdang') || (s.title && s.title.includes('当当')));
  } else if (seriesFilter === 'science') {
    result = result.filter(s => s.title && (s.title.includes('科学') || s.title.includes('🔬')));
  }
  return result;
}

function esc(str) {
  const d = document.createElement('div');
  d.textContent = str || '';
  return d.innerHTML;
}

// ===== 打开故事 =====
function openStory(id) {
  const story = STORIES.find(s => s.id === id);
  if (!story) return;
  document.getElementById('readingTitleBar').textContent = story.title;
  const el = document.getElementById('readingContent');
  const paras = Array.isArray(story.content)
    ? story.content.map(p => '<p>' + esc(p) + '</p>').join('')
    : '<p>' + esc(story.content) + '</p>';
  const py = document.getElementById('pinyinToggle')?.classList.contains('active') ? 'has-pinyin' : '';
  el.innerHTML = '<div class="reading-date">' + esc(story.date || '') + '</div>'
    + '<div class="reading-title">' + esc(story.title) + '</div>'
    + '<div class="reading-badges"><span class="age-tag">' + esc(story.ageLabel || '') + '</span>'
    + '<span class="lang-tag ' + story.language + '">' + (story.language === 'zh' ? '中文' : 'EN') + '</span></div>'
    + '<div class="reading-divider">✦ ✦ ✦</div>'
    + '<div class="reading-body lang-' + story.language + ' ' + py + '">' + paras + '</div>'
    + '<div class="reading-moral"><div class="reading-moral-title">📖 故事小语</div>'
    + '<div class="reading-moral-text ' + py + '">' + esc(story.moral || '') + '</div></div>'
    + '<div class="reading-footer">🌛 晚安，做个好梦</div>';
  document.getElementById('readingPage').classList.add('active');
  window.scrollTo(0, 0);
  if (py && window.pinyinPro) applyPinyin();
}

// ===== 拼音 =====
function applyPinyin() {
  const body = document.querySelector('.reading-body');
  if (!body || !window.pinyinPro) return;
  body.querySelectorAll('p').forEach(p => {
    const text = p.textContent;
    const py = window.pinyinPro.pinyin(text, { toneType: 'none', type: 'array' });
    const chars = text.split('');
    let html = '';
    chars.forEach((c, i) => {
      if (/[一-鿿]/.test(c)) html += '<ruby>' + c + '<rt>' + (py[i] || '') + '</rt></ruby>';
      else html += c;
    });
    p.innerHTML = html;
  });
}

// ===== 事件绑定 =====
document.addEventListener('DOMContentLoaded', () => {
  // 拼音开关
  const pt = document.getElementById('pinyinToggle');
  pt?.addEventListener('click', () => {
    pt.classList.toggle('active');
    const body = document.querySelector('.reading-body');
    if (!body) return;
    body.classList.toggle('has-pinyin', pt.classList.contains('active'));
    const mt = document.querySelector('.reading-moral-text');
    if (mt) mt.classList.toggle('has-pinyin', pt.classList.contains('active'));
    if (pt.classList.contains('active')) applyPinyin();
    else {
      const title = document.getElementById('readingTitleBar').textContent;
      const s = STORIES.find(x => x.title === title);
      if (s) openStory(s.id);
    }
  });

  // 返回
  document.getElementById('backBtn')?.addEventListener('click', () => {
    document.getElementById('readingPage').classList.remove('active');
  });

  // Tab切换
  document.querySelectorAll('.tabs .tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.tab.active').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const sp = document.getElementById('storylinePage');
      if (tab.getAttribute('data-tab') === 'storyline') {
        sp?.classList.add('active');
        document.querySelector('.main')?.style.setProperty('display', 'none');
        renderStorylinePage();
      } else {
        sp?.classList.remove('active');
        document.querySelector('.main')?.style.setProperty('display', '');
        renderStoryList();
      }
    });
  });

  // 素材库导航
  document.querySelectorAll('.storyline-nav-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.storyline-nav-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const sec = btn.getAttribute('data-section');
      document.querySelectorAll('.storyline-section').forEach(s => s.classList.remove('active'));
      document.getElementById('sec-' + sec)?.classList.add('active');
    });
  });

  // 搜索面板
  const si = document.getElementById('searchInput');
  const sp = document.getElementById('searchPanel');
  const spi = document.getElementById('searchPanelInput');
  document.getElementById('searchBack')?.addEventListener('click', () => sp?.classList.remove('active'));
  si?.addEventListener('click', () => { sp?.classList.add('active'); spi?.focus(); });
  spi?.addEventListener('input', () => performSearch(spi.value));
  document.querySelectorAll('.filter-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      performSearch(spi?.value || '');
    });
  });
});

function performSearch(query) {
  const results = document.getElementById('searchResults');
  const stats = document.getElementById('searchStats');
  const filter = document.querySelector('.filter-chip.active')?.getAttribute('data-filter') || 'all';
  if (!query.trim()) { results.innerHTML = ''; stats.textContent = ''; return; }
  const kw = query.toLowerCase();
  let matched = [];
  if (filter === 'all' || ['title', 'content', 'moral'].includes(filter)) {
    STORIES.forEach(s => {
      let hit = false; let snip = '';
      if (filter === 'all' || filter === 'title') {
        if (s.title?.toLowerCase().includes(kw)) { hit = true; snip = s.title; }
      }
      if (!hit && (filter === 'all' || filter === 'content')) {
        const cs = Array.isArray(s.content) ? s.content.join(' ') : '';
        const i = cs.toLowerCase().indexOf(kw);
        if (i >= 0) { hit = true; snip = cs.substring(Math.max(0, i - 20), i + 60); }
      }
      if (!hit && (filter === 'all' || filter === 'moral')) {
        const i = (s.moral || '').toLowerCase().indexOf(kw);
        if (i >= 0) { hit = true; snip = (s.moral || '').substring(Math.max(0, i - 10), i + 50); }
      }
      if (hit) matched.push({ type: 'story', title: s.title, snippet: snip, date: s.dateShort, id: s.id });
    });
  }
  if (filter === 'all' || filter === 'character') {
    (STORYLINE.characters || []).forEach(c => {
      if (c.name?.toLowerCase().includes(kw) || c.species?.toLowerCase().includes(kw) || (c.desc || '').toLowerCase().includes(kw))
        matched.push({ type: 'character', title: c.name + ' (' + c.species + ')', snippet: c.desc });
    });
  }
  if (filter === 'all' || filter === 'destination') {
    (STORYLINE.destinations || []).forEach(d => {
      if (d.name?.toLowerCase().includes(kw) || (d.desc || '').toLowerCase().includes(kw))
        matched.push({ type: 'destination', title: d.name, snippet: d.desc });
    });
  }
  if (matched.length === 0) {
    stats.textContent = '找到 0 条结果';
    results.innerHTML = '<div class="search-empty"><div class="emoji">😅</div><p>没有找到相关故事</p></div>';
    return;
  }
  stats.textContent = '找到 ' + matched.length + ' 条结果';
  results.innerHTML = matched.map(m => {
    const tl = m.type === 'story' ? '📖 故事' : m.type === 'character' ? '🐱 角色' : '🗺️ 目的地';
    const hl = (m.snippet || '').replace(new RegExp('(' + kw.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi'), '<mark>$1</mark>');
    const ck = m.type === 'story' ? 'onclick="openStory(\'' + m.id + '\'); closeSearchPanel();"' : '';
    return '<div class="search-result-item" ' + ck + '><div class="search-result-title">' + tl + ' ' + esc(m.title) + '</div>'
      + '<div class="search-result-snippet">...' + hl + '...</div>'
      + (m.date ? '<div class="search-result-meta"><span style="font-size:12px;color:var(--text-lighter)">' + esc(m.date) + '</span></div>' : '')
      + '</div>';
  }).join('');
}

function closeSearchPanel() { document.getElementById('searchPanel')?.classList.remove('active'); }

function renderStorylinePage() {
  const cg = document.getElementById('charGrid');
  if (cg && STORYLINE.characters) {
    cg.innerHTML = STORYLINE.characters.map(c =>
      '<div class="char-card"><div class="char-icon">' + esc(c.icon || '🐱') + '</div>'
      + '<div class="char-name">' + esc(c.name) + '</div><div class="char-species">' + esc(c.species) + '</div>'
      + '<div class="char-status ' + (c.status === 'active' ? 'active' : 'pending') + '">'
      + (c.status === 'active' ? '已登场' : '待登场') + '</div></div>'
    ).join('');
  }
  const dl = document.getElementById('destList');
  if (dl && STORYLINE.destinations) {
    dl.innerHTML = STORYLINE.destinations.map(d =>
      '<div class="dest-card" style="border-left-color:' + (d.border || '#f0b850') + '">'
      + '<div class="dest-header"><div class="dest-name">' + esc(d.name) + '</div>'
      + '<div class="dest-type">' + esc(d.type) + '</div></div>'
      + '<div class="dest-desc">' + esc(d.desc) + '</div></div>'
    ).join('');
  }
  const al = document.getElementById('archiveList');
  if (al && STORYLINE.archive) {
    al.innerHTML = STORYLINE.archive.map(a =>
      '<div class="archive-item"><div class="archive-ep">ep' + a.ep + '</div>'
      + '<div class="archive-info"><div class="archive-title">' + esc(a.title) + '</div>'
      + '<div class="archive-theme">' + esc(a.theme) + '</div></div></div>'
    ).join('');
  }
  const tt = document.getElementById('themeTags');
  if (tt && STORYLINE.themes) {
    tt.innerHTML = STORYLINE.themes.map(t => '<span class="theme-tag">' + esc(t) + '</span>').join('');
  }
  const sl = document.getElementById('styleList');
  if (sl && STORYLINE.artStyles) {
    sl.innerHTML = STORYLINE.artStyles.map((s, i) =>
      '<div class="style-card"><div class="style-num">' + (i + 1) + '</div><div>' + esc(s) + '</div></div>'
    ).join('');
  }
}

// ===== 下拉刷新 =====
let touchStartY = 0;
let isRefreshing = false;
document.addEventListener('touchstart', (e) => { touchStartY = e.touches[0].clientY; });
document.addEventListener('touchmove', (e) => {
  const sy = window.scrollY;
  const cy = e.touches[0].clientY;
  if (sy === 0 && cy - touchStartY > 80 && !isRefreshing) {
    isRefreshing = true;
    loadStories().finally(() => { setTimeout(() => { isRefreshing = false; }, 1000); });
  }
});
</script>'''

# Replace from app_script_start to last_script_end
content = content[:app_script_start] + new_script + content[last_script_end:]

with open(INDEX, 'w', encoding='utf-8') as f:
    f.write(content)

print('Done! New script length:', len(new_script))
