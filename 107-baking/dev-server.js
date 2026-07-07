#!/usr/bin/env node
/**
 * dev-server.js  —  Local development server with hot-reload
 *
 * Features:
 *  - Serves all files statically from the current directory
 *  - Watches content.md → auto rebuilds course-data.js via md-to-data.js
 *  - Pushes a Server-Sent Event to all connected browsers on rebuild
 *  - Browser receives SSE → auto reloads the page
 *
 * Usage: npm run dev   (or node dev-server.js)
 * Then open: http://localhost:3456/
 *
 * GitHub Pages: just push. course-data.js is the static output.
 */

'use strict';
const http = require('http');
const net = require('net');
const fs   = require('fs');
const path = require('path');
const { build } = require('./md-to-data');

const PORT    = Number(process.env.PORT || 3456);
const ROOT    = __dirname;
const CONTENT = path.join(ROOT, 'content.md');

/* ── SSE clients registry ──────────────────────────────────────────────── */
const clients = new Set();

function broadcastReload() {
  for (const res of clients) {
    try { res.write('data: reload\n\n'); } catch(_) {}
  }
  console.log(`[dev-server] 🔁 Reload pushed to ${clients.size} client(s)`);
}

/* ── MIME types ─────────────────────────────────────────────────────────── */
const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css':  'text/css; charset=utf-8',
  '.js':   'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.md':   'text/markdown; charset=utf-8',
  '.png':  'image/png',
  '.jpg':  'image/jpeg',
  '.svg':  'image/svg+xml',
  '.ico':  'image/x-icon',
  '.pdf':  'application/pdf',
};

/* ── hot-reload injector snippet (injected into every HTML response) ─────── */
const HOT_RELOAD_SCRIPT = `
<script>
(function() {
  const es = new EventSource('/__hot');
  es.onmessage = function(e) {
    if (e.data === 'reload') {
      console.log('[hot-reload] 🔄 content.md changed — reloading...');
      location.reload();
    }
  };
  es.onerror = function() {
    // silently reconnect
  };
})();
</script>`;

/* ── HTTP server ────────────────────────────────────────────────────────── */
const server = http.createServer((req, res) => {
  const url = req.url.split('?')[0];

  // SSE endpoint
  if (url === '/__hot') {
    res.writeHead(200, {
      'Content-Type':  'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection':    'keep-alive',
      'Access-Control-Allow-Origin': '*'
    });
    res.write('retry: 2000\n\n'); // reconnect every 2s if dropped
    clients.add(res);
    req.on('close', () => clients.delete(res));
    return;
  }

  // Resolve file path
  let filePath = path.join(ROOT, url === '/' ? 'index.html' : url);

  // Directory → index.html
  if (fs.existsSync(filePath) && fs.statSync(filePath).isDirectory()) {
    filePath = path.join(filePath, 'index.html');
  }

  if (!fs.existsSync(filePath)) {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('404 Not Found: ' + url);
    return;
  }

  const ext  = path.extname(filePath).toLowerCase();
  const mime = MIME[ext] || 'application/octet-stream';

  let content = fs.readFileSync(filePath);

  // Inject hot-reload into HTML
  if (ext === '.html') {
    content = content.toString('utf8').replace('</body>', HOT_RELOAD_SCRIPT + '\n</body>');
  }

  res.writeHead(200, { 'Content-Type': mime });
  res.end(content);
});

/* ── Watcher ─────────────────────────────────────────────────────────────── */
let debounce = null;

function watchAndRebuild() {
  fs.watch(CONTENT, () => {
    clearTimeout(debounce);
    debounce = setTimeout(() => {
      console.log('[dev-server] 📝 content.md changed — rebuilding...');
      try {
        build();
        broadcastReload();
      } catch(e) {
        console.error('[dev-server] ❌ Build error:', e.message);
      }
    }, 200);
  });
}

/* ── Start ───────────────────────────────────────────────────────────────── */
// Initial build
try {
  build();
} catch(e) {
  console.warn('[dev-server] ⚠️  Initial build error:', e.message);
}

function findAvailablePort(startPort, attemptsLeft = 10) {
  return new Promise((resolve, reject) => {
    const tester = net.createServer()
      .once('error', err => {
        if (err.code === 'EADDRINUSE' && attemptsLeft > 0) {
          resolve(findAvailablePort(startPort + 1, attemptsLeft - 1));
        } else {
          reject(err);
        }
      })
      .once('listening', () => {
        tester.close(() => resolve(startPort));
      })
      .listen(startPort);
  });
}

findAvailablePort(PORT).then(port => {
  if (port !== PORT) {
    console.warn(`[dev-server] Port ${PORT} is already in use; using ${port} instead.`);
  }
  server.listen(port, () => {
    console.log('');
    console.log('Dev Server Ready');
    console.log(`Open: http://localhost:${port}/`);
    console.log('Edit content.md -> browser auto-reloads');
    console.log('Ctrl+C to stop');
    console.log('');
  });
}).catch(err => {
  console.error('[dev-server] Could not start server:', err.message);
  process.exit(1);
});

watchAndRebuild();
