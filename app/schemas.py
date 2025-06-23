from marshmallow import Schema, fields, validate, validates, ValidationError
import re

class UserRegistrationSchema(Schema):
    """Esquema para validar registro de usuario"""
    username = fields.Str(required=True, validate=[
        validate.Length(min=3, max=80),
        validate.Regexp(r'^[a-zA-Z0-9_]+$', error='Username can only contain letters, numbers and underscores')
    ])
    email = fields.Email(required=True, validate=validate.Length(max=120))
    password = fields.Str(required=True, validate=validate.Length(min=6, max=100))
    confirm_password = fields.Str(required=True)
    
    @validates('password')
    def validate_password(self, value):
        """Validar fortaleza de contraseña"""
        if not re.search(r'[A-Za-z]', value):
            raise ValidationError('Password must contain at least one letter')
        if not re.search(r'[0-9]', value):
            raise ValidationError('Password must contain at least one number')
    
    def validate_passwords_match(self, data, **kwargs):
        """Validar que las contraseñas coincidan"""
        if 'password' in data and 'confirm_password' in data:
            if data['password'] != data['confirm_password']:
                raise ValidationError({'confirm_password': ['Passwords must match']})
        return data

class UserLoginSchema(Schema):
    """Esquema para validar login de usuario"""
    username = fields.Str(required=True, validate=validate.Length(min=1, max=80))
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
        if not re.search(r'[A-Za-z]', value):
            raise ValidationError('Password must contain at least one letter')
        if not re.search(r'[0-9]', value):
            raise ValidationError('Password must contain at least one number') 