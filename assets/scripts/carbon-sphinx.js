// Runtime behaviour for the Carbon Sphinx theme.
//
// Only the Carbon web components the templates use are imported, so the
// bundle stays as small as the UI shell allows.

import "@carbon/web-components/es/components/ui-shell/header.js";
import "@carbon/web-components/es/components/ui-shell/header-name.js";
import "@carbon/web-components/es/components/ui-shell/header-nav.js";
import "@carbon/web-components/es/components/ui-shell/header-nav-item.js";
import "@carbon/web-components/es/components/ui-shell/header-menu-button.js";
import "@carbon/web-components/es/components/ui-shell/header-global-action.js";
import "@carbon/web-components/es/components/ui-shell/header-panel.js";
import "@carbon/web-components/es/components/ui-shell/side-nav.js";
import "@carbon/web-components/es/components/ui-shell/side-nav-items.js";
import "@carbon/web-components/es/components/ui-shell/side-nav-link.js";
import "@carbon/web-components/es/components/ui-shell/header-side-nav-items.js";

const MODE_KEY = "carbon-sphinx-mode";
const MODES = ["auto", "light", "dark"];
const MODE_LABELS = {
  auto: "Theme: match system",
  light: "Theme: light",
  dark: "Theme: dark",
};

// ---------------------------------------------------------------- theme mode

function readMode() {
  try {
    const mode = localStorage.getItem(MODE_KEY);
    return MODES.includes(mode) ? mode : "auto";
  } catch {
    return "auto";
  }
}

function writeMode(mode) {
  try {
    localStorage.setItem(MODE_KEY, mode);
  } catch {
    // Storage unavailable (private mode, blocked cookies): keep in-memory only.
  }
}

const darkQuery = window.matchMedia("(prefers-color-scheme: dark)");

/** Apply the Carbon theme zone class for `mode` to <body>. */
function applyMode(mode) {
  const body = document.body;
  const light = body.dataset.lightTheme;
  const dark = body.dataset.darkTheme;
  const useDark = mode === "dark" || (mode === "auto" && darkQuery.matches);
  body.classList.remove(`cds--${light}`, `cds--${dark}`);
  body.classList.add(`cds--${useDark ? dark : light}`);
  body.dataset.mode = mode;
  document.documentElement.style.colorScheme = useDark ? "dark" : "light";

  const toggle = document.querySelector("[data-carbon-theme-toggle]");
  if (toggle) {
    toggle.setAttribute("tooltip-text", MODE_LABELS[mode]);
    toggle.setAttribute("aria-label", MODE_LABELS[mode]);
    for (const icon of toggle.querySelectorAll("[data-mode-icon]")) {
      icon.hidden = icon.dataset.modeIcon !== mode;
    }
  }
}

function setupThemeToggle() {
  applyMode(readMode());
  darkQuery.addEventListener("change", () => applyMode(readMode()));
  document.querySelector("[data-carbon-theme-toggle]")?.addEventListener("click", () => {
    const next = MODES[(MODES.indexOf(readMode()) + 1) % MODES.length];
    writeMode(next);
    applyMode(next);
  });
}

// ---------------------------------------------------------------- navigation

/**
 * Add expand/collapse buttons to every navigation entry that has children.
 * Branches leading to the current page start expanded. Without JavaScript
 * the full tree is shown, so navigation never depends on this code.
 */
function setupNavigation() {
  const nav = document.querySelector("nav.carbon-nav");
  if (!nav) return;
  const chevron = document.getElementById("carbon-icon-chevron");
  let counter = 0;
  for (const item of nav.querySelectorAll("li")) {
    const sublist = item.querySelector(":scope > ul");
    if (!sublist) continue;
    const id = sublist.id || `carbon-nav-${counter++}`;
    sublist.id = id;
    const expanded = item.classList.contains("current");
    const button = document.createElement("button");
    button.type = "button";
    button.className = "carbon-nav__toggle";
    button.setAttribute("aria-controls", id);
    button.setAttribute("aria-expanded", String(expanded));
    const label = item.querySelector(":scope > a")?.textContent?.trim() ?? "";
    button.setAttribute("aria-label", `Toggle ${label}`);
    if (chevron) button.append(chevron.content.cloneNode(true));
    button.addEventListener("click", () => {
      const open = button.getAttribute("aria-expanded") === "true";
      button.setAttribute("aria-expanded", String(!open));
    });
    item.classList.add("carbon-nav__parent");
    item.insertBefore(button, sublist);
  }
  // Keep the current page visible in a long navigation tree.
  nav.querySelector("a.current")?.scrollIntoView({ block: "center" });
}

// ---------------------------------------------------------------- search

function setupSearchPanel() {
  const action = document.querySelector("[data-carbon-search-toggle]");
  const panel = document.getElementById("carbon-search-panel");
  if (!action || !panel) return;
  // Focus the input once the panel opens.
  new MutationObserver(() => {
    if (panel.hasAttribute("expanded")) {
      requestAnimationFrame(() => panel.querySelector("input")?.focus());
    }
  }).observe(panel, { attributes: true, attributeFilter: ["expanded"] });
  // "/" opens search, like most documentation sites.
  document.addEventListener("keydown", (event) => {
    if (event.key !== "/" || event.defaultPrevented) return;
    const target = event.target;
    if (target.closest?.("input, textarea, select, [contenteditable]")) return;
    event.preventDefault();
    if (!panel.hasAttribute("expanded")) action.click();
  });
}

// ---------------------------------------------------------------- page toc

/**
 * Highlight the in-page TOC entry for the section being read: the last
 * section whose heading has scrolled past the top of the viewport. Sections
 * hidden by `toc_depth` highlight their nearest visible parent entry.
 */
function setupScrollSpy() {
  const toc = document.querySelector(".carbon-toc");
  if (!toc) return;
  const entries = [];
  for (const link of toc.querySelectorAll("a[href^='#']")) {
    if (link.hash.length < 2) continue; // the page title entry ("#")
    const section = document.getElementById(decodeURIComponent(link.hash.slice(1)));
    if (!section) continue;
    // Sphinx puts the id on <section>; measure its heading if it has one.
    const heading = section.querySelector(":scope > :is(h1, h2, h3, h4, h5, h6)") ?? section;
    entries.push({ link, heading });
  }
  if (!entries.length) return;

  const visibleLink = (link) => {
    let current = link;
    while (current && !current.offsetParent) {
      current = current.closest("ul")?.closest("li")?.querySelector(":scope > a") ?? null;
    }
    return current;
  };

  let active = null;
  let scheduled = false;
  const update = () => {
    scheduled = false;
    const threshold = parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop) || 64;
    let current = entries[0];
    for (const entry of entries) {
      if (entry.heading.getBoundingClientRect().top - threshold <= 1) current = entry;
      else break;
    }
    // At the very bottom, the last section counts as read.
    if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2) {
      current = entries[entries.length - 1];
    }
    const link = visibleLink(current.link);
    if (link === active) return;
    active?.classList.remove("carbon-toc__active");
    active = link;
    active?.classList.add("carbon-toc__active");
  };
  const schedule = () => {
    if (!scheduled) {
      scheduled = true;
      requestAnimationFrame(update);
    }
  };
  window.addEventListener("scroll", schedule, { passive: true });
  window.addEventListener("resize", schedule, { passive: true });
  update();
}

// ---------------------------------------------------------------- tables

/** Let wide tables scroll horizontally instead of overflowing the page. */
function wrapTables() {
  for (const table of document.querySelectorAll(".carbon-article table.docutils")) {
    if (table.parentElement.classList.contains("carbon-table-wrapper")) continue;
    const wrapper = document.createElement("div");
    wrapper.className = "carbon-table-wrapper";
    table.before(wrapper);
    wrapper.append(table);
  }
}

function init() {
  setupThemeToggle();
  wrapTables();
  setupNavigation();
  setupSearchPanel();
  setupScrollSpy();
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}
