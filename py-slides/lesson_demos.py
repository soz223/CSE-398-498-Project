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

