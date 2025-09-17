from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


from bot.core.config import Config
from .repositorys import UserRepository
from .base import Base


class DataBase:

    def __init__(self):
        self.engine = create_async_engine(Config.extract_postgres_connection())

        self._session_pool: sessionmaker[AsyncSession] = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

        self.users = UserRepository(self._session_pool)

    async def sync(self):
        async with self.engine.begin() as session:
            await session.run_sync(Base.metadata.create_all)