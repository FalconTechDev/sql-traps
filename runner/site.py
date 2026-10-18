"""Build a static site (site/index.html) from results.json and the trap catalog."""
import html
import json
import pathlib

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent


def cell_text(v):
    if "error" in v:
        return "ERROR: " + v["error"][:80]
    return "; ".join(",".join(r) for r in v["rows"]) or "(no rows)"


def build(root=ROOT):
    d = json.loads((root / "results" / "results.json").read_text(encoding="utf-8"))
    traps = {}
    for p in sorted((root / "traps").glob("*.yaml")):
        t = yaml.safe_load(p.read_text(encoding="utf-8"))
        traps[t["id"]] = t
    engines = list(d["engines"])
    out = ["<!doctype html><meta charset=utf-8><title>sql-traps</title>",
           "<style>body{font:15px system-ui;max-width:1100px;margin:2em auto;padding:0 1em}"
           "table{border-collapse:collapse;width:100%}td,th{border:1px solid #bbb;padding:4px 8px;vertical-align:top}"
           ".diff{background:#fff3cd}.err{color:#b00020}</style>",
           f"<h1>sql-traps</h1><p>Run at {html.escape(d['run_at'])}. Every cell is an actual query result.</p><ul>"]
    out += [f"<li><b>{e}</b>: {html.escape(v[:90])}</li>" for e, v in d["engines"].items()] + ["</ul>"]
    for tid, t in d["traps"].items():
        meta = traps[tid]
        out.append(f"<h2 id={tid}>{html.escape(t['title'])}</h2><table><tr><th>case</th>"
                   + "".join(f"<th>{e}</th>" for e in engines) + "</tr>")
        for name, r in t["cases"].items():
            cells = [cell_text(r[e]) for e in engines]
            cls = " class=diff" if len(set(cells)) > 1 else ""
            out.append(f"<tr{cls}><td>{html.escape(name)}</td>" + "".join(
                f"<td{' class=err' if c.startswith('ERROR') else ''}>{html.escape(c)}</td>" for c in cells) + "</tr>")
        out.append("</table><p>" + html.escape(meta.get("explanation", "")) + "</p><ul>")
        out += [f"<li><a href='{html.escape(s['url'])}'>{html.escape(s['title'])}</a> (checked {s['checked']})</li>"
                for s in meta.get("sources", [])] + ["</ul>"]
    (root / "site").mkdir(exist_ok=True)
    (root / "site" / "index.html").write_text("\n".join(out), encoding="utf-8")


if __name__ == "__main__":
    build()
