import os

# from dotenv import load_dotenv
# from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

# load_dotenv()

# database_path = os.environ['DATABASE_URL']

database_name = 'baseball'
database_path = 'postgres://{}:{}@{}/{}'.format(
    'postgres', 'asdf', 'localhost:5432', database_name)

# database_filename = 'baseball.db'
# project_dir = os.path.dirname(os.path.abspath(__file__))
# database_path = 'sqlite:///{}'.format(
#     os.path.join(project_dir, database_filename)
# )

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_and_create_all():
    """
    used to reinitialize database. calling this will delete existing db
    data, so make sure it's what you want to do.
    """
    db.drop_all()
    db.create_all()


class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    number = db.Column(db.Integer)
    position = db.Column(db.String)
    salary = db.Column(db.String)

    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'),
                        nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'),
                         nullable=False)

    team = db.relationship(
        'Team', backref=db.backref('player', cascade='all,delete'))
    agent = db.relationship(
        'Agent', backref=db.backref('player', cascade='all,delete'))

    def __init__(self, name, number, position, salary, team_id, agent_id):
        self.name = name
        self.number = number
        self.position = position
        self.salary = salary
        self.current_team = team_id
        self.current_agent = agent_id

    def __repr__(self):
        return f'{self.name} is a baseball player. His number is' \
               f' {self.number} and his position is {self.position}.'

    def insert(self):
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
            'position': self.position,
            'team_id': self.team_id
        }


class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String)
    team_short = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)

    def __init__(self, team_name, team_short, city, state):
        self.team_name = team_name
        self.team_short = team_short
        self.city = city
        self.state = state

    def __repr__(self):
        return f'The {self.team_name} (abbreviated {self.team_short}) are ' \
               f'based in {self.city}, {self.state}.'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'team_name': self.team_name,
            'team_short': self.team_short,
            'team_city': self.city,
            'team_state': self.state,
            'players': [player.format() for player in self.players]
        }


class Agent(db.Model):
    __tablename__ = 'agents'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'{self.name} is a baseball player agent.'

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name
        }
