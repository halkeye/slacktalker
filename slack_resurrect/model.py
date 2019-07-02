# coding: utf-8
import random
from sqlalchemy import Column, Integer, String, desc
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .settings import CONFIG


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
    team_id = Column('team_id', String(255))

    @classmethod
    def new_from_slack(cls, slack_user):
        return User(
            id=slack_user['id'],
            team_id=slack_user['team_id'],
            name=slack_user['name'],
            real_name=slack_user['profile'].get('real_name', ''),
            first_name=slack_user['profile'].get('first_name', ''),
            last_name=slack_user['profile'].get('last_name', ''),
        )

    @classmethod
    def byid(cls, session, _id):
        return session.query(cls).filter(cls.id == _id).first()

    @classmethod
    def byname(cls, session, _id):
        return session.query(cls).filter(cls.name == _id).first()

    def __repr__(self):
        return "<model.User '{} - {}'>".format(self.name.encode('utf8'),
                                               self.real_name.encode('utf8'))

    @property
    def pretty_name(self):
        if self.real_name:
            return str(self.real_name)
        if self.first_name and self.last_name:
            return "{} {}".format(
                str(self.first_name),
                str(self.last_name)
            )
        return str(self.name)


ENGINE = None


def get_engine():
    global ENGINE
    if not ENGINE:
        ENGINE = create_engine(CONFIG.SQLALCHEMY_DATABASE_URI, echo=CONFIG.DEBUG_SQL)
    return ENGINE


def get_session():
    session = sessionmaker(bind=get_engine())
    return session()


def create_all():
    BaseModel.metadata.create_all(get_engine())
