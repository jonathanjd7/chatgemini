#!/usr/bin/env python
"""
Script de configuración para crear el archivo .env
Ejecuta este script para configurar automáticamente las variables de entorno
"""

import os
import secrets
import getpass

def generate_secret_key():
    """Generar una clave secreta segura"""
    return secrets.token_urlsafe(32)

def create_env_file():
    """Crear archivo .env con configuración básica"""
    
    print("🔧 Configuración de Flask Gemini Chat API")
    print("=" * 50)
    
    # Verificar si .env ya existe
    if os.path.exists('.env'):
        overwrite = input("El archivo .env ya existe. ¿Deseas sobrescribirlo? (y/N): ")
        if overwrite.lower() != 'y':
            print("❌ Configuración cancelada.")
            return
    
    # Generar claves secretas automáticamente
    secret_key = generate_secret_key()
    jwt_secret = generate_secret_key()
    
    # Solicitar API Key de Gemini
    print("\n📝 Necesitas obtener tu API Key de Google Gemini:")
    print("1. Ve a: https://makersuite.google.com/app/apikey")
    print("2. Crea una nueva API Key")
    print("3. Cópiala y pégala aquí")
    
    gemini_api_key = getpass.getpass("\n🔑 Ingresa tu GEMINI_API_KEY: ").strip()
    
    if not gemini_api_key:
        print("❌ API Key de Gemini es requerida. Configuración cancelada.")
        return
    
    # Configurar entorno
    environment = input("\n🌍 Entorno (development/production) [development]: ").strip() or "development"
    
    # Configurar base de datos
    print("\n💾 Configuración de base de datos:")
    print("1. SQLite (recomendado para desarrollo)")
    print("2. PostgreSQL")
    print("3. MySQL")
    
    db_choice = input("Selecciona (1-3) [1]: ").strip() or "1"
    
    if db_choice == "1":
        database_url = "sqlite:///chat.db"
    elif db_choice == "2":
        db_user = input("Usuario PostgreSQL: ").strip()
        db_pass = getpass.getpass("Contraseña PostgreSQL: ").strip()
        db_host = input("Host PostgreSQL [localhost]: ").strip() or "localhost"
        db_port = input("Puerto PostgreSQL [5432]: ").strip() or "5432"
        db_name = input("Nombre de la base de datos: ").strip()
        database_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    else:
        db_user = input("Usuario MySQL: ").strip()
        db_pass = getpass.getpass("Contraseña MySQL: ").strip()
        db_host = input("Host MySQL [localhost]: ").strip() or "localhost"
        db_port = input("Puerto MySQL [3306]: ").strip() or "3306"
        db_name = input("Nombre de la base de datos: ").strip()
        database_url = f"mysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    
    # Crear contenido del archivo .env
    env_content = f"""# Configuración Flask
FLASK_APP=run.py
FLASK_ENV={environment}

# Claves secretas (generadas automáticamente)
SECRET_KEY={secret_key}
JWT_SECRET_KEY={jwt_secret}

# Base de datos
DATABASE_URL={database_url}

# API Key de Google Gemini
GEMINI_API_KEY={gemini_api_key}

# Configuración CORS (para desarrollo)
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
"""
    
    # Escribir archivo .env
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("\n✅ Archivo .env creado exitosamente!")
        print("\n📋 Configuración aplicada:")
        print(f"   - Entorno: {environment}")
        print(f"   - Base de datos: {database_url}")
        print(f"   - API Key configurada: {'✓' if gemini_api_key else '✗'}")
        print(f"   - Claves secretas: Generadas automáticamente")
        
        print("\n🚀 Próximos pasos:")
        print("1. Instalar dependencias: pip install -r requirements.txt")
        print("2. Inicializar base de datos: flask db init")
        print("3. Crear migraciones: flask db migrate -m 'Initial migration'")
        print("4. Aplicar migraciones: flask db upgrade")
        print("5. Ejecutar aplicación: python run.py")
        
    except Exception as e:
        print(f"❌ Error al crear archivo .env: {e}")

def show_manual_setup():
    """Mostrar instrucciones para configuración manual"""
    print("\n📖 CONFIGURACIÓN MANUAL")
    print("=" * 50)
    print("Si prefieres configurar manualmente, crea un archivo llamado '.env' con:")
    print()
    print("FLASK_APP=run.py")
    print("FLASK_ENV=development")
    print("SECRET_KEY=tu_secreto_muy_seguro")
    print("JWT_SECRET_KEY=otro_secreto_jwt")
    print("DATABASE_URL=sqlite:///chat.db")
    print("GEMINI_API_KEY=TU_API_KEY_GOOGLE_GEMINI")
    print("CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000")
    print()
    print("🔑 Para obtener tu API Key de Gemini:")
    print("1. Ve a: https://makersuite.google.com/app/apikey")
    print("2. Crea una nueva API Key")
    print("3. Reemplaza 'TU_API_KEY_GOOGLE_GEMINI' con tu clave real")

if __name__ == "__main__":
    print("🎯 Configurador de Flask Gemini Chat API")
    print("=" * 50)
    
    choice = input("¿Deseas configuración automática (a) o ver instrucciones manuales (m)? [a]: ").strip().lower()
    
    if choice == 'm':
        show_manual_setup()
    else:
        create_env_file() 