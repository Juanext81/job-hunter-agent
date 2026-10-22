import sys

import requests

from src.agent.models import Job


def fetch_jobs() -> list[Job]:
    url = "https://remoteok.com/api"
    headers = {"User-Agent": "job-hunter-agent/1.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        # Skip first element (metadata/legal notice)
        offers = [item for item in data if isinstance(item, dict) and "slug" in item]
        jobs = []
        for offer in offers:
            tags = offer.get("tags") or []
            jobs.append(Job(
                id=f"remoteok-{offer.get('slug', '')}",
                source="remoteok",
                title=offer.get("position", ""),
                company=offer.get("company", ""),
                url=offer.get("url", ""),
                description=offer.get("description", ""),
                tags=tags if isinstance(tags, list) else [],
                location=offer.get("location") or "Remote",
                salary_min=offer.get("salary_min") or None,
                salary_max=offer.get("salary_max") or None,
                posted_at=offer.get("date"),
            ))
        return jobs
    except Exception as e:
        print(f"[remoteok] fetch error: {e}", file=sys.stderr)
        return []
