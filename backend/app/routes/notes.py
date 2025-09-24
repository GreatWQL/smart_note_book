from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Note

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('', methods=['GET'])
@jwt_required()
def get_notes():
    """获取当前用户的所有笔记"""
    try:
        user_id = get_jwt_identity()
        notes = Note.query.filter_by(user_id=user_id).order_by(Note.updated_at.desc()).all()
        return jsonify({'notes': [note.to_dict() for note in notes]}), 200
    except Exception as e:
        return jsonify({'error': f'获取笔记失败: {str(e)}'}), 500

@notes_bp.route('', methods=['POST'])
@jwt_required()
def create_note():
    """创建新笔记"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('title'):
            return jsonify({'error': '笔记标题是必需的'}), 400
        
        note = Note(
            user_id=user_id,
            title=data['title'],
            content=data.get('content', ''),
            folder=data.get('folder', '默认文件夹')
        )
        
        db.session.add(note)
        db.session.commit()
        
        return jsonify({'message': '笔记创建成功', 'note': note.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'创建笔记失败: {str(e)}'}), 500

@notes_bp.route('/<int:note_id>', methods=['PUT'])
@jwt_required()
def update_note(note_id):
    """更新笔记"""
    try:
        user_id = get_jwt_identity()
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        
        if not note:
            return jsonify({'error': '笔记不存在'}), 404
        
        data = request.get_json()
        if data.get('title'):
            note.title = data['title']
        if 'content' in data:
            note.content = data['content']
        if data.get('folder'):
            note.folder = data['folder']
        
        db.session.commit()
        return jsonify({'message': '笔记更新成功', 'note': note.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'更新笔记失败: {str(e)}'}), 500

@notes_bp.route('/<int:note_id>', methods=['DELETE'])
@jwt_required()
def delete_note(note_id):
    """删除笔记"""
    try:
        user_id = get_jwt_identity()
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        
        if not note:
            return jsonify({'error': '笔记不存在'}), 404
        
        db.session.delete(note)
        db.session.commit()
        
        return jsonify({'message': '笔记删除成功'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'删除笔记失败: {str(e)}'}), 500