# --8<-- [start:imports]
from sqlalchemy3 import Column, Integer, String
from sqlalchemy3.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# --8<-- [end:imports]


# --8<-- [start:model]
class Department(Base):
    __tablename__ = "department"
    id = Column(Integer, primary_key=True)
    name = Column(String)


# --8<-- [end:model]
