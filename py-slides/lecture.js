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

let lectureTrace;
let environmentFrame;

function updateEnvironmentScope() {
  environmentFrame = undefined;
  const panel = root.querySelector('.env-panel');
  if (!panel || !lectureTrace) return;
  const stepIndex = Number(new URL(location.href).searchParams.get('step') || 0);
  const step = lectureTrace.steps[stepIndex];
  const values = Object.entries(step?.env || {}).filter(([, value]) => value !== null);
  const sourceLine = step?.stack?.at(-1)?.line_number;
  const line = [...root.querySelectorAll('.line-number')]
    .find(element => Number(element.textContent.trim()) === sourceLine)?.closest('.line');
  const bounds = line?.getBoundingClientRect();
  const headerBottom = root.querySelector('.header')?.getBoundingClientRect().bottom || 0;
  const visible = values.length > 0 && bounds && bounds.bottom > headerBottom && bounds.top < innerHeight;
  const display = visible ? '' : 'none';
  if (panel.style.display !== display) panel.style.display = display;
  for (const row of panel.querySelectorAll('tr')) {
    const label = row.querySelector('td')?.textContent.trim();
    const hidden = !values.some(([name]) => label === name);
    if (row.hidden !== hidden) row.hidden = hidden;
  }
}

function scheduleEnvironmentScope() {
  if (environmentFrame === undefined) environmentFrame = requestAnimationFrame(updateEnvironmentScope);
}

fetch(new URL('var/traces/lecture_19_full.json', document.baseURI), {cache: 'no-store'})
  .then(response => response.json())
  .then(trace => { lectureTrace = trace; scheduleEnvironmentScope(); });
new MutationObserver(scheduleEnvironmentScope).observe(root, {childList: true, subtree: true, attributes: true});
addEventListener('scroll', scheduleEnvironmentScope, {passive: true, capture: true});
addEventListener('resize', scheduleEnvironmentScope);
addEventListener('popstate', scheduleEnvironmentScope);
