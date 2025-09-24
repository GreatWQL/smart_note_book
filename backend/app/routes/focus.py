from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import FocusSession

focus_bp = Blueprint('focus', __name__)

@focus_bp.route('', methods=['POST'])
@jwt_required()
def create_focus_session():
    """创建专注记录"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('duration_minutes'):
            return jsonify({'error': '专注时长是必需的'}), 400
        
        focus_session = FocusSession(
            user_id=user_id,
            project_id=data.get('project_id'),
            duration_minutes=data['duration_minutes']
        )
        
        db.session.add(focus_session)
        db.session.commit()
        
        return jsonify({'message': '专注记录创建成功', 'focus_session': focus_session.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'创建专注记录失败: {str(e)}'}), 500

@focus_bp.route('', methods=['GET'])
@jwt_required()
def get_focus_sessions():
    """获取专注记录"""
    try:
        user_id = get_jwt_identity()
        sessions = FocusSession.query.filter_by(user_id=user_id).order_by(FocusSession.start_time.desc()).all()
        return jsonify({'focus_sessions': [session.to_dict() for session in sessions]}), 200
    except Exception as e:
        return jsonify({'error': f'获取专注记录失败: {str(e)}'}), 500