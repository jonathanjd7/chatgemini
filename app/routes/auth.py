from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app import db
from app.models import User
from app.schemas import UserRegistrationSchema, UserLoginSchema
from app.utils import handle_error

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Registrar nuevo usuario"""
    try:
        # Obtener datos del request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        # Validaciones básicas
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters long'}), 400
        
        # Verificar si el email ya existe
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # Crear username basado en email (parte antes del @)
        username = email.split('@')[0]
        
        # Asegurar que el username sea único
        counter = 1
        original_username = username
        while User.query.filter_by(username=username).first():
            username = f"{original_username}{counter}"
            counter += 1
        
        # Crear nuevo usuario
        user = User(
            username=username,
            email=email
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Crear tokens (convertir ID a string)
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict(),
            'user_id': user.id,
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@auth_bp.route('/login', methods=['POST'])
def login():
    """Iniciar sesión"""
    try:
        # Obtener datos del request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        # Validaciones básicas
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Buscar usuario por email (no username)
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Account is disabled'}), 401
        
        # Crear tokens (convertir ID a string)
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'user_id': user.id,
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
        
    except Exception as e:
        return handle_error(e)

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refrescar token de acceso"""
    try:
        current_user_id = get_jwt_identity()
        new_token = create_access_token(identity=str(current_user_id))
        
        return jsonify({
            'access_token': new_token
        }), 200
        
    except Exception as e:
        return handle_error(e)

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Obtener perfil del usuario actual"""
    try:
        current_user_id = int(get_jwt_identity())  # Convertir de string a int
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return handle_error(e) 