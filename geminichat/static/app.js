// ===== CONFIGURACIÓN Y VARIABLES GLOBALES =====
const API_BASE_URL = '';
let currentToken = null;
let currentUser = null;

// ===== ELEMENTOS DEL DOM =====
const authPanel = document.getElementById('auth-panel');
const chatPanel = document.getElementById('chat-panel');
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const authMessage = document.getElementById('auth-message');
const chatMessages = document.getElementById('chat-messages');
const typingIndicator = document.getElementById('typing-indicator');
const messageInput = document.getElementById('message-input');
const sendBtn = document.getElementById('send-btn');
const charCount = document.querySelector('.char-count');
const userEmailSpan = document.getElementById('user-email');

// ===== INICIALIZACIÓN =====
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    checkAuthStatus();
});

function initializeApp() {
    // Cargar token desde localStorage
    currentToken = localStorage.getItem('gemini_chat_token');
    currentUser = JSON.parse(localStorage.getItem('gemini_chat_user') || 'null');
    
    // Auto-resize del textarea
    setupTextareaAutoResize();
}

function setupEventListeners() {
    // Formularios de autenticación
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
    document.getElementById('registerForm').addEventListener('submit', handleRegister);
    
    // Chat
    document.getElementById('chat-form').addEventListener('submit', handleSendMessage);
    messageInput.addEventListener('input', updateCharCount);
    messageInput.addEventListener('keydown', handleKeyDown);
    
    // Botones
    document.getElementById('logout-btn').addEventListener('click', handleLogout);
    document.getElementById('clear-chat').addEventListener('click', handleClearChat);
}

// ===== FUNCIONES DE AUTENTICACIÓN =====
async function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    const button = e.target.querySelector('button[type="submit"]');
    
    setButtonLoading(button, true);
    clearMessage();
    
    try {
        const response = await fetch('/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Login exitoso
            currentToken = data.access_token;
            currentUser = { id: data.user_id, email: email };
            
            // Guardar en localStorage
            localStorage.setItem('gemini_chat_token', currentToken);
            localStorage.setItem('gemini_chat_user', JSON.stringify(currentUser));
            
            showMessage('¡Login exitoso! Bienvenido al chat.', 'success');
            setTimeout(() => showChatPanel(), 1000);
        } else {
            showMessage(data.error || 'Error al iniciar sesión', 'error');
        }
    } catch (error) {
        showMessage('Error de conexión. Verifica que la API esté funcionando.', 'error');
        console.error('Login error:', error);
    } finally {
        setButtonLoading(button, false);
    }
}

async function handleRegister(e) {
    e.preventDefault();
    
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const button = e.target.querySelector('button[type="submit"]');
    
    setButtonLoading(button, true);
    clearMessage();
    
    try {
        const response = await fetch('/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showMessage('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success');
            setTimeout(() => showLogin(), 2000);
            
            // Pre-llenar el formulario de login
            document.getElementById('loginEmail').value = email;
        } else {
            showMessage(data.error || 'Error al registrar usuario', 'error');
        }
    } catch (error) {
        showMessage('Error de conexión. Verifica que la API esté funcionando.', 'error');
        console.error('Register error:', error);
    } finally {
        setButtonLoading(button, false);
    }
}

function handleLogout() {
    currentToken = null;
    currentUser = null;
    localStorage.removeItem('gemini_chat_token');
    localStorage.removeItem('gemini_chat_user');
    
    showAuthPanel();
    clearChatMessages();
    showMessage('Sesión cerrada correctamente', 'success');
}

// ===== FUNCIONES DE CHAT =====
async function sendMessage(messageText) {
    if (!currentToken) {
        showMessage('Sesión expirada. Por favor, inicia sesión nuevamente.', 'error');
        handleLogout();
        return;
    }
    
    try {
        const response = await fetch('/chat/send', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${currentToken}`
            },
            body: JSON.stringify({ content: messageText })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            return {
                success: true,
                userMessage: data.user_message,
                aiResponse: data.gemini_response,
                timestamp: data.timestamp
            };
        } else {
            if (response.status === 401 || response.status === 422) {
                showMessage('Sesión expirada. Por favor, inicia sesión nuevamente.', 'error');
                setTimeout(() => handleLogout(), 2000);
            }
            return {
                success: false,
                error: data.error || 'Error al enviar mensaje'
            };
        }
    } catch (error) {
        console.error('Send message error:', error);
        return {
            success: false,
            error: 'Error de conexión'
        };
    }
}

async function handleSendMessage(e) {
    e.preventDefault();
    
    const messageText = messageInput.value.trim();
    if (!messageText) return;
    
    // Deshabilitar input y botón
    setInputDisabled(true);
    
    // Mostrar mensaje del usuario
    addMessage(messageText, 'user');
    
    // Limpiar input
    messageInput.value = '';
    updateCharCount();
    
    // Mostrar indicador de escritura
    showTypingIndicator();
    
    // Enviar mensaje
    const result = await sendMessage(messageText);
    
    // Ocultar indicador de escritura
    hideTypingIndicator();
    
    if (result.success) {
        // Mostrar respuesta de Gemini
        addMessage(result.aiResponse, 'bot');
    } else {
        // Mostrar error
        addMessage(`Error: ${result.error}`, 'bot', true);
    }
    
    // Rehabilitar input y botón
    setInputDisabled(false);
    messageInput.focus();
}

function addMessage(content, sender, isError = false) {
    const messageContainer = document.createElement('div');
    messageContainer.className = `message-container ${sender}`;
    
    const avatar = document.createElement('div');
    avatar.className = sender === 'user' ? 'user-avatar' : 'bot-avatar';
    avatar.textContent = sender === 'user' ? '👤' : '🤖';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    if (isError) {
        messageContent.style.backgroundColor = '#fee2e2';
        messageContent.style.color = '#dc2626';
        messageContent.style.borderLeft = '4px solid #dc2626';
    }
    
    // Convertir saltos de línea a <br>
    const formattedContent = content.replace(/\n/g, '<br>');
    messageContent.innerHTML = `<p>${formattedContent}</p>`;
    
    // Timestamp
    const timestamp = document.createElement('div');
    timestamp.className = 'message-timestamp';
    timestamp.textContent = new Date().toLocaleTimeString();
    messageContent.appendChild(timestamp);
    
    messageContainer.appendChild(avatar);
    messageContainer.appendChild(messageContent);
    
    chatMessages.appendChild(messageContainer);
    scrollToBottom();
}

function showTypingIndicator() {
    typingIndicator.classList.remove('hidden');
    scrollToBottom();
}

function hideTypingIndicator() {
    typingIndicator.classList.add('hidden');
}

function scrollToBottom() {
    setTimeout(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 100);
}

function handleClearChat() {
    if (confirm('¿Estás seguro de que quieres limpiar el chat?')) {
        clearChatMessages();
    }
}

function clearChatMessages() {
    // Mantener solo el mensaje de bienvenida
    const welcomeMessage = chatMessages.querySelector('.welcome-message');
    chatMessages.innerHTML = '';
    if (welcomeMessage) {
        chatMessages.appendChild(welcomeMessage);
    }
}

// ===== FUNCIONES DE UI =====
function showLogin() {
    loginForm.classList.add('active');
    registerForm.classList.remove('active');
    clearMessage();
}

function showRegister() {
    registerForm.classList.add('active');
    loginForm.classList.remove('active');
    clearMessage();
}

function showAuthPanel() {
    authPanel.classList.remove('hidden');
    chatPanel.classList.add('hidden');
    document.body.style.overflow = 'auto';
}

function showChatPanel() {
    authPanel.classList.add('hidden');
    chatPanel.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    
    // Configurar información del usuario
    if (currentUser) {
        userEmailSpan.textContent = currentUser.email;
    }
    
    // Enfocar input
    setTimeout(() => messageInput.focus(), 100);
}

function showMessage(message, type) {
    authMessage.textContent = message;
    authMessage.className = `message ${type}`;
}

function clearMessage() {
    authMessage.className = 'message';
    authMessage.textContent = '';
}

function setButtonLoading(button, loading) {
    if (loading) {
        button.classList.add('loading');
        button.disabled = true;
    } else {
        button.classList.remove('loading');
        button.disabled = false;
    }
}

function setInputDisabled(disabled) {
    messageInput.disabled = disabled;
    sendBtn.disabled = disabled;
}

function updateCharCount() {
    const current = messageInput.value.length;
    const max = messageInput.maxLength;
    charCount.textContent = `${current}/${max}`;
    
    if (current > max * 0.9) {
        charCount.style.color = '#ef4444';
    } else {
        charCount.style.color = '#6b7280';
    }
}

function handleKeyDown(e) {
    if (e.key === 'Enter') {
        if (e.ctrlKey || e.metaKey) {
            // Ctrl+Enter o Cmd+Enter para enviar
            e.preventDefault();
            if (!sendBtn.disabled) {
                document.getElementById('chat-form').dispatchEvent(new Event('submit'));
            }
        }
        // Enter normal para nueva línea (comportamiento por defecto)
    }
}

function setupTextareaAutoResize() {
    messageInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 120) + 'px';
    });
}

function checkAuthStatus() {
    if (currentToken && currentUser) {
        // Verificar si el token sigue siendo válido
        verifyToken().then(valid => {
            if (valid) {
                showChatPanel();
            } else {
                handleLogout();
            }
        });
    } else {
        showAuthPanel();
    }
}

async function verifyToken() {
    if (!currentToken) return false;
    
    try {
        const response = await fetch('/api/status', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${currentToken}`
            }
        });
        
        return response.ok;
    } catch (error) {
        console.error('Token verification error:', error);
        return false;
    }
}

// ===== FUNCIONES GLOBALES PARA EL HTML =====
window.showLogin = showLogin;
window.showRegister = showRegister;

// ===== DEBUG (solo en desarrollo) =====
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    window.debugChat = {
        currentToken,
        currentUser,
        sendMessage,
        clearToken: () => {
            localStorage.removeItem('gemini_chat_token');
            localStorage.removeItem('gemini_chat_user');
            location.reload();
        }
    };
    console.log('🐛 Debug tools available in window.debugChat');
} 