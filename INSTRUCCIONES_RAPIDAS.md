# 🚀 Instrucciones Rápidas - Flask Gemini Chat

## ⚡ Levantar la App en 3 Pasos

### 1️⃣ **Instalar Dependencias**
```bash
pip install -r requirements.txt
```

**Si hay error con psycopg2-binary** (normal en Windows):
```bash
pip install Flask Flask-SQLAlchemy Flask-JWT-Extended Flask-Migrate Flask-CORS marshmallow Werkzeug python-dotenv google-generativeai
```

### 2️⃣ **Configurar API Key**
```bash
python config_setup.py
```
- Ve a: https://makersuite.google.com/app/apikey
- Crea una API Key gratuita
- Pégala cuando te lo pida el script

### 3️⃣ **¡Levantar la App!**
```bash
python run.py
```

**¡Listo!** Accede a: http://localhost:5000

---

## 🎯 Opción Automática (Recomendada)

Si quieres que todo se haga automáticamente:
```bash
python quick_start.py
```

---

## 🐛 Problemas Comunes

### ❌ "python no se reconoce"
- Reinstala Python desde python.org
- ✅ Marca "Add Python to PATH"

### ❌ "No module named 'flask'"
- Activa el entorno virtual: `venv\Scripts\activate` (Windows)
- Reinstala: `pip install -r requirements.txt`

### ❌ "Error de API Key"
- Verifica que empiece con `AIzaSy`
- No hay espacios en el archivo `.env`

### ❌ "Puerto 5000 ocupado"
- Cierra otras apps que usen el puerto 5000
- O cambia el puerto en `run.py`

---

## 📱 Acceso desde Móvil

1. Encuentra tu IP: `ipconfig` (Windows) o `ifconfig` (Mac/Linux)
2. En tu móvil ve a: `http://TU_IP:5000`
3. ¡Asegúrate de estar en la misma WiFi!

---

## 🔧 Comandos Útiles

```bash
# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Actualizar pip
python -m pip install --upgrade pip

# Verificar instalación
python -c "import flask; print('Flask instalado correctamente')"
```

---

**¿Necesitas ayuda?** Consulta el README.md completo o abre un issue en GitHub. 