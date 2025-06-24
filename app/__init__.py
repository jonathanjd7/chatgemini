from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import Config

# Inicialización de extensiones
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app(config_class=Config):
    """Factory pattern para crear la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Ruta principal
    @app.route('/')
    def index():
        return render_template('index.html')
    
    
    # Registrar blueprints
    from app.routes.auth import auth_bp
    from app.routes.chat import chat_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    
    # Importar modelos para que Flask-Migrate los detecte
    from app import models
    
    return app 