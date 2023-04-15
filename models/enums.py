import enum


class RoleType(enum.Enum):
    user = "user"
    admin = "admin"


class UserStatus(enum.Enum):
    basic = "basic"
    premium = "premium"


class SubscriptionStatus(enum.Enum):
    active = "active"
    paused = "paused"
    canceled = "canceled"
