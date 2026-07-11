// Verify the baking print tool's full-exam and compact-notes layouts.
// Usage: node scripts/verify-baking-print-layout.mjs
import assert from "node:assert/strict";
import { mkdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { chromium } from "playwright";

const here = dirname(fileURLToPath(import.meta.url));
const webRoot = resolve(here, "..");
const outputDir = resolve(webRoot, "verification", "baking-print-layout");
const url = pathToFileURL(resolve(webRoot, "100-114-baking-print", "index.html")).href;

await mkdir(outputDir, { recursive: true });
const browser = await chromium.launch({ headless: true });

try {
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 }, locale: "zh-TW" });
  const errors = [];
  page.on("pageerror", (error) => errors.push(`[pageerror] ${error.message}`));
  page.on("console", (message) => {
    if (message.type() === "error") errors.push(`[console.error] ${message.text()}`);
  });

  await page.goto(url, { waitUntil: "domcontentloaded" });
  await page.waitForSelector(".body-cell");

  assert.equal(await page.locator(".body-cell").count(), 1832, "all questions render");
  assert.equal(await page.locator(".section-row").count(), 33, "all subsection rows render");
  assert.equal(await page.locator("body").getAttribute("class"), "exam-layout");

  const examWidths = await page.evaluate(() => ({
    answer: document.querySelector(".answer-cell").getBoundingClientRect().width,
    source: document.querySelector(".source-cell").getBoundingClientRect().width,
    majorDisplay: getComputedStyle(document.querySelector(".major-section-row")).display,
  }));
  assert.ok(examWidths.answer <= 60, `answer column is narrow: ${examWidths.answer}px`);
  assert.ok(examWidths.source <= 130, `source column is narrow: ${examWidths.source}px`);
  assert.equal(examWidths.majorDisplay, "none", "major-only row stays hidden in exam mode");
  await page.screenshot({ path: resolve(outputDir, "exam-layout.png") });

  await page.locator("#layoutMode").selectOption("notes");
  await page.waitForFunction(() => document.body.classList.contains("notes-layout"));
  const notesState = await page.evaluate(() => ({
    answerDisplay: getComputedStyle(document.querySelector(".note-answer")).display,
    optionDisplay: getComputedStyle(document.querySelector(".options")).display,
    sourceDisplay: getComputedStyle(document.querySelector(".note-source")).display,
    majorDisplay: getComputedStyle(document.querySelector(".major-section-row")).display,
    metaDisplay: getComputedStyle(document.querySelector(".print-meta")).display,
    firstAnswer: document.querySelector(".note-answer").textContent.trim(),
  }));
  assert.equal(notesState.answerDisplay, "inline", "compact answer is visible");
  assert.equal(notesState.optionDisplay, "none", "multiple-choice options are hidden");
  assert.equal(notesState.sourceDisplay, "inline", "muted source is visible");
  assert.equal(notesState.majorDisplay, "table-row", "major section bar is visible");
  assert.equal(notesState.metaDisplay, "none", "setting summary is hidden in compact notes");
  assert.match(notesState.firstAnswer, /聚氯乙烯/, "answer core is rendered as text");
  await page.emulateMedia({ media: "print" });
  const printPageName = await page.locator(".page-shell").evaluate((node) => getComputedStyle(node).page);
  assert.equal(printPageName, "note-sheet", "compact layout uses the portrait page rule");
  await page.screenshot({ path: resolve(outputDir, "notes-print-layout.png") });
  assert.deepEqual(errors, [], errors.join("\n"));
  console.log("PASS: exam and compact-notes layouts verified");
} finally {
  await browser.close();
}
