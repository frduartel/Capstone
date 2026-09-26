# Archivo: train_model.py
# (MODIFICADO PARA ENTRENAR CON DATOS DE DOS MANOS)
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC # O el modelo que prefieras
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns

# --- Configuración ---
DATA_PATH = "datos_señas_palabras_v1"
CSV_FILENAME = "datos_palabras_dos_manos.csv" # <--- USA EL NUEVO CSV de dos manos
CSV_FILE_PATH = os.path.join(DATA_PATH, CSV_FILENAME)

MODEL_SAVE_PATH = "modelos_entrenados_palabras_v1" # Carpeta para guardar modelos
MODEL_PKL_FILENAME = 'modelo_palabras_svc_dos_manos.pkl' # Nuevo nombre para el modelo
SCALER_PKL_FILENAME = 'scaler_palabras_dos_manos.pkl'   # Nuevo nombre para el scaler
CONFUSION_MATRIX_IMG_FILENAME = 'confusion_matrix_SVC_dos_manos.png' # Nuevo nombre para la imagen

if not os.path.exists(MODEL_SAVE_PATH):
    os.makedirs(MODEL_SAVE_PATH)
    print(f"Carpeta de modelos creada/verificada: {MODEL_SAVE_PATH}")

try:
    df = pd.read_csv(CSV_FILE_PATH)
except FileNotFoundError:
    print(f"Error Crítico: '{CSV_FILE_PATH}' no encontrado. Asegúrate de haber ejecutado 'capture_data.py' primero con la configuración correcta."); exit()
if df.empty: print("Error Crítico: El CSV está vacío."); exit()

print(f"Datos cargados desde '{CSV_FILENAME}'. Total muestras: {len(df)}")
print(f"Número de características detectadas (sin etiqueta): {df.shape[1] - 1}")
print("Distribución de clases:"); print(df['label'].value_counts())
print("----------------------------------------------------")

X = df.drop('label', axis=1); y = df['label']
if X.empty: print("Error Crítico: No hay características (X está vacío)."); exit()
print(f"Dimensiones de X (características): {X.shape}")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
print(f"Muestras entrenamiento: {len(X_train)}, Prueba: {len(X_test)}")

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("Características escaladas.")
print(f"Número de características después del escalado (esperado: {X_train_scaled.shape[1]}): {scaler.n_features_in_}")
print("----------------------------------------------------")

# Ajustar parámetros del modelo puede ser necesario, especialmente con más características.
# Considera aumentar 'C' si la complejidad del problema aumenta.
# Prueba también con otros kernels si 'rbf' no da buenos resultados (ej. 'linear', 'poly').
# El valor de 'C' (ej. 40) es un hiperparámetro. Podrías necesitar ajustarlo.
# Para datos de alta dimensionalidad, a veces un 'C' más bajo o 'gamma' más bajo puede ayudar a evitar el sobreajuste.
model_svc = SVC(kernel='rbf', C=30, gamma='scale', probability=True, random_state=42)
model_name_suffix = "SVC_dos_manos"

print(f"Entrenando el modelo {model_name_suffix} con datos de dos manos...")
model_svc.fit(X_train_scaled, y_train)
print(f"Modelo {model_name_suffix} entrenado.")
model_to_evaluate = model_svc # Selecciona el modelo a evaluar

print("----------------------------------------------------")
print(f"Evaluando el modelo: {model_name_suffix}")
y_pred_train = model_to_evaluate.predict(X_train_scaled)
train_accuracy = accuracy_score(y_train, y_pred_train) * 100
print(f"\nPrecisión ENTRENAMIENTO: {train_accuracy:.2f}%")

y_pred_test = model_to_evaluate.predict(X_test_scaled)
test_accuracy = accuracy_score(y_test, y_pred_test) * 100
print(f"Precisión PRUEBA: {test_accuracy:.2f}%") # ¡Esta es la crucial!

print("\nReporte de Clasificación (Prueba):")
# Obtener las clases del modelo entrenado para el reporte
class_names = model_to_evaluate.classes_
print(classification_report(y_test, y_pred_test, target_names=class_names, zero_division=0))

print("\nMatriz de Confusión (Prueba):")
cm = confusion_matrix(y_test, y_pred_test, labels=class_names)
plt.figure(figsize=(max(8, len(class_names)), max(6, len(class_names)*0.8))) # Ajustar tamaño dinámicamente
sns.heatmap(cm, annot=True, fmt='d', cmap='YlGnBu',
            xticklabels=class_names, yticklabels=class_names)
plt.xlabel('Predicción del Modelo')
plt.ylabel('Etiqueta Verdadera')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.title(f'Matriz de Confusión - {model_name_suffix}')
plt.tight_layout()
confusion_matrix_full_path = os.path.join(MODEL_SAVE_PATH, CONFUSION_MATRIX_IMG_FILENAME)
plt.savefig(confusion_matrix_full_path)
print(f"Matriz de confusión guardada en: {confusion_matrix_full_path}")
# plt.show() # Descomenta para verla al ejecutar, pero puede pausar el script

print("----------------------------------------------------")
model_full_path = os.path.join(MODEL_SAVE_PATH, MODEL_PKL_FILENAME)
scaler_full_path = os.path.join(MODEL_SAVE_PATH, SCALER_PKL_FILENAME)
joblib.dump(model_to_evaluate, model_full_path)
joblib.dump(scaler, scaler_full_path)
print(f"\nModelo entrenado y guardado (SOBRESCRITO) en: {model_full_path}")
print(f"Scaler guardado (SOBRESCRITO) en: {scaler_full_path}")
print("\nClases aprendidas por el modelo:", class_names)
print(f"El modelo espera {scaler.n_features_in_} características de entrada.")
print("----------------------------------------------------")
print(f"Entrenamiento completado. 'app_palabras.py' deberá cargar '{MODEL_PKL_FILENAME}' y '{SCALER_PKL_FILENAME}'.")