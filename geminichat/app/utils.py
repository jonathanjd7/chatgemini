import logging
from datetime import datetime
from flask import jsonify, current_app
import google.generativeai as genai
from app.config import Config

def handle_error(error):
    """Manejar errores de forma centralizada"""
    # Log del error
    current_app.logger.error(f"Error: {str(error)}")
    
    # Si es un error conocido, devolver mensaje específico
    if hasattr(error, 'code'):
        return jsonify({'error': str(error)}), error.code
    
    # Error genérico del servidor
    return jsonify({'error': 'Internal server error'}), 500

def configure_gemini():
    """Configurar la API de Gemini"""
    api_key = current_app.config.get('GEMINI_API_KEY')
    
    if not api_key:
        raise ValueError('GEMINI_API_KEY not found in configuration')
    
    genai.configure(api_key=api_key)

def validate_gemini_response(response):
    """Validar respuesta de Gemini AI"""
    if not response or not hasattr(response, 'text'):
        raise ValueError('Invalid response from Gemini AI')
    
    if not response.text or response.text.strip() == '':
        raise ValueError('Empty response from Gemini AI')
    
    return True

def setup_logging(app):
    """Configurar logging para la aplicación"""
    if not app.debug and not app.testing:
        # Configurar logging para producción
        if not app.logger.handlers:
            file_handler = logging.FileHandler('logs/flask_gemini.log')
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            app.logger.setLevel(logging.INFO)
            app.logger.info('Flask Gemini startup')

def sanitize_input(text):
    """Sanitizar entrada de texto para prevenir inyecciones"""
    if not isinstance(text, str):
        return str(text)
    
    # Remover caracteres peligrosos básicos
    dangerous_chars = ['<', '>', '"', "'", '&']
    for char in dangerous_chars:
        text = text.replace(char, '')
    
    return text.strip()

def truncate_text(text, max_length=1000):
    """Truncar texto si es muy largo"""
    if len(text) <= max_length:
        return text
    
    return text[:max_length] + "..."

def format_api_response(success=True, message=None, data=None, errors=None):
    """Formatear respuesta estándar de API"""
    response = {
        'success': success,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    if message:
        response['message'] = message
    
    if data:
        response['data'] = data
    
    if errors:
        response['errors'] = errors
    
    return response 