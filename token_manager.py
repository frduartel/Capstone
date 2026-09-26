# token_manager.py
import streamlit as st
import pandas as pd
from datetime import timedelta, timezone # Import timezone
from utils import load_data, save_data, COLUMNS_MAP # Usará el utils.py del LSCh
import secrets

class TokenManager:
    def __init__(self):
        self.token_name = "lsch_auth_token" # Nombre de token específico para esta app
        self.token_expiry_hours = 24
        self.token_length = 32

    def _generate_token(self):
        return secrets.token_urlsafe(self.token_length)

    def _get_current_token_from_url(self):
        return st.query_params.get(self.token_name, None)

    def _update_url_with_token(self, token_value=None):
        current_params = dict(st.query_params)
        if token_value:
            current_params[self.token_name] = token_value
        elif self.token_name in current_params:
            del current_params[self.token_name]
        
        if current_params != dict(st.query_params):
            st.query_params.clear()
            if current_params:
                st.query_params.update(**current_params)

    def _get_client_ip_address(self):
        try:
            from streamlit.web.server.server import Server
            session_info = Server.get_current()._get_session_info()
            if session_info and hasattr(session_info, 'client') and session_info.client:
                return session_info.client.address
            if hasattr(st, 'http_headers') and st.http_headers: # Adaptado para Streamlit Cloud / versiones recientes
                x_forwarded_for = st.http_headers.get('X-Forwarded-For')
                if x_forwarded_for: return x_forwarded_for.split(',')[0].strip()
                # Headeers comunes para IP de cliente en diferentes proxies
                real_ip_headers = ['X-Real-Ip', 'True-Client-Ip', 'CF-Connecting-IP']
                for header in real_ip_headers:
                    ip = st.http_headers.get(header)
                    if ip: return ip.split(',')[0].strip()
                return st.http_headers.get('Remote-Addr', "unknown_ip") # Fallback
        except Exception:
            pass # Silenciar errores si no se puede obtener
        return "unknown_ip"

    def create_session(self, username_auth):
        token = self._generate_token()
        now_utc_naive = pd.Timestamp.now(tz=timezone.utc).tz_localize(None)

        sessions_df = load_data("sessions")
        new_session_data = {col: None for col in COLUMNS_MAP["sessions"]} # Inicializar con None
        new_session_data.update({
            'token': token,
            'username': username_auth,
            'created_at': now_utc_naive,
            'expires_at': now_utc_naive + pd.Timedelta(hours=self.token_expiry_hours),
            'is_active': True,
            'last_activity': now_utc_naive,
            'ip_address': self._get_client_ip_address()
        })
        new_session_entry = pd.DataFrame([new_session_data], columns=COLUMNS_MAP["sessions"])
        sessions_df = pd.concat([sessions_df, new_session_entry], ignore_index=True)
        save_data("sessions", sessions_df)

        users_df = load_data("users")
        if 'last_login' not in users_df.columns: users_df['last_login'] = pd.NaT
        users_df.loc[users_df['username'] == username_auth, 'last_login'] = now_utc_naive
        save_data("users", users_df)

        user_role_session = 'user' # Rol por defecto
        if not users_df[users_df['username'] == username_auth].empty:
            user_role_session = users_df[users_df['username'] == username_auth]['role'].iloc[0]

        st.session_state.update({
            'authenticated': True,
            'current_user': username_auth,
            'user_role': user_role_session,
            'session_token': token
        })
        self._update_url_with_token(token)
        return token

    def validate_session(self):
        if st.session_state.get('authenticated', False) and st.session_state.get('session_token'):
            return True

        token_from_url = self._get_current_token_from_url()
        if not token_from_url:
            self._clear_session_state_and_url_token()
            return False

        sessions_df = load_data("sessions")
        now_utc_naive_validation = pd.Timestamp.now(tz=timezone.utc).tz_localize(None)

        if 'expires_at' in sessions_df.columns:
            sessions_df['expires_at'] = pd.to_datetime(sessions_df['expires_at'], errors='coerce')
        else: # Si la columna no existe, ninguna sesión puede ser válida por token
            self._clear_session_state_and_url_token(token_in_url_is_invalid=True)
            return False

        valid_session_entry = sessions_df[
            (sessions_df['token'] == token_from_url) &
            (sessions_df['is_active'] == True) &
            (sessions_df['expires_at'] > now_utc_naive_validation)
        ]

        if not valid_session_entry.empty:
            session_data = valid_session_entry.iloc[0]
            sessions_df.loc[sessions_df['token'] == token_from_url, 'last_activity'] = now_utc_naive_validation
            save_data("sessions", sessions_df)

            users_df_val = load_data("users")
            user_data_val = users_df_val[users_df_val['username'] == session_data['username']]
            user_role_val = 'user' # Rol por defecto
            if not user_data_val.empty:
                 user_role_val = user_data_val['role'].iloc[0]

            st.session_state.update({
                'authenticated': True,
                'current_user': session_data['username'],
                'user_role': user_role_val,
                'session_token': token_from_url
            })
            return True
        else:
            self._clear_session_state_and_url_token(token_in_url_is_invalid=True)
            return False

    def _clear_session_state_and_url_token(self, token_in_url_is_invalid=False):
        st.session_state.pop('authenticated', None)
        st.session_state.pop('current_user', None)
        st.session_state.pop('user_role', None)
        st.session_state.pop('session_token', None)
        if token_in_url_is_invalid or self._get_current_token_from_url():
            self._update_url_with_token(None)

    def destroy_session(self):
        token_to_invalidate = st.session_state.get('session_token') or self._get_current_token_from_url()
        if token_to_invalidate:
            try:
                sessions_df_destroy = load_data("sessions")
                if not sessions_df_destroy.empty and 'token' in sessions_df_destroy.columns:
                    now_for_expiry = pd.Timestamp.now(tz=timezone.utc).tz_localize(None)
                    sessions_df_destroy.loc[
                        sessions_df_destroy['token'] == token_to_invalidate,
                        ['is_active', 'expires_at']
                    ] = [False, now_for_expiry]
                    save_data("sessions", sessions_df_destroy)
            except Exception as e_destroy:
                print(f"LSCh Auth: Error al invalidar token en backend: {e_destroy}")
        self._clear_session_state_and_url_token()