# import os

# from dotenv import load_dotenv
# from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

# load_dotenv()

# database_path = os.environ['DATABASE_URL']

database_name = 'baseball'
database_path = 'postgres://{}:{}@{}/{}'.format(
    'postgres', 'asdf', 'localhost:5432', database_name)


db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_and_create_all():
    """used to reinitialize database. calling this will delete existing db
    data, so make sure it's what you want to do."""
    db.drop_all()
    db.create_all()


class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    number = db.Column(db.Integer)
    position = db.Column(db.String)

    playerstats_id = db.Column(db.Integer, db.ForeignKey(
        'stats.id'), nullable=False)
    stats = db.relationship(
        'Stats', backref=db.backref('playerstats', cascade='all, delete'))

    playerdetails_id = db.Column(db.Integer, db.ForeignKey(
        'details.id'), nullable=False)
    details = db.relationship(
        'Details', backref=db.backref('playerdetails', cascade='all, delete'))

    def __init__(self, name, number, position):
        self.name = name
        self.number = number
        self.position = position

    def __repr__(self, name, number, position):
        return f'{name} is a player on this team. His number is {number} and' \
               f' his position is {position}.'

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


class Stats(db.Model):
    __tablename__ = 'stats'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    batting_avg = db.Column(db.Integer)
    on_base = db.Column(db.Integer)
    strikeouts = db.Column(db.Integer)
    walks = db.Column(db.Integer)

    def __init__(self, name, batting_avg, on_base, strikeouts, walks):
        self.name = name
        self.batting_avg = batting_avg
        self.on_base = on_base
        self.strikeouts = strikeouts
        self.walks = walks

    def __repr__(self, name, batting_avg, on_base, strikeouts, walks):
        return f'{name} is currently batting {batting_avg}. His OBP is ' \
               f'{on_base}. He\'s struck out {strikeouts} times, and has' \
               f' {walks} walks.'

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


class Details(db.Model):
    __tablename__ = 'details'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    birthplace = db.Column(db.String)
    birthdate = db.Column(db.Integer)
    lives_in = db.Column(db.String)
    hobby = db.Column(db.String)

    def __init__(self, name, birthplace, birthdate, lives_in, hobby):
        self.name = name
        self.birthplace = birthplace
        self.birthdate = birthdate
        self.lives_in = lives_in
        self.hobby = hobby

    def __repr__(self, name, birthplace, birthdate, lives_in, hobby):
        return f'{name} was born in {birthplace} on {birthdate}. In addition' \
               f'to long walks on the beach, he really likes {hobby}.'

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
            'birthplace': self.birthplace,
            'birthdate': self.birthdate,
            'lives_in': self.lives_in,
            'hobby': self.hobby
        }


# class TeamStats(db.Model):
#     __tablename__ = 'team_stats'
#
#     id = db.Column(db.Integer, primary_key=True)
#     total_wins = db.Column(db.Integer)
#     total_losses = db.Column(db.Integer)
#     total_players = db.Column(db.Integer)
#     player_list = db.Column(db.String)
