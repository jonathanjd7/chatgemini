import os
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from marshmallow import Schema, fields, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
import google.generativeai as genai
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Inicializar Flask
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Inicializar JWT
jwt = JWTManager(app)

# Configurar base de datos SQLAlchemy
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///chat.db')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Configurar Google Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Modelos de base de datos
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relación con mensajes de chat
    messages = relationship("ChatMessage", back_populates="user")

class ChatMessage(Base):
    __tablename__ = 'chat_messages'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user_message = Column(Text, nullable=False)
    gemini_response = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relación con usuario
    user = relationship("User", back_populates="messages")

# Crear tablas
Base.metadata.create_all(bind=engine)

# Schemas de validación con Marshmallow
class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=lambda x: len(x) >= 6)

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class ChatSchema(Schema):
    content = fields.Str(required=True)

# Funciones auxiliares
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        pass

def list_available_models():
    """Listar modelos disponibles de Gemini"""
    try:
        models = genai.list_models()
        available = []
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                available.append(model.name)
        return available
    except Exception as e:
        print(f"Error al listar modelos: {e}")
        return []

def generate_gemini_response(user_input):
    """Generar respuesta usando Google Gemini"""
    try:
        # Crear cliente y generar respuesta con el modelo actualizado
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        # Si falla con gemini-1.5-flash, intentar con gemini-1.5-pro
        try:
            model = genai.GenerativeModel('gemini-1.5-pro')
            response = model.generate_content(user_input)
            return response.text
        except Exception as e2:
            # Como último recurso, intentar con gemini-1.0-pro
            try:
                model = genai.GenerativeModel('gemini-1.0-pro')
                response = model.generate_content(user_input)
                return response.text
            except Exception as e3:
                return f"Error al generar respuesta: {str(e3)}"

# RUTAS DE AUTENTICACIÓN
@app.route('/auth/register', methods=['POST'])
def register():
    """Registrar nuevo usuario con email + contraseña"""
    try:
        # Validar datos de entrada
        schema = RegisterSchema()
        data = schema.load(request.json)
        
        db = get_db()
        
        # Verificar si el usuario ya existe
        existing_user = db.query(User).filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'error': 'El email ya está registrado'}), 400
        
        # Crear nuevo usuario
        hashed_password = generate_password_hash(data['password'])
        new_user = User(
            email=data['email'],
            password_hash=hashed_password
        )
        
        db.add(new_user)
        db.commit()
        
        return jsonify({
            'message': 'Usuario registrado exitosamente',
            'user_id': new_user.id
        }), 201
        
    except ValidationError as e:
        return jsonify({'errors': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@app.route('/auth/login', methods=['POST'])
def login():
    """Login y devolución de token JWT"""
    try:
        # Validar datos de entrada
        schema = LoginSchema()
        data = schema.load(request.json)
        
        db = get_db()
        
        # Buscar usuario
        user = db.query(User).filter_by(email=data['email']).first()
        
        if not user or not check_password_hash(user.password_hash, data['password']):
            return jsonify({'error': 'Credenciales inválidas'}), 401
        
        # Crear token JWT
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'message': 'Login exitoso',
            'access_token': access_token,
            'user_id': user.id
        }), 200
        
    except ValidationError as e:
        return jsonify({'errors': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

# RUTAS DE CHAT
@app.route('/chat/send', methods=['POST'])
@jwt_required()
def send_message():
    """Enviar mensaje al modelo Gemini y retornar respuesta"""
    try:
        # Validar datos de entrada
        schema = ChatSchema()
        data = schema.load(request.json)
        
        # Obtener ID del usuario desde JWT
        current_user_id = int(get_jwt_identity())
        
        # Verificar que Gemini esté configurado
        if not GEMINI_API_KEY:
            return jsonify({'error': 'API Key de Gemini no configurada'}), 500
        
        # Generar respuesta con Gemini
        user_message = data['content']
        gemini_response = generate_gemini_response(user_message)
        
        # Guardar en base de datos
        db = get_db()
        chat_message = ChatMessage(
            user_id=current_user_id,
            user_message=user_message,
            gemini_response=gemini_response
        )
        
        db.add(chat_message)
        db.commit()
        
        return jsonify({
            'message': 'Mensaje enviado exitosamente',
            'user_message': user_message,
            'gemini_response': gemini_response,
            'timestamp': chat_message.timestamp.isoformat()
        }), 200
        
    except ValidationError as e:
        return jsonify({'errors': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@app.route('/chat/history', methods=['GET'])
@jwt_required()
def get_chat_history():
    """Obtener historial de chats del usuario"""
    try:
        # Obtener ID del usuario desde JWT
        current_user_id = int(get_jwt_identity())
        
        db = get_db()
        
        # Obtener mensajes del usuario ordenados por fecha
        messages = db.query(ChatMessage).filter_by(user_id=current_user_id)\
            .order_by(ChatMessage.timestamp.desc()).all()
        
        # Formatear respuesta
        chat_history = []
        for msg in messages:
            chat_history.append({
                'id': msg.id,
                'user_message': msg.user_message,
                'gemini_response': msg.gemini_response,
                'timestamp': msg.timestamp.isoformat()
            })
        
        return jsonify({
            'message': 'Historial obtenido exitosamente',
            'total_messages': len(chat_history),
            'chat_history': chat_history
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

# RUTAS FRONTEND
@app.route('/')
def index():
    """Página principal del chat"""
    return render_template('index.html')

# RUTA BÁSICA DE PRUEBA API
@app.route('/api/status', methods=['GET'])
def health_check():
    """Ruta básica para verificar que la API funciona"""
    available_models = []
    if GEMINI_API_KEY:
        available_models = list_available_models()
    
    return jsonify({
        'message': 'Flask Gemini API funcionando correctamente',
        'status': 'OK',
        'gemini_configured': bool(GEMINI_API_KEY),
        'available_models': available_models
    }), 200

@app.route('/api/models', methods=['GET'])
def get_available_models():
    """Obtener lista de modelos disponibles"""
    if not GEMINI_API_KEY:
        return jsonify({'error': 'API Key de Gemini no configurada'}), 500
    
    models = list_available_models()
    return jsonify({
        'available_models': models,
        'total': len(models)
    }), 200

# MANEJO DE ERRORES
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint no encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500

if __name__ == '__main__':
    print("🚀 Iniciando Flask Gemini API...")
    print("📋 Rutas disponibles:")
    print("   POST /auth/register - Registrar usuario")
    print("   POST /auth/login - Iniciar sesión")
    print("   POST /chat/send - Enviar mensaje (JWT requerido)")
    print("   GET /chat/history - Obtener historial (JWT requerido)")
    print("   GET / - Verificar estado")
    print(f"🔑 Gemini configurado: {'✅' if GEMINI_API_KEY else '❌'}")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000) 