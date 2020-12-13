import datetime
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Artifact(object):
    name: str
    type: str
    created_at: datetime = None
    metadata: Optional[Dict[str, str]] = None
    run_key: Optional[int] = None
    run_name: Optional[str] = None
    updated_at: datetime = None
    version: Optional[int] = None
