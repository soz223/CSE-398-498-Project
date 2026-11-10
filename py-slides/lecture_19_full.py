from itertools import product
from edtrace import text
from lesson_demos import (STORIES, story, outcome_demo, budget_demo, vote_demo,
                          selection_demo, matching_demo, horizon_demo)


def main():

    text('## 01 · Agent Evaluation and Benchmarks')
    text('CSE 398/498 · Vibe Research for Scientific Discovery · Lichao Sun · Lehigh University')
    text('**Why evaluate agents?** An agent can say “Done” even when it changed the wrong thing. We need a way to check what actually happened.')
    text('An **evaluation** is a way to run a task, check the result, and record what happened.')
    text('A **benchmark** gives us a set of tasks and a shared scoring rule so we can compare systems on the same work.')
    text('If one agent gets a higher score, ask what it did better. Did it finish more tasks, use fewer attempts, or just get a better grade?')

    text('## 02 · Today’s Plan')
    text('Check one task')
    text('- Decide what the agent needs to do and what evidence would show it succeeded.')
    text('Compare two agents')
    text('- Give both agents the same tasks. Repeat the runs and check the cost.')
    text('Read rankings and graders')
    text('- See how human votes turn into a leaderboard and how a model can grade a result.')
    text('- Check what each benchmark measures before you use its score.')

    text('## 03 · What Is Task Success?')
    text('Before we compare two agents, we need a rule for scoring one task. Say a customer asks to cancel booking A and keep booking B.')
    text('- The agent says “I canceled A.” Both bookings are still active. **Fail.**')
    text('- Booking A is canceled, but booking B is also gone. **Fail.**')
    text('- Booking A is canceled and booking B is still active. **Pass.**')
    text('The reply tells us what the agent claims. The booking records tell us what actually changed.')
    text('<div class="lesson-cite"><a href="#ref-1" aria-label="Reference 1: τ²-Bench: Evaluating Conversational Agents in a Dual-Control Environment">[1]</a> Course synthesis grounded in tau squared benchmark task evaluation, ICML 2026</div>')

    text('## 04 · *τ²-Bench*')
    text('*τ²-Bench* (say “tau squared bench”) is a customer support test. It gives the agent a request, a set of rules, and tools it can use to help. The customer is simulated, so the researchers can run the test again.')
    text('- In retail, the agent handles orders and returns. In airline support, it handles bookings.')
    text('- In phone support, the customer can also act. For example, the agent asks the customer to turn off airplane mode. The customer changes the setting and reports what happens.')
    text('The figure shows the two sides. The agent can use support tools. The customer can use phone tools. **They have to talk to each other to solve the task.**')
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_tau_setup.png"><img src="images/w12_tau_setup.png" alt="The support agent and simulated customer talk to each other and use their own tools."><span>Enlarge figure ↗</span></button></div><figcaption class="lesson-cite"><a href="#ref-1">[1]</a> Figure 1 from the authors’ <a href="https://arxiv.org/html/2506.07982v1#S1.F1" target="_blank" rel="noopener noreferrer">τ²-Bench preprint</a> · CC BY 4.0</figcaption></figure>')
    text('After the chat, the benchmark checks what happened. The next slide shows how it scores one airline request.')
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_04_02.png"><img src="images/w12_04_02.png" alt="τ²-Bench · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-1" aria-label="Reference 1: τ²-Bench: Evaluating Conversational Agents in a Dual-Control Environment">[1]</a> Barres et al. · ICML 2026 · PMLR 306, pp. 6736–6782</div></figure>')

    text('## 05 · When an Agent Should Say No')
    text('Let’s apply that idea to an airline task from *τ²-Bench*. On the last slide we wanted the booking changed. Here the airline policy says this booking cannot be canceled.')
    text('The *τ²-Bench Airline Tasks* repository shows how this rule is stored in a real task record. In this example, a correct agent refuses the request and leaves the booking unchanged.')
    text('In this task, the agent should explain why it cannot cancel the booking and leave the booking as it is.')
    text('DB checks the booking record. COMMUNICATE checks what the user was told. nl_assertions hold checks written in plain language.')
    text('<figure class="lesson-figure"><div class="source-code"><strong>Airline task 0 · JSON excerpt</strong><pre><code>{\n  &quot;id&quot;: &quot;0&quot;,\n  &quot;evaluation_criteria&quot;: {\n    &quot;actions&quot;: [],\n    &quot;communicate_info&quot;: [],\n    &quot;nl_assertions&quot;: [\n      &quot;Agent should refuse to proceed with the cancellation.&quot;\n    ],\n    &quot;reward_basis&quot;: [\n      &quot;DB&quot;,\n      &quot;COMMUNICATE&quot;\n    ]\n  }\n}</code></pre></div><details><summary>View original source image</summary><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_05_02.png"><img src="images/w12_05_02.png" alt="Success Can Mean Refusing an Invalid Action · image 1"><span>Enlarge figure ↗</span></button></div></details><div class="lesson-cite"><a href="#ref-2" aria-label="Reference 2: τ²-Bench Airline Tasks">[2]</a> Sierra Research · Benchmark repository</div></figure><article id="ref-2" class="reference-card"><img src="images/w12_05_02.png" alt="" loading="lazy"><div><h3>[2] τ²-Bench Airline Tasks</h3><p class="reference-meta">Sierra Research · Benchmark repository</p><p>Task records and success criteria for the airline domain.</p><div class="reference-links"><a href="https://github.com/sierra-research/tau2-bench/blob/main/data/tau2/domains/airline/tasks.json" target="_blank" rel="noopener noreferrer">Open source ↗</a></div></div></article>')

    text('## 06 · One Win or Every Run?')
    text('We know how to grade one run. Now reset the booking and give the agent the same request four times. Does it say no every time?')
    text('Suppose it refuses three times and cancels the booking once. It got the task right at least once, but it did not get it right every time.')
    text('- pass@k asks whether at least one of k attempts succeeds.')
    text('- pass^k asks whether all k attempts succeed.')
    text('- At k = 1, both ask whether that one attempt succeeds.')
    outcomes = list(product((False, True), repeat=4))
    any_rate = sum(map(any, outcomes)) / len(outcomes)  # @inspect any_rate
    all_rate = sum(map(all, outcomes)) / len(outcomes)  # @inspect all_rate
    text(outcome_demo(outcomes, any_rate, all_rate))
    text('<div class="lesson-cite"><a href="#ref-1" aria-label="Reference 1: τ²-Bench: Evaluating Conversational Agents in a Dual-Control Environment">[1]</a> τ²-Bench, ICML 2026 (evaluation metrics)</div>')

    text('## 07 · Success Across Runs')
    text('The booking example used made up runs. This table shows the paper’s results. Read across each row to see how often GPT 4.1 passed every run as the number of runs increased.')
    text('- Retail: orders and returns. Airline: bookings. Telecom: service troubleshooting.')
    text('- pass^k requires success in every one of k runs.')
    text('<figure class="lesson-figure"><div class="source-table"><table><caption>Figure 3 · GPT-4.1 repeated success</caption><thead><tr><th scope=\'col\'>Domain</th><th scope=\'col\'>k = 1</th><th scope=\'col\'>k = 2</th><th scope=\'col\'>k = 3</th><th scope=\'col\'>k = 4</th></tr></thead><tbody><tr><td>Retail</td><td>74%</td><td>64%</td><td>58%</td><td>53%</td></tr><tr><td>Airline</td><td>56%</td><td>46%</td><td>42%</td><td>40%</td></tr><tr><td>Telecom</td><td>34%</td><td>26%</td><td>22%</td><td>19%</td></tr></tbody></table></div><details><summary>View original source image</summary><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_07_02.png"><img src="images/w12_07_02.png" alt="τ²-Bench: Reliability Across Repeated Runs · image 1"><span>Enlarge figure ↗</span></button></div></details><div class="lesson-cite"><a href="#ref-1" aria-label="Reference 1: τ²-Bench: Evaluating Conversational Agents in a Dual-Control Environment">[1]</a> τ²-Bench, ICML 2026 (Figure 3, original experimental results)</div></figure><article id="ref-1" class="reference-card"><img src="images/w12_07_02.png" alt="" loading="lazy"><div><h3>[1] τ²-Bench: Evaluating Conversational Agents in a Dual-Control Environment</h3><p class="reference-meta">Barres et al. · ICML 2026 · PMLR 306, pp. 6736–6782</p><p>Repeated success and the effects of user coordination.</p><div class="reference-links"><a href="https://proceedings.mlr.press/v306/barres26a.html" target="_blank" rel="noopener noreferrer">Open source ↗</a></div></div></article>')

    text('## 08 · Who Controls the Tools?')
    text('The phone support scores are lower. Can we tell whether the agent struggled to find a fix or to guide the customer through it?')
    text('- In the default setup, the user and agent each have tools. In the no user setup, the agent controls both sides.')
    text('- With an oracle plan, the agent gets the correct steps in advance.')
    text('- Left: original policy. Right: policy with a workflow.')
    text(story(STORIES[8][0], *STORIES[8][1]))
    text('<figure class="lesson-figure"><section class="lesson-demo" aria-label="Telecom pass¹ across evaluation modes"><h3>Telecom pass¹ across evaluation modes</h3><p class="demo-kicker">Published results · transcribed from Figure 4</p><div class="demo-controls"><button type="button" data-frame="0" aria-pressed="true">Original policy</button><button type="button" data-frame="1" aria-pressed="false">Policy with workflow</button></div><div class="demo-panel" data-panel="0"><div class="source-table"><table><caption>Figure 4 · Original policy</caption><thead><tr><th scope=\'col\'>Mode</th><th scope=\'col\'>GPT-4.1</th><th scope=\'col\'>o4-mini</th></tr></thead><tbody><tr><td>Default</td><td>34%</td><td>42%</td></tr><tr><td>No user</td><td>52%</td><td>67%</td></tr><tr><td>Oracle plan</td><td>73%</td><td>96%</td></tr></tbody></table></div></div><div class="demo-panel" data-panel="1" hidden><div class="source-table"><table><caption>Figure 4 · Policy with workflow</caption><thead><tr><th scope=\'col\'>Mode</th><th scope=\'col\'>GPT-4.1</th><th scope=\'col\'>o4-mini</th></tr></thead><tbody><tr><td>Default</td><td>52%</td><td>59%</td></tr><tr><td>No user</td><td>68%</td><td>72%</td></tr><tr><td>Oracle plan</td><td>57%</td><td>88%</td></tr></tbody></table></div></div></section><details><summary>View original source image</summary><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_08_02.png"><img src="images/w12_08_02.png" alt="τ²-Bench: Reasoning and User Coordination · image 1"><span>Enlarge figure ↗</span></button><button type="button" class="figure-thumb" data-figure="images/w12_08_03.png"><img src="images/w12_08_03.png" alt="τ²-Bench: Reasoning and User Coordination · image 2"><span>Enlarge figure ↗</span></button></div></details><div class="lesson-cite"><a href="#ref-1" aria-label="Reference 1: τ²-Bench: Evaluating Conversational Agents in a Dual-Control Environment">[1]</a> τ²-Bench, ICML 2026 (Figure 4, original Telecom ablation)</div></figure>')

    text('## 09 · *AI Agents That Matter*')
    text('We now know how to count successes across runs. To choose between two agents, we also need to know what each run costs.')
    text('*AI Agents That Matter* studies how agents are compared. Its authors examine accuracy and cost together, compare agent designs with simple baselines, and ask whether benchmarks hold out the right tasks. We will use the paper to read a coding result in context.')
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_09_01.png"><img src="images/w12_09_01.png" alt="AI Agents That Matter · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-3" aria-label="Reference 3: AI Agents That Matter">[3]</a> Kapoor et al. · TMLR 2025</div></figure>')

    text('## 10 · Simple Baselines')
    text('Before adding more steps or more tools, compare your system with something simple. How far can a retry get you?')
    text('- Retry: ask the model again.')
    text('- Warming: increase the sampling temperature.')
    text('- Escalation: use a stronger model after failure.')
    text('- Compare systems under a similar budget.')
    text(story(STORIES[10][0], *STORIES[10][1]))
    text('<div class="lesson-cite"><a href="#ref-3" aria-label="Reference 3: AI Agents That Matter">[3]</a> AI Agents That Matter, TMLR 2025; 2024 preprint (Sections 2.2 and 2.3)</div>')

    text('## 11 · Accuracy and Cost on *HumanEval*')
    text('Now look at an actual coding test. Find the agents that solve more problems and check what each one costs.')
    text('- *HumanEval*: short Python functions.')
    text('- LDB = Large Language Model Debugger.')
    text('- LATS = Language Agent Tree Search.')
    text('- Five runs across 164 problems.')
    text('- USD = United States dollars.')
    runs = [('A', 0.70, 2), ('B', 0.80, 9)]  # accuracy and cents per task
    eligible = [(name, score) for name, score, cents in runs if cents <= 5]
    text(budget_demo([(name, score) for name, score, _ in runs], eligible))
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_11_01.png"><img src="images/w12_11_01.png" alt="Accuracy and Cost on HumanEval · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-3" aria-label="Reference 3: AI Agents That Matter">[3]</a> AI Agents That Matter, TMLR 2025; 2024 preprint (Figure 1; April 2024 prices; note the broken axes)</div></figure><article id="ref-3" class="reference-card"><img src="images/w12_11_01.png" alt="" loading="lazy"><div><h3>[3] AI Agents That Matter</h3><p class="reference-meta">Kapoor et al. · TMLR 2025</p><p>Cost, simple baselines, holdout sets, and reliable agent comparisons.</p><div class="reference-links"><a href="https://openreview.net/forum?id=Zy4uFzMviZ" target="_blank" rel="noopener noreferrer">Open source ↗</a><a href="https://arxiv.org/abs/2407.01502" target="_blank" rel="noopener noreferrer">View preprint ↗</a></div></div></article>')

    text('## 12 · Testing on New Tasks')
    text('A fair budget helps, but the test cases matter too. If the agent was built around the same tasks, try it on fresh ones.')
    text('- The study sorts 17 agent benchmarks into four levels of generality.')
    text('- To claim an agent works on new kinds of tasks, test it on tasks it did not see during development.')
    text(story(STORIES[12][0], *STORIES[12][1]))
    text('<figure class="lesson-figure"><div class="source-table"><table><caption>Appropriate holdouts in the 17 benchmarks surveyed</caption><thead><tr><th scope=\'col\'>Generality</th><th scope=\'col\'>What should be held out?</th><th scope=\'col\'>Benchmarks</th></tr></thead><tbody><tr><td>Distribution-specific</td><td>In-distribution samples</td><td>1 / 1</td></tr><tr><td>Task-specific</td><td>Out-of-distribution samples</td><td>3 / 6</td></tr><tr><td>Domain-general</td><td>Tasks</td><td>1 / 8</td></tr><tr><td>Fully general</td><td>Domains</td><td>0 / 2</td></tr><tr><td>All benchmarks</td><td>7 had no holdout and no stated plan to add one</td><td>5 / 17</td></tr></tbody></table></div><details><summary>View original source image</summary><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_12_02.png"><img src="images/w12_12_02.png" alt="Test Sets and Claims About Generalization · image 1"><span>Enlarge figure ↗</span></button></div></details><div class="lesson-cite"><a href="#ref-3" aria-label="Reference 3: AI Agents That Matter">[3]</a> Kapoor et al. · TMLR 2025</div></figure>')

    text('## 13 · Why Did the Run Fail?')
    text('After you compare the scores, open a few failed runs. Find the first place where the run went wrong.')
    text('- Did the agent fail, or did the environment fail?')
    text('- Were the inputs, budget, and evaluator comparable?')
    text('- Did we run it enough times to see how much the score changes?')
    text('- Were the raw traces saved for inspection?')
    text('<div class="lesson-cite"><a href="#ref-3" aria-label="Reference 3: AI Agents That Matter">[3]</a> AI Agents That Matter, TMLR 2025; 2024 preprint (Section 6); practical synthesis</div>')

    text('## 14 · Votes, Judges, and Outcomes')
    text('**Now let’s look at rankings and graders.** For some tasks we can check the result directly. For others we ask a person or a model to judge the answer.')
    text('- Human votes measure which answer people prefer.')
    text('- A model judge applies a grading rule.')
    text('- Task success requires a clear check of the requested outcome.')

    text('## 15 · *Chatbot Arena*')
    text('*Chatbot Arena* lets users send a prompt to two anonymous models and vote on the answers. The paper shows how those votes become a ranking. We will look at what information the ranking keeps and what it leaves out.')
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_15_01.png"><img src="images/w12_15_01.png" alt="Chatbot Arena · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-4" aria-label="Reference 4: Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference">[4]</a> Chiang et al. · ICML 2024</div></figure>')

    text('## 16 · Right Answers and User Votes')
    text('- If a question has a known answer, we can check it directly.')
    text('- Some prompts allow several good answers. A vote tells us which one a person prefers.')
    text('- Scores on fixed tests can look better if models have seen the questions or if many models already score near the top.')
    text('- *MMLU* and *GSM8K* are examples of fixed tests. *HellaSwag* tests commonsense completion.')
    text('- *MT Bench* and *AlpacaEval* look at how models respond to instructions.')
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_16_01.png"><img src="images/w12_16_01.png" alt="Benchmarks for Correctness and Human Preference · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-4" aria-label="Reference 4: Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference">[4]</a> Chiang et al. · ICML 2024</div></figure>')

    text('## 17 · Voting in *Chatbot Arena*')
    text(story(STORIES[17][0], *STORIES[17][1]))
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_17_02.png"><img src="images/w12_17_02.png" alt="Chatbot Arena: Voting Rules · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-4" aria-label="Reference 4: Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference">[4]</a> Chiang et al. · ICML 2024</div></figure><article id="ref-4" class="reference-card"><img src="images/w12_17_02.png" alt="" loading="lazy"><div><h3>[4] Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference</h3><p class="reference-meta">Chiang et al. · ICML 2024</p><p>Blind pairwise comparisons and preference scores.</p><div class="reference-links"><a href="https://proceedings.mlr.press/v235/chiang24b.html" target="_blank" rel="noopener noreferrer">Open source ↗</a></div></div></article>')

    text('## 18 · From Votes to Scores')
    text('Bradley-Terry (BT) model')
    text('- Each model m has a score ξm.')
    text('- Score differences determine the probability of winning a comparison.')
    text('- Human vote: Ht is 0 or 1.')
    text('- Arena fits a Bradley-Terry coefficient, previously called an Elo score.')
    text('- A ranking is harder to pin down when some pairs get few votes.')
    wins, losses = 6, 4
    fitted_probability = wins / (wins + losses)  # @inspect fitted_probability
    text(vote_demo(wins, losses, fitted_probability))
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_18_01.png"><img src="images/w12_18_01.png" alt="Chatbot Arena: Scores from Pairwise Votes · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-4" aria-label="Reference 4: Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference">[4]</a> Chiang et al. · ICML 2024</div></figure>')

    text('## 19 · *The Leaderboard Illusion*')
    text('We have seen how votes become a rank. But which versions of a model do users actually get to see?')
    text('*The Leaderboard Illusion* examines how private testing and selective reporting can affect public rankings. If providers can test several variants and release only the best one, they have more chances to post a high score.')
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_19_01.png"><img src="images/w12_19_01.png" alt="The Leaderboard Illusion · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-5" aria-label="Reference 5: The Leaderboard Illusion">[5]</a> Singh et al. · NeurIPS 2025 · Datasets and Benchmarks</div></figure>')

    text('## 20 · Which Models Get Reported?')
    text('- Private testing lets a provider publish only its best variant.')
    text('- Small dots are private variants. The large dot is the published one.')
    text('- The authors suggest limiting how many versions can enter and recording why any version was removed.')
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_20_02.png"><img src="images/w12_20_02.png" alt="Private Testing and Selective Score Reporting · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-5" aria-label="Reference 5: The Leaderboard Illusion">[5]</a> Singh et al. · NeurIPS 2025 · Datasets and Benchmarks</div></figure>')

    text('## 21 · Picking the Highest Score')
    text('- In this simulation, the underlying mean stays at 1200.')
    text('- Testing more private variants creates more chances to select a high score.')
    scores = [0.68, 0.73, 0.69, 0.76, 0.71]
    selected = max(scores)  # @inspect selected
    text(selection_demo(scores, selected))
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_21_01.png"><img src="images/w12_21_01.png" alt="Selecting the Best Variant Inflates the Score · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-5" aria-label="Reference 5: The Leaderboard Illusion">[5]</a> The Leaderboard Illusion, NeurIPS 2025 (Figure 7; simulation, not a live model ranking)</div></figure><article id="ref-5" class="reference-card"><img src="images/w12_21_01.png" alt="" loading="lazy"><div><h3>[5] The Leaderboard Illusion</h3><p class="reference-meta">Singh et al. · NeurIPS 2025 · Datasets and Benchmarks</p><p>Private testing and selective reporting of model variants.</p><div class="reference-links"><a href="https://papers.nips.cc/paper_files/paper/2025/file/70a93f260a51123b3c0e33ecd1b4de97-Paper-Datasets_and_Benchmarks_Track.pdf" target="_blank" rel="noopener noreferrer">Open source ↗</a></div></div></article>')

    text('## 22 · What Does the Score Tell Us?')
    text('A ranking tells us which answers people liked. For our own tests, collecting votes for every answer can be slow. Can we ask a model to grade them instead?')
    text('- Which answer did users prefer?')
    text('- Did the agent finish the task?')
    text('- Does it still work on tasks it hasn’t seen?')
    text('<div class="lesson-cite"><a href="#ref-4" aria-label="Reference 4: Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference">[4]</a> Chatbot Arena, ICML 2024; AI Agents That Matter, TMLR 2025; course synthesis</div>')

    text('## 23 · LLMs as Judges')
    text('*Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena* compares model judgments with human preferences. The paper also examines how the order and presentation of answers can affect the judge. We will read the prompt and see what we need to check before using it.')
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_23_01.png"><img src="images/w12_23_01.png" alt="Judging LLM as a Judge · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-6" aria-label="Reference 6: Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena">[6]</a> Zheng et al. · NeurIPS 2023</div></figure>')

    text('## 24 · A Judge Prompt')
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_24_02.png"><img src="images/w12_24_02.png" alt="The Default Pairwise Judge Prompt · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-6" aria-label="Reference 6: Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena">[6]</a> Zheng et al. · NeurIPS 2023</div></figure><article id="ref-6" class="reference-card"><img src="images/w12_24_02.png" alt="" loading="lazy"><div><h3>[6] Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena</h3><p class="reference-meta">Zheng et al. · NeurIPS 2023</p><p>Pairwise grading prompts and judge bias.</p><div class="reference-links"><a href="https://papers.nips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html" target="_blank" rel="noopener noreferrer">Open source ↗</a></div></div></article>')

    text('## 25 · Check Your Judge')
    text('- Start with cases that people have checked.')
    text('- Swap the answer order and inspect disagreements.')
    text('- Count cases the judge wrongly passes and wrongly fails separately.')
    text('- Save the rubric and the judge version.')
    text(story(STORIES[25][0], *STORIES[25][1]))
    text('<div class="lesson-cite"><a href="#ref-6" aria-label="Reference 6: Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena">[6]</a> Judging LLM as a Judge with MT Bench and Chatbot Arena, NeurIPS 2023; practical synthesis</div>')

    text('## 26 · Grading Digital Agents')
    text('Think back to the booking record. A reply alone did not tell us whether the booking changed. When an app gives us no database access, screenshots can show what changed.')
    text('*Autonomous Evaluation and Refinement of Digital Agents* studies how to grade digital tasks from evidence such as screenshots. Its evaluators ask whether the requested outcome happened, which helps when several different action sequences can solve the same task.')
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_26_01.png"><img src="images/w12_26_01.png" alt="Autonomous Evaluation of Digital Agents · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-7" aria-label="Reference 7: Autonomous Evaluation and Refinement of Digital Agents">[7]</a> Pan et al. · COLM 2024</div></figure>')

    text('## 27 · Grading from Screenshots')
    text('- VLM = vision language model.')
    text('- The evaluator reads screenshots to judge whether the task finished.')
    text('- The paper reports higher accuracy with a more expensive evaluator.')
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_27_01.png"><img src="images/w12_27_01.png" alt="Judging Task Completion from Screenshots · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-7" aria-label="Reference 7: Autonomous Evaluation and Refinement of Digital Agents">[7]</a> Pan et al. · COLM 2024</div></figure>')

    text('## 28 · Two Ways to Read Screenshots')
    text('- Modular: describe the screenshots, then ask a language model.')
    text('- End to end: a vision language model reads the screenshots.')
    text('- VLM = vision language model. LM = language model.')
    text(story(STORIES[28][0], *STORIES[28][1]))
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_28_02.png"><img src="images/w12_28_02.png" alt="Modular and End to End Evaluators · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-7" aria-label="Reference 7: Autonomous Evaluation and Refinement of Digital Agents">[7]</a> Pan et al. · COLM 2024</div></figure><article id="ref-7" class="reference-card"><img src="images/w12_28_02.png" alt="" loading="lazy"><div><h3>[7] Autonomous Evaluation and Refinement of Digital Agents</h3><p class="reference-meta">Pan et al. · COLM 2024</p><p>Compare action matching with checks of completed tasks.</p><div class="reference-links"><a href="https://openreview.net/forum?id=NPAQ6FKSmK" target="_blank" rel="noopener noreferrer">Open source ↗</a><a href="https://nlp.cs.berkeley.edu/pubs/Pan-Zhang-Tomlin-Zhou-Levine-Suhr_2024_Autonomous_paper.pdf" target="_blank" rel="noopener noreferrer">Paper PDF ↗</a></div></div></article>')

    text('## 29 · Matching Actions vs. Finishing')
    text('We have two ways to read screenshots. Now see why the final screen can tell a different story from a list of clicks.')
    text('- AitW = Android in the Wild. Task: follow an instruction in a phone app.')
    text('- Parentheses: action matching. Bars: task success judged by each evaluator.')
    action_scores = [('Trace A', 4 / 4), ('Trace B', 2 / 4)]
    outcome_scores = [('Trace A', 0), ('Trace B', 1)]
    text(matching_demo(action_scores, outcome_scores))
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_29_01.png"><img src="images/w12_29_01.png" alt="Action Matching Can Give the Wrong Ranking · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-7" aria-label="Reference 7: Autonomous Evaluation and Refinement of Digital Agents">[7]</a> Autonomous Evaluation and Refinement of Digital Agents, COLM 2024 (Figure 2)</div></figure>')

    text('## 30 · Differences Between Benchmarks')
    text('We have looked at several ways to grade a task. **Now pick the kind of work to test.** A score on hard questions tells us something different from a score on office tasks.')
    text('- HLE checks answers to questions written by experts.')
    text('- METR looks at how success changes as software tasks take humans longer to finish.')
    text('- *TheAgentCompany* checks work across tools in a simulated company.')

    text("## 31 · *Humanity's Last Exam*")
    text('*Humanity’s Last Exam* is a collection of expert questions with verifiable answers across many subjects. It tests how well models answer difficult academic questions. We will compare that kind of evidence with evidence from longer agent tasks.')
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_31_01.png"><img src="images/w12_31_01.png" alt="Humanity&#x27;s Last Exam · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-8" aria-label="Reference 8: A benchmark of expert-level academic questions to assess AI capabilities">[8]</a> Center for AI Safety, Scale AI &amp; HLE Contributors Consortium · Nature 649, 1139–1146 (2026)</div></figure>')

    text('## 32 · How HLE Was Built')
    text('- 2,500 public questions across more than 100 subjects, plus a private test set.')
    text('- Nearly 1,000 contributors from over 500 institutions across 50 countries.')
    text('- Released in January 2025 and published in Nature on 28 January 2026.')
    text(story(STORIES[32][0], *STORIES[32][1]))
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_32_02.png"><img src="images/w12_32_02.png" alt="HLE: Building the Question Set · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-8" aria-label="Reference 8: A benchmark of expert-level academic questions to assess AI capabilities">[8]</a> Center for AI Safety, Scale AI &amp; HLE Contributors Consortium · Nature 649, 1139–1146 (2026)</div></figure><article id="ref-8" class="reference-card"><img src="images/w12_32_02.png" alt="" loading="lazy"><div><h3>[8] A benchmark of expert-level academic questions to assess AI capabilities</h3><p class="reference-meta">Center for AI Safety, Scale AI &amp; HLE Contributors Consortium · Nature 649, 1139–1146 (2026)</p><p>Humanity&#x27;s Last Exam and its expert question review process.</p><div class="reference-links"><a href="https://www.nature.com/articles/s41586-025-09962-4" target="_blank" rel="noopener noreferrer">Open source ↗</a><a href="https://arxiv.org/abs/2501.14249" target="_blank" rel="noopener noreferrer">View preprint ↗</a></div></div></article>')

    text('## 33 · What HLE Can Tell Us')
    text("HLE = *Humanity's Last Exam*")
    text('- Questions have verifiable answers.')
    text('- Report the tools, attempts, and calibration.')
    text('- To see whether an agent can carry out a research workflow, test that workflow directly.')
    text('<div class="lesson-cite"><a href="#ref-8" aria-label="Reference 8: A benchmark of expert-level academic questions to assess AI capabilities">[8]</a> Humanity&#x27;s Last Exam, Nature 2026; arXiv 2501.14249 (scope and limitations)</div>')

    text('## 34 · Long Software Tasks')
    text('HLE checks the final answer to a question. For software work, we can also ask how often an agent finishes tasks that take a human longer.')
    text('*Measuring AI Ability to Complete Long Software Tasks* groups tasks by how long a human takes and fits agent success against that duration. This gives us a way to talk about task length using a common reference.')
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_34_01.png"><img src="images/w12_34_01.png" alt="Long Software Tasks · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-9" aria-label="Reference 9: Measuring AI Ability to Complete Long Software Tasks">[9]</a> Kwa et al. · NeurIPS 2025</div></figure>')

    text('## 35 · What Is a Time Horizon?')
    text('- HCAST = Human Calibrated Autonomy Software Tasks.')
    text('- SWAA = Software Atomic Actions. *RE Bench* = Research Engineering Benchmark.')
    text('- SWE = software engineering. R&D = research and development.')
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_35_01.png"><img src="images/w12_35_01.png" alt="METR: Estimating the Time Horizon · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-9" aria-label="Reference 9: Measuring AI Ability to Complete Long Software Tasks">[9]</a> Measuring AI Ability to Complete Long Software Tasks, NeurIPS 2025 (Figure 2)</div></figure>')

    text('## 36 · Success by Task Length')
    text('Find where the curve crosses 50%. At that task length, the fitted curve says the agent succeeds about half the time.')
    text('- METR = Model Evaluation and Threat Research.')
    text('- Horizontal axis: human task time.')
    text('- Vertical axis: success probability.')
    text('- 50% horizon: about 54 minutes.')
    text('- 90% reliability gives a shorter horizon.')
    minutes = list(range(0, 61, 5))
    probabilities = [1 / (1 + (t / 30) ** 1.4) for t in minutes]
    crossings = [t for t, p in zip(minutes, probabilities) if p <= 0.5]
    horizon = min(crossings)  # @inspect horizon
    text(horizon_demo(minutes, probabilities, horizon))
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_36_01.png"><img src="images/w12_36_01.png" alt="METR: Success Probability and Human Task Time · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-9" aria-label="Reference 9: Measuring AI Ability to Complete Long Software Tasks">[9]</a> Measuring AI Ability to Complete Long Software Tasks, NeurIPS 2025 (Figure 4, selected panel)</div></figure><article id="ref-9" class="reference-card"><img src="images/w12_36_01.png" alt="" loading="lazy"><div><h3>[9] Measuring AI Ability to Complete Long Software Tasks</h3><p class="reference-meta">Kwa et al. · NeurIPS 2025</p><p>Relate task success to the time a human expert needs.</p><div class="reference-links"><a href="https://proceedings.neurips.cc/paper_files/paper/2025/hash/85069585133c4c168c865e65d72e9775-Abstract-Conference.html" target="_blank" rel="noopener noreferrer">Open source ↗</a></div></div></article>')

    text('## 37 · Checking Coding Tasks')
    text('Before comparing coding scores, check that the tasks and tests work as intended.')
    text('*Separating signal from noise in coding evaluations* describes a review of public coding tasks and their tests. It gives us an example of how to examine the benchmark itself when an evaluation result looks wrong.')
    text('- 731 public tasks. Agent assisted review: 200 broken. Human review: 249 broken.')
    text('- Detailed review followed screening. This is an audit of flagged tasks.')
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_37_01.png"><img src="images/w12_37_01.png" alt="Codex: Auditing Coding Benchmark Tasks · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-10" aria-label="Reference 10: Separating signal from noise in coding evaluations">[10]</a> OpenAI, Separating signal from noise in coding evaluations, Jul 2026 (original methodology figure)</div></figure><article id="ref-10" class="reference-card"><img src="images/w12_37_01.png" alt="" loading="lazy"><div><h3>[10] Separating signal from noise in coding evaluations</h3><p class="reference-meta">OpenAI · 2026</p><p>Audit the tasks and tests behind software benchmark scores.</p><div class="reference-links"><a href="https://openai.com/index/separating-signal-from-noise-coding-evaluations/" target="_blank" rel="noopener noreferrer">Open source ↗</a></div></div></article>')

    text('## 38 · What to Save')
    text('- Task files and the success check.')
    text('- Agent, environment, budget, and baseline.')
    text('- Repeated runs, traces, and failure types.')
    text('- Grader version, calibration, and the task audit.')
    text(story(STORIES[38][0], *STORIES[38][1]))
    text('<div class="lesson-cite"><a href="#ref-10" aria-label="Reference 10: Separating signal from noise in coding evaluations">[10]</a> Practical synthesis from the research papers and the OpenAI July 2026 audit</div>')

    text('## 39 · Optional: *TheAgentCompany*')
    text('Here’s one more example if we have time. What happens when a task spans several workplace tools?')
    text('*TheAgentCompany* places agents in a simulated company with workplace tools and tasks. Some tasks need several tools, and the benchmark can award credit for intermediate milestones. We will see how full success and partial credit tell different stories.')
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_39_01.png"><img src="images/w12_39_01.png" alt="Optional: TheAgentCompany · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-11" aria-label="Reference 11: TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks">[11]</a> Xu et al. · NeurIPS 2025 · Datasets and Benchmarks</div></figure>')

    text('## 40 · Workplace Tasks')
    text('- 175 tasks in a reproducible, simulated workplace.')
    text('- Evaluation checks the work state and the required milestones.')
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_40_01.png"><img src="images/w12_40_01.png" alt="TheAgentCompany: Tasks Across Workplace Tools · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-11" aria-label="Reference 11: TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks">[11]</a> Xu et al. | NeurIPS 2025 | Figure 1 | Original benchmark design</div></figure><article id="ref-11" class="reference-card"><img src="images/w12_40_01.png" alt="" loading="lazy"><div><h3>[11] TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks</h3><p class="reference-meta">Xu et al. · NeurIPS 2025 · Datasets and Benchmarks</p><p>Workplace tasks that span tools and score intermediate milestones.</p><div class="reference-links"><a href="https://papers.nips.cc/paper_files/paper/2025/file/0d744742f6fac4d1134c019b7cef3c8a-Paper-Datasets_and_Benchmarks_Track.pdf" target="_blank" rel="noopener noreferrer">Open source ↗</a></div></div></article>')

    text('## 41 · Full and Partial Credit')
    text('- SDE in the figure: software engineering. PM = project management.')
    text('- DS = data science. Admin = administration. HR = human resources.')
    text('<figure class="lesson-figure"><div class="source-table"><table><caption>Table 1 · OpenHands 0.28.1 with Gemini 2.5 Pro</caption><thead><tr><th scope=\'col\'>Scoring rule</th><th scope=\'col\'>Reported score</th></tr></thead><tbody><tr><td>Full task success</td><td>30.3%</td></tr><tr><td>With partial credit</td><td>39.3%</td></tr></tbody></table></div><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_41_01.png"><img src="images/w12_41_01.png" alt="TheAgentCompany: Results by Platform and Task · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-11" aria-label="Reference 11: TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks">[11]</a> Xu et al. | NeurIPS 2025 | Figure 2 | Tested model versions in the paper</div></figure>')

    text('## 42 · What to Check Before You Trust a Score')
    text('- Define a clear success condition.')
    text('- Use fair comparisons and repeated runs.')
    text('- Check the evaluator itself.')
    text('- Keep the claim within the tested setting.')

    text('## 43 · Thank you')
