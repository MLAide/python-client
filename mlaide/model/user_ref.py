from dataclasses import dataclass


@dataclass
class UserRef(object):
    userId: str
    nickName: str
