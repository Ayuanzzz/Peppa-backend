from flask import Blueprint, jsonify, request
from flask_cors import CORS
from models import Project
from exts import db

project_bp = Blueprint('project', __name__)
CORS(project_bp)


@project_bp.route('/', methods=['POST'])
def create_project():
    name = request.json['name']
    num = request.json['num']
    project = Project(name=name, num=num)
    try:
        db.session.add(project)
        db.session.commit()
        return jsonify({'status': 200, 'message': 'Project add successfully!'})
    except:
        db.session.rollback()
        return 'error'


@project_bp.route('/page/<int:page_id>', methods=['GET'])
def list_projects(page_id):
    per_page = 10
    offset = (page_id - 1) * per_page
    count = db.session.query(Project).count()
    projects = db.session.query(Project).order_by(Project.timestamp.desc()). \
        offset(offset).limit(per_page).all()

    output = [{'id': pt.id,
               'name': pt.name,
               'num': pt.num,
               'timestamp': pt.timestamp.strftime('%Y-%m-%d')
               }
              for pt in projects]


    return jsonify({'projects': output, 'count': count})


@project_bp.route('/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = Project.query.filter_by(id=project_id).first()

    if not project:
        return jsonify({'message': 'Project not found!'})

    return jsonify({'project': project.to_dict()})


@project_bp.route('/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    project = Project.query.filter_by(id=project_id).first()

    if not project:
        return jsonify({'message': 'Project not found!'})

    project.name = request.json.get('name', project.name)
    project.num = request.json.get('num', project.num)

    try:
        db.session.commit()
        return jsonify({'message': 'Project updated successfully!'})
    except:
        db.session.rollback()
        return jsonify({'message': 'Something went wrong!'})


@project_bp.route('/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    project = Project.query.filter_by(id=project_id).first()

    if not project:
        return jsonify({'message': 'Project not found!'})

    try:
        db.session.delete(project)
        db.session.commit()
        return jsonify({'status': 200, 'message': 'Project deleted successfully!'})
    except:
        db.session.rollback()
        return jsonify({'message': 'Something went wrong!'})
