"""
Service Worker Module for Offline Functionality
Progressive Web App features, caching strategies, and offline support
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
from flask import Blueprint, request, make_response, current_app
import logging

logger = logging.getLogger(__name__)

class ServiceWorkerManager:
    """Service Worker management for PWA features"""

    def __init__(self, app=None):
        self.app = app
        self.static_cache_name = 'android-gen-static-v1'
        self.dynamic_cache_name = 'android-gen-dynamic-v1'
        self.api_cache_name = 'android-gen-api-v1'

        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initialize with Flask app"""
        self.app = app

        # Register service worker routes
        sw_bp = Blueprint('service_worker', __name__, url_prefix='/sw')

        @sw_bp.route('/sw.js')
        def service_worker():
            """Serve the service worker JavaScript"""
            response = make_response(self.generate_service_worker())
            response.headers['Content-Type'] = 'application/javascript'
            response.headers['Cache-Control'] = 'no-cache'
            return response

        @sw_bp.route('/manifest.json')
        def web_manifest():
            """Serve the web app manifest"""
            response = make_response(self.generate_manifest())
            response.headers['Content-Type'] = 'application/manifest+json'
            return response

        @sw_bp.route('/offline')
        def offline_page():
            """Serve offline fallback page"""
            return self.generate_offline_page()

        app.register_blueprint(sw_bp)

        logger.info("Service Worker routes registered")

    def generate_service_worker(self) -> str:
        """Generate service worker JavaScript"""
        # Get static assets to cache
        static_assets = self.get_static_assets()

        sw_js = f'''
// Android App Generator Service Worker
const STATIC_CACHE = '{self.static_cache_name}';
const DYNAMIC_CACHE = '{self.dynamic_cache_name}';
const API_CACHE = '{self.api_cache_name}';

// Assets to cache immediately
const STATIC_ASSETS = {json.dumps(static_assets, indent=2)};

// API endpoints to cache
const API_ENDPOINTS = [
    '/api/templates',
    '/api/ai-suggestions',
    '/api/analytics'
];

// Install event - cache static assets
self.addEventListener('install', event => {{
    console.log('Service Worker installing...');
    event.waitUntil(
        caches.open(STATIC_CACHE)
            .then(cache => {{
                console.log('Caching static assets...');
                return cache.addAll(STATIC_ASSETS);
            }})
            .then(() => self.skipWaiting())
    );
}});

// Activate event - clean old caches
self.addEventListener('activate', event => {{
    console.log('Service Worker activating...');
    event.waitUntil(
        caches.keys().then(cacheNames => {{
            return Promise.all(
                cacheNames.map(cacheName => {{
                    if (cacheName !== STATIC_CACHE &&
                        cacheName !== DYNAMIC_CACHE &&
                        cacheName !== API_CACHE) {{
                        console.log('Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }}
                }})
            );
        }})
        .then(() => self.clients.claim())
    );
}});

// Fetch event - serve from cache or network
self.addEventListener('fetch', event => {{
    const {{ request }} = event;
    const url = new URL(request.url);

    // Handle different types of requests
    if (request.method === 'GET') {{
        if (url.pathname.startsWith('/api/')) {{
            // API requests - Network first with cache fallback
            event.respondWith(handleApiRequest(request));
        }} else if (STATIC_ASSETS.some(asset => url.pathname.endsWith(asset))) {{
            // Static assets - Cache first
            event.respondWith(handleStaticRequest(request));
        }} else {{
            // Other requests - Network first with cache fallback
            event.respondWith(handleDynamicRequest(request));
        }}
    }}
}});

// Handle API requests
async function handleApiRequest(request) {{
    try {{
        // Try network first
        const networkResponse = await fetch(request);
        if (networkResponse.ok) {{
            // Cache successful responses
            const cache = await caches.open(API_CACHE);
            cache.put(request, networkResponse.clone());
            return networkResponse;
        }}
    }} catch (error) {{
        console.log('Network failed, trying cache...');
    }}

    // Fallback to cache
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {{
        return cachedResponse;
    }}

    // Return offline response
    return new Response(
        JSON.stringify({{
            error: 'Offline',
            message: 'İnternet bağlantısı yok. Önbellekten veri yükleniyor.'
        }}),
        {{
            status: 503,
            headers: {{ 'Content-Type': 'application/json' }}
        }}
    );
}}

// Handle static asset requests
async function handleStaticRequest(request) {{
    // Try cache first
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {{
        return cachedResponse;
    }}

    // Fallback to network
    try {{
        const networkResponse = await fetch(request);
        return networkResponse;
    }} catch (error) {{
        console.log('Static asset fetch failed:', error);
        return new Response('Asset not available offline', {{ status: 503 }});
    }}
}}

// Handle dynamic requests
async function handleDynamicRequest(request) {{
    try {{
        // Try network first
        const networkResponse = await fetch(request);
        if (networkResponse.ok) {{
            // Cache for future use
            const cache = await caches.open(DYNAMIC_CACHE);
            cache.put(request, networkResponse.clone());
            return networkResponse;
        }}
    }} catch (error) {{
        console.log('Network failed, trying cache...');
    }}

    // Fallback to cache
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {{
        return cachedResponse;
    }}

    // Return offline page for navigation requests
    if (request.mode === 'navigate') {{
        const offlineResponse = await caches.match('/sw/offline');
        if (offlineResponse) {{
            return offlineResponse;
        }}
    }}

    return new Response('Offline - Content not available', {{ status: 503 }});
}}

// Background sync for offline actions
self.addEventListener('sync', event => {{
    console.log('Background sync triggered:', event.tag);

    if (event.tag === 'background-sync-projects') {{
        event.waitUntil(syncPendingProjects());
    }}
}});

// Push notifications
self.addEventListener('push', event => {{
    console.log('Push notification received');

    if (event.data) {{
        const data = event.data.json();
        const options = {{
            body: data.message || 'Yeni bildirim',
            icon: '/static/icon-192.png',
            badge: '/static/icon-192.png',
            data: data,
            actions: [
                {{
                    action: 'view',
                    title: 'Görüntüle'
                }},
                {{
                    action: 'dismiss',
                    title: 'Kapat'
                }}
            ]
        }};

        event.waitUntil(
            self.registration.showNotification(data.title || 'Android Generator', options)
        );
    }}
}});

// Notification click handler
self.addEventListener('notificationclick', event => {{
    console.log('Notification clicked:', event.action);

    event.notification.close();

    if (event.action === 'view') {{
        event.waitUntil(
            clients.openWindow(event.notification.data.url || '/')
        );
    }}
}});

// Sync pending projects when back online
async function syncPendingProjects() {{
    try {{
        const cache = await caches.open('pending-projects');
        const keys = await cache.keys();

        for (const request of keys) {{
            try {{
                await fetch(request);
                await cache.delete(request);
                console.log('Synced pending project');
            }} catch (error) {{
                console.error('Failed to sync project:', error);
            }}
        }}
    }} catch (error) {{
        console.error('Background sync failed:', error);
    }}
}}

// Cache management utilities
self.addEventListener('message', event => {{
    if (event.data && event.data.type === 'CACHE_CLEANUP') {{
        cleanupOldCaches();
    }}
}});

async function cleanupOldCaches() {{
    const cacheNames = await caches.keys();
    const validCaches = [STATIC_CACHE, DYNAMIC_CACHE, API_CACHE];

    for (const cacheName of cacheNames) {{
        if (!validCaches.includes(cacheName)) {{
            await caches.delete(cacheName);
            console.log('Cleaned up old cache:', cacheName);
        }}
    }}
}}

// Periodic cache cleanup
setInterval(cleanupOldCaches, 24 * 60 * 60 * 1000); // Daily cleanup
'''

        return sw_js

    def generate_manifest(self) -> str:
        """Generate web app manifest"""
        manifest = {
            "name": "Android App Generator",
            "short_name": "AndroidGen",
            "description": "AI-powered Android app generation platform",
            "start_url": "/",
            "display": "standalone",
            "background_color": "#0f172a",
            "theme_color": "#6366f1",
            "orientation": "portrait-primary",
            "scope": "/",
            "lang": "tr",
            "categories": ["developer", "productivity"],
            "icons": [
                {
                    "src": "/static/icon-192.png",
                    "sizes": "192x192",
                    "type": "image/png",
                    "purpose": "any maskable"
                },
                {
                    "src": "/static/icon-512.png",
                    "sizes": "512x512",
                    "type": "image/png",
                    "purpose": "any maskable"
                }
            ],
            "shortcuts": [
                {
                    "name": "New Project",
                    "short_name": "New App",
                    "description": "Create a new Android app",
                    "url": "/#generator",
                    "icons": [{"src": "/static/icon-192.png", "sizes": "192x192"}]
                },
                {
                    "name": "Templates",
                    "short_name": "Templates",
                    "description": "Browse app templates",
                    "url": "/#templates",
                    "icons": [{"src": "/static/icon-192.png", "sizes": "192x192"}]
                }
            ],
            "related_applications": [],
            "prefer_related_applications": False
        }

        return json.dumps(manifest, indent=2, ensure_ascii=False)

    def generate_offline_page(self) -> str:
        """Generate offline fallback page"""
        offline_html = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Offline - Android App Generator</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: white;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .offline-container {
            text-align: center;
            max-width: 400px;
        }
        .offline-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
            opacity: 0.7;
        }
        .offline-title {
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }
        .offline-message {
            opacity: 0.8;
            margin-bottom: 2rem;
            line-height: 1.6;
        }
        .retry-btn {
            background: #6366f1;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
            transition: background 0.3s;
        }
        .retry-btn:hover {
            background: #4f46e5;
        }
    </style>
</head>
<body>
    <div class="offline-container">
        <div class="offline-icon">📱</div>
        <h1 class="offline-title">Offline Mod</h1>
        <p class="offline-message">
            İnternet bağlantınız yok. Bazı özellikler sınırlı olabilir.
            Bağlantınız geri geldiğinde otomatik olarak senkronize edilecektir.
        </p>
        <button class="retry-btn" onclick="window.location.reload()">
            Tekrar Dene
        </button>
    </div>

    <script>
        // Check for connection restoration
        window.addEventListener('online', function() {
            window.location.reload();
        });

        // Register for background sync if supported
        if ('serviceWorker' in navigator && 'sync' in window.ServiceWorkerRegistration.prototype) {
            navigator.serviceWorker.ready.then(function(registration) {
                return registration.sync.register('background-sync-projects');
            });
        }
    </script>
</body>
</html>
        '''
        return offline_html

    def get_static_assets(self) -> List[str]:
        """Get list of static assets to cache"""
        assets = [
            '/',
            '/static/manifest.json',
            '/static/icon-192.png',
            '/static/icon-512.png',
            '/sw/offline'
        ]

        # Add CSS and JS files if they exist
        static_dir = os.path.join(self.app.root_path, 'static') if self.app else None
        if static_dir and os.path.exists(static_dir):
            for file in os.listdir(static_dir):
                if file.endswith(('.css', '.js', '.png', '.jpg', '.jpeg', '.svg', '.ico')):
                    assets.append(f'/static/{file}')

        return assets

    def generate_cache_key(self, content: str) -> str:
        """Generate cache key for content"""
        return hashlib.md5(content.encode()).hexdigest()

class PWAManager:
    """Progressive Web App management"""

    def __init__(self, service_worker_manager: ServiceWorkerManager = None):
        self.sw_manager = service_worker_manager
        self.install_prompt = None

    def get_pwa_headers(self) -> Dict[str, str]:
        """Get PWA-related HTTP headers"""
        return {
            'X-PWA-Capable': 'yes',
            'Service-Worker-Allowed': '/',
            'Cache-Control': 'public, max-age=31536000, immutable'
        }

    def should_show_install_prompt(self, user_agent: str, visit_count: int) -> bool:
        """Determine if install prompt should be shown"""
        # Show prompt for mobile devices after a few visits
        is_mobile = 'Mobile' in user_agent or 'Android' in user_agent
        return is_mobile and visit_count >= 3

    def track_pwa_metrics(self, event_type: str, data: Dict[str, Any]):
        """Track PWA usage metrics"""
        logger.info(f"PWA Event: {event_type} - {data}")

    def generate_install_script(self) -> str:
        """Generate JavaScript for PWA install prompt"""
        install_js = '''
// PWA Install Prompt Handler
let deferredPrompt;

window.addEventListener('beforeinstallprompt', (e) => {
    // Prevent the mini-infobar from appearing on mobile
    e.preventDefault();
    // Stash the event so it can be triggered later
    deferredPrompt = e;

    // Show custom install button
    showInstallButton();
});

window.addEventListener('appinstalled', (evt) => {
    // Log install event
    console.log('PWA was installed successfully');
    trackPWAMetric('installed');

    // Hide install button
    hideInstallButton();
});

function showInstallButton() {
    const installButton = document.getElementById('pwa-install-btn');
    if (installButton) {
        installButton.style.display = 'block';
        installButton.addEventListener('click', installPWA);
    }
}

function hideInstallButton() {
    const installButton = document.getElementById('pwa-install-btn');
    if (installButton) {
        installButton.style.display = 'none';
    }
}

async function installPWA() {
    if (!deferredPrompt) return;

    // Show the install prompt
    deferredPrompt.prompt();

    // Wait for the user to respond to the prompt
    const { outcome } = await deferredPrompt.userChoice;

    // Reset the deferred prompt
    deferredPrompt = null;

    // Track result
    trackPWAMetric('install_prompt_result', { outcome });
}

function trackPWAMetric(event, data = {}) {
    // Send metric to analytics
    if (typeof gtag !== 'undefined') {
        gtag('event', `pwa_${event}`, {
            event_category: 'pwa',
            event_label: JSON.stringify(data)
        });
    }

    // Send to service worker for offline tracking
    if ('serviceWorker' in navigator && 'controller' in navigator.serviceWorker) {
        navigator.serviceWorker.controller.postMessage({
            type: 'PWA_METRIC',
            event: event,
            data: data,
            timestamp: Date.now()
        });
    }
}

// Check if app is already installed
window.addEventListener('load', () => {
    if (window.matchMedia && window.matchMedia('(display-mode: standalone)').matches) {
        trackPWAMetric('running_as_pwa');
    }
});
'''
        return install_js

# Global instances
sw_manager = ServiceWorkerManager()
pwa_manager = PWAManager(sw_manager)

# Utility functions
def get_service_worker_content() -> str:
    """Get service worker JavaScript content"""
    return sw_manager.generate_service_worker()

def get_manifest_content() -> str:
    """Get web app manifest content"""
    return sw_manager.generate_manifest()

def get_offline_page_content() -> str:
    """Get offline page HTML content"""
    return sw_manager.generate_offline_page()

def is_pwa_capable(user_agent: str) -> bool:
    """Check if user agent supports PWA features"""
    pwa_browsers = ['Chrome', 'Edge', 'Safari', 'SamsungBrowser']
    return any(browser in user_agent for browser in pwa_browsers)

def register_pwa_routes(app):
    """Register PWA-related routes with Flask app"""
    sw_manager.init_app(app)