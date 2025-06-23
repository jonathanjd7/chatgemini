#!/usr/bin/env python
"""
Script para probar los modelos de Gemini disponibles
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_models_endpoint():
    """Probar endpoint de modelos disponibles"""
    print("🔍 Verificando modelos disponibles...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/models")
        if response.status_code == 200:
            data = response.json()
            print("✅ Modelos disponibles:")
            for model in data['available_models']:
                print(f"   - {model}")
            print(f"📊 Total: {data['total']} modelos")
            return True
        else:
            print(f"❌ Error al obtener modelos: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_status_endpoint():
    """Probar endpoint de status"""
    print("\n🔍 Verificando status de la API...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/status")
        if response.status_code == 200:
            data = response.json()
            print("✅ Status API:")
            print(f"   - Estado: {data['status']}")
            print(f"   - Gemini configurado: {data['gemini_configured']}")
            print(f"   - Modelos disponibles: {len(data.get('available_models', []))}")
            return True
        else:
            print(f"❌ Error en status: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_chat_functionality():
    """Probar funcionalidad completa de chat"""
    print("\n🧪 Probando funcionalidad de chat completa...")
    
    # 1. Registrar usuario de prueba
    print("📝 1. Registrando usuario de prueba...")
    test_user = {
        "email": "test_models@example.com",
        "password": "test123456"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code in [201, 400]:  # 400 si ya existe
            print("✅ Usuario registrado/ya existe")
        else:
            print(f"❌ Error registrando usuario: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Error en registro: {e}")
        return False
    
    # 2. Login
    print("🔐 2. Haciendo login...")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            token = response.json().get('access_token')
            print("✅ Login exitoso")
        else:
            print(f"❌ Error en login: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Error en login: {e}")
        return False
    
    # 3. Probar chat con Gemini
    print("💬 3. Probando chat con Gemini...")
    try:
        chat_message = {
            "content": "Hola, ¿puedes responder con un saludo breve?"
        }
        
        response = requests.post(
            f"{BASE_URL}/chat/send",
            json=chat_message,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Chat funcionando correctamente!")
            print(f"   Mensaje enviado: {data['user_message'][:50]}...")
            print(f"   Respuesta Gemini: {data['gemini_response'][:100]}...")
            return True
        else:
            print(f"❌ Error en chat: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Error en chat: {e}")
        return False

def main():
    """Ejecutar todas las pruebas"""
    print("🎯 PRUEBA DE MODELOS GEMINI")
    print("=" * 50)
    
    # Esperar que la API esté lista
    print("⏳ Esperando que la API esté lista...")
    time.sleep(3)
    
    results = []
    
    # Ejecutar pruebas
    results.append(("Status API", test_status_endpoint()))
    results.append(("Modelos disponibles", test_models_endpoint()))
    results.append(("Chat completo", test_chat_functionality()))
    
    # Mostrar resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! Los modelos de Gemini funcionan correctamente.")
        print("\n🚀 Puedes usar la aplicación en: http://localhost:5000")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa la configuración de Gemini.")

if __name__ == "__main__":
    main() 