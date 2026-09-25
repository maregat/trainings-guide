const CACHE_NAME = 'trainings-guide-v2';
const STATIC_ASSETS = [
    '/',
    '/index.html',
    '/app.js',
    '/styles.css',
    '/manifest.json',
    '../data/exercises.json'
];

// ============================================
// Installation
// ============================================

self.addEventListener('install', (event) => {
    console.log('Service Worker: Installation gestartet...');
    
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('Service Worker: Cache erstellt, Assets werden gecacht...');
                return cache.addAll(STATIC_ASSETS)
                    .catch(() => {
                        console.log('Service Worker: Einige Assets konnten nicht gecacht werden (das ist ok)');
                    });
            })
            .then(() => self.skipWaiting())
    );
});

// ============================================
// Aktivierung
// ============================================

self.addEventListener('activate', (event) => {
    console.log('Service Worker: Aktiviert');
    
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((name) => {
                    if (name !== CACHE_NAME) {
                        console.log(`Service Worker: Alten Cache ${name} gelöscht`);
                        return caches.delete(name);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// ============================================
// Fetch: Smart Cache Strategy
// ============================================

self.addEventListener('fetch', (event) => {
    // Nur GET-Requests
    if (event.request.method !== 'GET') {
        return;
    }
    
    // Ignore Chrome extensions und Nicht-HTTP(S)
    if (!event.request.url.startsWith('http')) {
        return;
    }
    
    // Network-First für exercises.json (immer versuchen, neu zu laden)
    if (event.request.url.includes('exercises.json')) {
        event.respondWith(
            fetch(event.request)
                .then((response) => {
                    if (response && response.status === 200) {
                        // Cache die neue Version
                        const responseToCache = response.clone();
                        caches.open(CACHE_NAME).then((cache) => {
                            cache.put(event.request, responseToCache);
                        });
                        return response;
                    }
                    return response;
                })
                .catch(() => {
                    // Offline: Nutze gecachte Version
                    return caches.match(event.request)
                        .then((cachedResponse) => {
                            if (cachedResponse) {
                                return cachedResponse;
                            }
                            throw new Error('No cached data available');
                        });
                })
        );
        return;
    }
    
    // Cache-First für alle anderen Assets (HTML, CSS, JS, etc.)
    event.respondWith(
        caches.match(event.request)
            .then((cachedResponse) => {
                // Cache Hit: gebe cached response zurück
                if (cachedResponse) {
                    console.log(`Service Worker: Cache Hit - ${event.request.url}`);
                    return cachedResponse;
                }
                
                // Cache Miss: fetche von Network
                console.log(`Service Worker: Cache Miss - ${event.request.url}`);
                return fetch(event.request)
                    .then((response) => {
                        // Nur erfolgreich Responses cachen
                        if (!response || response.status !== 200 || response.type === 'error') {
                            return response;
                        }
                        
                        // Clone die Response (kann nur einmal gelesen werden)
                        const responseToCache = response.clone();
                        
                        // Cache im Hintergrund
                        caches.open(CACHE_NAME)
                            .then((cache) => {
                                cache.put(event.request, responseToCache);
                            });
                        
                        return response;
                    })
                    .catch(() => {
                        // Offline: Zeige Fallback
                        console.log(`Service Worker: Offline - ${event.request.url}`);
                        return new Response(
                            'Offline. Diese Seite ist nicht verfügbar.',
                            { status: 503, statusText: 'Offline' }
                        );
                    });
            })
    );
});
