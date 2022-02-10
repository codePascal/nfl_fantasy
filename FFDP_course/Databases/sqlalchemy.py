"""
Example script to handle databases with SQLAlchemy

Source:
    https://www.fantasyfootballdatapros.com/course/section/15
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import delcatative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:', echo=True)

Base = delcatative_base()


class Player(Base):
    __tablename__ = "player_"
    id = Column(Integer, primary_key=True)

