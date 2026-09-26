# auth.py
import streamlit as st
from token_manager import TokenManager # Usará el token_manager.py del LSCh
from utils import load_data, hash_password # Usará el utils.py del LSCh
from datetime import datetime, timedelta, timezone # Import timezone

# Crear una instancia del gestor de tokens
session_manager = TokenManager()

def authenticate_user(username, password):
    """Autentica un usuario verificando credenciales."""
    users_df = load_data("users")
    
    # Asegurarse que 'username' y 'active' existan para evitar KeyErrors
    if 'username' not in users_df.columns or 'active' not in users_df.columns:
        st.error("Error de configuración: Faltan columnas esenciales en el archivo de usuarios.")
        return False
        
    user_query = users_df[(users_df['username'] == username) & (users_df['active'] == True)]

    # Manejo de intentos de login (simplificado)
    if 'login_attempts' not in st.session_state:
        st.session_state.login_attempts = {}
    
    attempts = st.session_state.login_attempts.get(username, 0)
    if attempts >= 5: # Límite de intentos
        # Podrías añadir un bloqueo temporal aquí si lo deseas
        st.error("Demasiados intentos fallidos. Por favor, inténtalo más tarde.")
        return False
    
    if not user_query.empty and user_query.iloc[0]['password'] == hash_password(password):
        st.session_state.login_attempts[username] = 0 # Resetear intentos
        session_manager.create_session(username) # Crear sesión a través del manager
        st.session_state.authenticated = True # Confirmar estado
        # st.rerun() # No es necesario aquí, se maneja en el formulario
        return True
    else:
        st.session_state.login_attempts[username] = attempts + 1
        st.error("Nombre de usuario o contraseña incorrectos.")
        return False

def logout_user():
    """Cierra la sesión actual del usuario."""
    session_manager.destroy_session() # Destruir sesión a través del manager
    # Limpiar explícitamente el estado de la sesión de Streamlit relacionado con la app
    keys_to_pop = ['authenticated', 'current_user', 'user_role', 'session_token', 'camera_is_active', 'accumulated_phrase_words', 'last_added_sign_info']
    for key in keys_to_pop:
        st.session_state.pop(key, None)
    st.query_params.clear() # Limpiar parámetros de URL también
    st.rerun()

# Añadir esta función para verificar roles
def require_admin():
    """Verifica si el usuario es administrador, si no, muestra error y detiene ejecución."""
    if not st.session_state.get('authenticated', False):
        check_authentication()
    
    if st.session_state.get('user_role') != 'admin':
        st.error("⛔ Acceso restringido. Necesitas privilegios de administrador.")
        st.stop()

def check_authentication(required_role=None, target_page_on_fail="app_palabras.py"):
    """
    Verifica si el usuario está autenticado. Si no, redirige a la página principal.
    Si se requiere un rol, también lo verifica.
    """
    if not session_manager.validate_session(): # Usa el manager para validar
        st.error("🔒 Debes iniciar sesión para acceder a esta página.")
        if st.button("Ir a Inicio de Sesión"):
             st.switch_page(target_page_on_fail) # Redirigir a la página de login/principal
        st.stop() # Detener la ejecución de la página actual

    # Verificación de rol si es necesario (simplificado para el LSCh, puede que no necesites roles complejos al inicio)
    if required_role:
        user_current_role = st.session_state.get('user_role', 'user') # Obtener rol actual
        if user_current_role != required_role:
            st.error(f"⛔ Acceso restringido. Necesitas rol de '{required_role}' para esta funcionalidad.")
            # Opcional: botón para volver o redirigir
            if st.button("Volver al inicio"):
                st.switch_page(target_page_on_fail)
            st.stop()
    return True # Usuario autenticado (y con rol si se especificó)