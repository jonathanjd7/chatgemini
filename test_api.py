#!/usr/bin/env python
"""
Script de prueba para verificar el funcionamiento de Flask Gemini API
Prueba todas las rutas implementadas
"""

import requests
import json
import time

# Configuración
BASE_URL = "http://localhost:5000"
TEST_USER = {
    "email": "test@example.com",
    "password": "test123456"
}

def print_separator(title):
    print(f"\n{'='*50}")
    print(f"🧪 {title}")
    print('='*50)

def test_health_check():
    """Probar ruta de verificación de estado"""
    print_separator("VERIFICACIÓN DE ESTADO")
    
    try:
        response = requests.get(f"{BASE_URL}/api/status")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_register():
    """Probar registro de usuario"""
    print_separator("REGISTRO DE USUARIO")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=TEST_USER,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code in [201, 400]  # 400 si ya existe
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_login():
    """Probar login y obtener token"""
    print_separator("LOGIN DE USUARIO")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=TEST_USER,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            return data.get('access_token')
        else:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_chat_send(token):
    """Probar envío de mensaje a Gemini"""
    print_separator("ENVIAR MENSAJE A GEMINI")
    
    if not token:
        print("❌ No hay token disponible")
        return False
    
    try:
        test_message = {
            "content": "Hola, ¿cómo estás? Responde brevemente."
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.post(
            f"{BASE_URL}/chat/send",
            json=test_message,
            headers=headers
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_chat_history(token):
    """Probar obtención de historial de chat"""
    print_separator("OBTENER HISTORIAL DE CHAT")
    
    if not token:
        print("❌ No hay token disponible")
        return False
    
    try:
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.get(
            f"{BASE_URL}/chat/history",
            headers=headers
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_invalid_routes():
    """Probar rutas inexistentes"""
    print_separator("PRUEBA DE RUTAS INEXISTENTES")
    
    try:
        response = requests.get(f"{BASE_URL}/ruta/inexistente")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 404
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Ejecutar todas las pruebas"""
    print("🎯 PRUEBAS DE FLASK GEMINI API")
    print("Asegúrate de que la API esté ejecutándose en http://localhost:5000")
    
    # Esperar un poco para que el usuario confirme
    input("\n👆 Presiona Enter cuando la API esté ejecutándose...")
    
    results = []
    
    # Ejecutar pruebas
    results.append(("Health Check", test_health_check()))
    results.append(("Registro", test_register()))
    
    # Login y obtener token
    token = test_login()
    results.append(("Login", token is not None))
    
    # Pruebas que requieren token
    if token:
        results.append(("Chat Send", test_chat_send(token)))
        results.append(("Chat History", test_chat_history(token)))
    else:
        print("⚠️ Saltando pruebas de chat por falta de token")
    
    results.append(("Rutas Inexistentes", test_invalid_routes()))
    
    # Mostrar resumen
    print_separator("RESUMEN DE PRUEBAS")
    total_tests = len(results)
    passed_tests = sum(1 for _, result in results if result)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\n📊 Resultado: {passed_tests}/{total_tests} pruebas pasaron")
    
    if passed_tests == total_tests:
        print("🎉 ¡Todas las pruebas pasaron! La API funciona correctamente.")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa la configuración.")

if __name__ == "__main__":
    main() 