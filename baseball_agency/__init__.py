from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    # set up flask blueprints
    from .players.player_views import players_bp
    app.register_blueprint(players_bp)

    from .teams.team_views import teams_bp
    app.register_blueprint(teams_bp)

    from .agents.agent_views import agents_bp
    app.register_blueprint(agents_bp)

    from .errors import errors_bp
    app.register_blueprint(errors_bp)

    return app


from baseball_agency import models  # noqa
