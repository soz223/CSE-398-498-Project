"""HTML helpers and reference data for the Lecture 21 slides."""

from html import escape

# Each reference: number shown in the slides, card text, thumbnail, and source link.
REFERENCES = {
    "mcpthreat": dict(
        n=1,
        title="Model Context Protocol Threat Modeling and Analyzing Vulnerabilities to Prompt Injection with Tool Poisoning",
        meta="Huang, Huang, Tran, Milani Fard · arXiv 2603.22489, 2026",
        note="A threat model of MCP with 57 threats, and tool poisoning tests on seven clients.",
        thumb="images/l21_title_mcpthreat.png",
        url="https://arxiv.org/abs/2603.22489",
    ),
    "invariant": dict(
        n=2,
        title="MCP Security Notification: Tool Poisoning Attacks",
        meta="Invariant Labs · April 2025",
        note="The first public report of tool poisoning, rug pulls, and shadowing in MCP.",
        thumb="images/l21_invariant_poison.png",
        url="https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks",
    ),
    "mcptox": dict(
        n=3,
        title="MCPTox: A Benchmark for Tool Poisoning Attack on Real-World MCP Servers",
        meta="Wang, Gao, Wang, et al. · AAAI 2026",
        note="A benchmark of tool poisoning built on 45 real MCP servers.",
        thumb="images/l21_title_mcptox.png",
        url="https://ojs.aaai.org/index.php/AAAI/article/view/40895",
    ),
    "agentvigil": dict(
        n=4,
        title="AgentVigil: Automatic Black-Box Red-teaming for Indirect Prompt Injection against LLM Agents",
        meta="Wang, Siu, Ye, et al. · Findings of EMNLP 2025",
        note="Generates injection attacks with seed mutation and tree search.",
        thumb="images/l21_title_agentvigil.png",
        url="https://aclanthology.org/2025.findings-emnlp.1258/",
    ),
    "mcpspec": dict(
        n=5,
        title="Model Context Protocol Specification and Security Best Practices",
        meta="modelcontextprotocol.io · version 2026-07-28",
        note="The protocol rules for servers and clients, and the official security guide.",
        thumb="images/l21_mcpspec_tools.png",
        url="https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security",
    ),
    "codex": dict(
        n=6,
        title="Codex Documentation: Agent Approvals and Security, and Rules",
        meta="OpenAI · checked October 2026",
        note="How Codex separates the sandbox, the approval policy, and command rules.",
        thumb="images/l21_codex_rules.png",
        url="https://learn.chatgpt.com/docs/agent-approvals-security",
    ),
    "aris": dict(
        n=7,
        title="ARIS: Autonomous Research via Adversarial Multi-Agent Collaboration",
        meta="arXiv 2605.03042, 2026",
        note="A research agent system whose limitations section discusses where code is sent.",
        thumb="images/l21_title_aris.png",
        url="https://arxiv.org/abs/2605.03042",
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
