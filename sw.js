const CACHE='jujuy-app-v1';
const ASSETS=['./','index.html','styles.css','app.js','model.js','data/schedule.json','manifest.webmanifest','icon.svg','icon-192.png','icon-512.png','docs/PROGRAMACION.md','docs/programacion.csv'];
self.addEventListener('install',event=>event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(ASSETS))));
self.addEventListener('activate',event=>event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('jujuy-app-')&&k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',event=>{const u=new URL(event.request.url);if(event.request.method!=='GET'||u.origin!==self.location.origin||u.pathname.includes('/.'))return;
 if(event.request.mode==='navigate'){const root=new URL('./',self.location.href).pathname;const appPage=u.pathname===root||u.pathname===root+'index.html';event.respondWith(fetch(event.request).catch(()=>caches.match(event.request).then(r=>r||(appPage?caches.match('./'):new Response('Sin conexión. Descarga este documento cuando tengas acceso a la red.',{status:503,headers:{'Content-Type':'text/plain; charset=utf-8'}})))));return;}
 event.respondWith(caches.match(event.request).then(cached=>cached||fetch(event.request)));
});
