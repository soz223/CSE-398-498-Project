from itertools import product
from edtrace import text
from lesson_demos import (STORIES, story, outcome_demo, budget_demo, vote_demo,
                          selection_demo, matching_demo, horizon_demo)


def main():

    text('## 01 · Agent Evaluation and Benchmarks')
    text('CSE 398/498 · Vibe Research for Scientific Discovery · Lichao Sun · Lehigh University')

    text("## 02 · Today's Plan")
    text('Learning goal\n- Understand what an agent benchmark score actually measures.\nPapers and evaluations\n- τ²-Bench and AI Agents That Matter for reliability and cost.\n- Chatbot Arena and model judges for preferences and grading.\n- HLE, METR, and TheAgentCompany for different kinds of tasks.\nHow we will read the evidence\n- Check the success rule, repeated runs, evaluator, and task coverage.')

    text('## 03 · What Counts as Task Success?')
    text('- The agent says it finished.\n- The trace records what it tried.\n- The environment shows whether the requested change happened.')
    text(story(STORIES[3][0], *STORIES[3][1]))
    text('<div class="lesson-cite"><a href="#ref-1" aria-label="Reference 1: τ²-Bench: Evaluating Conversational Agents in a Dual-Control Environment">[1]</a> Course synthesis grounded in tau squared benchmark task evaluation, ICML 2026</div>')

    text('## 04 · τ²-Bench')
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_04_02.png"><img src="images/w12_04_02.png" alt="τ²-Bench · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-1" aria-label="Reference 1: τ²-Bench: Evaluating Conversational Agents in a Dual-Control Environment">[1]</a> Barres et al. · ICML 2026 · PMLR 306, pp. 6736–6782</div></figure>')

    text('## 05 · Success Can Mean Refusing an Invalid Action')
    text('DB: database state. COMMUNICATE: required user information. nl_assertions: natural language checks.')
    text(story(STORIES[5][0], *STORIES[5][1]))
    text('<figure class="lesson-figure"><div class="source-code"><strong>Airline task 0 · JSON excerpt</strong><pre><code>{\n  &quot;id&quot;: &quot;0&quot;,\n  &quot;evaluation_criteria&quot;: {\n    &quot;actions&quot;: [],\n    &quot;communicate_info&quot;: [],\n    &quot;nl_assertions&quot;: [\n      &quot;Agent should refuse to proceed with the cancellation.&quot;\n    ],\n    &quot;reward_basis&quot;: [\n      &quot;DB&quot;,\n      &quot;COMMUNICATE&quot;\n    ]\n  }\n}</code></pre></div><details><summary>View original source image</summary><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_05_02.png"><img src="images/w12_05_02.png" alt="Success Can Mean Refusing an Invalid Action · image 1"><span>Enlarge figure ↗</span></button></div></details><div class="lesson-cite"><a href="#ref-2" aria-label="Reference 2: τ²-Bench Airline Tasks">[2]</a> Sierra Research · Benchmark repository</div></figure><article id="ref-2" class="reference-card"><img src="images/w12_05_02.png" alt="" loading="lazy"><div><h3>[2] τ²-Bench Airline Tasks</h3><p class="reference-meta">Sierra Research · Benchmark repository</p><p>Task records and success criteria for the airline domain.</p><div class="reference-links"><a href="https://github.com/sierra-research/tau2-bench/blob/main/data/tau2/domains/airline/tasks.json" target="_blank" rel="noopener noreferrer">Open source ↗</a></div></div></article>')

    text('## 06 · Repeated Success: pass@k and pass^k')
    text('- pass@k: at least one success in k attempts.\n- pass^k: all k attempts succeed.\n- At k = 1, both measure a single attempt.\n- Choose the metric that matches the reliability question.')
    outcomes = list(product((False, True), repeat=4))
    any_rate = sum(map(any, outcomes)) / len(outcomes)  # @inspect any_rate
    all_rate = sum(map(all, outcomes)) / len(outcomes)  # @inspect all_rate
    text(outcome_demo(outcomes, any_rate, all_rate))
    text('<div class="lesson-cite"><a href="#ref-1" aria-label="Reference 1: τ²-Bench: Evaluating Conversational Agents in a Dual-Control Environment">[1]</a> τ²-Bench, ICML 2026 (evaluation metrics)</div>')

    text('## 07 · τ²-Bench: Reliability Across Repeated Runs')
    text('- Retail: orders and returns. Airline: bookings. Telecom: service troubleshooting.\n- pass^k requires success in every one of k runs.')
    text('<figure class="lesson-figure"><div class="source-table"><table><caption>Figure 3 · GPT-4.1 repeated success</caption><thead><tr><th scope=\'col\'>Domain</th><th scope=\'col\'>k = 1</th><th scope=\'col\'>k = 2</th><th scope=\'col\'>k = 3</th><th scope=\'col\'>k = 4</th></tr></thead><tbody><tr><td>Retail</td><td>74%</td><td>64%</td><td>58%</td><td>53%</td></tr><tr><td>Airline</td><td>56%</td><td>46%</td><td>42%</td><td>40%</td></tr><tr><td>Telecom</td><td>34%</td><td>26%</td><td>22%</td><td>19%</td></tr></tbody></table></div><details><summary>View original source image</summary><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_07_02.png"><img src="images/w12_07_02.png" alt="τ²-Bench: Reliability Across Repeated Runs · image 1"><span>Enlarge figure ↗</span></button></div></details><div class="lesson-cite"><a href="#ref-1" aria-label="Reference 1: τ²-Bench: Evaluating Conversational Agents in a Dual-Control Environment">[1]</a> τ²-Bench, ICML 2026 (Figure 3, original experimental results)</div></figure><article id="ref-1" class="reference-card"><img src="images/w12_07_02.png" alt="" loading="lazy"><div><h3>[1] τ²-Bench: Evaluating Conversational Agents in a Dual-Control Environment</h3><p class="reference-meta">Barres et al. · ICML 2026 · PMLR 306, pp. 6736–6782</p><p>Repeated success and the effects of user coordination.</p><div class="reference-links"><a href="https://proceedings.mlr.press/v306/barres26a.html" target="_blank" rel="noopener noreferrer">Open source ↗</a></div></div></article>')

    text('## 08 · τ²-Bench: Reasoning and User Coordination')
    text('- Default: shared control. No user: the agent directly controls both sides.\n- Oracle plan: the correct plan is supplied.\n- Left: original policy. Right: policy with a workflow.')
    text(story(STORIES[8][0], *STORIES[8][1]))
    text('<figure class="lesson-figure"><section class="lesson-demo" aria-label="Telecom pass¹ across evaluation modes"><h3>Telecom pass¹ across evaluation modes</h3><p class="demo-kicker">Published results · transcribed from Figure 4</p><div class="demo-controls"><button type="button" data-frame="0" aria-pressed="true">Original policy</button><button type="button" data-frame="1" aria-pressed="false">Policy with workflow</button></div><div class="demo-panel" data-panel="0"><div class="source-table"><table><caption>Figure 4 · Original policy</caption><thead><tr><th scope=\'col\'>Mode</th><th scope=\'col\'>GPT-4.1</th><th scope=\'col\'>o4-mini</th></tr></thead><tbody><tr><td>Default</td><td>34%</td><td>42%</td></tr><tr><td>No user</td><td>52%</td><td>67%</td></tr><tr><td>Oracle plan</td><td>73%</td><td>96%</td></tr></tbody></table></div></div><div class="demo-panel" data-panel="1" hidden><div class="source-table"><table><caption>Figure 4 · Policy with workflow</caption><thead><tr><th scope=\'col\'>Mode</th><th scope=\'col\'>GPT-4.1</th><th scope=\'col\'>o4-mini</th></tr></thead><tbody><tr><td>Default</td><td>52%</td><td>59%</td></tr><tr><td>No user</td><td>68%</td><td>72%</td></tr><tr><td>Oracle plan</td><td>57%</td><td>88%</td></tr></tbody></table></div></div></section><details><summary>View original source image</summary><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_08_02.png"><img src="images/w12_08_02.png" alt="τ²-Bench: Reasoning and User Coordination · image 1"><span>Enlarge figure ↗</span></button><button type="button" class="figure-thumb" data-figure="images/w12_08_03.png"><img src="images/w12_08_03.png" alt="τ²-Bench: Reasoning and User Coordination · image 2"><span>Enlarge figure ↗</span></button></div></details><div class="lesson-cite"><a href="#ref-1" aria-label="Reference 1: τ²-Bench: Evaluating Conversational Agents in a Dual-Control Environment">[1]</a> τ²-Bench, ICML 2026 (Figure 4, original Telecom ablation)</div></figure>')

    text('## 09 · AI Agents That Matter')
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_09_01.png"><img src="images/w12_09_01.png" alt="AI Agents That Matter · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-3" aria-label="Reference 3: AI Agents That Matter">[3]</a> Kapoor et al. · TMLR 2025</div></figure>')

    text('## 10 · Simple Baselines for Agent Evaluation')
    text('- Retry: ask the model again.\n- Warming: increase the sampling temperature.\n- Escalation: use a stronger model after failure.\n- Compare systems under a similar budget.')
    text(story(STORIES[10][0], *STORIES[10][1]))
    text('<div class="lesson-cite"><a href="#ref-3" aria-label="Reference 3: AI Agents That Matter">[3]</a> AI Agents That Matter, TMLR 2025; 2024 preprint (Sections 2.2 and 2.3)</div>')

    text('## 11 · Accuracy and Cost on HumanEval')
    text('- HumanEval: short Python functions.\n- LDB = Large Language Model Debugger.\n- LATS = Language Agent Tree Search.\n- Five runs across 164 problems.\n- USD = United States dollars.')
    runs = [('A', 0.70, 2), ('B', 0.80, 9)]  # accuracy and cents per task
    eligible = [(name, score) for name, score, cents in runs if cents <= 5]
    text(budget_demo([(name, score) for name, score, _ in runs], eligible))
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_11_01.png"><img src="images/w12_11_01.png" alt="Accuracy and Cost on HumanEval · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-3" aria-label="Reference 3: AI Agents That Matter">[3]</a> AI Agents That Matter, TMLR 2025; 2024 preprint (Figure 1; April 2024 prices; note the broken axes)</div></figure><article id="ref-3" class="reference-card"><img src="images/w12_11_01.png" alt="" loading="lazy"><div><h3>[3] AI Agents That Matter</h3><p class="reference-meta">Kapoor et al. · TMLR 2025</p><p>Cost, simple baselines, holdout sets, and reliable agent comparisons.</p><div class="reference-links"><a href="https://openreview.net/forum?id=Zy4uFzMviZ" target="_blank" rel="noopener noreferrer">Open source ↗</a><a href="https://arxiv.org/abs/2407.01502" target="_blank" rel="noopener noreferrer">View preprint ↗</a></div></div></article>')

    text('## 12 · Test Sets and Claims About Generalization')
    text('- The study sorts 17 agent benchmarks into four levels of generality.\n- Broader claims require test cases that differ more from the development set.')
    text(story(STORIES[12][0], *STORIES[12][1]))
    text('<figure class="lesson-figure"><div class="source-table"><table><caption>Appropriate holdouts in the 17 benchmarks surveyed</caption><thead><tr><th scope=\'col\'>Generality</th><th scope=\'col\'>What should be held out?</th><th scope=\'col\'>Benchmarks</th></tr></thead><tbody><tr><td>Distribution-specific</td><td>In-distribution samples</td><td>1 / 1</td></tr><tr><td>Task-specific</td><td>Out-of-distribution samples</td><td>3 / 6</td></tr><tr><td>Domain-general</td><td>Tasks</td><td>1 / 8</td></tr><tr><td>Fully general</td><td>Domains</td><td>0 / 2</td></tr><tr><td>All benchmarks</td><td>7 had no holdout and no stated plan to add one</td><td>5 / 17</td></tr></tbody></table></div><details><summary>View original source image</summary><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_12_02.png"><img src="images/w12_12_02.png" alt="Test Sets and Claims About Generalization · image 1"><span>Enlarge figure ↗</span></button></div></details><div class="lesson-cite"><a href="#ref-3" aria-label="Reference 3: AI Agents That Matter">[3]</a> Kapoor et al. · TMLR 2025</div></figure>')

    text('## 13 · Diagnosing Evaluation Failures')
    text('- Did the agent fail, or did the environment fail?\n- Were the inputs, budget, and evaluator comparable?\n- Were there enough repeated runs to measure uncertainty?\n- Were the raw traces saved for inspection?')
    text('<div class="lesson-cite"><a href="#ref-3" aria-label="Reference 3: AI Agents That Matter">[3]</a> AI Agents That Matter, TMLR 2025; 2024 preprint (Section 6); practical synthesis</div>')

    text('## 14 · Preference Scores and Task Success')
    text('- Human votes measure which answer people prefer.\n- A model judge applies a grading rule.\n- Task success requires a clear check of the requested outcome.')

    text('## 15 · Chatbot Arena')
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_15_01.png"><img src="images/w12_15_01.png" alt="Chatbot Arena · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-4" aria-label="Reference 4: Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference">[4]</a> Chiang et al. · ICML 2024</div></figure>')

    text('## 16 · Benchmarks for Correctness and Human Preference')
    text('- Static tests can suffer from contamination, overfitting, and saturated scores.\n- Known correct answers are available only for some kinds of tasks.')
    text('- MMLU = Massive Multitask Language Understanding. GSM8K = Grade School Math 8K.\n- MT Bench = Multi Turn Benchmark. HellaSwag: commonsense completion. AlpacaEval: instruction following.')
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_16_01.png"><img src="images/w12_16_01.png" alt="Benchmarks for Correctness and Human Preference · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-4" aria-label="Reference 4: Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference">[4]</a> Chiang et al. · ICML 2024</div></figure>')

    text('## 17 · Chatbot Arena: Voting Rules')
    text(story(STORIES[17][0], *STORIES[17][1]))
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_17_02.png"><img src="images/w12_17_02.png" alt="Chatbot Arena: Voting Rules · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-4" aria-label="Reference 4: Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference">[4]</a> Chiang et al. · ICML 2024</div></figure><article id="ref-4" class="reference-card"><img src="images/w12_17_02.png" alt="" loading="lazy"><div><h3>[4] Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference</h3><p class="reference-meta">Chiang et al. · ICML 2024</p><p>Blind pairwise comparisons and preference scores.</p><div class="reference-links"><a href="https://proceedings.mlr.press/v235/chiang24b.html" target="_blank" rel="noopener noreferrer">Open source ↗</a></div></div></article>')

    text('## 18 · Chatbot Arena: Scores from Pairwise Votes')
    text('Bradley-Terry (BT) model\n- Each model m has a score ξm.\n- Score differences determine the probability of winning a comparison.')
    text('- Human vote: Ht is 0 or 1.\n- Arena fits a Bradley-Terry coefficient, previously called an Elo score.\n- Uncertainty depends on which model pairs receive votes.')
    wins, losses = 6, 4
    fitted_probability = wins / (wins + losses)  # @inspect fitted_probability
    text(vote_demo(wins, losses, fitted_probability))
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_18_01.png"><img src="images/w12_18_01.png" alt="Chatbot Arena: Scores from Pairwise Votes · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-4" aria-label="Reference 4: Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference">[4]</a> Chiang et al. · ICML 2024</div></figure>')

    text('## 19 · The Leaderboard Illusion')
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_19_01.png"><img src="images/w12_19_01.png" alt="The Leaderboard Illusion · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-5" aria-label="Reference 5: The Leaderboard Illusion">[5]</a> Singh et al. · NeurIPS 2025 · Datasets and Benchmarks</div></figure>')

    text('## 20 · Private Testing and Selective Score Reporting')
    text('- Private testing lets a provider publish only its best variant.\n- Small dots are private variants. The large dot is the published one.\n- The paper calls for limits on variants and auditable removal rules.')
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_20_02.png"><img src="images/w12_20_02.png" alt="Private Testing and Selective Score Reporting · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-5" aria-label="Reference 5: The Leaderboard Illusion">[5]</a> Singh et al. · NeurIPS 2025 · Datasets and Benchmarks</div></figure>')

    text('## 21 · Selecting the Best Variant Inflates the Score')
    text('- In this simulation, the underlying mean stays at 1200.\n- Testing more private variants creates more chances to select a high score.')
    scores = [0.68, 0.73, 0.69, 0.76, 0.71]
    selected = max(scores)  # @inspect selected
    text(selection_demo(scores, selected))
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_21_01.png"><img src="images/w12_21_01.png" alt="Selecting the Best Variant Inflates the Score · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-5" aria-label="Reference 5: The Leaderboard Illusion">[5]</a> The Leaderboard Illusion, NeurIPS 2025 (Figure 7; simulation, not a live model ranking)</div></figure><article id="ref-5" class="reference-card"><img src="images/w12_21_01.png" alt="" loading="lazy"><div><h3>[5] The Leaderboard Illusion</h3><p class="reference-meta">Singh et al. · NeurIPS 2025 · Datasets and Benchmarks</p><p>Private testing and selective reporting of model variants.</p><div class="reference-links"><a href="https://papers.nips.cc/paper_files/paper/2025/file/70a93f260a51123b3c0e33ecd1b4de97-Paper-Datasets_and_Benchmarks_Track.pdf" target="_blank" rel="noopener noreferrer">Open source ↗</a></div></div></article>')

    text('## 22 · Preference, Task Success, and Generalization')
    text('- Preference: which answer did users like?\n- Task success: did the agent complete the goal?\n- Generalization: does it work on new tasks?')
    text('<div class="lesson-cite"><a href="#ref-4" aria-label="Reference 4: Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference">[4]</a> Chatbot Arena, ICML 2024; AI Agents That Matter, TMLR 2025; course synthesis</div>')

    text('## 23 · Judging LLM as a Judge')
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_23_01.png"><img src="images/w12_23_01.png" alt="Judging LLM as a Judge · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-6" aria-label="Reference 6: Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena">[6]</a> Zheng et al. · NeurIPS 2023</div></figure>')

    text('## 24 · The Default Pairwise Judge Prompt')
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_24_02.png"><img src="images/w12_24_02.png" alt="The Default Pairwise Judge Prompt · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-6" aria-label="Reference 6: Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena">[6]</a> Zheng et al. · NeurIPS 2023</div></figure><article id="ref-6" class="reference-card"><img src="images/w12_24_02.png" alt="" loading="lazy"><div><h3>[6] Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena</h3><p class="reference-meta">Zheng et al. · NeurIPS 2023</p><p>Pairwise grading prompts and judge bias.</p><div class="reference-links"><a href="https://papers.nips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html" target="_blank" rel="noopener noreferrer">Open source ↗</a></div></div></article>')

    text('## 25 · Checking the Model Judge')
    text('- Start with cases that people have checked.\n- Swap the answer order and inspect disagreements.\n- Count false success and false failure separately.\n- Save the rubric and the judge version.')
    text(story(STORIES[25][0], *STORIES[25][1]))
    text('<div class="lesson-cite"><a href="#ref-6" aria-label="Reference 6: Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena">[6]</a> Judging LLM as a Judge with MT Bench and Chatbot Arena, NeurIPS 2023; practical synthesis</div>')

    text('## 26 · Autonomous Evaluation of Digital Agents')
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_26_01.png"><img src="images/w12_26_01.png" alt="Autonomous Evaluation of Digital Agents · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-7" aria-label="Reference 7: Autonomous Evaluation and Refinement of Digital Agents">[7]</a> Pan et al. · COLM 2024</div></figure>')

    text('## 27 · Judging Task Completion from Screenshots')
    text('- VLM = vision language model.\n- The evaluator reads screenshots to judge whether the task finished.\n- The paper reports higher accuracy with a more expensive evaluator.')
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_27_01.png"><img src="images/w12_27_01.png" alt="Judging Task Completion from Screenshots · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-7" aria-label="Reference 7: Autonomous Evaluation and Refinement of Digital Agents">[7]</a> Pan et al. · COLM 2024</div></figure>')

    text('## 28 · Modular and End to End Evaluators')
    text('- Modular: describe the screenshots, then ask a language model.\n- End to end: a vision language model reads the screenshots.\n- VLM = vision language model. LM = language model.')
    text(story(STORIES[28][0], *STORIES[28][1]))
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_28_02.png"><img src="images/w12_28_02.png" alt="Modular and End to End Evaluators · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-7" aria-label="Reference 7: Autonomous Evaluation and Refinement of Digital Agents">[7]</a> Pan et al. · COLM 2024</div></figure><article id="ref-7" class="reference-card"><img src="images/w12_28_02.png" alt="" loading="lazy"><div><h3>[7] Autonomous Evaluation and Refinement of Digital Agents</h3><p class="reference-meta">Pan et al. · COLM 2024</p><p>Compare action matching with checks of completed tasks.</p><div class="reference-links"><a href="https://openreview.net/forum?id=NPAQ6FKSmK" target="_blank" rel="noopener noreferrer">Open source ↗</a><a href="https://nlp.cs.berkeley.edu/pubs/Pan-Zhang-Tomlin-Zhou-Levine-Suhr_2024_Autonomous_paper.pdf" target="_blank" rel="noopener noreferrer">Paper PDF ↗</a></div></div></article>')

    text('## 29 · Action Matching Can Give the Wrong Ranking')
    text('- AitW = Android in the Wild. Task: follow an instruction in a phone app.\n- Parentheses: action matching. Bars: task success judged by each evaluator.')
    action_scores = [('Trace A', 4 / 4), ('Trace B', 2 / 4)]
    outcome_scores = [('Trace A', 0), ('Trace B', 1)]
    text(matching_demo(action_scores, outcome_scores))
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_29_01.png"><img src="images/w12_29_01.png" alt="Action Matching Can Give the Wrong Ranking · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-7" aria-label="Reference 7: Autonomous Evaluation and Refinement of Digital Agents">[7]</a> Autonomous Evaluation and Refinement of Digital Agents, COLM 2024 (Figure 2)</div></figure>')

    text('## 30 · What Different Benchmarks Measure')
    text('- Some benchmarks test answers to difficult questions.\n- Others test whether an agent can finish a longer sequence of work.\n- Evidence from one setting may not predict performance in another.')

    text("## 31 · Humanity's Last Exam")
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_31_01.png"><img src="images/w12_31_01.png" alt="Humanity&#x27;s Last Exam · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-8" aria-label="Reference 8: A benchmark of expert-level academic questions to assess AI capabilities">[8]</a> Center for AI Safety, Scale AI &amp; HLE Contributors Consortium · Nature 649, 1139–1146 (2026)</div></figure>')

    text('## 32 · HLE: Building the Question Set')
    text('- 2,500 public questions across more than 100 subjects, plus a private test set.\n- Nearly 1,000 contributors from over 500 institutions across 50 countries.\n- Released in January 2025 and published in Nature on 28 January 2026.')
    text(story(STORIES[32][0], *STORIES[32][1]))
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_32_02.png"><img src="images/w12_32_02.png" alt="HLE: Building the Question Set · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-8" aria-label="Reference 8: A benchmark of expert-level academic questions to assess AI capabilities">[8]</a> Center for AI Safety, Scale AI &amp; HLE Contributors Consortium · Nature 649, 1139–1146 (2026)</div></figure><article id="ref-8" class="reference-card"><img src="images/w12_32_02.png" alt="" loading="lazy"><div><h3>[8] A benchmark of expert-level academic questions to assess AI capabilities</h3><p class="reference-meta">Center for AI Safety, Scale AI &amp; HLE Contributors Consortium · Nature 649, 1139–1146 (2026)</p><p>Humanity&#x27;s Last Exam and its expert question review process.</p><div class="reference-links"><a href="https://www.nature.com/articles/s41586-025-09962-4" target="_blank" rel="noopener noreferrer">Open source ↗</a><a href="https://arxiv.org/abs/2501.14249" target="_blank" rel="noopener noreferrer">View preprint ↗</a></div></div></article>')

    text('## 33 · HLE: Scope and Reporting Requirements')
    text("HLE = Humanity's Last Exam\n- Questions have verifiable answers.\n- Report the tools, attempts, and calibration.\n- Research workflows require additional tests.")
    text('<div class="lesson-cite"><a href="#ref-8" aria-label="Reference 8: A benchmark of expert-level academic questions to assess AI capabilities">[8]</a> Humanity&#x27;s Last Exam, Nature 2026; arXiv 2501.14249 (scope and limitations)</div>')

    text('## 34 · Long Software Tasks')
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_34_01.png"><img src="images/w12_34_01.png" alt="Long Software Tasks · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-9" aria-label="Reference 9: Measuring AI Ability to Complete Long Software Tasks">[9]</a> Kwa et al. · NeurIPS 2025</div></figure>')

    text('## 35 · METR: Estimating the Time Horizon')
    text('- HCAST = Human Calibrated Autonomy Software Tasks.\n- SWAA = Software Atomic Actions. RE Bench = Research Engineering Benchmark.\n- SWE = software engineering. R&D = research and development.')
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_35_01.png"><img src="images/w12_35_01.png" alt="METR: Estimating the Time Horizon · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-9" aria-label="Reference 9: Measuring AI Ability to Complete Long Software Tasks">[9]</a> Measuring AI Ability to Complete Long Software Tasks, NeurIPS 2025 (Figure 2)</div></figure>')

    text('## 36 · METR: Success Probability and Human Task Time')
    text('- METR = Model Evaluation and Threat Research.\n- Horizontal axis: human task time.\n- Vertical axis: success probability.\n- 50% horizon: about 54 minutes.\n- 90% reliability gives a shorter horizon.')
    minutes = list(range(0, 61, 5))
    probabilities = [1 / (1 + (t / 30) ** 1.4) for t in minutes]
    crossings = [t for t, p in zip(minutes, probabilities) if p <= 0.5]
    horizon = min(crossings)  # @inspect horizon
    text(horizon_demo(minutes, probabilities, horizon))
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_36_01.png"><img src="images/w12_36_01.png" alt="METR: Success Probability and Human Task Time · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-9" aria-label="Reference 9: Measuring AI Ability to Complete Long Software Tasks">[9]</a> Measuring AI Ability to Complete Long Software Tasks, NeurIPS 2025 (Figure 4, selected panel)</div></figure><article id="ref-9" class="reference-card"><img src="images/w12_36_01.png" alt="" loading="lazy"><div><h3>[9] Measuring AI Ability to Complete Long Software Tasks</h3><p class="reference-meta">Kwa et al. · NeurIPS 2025</p><p>Relate task success to the time a human expert needs.</p><div class="reference-links"><a href="https://proceedings.neurips.cc/paper_files/paper/2025/hash/85069585133c4c168c865e65d72e9775-Abstract-Conference.html" target="_blank" rel="noopener noreferrer">Open source ↗</a></div></div></article>')

    text('## 37 · Codex: Auditing Coding Benchmark Tasks')
    text('- 731 public tasks. Agent assisted review: 200 broken. Human review: 249 broken.\n- Detailed review followed screening. This is an audit of flagged tasks.')
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_37_01.png"><img src="images/w12_37_01.png" alt="Codex: Auditing Coding Benchmark Tasks · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-10" aria-label="Reference 10: Separating signal from noise in coding evaluations">[10]</a> OpenAI, Separating signal from noise in coding evaluations, Jul 2026 (original methodology figure)</div></figure><article id="ref-10" class="reference-card"><img src="images/w12_37_01.png" alt="" loading="lazy"><div><h3>[10] Separating signal from noise in coding evaluations</h3><p class="reference-meta">OpenAI · 2026</p><p>Audit the tasks and tests behind software benchmark scores.</p><div class="reference-links"><a href="https://openai.com/index/separating-signal-from-noise-coding-evaluations/" target="_blank" rel="noopener noreferrer">Open source ↗</a></div></div></article>')

    text('## 38 · What to Save with an Evaluation Result')
    text('- Task files and the success check.\n- Agent, environment, budget, and baseline.\n- Repeated runs, traces, and failure types.\n- Grader version, calibration, and the task audit.')
    text(story(STORIES[38][0], *STORIES[38][1]))
    text('<div class="lesson-cite"><a href="#ref-10" aria-label="Reference 10: Separating signal from noise in coding evaluations">[10]</a> Practical synthesis from the research papers and the OpenAI July 2026 audit</div>')

    text('## 39 · Optional: TheAgentCompany')
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_39_01.png"><img src="images/w12_39_01.png" alt="Optional: TheAgentCompany · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-11" aria-label="Reference 11: TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks">[11]</a> Xu et al. · NeurIPS 2025 · Datasets and Benchmarks</div></figure>')

    text('## 40 · TheAgentCompany: Tasks Across Workplace Tools')
    text('- 175 tasks in a reproducible, simulated workplace.\n- Evaluation checks the work state and the required milestones.')
    text('<figure class="lesson-figure"><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_40_01.png"><img src="images/w12_40_01.png" alt="TheAgentCompany: Tasks Across Workplace Tools · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-11" aria-label="Reference 11: TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks">[11]</a> Xu et al. | NeurIPS 2025 | Figure 1 | Original benchmark design</div></figure><article id="ref-11" class="reference-card"><img src="images/w12_40_01.png" alt="" loading="lazy"><div><h3>[11] TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks</h3><p class="reference-meta">Xu et al. · NeurIPS 2025 · Datasets and Benchmarks</p><p>Workplace tasks that span tools and score intermediate milestones.</p><div class="reference-links"><a href="https://papers.nips.cc/paper_files/paper/2025/file/0d744742f6fac4d1134c019b7cef3c8a-Paper-Datasets_and_Benchmarks_Track.pdf" target="_blank" rel="noopener noreferrer">Open source ↗</a></div></div></article>')

    text('## 41 · TheAgentCompany: Results by Platform and Task')
    text('- SDE in the figure: software engineering. PM = project management.\n- DS = data science. Admin = administration. HR = human resources.')
    text('<figure class="lesson-figure"><div class="source-table"><table><caption>Table 1 · OpenHands 0.28.1 with Gemini 2.5 Pro</caption><thead><tr><th scope=\'col\'>Scoring rule</th><th scope=\'col\'>Reported score</th></tr></thead><tbody><tr><td>Full task success</td><td>30.3%</td></tr><tr><td>With partial credit</td><td>39.3%</td></tr></tbody></table></div><div class="figure-strip"><button type="button" class="figure-thumb" data-figure="images/w12_41_01.png"><img src="images/w12_41_01.png" alt="TheAgentCompany: Results by Platform and Task · image 1"><span>Enlarge figure ↗</span></button></div><div class="lesson-cite"><a href="#ref-11" aria-label="Reference 11: TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks">[11]</a> Xu et al. | NeurIPS 2025 | Figure 2 | Tested model versions in the paper</div></figure>')

    text('## 42 · Evaluation: Success, Fairness, and Scope')
    text('- Define a clear success condition.\n- Use fair comparisons and repeated runs.\n- Check the evaluator itself.\n- Keep the claim within the tested setting.')

    text('## 43 · Thank you')
