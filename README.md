# 🤖 Flask Gemini Chat - Versión Avanzada

Una aplicación web completa de chat con **Google Gemini AI**, construida con Flask y una interfaz moderna. Incluye autenticación JWT, gestión de múltiples conversaciones, títulos automáticos inteligentes, modo oscuro completo y una interfaz de usuario altamente optimizada.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![Gemini](https://img.shields.io/badge/Google_Gemini-1.5_Flash-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Características Principales

### 🎯 **Funcionalidades Avanzadas**
- 🔐 **Autenticación completa** con JWT (registro, login, tokens seguros)
- 💬 **Chat inteligente** con Google Gemini AI 1.5-Flash (última generación)
- 📝 **Títulos automáticos** generados por IA para cada conversación
- 🌙 **Modo oscuro completo** con auto-detección de preferencias del sistema
- 📏 **Sidebar redimensionable** con persistencia de preferencias
- 💾 **Múltiples conversaciones** con historial completo y navegación
- ✏️ **Edición de mensajes** en tiempo real con reenvío automático
- 🎨 **Interfaz optimizada** con fuentes y espaciado mejorados

### 🔧 **Funcionalidades Técnicas**
- 🗄️ **Base de datos robusta** con SQLAlchemy (SQLite por defecto)
- 🔒 **Seguridad avanzada** con validación completa y hasheo de contraseñas
- 📱 **Diseño responsive** optimizado para móvil y desktop
- ⚡ **Performance optimizada** con carga asíncrona y UX fluida
- 🛠️ **Auto-configuración inteligente** con detección de errores
- 🎭 **Temas dinámicos** con transiciones suaves

## 🆕 Últimas Actualizaciones

### **v2.0 - Interfaz Avanzada (Enero 2025)**
- ✅ **Títulos Automáticos**: La IA genera títulos descriptivos basados en el contenido de cada conversación
- ✅ **Modo Oscuro Completo**: Implementación completa con 50+ variables CSS y auto-detección
- ✅ **Sidebar Redimensionable**: Barra lateral ajustable con persistencia en localStorage (200px-500px)
- ✅ **Múltiples Conversaciones**: Sistema completo de gestión con navegación entre chats
- ✅ **Mejoras Visuales**: Optimización de fuentes, espaciado y densidad visual
- ✅ **Correcciones Críticas**: Base de datos, tokens JWT y modelo Gemini actualizados

### **Correcciones Implementadas**
- 🔧 **Base de datos**: Configuración consistente con `flask_gemini.db`
- 🔧 **JWT Tokens**: Manejo correcto de strings en identity
- 🔧 **Modelo Gemini**: Actualizado de `gemini-pro` a `gemini-1.5-flash`
- 🔧 **Frontend**: Mensajes aparecen correctamente en tiempo real

## 📷 Vista Previa

### 🌙 Modo Oscuro con Sidebar Redimensionable
```
┌─────────────────────────────────────────────────────────────────┐
│ 🌙 Modo Oscuro Activado | Gemini Chat | 🌞 Modo Claro 🚪 Salir │
├──────────────────┬──────────────────────────────────────────────┤
│ 💬 Conversaciones│ Usuario: ¿Cómo funciona React?              │
│ ➕ Nueva          │ 🤖 Gemini: React es una biblioteca de...    │
│                  │                                              │
│ 📝 Ayuda React   │ Usuario: Dame un ejemplo práctico           │
│ 🍳 Recetas Pasta │ 🤖 Gemini: Aquí tienes un componente...    │
│ 🎵 Mejor Música  │                                              │
│ ┆ ◀ Resize       │ ┌─────────────────────────────────────────┐ │
│                  │ │ Escribe tu mensaje aquí...              │ │
│                  │ │                                    📤 │ │
│                  │ └─────────────────────────────────────────┘ │
└──────────────────┴──────────────────────────────────────────────┘
```

### ☀️ Modo Claro con Títulos Automáticos
Los títulos se generan automáticamente basados en el contenido:
- "¿Puedes ayudarme con Python?" → **"Ayuda con Python"**
- "Necesito recetas fáciles" → **"Recetas fáciles"**
- "Explícame inteligencia artificial" → **"Inteligencia Artificial: Explicación"**

## 🚀 Instalación Rápida

### Opción 1: Auto-instalación (Recomendado)
```bash
# 1. Clonar el repositorio
git clone https://github.com/jonathanjd7/flask-gemini-chat.git
cd flask-gemini-chat

# 2. Ejecutar instalación automática
python quick_start.py
```

### Opción 2: Instalación Manual

#### 1. **Configuración del Entorno**
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno (Windows)
venv\Scripts\activate

# Activar entorno (macOS/Linux)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

#### 2. **Configurar Variables de Entorno**
```bash
# Crear archivo .env
python setup_env.py
```

O crear manualmente:
```env
# .env
SECRET_KEY=tu_clave_secreta_super_segura
JWT_SECRET_KEY=otra_clave_jwt_secreta
GEMINI_API_KEY=tu_api_key_de_google_gemini
DATABASE_URL=sqlite:///flask_gemini.db
FLASK_ENV=development
```

#### 3. **Obtener API Key de Google Gemini**
1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Inicia sesión con tu cuenta de Google
3. Crea una nueva API Key
4. Cópiala en tu archivo `.env`

#### 4. **Ejecutar la Aplicación**
```bash
python run.py
```

¡Abre **http://localhost:5000** y comienza a chatear! 🚀

## 🎯 Guía de Uso Completa

### 1. **Autenticación**
- **Registro**: Email + contraseña (mín. 6 caracteres)
- **Login**: Automático redirect al chat
- **Seguridad**: Tokens JWT con refresh automático

### 2. **Gestión de Conversaciones**
- **📝 Nueva Conversación**: Botón "Nueva" en sidebar
- **🏷️ Títulos Automáticos**: Generados por IA en el primer mensaje
- **📂 Navegación**: Click en cualquier conversación para cambiar
- **🗑️ Eliminar**: Botón de papelera en cada conversación

### 3. **Interfaz Avanzada**
- **🌙 Modo Oscuro**: Toggle automático, detecta preferencias del sistema
- **📏 Sidebar Redimensionable**: Arrastra el borde derecho para ajustar (200px-500px)
- **💾 Persistencia**: Preferencias guardadas en localStorage
- **📱 Responsive**: Optimizado para móvil y desktop

### 4. **Chat Inteligente**
- **✏️ Edición**: Click en ✏️ para editar mensajes enviados
- **🔄 Reenvío**: Los mensajes editados se reenvían automáticamente
- **⌨️ Atajos**: 
  - `Enter` → Enviar mensaje
  - `Shift+Enter` → Nueva línea
- **📊 Contador**: Máximo 5000 caracteres por mensaje

### 5. **Funciones del Sistema**
- **🔄 Historial**: Todas las conversaciones se guardan automáticamente
- **⚡ Carga Rápida**: Optimizada para performance
- **🛡️ Seguridad**: Validación completa en frontend y backend

## 📁 Estructura del Proyecto Actualizada

```
flask-gemini-chat/
├── 📱 **Frontend Optimizado**
│   ├── app/
│   │   ├── templates/
│   │   │   └── index.html          # UI completa con modo oscuro
│   │   └── static/
│   │       ├── style.css           # 1000+ líneas de CSS optimizado
│   │       └── app.js              # JavaScript con funciones avanzadas
├── 🔧 **Backend Robusto**
│   ├── app/
│   │   ├── __init__.py             # Factory pattern Flask
│   │   ├── config.py               # Configuración multi-entorno
│   │   ├── models.py               # Modelos User, Conversation, Message
│   │   ├── schemas.py              # Validación con Marshmallow
│   │   ├── utils.py                # Utilidades compartidas
│   │   └── routes/
│   │       ├── auth.py             # Autenticación JWT
│   │       └── chat.py             # Chat con títulos automáticos
├── 🛠️ **Configuración y Scripts**
│   ├── run.py                      # Punto de entrada principal
│   ├── .env                        # Variables de entorno
│   ├── requirements.txt            # Dependencias actualizadas
│   ├── config_setup.py            # Auto-configuración inteligente
│   └── quick_start.py             # Instalación automática
├── 💾 **Base de Datos**
│   └── instance/
│       └── flask_gemini.db         # SQLite con esquema completo
└── 📖 **Documentación**
    └── README.md                   # Esta documentación completa
```

## 🔌 API Endpoints Completa

### 🔐 **Autenticación**
| Método | Endpoint | Descripción | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `POST` | `/auth/register` | Registrar usuario | `{email, password}` | JWT Token |
| `POST` | `/auth/login` | Iniciar sesión | `{email, password}` | JWT Token |

### 💬 **Chat y Conversaciones**
| Método | Endpoint | Descripción | Auth | Response |
|--------|----------|-------------|------|----------|
| `POST` | `/chat/send_message` | Enviar mensaje + generar título automático | 🔒 | Respuesta IA |
| `GET` | `/chat/conversations` | Listar todas las conversaciones | 🔒 | Array de conversaciones |
| `POST` | `/chat/conversations` | Crear nueva conversación | 🔒 | Nueva conversación |
| `GET` | `/chat/conversations/<id>` | Obtener conversación específica | 🔒 | Conversación + mensajes |
| `DELETE` | `/chat/conversations/<id>` | Eliminar conversación | 🔒 | Status |
| `PUT` | `/chat/messages/<id>` | Editar mensaje | 🔒 | Mensaje actualizado |

## 🎨 Funcionalidades Visuales Avanzadas

### **🌙 Sistema de Temas**
```css
/* Variables CSS dinámicas para modo claro/oscuro */
:root {
  --primary-color: #667eea;
  --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  /* +50 variables más... */
}

[data-theme="dark"] {
  --primary-color: #818cf8;
  --bg-gradient: linear-gradient(135deg, #1e293b 0%, #334155 100%);
  /* Paleta completa para modo oscuro */
}
```

### **📏 Sidebar Redimensionable**
- **Rango**: 200px - 500px
- **Persistencia**: LocalStorage
- **Responsive**: Se oculta en móvil
- **Indicador visual**: Handle azul al hover

### **🎯 Optimizaciones Visuales**
- **Fuentes optimizadas**: Reducidas para mejor densidad
- **Espaciado inteligente**: Más contenido sin perder legibilidad
- **Avatares compactos**: 36px en lugar de 40px
- **Line-height**: Optimizado a 1.4 para mejor aprovechamiento

## 🧪 Testing y Verificación

### **Scripts de Prueba Disponibles**
```bash
# Probar autenticación completa
python test_auth.py

# Probar flujo de chat con títulos automáticos
python test_chat_flow.py

# Verificar funcionalidad de títulos automáticos
python test_auto_titles.py

# Probar sidebar redimensionable
python test_resize_feature.py

# Verificar modo oscuro
python test_dark_mode.py
```

### **Verificación Manual**
1. **Títulos automáticos**: Envía un mensaje y verifica que se genere título
2. **Modo oscuro**: Toggle entre temas y verifica persistencia
3. **Sidebar**: Redimensiona y recarga página para verificar persistencia
4. **Conversaciones**: Crea múltiples chats y navega entre ellos

## 🐛 Solución de Problemas Actualizados

### **Problemas Corregidos Automáticamente**
- ✅ **Error "no such table: users"**: Configuración de BD corregida
- ✅ **JWT Subject error**: Manejo de strings implementado
- ✅ **Gemini model 404**: Actualizado a gemini-1.5-flash
- ✅ **Mensajes no aparecen**: Frontend corregido para mostrar contenido

### **Si encuentras problemas nuevos:**

#### **Base de datos corrupta**
```bash
# Recrear BD con nuevo esquema
python -c "
from app import create_app, db
app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()
    print('Base de datos recreada exitosamente')
"
```

#### **Preferencias UI corruptas**
```javascript
// En consola del navegador
localStorage.removeItem('sidebar_width');
localStorage.removeItem('theme');
location.reload();
```

#### **API Key inválida**
1. Verifica en [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Regenera la key si es necesario
3. Actualiza `.env` sin espacios extra

## 🚀 Despliegue en Producción

### **Variables para Producción**
```env
FLASK_ENV=production
SECRET_KEY=clave_ultra_segura_generada_aleatoriamente_64_chars
JWT_SECRET_KEY=otra_clave_ultra_segura_diferente_64_chars
DATABASE_URL=postgresql://user:pass@host:5432/production_db
GEMINI_API_KEY=tu_api_key_produccion
```

### **Con Docker**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "run:app"]
```

### **Con Railway/Render/Heroku**
```bash
# Procfile
web: gunicorn -w 4 -b 0.0.0.0:$PORT run:app
```

## 💡 Funcionalidades Futuras Planeadas

- [ ] 📁 **Subida de archivos** e imágenes al chat
- [ ] 🔍 **Búsqueda avanzada** en el historial
- [ ] 📊 **Estadísticas de uso** y analytics
- [ ] 🌐 **Internacionalización** (i18n) multiidioma
- [ ] 🔔 **Notificaciones push** para respuestas
- [ ] 📱 **PWA** (Progressive Web App)
- [ ] 🤖 **Múltiples modelos IA** (GPT, Claude, etc.)
- [ ] 👥 **Chat grupal** y colaborativo

## 🤝 Contribuciones

¡Las contribuciones son muy bienvenidas! Especialmente en:

### **🎯 Áreas Prioritarias**
- 🎨 **UI/UX**: Mejoras en diseño y experiencia
- 🔧 **Performance**: Optimizaciones de velocidad
- 🐛 **Bug fixes**: Corrección de errores
- 📱 **Mobile**: Mejoras en responsive
- 🧪 **Testing**: Más casos de prueba

### **📋 Proceso de Contribución**
1. Fork el proyecto
2. Crea una rama: `git checkout -b feature/nueva-caracteristica`
3. Commit: `git commit -am 'Agregar: nueva característica increíble'`
4. Push: `git push origin feature/nueva-caracteristica`
5. Abre un Pull Request con descripción detallada

## 📈 Changelog

### **v2.0.0 - Interfaz Avanzada (Enero 2025)**
- ➕ Títulos automáticos generados por IA
- ➕ Modo oscuro completo con 50+ variables CSS
- ➕ Sidebar redimensionable (200px-500px)
- ➕ Sistema de múltiples conversaciones
- ➕ Edición de mensajes en tiempo real
- ➕ Optimizaciones visuales y de performance
- 🔧 Corrección de base de datos y JWT
- 🔧 Actualización a Gemini 1.5-Flash

### **v1.0.0 - Versión Base**
- ➕ Chat básico con Gemini
- ➕ Autenticación JWT
- ➕ Interfaz web responsive

## 📝 Licencia

Este proyecto está bajo la **Licencia MIT**. Ver archivo `LICENSE` para detalles completos.

## 👨‍💻 Desarrollador

**Jonathan JD**
- 🐙 **GitHub**: [jonathanjd7](https://github.com/jonathanjd7)
- 📧 **Email**: jonathanjd7@gmail.com
- 💼 **LinkedIn**: [Jonathan JD](https://linkedin.com/in/jonathanjd)

## 🙏 Agradecimientos y Tecnologías

### **🤖 IA y APIs**
- [Google Gemini AI](https://ai.google.dev/) - Por la API de inteligencia artificial
- [Google AI Studio](https://makersuite.google.com/) - Por las herramientas de desarrollo

### **🔧 Backend**
- [Flask](https://flask.palletsprojects.com/) - Framework web minimalista
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM potente y flexible
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/) - Manejo de tokens JWT
- [Marshmallow](https://marshmallow.readthedocs.io/) - Serialización y validación

### **🎨 Frontend**
- [Vanilla JavaScript](https://developer.mozilla.org/) - Sin frameworks, máximo rendimiento
- [CSS Grid & Flexbox](https://css-tricks.com/) - Layout moderno
- [CSS Custom Properties](https://developer.mozilla.org/en-US/docs/Web/CSS/--*) - Temas dinámicos

### **🛠️ Herramientas de Desarrollo**
- [Python 3.9+](https://python.org/) - Lenguaje base
- [Git](https://git-scm.com/) - Control de versiones
- [SQLite](https://sqlite.org/) - Base de datos embebida

---

## ⭐ ¿Te Gustó el Proyecto?

Si **Flask Gemini Chat** te resultó útil o interesante:

1. 🌟 **Dale una estrella** en GitHub
2. 🍴 **Fork** el proyecto para tus propias modificaciones
3. 📢 **Comparte** con otros desarrolladores
4. 🐛 **Reporta bugs** o sugiere mejoras
5. 🤝 **Contribuye** con código o documentación

### **📊 Estadísticas del Proyecto**
- 📝 **Líneas de código**: ~3,000+
- 🎨 **Líneas de CSS**: ~1,000+
- ⚡ **Funcionalidades**: 15+ características principales
- 🧪 **Tests**: Cobertura completa de funcionalidades críticas

---

**🚀 ¡Empezar es súper fácil! Solo ejecuta `python quick_start.py` y comienza a chatear con IA en menos de 5 minutos!**

---

*Última actualización: Enero 2025 | Versión: 2.0.0 Advanced*
