from flask import Flask
from flask_login import LoginManager

from config import Config
from models import db, User
from routes import app as routes_app
from api import api


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'app.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


app.register_blueprint(routes_app)
app.register_blueprint(api)


if __name__ == '__main__':
    app.run()
