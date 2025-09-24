from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
import io
from datetime import datetime
from app import db
from app.models import User, Note, Project, Task, FocusSession

data_bp = Blueprint('data', __name__)

@data_bp.route('/export', methods=['GET'])
@jwt_required()
def export_data():
    """导出用户所有数据"""
    try:
        user_id = get_jwt_identity()
        
        # 获取用户信息
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': '用户不存在'}), 404
        
        # 收集所有数据
        export_data = {
            'user': user.to_dict(),
            'notes': [note.to_dict() for note in user.notes],
            'projects': [project.to_dict() for project in user.projects],
            'tasks': [task.to_dict() for task in user.tasks],
            'focus_sessions': [session.to_dict() for session in user.focus_sessions],
            'export_time': datetime.utcnow().isoformat(),
            'version': '1.0'
        }
        
        # 创建JSON文件
        json_data = json.dumps(export_data, ensure_ascii=False, indent=2)
        
        # 创建文件对象
        file_obj = io.BytesIO()
        file_obj.write(json_data.encode('utf-8'))
        file_obj.seek(0)
        
        filename = f"smart_notebook_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        return send_file(
            file_obj,
            as_attachment=True,
            download_name=filename,
            mimetype='application/json'
        )
        
    except Exception as e:
        return jsonify({'error': f'导出数据失败: {str(e)}'}), 500

@data_bp.route('/import', methods=['POST'])
@jwt_required()
def import_data():
    """导入数据"""
    try:
        user_id = get_jwt_identity()
        
        if 'file' not in request.files:
            return jsonify({'error': '没有上传文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
        
        if not file.filename.endswith('.json'):
            return jsonify({'error': '只支持JSON格式文件'}), 400
        
        # 读取文件内容
        try:
            file_content = file.read().decode('utf-8')
            import_data = json.loads(file_content)
        except (UnicodeDecodeError, json.JSONDecodeError):
            return jsonify({'error': '文件格式错误'}), 400
        
        # 验证数据格式
        required_keys = ['notes', 'projects', 'tasks', 'focus_sessions']
        if not all(key in import_data for key in required_keys):
            return jsonify({'error': '数据格式不完整'}), 400
        
        # 开始导入数据
        imported_counts = {
            'notes': 0,
            'projects': 0,
            'tasks': 0,
            'focus_sessions': 0
        }
        
        # 导入项目（需要先导入，因为任务和专注记录可能引用项目）
        project_id_mapping = {}  # 旧ID -> 新ID的映射
        for project_data in import_data['projects']:
            old_project_id = project_data.get('id')
            project = Project(
                user_id=user_id,
                name=project_data['name'],
                color=project_data.get('color', '#3498db')
            )
            db.session.add(project)
            db.session.flush()  # 获取新的ID
            if old_project_id:
                project_id_mapping[old_project_id] = project.id
            imported_counts['projects'] += 1
        
        # 导入笔记
        for note_data in import_data['notes']:
            note = Note(
                user_id=user_id,
                title=note_data['title'],
                content=note_data.get('content', ''),
                folder=note_data.get('folder', '默认文件夹')
            )
            db.session.add(note)
            imported_counts['notes'] += 1
        
        # 导入任务
        for task_data in import_data['tasks']:
            old_project_id = task_data.get('project_id')
            new_project_id = project_id_mapping.get(old_project_id) if old_project_id else None
            
            # 处理日期
            due_date = None
            remind_at = None
            if task_data.get('due_date'):
                try:
                    due_date = datetime.fromisoformat(task_data['due_date'].replace('Z', '+00:00'))
                except ValueError:
                    pass
            if task_data.get('remind_at'):
                try:
                    remind_at = datetime.fromisoformat(task_data['remind_at'].replace('Z', '+00:00'))
                except ValueError:
                    pass
            
            task = Task(
                user_id=user_id,
                project_id=new_project_id,
                title=task_data['title'],
                status=task_data.get('status', 'todo'),
                priority=task_data.get('priority', 'medium'),
                due_date=due_date,
                remind_at=remind_at
            )
            db.session.add(task)
            imported_counts['tasks'] += 1
        
        # 导入专注记录
        for session_data in import_data['focus_sessions']:
            old_project_id = session_data.get('project_id')
            new_project_id = project_id_mapping.get(old_project_id) if old_project_id else None
            
            # 处理开始时间
            start_time = datetime.utcnow()
            if session_data.get('start_time'):
                try:
                    start_time = datetime.fromisoformat(session_data['start_time'].replace('Z', '+00:00'))
                except ValueError:
                    pass
            
            focus_session = FocusSession(
                user_id=user_id,
                project_id=new_project_id,
                start_time=start_time,
                duration_minutes=session_data['duration_minutes']
            )
            db.session.add(focus_session)
            imported_counts['focus_sessions'] += 1
        
        db.session.commit()
        
        return jsonify({
            'message': '数据导入成功',
            'imported_counts': imported_counts
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'导入数据失败: {str(e)}'}), 500