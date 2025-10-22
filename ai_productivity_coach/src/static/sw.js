const CACHE = 'ai-coach-v1';
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(cache => cache.addAll(['/','/static/style.css','/static/manifest.json'])));
});
self.addEventListener('fetch', e => {
  e.respondWith(caches.match(e.request).then(r => r || fetch(e.request)));
});

<script>
if('serviceWorker' in navigator){
  navigator.serviceWorker.register('/static/sw.js').catch(()=>{})}

</script>