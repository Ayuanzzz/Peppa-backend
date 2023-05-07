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


@users_bp.route('/<int:page_id>', methods=['GET'])
def list_users(page_id):
    per_page = 10
    offset = (page_id - 1) * per_page
    count = db.session.query(User).filter_by(role='user', employed=1).count()
    users = db.session.query(User).filter_by(role='user', employed=1). \
        order_by(User.timestamp.desc()). \
        offset(offset).limit(per_page).all()

    output = [{'id': u.id,
               'name': u.name,
               'timestamp': u.timestamp.strftime('%Y-%m-%d')
               }
              for u in users]

    return jsonify({'status':200,'users': output,'count':count})

#获取所有员工
@users_bp.route('/all', methods=['GET'])
def list_all_users():
    users = db.session.query(User).filter_by(role='user', employed=1). \
        order_by(User.timestamp.desc()).all()

    output = [{'id': u.id,
               'name': u.name,
               'timestamp': u.timestamp.strftime('%Y-%m-%d')
               }
              for u in users]

    return jsonify({'status':200,'users': output})

# 根据员工id获取
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

