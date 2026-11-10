from html import escape
import json


def code_block(source, label):
    return (
        f'<div class="source-code"><strong>{escape(label)}</strong>'
        f'<pre><code>{escape(source)}</code></pre></div>'
    )


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
    return ""
