import datetime
from dataclasses import dataclass


@dataclass
class Git(object):
    commit_time: datetime
    commit_hash: str
    is_dirty: bool
    repository_uri: str
