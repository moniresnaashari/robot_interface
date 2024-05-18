from sqlalchemy import Column, Integer, String

from app.database import Base


class CommandsPosition(Base):
    __tablename__ = "robot_commands_position"

    id = Column(Integer, primary_key=True, index=True)
    command = Column(String)
    x = Column(Integer)
    y = Column(Integer)
    direction = Column(String)
