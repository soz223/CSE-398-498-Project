from dataclasses import dataclass
from edtrace import text
from lecture_support import card, figure


def main():
    # Part 1. Where attacks enter the tool layer
    introduction()
    how_agents_reach_tools()
    tool_poisoning()
    rug_pulls_and_shadowing()
    real_clients()

    # Part 2. Measuring tool poisoning
    mcptox()
    which_attacks_work()
    agentvigil()

    # Part 3. Controls around the model
    protocol_rules()
    confused_deputy()
    urls_and_local_servers()
    codex_controls()

    # Part 4. Agents in your own research
    where_data_goes()
    disclosing_agent_use()
    summary()


def introduction():
    text("## 01 · The Agent Attack Surface")
    text("CSE 398/498 · Vibe Research for Scientific Discovery · Lichao Sun · Lehigh University")
    text("Last time we studied attacks on the model itself. Today we follow information through **the software around the model**.")
    text("- We start with **MCP**, the protocol that connects agents to tools, and see where attacks enter.")
    text("- Then we look at how researchers **measure tool poisoning**.")
    text("- Next we study **controls** that check an action before it runs.")
    text("- Finally we apply these ideas to **your own research project**.")
    text("Today we are going to study two questions. **Where does untrusted text enter, and where can software stop a bad action?**")


def how_agents_reach_tools():
    text("## 02 · How an Agent Reaches Its Tools")
    text("Let's first see how an agent connects to its tools. Most agents today use **MCP**, the Model Context Protocol. This work by *Huang et al.* builds a threat model for it.")
    text(card("mcpthreat"))
    text("- The **host** runs the application, and its **client** talks to one or more **servers**.")
    text("- Each server offers tools. Each tool comes with a name and a description.")
    text(figure("images/l21_mcpthreat_fig1.png", "Complete MCP threat model with numbered interactions and trust boundaries.", "mcpthreat", "MCP Threat Modeling, Figure 1. Follow the numbered interactions.", width=620))
    text("- Follow the request from the user through the host and client to the server.")
    text("- The model also receives information about the tools. The server checks which resources the request can access.")
    text("The authors find **57 threats** across five components. Each arrow crosses a boundary where one part trusts another. Next we look at the most common threat.")


def tool_poisoning():
    text("## 03 · Tool Poisoning")
    text("The model reads every tool description before it picks a tool. So the description itself is a way in. We call this **tool poisoning**.")
    text("- Here the tool only adds two numbers. Its description hides an **IMPORTANT** block.")
    text("- The block asks the model to read a private file, pass it along as an argument, and keep quiet about it.")
    text(figure("images/l21_mcpthreat_add.png", "Python code of an add tool whose docstring asks the model to read secret files.", "mcpthreat", "MCP Threat Modeling, Section 5.1.1. A poisoned addition tool.", width=430))
    text("- The user only asks to add 12 and 12. The user never sees the description, and the model always does.")
    text("*Invariant Labs* first reported this attack in April 2025.")
    text(card("invariant"))
    text("So we treat a tool description as **untrusted input**, just like a web page. Next we see how the attack can change over time.")


def rug_pulls_and_shadowing():
    text("## 04 · Rug Pulls and Shadowing")
    text("Tool poisoning also comes in quieter forms. *Invariant Labs* describes two of them.")
    text("- In a **rug pull**, the user approves a harmless server. Later, the server changes its tool description.")
    text(figure("images/l21_invariant_rugpull.png", "The user installs a benign service, and at use time it is swapped for an injected one.", "invariant", "Invariant Labs, rug pull. Installation time is on the left, and use time is on the right.", width=430))
    text("- So an old approval may not cover the description the model reads today.")
    text("- In **shadowing**, one server's description changes how the agent uses another server's tool.")
    text(figure("images/l21_invariant_shadow.png", "An injected service changes how the agent uses a trusted send_email tool.", "invariant", "Invariant Labs, shadowing. The user asks for an email to alice@mail.com.", width=560))
    text("- In this example, a poisoned tool tells the agent to send every email to the attacker. The trusted email tool then does the sending.")
    text("So we need to know **where each rule came from**. Next we ask how real clients handle these attacks.")


def real_clients():
    text("## 05 · How Real Clients Respond")
    text("The same threat modeling work tests these attacks on seven real MCP clients.")
    text(figure("images/l21_mcpthreat_tab19.png", "Table of four attacks against seven MCP clients, colored safe, partial, or unsafe.", "mcpthreat", "MCP Threat Modeling, Table 19. Green is safe, yellow is partial, and red is unsafe."))
    text("- Each row is an attack, such as reading files or remote code execution. Each column is a client.")
    text("- Results vary a lot from client to client. Five of the seven clients do not **validate tool descriptions** before use.")
    text("- These clients were tested in November 2025, and newer versions may behave differently.")
    text("So when your client, model, or settings change, you rerun the tests. Next we move from case studies to a benchmark.")


def mcptox():
    text("## 06 · MCPTox: A Benchmark for Tool Poisoning")
    text("Case studies show that an attack is possible. To see how often it works, we need a benchmark. This work, *MCPTox*, builds one from real MCP servers.")
    text(card("mcptox"))
    text("- It uses **45 real servers**, **353 tools**, and **1,348 test cases**.")
    text("- The agent carries out a normal task. The attacker only changes the metadata of one tool.")
    text("- The test checks whether the agent ends up following the attacker's goal.")
    text(figure("images/l21_mcptox_fig2.png", "MCPTox pipeline with a poisoned security_check tool and three evaluation outcomes.", "mcptox", "MCPTox, Figure 2.", width=620))
    text("The poisoned tool never needs to be called. The model reads its description while it picks other tools. Next we look at the results.")


def which_attacks_work():
    text("## 07 · Which Attacks Work Best")
    text("Now we look at how often these attacks succeed. ASR means attack success rate, so a higher bar is worse.")
    text(figure("images/l21_mcptox_fig1b.png", "Attack success rate for about twenty models.", "mcptox", "MCPTox, Figure 1b. Each bar is one model.", width=620))
    text("- Several models are fooled more than 60% of the time. A strong general model is not automatically a safe one.")
    text("- The authors compare three kinds of attack. In **P3**, the agent calls the right tool with **the wrong arguments**.")
    text(figure("images/l21_mcptox_fig5.png", "Average ASR for attack paradigms P1, P2, P3, and for stronger prompt wording.", "mcptox", "MCPTox, Figure 5. Left, three attack paradigms. Right, stronger wording of the attack.", width=560))
    text("- P3 succeeds most often, almost half the time on average.")
    text("This means a check on the tool name alone can miss the attack. Here is a small sketch in Python, as **our own example**.")
    call = ToolCall(tool="send_email", to="attkr@pwnd.com")
    name_ok = call.tool in APPROVED_TOOLS  # @inspect name_ok
    args_ok = recipient_is_known(call)  # @stepover @clear name_ok @inspect args_ok
    text("The tool name passes the check, and the recipient fails it. So we check **the complete arguments** before a tool runs. Next we ask how attackers find such inputs.")  # @clear args_ok


def agentvigil():
    text("## 08 · AgentVigil: Attacks That Learn from Feedback")
    text("So far the attacks were written by hand. This work, *AgentVigil*, generates them automatically and learns from each attempt.")
    text(card("agentvigil"))
    text("- It starts from seed attacks and changes them with a mutator.")
    text("- It sends each attack to the agent through external data, and a scorer checks the result.")
    text("- A tree search picks which seeds to explore next.")
    text(figure("images/l21_agentvigil_fig2.png", "The agent system on the left and the seed, mutator, scorer loop on the right.", "agentvigil", "AgentVigil, Figure 2. The agent is on the left, and the test loop is on the right."))
    text("- Removing the good starting seeds, or the seed selection, lowers coverage.")
    text(figure("images/l21_agentvigil_fig3.png", "Coverage over ten steps for the full method and two ablations.", "agentvigil", "AgentVigil, Figure 3. Higher coverage means attacks succeed on more tasks.", width=460))
    text("Recall the attack budget from last lecture. An attacker that learns needs fewer tries, so we compare methods **at the same budget**. Next we turn from attacks to controls.")


def protocol_rules():
    text("## 09 · What the Protocol Requires")
    text("We have seen how attacks reach the model. Now we follow the model's output outward. Before a tool call runs, other software still has a chance to stop it. Let's first look at what the MCP specification asks for.")
    text(card("mcpspec"))
    text("- Servers **must** validate inputs, control access, and sanitize outputs.")
    text("- Clients **should** ask the user before sensitive operations, and let the user deny a tool call.")
    text(figure("images/l21_mcpspec_tools.png", "Lists of what MCP servers must do and what clients should do.", "mcpspec", "MCP specification, Tools, Security Considerations.", width=430))
    text("- Tool annotations, such as a hint that a tool only reads, are claims made by the server. The specification says to treat them as untrusted unless the server is trusted.")
    text("A rule on paper does not prove that a client follows it. Recall that five of seven clients skipped validation. So we check **what the implementation enforces**. Next we look at failures that happen even without a model.")


def confused_deputy():
    text("## 10 · The Confused Deputy")
    text("Some attacks around agents do not involve the model at all. The MCP security guide describes a **confused deputy**.")
    text("- A proxy server holds permissions that the attacker lacks.")
    text("- The attacker tricks the proxy into using those permissions on the attacker's behalf.")
    text(figure("images/l21_deputy_setup.png", "Sequence diagram where a consent cookie lets the request skip consent.", "mcpspec", "MCP Security Best Practices, confused deputy. A stored consent cookie lets the request skip the consent screen.", width=560))
    text("- By the end, the attacker reaches a third party API **as the user**.")
    text(figure("images/l21_deputy_attack.png", "Sequence diagram ending with the attacker impersonating the user.", "mcpspec", "MCP Security Best Practices, confused deputy, the rest of the attack.", width=560))
    text("A better prompt cannot fix this. We fix it in the authorization code, for example by setting the consent cookie only after the user approves. Next we look at two more risks of this kind.")


def urls_and_local_servers():
    text("## 11 · Fetching URLs and Running Local Servers")
    text("Two more risks come from ordinary software. Let's first look at **server side request forgery**, or SSRF.")
    text("- A malicious server gives the client a URL, and the client fetches it without checking.")
    text("- The URL points to an internal address, such as a cloud metadata service, and secrets leak back.")
    text(figure("images/l21_ssrf.png", "The client follows a URL to an internal metadata service.", "mcpspec", "MCP Security Best Practices, SSRF."))
    text("- So the guide says clients should block private and reserved IP ranges.")
    text("- The second risk is a **local server**. It is a program that runs on your machine with your permissions.")
    text(figure("images/l21_local_server.png", "Three attacks on local MCP servers and two example startup commands.", "mcpspec", "MCP Security Best Practices, local server compromise.", width=560))
    text("Before you install one, you check where it came from and what it can access. Next we see how a coding agent limits this access.")


def codex_controls():
    text("## 12 · Sandbox, Approval, and Rules in Codex")
    text("Now let's connect these ideas to a tool you can use. *Codex*, OpenAI's coding agent, separates two settings.")
    text(card("codex"))
    text("- The **sandbox** limits what a command can read, write, or reach on the network.")
    text("- The **approval policy** decides when Codex must ask you first.")
    text(figure("images/l21_codex_sandbox.png", "Codex documentation describing sandbox mode and approval policy.", "codex", "Codex documentation, Agent approvals and security.", width=560))
    text("- **Rules** add finer control. Each rule matches the start of a command and decides to allow, prompt, or forbid it.")
    text(figure("images/l21_codex_rules.png", "A prefix_rule with pattern gh pr view and decision prompt.", "codex", "Codex documentation, Rules. This rule asks before running gh pr view.", width=520))
    text("Here is how such rules work, in a short Python sketch of **our own**.")
    decision = decide(["gh", "pr", "view", "42"])  # @stepover @inspect decision
    decision = decide(["rm", "-rf", "data"])  # @stepover @inspect decision
    text("The first command needs your approval, and the second is forbidden. So we keep the workspace small and review actions that leave it. Next we bring these ideas into your own project.")  # @clear decision


def where_data_goes():
    text("## 13 · Where Your Data Goes")
    text("The same questions apply when you use agents for research. Let's first ask **where project material goes**.")
    text(card("aris"))
    text("- This work, *ARIS*, runs research with one model that writes code and a model from another provider that reviews it.")
    text("- Its authors warn that a repository review may send source code to **external LLM APIs**.")
    text("- They advise against it for code with secrets, until a local review path exists.")
    text("- Code, logs, data samples, and drafts can each have **different sharing rules**.")
    text("So before you hand work to an agent, you list which service receives which material. Next we look at how to report agent use in a paper.")


def disclosing_agent_use():
    text("## 14 · Disclosing Agent Use")
    text("Readers of your paper need to know what the agent did. Here is a short checklist, based on our syllabus and the ACL policy on publication ethics.")
    text("- You name the agent, the model, their versions, and any skills you used.")
    text("- You say which sections and code the agent produced, and who checked them.")
    text("- You record the data and code behind each figure, and say whether any images were generated.")
    text("- You record who checked the references and which ones were removed.")
    text("- You keep the session log with your code.")
    text("These records let a reader follow what happened. **The authors remain responsible for everything they submit.** Now let's put the lecture together.")


def summary():
    text("## 15 · Summary")
    text("Let's put the pieces together.")
    text("- Tool descriptions and tool results are **untrusted input**, just like web pages.")
    text("- An attack can pick the right tool with **the wrong arguments**, so we check the complete call.")
    text("- Validation, authorization code, sandboxes, and approvals limit what an action can reach.")
    text("- Logs and disclosure let others **check what happened**.")
    text("Now we can answer our two questions. **Where does untrusted text enter, and where can software stop a bad action?**")


# Teaching sketches for Sections 07 and 12 (our own examples)

@dataclass
class ToolCall:
    tool: str
    to: str


APPROVED_TOOLS = {"add", "send_email"}
KNOWN_CONTACTS = {"alice@mail.com"}  # recipients named in the user's request


def recipient_is_known(call: ToolCall) -> bool:
    return call.to in KNOWN_CONTACTS


RULES = [
    (("gh", "pr", "view"), "prompt"),
    (("rm", "-rf"), "forbid"),
]


def decide(command: list[str]) -> str:
    # Return the decision of the first rule whose prefix matches the command.
    for prefix, decision in RULES:
        if tuple(command[:len(prefix)]) == prefix:
            return decision
    return "use sandbox and approval policy"
