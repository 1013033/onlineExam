#!/usr/bin/env node
/**
 * md-to-data.js  —  content.md → course-data.js
 * Usage: node md-to-data.js [--watch]
 *
 * Parses content.md and writes window.COURSE = {...} to course-data.js
 * so that index.html works identically in dev and on GitHub Pages.
 */

'use strict';
const fs   = require('fs');
const path = require('path');

const SRC          = path.join(__dirname, 'content.md');
const DEST         = path.join(__dirname, 'course-data.js');
const PORTAL_DEST  = path.join(__dirname, '..', 'portal-data.js');

/* ── tiny YAML parser (subset sufficient for this schema) ───────────────── */
function parseYaml(block) {
  const obj = {};
  const lines = block.split('\n');
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    if (!line.trim() || line.trim().startsWith('#')) { i++; continue; }

    // Sequence item under a key  (already stored via the parent)
    if (line.match(/^\s+-\s/)) { i++; continue; }

    const colonIdx = line.indexOf(':');
    if (colonIdx === -1) { i++; continue; }

    const key = line.slice(0, colonIdx).trim();
    const rest = line.slice(colonIdx + 1).trim();

    if (rest === '|' || rest === '>') {
      // Block scalar — collect until de-indent
      const baseIndent = line.match(/^(\s*)/)[1].length;
      let scalar = '';
      i++;
      while (i < lines.length) {
        const l = lines[i];
        if (l.trim() === '' || l.match(/^(\s*)/)[1].length > baseIndent) {
          scalar += (l.trim() === '' ? '\n' : l.trim() + '\n');
          i++;
        } else { break; }
      }
      obj[key] = scalar.trimEnd();
      continue;
    }

    if (rest === '') {
      // Possible sequence
      const seq = [];
      const baseIndent = line.match(/^(\s*)/)[1].length;
      i++;
      while (i < lines.length) {
        const l = lines[i];
        const m = l.match(/^(\s*)- (.*)/);
        if (m && m[1].length === baseIndent) {
          // inline mapping item?
          const val = m[2].trim();
          if (val.startsWith('{')) {
            // parse inline map
            const pairs = val.replace(/[{}]/g, '').split(',');
            const item = {};
            pairs.forEach(p => {
              const [k, v] = p.split(':').map(s => s.trim());
              item[k] = coerce(v);
            });
            seq.push(item);
          } else if (val) {
            seq.push(coerce(val));
          } else {
            // multi-line mapping item
            const item = {};
            i++;
            const itemIndent = baseIndent + 2;
            while (i < lines.length) {
              const il = lines[i];
              if (il.match(/^(\s*)/)[1].length < itemIndent && il.trim()) break;
              const ci = il.indexOf(':');
              if (ci > -1) {
                const ik = il.slice(0, ci).trim();
                const iv = il.slice(ci + 1).trim();
                item[ik] = coerce(iv);
              }
              i++;
            }
            seq.push(item);
            continue;
          }
        } else { break; }
        i++;
      }
      obj[key] = seq;
      continue;
    }

    obj[key] = coerce(rest);
    i++;
  }
  return obj;
}

function coerce(v) {
  if (v === undefined || v === null) return v;
  v = v.replace(/^["']|["']$/g, '');
  if (v === 'true') return true;
  if (v === 'false') return false;
  if (v === 'null') return null;
  if (!isNaN(v) && v !== '') return Number(v);
  // array shorthand [A, B, C]
  if (v.startsWith('[') && v.endsWith(']')) {
    return v.slice(1,-1).split(',').map(x => coerce(x.trim()));
  }
  return v;
}

/* ── answer normaliser ───────────────────────────────────────────────────── */
const LETTER = { A:0, B:1, C:2, D:3, E:4 };

function normaliseAnswer(raw, type) {
  if (type === 'text') return null;
  if (Array.isArray(raw)) {
    return raw.map(x => {
      const up = String(x).toUpperCase().trim();
      return LETTER[up] !== undefined ? LETTER[up] : Number(x);
    });
  }
  const up = String(raw).toUpperCase().trim();
  if (LETTER[up] !== undefined) return LETTER[up];
  return Number(raw);
}

/* ── question type detector ─────────────────────────────────────────────── */
function detectQuizType(heading, yaml) {
  if (yaml.type) return yaml.type;
  if (/多選/.test(heading)) return 'multiple';
  if (/手寫|非選擇|表格|簡答|混合題/.test(heading) && yaml.subQuestions) return 'text';
  if (/混合單選/.test(heading)) return 'single';
  return 'single';
}

/* ── main parser ─────────────────────────────────────────────────────────── */
function parseContent(md) {
  // Normalise line endings
  md = md.replace(/\r\n/g, '\n').replace(/\r/g, '\n');

  // ── Strip HTML comments <!-- ... --> (single-line & multi-line) ──────────
  // Users can comment out any block in content.md and it will be ignored.
  // Example: <!-- ## Q5 · 單選題 ... --> won't appear in the output.
  md = md.replace(/<!--[\s\S]*?-->/g, '');

  const COURSE = { meta: {}, materials: [], quiz: [] };
  let portalMeta = {};
  let portalExams = [];

  // Split into top-level sections by `# HEADING`
  const sections = md.split(/\n(?=# )/);

  for (const section of sections) {
    const lines = section.split('\n');
    const heading = lines[0].replace(/^#\s*/, '').trim();

    if (heading === 'META') {
      parseMeta(section, COURSE);
    } else if (heading.startsWith('DAY')) {
      const dayId = 'day' + heading.replace(/^DAY\s*/i, '');
      COURSE[dayId] = parseDay(section, dayId);
      // Register in meta.days
      if (!COURSE.meta.days) COURSE.meta.days = [];
    } else if (heading === 'MATERIALS') {
      COURSE.materials = parseMaterials(section);
    } else if (heading === 'QUIZ') {
      COURSE.quiz = parseQuiz(section);
    } else if (heading === 'PORTAL') {
      ({ meta: portalMeta, exams: portalExams } = parsePortal(section));
    }
  }

  return { COURSE, portalMeta, portalExams };
}

/* ── META section ────────────────────────────────────────────────────────── */
function parseMeta(section, COURSE) {
  const yamlBlock = extractFirstYaml(section);
  if (yamlBlock) {
    const y = parseYaml(yamlBlock);
    Object.assign(COURSE.meta, y);
  }

  // objectives
  const objMatch = section.match(/## 學習目標([\s\S]*?)(?=\n##|\n# |$)/);
  if (objMatch) {
    COURSE.meta.objectives = objMatch[1].trim().split('\n')
      .filter(l => l.trim().startsWith('-'))
      .map(l => l.replace(/^-\s*/, '').trim());
  }

  // schedule table
  const schedMatch = section.match(/## 考科時程([\s\S]*?)(?=\n##|\n# |$)/);
  if (schedMatch) {
    const rows = schedMatch[1].trim().split('\n')
      .filter(l => l.includes('|') && !l.match(/^[\s|:-]+$/));
    // skip header
    COURSE.meta.schedule = rows.slice(1).map(row =>
      row.split('|').map(c => c.trim()).filter(Boolean)
    );
  }
}

/* ── DAY section ─────────────────────────────────────────────────────────── */
function parseDay(section, dayId) {
  const yamlBlock = extractFirstYaml(section);
  const y = yamlBlock ? parseYaml(yamlBlock) : {};

  const day = {
    id: y.id || dayId,
    title: y.title || '',
    date: y.date_label || y.date || '',
    hours: y.hours_label || String(y.hours || ''),
    learningGoal: y.learningGoal || '',
    hero: { title: y.hero_title || '', lead: y.hero_lead || '' },
    units: [],
    schedule: []
  };

  // Add to meta.days if not present
  // (done externally in caller)

  // Parse ## 單元 sub-sections
  const unitSections = section.split(/\n(?=## 單元)/);
  unitSections.shift(); // drop preamble

  for (const us of unitSections) {
    const unit = parseUnit(us);
    if (unit) day.units.push(unit);
  }

  return day;
}

/* ── UNIT sub-section ────────────────────────────────────────────────────── */
function parseUnit(section) {
  const firstLine = section.split('\n')[0];
  const titleMatch = firstLine.match(/^## 單元[一二三四五六七八九十\d]+[：:]\s*(.+)/);
  const title = titleMatch ? titleMatch[1].trim() : firstLine.replace(/^##\s*/, '').trim();

  const yamlBlock = extractFirstYaml(section);
  const y = yamlBlock ? parseYaml(yamlBlock) : {};

  const unit = {
    id: y.id || '',
    title: title,
    subtitle: y.subtitle || '',
    time: y.time || '',
    goals: [],
    tasks: [],
    materials: [],
    illustrations: [],
    prompts: []
  };

  // ### 學習目標
  const goalMatch = section.match(/### 學習目標([\s\S]*?)(?=\n###|\n##|\n# |$)/);
  if (goalMatch) {
    unit.goals = goalMatch[1].trim().split('\n')
      .filter(l => l.trim().startsWith('-'))
      .map(l => l.replace(/^-\s*/, '').trim());
  }

  // ### 任務清單  - [id] label
  const taskMatch = section.match(/### 任務清單([\s\S]*?)(?=\n###|\n##|\n# |$)/);
  if (taskMatch) {
    unit.tasks = taskMatch[1].trim().split('\n')
      .filter(l => l.trim().match(/^-\s*\[/))
      .map(l => {
        const m = l.match(/^-\s*\[([^\]]+)\]\s*(.+)/);
        return m ? { id: m[1].trim(), label: m[2].trim() } : null;
      }).filter(Boolean);
  }

  // ### 素材  - [TYPE] name | desc
  const matMatch = section.match(/### 素材([\s\S]*?)(?=\n###|\n##|\n# |$)/);
  if (matMatch) {
    unit.materials = matMatch[1].trim().split('\n')
      .filter(l => l.trim().startsWith('-'))
      .map(l => {
        const m = l.match(/^-\s*\[([^\]]+)\]\s*([^|]+)\s*\|\s*(.+)/);
        if (m) {
          const id = 'd1-m' + Math.random().toString(36).slice(2,6);
          return { id, type: m[1].trim(), name: m[2].trim(), desc: m[3].trim() };
        }
        return null;
      }).filter(Boolean);
  }

  // ### 插圖  - name | kind | alt
  const illMatch = section.match(/### 插圖([\s\S]*?)(?=\n###|\n##|\n# |$)/);
  if (illMatch) {
    unit.illustrations = illMatch[1].trim().split('\n')
      .filter(l => l.trim().startsWith('-'))
      .map(l => {
        const parts = l.replace(/^-\s*/, '').split('|').map(s => s.trim());
        return parts.length >= 3
          ? { name: parts[0], kind: parts[1], alt: parts[2] }
          : null;
      }).filter(Boolean);
  }

  return unit;
}

/* ── MATERIALS section ───────────────────────────────────────────────────── */
function parseMaterials(section) {
  return section.split('\n')
    .filter(l => l.trim().startsWith('-'))
    .map(l => {
      const m = l.match(/^-\s*\[([^\]]+)\]\s*([^|]+)\s*\|\s*(.+)/);
      if (m) return { id: 'm-' + Math.random().toString(36).slice(2,6), type: m[1].trim(), name: m[2].trim(), desc: m[3].trim() };
      return null;
    }).filter(Boolean);
}

/* ── QUIZ section ────────────────────────────────────────────────────────── */
function parseQuiz(section) {
  const items = [];
  // Split on `## Q<N>` headings
  const qSections = section.split(/\n(?=## Q\d+)/);
  qSections.shift(); // drop preamble

  for (const qs of qSections) {
    const lines = qs.split('\n');
    const headingLine = lines[0]; // ## Q1 · 單選題
    const idMatch = headingLine.match(/## (Q\d+)/i);
    if (!idMatch) continue;
    const id = idMatch[1].toLowerCase();

    const yamlBlock = extractLastYaml(qs);
    const y = yamlBlock ? parseYaml(yamlBlock) : {};

    const type = detectQuizType(headingLine, y);

    // Question text: everything between heading and first bullet/yaml
    const bodyLines = [];
    let inOptions = false;
    const optionLines = [];

    for (let i = 1; i < lines.length; i++) {
      const l = lines[i];
      if (l.trimStart().startsWith('```')) break; // stop at yaml block
      if (l.trim().match(/^\([A-E]\)|^-\s*\([A-E]\)/)) {
        inOptions = true;
        optionLines.push(l.trim().replace(/^-\s*/, ''));
      } else if (!inOptions) {
        if (l.trim()) bodyLines.push(l.trim());
      }
    }

    // For text-type, question is everything before yaml (no options)
    const qText = type === 'text'
      ? bodyLines.join('\n').trim()
      : bodyLines.filter(l => !l.trim().match(/^\([A-E]\)/)).join('\n').trim();

    const item = {
      id: id,
      type: type,
      sourceUnit: y.unit || '',
      q: headingLine.includes('·') ? qText : qText
    };

    if (type === 'text') {
      // subQuestions from yaml
      item.subQuestions = (y.subQuestions || []).map(sq => ({
        label: sq.label || '',
        placeholder: sq.placeholder || '請在此輸入您的作答...'
      }));
      item.answer = y.answer || {};
      // Ensure answer keys are strings
      const a = {};
      Object.entries(item.answer).forEach(([k, v]) => { a[String(k)] = v; });
      item.answer = a;
    } else {
      item.options = optionLines;
      item.answer = normaliseAnswer(y.answer, type);
    }

    item.explanation = (y.explanation || '').trim();

    items.push(item);
  }
  return items;
}

/* ── PORTAL section ──────────────────────────────────────────────────────── */
function parsePortal(section) {
  const yamlBlock = extractFirstYaml(section);
  const meta = yamlBlock ? parseYaml(yamlBlock) : {};

  const exams = [];
  const examSections = section.split(/\n(?=## )/);
  examSections.shift();

  for (const es of examSections) {
    const yaml = extractFirstYaml(es);
    if (yaml) {
      const y = parseYaml(yaml);
      if (y.id) exams.push(y);
    }
  }

  return { meta, exams };
}

/* ── helpers ─────────────────────────────────────────────────────────────── */
function extractFirstYaml(text) {
  const m = text.match(/```(?:yaml)?\n([\s\S]*?)```/);
  return m ? m[1] : null;
}

function extractLastYaml(text) {
  const matches = [...text.matchAll(/```(?:yaml)?\n([\s\S]*?)```/g)];
  return matches.length ? matches[matches.length - 1][1] : null;
}

/* ── post-process: sync meta.days from parsed days ───────────────────────── */
function postProcess(COURSE) {
  const days = [];
  let n = 1;
  while (COURSE[`day${n}`]) {
    const d = COURSE[`day${n}`];
    const y = COURSE.meta; // reuse meta dates field if needed
    days.push({ id: `day${n}`, n, date: d.date || '', title: d.title, hours: parseFloat(d.hours) || 1.5 });
    n++;
  }
  COURSE.meta.days = days;

  // Copy schedule from meta if set
  if (COURSE.meta.schedule) {
    if (COURSE.day1) COURSE.day1.schedule = COURSE.meta.schedule;
    delete COURSE.meta.schedule;
  } else if (COURSE.day1 && !COURSE.day1.schedule.length) {
    COURSE.day1.schedule = [];
  }

  // sharedCase
  COURSE.sharedCase = null;

  return COURSE;
}

/* ── write output ────────────────────────────────────────────────────────── */
function build() {
  console.log('[md-to-data] Reading content.md ...');
  const md = fs.readFileSync(SRC, 'utf8');
  const { COURSE, portalMeta, portalExams } = parseContent(md);
  postProcess(COURSE);

  const timestamp = new Date().toISOString();

  const out = [
    '// AUTO-GENERATED by md-to-data.js — DO NOT EDIT DIRECTLY',
    '// Edit content.md instead, then run: npm run build',
    '//',
    `// Generated: ${timestamp}`,
    '',
    `window.COURSE = ${JSON.stringify(COURSE, null, 2)};`,
    '',
    `window.PORTAL = ${JSON.stringify({ meta: portalMeta, exams: portalExams }, null, 2)};`,
  ].join('\n');

  fs.writeFileSync(DEST, out, 'utf8');
  console.log('[md-to-data] ✅ course-data.js written successfully.');

  // Also write portal-data.js for the web root index.html
  // Smart merge logic: Read existing portal-data.js and merge window.PORTAL.exams so we don't wipe out other exams
  let finalPortalData = { meta: portalMeta, exams: portalExams };
  try {
    if (fs.existsSync(PORTAL_DEST)) {
      const existingContent = fs.readFileSync(PORTAL_DEST, 'utf8');
      const jsonMatch = existingContent.match(/window\.PORTAL\s*=\s*([\s\S]+?);/);
      if (jsonMatch) {
        const existingPortal = JSON.parse(jsonMatch[1]);
        if (existingPortal && Array.isArray(existingPortal.exams)) {
          const examMap = new Map();
          // First add existing exams
          existingPortal.exams.forEach(ex => examMap.set(ex.id, ex));
          // Overwrite/append with current exams
          portalExams.forEach(ex => examMap.set(ex.id, ex));
          
          finalPortalData.exams = Array.from(examMap.values());
          // Merge meta (prefer existing dashboard title/subtitle unless updated)
          finalPortalData.meta = Object.assign({}, existingPortal.meta, portalMeta);
        }
      }
    }
  } catch (e) {
    console.warn('[md-to-data] ⚠️ Could not merge existing portal-data.js:', e.message);
  }

  const portalOut = [
    '// AUTO-GENERATED by md-to-data.js — DO NOT EDIT DIRECTLY',
    '// Edit 114-baking-contest/content.md instead, then run: npm run build',
    '//',
    `// Generated: ${timestamp}`,
    '',
    `window.PORTAL = ${JSON.stringify(finalPortalData, null, 2)};`,
  ].join('\n');

  try {
    fs.writeFileSync(PORTAL_DEST, portalOut, 'utf8');
    console.log('[md-to-data] ✅ portal-data.js written and merged successfully.');
  } catch(e) {
    console.warn('[md-to-data] ⚠️  Could not write portal-data.js:', e.message);
  }

  return { COURSE, portalMeta, portalExams };
}

/* ── watch mode ──────────────────────────────────────────────────────────── */
if (require.main === module) {
  build();

  if (process.argv.includes('--watch')) {
    console.log('[md-to-data] 👁  Watching content.md for changes...');
    let debounce = null;
    fs.watch(SRC, () => {
      clearTimeout(debounce);
      debounce = setTimeout(() => {
        try { build(); } catch(e) { console.error('[md-to-data] ❌ Parse error:', e.message); }
      }, 150);
    });
  }
}

module.exports = { build };
