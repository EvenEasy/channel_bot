import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    @staticmethod
    def extract_postgres_connection() -> str:
        return "{engine_url}://{username}:{password}@{ip}/{database_name}".format(
            engine_url="postgresql+asyncpg",
            username=os.getenv('DATABASE_USER'),
            password=os.getenv('PASSWORD'),
            ip=os.getenv('DATABASE_HOST'),
            database_name=os.getenv('DATABASE_NAME'),
        )

    @staticmethod
    def token() -> str:
        return os.getenv('BOT_TOKEN')
    
    @staticmethod
    def get_admins() -> int:
        return os.getenv('ADMIN_ID')
