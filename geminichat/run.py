import os
from dotenv import load_dotenv
from app import create_app, db
from app.models import User, Conversation, Message

# Cargar variables de entorno
load_dotenv()

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Contexto para Flask shell"""
    return {
        'db': db,
        'User': User,
        'Conversation': Conversation,
        'Message': Message
    }

@app.cli.command()
def create_db():
    """Crear todas las tablas de la base de datos"""
    db.create_all()
    print("Database tables created successfully!")

@app.cli.command()
def drop_db():
    """Eliminar todas las tablas de la base de datos"""
    db.drop_all()
    print("Database tables dropped successfully!")

@app.cli.command()
def reset_db():
    """Resetear la base de datos"""
    db.drop_all()
    db.create_all()
    print("Database reset successfully!")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 