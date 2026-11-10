const root = document.querySelector("#root");
const figureViewer = document.querySelector("#figure-viewer");
const largeFigure = document.querySelector("#large-figure");
let figureTrigger;

root.addEventListener("click", (event) => {
  const thumbnail = event.target.closest("button[data-figure]");
  if (thumbnail) {
    figureTrigger = thumbnail;
    const label = thumbnail.querySelector("img").alt;
    document.querySelector("#figure-title").textContent = label;
    largeFigure.src = thumbnail.dataset.figure;
    largeFigure.alt = label;
    document.querySelector("#original-figure").href = thumbnail.dataset.figure;
    figureViewer.showModal();
    return;
  }

  const control = event.target.closest("button[data-frame]");
  if (!control) return;
  const demo = control.closest(".lesson-demo");
  for (const button of demo.querySelectorAll("[data-frame]")) {
    button.setAttribute("aria-pressed", String(button === control));
  }
  for (const panel of demo.querySelectorAll("[data-panel]")) {
    panel.hidden = panel.dataset.panel !== control.dataset.frame;
    panel.classList.toggle("entered", !panel.hidden);
  }
});

document.querySelector("#close-figure").addEventListener("click", () => figureViewer.close());
figureViewer.addEventListener("click", (event) => {
  if (event.target === figureViewer) figureViewer.close();
});
figureViewer.addEventListener("close", () => figureTrigger?.focus());

function addChapterMenu() {
  const header = root.querySelector(".header");
  const headings = [...root.querySelectorAll(".markdown h2")];
  if (!header || headings.length < 43 || header.querySelector("#chapter-jump")) return;
  const select = document.createElement("select");
  select.id = "chapter-jump";
  select.setAttribute("aria-label", "Jump to section");
  select.add(new Option("Jump to section…", ""));
  headings.forEach((heading, index) => select.add(new Option(heading.textContent, index)));
  select.addEventListener("change", () => {
    if (select.value !== "") {
      const heading = root.querySelectorAll(".markdown h2")[Number(select.value)];
      heading?.closest(".line")?.scrollIntoView({block: "start"});
    }
    select.value = "";
  });
  header.append(select);
}

new MutationObserver(addChapterMenu).observe(root, {childList: true, subtree: true});
addChapterMenu();
