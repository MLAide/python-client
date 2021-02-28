from dataclasses import dataclass


@dataclass
class UserRef(object):
    user_id: str
    nick_name: str
