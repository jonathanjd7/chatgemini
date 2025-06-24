from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
import google.generativeai as genai
from app import db
from app.models import User, Conversation, Message
from app.schemas import ChatMessageSchema, ConversationSchema
from app.utils import handle_error, configure_gemini
from app.config import Config

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/conversations', methods=['GET'])
@jwt_required()
def get_conversations():
    """Obtener todas las conversaciones del usuario"""
    try:
        current_user_id = int(get_jwt_identity())
        conversations = Conversation.query.filter_by(user_id=current_user_id).order_by(Conversation.updated_at.desc()).all()
        
        return jsonify({
            'conversations': [conv.to_dict() for conv in conversations]
        }), 200
        
    except Exception as e:
        return handle_error(e)

@chat_bp.route('/conversations', methods=['POST'])
@jwt_required()
def create_conversation():
    """Crear nueva conversación"""
    try:
        current_user_id = int(get_jwt_identity())
        schema = ConversationSchema()
        data = schema.load(request.json)
        
        conversation = Conversation(
            user_id=current_user_id,
            title=data.get('title', 'Nueva Conversación')
        )
        
        db.session.add(conversation)
        db.session.commit()
        
        return jsonify({
            'message': 'Conversation created successfully',
            'conversation': conversation.to_dict()
        }), 201
        
    except ValidationError as e:
        return jsonify({'errors': e.messages}), 400
    except Exception as e:
        return handle_error(e)

@chat_bp.route('/conversations/<int:conversation_id>/messages', methods=['GET'])
@jwt_required()
def get_messages(conversation_id):
    """Obtener mensajes de una conversación"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # Verificar que la conversación pertenece al usuario
        conversation = Conversation.query.filter_by(id=conversation_id, user_id=current_user_id).first()
        if not conversation:
            return jsonify({'error': 'Conversation not found'}), 404
        
        messages = Message.query.filter_by(conversation_id=conversation_id).order_by(Message.timestamp.asc()).all()
        
        return jsonify({
            'messages': [msg.to_dict() for msg in messages]
        }), 200
        
    except Exception as e:
        return handle_error(e)

@chat_bp.route('/conversations/<int:conversation_id>/messages', methods=['POST'])
@jwt_required()
def send_message(conversation_id):
    """Enviar mensaje y obtener respuesta de Gemini"""
    try:
        current_user_id = int(get_jwt_identity())
        schema = ChatMessageSchema()
        data = schema.load(request.json)
        
        # Verificar que la conversación pertenece al usuario
        conversation = Conversation.query.filter_by(id=conversation_id, user_id=current_user_id).first()
        if not conversation:
            return jsonify({'error': 'Conversation not found'}), 404
        
        # Configurar y usar Gemini
        configure_gemini()
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Obtener historial de la conversación para contexto ANTES de agregar el nuevo mensaje
        previous_messages = Message.query.filter_by(conversation_id=conversation_id).order_by(Message.timestamp.asc()).all()
        
        # Verificar si es el primer mensaje para generar título automático
        is_first_message = len(previous_messages) == 0
        
        
        # Guardar mensaje del usuario
        user_message = Message(
            conversation_id=conversation_id,
            content=data['content'],
            role='user'
        )
        db.session.add(user_message)
        
        # Construir contexto para Gemini
        context = []
        for msg in previous_messages:
            context.append(f"{msg.role}: {msg.content}")
        
        # Añadir el nuevo mensaje
        context.append(f"user: {data['content']}")
        
        # Generar respuesta
        prompt = "\n".join(context)
        response = model.generate_content(prompt)
        
        # Guardar respuesta de Gemini
        ai_message = Message(
            conversation_id=conversation_id,
            content=response.text,
            role='assistant'
        )
        db.session.add(ai_message)
        
        # Si es el primer mensaje, generar título automático
        conversation_updated = False
        if is_first_message and conversation.title == 'Nueva Conversación':
            try:
                # Generar título basado en el primer mensaje
                title_prompt = f"""Genera un título descriptivo y conciso (máximo 6 palabras) para una conversación que comienza con este mensaje: "{data['content']}"

Responde SOLO con el título, sin comillas ni explicaciones adicionales. El título debe ser claro y representar el tema principal."""
                
                title_response = model.generate_content(title_prompt)
                generated_title = title_response.text.strip()
                
                # Limpiar el título (remover comillas si las hay)
                generated_title = generated_title.replace('"', '').replace("'", "").strip()
                
                # Validar que el título no esté vacío y no sea muy largo
                if generated_title and len(generated_title) <= 50:
                    conversation.title = generated_title
                    conversation_updated = True
                else:
                    # Fallback: usar las primeras palabras del mensaje
                    words = data['content'].split()[:6]
                    conversation.title = ' '.join(words) + ('...' if len(data['content'].split()) > 6 else '')
                    conversation_updated = True
                    
            except Exception as title_error:
                print(f"Error generando título: {title_error}")
                # Fallback: usar las primeras palabras del mensaje
                words = data['content'].split()[:6]
                conversation.title = ' '.join(words) + ('...' if len(data['content'].split()) > 6 else '')
                conversation_updated = True
        
        # Actualizar timestamp de la conversación
        conversation.updated_at = db.func.now()
        
        db.session.commit()
        
        response_data = {
            'user_message': user_message.to_dict(),
            'ai_response': ai_message.to_dict()
        }
        
        # Incluir información de la conversación actualizada si cambió el título
        if conversation_updated:
            response_data['conversation_updated'] = conversation.to_dict()
        
        return jsonify(response_data), 200
        
    except ValidationError as e:
        return jsonify({'errors': e.messages}), 400
    except Exception as e:
        return handle_error(e)

@chat_bp.route('/conversations/<int:conversation_id>', methods=['DELETE'])
@jwt_required()
def delete_conversation(conversation_id):
    """Eliminar conversación"""
    try:
        current_user_id = int(get_jwt_identity())
        
        conversation = Conversation.query.filter_by(id=conversation_id, user_id=current_user_id).first()
        if not conversation:
            return jsonify({'error': 'Conversation not found'}), 404
        
        db.session.delete(conversation)
        db.session.commit()
        
        return jsonify({
            'message': 'Conversation deleted successfully'
        }), 200
        
    except Exception as e:
        return handle_error(e) 