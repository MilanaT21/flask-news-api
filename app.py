from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from models import db
from models import User


from routes import app as routes_app
from api import api


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

login_manager.login_view = 'login'
login_manager.init_app(app)

app.register_blueprint(routes_app)
app.register_blueprint(api)

if __name__ == '__main__':
    app.run(debug=True)


"""
Разработайте web-приложение с поддержкой следующего функционала
1. Регистрация пользователей - хранение информации о пользователе (имя, фамилия, email, пароль), 
возможность добавления, удаления, редактирования пользователей.
2. Размещение новостей - каждый пользователь после регистрации имеет возможность просмотра всех новостей, 
добавления, удаления и редактирования своих новостей.
3. Доступ через API к ресурсам - пользователи, 
новости с полной поддержкой всех операций (get, post, put, delete).
4. Разработайте клиентский модуль для тестирования API.
5. Разместите код приложения на github.
6. Сделайте хостинг приложения на glitch.com

В ответе приведите ссылки на github и glitch
"""