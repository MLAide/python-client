from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Any, Dict, cast


@dataclass
class Project:
    """  """

    id: str
    name: str
    display_name: str
    created_at: datetime.datetime

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        display_name = self.display_name
        created_at = self.created_at.isoformat()

        return {
            "id": id,
            "name": name,
            "displayName": display_name,
            "createdAt": created_at,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> Project:
        id = d["id"]

        name = d["name"]

        display_name = d["displayName"]

        created_at = datetime.datetime.fromisoformat(d["createdAt"])

        return Project(id=id, name=name, display_name=display_name, created_at=created_at,)
