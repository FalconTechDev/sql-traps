# sql-traps

Queries that look the same but return different results on MySQL, MariaDB, PostgreSQL and SQL Server. Every result in the matrix comes from actually running the query in Docker; engine versions and run time are stored with it.

## Run

```bash
docker compose up -d
python -m venv .venv && .venv/bin/pip install -r requirements.txt   # Windows: .venv\Scripts\pip
.venv/bin/python runner/runner.py      # writes results/results.json
.venv/bin/python runner/matrix.py      # results/matrix.md
.venv/bin/python runner/site.py        # site/index.html
.venv/bin/pytest -q tests
```

Note: the SQL Server image needs `ACCEPT_EULA=Y` (set in docker-compose.yml, Developer edition); the compose passwords are throwaway local test values.

## Trap format
`traps/<id>.yaml`: `setup`, `cases` (name + sql), `teardown`, then `explanation` and `sources` (URL + date checked). Claims without a verified source are marked "not checked".

## Status (2026-10-18)
11 traps, 4 engines (versions in `results/results.json`). 3 traps show no divergence (kept as controls). Not done: 30 traps, GitHub Pages deploy, a CI run on GitHub, release tag.
