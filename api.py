from flask import Blueprint, request, jsonify
from models import db, User, News
from werkzeug.security import generate_password_hash

api = Blueprint('api', __name__, url_prefix='/api')


# Users
@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()

    return jsonify([
        {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }
        for user in users
    ]), 200


@api.route('/users', methods=['POST'])
def create_user():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({'error': 'JSON body is required'}), 400

    required_fields = ['first_name', 'last_name', 'email', 'password']

    if not all(field in data for field in required_fields):
        return jsonify({
            'error': 'first_name, last_name, email and password are required'
        }), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({
            'error': 'User with this email already exists'
        }), 409

    new_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password=generate_password_hash(data['password'])
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'message': 'User created',
        'user_id': new_user.id
    }), 201


@api.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = db.session.get(User, user_id)

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json(silent=True)

    if not data:
        return jsonify({'error': 'JSON body is required'}), 400

    if 'email' in data:
        existing_user = User.query.filter_by(email=data['email']).first()

        if existing_user and existing_user.id != user.id:
            return jsonify({
                'error': 'User with this email already exists'
            }), 409

        user.email = data['email']

    if 'first_name' in data:
        user.first_name = data['first_name']

    if 'last_name' in data:
        user.last_name = data['last_name']

    db.session.commit()

    return jsonify({
        'message': 'User updated'
    }), 200


@api.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = db.session.get(User, user_id)

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({
        'message': 'User deleted'
    }), 200


# News
@api.route('/news', methods=['GET'])
def get_news():
    news = News.query.all()

    return jsonify([
        {
            'id': item.id,
            'title': item.title,
            'content': item.content,
            'user_id': item.user_id
        }
        for item in news
    ]), 200


@api.route('/news', methods=['POST'])
def create_news():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({'error': 'JSON body is required'}), 400

    required_fields = ['title', 'content', 'user_id']

    if not all(field in data for field in required_fields):
        return jsonify({
            'error': 'title, content and user_id are required'
        }), 400

    user = db.session.get(User, data['user_id'])

    if user is None:
        return jsonify({
            'error': 'User not found'
        }), 404

    new_news = News(
        title=data['title'],
        content=data['content'],
        user_id=data['user_id']
    )

    db.session.add(new_news)
    db.session.commit()

    return jsonify({
        'message': 'News created',
        'news_id': new_news.id
    }), 201


@api.route('/news/<int:news_id>', methods=['PUT'])
def update_news(news_id):
    news = db.session.get(News, news_id)

    if news is None:
        return jsonify({'error': 'News not found'}), 404

    data = request.get_json(silent=True)

    if not data:
        return jsonify({'error': 'JSON body is required'}), 400

    if 'title' in data:
        news.title = data['title']

    if 'content' in data:
        news.content = data['content']

    db.session.commit()

    return jsonify({
        'message': 'News updated'
    }), 200


@api.route('/news/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    news = db.session.get(News, news_id)

    if news is None:
        return jsonify({'error': 'News not found'}), 404

    db.session.delete(news)
    db.session.commit()

    return jsonify({
        'message': 'News deleted'
    }), 200
