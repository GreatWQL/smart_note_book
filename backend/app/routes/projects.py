from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Project

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('', methods=['GET'])
@jwt_required()
def get_projects():
    """获取当前用户的所有项目"""
    try:
        user_id = get_jwt_identity()
        projects = Project.query.filter_by(user_id=user_id).order_by(Project.created_at.desc()).all()
        return jsonify({'projects': [project.to_dict() for project in projects]}), 200
    except Exception as e:
        return jsonify({'error': f'获取项目失败: {str(e)}'}), 500

@projects_bp.route('', methods=['POST'])
@jwt_required()
def create_project():
    """创建新项目"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('name'):
            return jsonify({'error': '项目名称是必需的'}), 400
        
        project = Project(
            user_id=user_id,
            name=data['name'],
            color=data.get('color', '#3498db')
        )
        
        db.session.add(project)
        db.session.commit()
        
        return jsonify({'message': '项目创建成功', 'project': project.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'创建项目失败: {str(e)}'}), 500

@projects_bp.route('/<int:project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    """更新项目"""
    try:
        user_id = get_jwt_identity()
        project = Project.query.filter_by(id=project_id, user_id=user_id).first()
        
        if not project:
            return jsonify({'error': '项目不存在'}), 404
        
        data = request.get_json()
        if data.get('name'):
            project.name = data['name']
        if data.get('color'):
            project.color = data['color']
        
        db.session.commit()
        return jsonify({'message': '项目更新成功', 'project': project.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'更新项目失败: {str(e)}'}), 500

@projects_bp.route('/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    """删除项目"""
    try:
        user_id = get_jwt_identity()
        project = Project.query.filter_by(id=project_id, user_id=user_id).first()
        
        if not project:
            return jsonify({'error': '项目不存在'}), 404
        
        db.session.delete(project)
        db.session.commit()
        
        return jsonify({'message': '项目删除成功'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'删除项目失败: {str(e)}'}), 500