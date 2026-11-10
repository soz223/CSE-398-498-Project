from html import escape


def demo(title, frames, kicker="Teaching example"):
    tabs = []
    panels = []
    for index, (label, body) in enumerate(frames):
        current = index == 0
        pressed = str(current).lower()
        tabs.append(
            f'<button type="button" data-frame="{index}" aria-pressed="{pressed}">'
            f'{escape(label)}</button>'
        )
        hidden = "" if current else " hidden"
        panels.append(f'<div class="demo-panel" data-panel="{index}"{hidden}>{body}</div>')
    return (
        f'<section class="lesson-demo" aria-label="{escape(title)}"><h3>{escape(title)}</h3>'
        f'<p class="demo-kicker">{escape(kicker)}</p><div class="demo-controls">'
        f'{"".join(tabs)}</div>{"".join(panels)}</section>'
    )


def story(title, *frames):
    return demo(title, [(label, f"<p>{escape(body)}</p>") for label, body in frames])


def outcome_demo(outcomes, any_rate, all_rate):
    def grid(accept):
        cells = []
        for outcome in outcomes:
            label = " ".join("S" if x else "F" for x in outcome)
            selected = ' class="qualifies"' if accept(outcome) else ""
            cells.append(f"<span{selected}>{label}</span>")
        return '<div class="outcome-grid">' + "".join(cells) + "</div>"

    return demo("Which outcomes count?", [
        ("All outcomes", grid(lambda _: False) + "<p>S means success. F means failure. At p = 0.5, all 16 outcomes are equally likely.</p>"),
        ("At least one", grid(any) + f"<p>15 of 16 outcomes qualify. <strong>{any_rate:.2%}</strong></p>"),
        ("All four", grid(all) + f"<p>1 of 16 outcomes qualifies. <strong>{all_rate:.2%}</strong></p>"),
    ])


def bars(rows):
    result = []
    for label, value in rows:
        result.append(
            f'<div class="demo-bar"><span>{escape(label)}</span>'
            f'<span class="bar-track"><span style="width:{100 * value:.2f}%"></span></span>'
            f'<strong>{value:.0%}</strong></div>'
        )
    return "".join(result)


def budget_demo(scores, eligible):
    return demo("Does the ranking fit the budget?", [
        ("All runs", bars(scores) + "<p>A costs 2¢ per task. B costs 9¢ per task.</p>"),
        ("5¢ budget", bars(eligible) + "<p>B exceeds the budget. A is the best eligible run in this example.</p>"),
    ])


def vote_demo(wins, losses, fitted_probability):
    return demo("Turn pairwise votes into an estimate", [
        ("Count votes", f"<p>A wins {wins} comparisons. B wins {losses}. This example has no ties.</p>"),
        ("Fit a two-model score", bars([("A beats B", fitted_probability), ("B beats A", 1 - fitted_probability)])
         + "<p>With only this pair, the fitted win probability is A's share of decisive votes.</p>"),
    ])


def selection_demo(scores, selected):
    return demo("Pick a model before or after testing?", [
        ("Report all variants", bars([(f"Variant {i}", s) for i, s in enumerate(scores, 1)])),
        ("Report only the winner", bars([("Reported best", selected)])
         + "<p>The maximum is selected on this test set. Use fresh data to check whether the lead holds.</p>"),
    ])


def horizon_demo(minutes, probabilities, horizon):
    points = " ".join(f"{42 + t * 5:.1f},{138 - p * 108:.1f}"
                      for t, p in zip(minutes, probabilities))
    chart = (
        '<svg viewBox="0 0 374 170" role="img" aria-label="Illustrative success rate falls as human task time increases">'
        '<path d="M42 24V138H350" fill="none" stroke="currentColor"/>'
        f'<polyline points="{points}" fill="none" stroke="#14776d" stroke-width="3"/>'
        '<text x="5" y="34">100%</text><text x="12" y="87">50%</text>'
        '<text x="200" y="162">Human task time (min)</text>'
    )
    x = 42 + horizon * 5
    marker = (
        f'<path d="M42 84H{x}V138" fill="none" stroke="#a65516" stroke-dasharray="4 4"/>'
        f'<circle cx="{x}" cy="84" r="5" fill="#a65516"/>'
        f'<text x="{x - 9}" y="154">{horizon:g}</text>'
    )
    return demo("Read a 50% time horizon", [
        ("Read the axes", chart + "</svg><p>Each x value is how long a human takes on tasks of that difficulty.</p>"),
        ("Find 50%", chart + marker + f"</svg><p>The illustrative curve crosses 50% at <strong>{horizon:g} min</strong>.</p>"),
    ])


STORIES = {
    8: ("Remove one source of difficulty", (
        ("Default", "The agent must coordinate with a user and decide how to finish the task."),
        ("No user", "The agent can take the user's actions directly. Planning is still required."),
        ("Oracle plan", "The correct plan is supplied as well. Compare these controlled conditions in Figure 4."),
    )),
    10: ("Compare a simple baseline", (
        ("One attempt", "Ask the same model to solve the task once."),
        ("Retry", "Give that model another attempt. Record the extra calls and cost."),
        ("Compare", "Compare the more elaborate agent with a baseline that has a similar budget."),
    )),
    12: ("What is held out?", (
        ("New instance", "Test fresh instances while keeping the same task type."),
        ("New task", "Keep the environment and test a different goal."),
        ("New environment", "Change the tool or interface. The claim now needs broader evidence."),
    )),
    17: ("Collect a blind comparison", (
        ("Prompt", "Ask two anonymous models the same question."),
        ("Vote", "Choose the better response or a tie before revealing the model identities."),
    )),
    25: ("Audit a judge for order bias", (
        ("First order", "Question: What is 2 + 2? Answer A says 4. Answer B says 5. Our faulty example judge picks the first answer, A."),
        ("Swap positions", "Answer B now appears first and A appears second. Their text is unchanged. The same faulty judge picks B, which is wrong. It followed the position instead of checking the answer."),
    )),
    28: ("Compare two ways to score a task", (
        ("End to end", "Give the judge the task and screenshots. Ask for a single verdict."),
        ("Modular", "Extract the visible order status first. Compare that status with the success condition."),
    )),
    32: ("Screen a candidate question", (
        ("Draft", "An expert writes a difficult question and a proposed answer."),
        ("Check", "Verify that the question is unambiguous, the answer is correct, and the task tests the intended skill."),
    )),
    38: ("Build a reproducible record", (
        ("Score only", "A run reports 70% success. The denominator, budget and setup are missing."),
        ("Evidence package", "Record task IDs, success conditions, system versions, budgets, run logs and the grader."),
    )),
}
