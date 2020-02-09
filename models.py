import os

from dotenv import load_dotenv
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URL'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Player(db.Model):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    number = Column(Integer)
    position = Column(String)

    def __init__(self, name, number, position):
        self.name = name
        self.number = number
        self.position = position

    def __repr__(self, name, number, position):
        return f'{name} is a player on this team. His number is {number} and his position is {position}.'

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'number': self.number,
            'position': self.position
        }


class PlayerStats(db.Model):
    __tablename__ = 'player_stats'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    batting_avg = Column(Integer)
    on_base = Column(Integer)
    strikeouts = Column(Integer)
    walks = Column(Integer)

    def __init__(self, name, batting_avg, on_base, strikeouts, walks):
        self.name = name
        self.batting_avg = batting_avg
        self.on_base = on_base
        self.strikeouts = strikeouts
        self.walks = walks

    def __repr__(self, name, batting_avg, on_base, strikeouts, walks):
        return f'{name} is currently batting {batting_avg}. His OBP is {on_base}. He\'s struck out {strikeouts} ' \
               f'times, and has {walks} walks.'

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'batting_avg': self.batting_avg,
            'on_base_percentage': self.on_base,
            'strikeouts': self.strikeouts,
            'walks': self.walks
        }
