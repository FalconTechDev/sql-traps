"""Run every trap against every engine and store results with engine versions."""
import datetime
import json
import pathlib
import sys
import time

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
PASSWORD = "Traps_pass1"


def connect(engine):
    if engine == "mysql" or engine == "mariadb":
        import pymysql
        port = 33306 if engine == "mysql" else 33307
        return pymysql.connect(host="127.0.0.1", port=port, user="root",
                               password=PASSWORD, database="traps", autocommit=True)
    if engine == "postgres":
        import psycopg
        return psycopg.connect(host="127.0.0.1", port=35432, user="postgres",
                               password=PASSWORD, dbname="traps", autocommit=True)
    if engine == "mssql":
        import pymssql
        c = pymssql.connect("127.0.0.1", "sa", PASSWORD, port=31433, autocommit=True)
        c.cursor().execute("IF DB_ID('traps') IS NULL CREATE DATABASE traps")
        c.cursor().execute("USE traps")
        return c
    raise ValueError(engine)


ENGINES = ["mysql", "mariadb", "postgres", "mssql"]
VERSION_SQL = {"mssql": "SELECT @@VERSION"}


def wait_connect(engine, timeout=180):
    end = time.time() + timeout
    while True:
        try:
            return connect(engine)
        except Exception:
            if time.time() > end:
                raise
            time.sleep(3)


def norm(v):
    return "NULL" if v is None else str(v)


def run_sql(conn, sql):
    cur = conn.cursor()
    cur.execute(sql)
    if cur.description is None:
        return {"rows": []}
    return {"rows": [[norm(v) for v in r] for r in cur.fetchall()]}


def run_case(conn, sql):
    try:
        return run_sql(conn, sql)
    except Exception as e:  # engine error is a legitimate result
        return {"error": " ".join(str(e).split())[:300]}


def load_traps():
    return [yaml.safe_load(p.read_text(encoding="utf-8"))
            for p in sorted((ROOT / "traps").glob("*.yaml"))]


def main():
    traps = load_traps()
    out = {"run_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
           "engines": {}, "traps": {t["id"]: {"title": t["title"], "cases": {}} for t in traps}}
    for engine in ENGINES:
        conn = wait_connect(engine)
        cur = conn.cursor()
        cur.execute(VERSION_SQL.get(engine, "SELECT VERSION()"))
        out["engines"][engine] = " ".join(str(cur.fetchone()[0]).split())
        for t in traps:
            for stmt in t.get("teardown", []):
                run_case(conn, stmt)
            for stmt in t.get("setup", []):
                r = run_case(conn, stmt)
                if "error" in r:
                    raise SystemExit(f"setup failed {engine}/{t['id']}: {stmt}: {r['error']}")
            for c in t["cases"]:
                out["traps"][t["id"]]["cases"].setdefault(c["name"], {})[engine] = \
                    run_case(conn, c["sql"])
            for stmt in t.get("teardown", []):
                run_case(conn, stmt)
        conn.close()
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results" / "results.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print("ok", out["engines"])


if __name__ == "__main__":
    sys.exit(main())
