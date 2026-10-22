from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Job:
    id: str
    source: str
    title: str
    company: str
    url: str
    description: str
    tags: list[str] = field(default_factory=list)
    location: str = ""
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    posted_at: Optional[str] = None
