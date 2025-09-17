from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from datetime import datetime

from ..model import UserModel

class UserRepository:
    def __init__(self, session_pool: sessionmaker[AsyncSession]):
        self._session_pool = session_pool

    async def create(self, user_id: str, username: str, full_name: str, source_link: str = None):
        """
        Save user in db

        :user_id: user id
        :username: username
        """
        
        async with self._session_pool() as session:
            # get user
            user = await session.execute(
                select(UserModel).where(UserModel.user_id==user_id)
            )
            user = user.scalar()
            # if user is not in db, save
            if not user:
                # model
                new_user = UserModel(
                    user_id=user_id,
                    username=username,
                    full_name=full_name,
                    source_link=source_link,
                    date_added=int(round(datetime.now().timestamp()))
                )
                # add and commit
                session.add(new_user)
                await session.commit()
                    
                return new_user
                
            return user

    async def get(self, user_id: str) -> UserModel:
        """
        get user by user id

        :user_id: user id
        """

        async with self._session_pool() as session:
            response = await session.execute(
                select(UserModel).where(UserModel.user_id==user_id)
            )
            return response.scalar()

    async def get_all(self) -> list[UserModel]:
        """
        get all users

        :user_id: user id
        """

        async with self._session_pool() as session:
            # query
            query = select(UserModel)

            # return repsonse
            return (await session.execute(
                query
            )).scalars().all()

    async def update(self, user_id: str, data: dict = None, **kwargs):
        """
        Update user data

        :user_id: user id
        :data: data to update
        :kwargs: data to update
        """

        async with self._session_pool() as session:
            await session.execute(
                update(UserModel).where(UserModel.user_id == user_id).values(data | kwargs)
            )
            await session.commit()

    async def get_count(self, *filter) -> int:
        async with self._session_pool() as session:
            query = select(func.count()).select_from(UserModel)
            if filter: query = query.where(*filter)

            result = await session.execute(query)
            return result.scalar() or 0



