#!/usr/bin/env python
"""
Script para configurar el archivo .env con valores básicos
"""

import os
import secrets

def setup_env():
    """Configurar archivo .env con valores básicos"""
    
    # Generar clave JWT segura
    jwt_secret = secrets.token_urlsafe(32)
    
    env_content = f"""# Configuracion Flask Gemini API
# Generado automaticamente

# Secretos JWT (generado automaticamente)
JWT_SECRET_KEY={jwt_secret}

# Base de datos
DATABASE_URL=sqlite:///chat.db

# API Key de Google Gemini
# IMPORTANTE: Configura tu API Key aqui
# Obten tu clave en: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print("✅ Archivo .env configurado correctamente")
        print("📝 Configuración aplicada:")
        print(f"   - JWT Secret: Generada automáticamente")
        print(f"   - Database: SQLite (chat.db)")
        print(f"   - Gemini API Key: ⚠️ NECESITA CONFIGURACIÓN")
        print()
        print("🔑 IMPORTANTE: Para usar Gemini AI, configura tu API Key:")
        print("   1. Ve a: https://makersuite.google.com/app/apikey")
        print("   2. Crea una nueva API Key")
        print("   3. Edita el archivo .env y pega tu API Key")
        print()
        print("🚀 La aplicación funcionará sin Gemini para las rutas de autenticación")
        
    except Exception as e:
        print(f"❌ Error al crear archivo .env: {e}")

if __name__ == "__main__":
    print("🔧 Configurando archivo .env...")
    setup_env() 