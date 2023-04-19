from flask import Blueprint, jsonify, request
from flask_cors import CORS

from exts import db
from models import User

auth_bp = Blueprint('auth', __name__)
CORS(auth_bp)


@auth_bp.route('/register', methods=['POST'])
def register():
    name = request.json['name']
    password = request.json['password']

    # Check if the user already exists
    if User.query.filter_by(name=name).first():
        return {'status':409,'message': '用户已存在'}
    # Create new user
    user = User(name=name, password=password)
    try:
        db.session.add(user)
        db.session.commit()
        return {'status': 200}
    except:
        db.session.rollback()
        return 'error'

@auth_bp.route('/register/name', methods=['POST'])
def registerName():
    name = request.json['name']
    # Check if the user already exists
    if User.query.filter_by(name=name).first():
        return {'status':409,'message': '用户已存在'}
    else:
        return {'status':200,'message': '用户名可用'}

@auth_bp.route('/login', methods=['POST'])
def login():
    name = request.json['name']
    password = request.json['password']
    user = User.query.filter_by(name=name).first()
    if not user:
        return {
            'status': 204,
            'message': '该用户不存在'
        }
    elif password == user.password:
        return {'status': 200,'role': user.role,'id':user.id,'name':user.name}
    else:
        return {'status': 204, 'message': '密码错误'}
