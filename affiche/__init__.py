from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

db = SQLAlchemy()
ma = Marshmallow()
co = CORS()

def create_app(config_file = None):
    app = Flask(__name__)
    if config_file:
        app.config.from_pyfile(config_file)
    else:
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['DEBUG'] = True
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "flask_boilerplate_main.db")
        app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
        app.config.setdefault('RESTX_MASK_HEADER', False)
        app.config.setdefault('RESTX_MASK_SWAGGER', True)
    db.init_app(app)
    ma.init_app(app)
    co.init_app(app, resources={r'/*':{'origins':'*'}})
    from .services import api_bp
    app.register_blueprint(api_bp, url_prefix="/")
    app.app_context().push()
    db.create_all(app=app)
    return app