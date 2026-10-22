import yaml

from src.agent.matcher.keywords import build_keywords, score_job
from src.agent.sources.remoteok import fetch_jobs
from src.agent.store.db import connect, save_new_jobs


def load_profile(path: str = "profile.yaml") -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    profile = load_profile()
    keywords = build_keywords(profile)

    jobs = fetch_jobs()
    scores = {job.id: score_job(job, keywords) for job in jobs}

    conn = connect()
    new_jobs = save_new_jobs(conn, jobs, scores)

    relevant = sorted(
        (j for j in new_jobs if scores[j.id] > 0),
        key=lambda j: scores[j.id],
        reverse=True,
    )

    print(f"{len(jobs)} descargadas, {len(new_jobs)} nuevas, {len(relevant)} relevantes\n")
    for job in relevant:
        print(f"[{scores[job.id]:.0f}] {job.title} @ {job.company}")
        print(f"    {job.url}\n")


if __name__ == "__main__":
    main()