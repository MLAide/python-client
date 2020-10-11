from enum import Enum


class Stage(str, Enum):
    NONE = "NONE"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"
    ABANDONED = "ABANDONED"
    DEPRECATED = "DEPRECATED"
