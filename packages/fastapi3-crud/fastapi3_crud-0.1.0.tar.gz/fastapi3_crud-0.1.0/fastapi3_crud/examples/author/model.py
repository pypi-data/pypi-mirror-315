# --8<-- [start:imports]
from sqlalchemy3 import Column, ForeignKey, Integer, String
from sqlalchemy3.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# --8<-- [end:imports]
# --8<-- [start:model]
class Author(Base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profile.id"))
    name = Column(String)


# --8<-- [end:model]
