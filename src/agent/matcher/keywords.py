from src.agent.models import Job


def build_keywords(profile: dict) -> set[str]:
    return {s.lower() for group in profile["skills"].values() for s in group}


def score_job(job: Job, keywords: set[str]) -> float:
    matches = keywords & {t.lower() for t in job.tags}
    return float(len(matches))