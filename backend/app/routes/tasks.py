from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from app.models import Task

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('', methods=['GET'])
@jwt_required()
def get_tasks():
    """获取当前用户的所有任务"""
    try:
        user_id = get_jwt_identity()
        project_id = request.args.get('project_id')
        
        query = Task.query.filter_by(user_id=user_id)
        if project_id:
            query = query.filter_by(project_id=project_id)
        
        tasks = query.order_by(Task.created_at.desc()).all()
        return jsonify({'tasks': [task.to_dict() for task in tasks]}), 200
    except Exception as e:
        return jsonify({'error': f'获取任务失败: {str(e)}'}), 500

@tasks_bp.route('', methods=['POST'])
@jwt_required()
def create_task():
    """创建新任务"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('title'):
            return jsonify({'error': '任务标题是必需的'}), 400
        
        # 处理日期字符串
        due_date = None
        remind_at = None
        
        if data.get('due_date'):
            try:
                due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
            except ValueError:
                return jsonify({'error': '截止日期格式错误'}), 400
        
        if data.get('remind_at'):
            try:
                remind_at = datetime.fromisoformat(data['remind_at'].replace('Z', '+00:00'))
            except ValueError:
                return jsonify({'error': '提醒时间格式错误'}), 400
        
        task = Task(
            user_id=user_id,
            project_id=data.get('project_id'),
            title=data['title'],
            status=data.get('status', 'todo'),
            priority=data.get('priority', 'medium'),
            due_date=due_date,
            remind_at=remind_at
        )
        
        db.session.add(task)
        db.session.commit()
        
        return jsonify({'message': '任务创建成功', 'task': task.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'创建任务失败: {str(e)}'}), 500

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    """更新任务"""
    try:
        user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        
        if not task:
            return jsonify({'error': '任务不存在'}), 404
        
        data = request.get_json()
        
        if data.get('title'):
            task.title = data['title']
        if 'project_id' in data:
            task.project_id = data['project_id']
        if data.get('status'):
            task.status = data['status']
        if data.get('priority'):
            task.priority = data['priority']
        
        # 处理日期更新
        if 'due_date' in data:
            if data['due_date']:
                try:
                    task.due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
                except ValueError:
                    return jsonify({'error': '截止日期格式错误'}), 400
            else:
                task.due_date = None
        
        if 'remind_at' in data:
            if data['remind_at']:
                try:
                    task.remind_at = datetime.fromisoformat(data['remind_at'].replace('Z', '+00:00'))
                except ValueError:
                    return jsonify({'error': '提醒时间格式错误'}), 400
            else:
                task.remind_at = None
        
        db.session.commit()
        return jsonify({'message': '任务更新成功', 'task': task.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'更新任务失败: {str(e)}'}), 500

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """删除任务"""
    try:
        user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        
        if not task:
            return jsonify({'error': '任务不存在'}), 404
        
        db.session.delete(task)
        db.session.commit()
        
        return jsonify({'message': '任务删除成功'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'删除任务失败: {str(e)}'}), 500