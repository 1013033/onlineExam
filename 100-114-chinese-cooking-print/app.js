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
  sourceMode: document.getElementById("sourceMode"),
  optionLayout: document.getElementById("optionLayout"),
  optionPosition: document.getElementById("optionPosition"),
  printBtn: document.getElementById("printBtn"),
  questionCount: document.getElementById("questionCount"),
  modeLabel: document.getElementById("modeLabel")
};

const labels = {
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

function rowHtml(question) {
  const options = question.options
    .map((option) => `<span class="option">${escapeHtml(option)}</span>`)
    .join("");
  const source = escapeHtml(sourceText(question));

  return `
    <tr>
      <td class="answer-cell">${escapeHtml(question.answer)}</td>
      <td class="body-cell">
        <div class="body-inner">
          <p class="question-line">${escapeHtml(question.no)}. ${escapeHtml(question.question)}<span class="inline-source">${source}</span></p>
          <div class="options">${options}</div>
          <div class="body-source">${source}</div>
        </div>
      </td>
      <td class="source-cell">${source}</td>
    </tr>`;
}

function render() {
  els.body.innerHTML = questions.map(rowHtml).join("");
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
  const printTitle = els.printTitleInput.value.trim();

  document.documentElement.style.setProperty("--exam-font-size", `${fontSize}pt`);
  document.documentElement.style.setProperty("--exam-line-height", String(lineHeight));
  document.documentElement.style.setProperty("--question-option-gap", `${questionGap}px`);
  els.fontSizeValue.textContent = `${fontSize}pt`;
  els.lineHeightValue.textContent = lineHeight.toFixed(2).replace(/0$/, "");
  els.questionGapValue.textContent = `${questionGap}px`;
  els.printTitle.textContent = printTitle;
  document.title = printTitle ? `${printTitle} - 列印` : "考卷列印";

  els.table.className = [
    "exam-table",
    sourceMode === "three-column" ? "source-three-column" : "source-two-column",
    sourceMode === "two-column-inline" ? "source-inline" : "source-block",
    sourceVisible ? "source-visible" : "source-hidden",
    bordersVisible ? "print-borders" : "no-borders",
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
    labels.sourceMode[sourceMode],
    labels.optionLayout[optionLayout],
    labels.optionPosition[optionPosition],
    sourceVisible ? "顯示出處" : "隱藏出處",
    bordersVisible ? "列印框線" : "無框線"
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
    els.sourceMode,
    els.optionLayout,
    els.optionPosition
  ].forEach((control) => {
    control.addEventListener("input", applySettings);
    control.addEventListener("change", applySettings);
  });

  els.printBtn.addEventListener("click", () => {
    window.print();
  });
}

render();
bindControls();
applySettings();
