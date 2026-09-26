# Archivo: capture_data.py
# (MODIFICADO PARA CAPTURAR DATOS DE DOS MANOS)
import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import os
import time

# --- Configuración ---
DATA_PATH = "datos_señas_palabras_v1" # Carpeta para guardar los datos
CSV_FILENAME = "datos_palabras_dos_manos.csv" # Nuevo nombre para el CSV de dos manos

if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)
    print(f"Carpeta de datos creada/verificada: {DATA_PATH}")

# Lista de señas a recolectar (puedes modificarla)
SIGNS_TO_COLLECT = [
    "HOLA", "TE_QUIERO", "BIEN", "COMER", "CASA",
    "DORMIR", "DINOSAURIO", "AMERICA", "CINE",
    "ABURRIDO","ACAMPAR","ACUERDO","ALAMEDA", "ANIMAL",
    "APLAUDIR","ATENTO","BURRO","BURLARSE"
] # Mantén o actualiza según tus necesidades

NUM_SAMPLES_PER_SIGN = 100 # Aumentar muestras puede ser beneficioso para dos manos

# --- Configuración de MediaPipe y Extracción de Landmarks para DOS MANOS ---
mp_hands = mp.solutions.hands
hands_detector = mp_hands.Hands(
    static_image_mode=True,  # True para captura de datos, frame por frame
    max_num_hands=2,         # <--- CAMBIO IMPORTANTE: Detectar hasta 2 manos
    min_detection_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

# Constantes para la extracción de características
NUM_LANDMARKS_PER_HAND = 21
NUM_COORDS_PER_LANDMARK = 3
EXPECTED_FEATURES_PER_HAND = NUM_LANDMARKS_PER_HAND * NUM_COORDS_PER_LANDMARK # 63
TARGET_FEATURES_TWO_HANDS = 2 * EXPECTED_FEATURES_PER_HAND # 126 -> Este es el nuevo tamaño del vector

def extract_landmarks_for_2_hands_capture(multi_hand_world_landmarks, multi_handedness):
    """
    Extrae landmarks para hasta dos manos y los formatea en un vector único.
    Ordena las manos (izquierda, luego derecha) y usa ceros si una mano falta.
    Importante: cv2.flip(frame, 1) se usa, por lo que 'Left' en handedness es la mano IZQUIERDA del usuario.
    """
    left_hand_features = np.zeros(EXPECTED_FEATURES_PER_HAND)
    right_hand_features = np.zeros(EXPECTED_FEATURES_PER_HAND)

    if multi_hand_world_landmarks:
        for i, hand_landmarks in enumerate(multi_hand_world_landmarks):
            handedness_label = ""
            if multi_handedness and i < len(multi_handedness) and multi_handedness[i].classification:
                handedness_label = multi_handedness[i].classification[0].label

            current_hand_features_list = []
            for landmark in hand_landmarks.landmark: # Usar world_landmarks da coordenadas relativas a la mano
                current_hand_features_list.extend([landmark.x, landmark.y, landmark.z])
            
            current_hand_features = np.array(current_hand_features_list).flatten()

            if handedness_label == "Left": # Mano izquierda del usuario
                left_hand_features = current_hand_features
            elif handedness_label == "Right": # Mano derecha del usuario
                right_hand_features = current_hand_features
            elif len(multi_hand_world_landmarks) == 1: # Si solo hay una mano y no se pudo determinar L/R
                # Asumimos que es la mano "principal" y la colocamos como "izquierda" por defecto.
                # Esto es una simplificación. Podrías querer una lógica más compleja o
                # pedir al usuario que especifique si está usando la mano izquierda o derecha
                # si la seña es inherentemente de una sola mano.
                # Para la recolección de datos, sé consistente: si una seña de una mano la haces
                # con la derecha, asegúrate que MediaPipe la detecte como "Right".
                # Si MediaPipe no da etiqueta y solo hay una mano, la ponemos en left_hand_features.
                # Si siempre usas la misma mano para señas de una mano, esto debería ser consistente.
                left_hand_features = current_hand_features


    combined_features = np.concatenate((left_hand_features, right_hand_features))
    return combined_features.flatten()

# --- Inicio de Captura ---
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # Usar CAP_DSHOW puede mejorar la respuesta en Windows
if not cap.isOpened():
    print("Error Crítico: No se pudo acceder a la cámara web.")
    exit()

all_collected_data = []
print(f"Iniciando script de captura de datos para DOS MANOS para las siguientes {len(SIGNS_TO_COLLECT)} PALABRAS/POSES:")
print(f"    {', '.join(SIGNS_TO_COLLECT)}")
print(f"Los datos se guardarán en: {os.path.join(DATA_PATH, CSV_FILENAME)}")
print(f"Se esperan {TARGET_FEATURES_TWO_HANDS} características por muestra.")
print(f"Fecha y Hora: {time.strftime('%Y-%m-%d %H:%M:%S')}")
print("----------------------------------------------------")

for sign_label in SIGNS_TO_COLLECT:
    print(f"\nPreparándose para recolectar datos para la PALABRA/POSE: '{sign_label}'")
    print(f"**MUY IMPORTANTE**: Realiza la POSE ESTÁTICA CLAVE (con una o dos manos) que definiste para '{sign_label}'.")
    print(f"Coloca tu(s) mano(s) consistentemente frente a la cámara.")
    print(f"Cuando estés listo/a, presiona la tecla 's' para empezar a capturar {NUM_SAMPLES_PER_SIGN} muestras.")
    print("Presiona 'q' en cualquier momento para salir del script.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error al leer frame."); cap.release(); cv2.destroyAllWindows(); exit()
        frame = cv2.flip(frame, 1) # Espejar para que sea más intuitivo
        cv2.putText(frame, f"Listo para POSE '{sign_label}'? Pres 's'", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow(f'Captura de Datos - {len(SIGNS_TO_COLLECT)} Palabras LSCh (DOS MANOS)', frame)
        key = cv2.waitKey(10) & 0xFF
        if key == ord('s'): break
        if key == ord('q'): print("Saliendo."); cap.release(); cv2.destroyAllWindows(); exit()

    print(f"Iniciando captura de {NUM_SAMPLES_PER_SIGN} muestras para la POSE de '{sign_label}'...")
    samples_captured_for_this_sign = 0
    while samples_captured_for_this_sign < NUM_SAMPLES_PER_SIGN:
        ret, frame = cap.read()
        if not ret: print("Error al leer frame durante captura."); break
        
        frame_flipped = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame_flipped, cv2.COLOR_BGR2RGB)
        results = hands_detector.process(frame_rgb)
        display_frame = frame_flipped.copy()

        if results.multi_hand_world_landmarks: # Usar world_landmarks para consistencia de escala y rotación
            # Dibujar landmarks de todas las manos detectadas
            if results.multi_hand_landmarks: # multi_hand_landmarks son para dibujar en pantalla
                for hand_screen_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        display_frame, hand_screen_landmarks, mp_hands.HAND_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(121,22,76),thickness=2,circle_radius=2),
                        mp_drawing.DrawingSpec(color=(250,44,250),thickness=2,circle_radius=1))
            try:
                # Extraer landmarks de ambas manos (o una con padding)
                landmarks_data = extract_landmarks_for_2_hands_capture(
                    results.multi_hand_world_landmarks, # Pasar world landmarks
                    results.multi_handedness
                )

                if landmarks_data.shape[0] == TARGET_FEATURES_TWO_HANDS: # Verificar el nuevo tamaño
                    all_collected_data.append(list(landmarks_data) + [sign_label])
                    samples_captured_for_this_sign += 1
                    print(f"Muestra {samples_captured_for_this_sign}/{NUM_SAMPLES_PER_SIGN} para '{sign_label}' capturada.")
                    time.sleep(0.10) # Pausa de 100ms
                else:
                    print(f"Alerta: Dimensiones incorrectas. Esperadas {TARGET_FEATURES_TWO_HANDS}, obtenidas {landmarks_data.shape[0]}")
            except Exception as e:
                print(f"Error extrayendo landmarks: {e}")
                # No interrumpir la captura por un frame fallido, solo registrar
        else:
            cv2.putText(display_frame, "MANO(S) NO DETECTADA(S)", (display_frame.shape[1]//2-200, display_frame.shape[0]//2),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)

        cv2.putText(display_frame, f"Capturando POSE '{sign_label}': {samples_captured_for_this_sign}/{NUM_SAMPLES_PER_SIGN}",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2, cv2.LINE_AA)
        cv2.imshow(f'Captura de Datos - {len(SIGNS_TO_COLLECT)} Palabras LSCh (DOS MANOS)', display_frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            print("Captura interrumpida."); cap.release(); cv2.destroyAllWindows(); exit()

    print(f"Recolección para la POSE de '{sign_label}' completada.")
    if samples_captured_for_this_sign < NUM_SAMPLES_PER_SIGN:
        print(f"Advertencia: Solo {samples_captured_for_this_sign}/{NUM_SAMPLES_PER_SIGN} para '{sign_label}'.")
    
    # Mostrar mensaje de completado para la seña actual antes de la pausa
    cv2.putText(display_frame, f"'{sign_label}' OK. Prepara siguiente.", (10,60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2, cv2.LINE_AA)
    cv2.imshow(f'Captura de Datos - {len(SIGNS_TO_COLLECT)} Palabras LSCh (DOS MANOS)', display_frame)
    cv2.waitKey(1500) # Pausa de 1.5 segundos para que el usuario se prepare

cap.release()
cv2.destroyAllWindows()

if all_collected_data:
    # Las columnas ahora son para TARGET_FEATURES_TWO_HANDS
    column_names = [f'feature_{i+1}' for i in range(TARGET_FEATURES_TWO_HANDS)] + ['label']
    df = pd.DataFrame(all_collected_data, columns=column_names)
    csv_full_path = os.path.join(DATA_PATH, CSV_FILENAME)
    df.to_csv(csv_full_path, index=False)
    print(f"\n¡Recolección de datos completada!")
    print(f"Datos guardados (SOBRESCRITOS SI EL ARCHIVO EXISTÍA) en: {csv_full_path}")
    print(f"Total de muestras recolectadas: {len(df)}")
    print(f"Se esperaban {TARGET_FEATURES_TWO_HANDS} características por muestra.")
    print("Distribución de las muestras:"); print(df['label'].value_counts())
else:
    print("\nNo se recolectaron datos.")
print("----------------------------------------------------")
print(f"Siguiente paso: Ejecutar 'train_model.py' para entrenar con estos datos (asegúrate que use {CSV_FILENAME}).")