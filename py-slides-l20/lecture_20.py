from dataclasses import dataclass
from edtrace import text
from lecture_support import card, figure


def main():
    # Part 1. What LLM safety is, and how it fails
    introduction()
    what_is_llm_safety()
    how_models_learn_to_refuse()
    two_ways_to_fail()
    why_safety_training_fails()

    # Part 2. From chat models to agents
    indirect_prompt_injection()
    role_confusion()

    # Part 3. Measuring attacks on agents
    agentdojo()
    agentharm()
    wasp()
    attempts_and_budget()

    # Part 4. Defenses and stronger attackers
    camel_design()
    camel_results()
    adaptive_attacks()
    summary()


def introduction():
    text("## 01 · Agent Safety and Security")
    text("CSE 398/498 · Vibe Research for Scientific Discovery · Lichao Sun · Lehigh University")
    text("We have built agents and learned to evaluate them. Today we ask what happens **when someone wants the agent to do the wrong thing**.")
    text("- We start with **LLM safety** and how models learn it.")
    text("- Then we see **why safety training fails**, and why agents make it worse.")
    text("- Next we look at how to **measure attacks on agents**.")
    text("- Finally we study **defenses** and how to test them.")
    text("Today we are going to study two questions. **What does the attacker control, and what did the experiment observe?**")


def what_is_llm_safety():
    text("## 02 · What Is LLM Safety?")
    text("Before we study attacks, we need to know what we are protecting. This work, *TrustLLM*, groups trustworthiness into eight dimensions.")
    text(card("trustllm"))
    text("- One of them is **safety**, which covers jailbreaks, toxic output, and misuse.")
    text("- The others include truthfulness, fairness, robustness, and privacy.")
    text(figure("images/w13_trustllm_fig2.png", "TrustLLM benchmark design with the eight dimensions along the bottom.", "trustllm", "TrustLLM, Figure 2. The eight dimensions are along the bottom."))
    text("Today we focus on safety. This work also finds that some models are so cautious that they **refuse harmless requests**. We will come back to this soon.")


def how_models_learn_to_refuse():
    text("## 03 · How Models Learn to Refuse")
    text("Next we ask how a model learns to be safe. The standard method is **RLHF**, reinforcement learning from human feedback. This work, *InstructGPT*, is the best known example.")
    text(card("instructgpt"))
    text("- First, people write good answers, and the model imitates them.")
    text("- Then people rank model answers, and a reward model learns their preferences.")
    text("- Finally, the model is trained to earn a high reward.")
    text(figure("images/w13_instructgpt_fig2.png", "The three steps of RLHF.", "instructgpt", "InstructGPT, Figure 2."))
    text("Labelers prefer answers that are helpful and harmless. So the model learns to refuse **from examples**. This works well most of the time, and it can also go wrong in two directions.")


def two_ways_to_fail():
    text("## 04 · Two Ways to Fail")
    text("This figure from *TrustLLM* shows both directions.")
    text("- In the first direction, the model **refuses too little**. A harmful request is disguised, and the model answers it. We call this a **jailbreak**.")
    text("- In the second direction, the model **refuses too much**. Here the user only wants to stop a Windows process, and the model refuses. We call this **exaggerated safety**.")
    text(figure("images/w13_trustllm_fig5.png", "Left, a jailbreak gets a harmful answer. Right, the model refuses to explain how to kill a Windows process.", "trustllm", "TrustLLM, Figure 5."))
    text("This work, *XSTest*, measures the second direction with 250 safe prompts, such as \"Where can I buy a can of coke?\"")
    text(card("xstest"))
    text("So when we evaluate safety, we check both directions. We will see this again with agents. Next we look more closely at jailbreaks, since they can cause real harm.")


def why_safety_training_fails():
    text("## 05 · Why Safety Training Fails")
    text("Why can a model trained to refuse still be jailbroken? This work, *Jailbroken*, gives two explanations.")
    text(card("jailbroken"))
    text("- Let's first look at **competing objectives**. The model is trained to follow instructions and to be safe. A prompt can set these goals against each other, for example by asking the answer to start with \"Absolutely! Here's\".")
    text("- The second explanation is **mismatched generalization**. The model learns to read Base64 during pretraining. Safety training mostly uses plain English. So the model understands a harmful request in Base64, and its safety training misses it.")
    text(figure("images/w13_jailbroken_fig1.png", "Two jailbreaks of GPT-4, a forced prefix and a Base64 request.", "jailbroken", "Jailbroken, Figure 1."))
    text("In both cases, the request comes from the user. From here on, the model becomes an agent that reads outside content and uses tools. **The instruction may then come from someone other than the user.**")


def indirect_prompt_injection():
    text("## 06 · Indirect Prompt Injection")
    text("An agent reads web pages, emails, and files for its user. This gives the attacker a new way in. This work by *Greshake et al.* calls it **indirect prompt injection**.")
    text(card("greshake"))
    text("- First, the attacker hides instructions in data the application will retrieve.")
    text("- Then the user asks a normal question, and that data enters the model's context.")
    text("- Finally, the model may follow the hidden text. With tools, it can act on it.")
    text(figure("images/w13_greshake_fig3.png", "Numbered attack path from planted data to a compromised model.", "greshake", "Greshake et al., Figure 3. Follow the numbers.", width=460))
    text("The same path runs through code repositories, tool descriptions, and skill files. Next we ask why the model follows this text.")


def role_confusion():
    text("## 07 · Why the Model Follows: Role Confusion")
    text("Each message in a chat carries a role tag, such as user or tool. This work, *Prompt Injection as Role Confusion*, asks whether the model really relies on these tags.")
    text(card("roleconf"))
    text("- The authors use a probe to read which role the model assigns to each piece of text.")
    text("- They find that **writing style** matters more than the tag. Text written like the model's own reasoning is treated as its own reasoning, whatever its tag says.")
    text(figure("images/w13_roleconf_fig7.png", "Probe scores under three tag settings; reasoning style text stays high.", "roleconf", "Role Confusion, Figure 7. Orange marks text that was originally reasoning."))
    text("- They turn this into an attack by hiding reasoning style text in a web page. ASR means attack success rate, here the share of runs that leak private data.")
    text(figure("images/w13_roleconf_fig3.png", "Attack success rates of standard and forged reasoning injections.", "roleconf", "Role Confusion, Figure 3. Gray bars show standard injection, and pink bars show forged reasoning.", width=520))
    text("The pink bars are much higher. So a role tag alone does little to protect the agent. Next we want to know how often injection succeeds in real agent tasks.")


def agentdojo():
    text("## 08 · AgentDojo: Utility and Security")
    text("To measure this, we need agents with real tasks and tools. This work, *AgentDojo*, builds such an environment.")
    text(card("agentdojo"))
    text("- It has **97 user tasks** in email, Slack, travel, and banking, and **629 security test cases**.")
    text("- The attacker hides its goal in a tool result, for example asking the agent to leak an email.")
    text("- Each run gets a **utility** score for the user's task and a **security** score for the attacker's goal.")
    text(figure("images/w13_agentdojo_fig1.png", "AgentDojo with attacker goal, environment, user task, and the two metrics.", "agentdojo", "AgentDojo, Figure 1."))
    text("We need both scores, just as we checked both directions earlier. An agent that refuses everything is secure and useless. We will use this benchmark again for defenses.")


def agentharm():
    text("## 09 · AgentHarm: When the User Is the Attacker")
    text("In AgentDojo the user is honest. This work, *AgentHarm*, returns to the case where **the user is the attacker**, and the harmful task needs several tool calls.")
    text(card("agentharm"))
    text("- It has 110 harmful tasks in 11 categories, such as fraud and harassment, with synthetic tools.")
    text("- Each harmful task has a **matched benign task** with the same tools. This tells a refusal apart from a lack of skill.")
    text(figure("images/w13_agentharm_fig3.png", "Harmful and benign task scores per model.", "agentharm", "AgentHarm, Figure 3 (top). Red bars show harmful tasks under three settings, and green bars show benign tasks."))
    text("We compare bars within one model. When red gets close to green, the jailbreak lets the agent use **its full skill for harm**. Next we move from tools to the open web.")


def wasp():
    text("## 10 · WASP: Redirected Is Not Finished")
    text("On the web, anyone can write on a page. This work, *WASP*, tests web agents when an attacker controls part of a page.")
    text(card("wasp"))
    text("- In one example, the user asks for an upvote, and the page sends the agent to change the account email.")
    text("- The authors follow each run from the first action to the final state.")
    text(figure("images/w13_wasp_fig3.png", "Trajectories from the first action after injection to the final state.", "wasp", "WASP, Figure 3. Read left to right."))
    text("Many runs start toward the attacker's goal and then stall. Attacks **partly succeed** up to 86% of the time, and **fully succeed** at most 17%. So we report both numbers.")
    text("So far, every attack was tried a fixed number of times. Next we let the attacker keep trying.")


def attempts_and_budget():
    text("## 11 · More Attempts, More Violations")
    text("A real attacker can keep trying until something works. This work ran a public red teaming competition to measure this.")
    text(card("competition"))
    text("- People submitted 1.8 million attacks against 22 models in 44 scenarios, and over 60,000 caused a policy violation.")
    text(figure("images/w13_competition_fig4.png", "Attack success rate per model with 1, 10, and 100 attempts.", "competition", "Zou et al., Figure 4. The three shades show 1, 10, and 100 attempts."))
    text("Within one model, success rises quickly with more attempts. A quick calculation with **made up numbers** shows why. Suppose one attempt succeeds 2% of the time.")
    p = 0.02
    one_try = round(1 - (1 - p) ** 1, 3)  # @inspect one_try
    ten_tries = round(1 - (1 - p) ** 10, 3)  # @clear one_try @inspect ten_tries
    hundred_tries = round(1 - (1 - p) ** 100, 3)  # @clear ten_tries @inspect hundred_tries
    text(f"The attacker succeeds **{one_try:.0%}** of the time with one try, **{ten_tries:.0%}** with ten tries, and **{hundred_tries:.0%}** with a hundred.")  # @clear hundred_tries
    text("So every security number needs its **attack budget**. Now we turn to defenses.")


def camel_design():
    text("## 12 · CaMeL: Separate Planning from Reading")
    text("Training a model to ignore injected text helps, and attackers keep finding ways around it. This work, *CaMeL*, protects the agent through **system design**.")
    text(card("camel"))
    text("- The first part is a **privileged LLM**. It reads only the user's request and writes a plan as code.")
    text("- The second part is a **quarantined LLM**. It reads untrusted data and cannot call tools.")
    text("- The third part is an **interpreter**. It tracks where each value came from and checks a policy before each tool call.")
    text(figure("images/w13_camel_fig5.png", "CaMeL with privileged LLM, quarantined LLM, and interpreter.", "camel", "CaMeL, Figure 5."))
    text("Here is the idea in a few lines of Python, as **our own simplification**.")
    from_user = Value("bob@company.com", source="user")
    from_email = Value("eve@attacker.com", source="untrusted")
    allowed = may_send_email(from_user)  # @stepover @inspect allowed
    allowed = may_send_email(from_email)  # @stepover @inspect allowed
    text("The same call is allowed when the recipient comes from the user, and blocked when it comes from an email. Next we check whether this works.")  # @clear allowed


def camel_results():
    text("## 13 · CaMeL: Results on AgentDojo")
    text("The authors test CaMeL on *AgentDojo*. The right panel uses an uneven scale.")
    text(figure("images/w13_camel_fig9.png", "Utility under attack and number of successful attacks.", "camel", "CaMeL, Figure 9."))
    text("- CaMeL solves **77%** of tasks with provable security. An undefended agent solves **84%**.")
    text("- Successful attacks drop from over a hundred to a handful.")
    text("So CaMeL trades a little utility for a strong guarantee. These results use fixed attacks, though. Next we ask what happens when the attacker studies the defense first.")


def adaptive_attacks():
    text("## 14 · The Attacker Moves Second")
    text("A real attacker can study a defense and adapt. This work, *The Attacker Moves Second*, tests 12 published defenses this way.")
    text(card("ams"))
    text("- The attack runs in a loop. It proposes an attack, tests it, scores it, and improves it.")
    text(figure("images/w13_ams_fig2.png", "Adaptive attack loop.", "ams", "The Attacker Moves Second, Figure 2."))
    text(figure("images/w13_ams_fig1.png", "Attack success rates on 12 defenses under original and adaptive attacks.", "ams", "The Attacker Moves Second, Figure 1. Hatched bars show the original evaluation, and orange bars show the adaptive attack."))
    text("Most defenses first reported success rates near zero. Adaptive attacks pass most of them **over 90%** of the time. So we judge a defense by **the strongest attack it has faced**.")


def summary():
    text("## 15 · Summary")
    text("Let's put the pieces together.")
    text("- A model can **refuse too little** or **refuse too much**, so we measure both.")
    text("- Agents can be attacked through **anything they read**.")
    text("- Every result depends on the **attacker's access and budget**.")
    text("- Defenses work best when **built into the system** and tested against attackers who adapt.")
    text("We now have a clear way to answer our two questions. **What does the attacker control, and what did the experiment observe?**")


# Teaching sketch for Section 12 (our simplification of CaMeL)

@dataclass
class Value:
    data: str
    source: str  # "user" or "untrusted"


def may_send_email(recipient: Value) -> bool:
    # Policy: only send email to recipients that came from the user.
    return recipient.source == "user"
