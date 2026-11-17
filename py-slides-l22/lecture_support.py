"""HTML helpers and reference data for the Lecture 22 slides."""

from html import escape

# Each reference: number shown in the slides, card text, thumbnail, and source link.
REFERENCES = {
    "neurips": dict(
        n=1,
        title="NeurIPS 2026 Reviewer Guidelines and Review Form",
        meta="NeurIPS · 2026",
        note="The fields every NeurIPS 2026 reviewer fills in, with instructions for each.",
        thumb="images/l22_neurips_form.png",
        url="https://neurips.cc/Conferences/2026/ReviewerGuidelines",
    ),
    "icml": dict(
        n=2,
        title="ICML 2026 Policy for LLM Use in Reviewing",
        meta="ICML · 2026",
        note="Two reviewer policies, with papers matched to compatible reviewers.",
        thumb="images/l22_icml_policy.png",
        url="https://icml.cc/Conferences/2026/LLM-Policy",
    ),
    "iclr": dict(
        n=3,
        title="Policies on Large Language Model Usage at ICLR 2026",
        meta="ICLR · 2026",
        note="Treats hidden prompts in a submission as attempted collusion.",
        thumb="images/l22_iclr_policy.png",
        url="https://iclr.cc/FAQ/LLM",
    ),
    "lin": dict(
        n=4,
        title="Hidden Prompts in Manuscripts Exploit AI-Assisted Peer Review",
        meta="Zhicheng Lin · Communications of the ACM, 2026",
        note="Documents 18 arXiv manuscripts with hidden instructions aimed at AI reviewers.",
        thumb="images/l22_title_lin.png",
        url="https://doi.org/10.1145/3779116",
    ),
    "spot": dict(
        n=5,
        title="When AI Co-Scientists Fail: SPOT, a Benchmark for Automated Verification of Scientific Research",
        meta="Son, Hong, Fan, et al. · arXiv 2505.11855, 2025",
        note="Tests whether multimodal LLMs find confirmed errors in published papers.",
        thumb="images/l22_title_spot.png",
        url="https://arxiv.org/abs/2505.11855",
    ),
    "thakkar": dict(
        n=6,
        title="A Large-Scale Randomized Study of Large Language Model Feedback in Peer Review",
        meta="Thakkar, Yuksekgonul, Silberg, et al. · Nature Machine Intelligence, 2026",
        note="A randomized experiment with AI feedback on reviews at ICLR 2025.",
        thumb="images/l22_title_thakkar.png",
        url="https://www.nature.com/articles/s42256-026-01188-x",
    ),
    "aaai": dict(
        n=7,
        title="AI-Assisted Peer Review at Scale: The AAAI-26 AI Review Pilot",
        meta="Biswas, Schoepp, Vasan, et al. · arXiv 2604.13940, 2026",
        note="One AI review for every main track paper at AAAI 2026, plus a planted error test.",
        thumb="images/l22_title_aaai.png",
        url="https://arxiv.org/abs/2604.13940",
    ),
    "paperbench": dict(
        n=8,
        title="PaperBench: Evaluating AI's Ability to Replicate AI Research",
        meta="Starace, Jaffe, Sherburn, et al. · ICML 2025",
        note="Agents reproduce ICML papers from scratch and are graded with detailed rubrics.",
        thumb="images/l22_title_paperbench.png",
        url="https://proceedings.mlr.press/v267/starace25a.html",
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
        f'<figcaption class="lesson-cite">{_ref_link(key) + " " if key else ""}{escape(caption)}</figcaption></figure>'
    )


def code_block(source, label):
    return (
        f'<div class="source-code"><strong>{escape(label)}</strong>'
        f'<pre><code>{escape(source)}</code></pre></div>'
    )
