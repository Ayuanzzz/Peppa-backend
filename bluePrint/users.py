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
    users = User.query.filter_by(role='user', employed=1).all()

    output = [user.to_dict() for user in users]

    return jsonify({'status':200,'users': output})


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

    user.employed = 0

    try:
        db.session.commit()
        return jsonify({'status':200,'message': 'User updated successfully!'})
    except:
        db.session.rollback()
        return jsonify({'message': 'Something went wrong!'})

