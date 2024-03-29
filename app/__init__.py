from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate

from app.settings import ENVIRONMENT

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(f"app.configuration.{ENVIRONMENT}Config")

    db.init_app(app)
    bs = Bootstrap(app)
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app

app = create_app()

migrate = Migrate(app, db)
