from pydantic import BaseModel
from sqlalchemy import Column, String, BigInteger

from .base import Base


class UserModel(Base):
    __tablename__ = "users"

    user_id     = Column(BigInteger, primary_key=True)
    full_name   = Column(String)
    username    = Column(String)
    source_link = Column(String)
    iam         = Column(String)
    date_added  = Column(BigInteger)
