const questions = window.EXAM_QUESTIONS || [];

const els = {
  body: document.getElementById("examBody"),
  table: document.getElementById("examTable"),
  printTitle: document.getElementById("printTitle"),
  printTitleInput: document.getElementById("printTitleInput"),
  fontSize: document.getElementById("fontSize"),
  fontSizeValue: document.getElementById("fontSizeValue"),
  lineHeight: document.getElementById("lineHeight"),
  lineHeightValue: document.getElementById("lineHeightValue"),
  questionGap: document.getElementById("questionGap"),
  questionGapValue: document.getElementById("questionGapValue"),
  showSource: document.getElementById("showSource"),
  printBorders: document.getElementById("printBorders"),
  showAnswers: document.getElementById("showAnswers"),
  layoutMode: document.getElementById("layoutMode"),
  sourceMode: document.getElementById("sourceMode"),
  optionLayout: document.getElementById("optionLayout"),
  optionPosition: document.getElementById("optionPosition"),
  printBtn: document.getElementById("printBtn"),
  questionCount: document.getElementById("questionCount"),
  modeLabel: document.getElementById("modeLabel")
};

const labels = {
  layoutMode: {
    exam: "完整考卷",
    notes: "精簡筆記"
  },
  sourceMode: {
    "three-column": "三欄右側",
    "two-column-block": "兩欄題內下方",
    "two-column-inline": "兩欄題目同行"
  },
  optionLayout: {
    horizontal: "橫向選項",
    vertical: "垂直選項"
  },
  optionPosition: {
    "next-line": "題目下一行",
    "same-line": "跟在題目後面"
  }
};

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function sourceText(question) {
  return question.sourceShort || `【${question.source}】`;
}

function questionParts(question) {
  const marker = " 解析提示：";
  const markerIndex = question.question.indexOf(marker);
  if (markerIndex < 0) {
    return { stem: question.question, note: "" };
  }
  return {
    stem: question.question.slice(0, markerIndex).trim(),
    note: question.question.slice(markerIndex + marker.length).trim()
  };
}

function answerText(question, note) {
  const coreMatch = note.match(/答案核心：(.+?)(?:；整併依據：|$)/);
  if (coreMatch) return coreMatch[1].trim();

  const letters = [...question.answer.matchAll(/[A-E]/g)].map((match) => match[0]);
  const selected = question.options
    .filter((option) => letters.some((letter) => option.startsWith(`(${letter})`)))
    .map((option) => option.replace(/^\([A-E]\)\s*/, ""));
  return selected.join("；") || question.answer;
}

function sectionParts(sectionTitle) {
  const parts = String(sectionTitle || "").split(/\s*\/\s*/, 2);
  return { major: parts[0] || "", subsection: parts[1] || "" };
}

function sectionHtml(sectionTitle, showMajor) {
  if (!sectionTitle) return "";
  const { major, subsection } = sectionParts(sectionTitle);
  const majorRow = showMajor
    ? `<tr class="major-section-row"><th colspan="3">${escapeHtml(major)}</th></tr>`
    : "";
  const noSubsection = subsection ? "" : " no-subsection";
  return `${majorRow}<tr class="section-row${noSubsection}"><th colspan="3"><span class="exam-section-title">${escapeHtml(sectionTitle)}</span><span class="notes-section-title">${escapeHtml(subsection || major)}</span></th></tr>`;
}

function rowHtml(question, showMajor) {
  const options = question.options
    .map((option) => `<span class="option">${escapeHtml(option)}</span>`)
    .join("");
  const source = escapeHtml(sourceText(question));
  const { stem, note } = questionParts(question);
  const compactAnswer = escapeHtml(answerText(question, note));
  const sectionRow = sectionHtml(question.sectionTitle, showMajor);

  return `${sectionRow}
    <tr>
      <td class="answer-cell">${escapeHtml(question.answer)}</td>
      <td class="body-cell">
        <div class="body-inner">
          <p class="question-line"><span class="question-stem">${escapeHtml(question.no)}. ${escapeHtml(stem)}</span><span class="teaching-note">${note ? ` 解析提示：${escapeHtml(note)}` : ""}</span><span class="note-answer"> → ${compactAnswer}</span><span class="inline-source">${source}</span><span class="note-source">${source}</span></p>
          <div class="options">${options}</div>
          <div class="body-source">${source}</div>
        </div>
      </td>
      <td class="source-cell">${source}</td>
    </tr>`;
}

function render() {
  let previousMajor = "";
  els.body.innerHTML = questions.map((question) => {
    const { major } = sectionParts(question.sectionTitle);
    const showMajor = Boolean(major && major !== previousMajor);
    if (major) previousMajor = major;
    return rowHtml(question, showMajor);
  }).join("");
  els.questionCount.textContent = `${questions.length} 題`;
}

function applySettings() {
  const fontSize = Number(els.fontSize.value);
  const lineHeight = Number(els.lineHeight.value);
  const questionGap = Number(els.questionGap.value);
  const sourceMode = els.sourceMode.value;
  const optionLayout = els.optionLayout.value;
  const optionPosition = els.optionPosition.value;
  const sourceVisible = els.showSource.checked;
  const bordersVisible = els.printBorders.checked;
  const answersVisible = els.showAnswers.checked;
  const layoutMode = els.layoutMode.value;
  const printTitle = els.printTitleInput.value.trim();

  document.documentElement.style.setProperty("--exam-font-size", `${fontSize}pt`);
  document.documentElement.style.setProperty("--exam-line-height", String(lineHeight));
  document.documentElement.style.setProperty("--question-option-gap", `${questionGap}px`);
  els.fontSizeValue.textContent = `${fontSize}pt`;
  els.lineHeightValue.textContent = lineHeight.toFixed(2).replace(/0$/, "");
  els.questionGapValue.textContent = `${questionGap}px`;
  els.printTitle.textContent = printTitle;
  document.title = printTitle ? `${printTitle} - 列印` : "考卷列印";
  document.body.classList.toggle("exam-layout", layoutMode === "exam");
  document.body.classList.toggle("notes-layout", layoutMode === "notes");

  els.table.className = [
    "exam-table",
    layoutMode === "notes" ? "layout-notes" : "layout-exam",
    sourceMode === "three-column" ? "source-three-column" : "source-two-column",
    sourceMode === "two-column-inline" ? "source-inline" : "source-block",
    sourceVisible ? "source-visible" : "source-hidden",
    bordersVisible ? "print-borders" : "no-borders",
    answersVisible ? "answers-visible" : "answers-hidden",
    optionLayout === "vertical" ? "options-vertical" : "options-horizontal",
    optionPosition === "same-line" ? "options-same-line" : "options-next-line"
  ].join(" ");

  document.querySelectorAll(".options").forEach((node) => {
    node.classList.toggle("vertical", optionLayout === "vertical");
  });

  document.querySelectorAll(".question-line").forEach((node) => {
    node.classList.toggle("with-gap", optionPosition === "next-line");
  });

  els.modeLabel.textContent = [
    labels.layoutMode[layoutMode],
    labels.sourceMode[sourceMode],
    labels.optionLayout[optionLayout],
    labels.optionPosition[optionPosition],
    sourceVisible ? "顯示出處" : "隱藏出處",
    bordersVisible ? "列印框線" : "無框線",
    answersVisible ? "顯示答案" : "隱藏答案"
  ].join(" · ");
}

function bindControls() {
  [
    els.fontSize,
    els.printTitleInput,
    els.lineHeight,
    els.questionGap,
    els.showSource,
    els.printBorders,
    els.showAnswers,
    els.sourceMode,
    els.optionLayout,
    els.optionPosition
  ].forEach((control) => {
    control.addEventListener("input", applySettings);
    control.addEventListener("change", applySettings);
  });

  els.layoutMode.addEventListener("change", () => {
    if (els.layoutMode.value === "notes") {
      els.fontSize.value = "9";
      els.lineHeight.value = "1.35";
      els.questionGap.value = "0";
      els.optionPosition.value = "same-line";
    } else {
      els.fontSize.value = "13";
      els.lineHeight.value = "1.55";
      els.questionGap.value = "24";
      els.optionPosition.value = "next-line";
    }
    applySettings();
  });

  els.printBtn.addEventListener("click", () => {
    window.print();
  });
}

render();
bindControls();
applySettings();
