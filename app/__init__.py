from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from config import config

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
TEMPLATE_DIR = Path().absolute() / "templates"
# TEMPLATE_DIR = "/home/jack/PycharmProjects/task/templates"


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)

    db.init_app(app)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
