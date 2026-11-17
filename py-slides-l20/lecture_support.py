"""HTML helpers and reference data for the Lecture 20 slides."""

from html import escape

# Each reference: number shown in the slides, card text, thumbnail, and source link.
REFERENCES = {
    "trustllm": dict(
        n=1,
        title="TrustLLM: Trustworthiness in Large Language Models",
        meta="Huang, Sun, Wang, et al. · ICML 2024",
        note="A taxonomy and benchmark for trustworthy LLMs, covering 16 models on over 30 datasets.",
        thumb="images/w13_trustllm_fig2.png",
        url="https://arxiv.org/abs/2401.05561",
    ),
    "instructgpt": dict(
        n=2,
        title="Training Language Models to Follow Instructions with Human Feedback",
        meta="Ouyang et al. · NeurIPS 2022",
        note="The three-step RLHF recipe behind InstructGPT.",
        thumb="images/w13_instructgpt_fig2.png",
        url="https://arxiv.org/abs/2203.02155",
    ),
    "xstest": dict(
        n=3,
        title="XSTest: A Test Suite for Identifying Exaggerated Safety Behaviours in LLMs",
        meta="Röttger, Kirk, Vidgen, Attanasio, Bianchi, Hovy · NAACL 2024",
        note="A test suite for over-refusal, with 200 unsafe prompts as a contrast set.",
        thumb="images/w13_xstest_fig1.png",
        url="https://arxiv.org/abs/2308.01263",
    ),
    "jailbroken": dict(
        n=4,
        title="Jailbroken: How Does LLM Safety Training Fail?",
        meta="Wei, Haghtalab, Steinhardt · NeurIPS 2023",
        note="Competing objectives and mismatched generalization as two causes of jailbreaks.",
        thumb="images/w13_title_jailbroken.png",
        url="https://papers.nips.cc/paper/2023/hash/fd6613131889a4b656206c50a8bd7790-Abstract-Conference.html",
    ),
    "greshake": dict(
        n=5,
        title="Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection",
        meta="Greshake, Abdelnabi, Mishra, Endres, Holz, Fritz · AISec 2023",
        note="Introduces indirect prompt injection through retrieved data.",
        thumb="images/w13_title_greshake.png",
        url="https://dl.acm.org/doi/10.1145/3605764.3623985",
    ),
    "roleconf": dict(
        n=6,
        title="Prompt Injection as Role Confusion",
        meta="Ye, Cui, Hadfield-Menell · ICML 2026",
        note="Models judge who is speaking from writing style more than from role tags.",
        thumb="images/w13_title_roleconf.png",
        url="https://proceedings.mlr.press/v306/ye26b.html",
    ),
    "agentdojo": dict(
        n=7,
        title="AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents",
        meta="Debenedetti et al. · NeurIPS 2024 Datasets and Benchmarks",
        note="A benchmark environment for prompt injection against tool-using agents.",
        thumb="images/w13_title_agentdojo.png",
        url="https://proceedings.neurips.cc/paper_files/paper/2024/hash/97091a5177d8dc64b1da8bf3e1f6fb54-Abstract-Datasets_and_Benchmarks_Track.html",
    ),
    "agentharm": dict(
        n=8,
        title="AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents",
        meta="Andriushchenko et al. · ICLR 2025",
        note="A benchmark of harmful requests that need multi-step tool use.",
        thumb="images/w13_title_agentharm.png",
        url="https://proceedings.iclr.cc/paper_files/paper/2025/hash/c493d23af93118975cdbc32cbe7323f5-Abstract-Conference.html",
    ),
    "wasp": dict(
        n=9,
        title="WASP: Benchmarking Web Agent Security Against Prompt Injection Attacks",
        meta="Evtimov et al. · NeurIPS 2025 Datasets and Benchmarks",
        note="Follows injected web agents from the first wrong step to the final outcome.",
        thumb="images/w13_title_wasp.png",
        url="https://proceedings.neurips.cc/paper_files/paper/2025/hash/1c9818387f5dd0a0bc151214660f059d-Abstract-Datasets_and_Benchmarks_Track.html",
    ),
    "competition": dict(
        n=10,
        title="Security Challenges in AI Agent Deployment: Insights from a Large Scale Public Competition",
        meta="Zou et al. · NeurIPS 2025 Datasets and Benchmarks",
        note="A public red-teaming competition against agents in simulated deployments.",
        thumb="images/w13_title_competition.png",
        url="https://proceedings.neurips.cc/paper_files/paper/2025/hash/73368bc7644c054b5bcc6490a8f2fb1c-Abstract-Datasets_and_Benchmarks_Track.html",
    ),
    "camel": dict(
        n=11,
        title="Defeating Prompt Injections by Design (CaMeL)",
        meta="Debenedetti et al. · SaTML 2026",
        note="A system-level defense that tracks where data comes from.",
        thumb="images/w13_title_camel.png",
        url="https://ieeexplore.ieee.org/abstract/document/11691650/authors",
    ),
    "ams": dict(
        n=12,
        title="The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against LLM Jailbreaks and Prompt Injections",
        meta="Nasr et al. · USENIX Security 2026",
        note="Re-tests published defenses with attacks that adapt to each one.",
        thumb="images/w13_title_ams.png",
        url="https://www.usenix.org/conference/usenixsecurity26/presentation/nasr",
    ),
}


def _ref_link(key):
    ref = REFERENCES[key]
    return f'<a href="#ref-{ref["n"]}" aria-label="Reference {ref["n"]}: {escape(ref["title"])}">[{ref["n"]}]</a>'


def card(key):
    """A compact reference card, shown where the paper first appears."""
    ref = REFERENCES[key]
    return (
        f'<article id="ref-{ref["n"]}" class="reference-card">'
        f'<img src="{ref["thumb"]}" alt="" loading="lazy"><div>'
        f'<h3>[{ref["n"]}] {escape(ref["title"])}</h3>'
        f'<p class="reference-meta">{escape(ref["meta"])}</p>'
        f'<p>{escape(ref["note"])}</p>'
        f'<div class="reference-links"><a href="{ref["url"]}" target="_blank" rel="noopener noreferrer">Open source ↗</a></div>'
        f'</div></article>'
    )


def figure(src, alt, key, caption, width=None):
    """An original figure that opens full size when clicked."""
    size = f' style="max-width:{width}px"' if width else ""
    return (
        f'<figure class="lesson-figure"><div class="figure-strip">'
        f'<button type="button" class="figure-thumb" data-figure="{src}">'
        f'<img src="{src}" alt="{escape(alt)}"{size}><span>Enlarge figure ↗</span></button></div>'
        f'<figcaption class="lesson-cite">{_ref_link(key)} {escape(caption)}</figcaption></figure>'
    )


def code_block(source, label):
    return (
        f'<div class="source-code"><strong>{escape(label)}</strong>'
        f'<pre><code>{escape(source)}</code></pre></div>'
    )
