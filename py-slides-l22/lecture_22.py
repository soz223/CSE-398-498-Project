from edtrace import text
from lecture_support import card, figure


def main():
    # Part 1. Reading and reviewing a paper
    introduction()
    reading_a_paper()
    useful_review_comments()
    the_review_form()

    # Part 2. AI in peer review
    venue_rules_and_hidden_prompts()
    spot()
    spot_results()
    feedback_experiment()
    feedback_results()
    aaai_pilot()
    planted_errors()

    # Part 3. Answering reviews of your own paper
    deciding_how_to_answer()
    writing_each_answer()

    # Part 4. From reviewing to reproducing, and the course
    paperbench()
    course_review()


def introduction():
    text("## 01 · Paper Reading, Peer Review, and Course Review")
    text("CSE 398/498 · Vibe Research for Scientific Discovery · Lichao Sun · Lehigh University")
    text("This is our last lecture. All semester we asked agents to produce research results. Today we ask **how a person, or an agent, checks a research result**.")
    text("- We start with how to **read** a paper and write a useful **review**.")
    text("- Then we look at new studies of **AI in peer review**.")
    text("- Next we practice **answering reviews** of our own paper.")
    text("- Finally we look back at **the whole course**.")
    text("Today we are going to study two questions. **What does the paper claim, and what evidence supports it?**")


def reading_a_paper():
    text("## 02 · Reading a Paper for Its Claims")
    text("Let's first look at how we read a paper. We read in layers, and each layer asks a different question.")
    text("- First, we read the title, abstract, introduction, and figures. We look for the **main claim**.")
    text("- Then we read the method and results. We ask **which evidence supports each claim**.")
    text("- Only when we need it, we read every detail closely enough to rerun or challenge the result.")
    text("A good abstract helps with the first layer. It answers four questions.")
    text("- What problem does the paper study, and why does it matter?")
    text("- What did the authors do, and what did they find?")
    text("If the abstract skips one of these, we look for the answer in the paper and avoid filling it in ourselves. Next we use this reading to write a review.")


def useful_review_comments():
    text("## 03 · Writing a Useful Review Comment")
    text("Now let's switch seats. You have read the paper, and you help others judge it. A useful comment points to **a claim, a method detail, or a result**.")
    text("- Compare two comments on the same paper. The first one says, \"The experiments are insufficient.\"")
    text("- The second one says, \"The experiments use only synthetic data. A real dataset would test whether the method generalizes.\"")
    text("- The second comment tells the authors **what is missing** and **why it matters**.")
    text("- A good suggestion also names a concrete change, such as a relevant published baseline.")
    text("We ask only for changes that affect a central claim. Next we see how a review form organizes these comments.")


def the_review_form():
    text("## 04 · The Review Form")
    text("Each venue gives reviewers a form. Here are the fields of the NeurIPS 2026 form.")
    text(card("neurips"))
    text(figure("images/l22_neurips_form.png", "Table of NeurIPS review form fields with the handbook's instruction for each.", "neurips", "NeurIPS 2026 review form, with the handbook's instruction for each field.", width=640))
    text("- The form separates the **summary**, the **strengths and weaknesses**, and the **scores**.")
    text("- The written reasons should agree with the score.")
    text("- Confidence describes how sure you are of your reading. It is separate from how much you like the topic.")
    text("A complete form still needs specific comments. Now that we know what a good review looks like, we ask what happens when AI joins the process.")


def venue_rules_and_hidden_prompts():
    text("## 05 · Venue Rules and Hidden Prompts")
    text("Venues now set rules for AI in reviewing, and the rules differ. You read them for each venue and each year.")
    text(card("icml"))
    text("- ICML 2026 offers two policies. Under the first, reviewers use no LLMs. Under the second, they may use LLMs to understand the paper and polish their writing.")
    text(figure("images/l22_icml_policy.png", "ICML 2026 Policy A and Policy B.", "icml", "ICML 2026 Policy for LLM use in reviewing.", width=620))
    text("- ICLR 2026 addresses a new attack. Some authors hide instructions in their paper, such as white text that asks for a positive review.")
    text(card("iclr"))
    text("- This work by *Lin* found **18 arXiv papers** with such hidden prompts in July 2025.")
    text(card("lin"))
    text(figure("images/l22_lin_tab1.png", "Table of hidden prompt types with the full prompt text.", "lin", "Lin, Table 1, the first three types of hidden prompt.", width=620))
    text("This is the indirect prompt injection we studied in the last two lectures. **The paper is evidence to assess, and its text has no authority over the reviewer.** Next we ask whether AI reviewers can find real problems.")


def spot():
    text("## 06 · SPOT: Can AI Find Real Errors?")
    text("A reviewer's main job is to find what is wrong. This work, *SPOT*, tests whether models can find **real errors in published papers**.")
    text(card("spot"))
    text("- The authors collect errors from withdrawn arXiv papers and from PubPeer, a site where readers discuss papers.")
    text("- They keep an error only when the original authors confirm it.")
    text("- This gives **83 papers** with **91 errors**, such as duplicated figures and wrong equations.")
    text(figure("images/l22_spot_fig1.png", "SPOT pipeline from seed collection and author validation to scoring model responses.", "spot", "SPOT, Figure 1. Green shows how the benchmark is built, and blue shows how answers are scored."))
    text("Each model reads the whole paper, with its text and images, and lists the errors it finds. Next we see how the answers are scored.")


def spot_results():
    text("## 07 · Precision, Recall, and the SPOT Results")
    text("We score an error finder with two numbers. **Precision** is the share of flagged issues that are real errors. **Recall** is the share of real errors that get flagged.")
    text("Here is an example with **made up numbers**. Suppose a paper has 2 known errors. The model flags 10 issues, and 1 of them is a known error.")
    known_errors = 2
    flagged = 10
    matched = 1
    precision = matched / flagged  # @inspect precision
    recall = matched / known_errors  # @clear precision @inspect recall
    text(f"So precision is **{precision:.0%}** and recall is **{recall:.0%}**. Now let's read the real results.")  # @clear recall
    text(figure("images/l22_spot_tab2.png", "Precision, recall, pass@1, and pass@4 for ten models.", "spot", "SPOT, Table 2. Each value is the mean over eight runs, with the standard deviation in small type."))
    text("- The best model, o3, finds **21.1%** of the errors, and only **6.1%** of its flags are correct.")
    text("- Across eight runs, the models rarely find the same error twice.")
    text("- These models are from early 2025, and newer ones may do better.")
    text("So AI can help a reviewer search, and **a person still checks every flag**. Next we test AI as a helper for human reviewers.")


def feedback_experiment():
    text("## 08 · An Experiment with AI Feedback on Reviews")
    text("AI can also give feedback **on a human review**. This work by *Thakkar et al.* tests this idea at ICLR 2025.")
    text(card("thakkar"))
    text("- The papers were split at random into three equal groups. No reviews, half of the reviews, or all reviews received feedback.")
    text("- Feedback arrived about one hour after a review was submitted.")
    text(figure("images/l22_thakkar_fig4a.png", "Three randomized groups and a timeline from October 15 to November 12.", "thakkar", "Thakkar et al., Figure 4a.", width=460))
    text("- The feedback asks reviewers to make vague comments specific, points to parts of the paper that may answer their questions, and flags unprofessional remarks.")
    text(figure("images/l22_thakkar_fig4c.png", "Feedback agent with actors, aggregator, critic, formatter, and reliability tests.", "thakkar", "Thakkar et al., Figure 4c. A critic and reliability tests check the feedback before it is posted."))
    text("The feedback comments on the review and leaves every decision about the paper to people. Because the groups were assigned at random, we can study its effect. Next we look at what changed.")


def feedback_results():
    text("## 09 · What Changed After Feedback")
    text("Now we look at how reviewers responded.")
    text(figure("images/l22_thakkar_fig1a.png", "Pie charts of control, feedback, and updated reviews.", "thakkar", "Thakkar et al., Figure 1a.", width=300))
    text("- Among reviews that received feedback, **26.6%** were updated. In the control group, **9.4%** were updated.")
    text("- Receiving feedback differs from being assigned to a group. Some assigned reviews needed no feedback, so the authors compare the randomized groups.")
    text("This tells us that feedback changed what reviewers did. Whether the reviews got better needs a separate measure. Next we look at a conference that added an AI review to every paper.")


def aaai_pilot():
    text("## 10 · The AAAI-26 AI Review Pilot")
    text("This work describes a much larger step. AAAI 2026 added **one AI review to every main track paper** in full review.")
    text(card("aaai"))
    text("- The pilot produced AI reviews for 22,977 papers.")
    text("- Each AI review covers story, presentation, evaluations, correctness, and significance. The system then critiques and refines its own draft.")
    text("- The AI review gives **no score and no recommendation**. People make every decision.")
    text(figure("images/l22_aaai_fig1a.png", "AAAI-26 AI review system next to the human review process.", "aaai", "AAAI-26 AI Review Pilot, Figure 1a.", width=520))
    text("Running at this scale shows the workflow is practical. Accuracy needs its own test, so the authors built a controlled one. Next we look at it.")


def planted_errors():
    text("## 11 · SPECS: Testing with Planted Errors")
    text("To measure accuracy, we need errors whose location we know. This test, called **SPECS**, plants them on purpose.")
    text("- The authors take accepted AAAI-25 papers and insert one error into each.")
    text("- The error falls into one of five areas, which give the test its name. They are story, presentation, evaluations, correctness, and significance.")
    text("- A judge model checks whether a review mentions the planted error. The test uses 783 changed papers.")
    text(figure("images/l22_aaai_fig4a.png", "SPECS pipeline from paper curation to perturbation and judging.", "aaai", "AAAI-26 AI Review Pilot, Figure 4a.", width=480))
    text(figure("images/l22_aaai_tab2.png", "Recall per SPECS criterion for baseline, targeted, and final systems.", "aaai", "AAAI-26 AI Review Pilot, Table 2."))
    text("- Mean recall rises from **0.43** for a baseline to **0.64** for the final system.")
    text("- On significance, the targeted system beats the final one. A mean can hide such differences.")
    text("SPOT used real errors, while SPECS plants them. The systems and errors differ, so we do not compare the two numbers directly. Next we turn to the other side and answer reviews of our own paper.")


def deciding_how_to_answer():
    text("## 12 · Deciding How to Answer")
    text("Now imagine you receive the reviews of your own paper. Let's first sort the requests, because each kind needs a different answer.")
    text("- If a reviewer finds a **real error**, you correct it.")
    text("- If a reviewer asks for **missing evidence**, you add an experiment when it tests a central claim.")
    text("- If a request **changes the scope** of the paper, you explain the boundary and give a reason.")
    text("Before you defend a claim, you check whether the reviewer is right. A misunderstanding can also show that your writing is unclear. Next we look at how to write each answer.")


def writing_each_answer():
    text("## 13 · Writing Each Answer")
    text("Our course guide writes each answer in three steps. We call them **retrieve, argue, and generate**.")
    text("- First, you **retrieve** the evidence, such as a line, a table, or prior work.")
    text("- Then you **argue**. You answer the concern in one sentence and explain what the evidence supports.")
    text("- Finally, you **generate** the change. You state exactly what will change in the paper.")
    text("Here is an example. A reviewer says that experimental details are missing.")
    text("- The authors point to the baseline settings, which follow earlier work and appear in Appendix A.3.")
    text("- They explain that nodes and labels become text, BERT gives the embeddings, and the data uses an 8:1:1 split.")
    text("- They promise to add these settings to the paper.")
    text(figure("images/l22_rebuttal_template.png", "A response block with Retrieve, Argue, Generate, and Status fields.", None, "Our course template for one reviewer concern.", width=560))
    text("This structure also helps an agent assist you, because a person can check each source and each promised edit. Next we move from reviewing a paper to reproducing it.")


def paperbench():
    text("## 14 · PaperBench: Reproducing a Paper")
    text("Reading and reviewing check a claim on paper. Reproducing the experiment is a stronger check. This work, *PaperBench*, asks an agent to reproduce a paper **from scratch**.")
    text(card("paperbench"))
    text("- The agent reads a paper and builds a code repository.")
    text("- A judge runs the code and grades it against a detailed rubric.")
    text("- The benchmark has **20 ICML 2024 papers** and **8,316 grading criteria**, written with the original authors.")
    text(figure("images/l22_paperbench_fig1.png", "Agent, submission, reproduction, and rubric grading.", "paperbench", "PaperBench, Figure 1. The score inside the figure is only an example."))
    text("- Each model ran three times per paper, with up to 12 hours per run. The best agent meets **21.0%** of the rubric.")
    text(figure("images/l22_paperbench_tab3.png", "Average replication scores for six models.", "paperbench", "PaperBench, Table 3.", width=420))
    text("These models are from early 2025, and newer agents may score higher. The lesson stays the same. **We ask which part of a result was reproduced, and what evidence was saved.** Now let's look back at the whole course.")


def course_review():
    text("## 15 · Looking Back at the Course")
    text("Let's put the whole course together.")
    text(figure("images/l22_course_schedule.png", "Weekly schedule of CSE 398/498 in Fall 2026.", None, "CSE 398/498 syllabus, Fall 2026.", width=640))
    text("- In weeks 1 to 3, we learned that an agent is a model running in a loop with an environment.")
    text("- In weeks 4 and 5, we studied how agents **reason and plan**.")
    text("- In weeks 6 to 8, we gave agents **memory, retrieval, and tools**.")
    text("- In weeks 9 and 10, we built **harnesses** and **coding agents**.")
    text("- In weeks 11 to 14, we studied **research agents**, **evaluation**, **security**, and today, **review**.")
    text("Your final project brings these pieces together. Final presentations and live demonstrations are on **Thursday, December 3**.")
    text("One habit connects every lecture. **Keep the task, the evidence, the actions, and the evaluation connected, so another person can check how a result was reached.**")
    text("Whenever you read a result, ask our two questions. **What does it claim, and what evidence supports it?** Thank you for a great semester.")
