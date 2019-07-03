import random
from .db import db


class WordEntry(db.Model):

    __tablename__ = 'word_entries'

    user = db.Column('user', db.String(9), primary_key=True)
    word_prev = db.Column('word_prev', db.String(255), primary_key=True)
    word_next = db.Column('word_next', db.String(255), primary_key=True)
    count = db.Column('count', db.Integer, nullable=False, index=True)

    def __repr__(self):
        return "<model.WordEntry '{}:{}:{}'>".format(self.user, self.word_prev,
                                                     self.word_next)

    def next(self, session):
        words = session.query(WordEntry).filter(
            WordEntry.user == self.user,
            WordEntry.word_prev == self.word_next
        ).order_by(WordEntry.count.desc).limit(10)
        return random.choice(list(words))


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column('id', db.String(9), primary_key=True)
    team_id = db.Column('team_id', db.String(255), primary_key=True)
    name = db.Column('name', db.String(255))
    real_name = db.Column('real_name', db.String(255))
    first_name = db.Column('first_name', db.String(255))
    last_name = db.Column('last_name', db.String(255))

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
    def byname(cls, session, team_id, _id):
        return session.query(cls).filter(cls.name == _id).filter(cls.team_id == team_id).first()

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
