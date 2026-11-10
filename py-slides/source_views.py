from html import escape
import json

from lesson_demos import demo


def code_block(source, label):
    return (
        f'<div class="source-code"><strong>{escape(label)}</strong>'
        f'<pre><code>{escape(source)}</code></pre></div>'
    )


def table(caption, columns, rows):
    header = "".join(f"<th scope='col'>{escape(column)}</th>" for column in columns)
    body = "".join(
        "<tr>" + "".join(f"<td>{escape(str(value))}</td>" for value in row) + "</tr>"
        for row in rows
    )
    return (f'<div class="source-table"><table><caption>{escape(caption)}</caption>'
            f"<thead><tr>{header}</tr></thead><tbody>{body}</tbody></table></div>")


def rates(rows):
    return [(label, *(f"{value:.0%}" for value in values)) for label, *values in rows]


def source_view(page):
    if page == 5:
        task = {
            "id": "0",
            "evaluation_criteria": {
                "actions": [],
                "communicate_info": [],
                "nl_assertions": [
                    "Agent should refuse to proceed with the cancellation."
                ],
                "reward_basis": ["DB", "COMMUNICATE"],
            },
        }
        return code_block(json.dumps(task, indent=2), "Airline task 0 · JSON excerpt")
    if page == 7:
        data = [
            ("Retail", .74, .64, .58, .53),
            ("Airline", .56, .46, .42, .40),
            ("Telecom", .34, .26, .22, .19),
        ]
        return table("Figure 3 · GPT-4.1 repeated success", ["Domain", "k = 1", "k = 2", "k = 3", "k = 4"], rates(data))
    if page == 8:
        columns = ["Mode", "GPT-4.1", "o4-mini"]
        original = [("Default", .34, .42), ("No user", .52, .67), ("Oracle plan", .73, .96)]
        workflow = [("Default", .52, .59), ("No user", .68, .72), ("Oracle plan", .57, .88)]
        return demo("Telecom pass¹ across evaluation modes", [
            ("Original policy", table("Figure 4 · Original policy", columns, rates(original))),
            ("Policy with workflow", table("Figure 4 · Policy with workflow", columns, rates(workflow))),
        ], kicker="Published results · transcribed from Figure 4")
    if page == 12:
        return table("Appropriate holdouts in the 17 benchmarks surveyed",
                     ["Generality", "What should be held out?", "Benchmarks"],
                     [("Distribution-specific", "In-distribution samples", "1 / 1"),
                      ("Task-specific", "Out-of-distribution samples", "3 / 6"),
                      ("Domain-general", "Tasks", "1 / 8"),
                      ("Fully general", "Domains", "0 / 2"),
                      ("All benchmarks", "7 had no holdout and no stated plan to add one", "5 / 17")])
    if page == 41:
        return table("Table 1 · OpenHands 0.28.1 with Gemini 2.5 Pro",
                     ["Scoring rule", "Reported score"],
                     [("Full task success", "30.3%"), ("With partial credit", "39.3%")])
    return ""
