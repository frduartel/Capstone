# auth_forms.py
import streamlit as st
from auth import authenticate_user # Usará el auth.py del LSCh
from utils import load_data, save_data, hash_password, COLUMNS_MAP # Usará el utils.py del LSCh
import pandas as pd
import re
from datetime import datetime, timezone # Import timezone

def login_form():
    """Muestra el formulario de inicio de sesión."""
    with st.form("login_form_lsch"):
        st.subheader("👤 Iniciar Sesión")
        username_login = st.text_input("Nombre de Usuario", key="login_username_lsch")
        password_login = st.text_input("Contraseña", type="password", key="login_password_lsch")
        submitted_login = st.form_submit_button("Entrar")

        if submitted_login:
            if not username_login or not password_login:
                st.error("Por favor, ingresa el nombre de usuario y la contraseña.")
            elif authenticate_user(username_login, password_login):
                st.success(f"¡Bienvenido {username_login}!")
                st.session_state.authenticated = True # Asegurar que se establece
                st.session_state.current_user = username_login # Guardar usuario actual
                # El rol se establece dentro de authenticate_user -> create_session
                st.rerun() # Forzar un rerun para que la app principal muestre contenido autenticado
            else:
                # El mensaje de error ya se muestra en authenticate_user
                pass

def register_form():
    """Muestra el formulario de registro."""
    with st.form("register_form_lsch"):
        st.subheader("✍️ Registrarse")
        email_register = st.text_input("Correo Electrónico", key="register_email_lsch")
        username_register = st.text_input("Nombre de Usuario (mín. 4 caracteres)", key="register_username_lsch")
        password_register = st.text_input("Contraseña (mín. 8 caracteres)", type="password", key="register_password_lsch")
        confirm_password_register = st.text_input("Confirmar Contraseña", type="password", key="register_confirm_password_lsch")
        
        # Solo mostrar selector de rol si el usuario actual es admin
        if st.session_state.get('authenticated', False) and st.session_state.get('user_role') == 'admin':
            role_register = st.selectbox("Rol", ['user', 'admin'], key="register_role_lsch")
        else:
            role_register = 'user'  # Valor por defecto para usuarios no admin
        
        submitted_register = st.form_submit_button("Registrarme")

        if submitted_register:
            errors = []
            
            # Validaciones básicas
            if not username_register or len(username_register) < 4:
                errors.append("El nombre de usuario debe tener al menos 4 caracteres.")
            if not email_register or not re.match(r"[^@]+@[^@]+\.[^@]+", email_register):
                errors.append("Por favor, ingresa un correo electrónico válido.")
            if not password_register or len(password_register) < 8:
                errors.append("La contraseña debe tener al menos 8 caracteres.")
            if password_register != confirm_password_register:
                errors.append("Las contraseñas no coinciden.")

            # Mostrar errores si existen
            if errors:
                for error in errors:
                    st.error(error)
            else:
                users_df = load_data("users")
                
                # Verificar si el usuario ya existe
                if username_register in users_df['username'].values:
                    st.error("Este nombre de usuario ya existe. Por favor, elige otro.")
                elif email_register in users_df['email'].values:
                    st.error("Este correo electrónico ya está registrado. ¿Quizás quieres iniciar sesión?")
                else:
                    try:
                        # Preparar datos del nuevo usuario
                        new_user_data = {col: None for col in COLUMNS_MAP["users"]}
                        new_user_data.update({
                            'username': username_register,
                            'password': hash_password(password_register),
                            'email': email_register,
                            'role': role_register,  # Usar el rol seleccionado
                            'active': True,         # Activar por defecto
                            'created_at': datetime.now(timezone.utc).replace(tzinfo=None), # Naive UTC
                            'last_login': pd.NaT
                        })
                        
                        # Asegurar que todas las columnas requeridas estén presentes
                        for col in COLUMNS_MAP["users"]:
                            if col not in new_user_data:
                                if 'time' in col or 'date' in col or col in ['created_at', 'last_login']:
                                    new_user_data[col] = pd.NaT
                                else:
                                    new_user_data[col] = None
                        
                        # Crear DataFrame con el nuevo usuario
                        new_user_entry = pd.DataFrame([new_user_data], columns=COLUMNS_MAP["users"])
                        
                        # Asegurar tipos de datos correctos si es el primer usuario
                        if users_df.empty:
                            users_df = users_df.astype(new_user_entry.dtypes)

                        # Combinar con usuarios existentes y guardar
                        updated_users_df = pd.concat([users_df, new_user_entry], ignore_index=True)
                        save_data("users", updated_users_df)
                        
                        # Mensaje de éxito diferente para admin
                        if st.session_state.get('user_role') == 'admin':
                            st.success(f"¡Usuario {username_register} registrado exitosamente con rol {role_register}!")
                        else:
                            st.success("¡Registro exitoso! Ahora puedes iniciar sesión.")
                        
                        # Limpiar campos del formulario después de registro exitoso
                        if st.session_state.get('user_role') != 'admin':
                            st.session_state.register_username_lsch = ""
                            st.session_state.register_email_lsch = ""
                            st.session_state.register_password_lsch = ""
                            st.session_state.register_confirm_password_lsch = ""
                        
                    except Exception as e:
                        st.error(f"Ocurrió un error durante el registro: {str(e)}")

def admin_create_user_form():
    """Formulario especial para que los administradores creen nuevos usuarios."""
    if not st.session_state.get('authenticated', False) or st.session_state.get('user_role') != 'admin':
        st.error("Acceso restringido a administradores")
        return
    
    with st.expander("🔧 Crear Nuevo Usuario (Admin)", expanded=True):
        with st.form("admin_create_user_form"):
            st.subheader("Crear Nuevo Usuario")
            
            col1, col2 = st.columns(2)
            with col1:
                new_username = st.text_input("Nombre de Usuario*", key="admin_new_username")
                new_email = st.text_input("Correo Electrónico*", key="admin_new_email")
            with col2:
                new_role = st.selectbox("Rol*", ['admin', 'user'], key="admin_new_role")
                new_status = st.checkbox("Activo", value=True, key="admin_new_status")
            
            new_password = st.text_input("Contraseña Temporal*", type="password", key="admin_new_password")
            
            submitted = st.form_submit_button("Crear Usuario")
            
            if submitted:
                errors = []
                if not new_username or len(new_username) < 4:
                    errors.append("El nombre de usuario debe tener al menos 4 caracteres.")
                if not new_email or not re.match(r"[^@]+@[^@]+\.[^@]+", new_email):
                    errors.append("Por favor, ingresa un correo electrónico válido.")
                if not new_password or len(new_password) < 8:
                    errors.append("La contraseña temporal debe tener al menos 8 caracteres.")
                
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    users_df = load_data("users")
                    
                    if new_username in users_df['username'].values:
                        st.error("Este nombre de usuario ya existe.")
                    elif new_email in users_df['email'].values:
                        st.error("Este correo electrónico ya está registrado.")
                    else:
                        try:
                            new_user_data = {
                                'username': new_username,
                                'password': hash_password(new_password),
                                'email': new_email,
                                'role': new_role,
                                'active': new_status,
                                'created_at': datetime.now(timezone.utc).replace(tzinfo=None),
                                'last_login': pd.NaT
                            }
                            
                            # Asegurar todas las columnas requeridas
                            for col in COLUMNS_MAP["users"]:
                                if col not in new_user_data:
                                    if 'time' in col or 'date' in col:
                                        new_user_data[col] = pd.NaT
                                    else:
                                        new_user_data[col] = None
                            
                            new_user_entry = pd.DataFrame([new_user_data], columns=COLUMNS_MAP["users"])
                            updated_users_df = pd.concat([users_df, new_user_entry], ignore_index=True)
                            save_data("users", updated_users_df)
                            
                            st.success(f"Usuario {new_username} creado exitosamente con rol {new_role}.")
                            st.info(f"Contraseña temporal: {new_password} (debe ser cambiada en el primer inicio de sesión)")
                            
                            # Limpiar el formulario
                            st.session_state.admin_new_username = ""
                            st.session_state.admin_new_email = ""
                            st.session_state.admin_new_password = ""
                            
                        except Exception as e:
                            st.error(f"Error al crear usuario: {str(e)}")