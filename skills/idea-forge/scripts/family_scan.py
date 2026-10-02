#!/usr/bin/env python3
"""Family Forge scanner: find overlapping skills and propose families.

Usage:
  python family_scan.py <dir> [<dir> ...] [--threshold 0.22] [--json]

Each <dir> is either a skill folder (contains SKILL.md) or a folder of skill
folders (searched recursively). Compares skills by their name, description,
headings, and key terms using TF-IDF cosine similarity, then groups them.

Words shared by a large share of skills (boilerplate taglines) are ignored, and
groups form by average similarity so one weak link can't chain unrelated skills.

Output: pairwise overlaps, proposed families, and a suggested action per family:
  MERGE   (similarity >= 0.55) the skills likely do the same job
  CHAIN   (similar, but one description names the other) a designed pipeline
  PLUGIN  (cluster of 2+ related standalone skills) bundle them as one plugin
  CROSS-PLUGIN  related skills in different plugins that compete to trigger
  SHARED  (shared reference file names) extract a shared reference
Standard library only.
"""
import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

STOP = set("""a an the and or but if then else of to in on for with by from as at is are was were be been
being this that these those it its into than so such can could should would will may might must do does
did done use used using user users skill skills claude when whenever any all each every not no only also
your you they them their our we he she his her i me my what which who how why where even out up about
more most less very just one two three new make makes made get gets want wants like etc via per""".split())


def tokenize(text):
    words = re.findall(r"[a-z][a-z0-9]+", text.lower())
    return [w[:-1] if w.endswith("s") and len(w) > 4 else w for w in words if w not in STOP and len(w) > 2]


def parse_skill(skill_md):
    text = skill_md.read_text(encoding="utf-8", errors="ignore")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    fm = m.group(1) if m else ""
    name = re.search(r"^name:\s*(.+)$", fm, re.M)
    desc = re.search(r"^description:\s*(.+?)(?=^\w+:|\Z)", fm, re.M | re.S)
    name = name.group(1).strip() if name else skill_md.parent.name
    desc = " ".join(desc.group(1).split()) if desc else ""
    headings = " ".join(re.findall(r"^#+\s*(.+)$", text, re.M))
    refs = sorted({p.name for p in skill_md.parent.glob("references/*.md")})
    # Weight: description counts double, then name, then headings
    doc = " ".join([desc, desc, name.replace("-", " "), headings])
    return {"name": name, "path": str(skill_md.parent), "description": desc,
            "tokens": tokenize(doc), "refs": refs, "plugin": plugin_of(skill_md.parent)}


def plugin_of(folder):
    """Plugin a skill already belongs to: 'plugin:skill' folder naming, or the
    nearest ancestor containing .claude-plugin/. None if standalone."""
    if ":" in folder.name:
        return folder.name.split(":", 1)[0]
    for anc in list(folder.parents)[:4]:
        if (anc / ".claude-plugin").is_dir():
            return anc.name
    return None


def find_skills(dirs):
    seen, skills = set(), []
    for d in dirs:
        root = Path(d).resolve()
        candidates = [root / "SKILL.md"] if (root / "SKILL.md").exists() else sorted(root.rglob("SKILL.md"))
        for s in candidates:
            if s.parent in seen:
                continue
            seen.add(s.parent)
            skills.append(parse_skill(s))
    return skills


def tfidf(skills):
    n = len(skills)
    df = Counter()
    for s in skills:
        df.update(set(s["tokens"]))
    # Boilerplate filter: in larger libraries, words shared by a big share of skills
    # (e.g. a family's standard tagline) say nothing about what each skill does.
    if n >= 8:
        cap = max(0.25 * n, 3)
        for s in skills:
            s["tokens"] = [t for t in s["tokens"] if df[t] <= cap]
    vecs = []
    for s in skills:
        tf = Counter(s["tokens"])
        v = {t: (c / len(s["tokens"])) * (math.log((1 + n) / (1 + df[t])) + 1) for t, c in tf.items()} if s["tokens"] else {}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        vecs.append({t: x / norm for t, x in v.items()})
    return vecs


def cosine(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(x * b.get(t, 0.0) for t, x in a.items())


def shared_terms(a, b, k=6):
    common = {t: a[t] * b[t] for t in a if t in b}
    return [t for t, _ in sorted(common.items(), key=lambda kv: -kv[1])[:k]]


def cluster(n, sim, threshold, max_size=8):
    """Average-linkage grouping: two groups join only if the average similarity
    across all their members clears the threshold. Prevents one weak link from
    chaining unrelated skills into a giant blob. max_size keeps families usable."""
    groups = [[i] for i in range(n)]
    while True:
        best, pair = threshold, None
        for a in range(len(groups)):
            for b in range(a + 1, len(groups)):
                ga, gb = groups[a], groups[b]
                if len(ga) + len(gb) > max_size:
                    continue
                avg = sum(sim[i][j] for i in ga for j in gb) / (len(ga) * len(gb))
                if avg >= best:
                    best, pair = avg, (a, b)
        if not pair:
            break
        a, b = pair
        groups[a] += groups.pop(b)
    return [g for g in groups if len(g) > 1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dirs", nargs="+")
    ap.add_argument("--threshold", type=float, default=0.22)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    skills = find_skills(a.dirs)
    if len(skills) < 2:
        print("Need at least 2 skills to compare. Found:", [s["name"] for s in skills])
        return 0
    vecs = tfidf(skills)
    n = len(skills)
    sim = [[0.0] * n for _ in range(n)]
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            sim[i][j] = sim[j][i] = cosine(vecs[i], vecs[j])
            if sim[i][j] >= a.threshold:
                pairs.append((i, j, sim[i][j]))
    pairs.sort(key=lambda p: -p[2])

    families = []
    for g in cluster(n, sim, a.threshold):
        members = [skills[i]["name"] for i in g]
        inner = [(i, j, sim[i][j]) for x, i in enumerate(g) for j in g[x + 1:]]
        top = max(p[2] for p in inner)
        ref_counts = Counter(r for i in g for r in skills[i]["refs"])
        shared_refs = sorted(r for r, c in ref_counts.items() if c > 1)
        actions = []
        for i, j, pair_sim in inner:
            if pair_sim >= 0.55:
                ni, nj = skills[i]["name"], skills[j]["name"]
                if nj in skills[i]["description"] or ni in skills[j]["description"]:
                    actions.append(f"CHAIN: {ni} + {nj} ({pair_sim:.2f}): one names the other, likely a designed "
                                   "pipeline; keep apart, make sure each description says when to use which")
                else:
                    actions.append(f"MERGE? {ni} + {nj} ({pair_sim:.2f}): likely the same job")
        plugins = {skills[i]["plugin"] for i in g}
        if len(plugins) == 1 and None not in plugins:
            actions.append(f"ALREADY A FAMILY in plugin '{plugins.pop()}': check for merges or shared references only")
        elif len(plugins - {None}) >= 2:
            actions.append("CROSS-PLUGIN OVERLAP across " + ", ".join(sorted(p for p in plugins if p))
                           + ": these compete to trigger; sharpen descriptions or consolidate")
        else:
            actions.append(f"PLUGIN: bundle {len(g)} skills as one plugin family")
        if shared_refs:
            actions.append(f"SHARED: extract shared reference(s): {', '.join(shared_refs)}")
        theme = Counter()
        for i in g:
            theme.update({t: x for t, x in vecs[i].items()})
        families.append({"members": members, "plugins": sorted({skills[i]["plugin"] or "standalone" for i in g}), "top_similarity": round(top, 3),
                         "theme": [t for t, _ in theme.most_common(5)],
                         "shared_references": shared_refs, "actions": actions})

    result = {
        "skills_scanned": len(skills),
        "pairs": [{"a": skills[i]["name"], "b": skills[j]["name"], "similarity": round(s, 3),
                   "shared_terms": shared_terms(vecs[i], vecs[j])} for i, j, s in pairs],
        "families": families,
    }
    if a.json:
        print(json.dumps(result, indent=2))
        return 0

    print(f"Scanned {len(skills)} skills (threshold {a.threshold}).\n")
    if not pairs:
        print("No meaningful overlaps found. Your skills are distinct.")
        return 0
    print("OVERLAPS")
    for p in result["pairs"]:
        print(f"  {p['similarity']:.2f}  {p['a']} <-> {p['b']}  [{', '.join(p['shared_terms'])}]")
    print("\nPROPOSED FAMILIES")
    for k, f in enumerate(families, 1):
        print(f"  Family {k}: {', '.join(f['members'])}  [{', '.join(f['plugins'])}]")
        print(f"    theme: {', '.join(f['theme'])}")
        for act in f["actions"]:
            print(f"    - {act}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
