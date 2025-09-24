from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func, extract
from datetime import datetime, timedelta
from app import db
from app.models import Task, FocusSession, Note, Project

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/tasks-summary', methods=['GET'])
@jwt_required()
def get_tasks_summary():
    """获取任务完成统计数据"""
    try:
        user_id = get_jwt_identity()
        
        # 获取最近7天的任务完成数据
        end_date = datetime.now()
        start_date = end_date - timedelta(days=6)
        
        # 按日期分组统计完成的任务数量
        completed_tasks = db.session.query(
            func.date(Task.updated_at).label('date'),
            func.count(Task.id).label('count')
        ).filter(
            Task.user_id == user_id,
            Task.status == 'done',
            Task.updated_at >= start_date,
            Task.updated_at <= end_date
        ).group_by(func.date(Task.updated_at)).all()
        
        # 构建完整的7天数据
        data = []
        for i in range(7):
            current_date = (start_date + timedelta(days=i)).date()
            count = 0
            for task_data in completed_tasks:
                if task_data.date == current_date:
                    count = task_data.count
                    break
            data.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'count': count
            })
        
        return jsonify({'tasks_summary': data}), 200
    except Exception as e:
        return jsonify({'error': f'获取任务统计失败: {str(e)}'}), 500

@analytics_bp.route('/focus-distribution', methods=['GET'])
@jwt_required()
def get_focus_distribution():
    """获取项目专注时长分布数据"""
    try:
        user_id = get_jwt_identity()
        
        # 按项目统计专注时长
        focus_data = db.session.query(
            Project.name.label('project_name'),
            func.sum(FocusSession.duration_minutes).label('total_minutes')
        ).join(
            FocusSession, Project.id == FocusSession.project_id
        ).filter(
            FocusSession.user_id == user_id
        ).group_by(Project.id, Project.name).all()
        
        # 添加无项目的专注时长
        no_project_focus = db.session.query(
            func.sum(FocusSession.duration_minutes).label('total_minutes')
        ).filter(
            FocusSession.user_id == user_id,
            FocusSession.project_id.is_(None)
        ).scalar()
        
        data = []
        for item in focus_data:
            data.append({
                'name': item.project_name,
                'value': item.total_minutes or 0
            })
        
        if no_project_focus:
            data.append({
                'name': '无项目',
                'value': no_project_focus
            })
        
        return jsonify({'focus_distribution': data}), 200
    except Exception as e:
        return jsonify({'error': f'获取专注分布失败: {str(e)}'}), 500

@analytics_bp.route('/word-count-trend', methods=['GET'])
@jwt_required()
def get_word_count_trend():
    """获取笔记字数增长趋势"""
    try:
        user_id = get_jwt_identity()
        
        # 获取最近30天的笔记字数变化
        end_date = datetime.now()
        start_date = end_date - timedelta(days=29)
        
        # 按日期统计笔记总字数
        notes_data = db.session.query(
            func.date(Note.created_at).label('date'),
            func.sum(func.length(Note.content)).label('total_chars')
        ).filter(
            Note.user_id == user_id,
            Note.created_at >= start_date,
            Note.created_at <= end_date
        ).group_by(func.date(Note.created_at)).all()
        
        # 构建累积字数数据
        data = []
        cumulative_chars = 0
        
        # 获取开始日期之前的总字数
        previous_chars = db.session.query(
            func.sum(func.length(Note.content))
        ).filter(
            Note.user_id == user_id,
            Note.created_at < start_date
        ).scalar() or 0
        
        cumulative_chars = previous_chars
        
        for i in range(30):
            current_date = (start_date + timedelta(days=i)).date()
            daily_chars = 0
            
            for note_data in notes_data:
                if note_data.date == current_date:
                    daily_chars = note_data.total_chars or 0
                    break
            
            cumulative_chars += daily_chars
            data.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'word_count': cumulative_chars // 2  # 简单估算：字符数除以2约等于字数
            })
        
        return jsonify({'word_count_trend': data}), 200
    except Exception as e:
        return jsonify({'error': f'获取字数趋势失败: {str(e)}'}), 500