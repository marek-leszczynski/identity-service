from sqlalchemy import ARRAY, Boolean, Column, Text, Uuid

from identity_service.database import Base


class User(Base):
    id = Column(Uuid(), primary_key=True)
    username = Column(Text(), nullable=False)
    password_hash = Column(Text(), nullable=False)
    is_root: Column[bool] = Column(Boolean(), nullable=False, server_default="false")
    permissions: Column[list] = Column(ARRAY(Text()))
