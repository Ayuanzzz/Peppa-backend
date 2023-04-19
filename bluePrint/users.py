from flask import Blueprint, jsonify, request
from flask_cors import CORS

from exts import db
from models import User

users_bp = Blueprint('users', __name__)
CORS(users_bp)

@users_bp.route('/', methods=['POST'])
def create_user():
    name = request.json['name']
    password = request.json['password']
    user = User(name=name, password=password)
    try:
        db.session.add(user)
        db.session.commit()
        return 'success'
    except:
        db.session.rollback()
        return 'error'


@users_bp.route('/', methods=['GET'])
def list_users():
    users = User.query.all()

    output = [user.to_dict() for user in users]

    return jsonify({'users': output})


@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'message': 'User not found!'})

    return jsonify({'user': user.to_dict()})


@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'message': 'User not found!'})

    user.name = request.json.get('name', user.name)
    # user.password = request.json.get('password', user.password)

    try:
        db.session.commit()
        return jsonify({'message': 'User updated successfully!'})
    except:
        db.session.rollback()
        return jsonify({'message': 'Something went wrong!'})


@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'message': 'User not found!'})

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully!'})
    except:
        db.session.rollback()
        return jsonify({'message': 'Something went wrong!'})
