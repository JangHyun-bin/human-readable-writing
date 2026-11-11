const languageLinks = [...document.querySelectorAll(".language-links a[href]")];
const languageBases = languageLinks.map((link) => link.getAttribute("href"));

function keepExampleAcrossLanguages(id) {
  languageLinks.forEach((link, index) => link.setAttribute("href", `${languageBases[index]}#${id}`));
}

function enhanceExampleBrowser(browser) {
  const tablist = browser.querySelector("[data-example-tabs]");
  if (!tablist) return null;

  const panels = new Map([...browser.querySelectorAll("[data-example-panel]")].map((panel) => [panel.id, panel]));
  const entries = [...tablist.querySelectorAll(".example-tab")].flatMap((tab) => {
    const panel = panels.get(tab.getAttribute("href").slice(1));
    return panel ? [{ tab, panel }] : [];
  });
  if (entries.length === 0) return null;

  tablist.setAttribute("role", "tablist");
  for (const { tab, panel } of entries) {
    tab.setAttribute("role", "tab");
    tab.setAttribute("aria-controls", panel.id);
    panel.setAttribute("role", "tabpanel");
    panel.setAttribute("aria-labelledby", tab.id);
  }

  function select(selected) {
    for (const entry of entries) {
      const active = entry === selected;
      entry.tab.setAttribute("aria-selected", String(active));
      entry.tab.tabIndex = active ? 0 : -1;
      entry.panel.hidden = !active;
    }
  }

  function choose(entry) {
    select(entry);
    history.replaceState(null, "", `#${entry.panel.id}`);
    keepExampleAcrossLanguages(entry.panel.id);
  }

  for (const entry of entries) {
    entry.tab.addEventListener("click", (event) => {
      if (event.button !== 0 || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
      event.preventDefault();
      choose(entry);
    });
  }

  tablist.addEventListener("keydown", (event) => {
    if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
    const current = entries.findIndex((entry) => entry.tab === document.activeElement);
    if (current === -1) return;
    const count = entries.length;
    let next;
    switch (event.key) {
      case "ArrowRight":
        next = (current + 1) % count;
        break;
      case "ArrowLeft":
        next = (current - 1 + count) % count;
        break;
      case "Home":
        next = 0;
        break;
      case "End":
        next = count - 1;
        break;
      default:
        return;
    }
    event.preventDefault();
    entries[next].tab.focus();
    choose(entries[next]);
  });

  select(entries[0]);

  return {
    show(id) {
      const entry = entries.find((candidate) => candidate.panel.id === id);
      if (!entry) return false;
      select(entry);
      entry.panel.scrollIntoView();
      return true;
    },
  };
}

const exampleBrowsers = [...document.querySelectorAll("[data-example-browser]")]
  .map(enhanceExampleBrowser)
  .filter(Boolean);

function showExampleFromHash() {
  let id;
  try {
    id = decodeURIComponent(location.hash.slice(1));
  } catch {
    return;
  }
  for (const browser of exampleBrowsers) {
    if (browser.show(id)) keepExampleAcrossLanguages(id);
  }
}

if (exampleBrowsers.length > 0) {
  showExampleFromHash();
  window.addEventListener("hashchange", showExampleFromHash);
}

const button = document.getElementById("copy-install");
const command = document.getElementById("install-command");
const status = document.getElementById("copy-status");

if (button && command && status) {
  const labels = button.dataset;

  button.addEventListener("click", async () => {
    button.disabled = true;
    button.dataset.state = "loading";
    button.textContent = labels.pending;
    status.textContent = "";
    status.removeAttribute("data-state");

    try {
      await navigator.clipboard.writeText(command.textContent);
      button.dataset.state = "success";
      button.textContent = labels.success;
      status.textContent = labels.successStatus;
    } catch {
      button.dataset.state = "error";
      button.textContent = labels.error;
      status.dataset.state = "error";
      status.textContent = labels.errorStatus;
    } finally {
      button.disabled = false;
    }
  });

  button.hidden = false;
}
