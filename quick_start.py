#!/usr/bin/env python
"""
Script de Inicio Rápido para Flask Gemini Chat API
Automatiza todo el proceso de configuración y puesta en marcha
"""

import os
import sys
import subprocess
import platform

def run_command(command, description, check=True):
    """Ejecutar comando con manejo de errores"""
    print(f"🔄 {description}...")
    try:
        if isinstance(command, str):
            result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        else:
            result = subprocess.run(command, check=check, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {description} completado")
            return True
        else:
            print(f"❌ Error en {description}: {result.stderr}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando: {command}")
        print(f"   Error: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ Comando no encontrado: {command}")
        return False

def check_python_version():
    """Verificar versión de Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    return True

def check_virtual_env():
    """Verificar si hay un entorno virtual"""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Entorno virtual detectado")
        return True
    else:
        print("⚠️  No se detectó entorno virtual")
        create_venv = input("¿Deseas crear un entorno virtual? (y/N): ").strip().lower()
        
        if create_venv == 'y':
            return create_virtual_environment()
        else:
            print("⚠️  Continuando sin entorno virtual (no recomendado)")
            return True

def create_virtual_environment():
    """Crear entorno virtual"""
    venv_name = "venv"
    
    if os.path.exists(venv_name):
        print(f"✅ Entorno virtual '{venv_name}' ya existe")
        return True
    
    print(f"🔄 Creando entorno virtual '{venv_name}'...")
    
    if run_command([sys.executable, "-m", "venv", venv_name], "Crear entorno virtual"):
        print(f"✅ Entorno virtual '{venv_name}' creado")
        print("\n🔄 Para activar el entorno virtual:")
        
        if platform.system() == "Windows":
            print(f"   {venv_name}\\Scripts\\activate")
        else:
            print(f"   source {venv_name}/bin/activate")
        
        print("\n⚠️  Activa el entorno virtual y ejecuta este script nuevamente")
        return False
    else:
        return False

def install_dependencies():
    """Instalar dependencias con manejo de errores mejorado"""
    if not os.path.exists("requirements.txt"):
        print("❌ Archivo requirements.txt no encontrado")
        return False
    
    print("🔄 Intentando instalar dependencias...")
    
    # Primero intentar con requirements.txt completo
    if run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                  "Instalar dependencias completas", check=False):
        return True
    
    print("⚠️  Error con requirements.txt completo, intentando instalación manual...")
    
    # Si falla, instalar dependencias esenciales manualmente
    essential_packages = [
        "Flask==2.3.3",
        "Flask-SQLAlchemy==3.0.5", 
        "Flask-JWT-Extended==4.5.3",
        "Flask-Migrate==4.0.5",
        "Flask-CORS==4.0.0",
        "marshmallow==3.20.1",
        "Werkzeug==2.3.7",
        "python-dotenv==1.0.0",
        "google-generativeai==0.3.0"
    ]
    
    print("📦 Instalando dependencias esenciales...")
    for package in essential_packages:
        if not run_command([sys.executable, "-m", "pip", "install", package], 
                          f"Instalar {package}", check=False):
            print(f"⚠️  Error instalando {package}, continuando...")
    
    print("✅ Instalación de dependencias completada")
    return True

def setup_environment():
    """Configurar variables de entorno"""
    if os.path.exists(".env"):
        overwrite = input("El archivo .env ya existe. ¿Deseas reconfigurarlo? (y/N): ").strip().lower()
        if overwrite != 'y':
            print("✅ Usando configuración .env existente")
            return True
    
    print("🔧 Configurando variables de entorno...")
    return run_command([sys.executable, "config_setup.py"], "Configurar variables de entorno")

def setup_database():
    """Configurar base de datos"""
    print("🗄️  Configurando base de datos...")
    
    # Intentar crear la base de datos directamente
    db_command = [
        sys.executable, "-c", 
        "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('✅ Base de datos creada exitosamente!')"
    ]
    
    if run_command(db_command, "Crear base de datos", check=False):
        return True
    
    print("⚠️  Error creando base de datos, intentando con Flask CLI...")
    
    # Si falla, intentar con Flask CLI
    commands = [
        ("flask db init", "Inicializar migraciones"),
        ("flask db migrate -m 'Initial migration'", "Crear migración inicial"),
        ("flask db upgrade", "Aplicar migraciones")
    ]
    
    for command, description in commands:
        if not run_command(command, description, check=False):
            # Si flask db init falla, puede ser que ya esté inicializado
            if "init" in command:
                print("ℹ️  Migraciones ya inicializadas, continuando...")
            else:
                print(f"⚠️  Error en {description}, continuando...")
    
    return True

def start_application():
    """Iniciar la aplicación"""
    print("\n🚀 ¡Configuración completada!")
    print("=" * 50)
    
    start_now = input("¿Deseas iniciar la aplicación ahora? (Y/n): ").strip().lower()
    
    if start_now != 'n':
        print("\n🌟 Iniciando Flask Gemini Chat API...")
        print("   Accede a: http://localhost:5000")
        print("   Presiona Ctrl+C para detener")
        print("=" * 50)
        
        try:
            subprocess.run([sys.executable, "run.py"], check=True)
        except KeyboardInterrupt:
            print("\n👋 Aplicación detenida")
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Error al iniciar aplicación: {e}")
            print("\n💡 Intenta ejecutar manualmente:")
            print("   python run.py")

def show_troubleshooting():
    """Mostrar guía de solución de problemas"""
    print("\n🔧 GUÍA DE SOLUCIÓN DE PROBLEMAS")
    print("=" * 50)
    print("Si encuentras errores:")
    print()
    print("1. **Error de psycopg2-binary**:")
    print("   - Es normal, ya está solucionado en requirements.txt")
    print("   - SQLite es suficiente para desarrollo")
    print()
    print("2. **Error de módulos no encontrados**:")
    print("   - Asegúrate de tener el entorno virtual activado")
    print("   - Ejecuta: pip install -r requirements.txt")
    print()
    print("3. **Error de API Key**:")
    print("   - Obtén tu clave en: https://makersuite.google.com/app/apikey")
    print("   - Configura el archivo .env correctamente")
    print()
    print("4. **Puerto 5000 ocupado**:")
    print("   - Cierra otras aplicaciones que usen el puerto 5000")
    print("   - O cambia el puerto en run.py")
    print()
    print("📖 Para más ayuda, consulta el README.md")

def main():
    """Función principal"""
    print("🎯 Flask Gemini Chat API - Inicio Rápido")
    print("=" * 50)
    print("Este script automatizará toda la configuración inicial")
    print()
    
    # Verificar prerrequisitos
    if not check_python_version():
        show_troubleshooting()
        return
    
    if not check_virtual_env():
        show_troubleshooting()
        return
    
    # Proceso de configuración
    steps = [
        (install_dependencies, "Instalar dependencias"),
        (setup_environment, "Configurar variables de entorno"),
        (setup_database, "Configurar base de datos")
    ]
    
    for step_func, step_name in steps:
        print(f"\n📋 Paso: {step_name}")
        print("-" * 30)
        
        if not step_func():
            print(f"\n❌ Error en: {step_name}")
            print("   Revisa los errores anteriores y intenta nuevamente")
            show_troubleshooting()
            return
    
    # Iniciar aplicación
    start_application()

if __name__ == "__main__":
    main() 