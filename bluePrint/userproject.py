from flask import Blueprint, jsonify, request
from flask_cors import CORS
from models import UserProject, Project, User
from exts import db

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
        return 'success'
    except:
        db.session.rollback()
        return 'error'


@userproject_bp.route('/', methods=['GET'])
def list_user_projects():
    userprojects = db.session.query(UserProject,
                                    User.name.label('user_name'),
                                    Project.name.label('project_name')). \
        join(User, UserProject.user_id == User.id). \
        join(Project, UserProject.project_id == Project.id).all()

    output = [{'id': up[0].id,
               'user_id': up[0].user_id,
               'user_name': up[1],
               'project_id': up[0].project_id,
               'project_name': up[2],
               'num': up[0].num,
               'level': up[0].level}
              for up in userprojects]

    return jsonify({'userprojects': output})


@userproject_bp.route('/project/<int:project_id>', methods=['GET'])
def get_by_project(project_id):
    userprojects = db.session.query(UserProject,
                                    User.name.label('user_name'),
                                    Project.name.label('project_name')). \
        filter_by(project_id=project_id). \
        join(User, UserProject.user_id == User.id). \
        join(Project, UserProject.project_id == Project.id).all()

    print(userprojects)

    if not userprojects:
        return jsonify({'message': 'UserProject not found!'})

    output = [{'id': up[0].id,
               'user_id': up[0].user_id,
               'user_name': up[1],
               'project_id': up[0].project_id,
               'project_name': up[2],
               'num': up[0].num,
               'level': up[0].level
               }
              for up in userprojects]
    return output

@userproject_bp.route('/user/<int:user_id>', methods=['GET'])
def get_by_user(user_id):
    userprojects = db.session.query(UserProject,
                                    User.name.label('user_name'),
                                    Project.name.label('project_name')). \
        filter_by(user_id=user_id). \
        join(User, UserProject.user_id == User.id). \
        join(Project, UserProject.project_id == Project.id).all()

    if not userprojects:
        return jsonify({'message': 'UserProject not found!'})

    output = [{'id': up[0].id,
               'user_id': up[0].user_id,
               'user_name': up[1],
               'project_id': up[0].project_id,
               'project_name': up[2],
               'num': up[0].num,
               'level': up[0].level
               }
              for up in userprojects]
    return output


@userproject_bp.route('/<int:userproject_id>', methods=['PUT'])
def update_user_project(userproject_id):
    userproject = UserProject.query.filter_by(id=userproject_id).first()

    if not userproject:
        return jsonify({'message': 'UserProject not found!'})

    userproject.user_id = request.json.get('user_id', userproject.user_id)
    userproject.project_id = request.json.get('project_id', userproject.project_id)
    userproject.num = request.json.get('num', userproject.num)
    userproject.level = request.json.get('level', userproject.level)

    try:
        db.session.commit()
        return jsonify({'message': 'UserProject updated successfully!'})
    except:
        db.session.rollback()
        return jsonify({'message': 'Something went wrong!'})


@userproject_bp.route('/<int:userproject_id>', methods=['DELETE'])
def delete_user_project(userproject_id):
    userproject = UserProject.query.filter_by(id=userproject_id).first()

    if not userproject:
        return jsonify({'message': 'UserProject not found!'})

    try:
        db.session.delete(userproject)
        db.session.commit()
        return jsonify({'message': 'UserProject deleted successfully!'})
    except:
        db.session.rollback()
        return jsonify({'message': 'Something went wrong!'})
