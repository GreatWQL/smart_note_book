from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # 配置
    app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smart_notebook.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string-change-in-production'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Token不过期，简化开发
    
    # 初始化扩展
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # 注册蓝图
    from app.routes.auth import auth_bp
    from app.routes.notes import notes_bp
    from app.routes.tasks import tasks_bp
    from app.routes.projects import projects_bp
    from app.routes.focus import focus_bp
    from app.routes.analytics import analytics_bp
    from app.routes.data import data_bp
    from app.routes.reminders import reminders_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(notes_bp, url_prefix='/api/notes')
    app.register_blueprint(tasks_bp, url_prefix='/api/tasks')
    app.register_blueprint(projects_bp, url_prefix='/api/projects')
    app.register_blueprint(focus_bp, url_prefix='/api/focus-sessions')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    app.register_blueprint(data_bp, url_prefix='/api/data')
    app.register_blueprint(reminders_bp, url_prefix='/api')
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    return app