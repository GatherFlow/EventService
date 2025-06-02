
import enum


class MemberRole(enum.Enum):
    user = "user"
    admin = "admin"
    owner = "owner"
    blacklist = "blacklist"
