# 🤖 Flask Gemini Chat

Una aplicación web completa de chat con **Google Gemini AI**, construida con Flask y una interfaz moderna. Incluye autenticación JWT, gestión de conversaciones persistentes y una interfaz de usuario intuitiva.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![Gemini](https://img.shields.io/badge/Google_Gemini-AI-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Características Principales

- 🔐 **Autenticación completa** con JWT (registro, login, refresh tokens)
- 💬 **Chat inteligente** con Google Gemini AI (modelos 1.5-flash, 1.5-pro, 1.0-pro)
- 📱 **Interfaz moderna** y responsive con HTML5, CSS3 y JavaScript
- 🗄️ **Base de datos persistente** con SQLAlchemy (SQLite, PostgreSQL, MySQL)
- 🔒 **Seguridad robusta** con validación de datos y hasheo de contraseñas
- 📊 **Gestión de conversaciones** con historial completo
- 🎨 **UI/UX atractiva** con animaciones y feedback visual
- ⚡ **Auto-configuración** con scripts inteligentes
- 🔧 **Multi-entorno** (desarrollo, producción, testing)

## 📷 Vista Previa

### Pantalla de Autenticación
![Login](https://via.placeholder.com/800x400/667eea/ffffff?text=Pantalla+de+Login)

### Interfaz de Chat
![Chat](https://via.placeholder.com/800x400/f093fb/ffffff?text=Interfaz+de+Chat+con+Gemini)

## 🚀 Instalación Rápida

### Opción 1: Auto-instalación (Recomendado)
```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/flask-gemini-chat.git
cd flask-gemini-chat

# 2. Ejecutar instalación automática
python quick_start.py
```

### Opción 2: Instalación Manual

#### 1. **Requisitos del Sistema**
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git (opcional)

#### 2. **Clonar el Repositorio**
```bash
git clone https://github.com/tu-usuario/flask-gemini-chat.git
cd flask-gemini-chat
```

#### 3. **Crear Entorno Virtual**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 4. **Instalar Dependencias**
```bash
pip install -r requirements.txt
```

#### 5. **Configurar Variables de Entorno**
```bash
# Opción A: Script automático
python setup_env.py

# Opción B: Manual - crear archivo .env
copy .env.example .env
# Editar .env con tus valores
```

#### 6. **Obtener API Key de Google Gemini**

**Método Recomendado - Google AI Studio:**
1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Inicia sesión con tu cuenta de Google
3. Haz clic en **"Create API Key"**
4. Copia la clave y pégala en tu archivo `.env`:
   ```env
   GEMINI_API_KEY=tu_api_key_aquí
   ```

**Método Alternativo - Google Cloud Console:**
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea/selecciona un proyecto
3. Habilita la **Generative AI API**
4. Ve a **API y servicios > Credenciales**
5. Crea una **Clave de API**
6. Configúrala en tu archivo `.env`

#### 7. **Inicializar Base de Datos**
```bash
# Crear las tablas
python -c "from app_basic import Base, engine; Base.metadata.create_all(engine)"

# O usar el comando personalizado
python app_basic.py create-db
```

#### 8. **Ejecutar la Aplicación**
```bash
python app_basic.py
```

## 🎯 Uso del Programa

### 1. **Acceder a la Aplicación**
- Abre tu navegador web
- Ve a: `http://localhost:5000`
- Verás la pantalla de autenticación

### 2. **Crear una Cuenta**
- Haz clic en "Regístrate aquí"
- Completa el formulario con tu email y contraseña
- La contraseña debe tener mínimo 6 caracteres

### 3. **Iniciar Sesión**
- Usa tu email y contraseña para entrar
- El sistema te redirigirá automáticamente al chat

### 4. **Chatear con Gemini**
- Escribe tu mensaje en el área de texto
- Presiona **Enter** o haz clic en el botón de envío
- También puedes usar **Ctrl+Enter** para enviar rápidamente
- Gemini responderá automáticamente

### 5. **Funciones Adicionales**
- **🗑️ Limpiar**: Borra el historial de chat actual
- **🚪 Salir**: Cierra tu sesión de forma segura
- **Contador de caracteres**: Muestra cuántos caracteres has escrito (máx. 5000)

## 📁 Estructura del Proyecto

```
flask-gemini-chat/
├── 📱 Frontend
│   ├── templates/
│   │   └── index.html          # Interfaz principal
│   └── static/
│       ├── style.css           # Estilos modernos
│       └── app.js              # Lógica del frontend
├── 🔧 Backend
│   ├── app_basic.py            # Aplicación Flask principal
│   ├── models.py               # Modelos de base de datos
│   └── schemas.py              # Validación de datos
├── 🛠️ Configuración
│   ├── .env                    # Variables de entorno
│   ├── requirements.txt        # Dependencias Python
│   ├── setup_env.py           # Auto-configuración
│   └── quick_start.py         # Instalación automática
├── 🧪 Testing
│   ├── test_api.py            # Pruebas de API
│   └── test_models.py         # Pruebas de modelos Gemini
└── 📖 Documentación
    └── README.md              # Esta documentación
```

## 🔌 API Endpoints

### 🔐 Autenticación
| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| `POST` | `/auth/register` | Registrar nuevo usuario | ❌ |
| `POST` | `/auth/login` | Iniciar sesión | ❌ |

### 💬 Chat
| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| `POST` | `/chat/send` | Enviar mensaje a Gemini | 🔒 |
| `GET` | `/chat/history` | Obtener historial | 🔒 |

### ℹ️ Sistema
| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/status` | Estado del sistema | ❌ |
| `GET` | `/api/models` | Modelos de Gemini disponibles | ❌ |

## 🔧 Configuración Avanzada

### Variables de Entorno (.env)
```env
# === CONFIGURACIÓN BÁSICA ===
FLASK_APP=app_basic.py
FLASK_ENV=development

# === SEGURIDAD ===
SECRET_KEY=tu_clave_secreta_flask
JWT_SECRET_KEY=tu_clave_jwt

# === BASE DE DATOS ===
# SQLite (por defecto)
DATABASE_URL=sqlite:///chat.db

# PostgreSQL (producción)
# DATABASE_URL=postgresql://user:pass@localhost/dbname

# === GOOGLE GEMINI ===
GEMINI_API_KEY=tu_api_key_gemini

# === CORS (frontend) ===
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Modelos de Gemini Disponibles
El sistema automáticamente detecta y usa el mejor modelo disponible:
1. **gemini-1.5-flash** (rápido y eficiente)
2. **gemini-1.5-pro** (más potente)
3. **gemini-1.0-pro** (fallback)

## 🧪 Pruebas y Verificación

### Ejecutar Pruebas Completas
```bash
# Verificar que Flask esté funcionando
python test_api.py

# Probar modelos de Gemini
python test_models.py
```

### Verificar Estado del Sistema
```bash
# Hacer petición al endpoint de status
curl http://localhost:5000/api/status

# Ver modelos disponibles
curl http://localhost:5000/api/models
```

## 🐛 Solución de Problemas

### Problema: "Error 404 models/gemini-pro is not found"
**Solución:** Ya corregido en la versión actual. El sistema usa automáticamente los modelos más recientes de Gemini.

### Problema: Error de conexión a la base de datos
**Solución:**
```bash
# Recrear la base de datos
python -c "from app_basic import Base, engine; Base.metadata.drop_all(engine); Base.metadata.create_all(engine)"
```

### Problema: Token JWT expirado
**Solución:** El frontend maneja automáticamente la renovación de tokens. Si persiste, cierra sesión y vuelve a entrar.

### Problema: API Key de Gemini inválida
**Solución:**
1. Verifica que la API Key esté correcta en el archivo `.env`
2. Asegúrate de que no haya espacios extra
3. Verifica que la API Key esté activa en Google AI Studio

### Problema: Puerto 5000 ocupado
**Solución:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID [número_proceso] /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

## 🚀 Despliegue en Producción

### Variables de Entorno para Producción
```env
FLASK_ENV=production
SECRET_KEY=clave_super_segura_generada_aleatoriamente
JWT_SECRET_KEY=otra_clave_super_segura
DATABASE_URL=postgresql://user:pass@host:5432/production_db
```

### Usando Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app_basic:app
```

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -am 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**Tu Nombre**
- GitHub: jonathanjd7 (https://github.com/jonathanjd7)
- Email: jonathanjd7@gmail.com

## 🙏 Agradecimientos

- [Google Gemini AI](https://ai.google.dev/) por la API de inteligencia artificial
- [Flask](https://flask.palletsprojects.com/) por el framework web
- [SQLAlchemy](https://www.sqlalchemy.org/) por el ORM
- Comunidad open source por las librerías utilizadas

---

⭐ **Si este proyecto te resultó útil, ¡dale una estrella en GitHub!** ⭐ 
