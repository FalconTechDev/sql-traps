import importlib.util
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "runner"))
import runner  # noqa: E402


def test_every_trap_is_well_formed():
    traps = runner.load_traps()
    assert len(traps) >= 10
    ids = [t["id"] for t in traps]
    assert len(ids) == len(set(ids))
    for t in traps:
        assert t["cases"] and all("sql" in c and "name" in c for c in t["cases"])
        assert t.get("explanation")
        for s in t.get("sources", []):
            assert s["url"].startswith("https://") and s["checked"]


def test_norm():
    assert runner.norm(None) == "NULL"
    assert runner.norm(3) == "3"


class FakeConn:
    def cursor(self):
        raise RuntimeError("boom\n  multi line")


def test_run_case_captures_engine_errors():
    assert runner.run_case(FakeConn(), "SELECT 1") == {"error": "boom multi line"}


def test_site_builds(tmp_path):
    spec = importlib.util.spec_from_file_location("sitegen", ROOT / "runner" / "site.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    for sub in ("results", "traps"):
        (tmp_path / sub).mkdir()
    (tmp_path / "results" / "results.json").write_text(
        '{"run_at":"x","engines":{"pg":"v1"},"traps":{"t":{"title":"T","cases":{"c":{"pg":{"rows":[["1"]]}}}}}}')
    (tmp_path / "traps" / "t.yaml").write_text(yaml.safe_dump({"id": "t", "title": "T", "explanation": "e"}))
    m.build(tmp_path)
    assert "<td>1</td>" in (tmp_path / "site" / "index.html").read_text()
