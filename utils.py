# utils.py
import pandas as pd
import duckdb
import os
from pathlib import Path
import hashlib
from datetime import datetime, timezone
from contextlib import contextmanager

DATA_DIR = "data"

# Mapeo de columnas para el proyecto LSCh
COLUMNS_MAP = {
    "users": [
        'username', 'password', 'email', 'role', 'active',
        'created_at', 'last_login'
    ],
    "sessions": [
        'token', 'username', 'created_at', 'expires_at',
        'is_active', 'last_activity', 'ip_address'
    ]
}

def ensure_data_dir():
    """Asegura que el directorio de datos exista."""
    Path(DATA_DIR).mkdir(exist_ok=True)

class DuckDBManager:
    """Gestor centralizado para operaciones con DuckDB"""
    
    def __init__(self, db_path=None):
        """
        Inicializa el gestor de DuckDB
        db_path: Ruta a la base de datos. Si es None, usa memoria
        """
        self.db_path = db_path or ':memory:'
        self.data_dir = DATA_DIR
        ensure_data_dir()
    
    @contextmanager
    def get_connection(self):
        """Context manager para manejar conexiones de forma segura"""
        conn = duckdb.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()
    
    def setup_views(self, conn):
        """Configura vistas para los archivos Parquet"""
        for table_name in COLUMNS_MAP.keys():
            parquet_path = Path(self.data_dir) / f"{table_name}.parquet"
            if parquet_path.exists():
                # Crear vista directamente sobre el archivo Parquet
                conn.execute(f"""
                    CREATE OR REPLACE VIEW {table_name} AS 
                    SELECT * FROM read_parquet('{parquet_path}')
                """)
    
    def query(self, sql_query, params=None):
        """Ejecuta una consulta SQL y retorna el resultado como DataFrame"""
        with self.get_connection() as conn:
            self.setup_views(conn)
            if params:
                result = conn.execute(sql_query, params).df()
            else:
                result = conn.execute(sql_query).df()
            return result
    
    def execute(self, sql_query, params=None):
        """Ejecuta una consulta SQL sin retornar resultados (INSERT, UPDATE, etc.)"""
        with self.get_connection() as conn:
            self.setup_views(conn)
            if params:
                conn.execute(sql_query, params)
            else:
                conn.execute(sql_query)

# Instancia global del gestor DuckDB
db_manager = DuckDBManager()

def query(sql_query, params=None):
    """Ejecuta una consulta SQL usando el gestor DuckDB global."""
    return db_manager.query(sql_query, params)

def load_data(data_name):
    """
    Carga datos usando DuckDB para mejor rendimiento
    """
    ensure_data_dir()
    file_path = Path(DATA_DIR) / f"{data_name}.parquet"
    expected_columns = COLUMNS_MAP.get(data_name, [])
    
    if not file_path.exists():
        # Crear DataFrame vacío con el esquema correcto
        empty_df = pd.DataFrame(columns=expected_columns)
        if data_name == "users":
            empty_df = empty_df.astype({
                'active': 'boolean',
                'created_at': 'datetime64[ns]',
                'last_login': 'datetime64[ns]'
            })
        elif data_name == "sessions":
            datetime_cols = ['created_at', 'expires_at', 'last_activity']
            astype_dict = {dt_col: 'datetime64[ns]' for dt_col in datetime_cols if dt_col in expected_columns}
            if 'is_active' in expected_columns:
                astype_dict['is_active'] = 'boolean'
            if astype_dict:
                empty_df = empty_df.astype(astype_dict)
        return empty_df
    
    try:
        # Usar DuckDB para leer el archivo Parquet
        df = db_manager.query(f"SELECT * FROM read_parquet('{file_path}')")
        
        # Asegurar todas las columnas esperadas
        for col in expected_columns:
            if col not in df.columns:
                if 'time' in col or 'date' in col or col in ['created_at', 'expires_at', 'last_login', 'last_activity']:
                    df[col] = pd.NaT
                elif col in ['active', 'is_active']:
                    df[col] = pd.NA
                else:
                    df[col] = None
        
        df = df[expected_columns]  # Reordenar columnas
        
        # Conversión de tipos
        if data_name == "users":
            if 'active' in df.columns: 
                df['active'] = df['active'].astype('boolean')
            if 'created_at' in df.columns: 
                df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
            if 'last_login' in df.columns: 
                df['last_login'] = pd.to_datetime(df['last_login'], errors='coerce')
        elif data_name == "sessions":
            if 'created_at' in df.columns: 
                df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
            if 'expires_at' in df.columns: 
                df['expires_at'] = pd.to_datetime(df['created_at'], errors='coerce')
            if 'is_active' in df.columns: 
                df['is_active'] = df['is_active'].astype('boolean')
            if 'last_activity' in df.columns: 
                df['last_activity'] = pd.to_datetime(df['last_activity'], errors='coerce')
            
        return df
        
    except Exception as e:
        print(f"Error al cargar {file_path}: {e}")
        return pd.DataFrame(columns=expected_columns)

def save_data(data_name, df):
    """Guarda datos - sigue usando Pandas para mantener compatibilidad"""
    ensure_data_dir()
    file_path = Path(DATA_DIR) / f"{data_name}.parquet"
    
    try:
        expected_columns = COLUMNS_MAP.get(data_name)
        df_to_save = df.copy()
        
        if expected_columns:
            for col in expected_columns:
                if col not in df_to_save.columns:
                    if 'time' in col or 'date' in col or col in ['created_at', 'expires_at', 'last_login', 'last_activity']:
                        df_to_save[col] = pd.NaT
                    elif col in ['active', 'is_active']:
                        df_to_save[col] = pd.NA
                    else:
                        df_to_save[col] = None
            df_to_save = df_to_save[expected_columns]
        
        # Convertir datetimes con timezone a UTC naive
        for col_name in df_to_save.select_dtypes(include=['datetimetz']).columns:
            df_to_save[col_name] = df_to_save[col_name].dt.tz_convert('UTC').dt.tz_localize(None)
        
        # Asegurar tipos correctos
        if data_name == "users" and 'active' in df_to_save.columns:
            df_to_save['active'] = df_to_save['active'].astype('boolean')
        if data_name == "sessions" and 'is_active' in df_to_save.columns:
            df_to_save['is_active'] = df_to_save['is_active'].astype('boolean')
        
        df_to_save.to_parquet(file_path, index=False)
        
    except Exception as e:
        print(f"Error al guardar {file_path}: {e}")

# Funciones de consulta SQL adicionales usando DuckDB

def get_active_users_count():
    """Obtiene el conteo de usuarios activos usando SQL"""
    query = """
    SELECT COUNT(*) as count 
    FROM users 
    WHERE active = true
    """
    result = db_manager.query(query)
    return result['count'].iloc[0] if not result.empty else 0

def get_user_by_username(username):
    """Obtiene un usuario por username usando SQL"""
    query = """
    SELECT * FROM users 
    WHERE username = ?
    """
    result = db_manager.query(query, [username])
    return result.iloc[0] if not result.empty else None

def get_recent_sessions(hours=24):
    """Obtiene sesiones recientes usando SQL"""
    query = f"""
    SELECT s.*, u.email, u.role
    FROM sessions s
    JOIN users u ON s.username = u.username
    WHERE CAST(s.created_at AS TIMESTAMP WITH TIME ZONE) >= CURRENT_TIMESTAMP - INTERVAL '{hours} hours'
    ORDER BY s.created_at DESC
    """
    return db_manager.query(query)

def get_user_statistics():
    """Obtiene estadísticas de usuarios usando SQL"""
    query = """
    SELECT 
        COUNT(*) as total_users,
        COUNT(CASE WHEN active = true THEN 1 END) as active_users,
        COUNT(CASE WHEN role = 'admin' THEN 1 END) as admin_users,
        COUNT(CASE WHEN role = 'user' THEN 1 END) as regular_users,
        COUNT(CASE WHEN last_login IS NOT NULL THEN 1 END) as users_logged_in
    FROM users
    """
    return db_manager.query(query).iloc[0]

def get_daily_registrations(days=30):
    """Obtiene registros diarios de los últimos N días"""
    query = f"""
    SELECT 
        DATE(created_at) as date,
        COUNT(*) as registrations
    FROM users
    WHERE CAST(created_at AS TIMESTAMP WITH TIME ZONE) >= CURRENT_TIMESTAMP - INTERVAL '{days} days'
    GROUP BY DATE(created_at)
    ORDER BY date
    """
    return db_manager.query(query)

def search_users(search_term):
    """Busca usuarios por username o email"""
    query = """
    SELECT username, email, role, active, created_at
    FROM users
    WHERE username ILIKE ? OR email ILIKE ?
    ORDER BY created_at DESC
    """
    search_pattern = f"%{search_term}%"
    return db_manager.query(query, [search_pattern, search_pattern])

def get_session_analytics():
    """Obtiene análisis de sesiones"""
    query = """
    WITH session_stats AS (
        SELECT 
            username,
            COUNT(*) as total_sessions,
            COUNT(CASE WHEN is_active = true THEN 1 END) as active_sessions,
            MAX(created_at) as last_session
        FROM sessions
        GROUP BY username
    )
    SELECT 
        u.username,
        u.email,
        u.role,
        COALESCE(s.total_sessions, 0) as total_sessions,
        COALESCE(s.active_sessions, 0) as active_sessions,
        s.last_session
    FROM users u
    LEFT JOIN session_stats s ON u.username = s.username
    ORDER BY s.total_sessions DESC NULLS LAST
    """
    return db_manager.query(query)

# Mantener funciones originales para compatibilidad
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def initialize_data():
    """Inicializa los archivos de datos si no existen y crea un usuario admin por defecto."""
    ensure_data_dir()
    print("LSCh Auth: Ejecutando initialize_data...")
    
    # Crear archivos parquet vacíos si no existen
    for data_name in COLUMNS_MAP.keys():
        file_path = Path(DATA_DIR) / f"{data_name}.parquet"
        if not file_path.exists():
            print(f"LSCh Auth: Creando archivo {data_name}.parquet inicial...")
            df_empty = load_data(data_name)
            save_data(data_name, df_empty)
    
    print("LSCh Auth: Verificando usuario admin...")
    
    # Verificar si existe admin usando SQL
    try:
        admin_exists = db_manager.query("SELECT COUNT(*) as count FROM users WHERE username = 'admin'")
        admin_count = admin_exists['count'].iloc[0] if not admin_exists.empty else 0
    except:
        # Si falla la consulta SQL, usar método tradicional
        df_users = load_data("users")
        admin_count = 1 if 'admin' in df_users['username'].values else 0
    
    if admin_count == 0:
        print("LSCh Auth: Admin no encontrado, añadiendo admin...")
        df_users = load_data("users")
        
        admin_data = {
            'username': 'admin',
            'password': hash_password("admin123"),  # Cambiar en producción
            'email': 'admin@lsch.cl',
            'role': 'admin',
            'active': True,
            'created_at': datetime.now(timezone.utc).replace(tzinfo=None),
            'last_login': pd.NaT
        }
        
        admin_df = pd.DataFrame([admin_data], columns=COLUMNS_MAP["users"])
        df_users = pd.concat([df_users, admin_df], ignore_index=True)
        save_data("users", df_users)
        print("LSCh Auth: Usuario admin creado.")
    else:
        print("LSCh Auth: Usuario admin ya existe.")
    
    print("LSCh Auth: initialize_data completado.")