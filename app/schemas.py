from marshmallow import Schema, fields, validate, validates, ValidationError
import re

class UserRegistrationSchema(Schema):
    """Esquema para validar registro de usuario"""
    email = fields.Email(required=True, validate=validate.Length(max=120))
    password = fields.Str(required=True, validate=validate.Length(min=6, max=100))
    
    @validates('password')
    def validate_password(self, value):
        """Validar fortaleza de contraseña"""
        if len(value) < 6:
            raise ValidationError('Password must be at least 6 characters long')

class UserLoginSchema(Schema):
    """Esquema para validar login de usuario"""
    email = fields.Email(required=True, validate=validate.Length(max=120))
    password = fields.Str(required=True, validate=validate.Length(min=1, max=100))

class ConversationSchema(Schema):
    """Esquema para validar creación de conversación"""
    title = fields.Str(validate=validate.Length(max=200), missing='Nueva Conversación')

class ChatMessageSchema(Schema):
    """Esquema para validar mensajes de chat"""
    content = fields.Str(required=True, validate=[
        validate.Length(min=1, max=5000),
        lambda x: x.strip() != '' or ValidationError('Message cannot be empty')
    ])

class UserUpdateSchema(Schema):
    """Esquema para actualizar perfil de usuario"""
    email = fields.Email(validate=validate.Length(max=120))
    current_password = fields.Str(validate=validate.Length(min=6, max=100))
    new_password = fields.Str(validate=validate.Length(min=6, max=100))
    
    @validates('new_password')
    def validate_new_password(self, value):
        """Validar fortaleza de nueva contraseña"""
        if len(value) < 6:
            raise ValidationError('Password must be at least 6 characters long') 