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
    # current_team = db.Column(db.String)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'),
                        nullable=False)
    # current_agent = db.Column(db.String)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'),
                         nullable=False)

    team = db.relationship(
        'Team', backref=db.backref('player', cascade='all,delete'))

    agent = db.relationship(
        'Agent', backref=db.backref('player', cascade='all,delete'))

    def __init__(self, name, number, position, current_team, current_agent):
        self.name = name
        self.number = number
        self.position = position
        self.current_team = current_team
        self.current_agent = current_agent

    def __repr__(self, name, number, position):
        return f'{name} is a player on this team. His number is {number} and' \
               f' his position is {position}.'

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
            'current_team': self.current_team,
            'current_agent': self.current_agent
        }


class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String)
    team_short = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    players = db.Column(db.ARRAY(db.String), default=[])

    def __init__(self, team_name, team_short, city, state):
        self.team_name = team_name
        self.team_short = team_short
        self.city = city
        self.state = state

    def __repr__(self, team_name, team_short, city, state, players):
        return f'The {team_name} (abbreviated {team_short}) are based in ' \
               f'{city}, {state}. There are currently {len(players)} on the ' \
               f'roster.'

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
    clients = db.Column(db.ARRAY(db.String), default=[])

    def __init__(self, name):
        self.name = name

    def __repr__(self, name):
        return f'{name} is a baseball player agent with a total of ' \
               f'{len(self.clients)} clients. They are: ' \
               f'{[client for client in self.clients]}'

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
            'clients': [client for client in self.clients]
        }
