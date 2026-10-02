#!/usr/bin/env python3
"""Visual scorecard: chart each skill's growth across versions.

Usage:
  python scorecard_chart.py <skill-dir-or-CHANGELOG.md> [more ...] -o scorecard.html

Reads "## <version> — <date>" headings and "Scorecard: Bigger n / Better n /
Stronger n / Faster n / Triggering n" lines from each CHANGELOG.md, then writes
one self-contained HTML file (inline SVG, no external scripts or images) with:
  - a growth line chart per skill (total score by version, plus each dimension)
  - a shape-of-the-skill radar for the latest version
  - a table of every version, with the weakest dimension highlighted
Works offline and on GitHub Pages. Standard library only.
"""
import argparse
import html
import math
import re
import sys
from pathlib import Path

DIMS = ["Bigger", "Better", "Stronger", "Faster", "Triggering"]
COLORS = {"Bigger": "#d9622b", "Better": "#2b7bd9", "Stronger": "#2ba36b",
          "Faster": "#9b4dd9", "Triggering": "#c9a227"}
HEAD = re.compile(r"^##\s+v?(\d+(?:\.\d+){0,2})\s*(?:[—–-]\s*(.+))?$", re.M)
SCORE = re.compile(r"^\s*(?:[-*]\s*)?Scorecard:\s*(.+)$", re.I | re.M)


def parse(path):
    p = Path(path)
    cl = p if p.is_file() else p / "CHANGELOG.md"
    text = cl.read_text(encoding="utf-8")
    name_m = re.search(r"^#\s*Changelog:?\s*(.+)$", text, re.M)
    name = name_m.group(1).strip() if name_m else cl.parent.name
    heads = list(HEAD.finditer(text))
    versions = []
    for k, h in enumerate(heads):
        block = text[h.end(): heads[k + 1].start() if k + 1 < len(heads) else len(text)]
        sm = SCORE.search(block)
        if not sm:
            continue
        scores = {}
        for d in DIMS:
            m = re.search(rf"{d}\s*(\d(?:\.\d)?)", sm.group(1), re.I)
            if m:
                scores[d] = float(m.group(1))
        if len(scores) < len(DIMS):
            continue
        note = sm.group(1).split("—", 1)[1].strip() if "—" in sm.group(1) else ""
        versions.append({"version": h.group(1), "date": (h.group(2) or "").strip(), "scores": scores, "note": note})
    versions.sort(key=lambda v: [int(x) for x in v["version"].split(".")])
    return name, versions


def line_chart(versions, w=560, h=260, pad=40):
    n = len(versions)
    xs = [w / 2] if n == 1 else [pad + (w - 2 * pad) * (i / (n - 1)) for i in range(n)]
    # Small vertical offset per dimension so identical scores don't hide each other
    off = {d: (k - 2) * 0.07 for k, d in enumerate(DIMS)}
    y = lambda v: h - pad - (h - 2 * pad) * ((v - 1) / 4)
    out = [f'<svg viewBox="0 0 {w} {h}" class="chart" role="img" aria-label="Scores by version">']
    for g in range(1, 6):
        out.append(f'<line x1="{pad}" x2="{w-pad}" y1="{y(g):.1f}" y2="{y(g):.1f}" class="grid"/>'
                   f'<text x="{pad-10}" y="{y(g)+4:.1f}" class="axis" text-anchor="end">{g}</text>')
    for i, v in enumerate(versions):
        out.append(f'<text x="{xs[i]:.1f}" y="{h-pad+18}" class="axis" text-anchor="middle">v{html.escape(v["version"])}</text>')
    for d in DIMS:
        pts = " ".join(f"{xs[i]:.1f},{y(v['scores'][d] + off[d]):.1f}" for i, v in enumerate(versions))
        out.append(f'<polyline points="{pts}" fill="none" stroke="{COLORS[d]}" stroke-width="2.5" opacity=".9"/>')
        for i, v in enumerate(versions):
            out.append(f'<circle cx="{xs[i]:.1f}" cy="{y(v["scores"][d] + off[d]):.1f}" r="3.5" fill="{COLORS[d]}">'
                       f'<title>{d} v{v["version"]}: {v["scores"][d]:g}</title></circle>')
    out.append("</svg>")
    return "".join(out)


def radar(scores, prev=None, size=240):
    c, r = size / 2, size / 2 - 46
    def pt(i, val):
        a = -math.pi / 2 + 2 * math.pi * i / len(DIMS)
        return c + r * (val / 5) * math.cos(a), c + r * (val / 5) * math.sin(a)
    out = [f'<svg viewBox="-20 0 {size + 40} {size}" class="radar" role="img" aria-label="Latest version shape">']
    for ring in range(1, 6):
        poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in (pt(i, ring) for i in range(len(DIMS))))
        out.append(f'<polygon points="{poly}" class="grid" fill="none"/>')
    for i, d in enumerate(DIMS):
        x, y = pt(i, 5.9)
        out.append(f'<text x="{x:.1f}" y="{y+4:.1f}" class="axis" text-anchor="middle">{d}</text>')
    if prev:
        poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in (pt(i, prev[d]) for i, d in enumerate(DIMS)))
        out.append(f'<polygon points="{poly}" class="prev"/>')
    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in (pt(i, scores[d]) for i, d in enumerate(DIMS)))
    out.append(f'<polygon points="{poly}" class="now"/></svg>')
    return "".join(out)


def section(name, versions):
    if not versions:
        return f'<section class="card"><h2>{html.escape(name)}</h2><p class="muted">No scorecard lines found in CHANGELOG.md yet.</p></section>'
    latest = versions[-1]
    prev = versions[-2]["scores"] if len(versions) > 1 else None
    total = sum(latest["scores"].values())
    delta = f'{total - sum(prev.values()):+g}' if prev else "first version"
    weakest = min(DIMS, key=lambda d: latest["scores"][d])
    rows = []
    for v in reversed(versions):
        lo = min(v["scores"].values())
        cells = "".join(f'<td class="{"weak" if v["scores"][d] == lo else ""}">{v["scores"][d]:g}</td>' for d in DIMS)
        rows.append(f'<tr><td>v{html.escape(v["version"])}</td><td>{html.escape(v["date"])}</td>{cells}'
                    f'<td><b>{sum(v["scores"].values()):g}</b>/25</td><td class="muted">{html.escape(v["note"])}</td></tr>')
    legend = "".join(f'<span><i style="background:{COLORS[d]}"></i>{d}</span>' for d in DIMS)
    return f"""<section class="card">
<h2>{html.escape(name)}</h2>
<p class="kpis"><b>v{html.escape(latest['version'])}</b> · total <b>{total:g}/25</b> · change <b>{delta}</b> · next focus: <b>{weakest}</b></p>
<div class="viz"><div>{line_chart(versions)}<div class="legend">{legend}</div></div>
<div>{radar(latest['scores'], prev)}<p class="muted center">Solid: latest. Dashed: previous.</p></div></div>
<div class="scroll"><table><thead><tr><th>Version</th><th>Date</th>{''.join(f'<th>{d}</th>' for d in DIMS)}<th>Total</th><th>Biggest gap</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div></section>"""


CSS = """
:root{--bg:#faf8f5;--fg:#1f1d1a;--muted:#6d675f;--card:#fff;--line:#e4dfd7;--now:rgba(217,98,43,.28);--nowS:#d9622b}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#181715;--fg:#efebe5;--muted:#a59f96;--card:#22201d;--line:#3a3631;--now:rgba(217,98,43,.35)}}
:root[data-theme="dark"]{--bg:#181715;--fg:#efebe5;--muted:#a59f96;--card:#22201d;--line:#3a3631;--now:rgba(217,98,43,.35)}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,-apple-system,Segoe UI,sans-serif;padding:24px}
main{max-width:980px;margin:0 auto}h1{margin:0 0 4px}h2{margin:0 0 6px}.muted{color:var(--muted)}.center{text-align:center}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px;margin:18px 0}
.viz{display:flex;flex-wrap:wrap;gap:16px;align-items:center}.viz>div:first-child{flex:1 1 420px}.viz>div:last-child{flex:0 1 260px}
svg{width:100%;height:auto}.grid{stroke:var(--line);stroke-width:1}.axis{fill:var(--muted);font-size:11px}
.now{fill:var(--now);stroke:var(--nowS);stroke-width:2}.prev{fill:none;stroke:var(--muted);stroke-dasharray:4 3}
.legend{display:flex;flex-wrap:wrap;gap:12px;font-size:13px}.legend i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:5px}
.scroll{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:13px;margin-top:12px}
th,td{padding:6px 8px;border-bottom:1px solid var(--line);text-align:left;white-space:nowrap}td.weak{color:#d9622b;font-weight:700}
.kpis{margin:0 0 10px}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("-o", "--output", default="scorecard.html")
    ap.add_argument("--title", default="Skill Scorecard")
    a = ap.parse_args()
    sections = []
    for inp in a.inputs:
        try:
            sections.append(section(*parse(inp)))
        except FileNotFoundError:
            print(f"WARN: no CHANGELOG.md found for {inp}", file=sys.stderr)
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(a.title)}</title><style>{CSS}</style></head><body><main>
<h1>{html.escape(a.title)}</h1><p class="muted">Each skill scored 1–5 on Bigger, Better, Stronger, Faster, and Triggering. Built with Idea Forge.</p>
{''.join(sections)}</main></body></html>"""
    Path(a.output).write_text(doc, encoding="utf-8")
    print(f"Wrote {a.output} ({len(sections)} skill(s))")


if __name__ == "__main__":
    main()
