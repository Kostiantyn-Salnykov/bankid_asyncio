import enum

__all__ = ["Endpoints", "CollectStatus"]


class Endpoints(str, enum.Enum):
    AUTH = "/auth"
    SIGN = "/sign"
    COLLECT = "/collect"
    CANCEL = "/cancel"


class CollectStatus(str, enum.Enum):
    PENDING = "pending"
    FAILED = "failed"
    COMPLETE = "complete"
