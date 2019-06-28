# coding: utf-8
import os
import random
from sqlalchemy import Column, Integer, String, desc
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


BaseModel = declarative_base()  # pylint: disable=invalid-name


class WordEntry(BaseModel):

    __tablename__ = 'word_entries'

    user = Column('user', String(9), primary_key=True)
    word_prev = Column('word_prev', String(255), primary_key=True)
    word_next = Column('word_next', String(255), primary_key=True)
    count = Column('count', Integer, nullable=False, index=True)

    def __repr__(self):
        return "<model.WordEntry '{}:{}:{}'>".format(self.user, self.word_prev,
                                                     self.word_next)

    def next(self, session):
        words = session.query(WordEntry).filter(
            WordEntry.user == self.user,
            WordEntry.word_prev == self.word_next
        ).order_by(desc(WordEntry.count)).limit(10)
        return random.choice(list(words))


class User(BaseModel):

    __tablename__ = 'users'

    id = Column('id', String(9), primary_key=True)
    name = Column('name', String(255))
    real_name = Column('real_name', String(255))
    first_name = Column('first_name', String(255))
    last_name = Column('last_name', String(255))
    image_24 = Column('image_24', String(255))
    image_32 = Column('image_32', String(255))
    image_48 = Column('image_48', String(255))
    image_72 = Column('image_72', String(255))
    image_192 = Column('image_192', String(255))
    image_original = Column('image_original', String(255))

    @classmethod
    def byid(cls, session, _id):
        return session.query(cls).filter(cls.id == _id).first()

    @classmethod
    def byname(cls, session, _id):
        return session.query(cls).filter(cls.name == _id).first()

    def __repr__(self):
        return "<model.User '{} - {}'>".format(self.name.encode('utf8'),
                                               self.real_name.encode('utf8'))

    def pretty_name(self):
        if self.real_name:
            return self.real_name.encode('utf8')
        if self.first_name and self.last_name:
            return "{} {}".format(
                self.first_name.encode('utf8'),
                self.last_name.encode('utf8')
            )
        return self.name.encode('utf8')


def get_session():
    engine = create_engine(os.environ['DATABASE_URL'], echo=False)
    session = sessionmaker(bind=engine)
    return session()


def create_all():
    engine = create_engine(os.environ['DATABASE_URL'])
    BaseModel.metadata.create_all(engine)
