#!/usr/bin/env python3
"""Draw an OS system map as one self-contained HTML file.

Usage:
  python os_map.py <os-folder> [-o os-map.html]
  python os_map.py <folder-of-skills> --prefix get-found-os: [-o os-map.html]

Reads os.json when present; otherwise infers the system (same logic as
validate_os.py). Shows the control layer (heartbeat, orchestrator, setup, brain,
scoreboard), then every component grouped by wave, or by the 'department'
metadata in the skills, with authority badges and handoffs. Includes the
validator's findings so problems are visible on the map. Responsive, theme-aware,
no external resources. Standard library only.
"""
import argparse
import html
import json
import re
import sys
from collections import OrderedDict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_os as v  # noqa: E402

AUTH = {"auto": ("Auto", "#2ba36b"), "approve": ("Approve", "#d9622b"), "suggest": ("Suggest", "#2b7bd9")}
E = html.escape


def meta(d, key):
    m = re.search(rf"^\s*{key}:\s*\"?([^\"\n]+)\"?\s*$", v.read(d / "SKILL.md"), re.M)
    return m.group(1).strip() if m else ""


def first_sentence(d):
    m = re.search(r"^description:\s*\"?(.+?)\"?\s*$", v.read(d / "SKILL.md"), re.M)
    text = m.group(1) if m else ""
    return (text.split(". ")[0][:140]).rstrip(".") if text and "TODO" not in text else ""


def load(root, prefix):
    spec_path = root / "os.json"
    if spec_path.exists():
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        errors, warnings, info = v.strict(root, spec)
        dirs = v.skill_dirs(root / "skills" if (root / "skills").is_dir() else root)
        comps = [{"skill": c["skill"], "job": c.get("job", ""), "auth": c.get("authority", ""),
                  "to": c.get("hands_off_to", []), "group": f"Wave {c.get('wave', 1)}",
                  "reads": c.get("reads", []), "writes": c.get("writes", [])} for c in spec.get("components", [])]
        system = {"name": spec.get("name", root.name), "mission": spec.get("mission", ""),
                  "orch": spec.get("orchestrator"), "setup": spec.get("setup"),
                  "beat": (spec.get("heartbeat") or {}).get("skill"),
                  "cadence": (spec.get("heartbeat") or {}).get("cadence", ""),
                  "brain": spec.get("brain", {}).get("file", ""),
                  "fields": spec.get("brain", {}).get("fields", []),
                  "score": spec.get("scoreboard", {}).get("metric", "")}
    else:
        errors, warnings, info = v.inferred(root, prefix)
        dirs = v.skill_dirs(root, prefix)
        sys_names = {info.get("orchestrator"), info.get("setup"), info.get("heartbeat")}
        comps = []
        for n, d in dirs.items():
            if n in sys_names:
                continue
            auto = meta(d, "autonomy").lower()
            auth = "auto" if ("autopilot" in auto or auto == "auto") else "suggest" if any(k in auto for k in ("human", "advis", "suggest", "coach")) else \
                   "approve" if auto else ""
            comps.append({"skill": n, "job": first_sentence(d), "auth": auth, "to": [],
                          "group": meta(d, "department") or "Components", "reads": [], "writes": []})
        system = {"name": prefix.rstrip(":-") or root.name, "mission": "", "orch": info.get("orchestrator"),
                  "setup": info.get("setup"), "beat": info.get("heartbeat"), "cadence": "",
                  "brain": info.get("brain") or "", "fields": [], "score": ""}
    return system, comps, errors, warnings


CSS = """
:root{--bg:#faf8f5;--fg:#1f1d1a;--muted:#6d675f;--card:#fff;--line:#e4dfd7;--accent:#d9622b;--soft:#fbeee6}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#181715;--fg:#efebe5;--muted:#a59f96;--card:#22201d;--line:#3a3631;--soft:#3a2a20}}
:root[data-theme="dark"]{--bg:#181715;--fg:#efebe5;--muted:#a59f96;--card:#22201d;--line:#3a3631;--soft:#3a2a20}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.45 system-ui,-apple-system,Segoe UI,sans-serif;padding:20px}
main{max-width:1100px;margin:0 auto}h1{margin:0}h2{font-size:16px;margin:22px 0 10px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}
.muted{color:var(--muted)}code{font-size:12.5px}
.control{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin-top:16px}
.node{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px}
.node.core{border:2px solid var(--accent);background:var(--soft)}.node b{display:block}.node small{color:var(--muted)}
.flow{color:var(--muted);font-size:13px;margin:10px 0 0}
.group{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px;margin:12px 0}
.group h3{margin:0 0 10px;font-size:15px}.count{color:var(--muted);font-weight:400}
.chips{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:8px}
.chip{border:1px solid var(--line);border-radius:10px;padding:8px 10px;font-size:13px}
.chip b{font-size:13.5px;word-break:break-word}.chip p{margin:4px 0 0;color:var(--muted)}
.badge{display:inline-block;font-size:11px;padding:1px 7px;border-radius:99px;color:#fff;margin-left:6px;vertical-align:1px}
.to{color:var(--accent);font-size:12px;margin-top:4px}
.issues{border-left:4px solid var(--accent);padding:10px 14px;background:var(--card);border-radius:8px}
.issues li{margin:3px 0}.ok{border-left-color:#2ba36b}
.legend span{margin-right:12px;font-size:13px}
"""


def render(system, comps, errors, warnings, title):
    groups = OrderedDict()
    for c in sorted(comps, key=lambda c: (c["group"], c["skill"])):
        groups.setdefault(c["group"], []).append(c)
    if all(g.startswith("Wave") for g in groups):
        groups = OrderedDict(sorted(groups.items(), key=lambda kv: int(re.sub(r"\D", "", kv[0]) or 0)))

    def node(label, name, extra="", core=False):
        if not name:
            return f'<div class="node"><b>{E(label)}</b><small>missing</small></div>'
        return f'<div class="node{" core" if core else ""}"><small>{E(label)}</small><b><code>{E(name)}</code></b>{extra}</div>'

    fields = f"<small>{E(', '.join(system['fields']))}</small>" if system["fields"] else ""
    control = "".join([
        node("Heartbeat" + (f" · {system['cadence']}" if system["cadence"] else ""), system["beat"]),
        node("Orchestrator", system["orch"], core=True),
        node("Setup", system["setup"]),
        node("Shared brain", system["brain"], fields),
    ])
    if system["score"]:
        control += f'<div class="node"><small>Scoreboard</small><b>{E(system["score"])}</b></div>'

    group_html = []
    for g, items in groups.items():
        chips = []
        for c in items:
            label, color = AUTH.get(c["auth"], ("", ""))
            badge = f'<span class="badge" style="background:{color}">{label}</span>' if label else ""
            job = f"<p>{E(c['job'])}</p>" if c["job"] else ""
            to = f'<div class="to">→ {E(", ".join(c["to"]))}</div>' if c["to"] else ""
            rw = ""
            if c["reads"] or c["writes"]:
                rw = f'<p>reads {E(", ".join(c["reads"]) or "–")} · writes {E(", ".join(c["writes"]) or "–")}</p>'
            chips.append(f'<div class="chip"><b>{E(c["skill"])}</b>{badge}{job}{rw}{to}</div>')
        group_html.append(f'<div class="group"><h3>{E(g)} <span class="count">· {len(items)}</span></h3>'
                          f'<div class="chips">{"".join(chips)}</div></div>')

    if errors or warnings:
        items = "".join(f"<li><b>Error:</b> {E(e)}</li>" for e in errors[:25])
        items += "".join(f"<li>{E(w)}</li>" for w in warnings[:25])
        more = len(errors) + len(warnings) - min(len(errors), 25) - min(len(warnings), 25)
        items += f"<li class='muted'>…and {more} more (run validate_os.py)</li>" if more > 0 else ""
        issues = f'<div class="issues"><ul>{items}</ul></div>'
    else:
        issues = '<div class="issues ok">No issues found by validate_os.py.</div>'

    legend = "".join(f'<span><span class="badge" style="background:{c}">{l}</span></span>' for l, c in AUTH.values())
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>{E(title)}</title><style>{CSS}</style></head>
<body><main><h1>{E(title)}</h1>
<p class="muted">{E(system['mission']) or 'System map'} · {len(comps)} components</p>
<h2>Control layer</h2><div class="control">{control}</div>
<p class="flow">Heartbeat runs the orchestrator → it reads the brain, picks the next move, and routes to a component → the component writes back to the brain.</p>
<h2>Health</h2>{issues}
<h2>Components</h2><p class="legend">{legend}</p>{''.join(group_html)}
<p class="muted">Built with Idea Forge.</p></main></body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--prefix", default="")
    ap.add_argument("-o", "--output", default="os-map.html")
    ap.add_argument("--title", default="")
    a = ap.parse_args()
    system, comps, errors, warnings = load(Path(a.folder).resolve(), a.prefix)
    title = a.title or f"{system['name']} system map"
    Path(a.output).write_text(render(system, comps, errors, warnings, title), encoding="utf-8")
    print(f"Wrote {a.output} ({len(comps)} components, {len(errors)} errors, {len(warnings)} warnings)")


if __name__ == "__main__":
    main()
