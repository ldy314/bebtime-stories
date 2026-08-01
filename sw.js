/**
 * Service Worker - 离线缓存 + 快速加载
 * 缓存策略:
 * - index.html: NetworkFirst (优先网络，保证最新)
 * - stories.json: StaleWhileRevalidate (缓存+后台更新)
 * - 静态资源: CacheFirst (长期缓存)
 */

const CACHE_NAME = 'bedtime-stories-v1';
const STATIC_CACHE = 'bedtime-static-v1';

// 预缓存核心文件
const PRECACHE_URLS = [
  '/',
  '/index.html',
  '/stories.json',
  '/storyline-data.json'
];

// 安装: 预缓存核心文件
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(PRECACHE_URLS);
    }).then(() => self.skipWaiting())
  );
});

// 激活: 清理旧缓存
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.filter(key => key !== CACHE_NAME && key !== STATIC_CACHE)
          .map(key => caches.delete(key))
      );
    }).then(() => self.clients.claim())
  );
});

// 拦截请求
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // 不处理非GET请求
  if (request.method !== 'GET') return;

  // 不处理chrome扩展等
  if (url.protocol !== 'http:' && url.protocol !== 'https:') return;

  // stories.json: StaleWhileRevalidate
  if (url.pathname.includes('stories.json') || url.pathname.includes('storyline-data.json')) {
    event.respondWith(staleWhileRevalidate(request, CACHE_NAME));
    return;
  }

  // index.html: NetworkFirst
  if (url.pathname === '/' || url.pathname.includes('.html')) {
    event.respondWith(networkFirst(request, CACHE_NAME));
    return;
  }

  // CDN资源: CacheFirst
  if (url.hostname.includes('jsdelivr.net') || url.hostname.includes('github')) {
    event.respondWith(cacheFirst(request, STATIC_CACHE));
    return;
  }

  // 其他: NetworkFirst
  event.respondWith(networkFirst(request, CACHE_NAME));
});

// NetworkFirst策略
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
    // 返回离线页面
    if (request.headers.get('Accept')?.includes('text/html')) {
      return new Response('<!DOCTYPE html><html><body><h1>离线模式</h1><p>请检查网络连接后重试</p></body></html>', {
        headers: { 'Content-Type': 'text/html' }
      });
    }
    return new Response('Offline', { status: 503 });
  }
}

// StaleWhileRevalidate策略
async function staleWhileRevalidate(request, cacheName) {
  const cached = await caches.match(request);
  
  const networkPromise = fetch(request).then(response => {
    if (response.ok) {
      caches.open(cacheName).then(cache => cache.put(request, response.clone()));
    }
    return response;
  }).catch(() => cached);

  return cached || networkPromise;
}

// CacheFirst策略
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

// 后台同步 (用于未来可能的离线操作)
self.addEventListener('sync', event => {
  if (event.tag === 'sync-stories') {
    event.waitUntil(syncStories());
  }
});

async function syncStories() {
  const cache = await caches.open(CACHE_NAME);
  const response = await fetch('/stories.json');
  if (response.ok) {
    await cache.put('/stories.json', response);
  }
}
