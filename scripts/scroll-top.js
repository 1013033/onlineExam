(function () {
  const BUTTON_ID = "scrollTopButton";
  const VISIBLE_CLASS = "is-visible";
  const THRESHOLD = 240;

  if (document.getElementById(BUTTON_ID)) return;

  const style = document.createElement("style");
  style.textContent = `
    .scroll-top-button {
      position: fixed;
      right: max(18px, env(safe-area-inset-right));
      bottom: max(18px, env(safe-area-inset-bottom));
      width: 48px;
      height: 48px;
      border: 1px solid var(--border, #d9e0de);
      border: 1px solid color-mix(in srgb, var(--border, #d9e0de) 70%, transparent);
      border-radius: 999px;
      background: var(--surface, #fff);
      background: color-mix(in srgb, var(--surface, #fff) 88%, transparent);
      color: var(--fg, #172024);
      box-shadow: 0 12px 32px rgba(23, 32, 36, 0.18);
      cursor: pointer;
      display: grid;
      place-items: center;
      font: 900 24px/1 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      opacity: 0;
      pointer-events: none;
      transform: translateY(10px);
      transition: opacity 180ms ease, transform 180ms ease, background-color 180ms ease;
      z-index: 900;
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
    }

    .scroll-top-button.is-visible {
      opacity: 1;
      pointer-events: auto;
      transform: translateY(0);
    }

    .scroll-top-button:hover {
      background: var(--accent, #176b87);
      color: #fff;
    }

    .scroll-top-button:focus-visible {
      outline: 3px solid var(--accent, #176b87);
      outline: 3px solid color-mix(in srgb, var(--accent, #176b87) 42%, transparent);
      outline-offset: 3px;
    }

    @media (max-width: 720px) {
      .scroll-top-button {
        right: max(14px, env(safe-area-inset-right));
        bottom: max(14px, env(safe-area-inset-bottom));
        width: 44px;
        height: 44px;
        font-size: 22px;
      }
    }

    @media print {
      .scroll-top-button {
        display: none !important;
      }
    }
  `;

  const button = document.createElement("button");
  button.id = BUTTON_ID;
  button.className = "scroll-top-button";
  button.type = "button";
  button.textContent = "↑";
  button.setAttribute("aria-label", "回到頁面最上方");
  button.title = "回到頁面最上方";

  function scrollPosition() {
    return window.scrollY || document.documentElement.scrollTop || document.body.scrollTop || 0;
  }

  function updateVisibility() {
    button.classList.toggle(VISIBLE_CLASS, scrollPosition() > THRESHOLD);
  }

  function scrollToTop() {
    const behavior = window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth";
    const scrollTarget = document.scrollingElement || document.documentElement || document.body;
    if (scrollTarget && typeof scrollTarget.scrollTo === "function") {
      scrollTarget.scrollTo({ top: 0, behavior });
    } else {
      window.scrollTo({ top: 0, behavior });
    }
  }

  document.head.appendChild(style);
  document.body.appendChild(button);
  button.addEventListener("click", scrollToTop);
  window.addEventListener("scroll", updateVisibility, { passive: true });
  window.addEventListener("resize", updateVisibility);
  updateVisibility();
})();
