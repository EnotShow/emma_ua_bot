from sqlalchemy import create_engine, Column, ForeignKey, Integer, Boolean, String, MetaData
from sqlalchemy.orm import declarative_base, relationship, Session, sessionmaker
import os


engine = create_engine(f"sqlite:///sqlitedb")  # echo=True

Base = declarative_base()
meta = MetaData(engine)
DBSession = sessionmaker(bind=engine)


class Questionnaire(Base):
    __tablename__ = 'questionnaire'

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, unique=True)
    username = Column(String(30))
    name = Column(String(30))
    age = Column(Integer)
    photo = Column(String(100))
    about = Column(String(500))
    sex = Column(Integer)
    country = (Column(String(20), default='Польша'))
    city = Column(String(30))
    find = Column(Integer)
    is_delete = Column(Boolean, default=False)
    is_banned = Column(Boolean, default=False)
    complaint_count = Column(Integer, default=0)
    likes = relationship('Likes', back_populates="questionnaire")


class Likes(Base):
    __tablename__ = 'likes'

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer)
    username = Column(String(30))
    questionnaire_user_id = Column(String(30), ForeignKey('questionnaire.user_id'))
    message = Column(String(500), nullable=True)
    questionnaire = relationship('Questionnaire', back_populates="likes")


def create_db():
    Base.metadata.create_all(engine)
