from flask import Blueprint, jsonify, request
from flask_cors import CORS
from models import UserProject, Project, User
from exts import db
from datetime import datetime

userproject_bp = Blueprint('userproject', __name__)
CORS(userproject_bp)


@userproject_bp.route('/', methods=['POST'])
def create_user_project():
    user_id = request.json['user_id']
    project_id = request.json['project_id']
    num = request.json.get('num', 0)
    level = request.json.get('level', 0)
    userproject = UserProject(user_id=user_id, project_id=project_id, num=num, level=level)
    try:
        db.session.add(userproject)
        db.session.commit()
        return jsonify({'status': 200})
    except:
        db.session.rollback()
        return 'error'


# 普通用户添加项目
@userproject_bp.route('/userAdd', methods=['POST'])
def create_by_user():
    name = request.json['name']
    user_id = request.json['user_id']
    num = request.json.get('num', 0)
    level = request.json.get('level', 0)
    timestamp = datetime.now()
    project = Project(name=name)
    project.userprojects = [UserProject(user_id=user_id, num=num, level=level, timestamp=timestamp)]
    try:
        db.session.add(project)
        db.session.commit()
        return jsonify({'status': 200})
    except:
        db.session.rollback()
        return 'error'


# 按员工获取
@userproject_bp.route('/<int:user_id>/<int:page_id>', methods=['GET'])
def list_user_projects(user_id, page_id):
    per_page = 10
    offset = (page_id - 1) * per_page
    count = db.session.query(UserProject,
                             User.name.label('user_name'),
                             Project.name.label('project_name')). \
        filter_by(user_id=user_id). \
        join(User, UserProject.user_id == User.id). \
        join(Project, UserProject.project_id == Project.id).count()
    userprojects = db.session.query(UserProject,
                                    User.name.label('user_name'),
                                    Project.name.label('project_name')). \
        filter_by(user_id=user_id). \
        join(User, UserProject.user_id == User.id). \
        join(Project, UserProject.project_id == Project.id). \
        order_by(UserProject.timestamp.desc()). \
        offset(offset).limit(per_page).all()

    output = [{'id': up[0].id,
               'user_id': up[0].user_id,
               'user_name': up[1],
               'project_id': up[0].project_id,
               'project_name': up[2],
               'num': up[0].num,
               'level': up[0].level,
               'status': up[0].status,
               'remark': up[0].remark,
               'timestamp': up[0].timestamp.strftime('%Y-%m-%d')
               }
              for up in userprojects]

    return jsonify({'status': 200, 'userprojects': output, "count": count})


# 按项目获取
@userproject_bp.route('/project/<int:project_id>/<int:page_id>', methods=['GET'])
def get_by_project(project_id, page_id):
    per_page = 10
    offset = (page_id - 1) * per_page
    count = db.session.query(UserProject,
                             User.name.label('user_name'),
                             Project.name.label('project_name')). \
        filter_by(project_id=project_id). \
        join(User, UserProject.user_id == User.id). \
        join(Project, UserProject.project_id == Project.id).count()
    userprojects = db.session.query(UserProject,
                                    User.name.label('user_name'),
                                    Project.name.label('project_name')). \
        filter_by(project_id=project_id). \
        join(User, UserProject.user_id == User.id). \
        join(Project, UserProject.project_id == Project.id). \
        order_by(UserProject.timestamp.desc()). \
        offset(offset).limit(per_page).all()

    print(userprojects)

    if not userprojects:
        return jsonify({'message': 'UserProject not found!'})

    output = [{'id': up[0].id,
               'user_id': up[0].user_id,
               'user_name': up[1],
               'project_id': up[0].project_id,
               'project_name': up[2],
               'num': up[0].num,
               'level': up[0].level,
               'status': up[0].status,
               'remark': up[0].remark,
               'timestamp': up[0].timestamp.strftime('%Y-%m-%d')
               }
              for up in userprojects]
    return jsonify({'status': 200, 'data': output, 'count': count})


# 按员工获取进行中的项目
@userproject_bp.route('/user/<int:user_id>/<int:page>', methods=['GET'])
def get_by_user(user_id, page):
    per_page = 10
    offset = (page - 1) * per_page
    count = db.session.query(UserProject,
                             User.name.label('user_name'),
                             Project.name.label('project_name')). \
        filter_by(user_id=user_id, status=1). \
        join(User, UserProject.user_id == User.id). \
        join(Project, UserProject.project_id == Project.id).count()

    userprojects = db.session.query(UserProject,
                                    User.name.label('user_name'),
                                    Project.name.label('project_name')). \
        filter_by(user_id=user_id, status=1). \
        join(User, UserProject.user_id == User.id). \
        join(Project, UserProject.project_id == Project.id). \
        order_by(UserProject.timestamp.desc()). \
        offset(offset).limit(per_page).all()

    if not userprojects:
        return jsonify({'message': 'UserProject not found!'})

    output = [{'id': up[0].id,
               'user_id': up[0].user_id,
               'user_name': up[1],
               'project_id': up[0].project_id,
               'project_name': up[2],
               'num': up[0].num,
               'level': up[0].level,
               'status': up[0].status,
               'remark': up[0].remark,
               'timestamp': up[0].timestamp.strftime('%Y-%m-%d')
               }
              for up in userprojects]
    return jsonify({'status': 200, 'data': output, 'count': count})


# 按员工获取已完成的项目
@userproject_bp.route('/userDone/<int:user_id>/<int:page>', methods=['GET'])
def get_by_userDone(user_id, page):
    per_page = 10
    offset = (page - 1) * per_page
    count = db.session.query(UserProject,
                             User.name.label('user_name'),
                             Project.name.label('project_name')). \
        filter_by(user_id=user_id, status=0). \
        join(User, UserProject.user_id == User.id). \
        join(Project, UserProject.project_id == Project.id).count()

    userprojects = db.session.query(UserProject,
                                    User.name.label('user_name'),
                                    Project.name.label('project_name')). \
        filter_by(user_id=user_id, status=0). \
        join(User, UserProject.user_id == User.id). \
        join(Project, UserProject.project_id == Project.id). \
        order_by(UserProject.timestamp.desc()). \
        offset(offset).limit(per_page).all()

    if not userprojects:
        return jsonify({'message': 'UserProject not found!'})

    output = [{'id': up[0].id,
               'user_id': up[0].user_id,
               'user_name': up[1],
               'project_id': up[0].project_id,
               'project_name': up[2],
               'num': up[0].num,
               'level': up[0].level,
               'status': up[0].status,
               'remark': up[0].remark,
               'timestamp': up[0].timestamp.strftime('%Y-%m-%d')
               }
              for up in userprojects]
    return jsonify({'status': 200, 'data': output, 'count': count})


@userproject_bp.route('changeStatus/<int:userproject_id>', methods=['PUT'])
def update_user_project(userproject_id):
    userproject = UserProject.query.filter_by(id=userproject_id).first()

    if not userproject:
        return jsonify({'message': 'UserProject not found!'})

    userproject.status = request.json.get('status', userproject.status)

    try:
        db.session.commit()
        return jsonify({'status': 200})
    except:
        db.session.rollback()
        return jsonify({'message': 'Something went wrong!'})


@userproject_bp.route('changeUp/<int:userproject_id>', methods=['PUT'])
def update_up(userproject_id):
    userproject = UserProject.query.filter_by(id=userproject_id).first()

    if not userproject:
        return jsonify({'message': 'UserProject not found!'})

    userproject.num = request.json.get('num', userproject.num)
    userproject.level = request.json.get('level', userproject.level)
    userproject.remark = request.json.get('remark', userproject.remark)

    try:
        db.session.commit()
        return jsonify({'status': 200})
    except:
        db.session.rollback()
        return jsonify({'message': 'Something went wrong!'})


@userproject_bp.route('/<int:user_id>/<int:project_id>', methods=['DELETE'])
def delete_user_project(user_id, project_id):
    userproject = UserProject.query.filter_by(user_id=user_id, project_id=project_id).first()

    if not userproject:
        return jsonify({'message': 'UserProject not found!'})

    try:
        db.session.delete(userproject)
        db.session.commit()
        return jsonify({'status': 200, 'message': 'UserProject deleted successfully!'})
    except:
        db.session.rollback()
        return jsonify({'message': 'Something went wrong!'})


@userproject_bp.route('byId/<int:up_id>', methods=['DELETE'])
def delete_by_id(up_id):
    userproject = UserProject.query.filter_by(id=up_id).first()

    if not userproject:
        return jsonify({'message': 'UserProject not found!'})

    try:
        db.session.delete(userproject)
        db.session.commit()
        return jsonify({'status': 200, 'message': 'UserProject deleted successfully!'})
    except:
        db.session.rollback()
        return jsonify({'message': 'Something went wrong!'})
