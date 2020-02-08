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


