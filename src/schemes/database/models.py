from src.consts.db import UserConsts


class User:
    user_id: int
    role: UserConsts.roles
    login: str
    password_hash: str
