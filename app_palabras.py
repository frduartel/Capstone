# app_palabras.py
# (VERSIÓN MEJORADA CON SEPARACIÓN ADMIN/USUARIO Y DUCKDB)
import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import joblib
from gtts import gTTS
import io
import os
import time
import pandas as pd
from datetime import datetime, timezone
import duckdb
import plotly.express as px

# --- Módulos de Autenticación ---
import utils as auth_utils
from token_manager import TokenManager
from auth import logout_user, check_authentication
from auth_forms import login_form, register_form

# --- Instancia del Gestor de Sesiones ---
session_manager = TokenManager()

# --- Configuración Inicial de la App (Modelos LSCh) ---
MODEL_DIR = "modelos_entrenados_palabras_v1"
MODEL_FILENAME = 'modelo_palabras_svc_dos_manos.pkl'
SCALER_FILENAME = 'scaler_palabras_dos_manos.pkl'
MODEL_FULL_PATH = os.path.join(MODEL_DIR, MODEL_FILENAME)
SCALER_FULL_PATH = os.path.join(MODEL_DIR, SCALER_FILENAME)

# --- Constantes para Extracción de Landmarks ---
NUM_LANDMARKS_PER_HAND = 21
NUM_COORDS_PER_LANDMARK = 3
EXPECTED_FEATURES_PER_HAND = NUM_LANDMARKS_PER_HAND * NUM_COORDS_PER_LANDMARK
TARGET_FEATURES_LSCH = 2 * EXPECTED_FEATURES_PER_HAND

# --- Configuración para DuckDB ---
PREDICTIONS_TABLE = "predictions"
COLUMNS_MAP = {
    "predictions": ['username', 'sign', 'confidence', 'timestamp']
}

def config_page():
    """Configura la página con estilos mejorados."""
    initial_sidebar_state = "expanded" if st.session_state.get('authenticated', False) else "collapsed"
    st.set_page_config(
        page_title="SignIA",
        page_icon="🤟",
        layout="wide",
        initial_sidebar_state=initial_sidebar_state,
    )
    
    # Estilos CSS globales - TEMA OSCURO
    st.markdown("""
    <style>
        /* Estilos generales - Fondo negro */
        .stApp {
            background-color: #000000 !important;
            color: #ffffff !important;
        }
        
        /* Sidebar - Azul oscuro */
        [data-testid="stSidebar"] {
            background-color: #0a1220 !important;
            color: white !important;
        }
        
        /* Botones - Azul brillante */
        .stButton>button {
            background-color: #1e88e5 !important;
            color: white !important;
            border: none !important;
        }
        
        .stButton>button:hover {
            background-color: #1565c0 !important;
        }
        
        /* Textos generales - Blanco */
        .stMarkdown, .stText, .stTextInput, .stTextArea, .stSelectbox {
            color: white !important;
        }
        
        /* Inputs - Gris oscuro */
        .stTextInput>div>div>input, 
        .stTextArea>div>div>textarea,
        .stSelectbox>div>div>select {
            background-color: #333 !important;
            color: white !important;
            border: 1px solid #444 !important;
        }
        
        /* Títulos y headers - Blanco */
        h1, h2, h3, h4, h5, h6 {
            color: white !important;
        }
        
        /* Mensajes de Streamlit */
        .stAlert {
            background-color: #333 !important;
            border: 1px solid #444 !important;
        }
        
        .stInfo {
            background-color: #1a237e !important;
        }
        
        /* Ajustar el contenedor de la cámara */
        .stImage>div>div>img {
            background-color: #000 !important;
            border: 2px solid #333 !important;
        }
        
        /* Botón de acceso principal */
        .main-access-btn {
            background-color: #4CAF50 !important;
            color: white !important;
            font-size: 20px !important;
            padding: 15px 30px !important;
            border-radius: 8px !important;
            margin: 20px auto !important;
            display: block !important;
            width: 80% !important;
        }
        .main-access-btn:hover {
            background-color: #45a049 !important;
        }
        
        /* Botón para volver al inicio */
        .back-home-btn {
            background-color: #FF5722 !important;
            color: white !important;
            font-size: 16px !important;
            padding: 10px 20px !important;
            border-radius: 6px !important;
            margin: 10px 0 !important;
        }
        .back-home-btn:hover {
            background-color: #E64A19 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    if not st.session_state.get('authenticated', False):
        st.markdown("""
            <style>
                section[data-testid="stSidebar"] {display: none !important;}
            </style>
        """, unsafe_allow_html=True)

def load_lsch_model_and_scaler():
    """Carga el modelo y el scaler para LSCh."""
    try:
        if os.path.exists(MODEL_FULL_PATH) and os.path.exists(SCALER_FULL_PATH):
            model = joblib.load(MODEL_FULL_PATH)
            scaler = joblib.load(SCALER_FULL_PATH)
            recognized_signs = list(model.classes_)
            
            if hasattr(scaler, 'n_features_in_') and scaler.n_features_in_ != TARGET_FEATURES_LSCH:
                st.error(f"Conflicto de dimensiones: El scaler espera {scaler.n_features_in_} características, "
                         f"pero la app está configurada para {TARGET_FEATURES_LSCH}.")
                return None, None, []
            
            print(f"LSCh: Modelo '{MODEL_FILENAME}' y scaler cargados. Señas: {recognized_signs}")
            return model, scaler, recognized_signs
        else:
            st.error(f"Error Crítico LSCh: Archivos de modelo/scaler no encontrados en '{MODEL_DIR}'.")
            return None, None, []
    except Exception as e:
        st.error(f"Error Crítico LSCh al cargar modelo/scaler: {e}")
        return None, None, []

def extract_landmarks_lsch(multi_hand_world_landmarks, multi_handedness):
    if TARGET_FEATURES_LSCH == 126: # Dos manos
        left_hand_features = np.zeros(EXPECTED_FEATURES_PER_HAND)
        right_hand_features = np.zeros(EXPECTED_FEATURES_PER_HAND)
        if multi_hand_world_landmarks:
            for i, hand_landmarks in enumerate(multi_hand_world_landmarks):
                handedness_label = ""
                if multi_handedness and i < len(multi_handedness) and multi_handedness[i].classification:
                    handedness_label = multi_handedness[i].classification[0].label
                current_hand_features_list = []
                for landmark in hand_landmarks.landmark:
                    current_hand_features_list.extend([landmark.x, landmark.y, landmark.z])
                current_hand_features = np.array(current_hand_features_list).flatten()
                if handedness_label == "Left": left_hand_features = current_hand_features
                elif handedness_label == "Right": right_hand_features = current_hand_features
                elif len(multi_hand_world_landmarks) == 1: left_hand_features = current_hand_features
        return np.concatenate((left_hand_features, right_hand_features)).flatten()
    
    elif TARGET_FEATURES_LSCH == 63: # Una mano
        features_live = []
        if multi_hand_world_landmarks:
            hand_world_landmarks_live = multi_hand_world_landmarks[0]
            for landmark_live in hand_world_landmarks_live.landmark:
                features_live.extend([landmark_live.x, landmark_live.y, landmark_live.z])
            return np.array(features_live).flatten()
        return np.array([])
    else:
        st.error(f"TARGET_FEATURES_LSCH ({TARGET_FEATURES_LSCH}) no es un valor esperado (63 o 126).")
        return np.array([])

def speak_text_with_gtts_lsch(text_to_speak, lang='es'):
    if not text_to_speak:
        st.toast("Nada que decir.", icon="🤷")
        return
    try:
        tts = gTTS(text=text_to_speak, lang=lang, slow=False)
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        st.audio(audio_fp, format='audio/mp3')
    except Exception as e:
        st.error(f"Error al generar o reproducir audio con gTTS: {e}")

def log_prediction(username, sign, confidence):
    """Registra una predicción en la tabla predictions usando DuckDB."""
    try:
        prediction_data = {
            'username': username,
            'sign': sign,
            'confidence': float(confidence),
            'timestamp': datetime.now(timezone.utc).replace(tzinfo=None)
        }
        df = pd.DataFrame([prediction_data], columns=COLUMNS_MAP["predictions"])
        auth_utils.save_data(PREDICTIONS_TABLE, df)
    except Exception as e:
        print(f"Error al registrar predicción: {e}")

def show_authentication_page():
    """Muestra la página de autenticación."""
    st.title("🔐 Traductor de Lenguaje de Señas Chileno")
    st.markdown("Por favor, inicia sesión o regístrate para continuar.")
    
    tab_login, tab_register = st.tabs([" Iniciar Sesión ", " Registrarse "])
    with tab_login:
        login_form()
    with tab_register:
        register_form()

def show_welcome_panel():
    """Muestra el panel de bienvenida con botón de acceso al traductor."""
    st.title("🤟 Bienvenido al Traductor LSCh")
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h3>Este sistema reconoce palabras en lenguaje de señas</h3>
        <p>Presiona el botón para comenzar la traducción</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("ENTRAR AL TRADUCTOR", key="main_access_btn", use_container_width=True, 
                help="Haz clic aquí para comenzar a usar el traductor de lenguaje de señas"):
        st.session_state.show_translator = True
        st.rerun()
    
    st.markdown("---")
    st.info("""
    **Señas reconocidas:** ABURRIDO, ACAMPAR, ACUERDO, ALAMEDA, AMERICA, ANIMAL, APLAUDIR, 
    ATENTO, BIEN, BURLARSE, BURRO, CASA, COMER, DINOSAURIO, DORMIR, HOLA, TE_QUIERO 
    """)

def show_main_translator_interface(lsch_model, lsch_scaler, lsch_recognized_signs):
    """Muestra la interfaz principal del traductor."""
    mp_hands_lsch = mp.solutions.hands
    hands_detector_lsch = mp_hands_lsch.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.50,
        min_tracking_confidence=0.45
    )
    mp_drawing_lsch = mp.solutions.drawing_utils
    
    # --- UI Principal ---
    st.title(f"🎤 Traductor Sign Language AI LSCh ")
    st.subheader("Creado por Kael, Joaquín y Franco para un mundo mejor")
    
    if st.button("🏠 Volver al Inicio", key="back_to_home_btn", 
                help="Volver a la página principal", 
                use_container_width=True,
                type="primary"):
        st.session_state.show_translator = False
        st.rerun()
    
    st.info(f"**Este prototipo reconoce las siguientes señas:**\n `{', '.join(lsch_recognized_signs)}`")

    if 'camera_is_active' not in st.session_state: st.session_state.camera_is_active = False
    if 'accumulated_phrase_words' not in st.session_state: st.session_state.accumulated_phrase_words = []
    if 'last_added_sign_info' not in st.session_state: st.session_state.last_added_sign_info = {"sign": None, "time": 0, "count":0}

    col_btn_start_stop_row1 = st.columns([1,1,1.5]) 
    with col_btn_start_stop_row1[0]:
        if st.button("🚀 Iniciar Cámara", key="start_lsch_cam", use_container_width=True, type="primary", disabled=st.session_state.camera_is_active):
            st.session_state.camera_is_active = True
            st.rerun()
    with col_btn_start_stop_row1[1]:
        if st.button("🛑 Detener Cámara", key="stop_lsch_cam", use_container_width=True, disabled=not st.session_state.camera_is_active):
            st.session_state.camera_is_active = False
            st.rerun()

    layout_main_cols = st.columns([2.5, 1.5])
    with layout_main_cols[0]:
        st.header("📹 Señal de Cámara")
        frame_display_placeholder = st.empty()
        if not st.session_state.camera_is_active: 
            frame_display_placeholder.info("Cámara desactivada. Presiona 'Iniciar Cámara' para comenzar.")

    with layout_main_cols[1]:
        st.header("📝 Traducción")
        st.subheader("Predicción Actual:")
        current_prediction_display_text = st.empty()
        current_prediction_display_text.markdown("`Esperando inicio...`")
        
        st.subheader("Frase Generada:")
        st.text_area("Frase:", 
                    value=" ".join(st.session_state.accumulated_phrase_words), 
                    height=100, 
                    key=f"phrase_display_lsch_auth_{len(st.session_state.accumulated_phrase_words)}", 
                    disabled=True)
        
        col_btn_escuchar, col_btn_limpiar_frase = st.columns(2)
        with col_btn_escuchar:
            if st.button("🎧 Escuchar Frase", key="listen_phrase_lsch", use_container_width=True,
                        disabled=not st.session_state.accumulated_phrase_words):
                speak_text_with_gtts_lsch(" ".join(st.session_state.accumulated_phrase_words))
        
        with col_btn_limpiar_frase:
            if st.button("🗑️ Limpiar Frase", key="clear_phrase_lsch", use_container_width=True,
                        disabled=not st.session_state.accumulated_phrase_words):
                st.session_state.accumulated_phrase_words = []
                st.session_state.last_added_sign_info = {"sign": None, "time": 0, "count":0}
                st.rerun()
    
    # --- Lógica de Cámara ---
    CONFIDENCE_THRESHOLD_FOR_DISPLAY = 0.55
    CONFIDENCE_THRESHOLD_FOR_ADDING_TO_PHRASE = 0.70
    DEBOUNCE_TIME_SECONDS = 1.7
    MAX_CONSECUTIVE_ADDS = 1

    if st.session_state.camera_is_active and lsch_model and lsch_scaler:
        video_capture_device = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not video_capture_device.isOpened():
            st.error("Error Crítico LSCh: No se pudo acceder a la cámara web."); st.session_state.camera_is_active = False; st.rerun()
        else:
            print(f"LSCh: Cámara iniciada (modelo con {len(lsch_recognized_signs)} palabras).")
            while st.session_state.camera_is_active and video_capture_device.isOpened():
                success, frame_from_cam = video_capture_device.read()
                if not success or frame_from_cam is None: st.warning("Frame LSCh no capturado."); time.sleep(0.1); continue
                
                frame_from_cam_flipped = cv2.flip(frame_from_cam, 1)
                frame_rgb_for_mediapipe = cv2.cvtColor(frame_from_cam_flipped, cv2.COLOR_BGR2RGB)
                frame_rgb_for_mediapipe.flags.writeable = False
                results_from_mediapipe = hands_detector_lsch.process(frame_rgb_for_mediapipe)
                frame_to_display_on_streamlit = frame_from_cam_flipped.copy()
                current_detected_sign_text = "`Detectando...`"

                if results_from_mediapipe.multi_hand_world_landmarks:
                    if results_from_mediapipe.multi_hand_landmarks:
                        for hand_screen_landmarks_data in results_from_mediapipe.multi_hand_landmarks:
                            mp_drawing_lsch.draw_landmarks(
                                frame_to_display_on_streamlit, hand_screen_landmarks_data, mp_hands_lsch.HAND_CONNECTIONS)
                    try:
                        live_features = extract_landmarks_lsch(
                            results_from_mediapipe.multi_hand_world_landmarks,
                            results_from_mediapipe.multi_handedness
                        )

                        if live_features.size > 0 and live_features.shape[0] == TARGET_FEATURES_LSCH:
                            live_features_scaled = lsch_scaler.transform(live_features.reshape(1, -1))
                            prediction_probabilities = lsch_model.predict_proba(live_features_scaled)[0]
                            predicted_class_index = np.argmax(prediction_probabilities)
                            prediction_confidence = prediction_probabilities[predicted_class_index]
                            predicted_sign_label = lsch_model.classes_[predicted_class_index]

                            if prediction_confidence >= CONFIDENCE_THRESHOLD_FOR_DISPLAY:
                                current_detected_sign_text = f"**{predicted_sign_label}** (Conf: {prediction_confidence:.2f})"
                                current_time_seconds = time.time(); last_info = st.session_state.last_added_sign_info
                                if prediction_confidence >= CONFIDENCE_THRESHOLD_FOR_ADDING_TO_PHRASE:
                                    allow_add = False
                                    if predicted_sign_label != last_info["sign"]:
                                        allow_add = True; st.session_state.last_added_sign_info["count"] = 1
                                    elif current_time_seconds - last_info["time"] > DEBOUNCE_TIME_SECONDS:
                                        if last_info["count"] < MAX_CONSECUTIVE_ADDS:
                                            allow_add = True; st.session_state.last_added_sign_info["count"] += 1
                                    
                                    if allow_add:
                                        add_to_phrase_cond = False
                                        if not st.session_state.accumulated_phrase_words or \
                                           st.session_state.accumulated_phrase_words[-1] != predicted_sign_label:
                                            add_to_phrase_cond = True
                                        elif predicted_sign_label == last_info["sign"] and \
                                             (current_time_seconds - last_info["time"] > DEBOUNCE_TIME_SECONDS):
                                            add_to_phrase_cond = True

                                        if add_to_phrase_cond:
                                            st.session_state.accumulated_phrase_words.append(predicted_sign_label)
                                            st.session_state.last_added_sign_info["sign"] = predicted_sign_label
                                            st.session_state.last_added_sign_info["time"] = current_time_seconds
                                            log_prediction(st.session_state.current_user, predicted_sign_label, prediction_confidence)
                                            st.rerun()
                            else:
                                current_detected_sign_text = "`Buscando seña... (baja conf.)`"
                        elif live_features.size > 0 and live_features.shape[0] != TARGET_FEATURES_LSCH:
                            current_detected_sign_text = f"`Error en dimensiones ({live_features.shape[0]} vs {TARGET_FEATURES_LSCH})`"
                    except Exception as e:
                        current_detected_sign_text = f"`Error procesando: {str(e)[:30]}...`"
                        print(f"LSCh: Error procesando landmarks en vivo: {e}")
                
                frame_display_placeholder.image(cv2.cvtColor(frame_to_display_on_streamlit, cv2.COLOR_BGR2RGB), channels="RGB")
                current_prediction_display_text.markdown(current_detected_sign_text)
                time.sleep(0.01) 
                if not st.session_state.camera_is_active: break
            
            video_capture_device.release()
            if not st.session_state.camera_is_active:
                frame_display_placeholder.info("Cámara detenida.")
                current_prediction_display_text.markdown("`Cámara detenida.`")

def show_tips_content():
    """Muestra el contenido de Tips"""
    st.title("💡 Consejos para Comunicarte en LSCh")
    st.markdown("""
### 👐 Aprende el alfabeto dactilológico (alfabeto manual)
- Es fundamental para deletrear nombres propios, lugares y palabras que no sabes cómo se señan.
- Practica hasta poder hacerlo con fluidez.

### 👀 Mantén el contacto visual
- En LSCh, la **expresión facial y el contacto visual** son esenciales para mostrar emociones, intenciones y tipo de oraciones (preguntas, afirmaciones, etc.).
- No mires al suelo o a otro lado mientras señalas.

### 😯 Usa expresiones faciales y corporales
- Son tan importantes como las manos.
- Por ejemplo, para una **pregunta**, debes levantar las cejas y mover ligeramente la cabeza hacia adelante.

### ✋ Usa una sola mano o ambas, según la seña
- Algunas señas se hacen con una sola mano y otras con las dos. Asegúrate de no mezclar.
- Si eres diestro, tu mano dominante debe ser la principal al señalar.

### 🗣️ No hables y señales al mismo tiempo (si no dominas la lengua)
- Al principio, puede ser mejor **concentrarte solo en las señas**.
- Más adelante puedes acompañarlas de voz si tu interlocutor lo prefiere.

### 🤔 Aprende vocabulario básico primero
Comienza por:
- **Saludos:** hola, adiós, gracias, por favor.
- **Pronombres personales:** yo, tú, él/ella, nosotros.
- **Preguntas básicas:** qué, quién, dónde, cuándo, por qué, cómo.
- **Colores, números, días de la semana, emociones.**

### 👂 Observa y practica con personas sordas o intérpretes certificados
- La mejor forma de aprender LSCh es con personas que la usan diariamente.
- Participa en actividades inclusivas o talleres.

### 📱 Usa recursos digitales para aprender
- Apps como **SpreadTheSign**, **Lingvano**, o videos en YouTube con contenido en **LSCh**.
- Prefiere canales chilenos o señantes locales.

### 📘 Sé paciente y constante
- La LSCh es una **lengua completa, visual y muy rica**.
- Aprenderla requiere tiempo y práctica. No temas equivocarte. Lo importante es mostrar respeto e interés genuino.
    """)

    
    if 'accumulated_phrase_words' in st.session_state and st.session_state.accumulated_phrase_words:
        current_sign = st.session_state.accumulated_phrase_words[-1]
        st.subheader(f"💡 Consejos para la seña: {current_sign}")
        
        sign_tips = {
            "hola": "Mueve la mano como un saludo, con la palma hacia afuera",
            "te_quiero": "Cruza los brazos sobre el pecho con las manos abiertas",
            "bien": "Levanta el pulgar hacia arriba con la mano abierta",
            "comer": "Junta los dedos y llévalos hacia la boca",
            "casa": "Forma una 'C' con ambas manos y colócalas cerca de la cara",
            "dormir": "Coloca la mano abierta cerca de la cara, como si descansaras la cabeza",
            "dinosaurio": "Imita las garras de un dinosaurio con ambas manos",
            "america": "Forma una 'A' con ambas manos y muévelas hacia el lado",
            "cine": "Imita el movimiento de una cámara de cine con las manos",
            "aburrido": "Coloca la mano en la barbilla con expresión de aburrimiento",
            "acampar": "Imita una tienda de campaña con las manos",
            "acuerdo": "Junta las manos como si firmaras un acuerdo",
            "alameda": "Seña local, mueve las manos como si caminaras por un parque",
            "animal": "Imita garras o movimientos de un animal",
            "aplaudir": "Golpea las manos suavemente",
            "atento": "Coloca las manos cerca de los oídos, como escuchando",
            "burro": "Imita las orejas de un burro con las manos",
            "burlarse": "Seña de burla con expresión facial y movimiento de manos"
        }
        
        tip = sign_tips.get(current_sign.lower(), "Realiza el gesto con claridad y precisión")
        st.info(f"**Cómo hacer esta seña:** {tip}")

def show_videos_content():
    """Muestra el contenido de Videos Tutoriales"""
    st.title("🎥 Tutoriales en Video para Aprender LSCh")
    st.subheader("Explora videos prácticos para aprender señas básicas de forma visual y entretenida")

    st.markdown("""
Estos tutoriales están diseñados para ayudarte a familiarizarte con la **Lengua de Señas Chilena (LSCh)**.  
Aquí podrás aprender saludos, el alfabeto dactilológico, vocabulario común y expresiones esenciales mediante ejemplos visuales.

👇 ¡Haz clic en los videos para comenzar a practicar tus primeras señas!
    """)
    
    with st.expander("🔤 Alfabeto Dactilológico"):
        st.video("https://youtu.be/8AkvNVUXiUw?feature=shared")
        st.video("https://youtu.be/Vw069dT12wU?feature=shared")
        st.video("https://youtu.be/LhHcQJkB008?feature=shared")
        st.markdown("Aprende el abecedario en LSCh paso a paso")
        
    with st.expander("👋 Saludos Básicos"):
        st.video("https://youtu.be/qG1CQFiHX6c?feature=shared")
        st.video("https://youtu.be/cBpjMSEuEvU?feature=shared")
        st.video("https://youtu.be/fhqAxgxOP1A?feature=shared")
        st.markdown("Cómo saludar y presentarte en LSCh")
        
    with st.expander("🗣️ Frases Comunes"):
        st.video("https://youtu.be/q6WZM7Mp-yk?feature=shared")
        st.video("https://youtu.be/iiB8k15GBno?feature=shared")
        st.video("https://youtu.be/kgeoWSjueAE?feature=shared")
        st.markdown("Frases útiles para el día a día")
        
    with st.expander("🏥 Emergencias"):
        st.video("https://youtu.be/Z53blnW5pY4?feature=shared")
        st.video("https://youtu.be/MkoUzhUrYCM?feature=shared")
        st.video("https://youtu.be/_8dhXsbxfcQ?feature=shared")
        st.video("https://youtu.be/fd6dQbCFpbk?feature=shared")
        st.markdown("Señas importantes para situaciones de emergencia")


def show_links_content():
    """Muestra el contenido de Enlaces Útiles"""
    st.title("🔗 Enlaces Útiles")
    st.markdown("""
    **Recursos esenciales para aprender y practicar lengua de señas chilena (LSCh) y otros lenguajes de señas:**  
    *Descarga diccionarios, accede a cursos gratuitos y conecta con comunidades.*  
    """)
    
    st.markdown("""
    ### 📚 Diccionarios y Documentos  
    - [Diccionario LSCh Parte 1 (A-H)](file:///C:/Users/pasit/Downloads/Diccionario_LSCh_A-H.pdf)  
    - [Diccionario LSCh Parte 2 (I-Z)](file:///C:/Users/pasit/Downloads/Diccionario_LSCh_I-Z.pdf)  
    - [Manual de Lenguajes de Signos (Euskadi)](https://www.euskadi.eus/contenidos/documentacion/inn_doc_esc_inclusiva/es_def/adjuntos/especiales/110021c_Pub_IDC_guia_leng_signos_lh1_c.pdf)  

    ### 🎓 Cursos y Comunidades  
    - [Cursos Gratuitos de LSCh (Fundación Wazu)](https://fundacionwazu.cl/servicios-a-empresas/curso-de-lengua-de-senas/?gad_source=1)  
    - [Asociación de Sordos de Chile](https://www.sordoschilenos.cl/)  

    ### 📱 Aplicaciones Prácticas  
    - [App de Lenguaje de Señas (Google Play)](https://play.google.com/store/apps/details?id=deaf.khokhar.yousaf.deafsignapp&hl=es_US)  
    """)

def show_resource_content(resource_name):
    """
    Muestra el contenido detallado de recursos educativos especializados

    Args:
        resource_name (str): Nombre del recurso a mostrar
    """
    st.title(f"📚 {resource_name}")

    # Diccionario de recursos
    resources = {
        "Diccionario LSCh Online": {
            "description": "Acceso al diccionario oficial de Lengua de Señas Chilena",
            "content": """
### 📘 Recurso completo para aprendizaje de señas

- [🔗 Diccionario LSCh A–H (PDF oficial del Mineduc)](https://especial.mineduc.cl/wp-content/uploads/sites/31/2018/07/Diccionario_LSCh_A-H.pdf)  
  Contiene señas organizadas alfabéticamente de la A a la H, con ilustraciones claras y explicaciones de configuración manual.

- [🔗 Diccionario LSCh I–Z (PDF oficial del Mineduc)](https://especial.mineduc.cl/wp-content/uploads/sites/31/2018/07/Diccionario_LSCh_I-Z.pdf)  
  Segunda parte del diccionario, con el resto del abecedario.
            """
        },
        "Cursos Gratuitos de LSCh": {
            "description": "Opciones formativas para aprender Lengua de Señas Chilena",
            "content": """
### 🎓 Oferta educativa disponible

- [🔗 Cursos básicos y talleres (Fundación Sordos Chilenos)](https://www.sordoschilenos.cl/que-hacemos/cursos-y-capacitaciones/)  
  Incluyen clases presenciales y online, para distintos niveles y perfiles (familias, profesionales, estudiantes, etc.).

- Certificación reconocida y acompañamiento pedagógico
- Talleres temáticos y actividades prácticas
            """
        },
        "Asociación de Sordos de Chile": {
            "description": "Organización líder en representación de la comunidad sorda",
            "content": """
### 🧩 Información institucional

- [🔗 Portal web oficial de ASOCH](http://www.asoch.cl/)  
  Espacio para acceder a noticias, eventos y recursos legales relacionados con la comunidad sorda en Chile.

- Servicios de orientación y apoyo legal  
- Inclusión laboral y derechos lingüísticos  
- Actividades y calendario comunitario
            """
        },
        "Manual de Lenguajes de Señas": {
            "description": "Guía pedagógica para enseñanza de LSCh",
            "content": """
### 📙 Material didáctico completo

- [🔗 Manual en línea (SlideShare)](https://es.slideshare.net/slideshow/manual-de-lengua-de-senaschilenaeducpdf/267044746)  
  Curso estructurado con fundamentos lingüísticos y actividades por nivel.

- [🔗 Manual para el curso de LSCh – Scribd](https://es.scribd.com/document/684564204/Manual-para-el-curso-de-LSCh)  
  Ideal para principiantes: saludos, números, vocabulario diario.

- [🔗 Manual LSCh Nivel Básico – Scribd](https://es.scribd.com/document/732041397/Manual-de-Lsch-Nivel-Basico)  
  Incluye gramática visual, expresión facial y contexto cultural.

- Guías para educadores y adaptaciones curriculares
            """
        }
    }

    # Verifica si el recurso existe y muestra su contenido
    if resource_name in resources:
        st.markdown(f"**{resources[resource_name]['description']}**")
        st.markdown(resources[resource_name]["content"])
    else:
        st.warning("El recurso seleccionado no está disponible.")


def manage_users():
    """Interfaz para gestionar usuarios con búsqueda mejorada."""
    try:
        from utils import search_users, get_user_statistics
        has_duckdb = True
    except ImportError:
        has_duckdb = False
    
    users_df = auth_utils.load_data("users")
    
    if has_duckdb:
        st.subheader("🔍 Buscar Usuarios")
        search_term = st.text_input("Buscar por username o email")
        if search_term:
            results = auth_utils.search_users(search_term)
            if not results.empty:
                st.dataframe(results, use_container_width=True)
            else:
                st.info("No se encontraron usuarios")
    
    st.subheader("Lista de Usuarios Registrados")
    display_df = users_df[['username', 'email', 'role', 'active', 'created_at']].copy()
    display_df['active'] = display_df['active'].astype(str)
    st.dataframe(display_df, use_container_width=True)
    
    st.subheader("Acciones de Administración")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Cambiar Rol de Usuario**")
        user_to_change = st.selectbox("Seleccionar Usuario", users_df['username'].unique(), key="change_role_user")
        new_role = st.selectbox("Nuevo Rol", ['admin', 'user'], key="new_role")
        if st.button("Actualizar Rol"):
            users_df.loc[users_df['username'] == user_to_change, 'role'] = new_role
            auth_utils.save_data("users", users_df)
            st.success(f"Rol de {user_to_change} actualizado a {new_role}")
    
    with col2:
        st.markdown("**Activar/Desactivar Usuario**")
        user_to_toggle = st.selectbox("Seleccionar Usuario", users_df['username'].unique(), key="toggle_user")
        current_status = users_df.loc[users_df['username'] == user_to_toggle, 'active'].iloc[0]
        new_status = not current_status
        action = "Activar" if new_status else "Desactivar"
        if st.button(f"{action} Usuario"):
            users_df.loc[users_df['username'] == user_to_toggle, 'active'] = new_status
            auth_utils.save_data("users", users_df)
            st.success(f"Usuario {user_to_toggle} {'activado' if new_status else 'desactivado'} correctamente")

def show_usage_stats():
    """Muestra estadísticas de uso del sistema usando DuckDB."""
    st.markdown("""
        Descubre el rendimiento integral de la plataforma con datos estratégicos que te permitirán:

📊 Monitorizar el crecimiento: Evolución de usuarios activos, patrones de registro y adopción

👤 Segmentación de usuarios: Distribución entre roles (administradores/usuarios) y estado de actividad

🤖 Eficiencia del modelo: Precisión en reconocimiento de señas, confianza promedio y tendencias de predicción

⏳ Dinámica de uso: Duración de sesiones, frecuencia de acceso y horas pico de actividad

Visualización interactiva con filtros personalizables para un análisis granular. Exporta reportes detallados para tomar decisiones basadas en datos.
    """)
    st.subheader("Datos de Uso del Sistema")
    
    try:
        user_stats = auth_utils.get_user_statistics()
    except AttributeError:
        users_df = auth_utils.load_data("users")
        user_stats = {
            'total_users': len(users_df),
            'active_users': users_df['active'].sum(),
            'admin_users': (users_df['role'] == 'admin').sum()
        }
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Usuarios", user_stats['total_users'])
    with col2:
        st.metric("Usuarios Activos", user_stats['active_users'])
    with col3:
        st.metric("Administradores", user_stats['admin_users'])
    
    st.subheader("Registros de Usuarios")
    
    # Cargar datos de usuarios para el expander
    users_df_for_display = auth_utils.load_data("users")
    if not users_df_for_display.empty:
        with st.expander("Ver Tabla de Registros de Usuarios"):
            st.dataframe(users_df_for_display[['username', 'email', 'role', 'active', 'created_at']], use_container_width=True)
    else:
        st.info("Actualmente no hay usuarios registrados en el sistema.")
        
    try:
        registrations = auth_utils.get_daily_registrations()
        if not registrations.empty:
            chart_data = {
                "labels": registrations['date'].dt.strftime('%Y-%m-%d').tolist(),
                "datasets": [{
                    "label": "Registros Diarios",
                    "data": registrations['registrations'].tolist(),
                    "backgroundColor": "#1e88e5",
                    "borderColor": "#1565c0",
                    "borderWidth": 1
                }]
            }
            st.markdown("""
            <div>
                <canvas id="registrationsChart"></canvas>
                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
                <script>
                    const ctx = document.getElementById('registrationsChart').getContext('2d');
                    new Chart(ctx, {
                        type: 'line',
                        data: """ + str(chart_data) + """,
                        options: {
                            scales: {
                                x: {
                                    title: {
                                        display: true,
                                        text: 'Fecha',
                                        color: '#ffffff'
                                    },
                                    ticks: {
                                        color: '#ffffff'
                                    }
                                },
                                y: {
                                    title: {
                                        display: true,
                                        text: 'Número de Registros',
                                        color: '#ffffff'
                                    },
                                    ticks: {
                                        color: '#ffffff'
                                    },
                                    beginAtZero: true
                                }
                            },
                            plugins: {
                                legend: {
                                    labels: {
                                        color: '#ffffff'
                                    }
                                }
                            }
                        }
                    });
                </script>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No hay datos de registros diarios para mostrar en el gráfico.")
    except AttributeError:
        users_df = auth_utils.load_data("users")
        if not users_df.empty and 'created_at' in users_df.columns:
            users_by_date = users_df.set_index('created_at').resample('D').size().reset_index(name='registrations')
            users_by_date.columns = ['date', 'registrations']
            chart_data = {
                "labels": users_by_date['date'].dt.strftime('%Y-%m-%d').tolist(),
                "datasets": [{
                    "label": "Registros Diarios",
                    "data": users_by_date['registrations'].tolist(),
                    "backgroundColor": "#1e88e5",
                    "borderColor": "#1565c0",
                    "borderWidth": 1
                }]
            }
            st.markdown("""
            <div>
                <canvas id="registrationsChartFallback"></canvas>
                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
                <script>
                    const ctx = document.getElementById('registrationsChartFallback').getContext('2d');
                    new Chart(ctx, {
                        type: 'line',
                        data: """ + str(chart_data) + """,
                        options: {
                            scales: {
                                x: {
                                    title: {
                                        display: true,
                                        text: 'Fecha',
                                        color: '#ffffff'
                                    },
                                    ticks: {
                                        color: '#ffffff'
                                    }
                                },
                                y: {
                                    title: {
                                        display: true,
                                        text: 'Número de Registros',
                                        color: '#ffffff'
                                    },
                                    ticks: {
                                        color: '#ffffff'
                                    },
                                    beginAtZero: true
                                }
                            },
                            plugins: {
                                legend: {
                                    labels: {
                                        color: '#ffffff'
                                    }
                                }
                            }
                        }
                    });
                </script>
            </div>
            """, unsafe_allow_html=True)
    
    st.subheader("Actividad de Sesiones")

    sessions_df = auth_utils.load_data("sessions")
    if not sessions_df.empty:
        with st.expander("Ver Tabla de Actividad de Sesiones"):
            st.dataframe(sessions_df, use_container_width=True)
    else:
        st.info("No hay datos de sesiones para mostrar.")

    try:
        sessions = auth_utils.get_recent_sessions()
        if not sessions.empty:
            st.markdown("##### Gráfico de Actividad de Sesiones Recientes")
            chart_data = {
                "labels": sessions['created_at'].dt.strftime('%Y-%m-%d %H:%M').tolist(),
                "datasets": [{
                    "label": "Sesiones Creadas",
                    "data": [1] * len(sessions),
                    "backgroundColor": "#4CAF50",
                    "borderColor": "#45a049",
                    "borderWidth": 1
                }]
            }
            st.markdown("""
            <div>
                <canvas id="sessionsChart"></canvas>
                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
                <script>
                    const ctx = document.getElementById('sessionsChart').getContext('2d');
                    new Chart(ctx, {
                        type: 'bar',
                        data: """ + str(chart_data) + """,
                        options: {
                            scales: {
                                x: {
                                    title: {
                                        display: true,
                                        text: 'Fecha y Hora',
                                        color: '#ffffff'
                                    },
                                    ticks: {
                                        color: '#ffffff'
                                    }
                                },
                                y: {
                                    title: {
                                        display: true,
                                        text: 'Número de Sesiones',
                                        color: '#ffffff'
                                    },
                                    ticks: {
                                        color: '#ffffff'
                                    },
                                    beginAtZero: true
                                }
                            },
                            plugins: {
                                legend: {
                                    labels: {
                                        color: '#ffffff'
                                    }
                                }
                            }
                        }
                    });
                </script>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No hay sesiones recientes para visualizar en el gráfico.")
    except (AttributeError, Exception) as e:
        if not sessions_df.empty and 'created_at' in sessions_df.columns:
            st.markdown("##### Gráfico de Historial de Sesiones")
            chart_data = {
                "labels": sessions_df['created_at'].dt.strftime('%Y-%m-%d %H:%M').tolist(),
                "datasets": [{
                    "label": "Sesiones Creadas",
                    "data": [1] * len(sessions_df),
                    "backgroundColor": "#4CAF50",
                    "borderColor": "#45a049",
                    "borderWidth": 1
                }]
            }
            st.markdown("""
            <div>
                <canvas id="sessionsChartFallback"></canvas>
                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
                <script>
                    const ctx = document.getElementById('sessionsChartFallback').getContext('2d');
                    new Chart(ctx, {
                        type: 'bar',
                        data: """ + str(chart_data) + """,
                        options: {
                            scales: {
                                x: {
                                    title: {
                                        display: true,
                                        text: 'Fecha y Hora',
                                        color: '#ffffff'
                                    },
                                    ticks: {
                                        color: '#ffffff'
                                    }
                                },
                                y: {
                                    title: {
                                        display: true,
                                        text: 'Número de Sesiones',
                                        color: '#ffffff'
                                    },
                                    ticks: {
                                        color: '#ffffff'
                                    },
                                    beginAtZero: true
                                }
                            },
                            plugins: {
                                legend: {
                                    labels: {
                                        color: '#ffffff'
                                    }
                                }
                            }
                        }
                    });
                </script>
            </div>
            """, unsafe_allow_html=True)
    
    st.subheader("Estadísticas de Predicciones")
    
    try:
        predictions_log = auth_utils.load_data("predictions_log")
    except Exception as e:
        predictions_log = pd.DataFrame()

    if not predictions_log.empty:
        with st.expander("Ver Log de Predicciones y Gráficos"):
            st.markdown("#### Log Completo de Predicciones")
            st.dataframe(predictions_log, use_container_width=True)

            # Gráfico de predicciones por seña
            st.markdown("#### Conteo de Predicciones por Seña")
            if 'predicted_sign' in predictions_log.columns:
                sign_counts = predictions_log['predicted_sign'].value_counts().reset_index()
                sign_counts.columns = ['sign', 'count']
                
                fig = px.bar(sign_counts, x='sign', y='count', title="Predicciones por Seña",
                             labels={'sign': 'Seña Reconocida', 'count': 'Número de Predicciones'},
                             color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("La columna 'predicted_sign' no se encuentra en el log.")

            # Gráfico de confianza promedio
            st.markdown("#### Confianza Promedio por Seña")
            if 'confidence' in predictions_log.columns and 'predicted_sign' in predictions_log.columns:
                avg_confidence = predictions_log.groupby('predicted_sign')['confidence'].mean().reset_index()
                
                fig2 = px.pie(avg_confidence, values='confidence', names='predicted_sign', 
                              title="Confianza Promedio por Seña",
                              color_discrete_sequence=px.colors.sequential.RdBu)
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("Faltan las columnas 'confidence' o 'predicted_sign' para este gráfico.")
                
    else:
        st.info(
            "No hay datos de predicciones disponibles para mostrar. "
            "El log de predicciones se genera a medida que los usuarios utilizan el traductor."
        )

def manage_model_config():
    """Interfaz para configurar el modelo."""
    st.subheader("Configuración Actual del Modelo")
    st.markdown(f"**Modelo cargado:** `{MODEL_FILENAME}`")
    st.markdown(f"**Scaler cargado:** `{SCALER_FILENAME}`")
    st.markdown(f"**Características esperadas:** `{TARGET_FEATURES_LSCH}`")
    
    st.subheader("Opciones de Administración")
    
    st.markdown("**Subir Nuevo Modelo**")
    uploaded_model = st.file_uploader("Seleccionar archivo de modelo (.pkl)", type=['pkl'], key="model_upload")
    uploaded_scaler = st.file_uploader("Seleccionar archivo de scaler (.pkl)", type=['pkl'], key="scaler_upload")
    
    if uploaded_model and uploaded_scaler:
        if st.button("Actualizar Modelo y Scaler"):
            try:
                with open(MODEL_FULL_PATH, 'wb') as f:
                    f.write(uploaded_model.getbuffer())
                with open(SCALER_FULL_PATH, 'wb') as f:
                    f.write(uploaded_scaler.getbuffer())
                
                model, scaler, signs = load_lsch_model_and_scaler()
                st.session_state.lsch_model = model
                st.session_state.lsch_scaler = scaler
                st.session_state.lsch_recognized_signs = signs
                
                st.success("Modelo y scaler actualizados correctamente. La aplicación se recargará.")
                time.sleep(2)
                st.rerun()
            except Exception as e:
                st.error(f"Error al actualizar el modelo: {e}")
    
    st.markdown("**Gestión de Datos de Entrenamiento**")
    if st.button("Reiniciar Datos de Entrenamiento (Precaución)"):
        try:
            backup_dir = os.path.join("datos_señas_palabras_v1", "backups")
            os.makedirs(backup_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(backup_dir, f"datos_palabras_dos_manos_{timestamp}.csv")
            original_path = os.path.join("datos_señas_palabras_v1", "datos_palabras_dos_manos.csv")
            
            if os.path.exists(original_path):
                import shutil
                shutil.copy2(original_path, backup_path)
                os.remove(original_path)
                st.success(f"Datos de entrenamiento reiniciados. Copia de seguridad guardada en {backup_path}")
            else:
                st.warning("No se encontró el archivo de datos original para hacer copia de seguridad.")
        except Exception as e:
            st.error(f"Error al reiniciar datos: {e}")

def show_sql_query_page():
    """Muestra una interfaz para ejecutar consultas SQL personalizadas."""
    st.markdown("""
    Ejecuta consultas SQL en tiempo real sobre la base de datos DuckDB con esta potente herramienta interactiva.

    ⚠ **Importante**  
    - Consultas de solo lectura (**SELECT**) permitidas sin restricciones  
    - Para operaciones de escritura (**INSERT/UPDATE/DELETE**):  
      ✓ Requieren privilegios administrativos  
      ✓ Se recomienda hacer backup previo  
      ✓ Verifica dos veces la sintaxis antes de ejecutar  

    💡 **Consejos profesionales**:  
    1. Prueba tus consultas con `LIMIT` en desarrollo  
    2. Usa transacciones para operaciones críticas  
    3. Consulta el diccionario de datos para conocer la estructura  

    *"Con gran poder viene gran responsabilidad" - Aprovecha esta herramienta con criterio*  
    """)
    
    # Text area for SQL query input
    sql_query = st.text_area("Escribe tu consulta SQL:", height=150, placeholder="SELECT * FROM users LIMIT 10")
    
    if st.button("Ejecutar Consulta", key="run_sql_query"):
        if sql_query.strip():
            try:
                result = auth_utils.query(sql_query)
                if not result.empty:
                    st.dataframe(result, use_container_width=True)
                else:
                    st.info("La consulta no devolvió resultados.")
            except Exception as e:
                st.error(f"Error al ejecutar la consulta: {e}")
        else:
            st.warning("Por favor, escribe una consulta SQL válida.")
    
    if st.button("⬅️ Volver al Panel de Control", key="back_to_admin_sql"):
        st.session_state.admin_page = None
        st.rerun()

def show_admin_page(page):
    """Muestra diferentes secciones del panel de administrador."""
    st.title(f"🔧 Panel de Administrador - {page.capitalize()}")
    
    if page == "users":
        st.header("👥 Gestión de Usuarios")
        manage_users()
    elif page == "stats":
        st.header("📊 Estadísticas de Uso")
        show_usage_stats()
    elif page == "model_config":
        st.header("⚙️ Configuración del Modelo")
        manage_model_config()
    elif page == "sql_query":
        st.header("🔍 Consultas SQL")
        show_sql_query_page()
    
    if page != "sql_query":  # Avoid duplicate back button for SQL page
        if st.button("⬅️ Volver al Panel de Control", key="back_to_admin"):
            st.session_state.admin_page = None
            st.rerun()

def show_admin_dashboard():
    """Muestra el panel de control principal del administrador."""
    st.title("🛠️ Panel de Control Administrativo")
    
    try:
        user_stats = auth_utils.get_user_statistics()
    except AttributeError:
        users_df = auth_utils.load_data("users")
        user_stats = {
            'total_users': len(users_df),
            'active_users': users_df['active'].sum(),
            'admin_users': (users_df['role'] == 'admin').sum()
        }
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Usuarios", user_stats['total_users'])
    with col2:
        st.metric("Usuarios Activos", user_stats['active_users'])
    with col3:
        st.metric("Administradores", user_stats['admin_users'])
    
    st.subheader("Opciones de Administración")
    admin_options = st.columns(4)
    
    with admin_options[0]:
        if st.button("👥 Gestión de Usuarios", use_container_width=True):
            st.session_state.admin_page = "users"
            st.rerun()
    
    with admin_options[1]:
        if st.button("📊 Estadísticas de Uso", use_container_width=True):
            st.session_state.admin_page = "stats"
            st.rerun()
    
    with admin_options[2]:
        if st.button("⚙️ Configuración del Modelo", use_container_width=True):
            st.session_state.admin_page = "model_config"
            st.rerun()
    
    with admin_options[3]:
        if st.button("🔍 Consultas SQL", use_container_width=True):
            st.session_state.admin_page = "sql_query"
            st.rerun()

def show_user_sidebar():
    """Muestra el sidebar para usuarios normales con recursos de aprendizaje."""
    with st.sidebar:
        st.success(f"Conectado: {st.session_state.current_user}")
        st.markdown("---")
        
        st.header("🚀 Traductor LSCh")
        if st.button("Traductor en Vivo", key="translator_btn"):
            st.session_state.show_tips = False
            st.session_state.show_videos = False
            st.session_state.show_links = False
            st.session_state.show_resources = False
            st.session_state.show_translator = True
            st.rerun()

        st.markdown("---")
        
        st.header("📚 Recursos de Aprendizaje LSCh")
        
        if st.button("💡 Tips", key="tips_btn"):
            st.session_state.show_tips = True
            st.session_state.show_videos = False
            st.session_state.show_links = False
            st.session_state.show_resources = False
            st.rerun()
            
        if st.button("🎥 Videos Tutoriales", key="videos_btn"):
            st.session_state.show_tips = False
            st.session_state.show_videos = True
            st.session_state.show_links = False
            st.session_state.show_resources = False
            st.rerun()
            
        if st.button("🔗 Enlaces Útiles", key="links_btn"):
            st.session_state.show_tips = False
            st.session_state.show_videos = False
            st.session_state.show_links = True
            st.session_state.show_resources = False
            st.rerun()
            
        st.markdown("---")
        
        st.header("📌 Recursos Adicionales")
        
        if st.button("📖 Diccionario LSCh Online", key="dict_btn"):
            st.session_state.show_tips = False
            st.session_state.show_videos = False
            st.session_state.show_links = False
            st.session_state.show_translator = False
            st.session_state.show_resources = True
            st.session_state.resource_to_show = "Diccionario LSCh Online"
            st.rerun()
            
        if st.button("🎓 Cursos Gratuitos de LSCh", key="courses_btn"):
            st.session_state.show_tips = False
            st.session_state.show_videos = False
            st.session_state.show_links = False
            st.session_state.show_translator = False
            st.session_state.show_resources = True
            st.session_state.resource_to_show = "Cursos Gratuitos de LSCh"
            st.rerun()
            
        if st.button("👥 Asociación de Sordos de Chile", key="asoch_btn"):
            st.session_state.show_tips = False
            st.session_state.show_videos = False
            st.session_state.show_links = False
            st.session_state.show_translator = False
            st.session_state.show_resources = True
            st.session_state.resource_to_show = "Asociación de Sordos de Chile"
            st.rerun()
            
        if st.button("📘 Manual de Lenguajes de Señas", key="manual_btn"):
            st.session_state.show_tips = False
            st.session_state.show_videos = False
            st.session_state.show_links = False
            st.session_state.show_translator = False
            st.session_state.show_resources = True
            st.session_state.resource_to_show = "Manual de Lenguajes de Señas"
            st.rerun()
            
        st.markdown("---")
        
        if st.button("🚪 Cerrar Sesión", key="logout_btn_lsch_sidebar", use_container_width=True):
            logout_user()

def show_admin_sidebar():
    """Muestra el sidebar para administradores con opciones de control."""
    with st.sidebar:
        st.success(f"Conectado como ADMIN: {st.session_state.current_user}")
        st.markdown("---")
        
        st.header("🛠️ Panel de Control")
            
        if st.button("👥 Gestión de Usuarios", key="admin_users_btn"):
            st.session_state.admin_page = "users"
            st.rerun()
            
        if st.button("📈 Estadísticas", key="admin_stats_btn"):
            st.session_state.admin_page = "stats"
            st.rerun()
            
        if st.button("⚙️ Configuración", key="admin_config_btn"):
            st.session_state.admin_page = "model_config"
            st.rerun()
            
        if st.button("🔍 Consultas SQL", key="admin_sql_btn"):
            st.session_state.admin_page = "sql_query"
            st.rerun()
            
        st.markdown("---")
        
        if st.button("🚪 Cerrar Sesión", key="admin_logout_btn", use_container_width=True):
            logout_user()

def show_user_interface(lsch_model, lsch_scaler, lsch_recognized_signs):
    """Muestra la interfaz completa para usuarios normales."""
    show_user_sidebar()
    
    if st.session_state.get('show_tips', False):
        show_tips_content()
    elif st.session_state.get('show_videos', False):
        show_videos_content()
    elif st.session_state.get('show_links', False):
        show_links_content()
    elif st.session_state.get('show_resources', False):
        show_resource_content(st.session_state.resource_to_show)
    elif st.session_state.get('show_translator', False):
        show_main_translator_interface(lsch_model, lsch_scaler, lsch_recognized_signs)
    else:
        show_welcome_panel()

def show_admin_interface(lsch_model, lsch_scaler, lsch_recognized_signs):
    """Muestra la interfaz completa para administradores."""
    show_admin_sidebar()
    
    if st.session_state.get('admin_page'):
        show_admin_page(st.session_state.admin_page)
    elif st.session_state.get('show_admin_panel', True):
        show_admin_dashboard()
    else:
        show_main_translator_interface(lsch_model, lsch_scaler, lsch_recognized_signs)

def main():
    if 'auth_initialized' not in st.session_state:
        auth_utils.initialize_data()
        st.session_state.auth_initialized = True

    session_manager.validate_session()
    config_page()

    if 'show_tips' not in st.session_state:
        st.session_state.show_tips = False
    if 'show_videos' not in st.session_state:
        st.session_state.show_videos = False
    if 'show_links' not in st.session_state:
        st.session_state.show_links = False
    if 'show_resources' not in st.session_state:
        st.session_state.show_resources = False
    if 'resource_to_show' not in st.session_state:
        st.session_state.resource_to_show = ""
    if 'show_translator' not in st.session_state:
        st.session_state.show_translator = True
    if 'show_admin_panel' not in st.session_state:
        st.session_state.show_admin_panel = True

    if not st.session_state.get('authenticated', False):
        show_authentication_page()
    else:
        if 'admin_page' not in st.session_state:
            st.session_state.admin_page = None
            
        if 'lsch_model' not in st.session_state or \
           'lsch_scaler' not in st.session_state or \
           'lsch_recognized_signs' not in st.session_state:
            model, scaler, signs = load_lsch_model_and_scaler()
            st.session_state.lsch_model = model
            st.session_state.lsch_scaler = scaler
            st.session_state.lsch_recognized_signs = signs
        
        if st.session_state.user_role == 'admin':
            show_admin_interface(
                st.session_state.lsch_model,
                st.session_state.lsch_scaler,
                st.session_state.lsch_recognized_signs
            )
        else:
            show_user_interface(
                st.session_state.lsch_model,
                st.session_state.lsch_scaler,
                st.session_state.lsch_recognized_signs
            )

if __name__ == "__main__":
    main()