/**
 * Service Worker - 离线缓存 + 快速加载
 * 缓存策略:
 * - index.html: NetworkFirst (优先网络，保证最新)
 * - stories.json: StaleWhileRevalidate (缓存+后台更新)
 * - 静态资源: CacheFirst (长期缓存)
 *
 * 注意: GitHub Pages 项目站路径为 /仓库名/ ，必须使用相对路径，
 * 不能用绝对路径 '/' (会指向域名根导致预缓存失败)。
 */

const CACHE_NAME = 'bedtime-stories-v2';
const STATIC_CACHE = 'bedtime-static-v2';

// 预缓存核心文件 (相对路径，兼容 GitHub Pages 子目录)
const PRECACHE_URLS = [
  './',
  './index.html',
  './stories.json',
  './storyline-data.json'
];

// 安装: 预缓存核心文件 (容错，单文件失败不影响整体)
self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE_NAME);
    await Promise.allSettled(
      PRECACHE_URLS.map(url => cache.add(url).catch(() => {}))
    );
    await self.skipWaiting();
  })());
});

// 激活: 清理旧缓存
self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(
      keys.filter(key => key !== CACHE_NAME && key !== STATIC_CACHE)
        .map(key => caches.delete(key))
    );
    await self.clients.claim();
  })());
});

// 拦截请求
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // 不处理非GET请求
  if (request.method !== 'GET') return;
  // 不处理 chrome 扩展等
  if (url.protocol !== 'http:' && url.protocol !== 'https:') return;
  // 不拦截跨域 API (避免破坏第三方请求)
  if (url.hostname !== location.hostname) return;

  // stories.json / storyline-data.json: StaleWhileRevalidate
  if (url.pathname.endsWith('stories.json') || url.pathname.endsWith('storyline-data.json')) {
    event.respondWith(staleWhileRevalidate(request, CACHE_NAME));
    return;
  }

  // index.html 及站内 HTML: NetworkFirst
  if (url.pathname.endsWith('.html') || url.pathname.endsWith('/')) {
    event.respondWith(networkFirst(request, CACHE_NAME));
    return;
  }

  // CDN 资源: CacheFirst
  if (url.hostname.includes('jsdelivr.net') || url.hostname.includes('cdn')) {
    event.respondWith(cacheFirst(request, STATIC_CACHE));
    return;
  }

  // 其他站内资源: NetworkFirst
  event.respondWith(networkFirst(request, CACHE_NAME));
});

// NetworkFirst 策略
async function networkFirst(request, cacheName) {
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, response.clone());
    }
    return response;
  } catch (e) {
    const cached = await caches.match(request);
    if (cached) return cached;
    if (request.headers.get('Accept')?.includes('text/html')) {
      return new Response('<!DOCTYPE html><html><body><h1>离线模式</h1><p>请检查网络连接后重试</p></body></html>', {
        headers: { 'Content-Type': 'text/html' }
      });
    }
    return new Response('Offline', { status: 503 });
  }
}

// StaleWhileRevalidate 策略
async function staleWhileRevalidate(request, cacheName) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(request);
  const networkPromise = fetch(request).then(response => {
    if (response.ok) cache.put(request, response.clone());
    return response;
  }).catch(() => cached);
  return cached || networkPromise;
}

// CacheFirst 策略
async function cacheFirst(request, cacheName) {
  const cached = await caches.match(request);
  if (cached) return cached;
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, response.clone());
    }
    return response;
  } catch (e) {
    return cached || new Response('Not Found', { status: 404 });
  }
}
