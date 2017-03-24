from flask import Flask, Blueprint
import os

# local imports
from config import app_config
from app.restplus import api_v1


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
    api_v1.init_app(blueprint)

    from . import modules
    modules.init_app(app)

    app.register_blueprint(blueprint)

    return app
