import os

from flask_sqlalchemy import SQLAlchemy

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
    """
    used to reinitialize database.
    calling this will delete existing db data!
    """
    db.drop_all()
    db.create_all()


class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    number = db.Column(db.String)
    position = db.Column(db.String)
    salary = db.Column(db.String)

    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'),
                        nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'),
                         nullable=False)

    team = db.relationship(
        'Team', backref=db.backref('player'))
    agent = db.relationship(
        'Agent', backref=db.backref('player'))

    def __init__(self, name, number, position, salary, team_id, agent_id):
        self.name = name
        self.number = number
        self.position = position
        self.salary = salary
        self.team_id = team_id
        self.agent_id = agent_id

    def __repr__(self):
        return f'{self.name} is a baseball player. His number is' \
               f' {self.number} and his position is {self.position}.'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'number': self.number,
            'position': self.position,
            'team_id': self.team_id
        }

    def format_extended(self):
        return {
            'id': self.id,
            'name': self.name,
            'number': self.number,
            'position': self.position,
            'team_id': self.team_id,
            'agent_id': self.agent_id,
            'salary': self.salary
        }


class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    abbr = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    total_payroll = db.Column(db.String)

    def __init__(self, name, abbr, city, state, total_payroll):
        self.name = name
        self.abbr = abbr
        self.city = city
        self.state = state
        self.total_payroll = total_payroll

    def __repr__(self):
        return f'The {self.name} ({self.abbr}) are based in ' \
               f'{self.city}, {self.state}.'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'abbr': self.abbr,
            'city': self.city,
            'state': self.state
        }

    def format_extended(self):
        return {
            'id': self.id,
            'name': self.name,
            'abbr': self.abbr,
            'city': self.city,
            'state': self.state,
            'total_payroll': self.total_payroll
        }


class Agent(db.Model):
    __tablename__ = 'agents'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    salary = db.Column(db.String)

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def __repr__(self):
        return f'{self.name} is a baseball player agent.'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def format_extended(self):
        return {
            'id': self.id,
            'name': self.name,
            'salary': self.salary
        }
