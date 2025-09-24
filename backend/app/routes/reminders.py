from flask import Blueprint, request, jsonify
from app import db
from app.models import Reminder
from datetime import datetime

reminders_bp = Blueprint('reminders', __name__)

@reminders_bp.route('/reminders', methods=['GET'])
def get_reminders():
    """获取所有提醒"""
    try:
        # 这里暂时使用用户ID=1，实际应该从认证中获取
        user_id = 1
        reminders = Reminder.query.filter_by(user_id=user_id).order_by(Reminder.remind_at.asc()).all()
        return jsonify({
            'success': True,
            'reminders': [reminder.to_dict() for reminder in reminders]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@reminders_bp.route('/reminders', methods=['POST'])
def create_reminder():
    """创建新提醒"""
    try:
        data = request.get_json()
        user_id = 1  # 暂时使用用户ID=1
        
        # 解析提醒时间
        remind_at = datetime.fromisoformat(data['remind_at'].replace('Z', '+00:00'))
        
        reminder = Reminder(
            user_id=user_id,
            title=data['title'],
            content=data.get('content', ''),
            remind_at=remind_at,
            is_recurring=data.get('is_recurring', False),
            recurring_type=data.get('recurring_type')
        )
        
        db.session.add(reminder)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'reminder': reminder.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@reminders_bp.route('/reminders/<int:reminder_id>', methods=['PUT'])
def update_reminder(reminder_id):
    """更新提醒"""
    try:
        user_id = 1  # 暂时使用用户ID=1
        reminder = Reminder.query.filter_by(id=reminder_id, user_id=user_id).first()
        
        if not reminder:
            return jsonify({'success': False, 'error': '提醒不存在'}), 404
        
        data = request.get_json()
        
        if 'title' in data:
            reminder.title = data['title']
        if 'content' in data:
            reminder.content = data['content']
        if 'remind_at' in data:
            reminder.remind_at = datetime.fromisoformat(data['remind_at'].replace('Z', '+00:00'))
        if 'is_completed' in data:
            reminder.is_completed = data['is_completed']
        if 'is_recurring' in data:
            reminder.is_recurring = data['is_recurring']
        if 'recurring_type' in data:
            reminder.recurring_type = data['recurring_type']
        
        reminder.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'reminder': reminder.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@reminders_bp.route('/reminders/<int:reminder_id>', methods=['DELETE'])
def delete_reminder(reminder_id):
    """删除提醒"""
    try:
        user_id = 1  # 暂时使用用户ID=1
        reminder = Reminder.query.filter_by(id=reminder_id, user_id=user_id).first()
        
        if not reminder:
            return jsonify({'success': False, 'error': '提醒不存在'}), 404
        
        db.session.delete(reminder)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@reminders_bp.route('/reminders/import', methods=['POST'])
def import_reminders():
    """导入提醒数据"""
    try:
        data = request.get_json()
        user_id = 1  # 暂时使用用户ID=1
        
        imported_count = 0
        for reminder_data in data.get('reminders', []):
            reminder = Reminder(
                user_id=user_id,
                title=reminder_data['title'],
                content=reminder_data.get('content', ''),
                remind_at=datetime.fromisoformat(reminder_data['remind_at'].replace('Z', '+00:00')),
                is_completed=reminder_data.get('is_completed', False),
                is_recurring=reminder_data.get('is_recurring', False),
                recurring_type=reminder_data.get('recurring_type')
            )
            db.session.add(reminder)
            imported_count += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'imported_count': imported_count
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500