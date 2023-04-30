from sqlalchemy import Column, Integer, Text, Uuid

from identity_service.database import Base, EncryptedField


class ServiceConfig(Base):
    id = Column(Uuid(), primary_key=True)
    public_key = Column(Text(), nullable=False)
    private_key: Column[bytes] = Column(EncryptedField(), nullable=False)
    jwt_issuer = Column(Text(), nullable=False)
    jwt_expiration = Column(Integer(), nullable=False)
    jwt_max_refreshes = Column(Integer(), nullable=False)
