// Verify wrong-review runtime behaviour. Usage: URL=http://127.0.0.1:8000/wrong-review/ node scripts/verify-wrong-review.mjs
import assert from 'node:assert/strict';
import { mkdir } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium, devices } from 'playwright';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, '..');
const SCREENSHOT_DIR = resolve(ROOT, 'data', 'wrong-review-verify');
const URL = process.env.URL || 'http://127.0.0.1:8000/wrong-review/';
const WRONG_BOOK_KEY = '115-chinese-cooking-b-progress-v2-wrong-book-v1';

const PROFILES = [
  {
    id: 'desktop',
    device: {
      viewport: { width: 1280, height: 900 },
      userAgent: 'Mozilla/5.0'
    }
  },
  {
    id: 'iphone-13',
    device: devices['iPhone 13']
  }
];

async function seedWrongBook(page) {
  await page.goto(URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.evaluate(key => {
    localStorage.clear();
    localStorage.setItem(key, JSON.stringify({
      q1: { missedAt: '2026-07-10T08:00:00+08:00', correctStreak: 1 },
      q2: { missedAt: '2026-07-10T08:05:00+08:00', correctStreak: 0 }
    }));
  }, WRONG_BOOK_KEY);
}

async function verifyProfile(browser, profile) {
  const context = await browser.newContext({ ...profile.device, locale: 'zh-TW' });
  const page = await context.newPage();
  const errors = [];
  const requests = [];

  page.on('pageerror', error => errors.push(`[pageerror] ${error.message}`));
  page.on('console', message => {
    if (message.type() === 'error') errors.push(`[console.error] ${message.text()}`);
  });
  page.on('request', request => {
    const url = request.url();
    if (url.includes('/course-data.js')) requests.push(url);
  });

  await seedWrongBook(page);
  await page.goto(URL, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForSelector('.wrong-card', { timeout: 10000 });

  const cards = page.locator('.wrong-card');
  await assertCount(cards, 2, `${profile.id}: should render seeded wrong cards`);

  const loadedCourseScripts = requests.filter(url => url.includes('/course-data.js'));
  assert.equal(loadedCourseScripts.length, 1, `${profile.id}: should load only one course-data.js`);
  assert.ok(
    loadedCourseScripts[0].includes('/115-chinese-cooking-b/course-data.js'),
    `${profile.id}: loaded unexpected course-data.js ${loadedCourseScripts[0]}`
  );

  const stats = await page.evaluate(() => ({
    total: document.querySelector('#totalCount')?.textContent,
    source: document.querySelector('#sourceCount')?.textContent,
    visible: document.querySelector('#visibleCount')?.textContent,
    options: [...document.querySelectorAll('#sourceFilter option')].map(option => option.value)
  }));
  assert.deepEqual(stats, {
    total: '2',
    source: '1',
    visible: '2',
    options: ['all', '115-chinese-cooking-b/']
  }, `${profile.id}: stats/source filter mismatch`);

  await page.locator('#searchInput').fill('不存在的查詢字串');
  await page.waitForFunction(() => document.querySelector('#visibleCount')?.textContent === '0');
  await assertCount(page.locator('.wrong-card'), 0, `${profile.id}: search should hide non-matches`);

  await page.locator('#searchInput').fill('');
  await page.waitForFunction(() => document.querySelector('#visibleCount')?.textContent === '2');
  await assertCount(cards, 2, `${profile.id}: clearing search should restore cards`);

  await page.locator('.learned-btn').first().click();
  await page.waitForFunction(() => document.querySelector('#totalCount')?.textContent === '1');
  const remainingWrongBook = await page.evaluate(key => JSON.parse(localStorage.getItem(key)), WRONG_BOOK_KEY);
  assert.equal(Object.keys(remainingWrongBook).length, 1, `${profile.id}: mark learned should persist removal`);

  const overflow = await page.evaluate(() => ({
    scrollWidth: document.documentElement.scrollWidth,
    innerWidth: window.innerWidth
  }));
  assert.ok(overflow.scrollWidth <= overflow.innerWidth, `${profile.id}: horizontal overflow ${overflow.scrollWidth} > ${overflow.innerWidth}`);

  await mkdir(SCREENSHOT_DIR, { recursive: true });
  await page.screenshot({ path: resolve(SCREENSHOT_DIR, `${profile.id}-wrong-review.png`), fullPage: false });

  assert.equal(errors.length, 0, `${profile.id} console/page errors:\n${errors.join('\n')}`);
  await context.close();
}

async function assertCount(locator, expected, message) {
  const actual = await locator.count();
  assert.equal(actual, expected, message);
}

const browser = await chromium.launch({ headless: true });
try {
  for (const profile of PROFILES) {
    await verifyProfile(browser, profile);
    console.log(`${profile.id}: passed`);
  }
  console.log('wrong-review verification passed');
} finally {
  await browser.close();
}
