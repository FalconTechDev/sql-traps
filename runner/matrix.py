"""Render results/results.json into results/matrix.md."""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
d = json.loads((ROOT / "results" / "results.json").read_text(encoding="utf-8"))
engines = list(d["engines"])


def cell(v):
    if "error" in v:
        return "ERROR: " + v["error"][:60].replace("|", "/")
    return "; ".join(",".join(r) for r in v["rows"]) if v["rows"] else "(no rows)"


lines = [f"Run: {d['run_at']}", ""]
lines += [f"- {e}: {v[:70]}" for e, v in d["engines"].items()] + [""]
lines += ["| trap / case | " + " | ".join(engines) + " | differs |", "|---|" + "---|" * (len(engines) + 1)]
for tid, t in d["traps"].items():
    for name, r in t["cases"].items():
        cells = [cell(r[e]) for e in engines]
        lines.append(f"| {tid}: {name} | " + " | ".join(cells) + f" | {'YES' if len(set(cells)) > 1 else 'no'} |")
(ROOT / "results" / "matrix.md").write_text("\n".join(lines), encoding="utf-8")
