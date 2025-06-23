from flask import Blueprint, request, jsonify
from models import db, User, News
from werkzeug.security import generate_password_hash

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': u.id,
        'first_name': u.first_name,
        'last_name': u.last_name,
        'email': u.email
    } for u in users])

@api.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password=generate_password_hash(data['password'])
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created'}), 201

@api.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.email = data.get('email', user.email)
    db.session.commit()
    return jsonify({'message': 'User updated'})

@api.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})


@api.route('/news', methods=['GET'])
def get_news():
    news = News.query.all()
    return jsonify([{
        'id': n.id,
        'title': n.title,
        'content': n.content,
        'user_id': n.user_id
    } for n in news])

@api.route('/news', methods=['POST'])
def create_news():
    data = request.json
    new = News(title=data['title'], content=data['content'], user_id=data['user_id'])
    db.session.add(new)
    db.session.commit()
    return jsonify({'message': 'News created'}), 201

@api.route('/news/<int:news_id>', methods=['PUT'])
def update_news(news_id):
    n = News.query.get_or_404(news_id)
    data = request.json
    n.title = data.get('title', n.title)
    n.content = data.get('content', n.content)
    db.session.commit()
    return jsonify({'message': 'News updated'})

@api.route('/news/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    n = News.query.get_or_404(news_id)
    db.session.delete(n)
    db.session.commit()
    return jsonify({'message': 'News deleted'})
