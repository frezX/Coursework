from time import time
from src.db import DB, database
from typing import Optional
from pymongo.collection import Collection
from src.modules.hashes import HASH, sha512
from src.consts.exceptions import DataError


class UserInteraction:
    def __init__(self):
        self.database: DB = database
        self.users: Collection = self.database.users
        self.sessions: Collection = self.database.sessions

    @staticmethod
    async def create_session(user_id: int) -> str:
        session: HASH = await sha512(string=f'{time()}-{user_id}')
        return session.value

    async def is_unique_login(self, login: str) -> bool:
        return not bool(self.users.find_one({'login': login}))

    async def create_user(self, login: str, password_hash: HASH, role: str) -> tuple[int, str]:
        count: int = self.users.count_documents({})
        user_id: int = count + 1
        user_data: dict = {
            '_id': user_id,
            'role': role,
            'login': login,
            'password_hash': password_hash.value
        }
        self.users.insert_one(document=user_data)
        session: str = await self.create_session(user_id=user_id)
        session_data: dict = {
            '_id': user_id,
            'session': session
        }
        self.sessions.insert_one(document=session_data)
        return user_id, session

    async def login(self, login: str, password_hash: HASH) -> tuple[int, str, str]:
        user: Optional[dict] = self.users.find_one({'login': login, 'password_hash': password_hash.value})
        if not user:
            raise DataError('Wrong login or password')
        user_id: int = user['_id']
        role: str = user['role']
        session: str = self.sessions.find_one({'_id': user_id})['session']
        return user_id, role, session
