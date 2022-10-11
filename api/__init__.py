from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mongoengine import MongoEngine
import os

bcrypt = Bcrypt()
db = MongoEngine()
key = os.environ.get("SECRET_KEY")

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)
    from .routes import auth, user, survey
    app.register_blueprint(user)
    app.register_blueprint(auth)
    app.register_blueprint(survey)
    bcrypt.init_app(app)
    db.init_app(app)

    return app