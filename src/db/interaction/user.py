from src.db import DB, database
from typing import Optional, NoReturn
from pymongo.collection import Collection
from src.modules.tools import get_timestamp
from src.modules.hashes import HASH, sha512
from src.consts.exceptions import DataError


class UserInteraction:
    def __init__(self):
        self.database: DB = database
        self.users: Collection = self.database.users
        self.sessions: Collection = self.database.sessions

    @staticmethod
    async def create_session(user_id: int) -> str:
        session: HASH = await sha512(string=f'{get_timestamp()}-{user_id}')
        return session.value

    async def is_unique_login(self, login: str) -> bool:
        return not bool(self.users.find_one(filter={'login': login}))

    async def create_user(self, login: str, password_hash: HASH, role: str) -> tuple[int, str, float]:
        count: int = self.users.count_documents(filter={})
        user_id: int = count + 1
        timestamp: float = get_timestamp()
        document: dict = {
            '_id': user_id,
            'role': role,
            'login': login,
            'password_hash': password_hash.value,
            'timestamp': timestamp
        }
        self.users.insert_one(document=document)
        session: str = await self.create_session(user_id=user_id)
        document: dict = {
            '_id': user_id,
            'session': session
        }
        self.sessions.insert_one(document=document)
        return user_id, session, timestamp

    async def login(self, login: str, password_hash: HASH) -> tuple[int, str, str, float] | NoReturn:
        user: Optional[dict] = self.users.find_one(filter={'login': login, 'password_hash': password_hash.value})
        if not user:
            raise DataError('Wrong login or password')
        user_id: int = user['_id']
        role: str = user['role']
        session: str = self.sessions.find_one(filter={'_id': user_id})['session']
        timestamp: float = user['timestamp']
        return user_id, role, session, timestamp

    async def verify_user_with_cookies(self, cookies: dict) -> bool:
        user_filter: dict = {
            '_id': int(cookies['id']),
            'role': cookies['role'],
            'login': cookies['login'],
        }
        if not self.users.find_one(filter=user_filter):
            return False
        session_in_db: Optional[dict] = self.sessions.find_one(filter={'_id': int(cookies['id'])})
        return session_in_db and session_in_db.get('session') == cookies['session']
