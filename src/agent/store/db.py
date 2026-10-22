import sqlite3
from pathlib import Path

from src.agent.models import Job

DB_PATH = Path("data/jobs.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
    id          TEXT PRIMARY KEY,
    source      TEXT NOT NULL,
    title       TEXT NOT NULL,
    company     TEXT,
    url         TEXT,
    description TEXT,
    tags        TEXT,
    location    TEXT,
    salary_min  INTEGER,
    salary_max  INTEGER,
    posted_at   TEXT,
    score       REAL DEFAULT 0,
    status      TEXT DEFAULT 'new',
    first_seen  TEXT DEFAULT CURRENT_TIMESTAMP
);
"""


def connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def save_new_jobs(conn: sqlite3.Connection, jobs: list[Job], scores: dict[str, float]) -> list[Job]:
    """Guarda solo las ofertas que no existían y devuelve esas nuevas."""
    new_jobs = []
    for job in jobs:
        cursor = conn.execute(
            """
            INSERT OR IGNORE INTO jobs
            (id, source, title, company, url, description, tags, location,
             salary_min, salary_max, posted_at, score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                job.id, job.source, job.title, job.company, job.url,
                job.description, ",".join(job.tags), job.location,
                job.salary_min, job.salary_max, job.posted_at,
                scores.get(job.id, 0),
            ),
        )
        if cursor.rowcount:
            new_jobs.append(job)
    conn.commit()
    return new_jobs