

  // Cache ID version
  const cacheID = 'v1';
  // Files to precache
  const cacheFiles = [
    // HTML Files
    './index.html',
    // CSS Files
    // Image Files
    // JS Files
    './sw.js',
    './app.js',
    // Misc. Files
    './manifest.json',
  ];

  // Service Worker Install Event
  self.addEventListener('install', function(event) {
    console.log('Attempting to install service worker and cache static assets');
    event.waitUntil(
      caches.open(cacheID)
      .then(function(cache) {
        return cache.addAll(cacheFiles);
      })
      .catch(function(error) {
        console.log(`Unable to add cached assets: ${error}`);
      })
    );
  });

  // Service Worker Activate Event
  self.addEventListener('activate', function(e) {
    e.waitUntil(
      // Load up all items from cache, and check if cache items are not outdated
      caches.keys().then(function(keyList) {
        return Promise.all(keyList.map(function(key) {
          if (key !== cacheID) {
            console.log('[ServiceWorker] Removing old cache', key);
            return caches.delete(key);
          }
        }));
      })
    );
    return self.clients.claim();
  });

  self.addEventListener('fetch', function(event) {
    event.respondWith(
      caches.open(cacheID).then(function(cache) {
        return cache.match(event.request).then(function (response) {
          return response || fetch(event.request).then(function(response) {
            if (event.request.method != "POST") {
              cache.put(event.request, response.clone());
            }
            return response;
          })
          .catch(function(error) {
            console.log("error: " + error);
            return caches.match('./offline.html');
          });;
        });
      })
    );
  });
  