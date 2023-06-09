from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from todo_api.config import DevelopmentConfig
from todo_api.controller.tasks_controller import tasks
from todo_api.controller.users_controller import users
from todo_api.errors.handlers import errors
from .models.models import (
    User,
    Task,
    db,
)


def create_app(database_uri=DevelopmentConfig.SQLALCHEMY_DATABASE_URI, testing=False):
    # create an app
    app = Flask(__name__)

    # load config from config.py file
    app.config.from_object(DevelopmentConfig)
    # For testing purpose
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['TESTING'] = testing

    # creation of migrate object
    migrate = Migrate()
    # creation of JWTManager object
    jwt = JWTManager()

    db.init_app(app)  # initialize the database
    migrate.init_app(app, db)  # initialize the flask migrate (Flask wrapper for Alembic)
    jwt.init_app(app)  # initialize the flask JWT

    app.register_blueprint(users, url_prefix="/")
    app.register_blueprint(tasks, url_prefix="/")
    app.register_blueprint(errors, url_prefix="/")

    return app
