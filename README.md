# SignIA — Reconocimiento de señas a texto y voz

Proyecto de capstone desarrollado por Kael, Joaquín y Franco. Reconoce un conjunto de palabras o poses de Lengua de Señas Chilena (LSCh) mediante una cámara web, muestra las predicciones como texto y permite escuchar la frase formada.

Es un prototipo de reconocimiento de poses de las manos: no interpreta de forma general conversaciones completas ni modela secuencias de movimiento. Su vocabulario depende del modelo entrenado.

## 1. Requisitos previos

- Windows de 64 bits y **Python 3.10 de 64 bits**.
- Cámara web disponible y permisos de cámara habilitados para aplicaciones de escritorio.
- Navegador web y parlantes o audífonos.
- Conexión a Internet para instalar las dependencias y generar voz con gTTS.
- Una copia completa del código, el archivo `requirements.txt` y los archivos del modelo y su escalador, o el CSV necesario para entrenar ambos.

La configuración actual usa `cv2.CAP_DSHOW`, un backend de cámara de Windows. Esta guía está orientada a ejecutar todo localmente en ese sistema. Al abrir la aplicación desde otro equipo, OpenCV sigue usando la cámara del equipo donde corre Python; no captura automáticamente la cámara del navegador remoto.

## 2. Organización de archivos

Coloca `README.md` y `requirements.txt` en la carpeta principal `sign_ai`, junto a `app_palabras.py`. Conserva exactamente los nombres de las carpetas, incluida la `ñ` de `datos_señas_palabras_v1`.

| Ruta relativa a `sign_ai` | Función |
| --- | --- |
| `README.md` | Esta guía |
| `requirements.txt` | Dependencias y versiones propuestas |
| `app_palabras.py` | Aplicación Streamlit |
| `auth.py` | Autenticación y control de acceso |
| `auth_forms.py` | Formularios de acceso y registro |
| `token_manager.py` | Gestión de sesiones |
| `utils.py` | Persistencia de datos y consultas DuckDB |
| `capture_data.py` | Captura de muestras de señas |
| `train_model.py` | Entrenamiento y evaluación del modelo |
| `listar_voces.py` | Utilidad independiente para listar voces del sistema |
| `modelos_entrenados_palabras_v1/modelo_palabras_svc_dos_manos.pkl` | Clasificador utilizado por la aplicación |
| `modelos_entrenados_palabras_v1/scaler_palabras_dos_manos.pkl` | Escalador correspondiente al clasificador |
| `datos_señas_palabras_v1/datos_palabras_dos_manos.csv` | Datos usados por el entrenamiento actual |
| `data/` | Archivos Parquet de usuarios, sesiones y predicciones |

La aplicación inicializa `data/users.parquet` y `data/sessions.parquet` si no existen. No es necesario instalar un servidor de base de datos: DuckDB consulta los archivos locales.

Los archivos `modelo_palabras_svc.pkl` y `datos_palabras_hola_tequiero_bien.csv` pertenecen a otra variante y no son los seleccionados por la configuración actual.

> Para usar el modelo existente necesitas **el modelo y su escalador del mismo entrenamiento**. El escalador de dos manos no se incluyó entre los archivos revisados para preparar esta guía. Consíguelo del proyecto original o genera una nueva pareja siguiendo la sección 6. No mezcles el modelo original con un escalador de otra ejecución.

## 3. Instalación en Windows

Abre PowerShell en la carpeta `sign_ai`. Puedes abrirla en el Explorador de archivos, escribir `powershell` en la barra de direcciones y presionar Enter.

Comprueba que Python 3.10 está disponible:

```powershell
py -3.10 --version
py -3.10 -c "import struct; print(struct.calcsize('P') * 8)"
```

El primer comando debe mostrar `Python 3.10.x`; el segundo, `64`. Si `py` no se reconoce, revisa la instalación de Python y su lanzador de Windows.

Crea un entorno virtual dentro del proyecto:

```powershell
py -3.10 -m venv .venv
```

Instala las dependencias y revisa su consistencia:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
```

`pip check` debería mostrar `No broken requirements found.`. Los comandos de esta guía usan directamente el Python del entorno virtual, por lo que no es necesario activar `.venv` ni cambiar la política de ejecución de PowerShell.

Cada integrante debe crear su propio entorno virtual. Comparte el código y `requirements.txt`, no la carpeta `.venv`.

### Dependencias utilizadas

| Componente | Librerías principales |
| --- | --- |
| Interfaz | Streamlit y Plotly |
| Cámara y detección de manos | opencv-contrib-python, MediaPipe y NumPy |
| Clasificación y escalado | scikit-learn y joblib |
| Datos y almacenamiento | pandas, DuckDB y PyArrow |
| Voz de la aplicación | gTTS |
| Gráficos del entrenamiento | Matplotlib y seaborn |
| Listado de voces locales | pyttsx3 |

El código utiliza un clasificador SVC; **no requiere TensorFlow ni Keras**. `opencv-contrib-python` proporciona el módulo `cv2` y es requerido por MediaPipe: no instales además `opencv-python` ni variantes `headless` en este entorno. La captura utiliza ventanas de OpenCV.

`requirements.txt` también fija `jax` y `jaxlib`, dependencias transitivas de MediaPipe. `pip` instala las demás dependencias transitivas automáticamente; por eso aparecerán más paquetes que los enumerados directamente en el archivo.

## 4. Iniciar la aplicación

Desde la carpeta principal, ejecuta:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app_palabras.py
```

Abre en el navegador la dirección **Local URL** que muestre la terminal. Mantén esa terminal abierta mientras uses la aplicación. Para detener el servidor, vuelve a ella y presiona `Ctrl+C`.

Ejecuta siempre los comandos desde `sign_ai`: las rutas de modelos, datos y archivos Parquet son relativas a la carpeta de trabajo.

### Primer acceso y roles

1. Abre la pestaña **Registrarse** y crea una cuenta para probar el traductor. El formulario requiere usuario de al menos 4 caracteres, correo y contraseña de al menos 8 caracteres.
2. Inicia sesión con esa cuenta. Los registros normales reciben el rol `user`.
3. Usa una cuenta `user` para la traducción. La cuenta `admin` abre el panel administrativo.

En una instalación nueva, el código crea una cuenta de demostración con usuario **`admin`** y contraseña **`admin123`**, si no existe un usuario llamado `admin`. Si recibiste archivos `data/` ya poblados, esa contraseña podría ser distinta. Estas credenciales están definidas en `utils.py` y deben sustituirse antes de publicar el proyecto; la interfaz actual no incluye un flujo de cambio de contraseña.

El administrador puede gestionar roles y activación de usuarios, consultar estadísticas, cargar archivos de modelo y escalador y ejecutar consultas SQL. Para una prueba de lectura del panel SQL:

```sql
SELECT username, role, active FROM users LIMIT 10;
```

## 5. Usar el traductor

1. Inicia sesión con una cuenta de usuario normal.
2. Accede a **Traductor en Vivo** o **ENTRAR AL TRADUCTOR**, según la pantalla visible.
3. Presiona **Iniciar Cámara**.
4. Coloca las manos completas frente a la cámara, con buena iluminación, y realiza una pose incluida en el vocabulario del modelo.
5. Observa la predicción y su confianza. Las predicciones que superan el umbral configurado se incorporan a **Frase Generada**.
6. Presiona **Detener Cámara** antes de reproducir o limpiar la frase.
7. Presiona **Escuchar Frase** y usa el reproductor de audio mostrado. La generación de voz requiere Internet.
8. Usa **Limpiar Frase** para comenzar otra frase y **Cerrar Sesión** para salir.

La aplicación muestra las clases cargadas desde el modelo. Esa lista es la referencia efectiva del vocabulario; algunos textos de bienvenida tienen listas escritas manualmente que pueden diferir.

La configuración actual muestra predicciones con confianza desde `0.55` y considera añadir palabras desde `0.70`, con controles para reducir repeticiones. Estas puntuaciones no garantizan una traducción correcta. Usa poses consistentes con las muestras de entrenamiento.

`listar_voces.py` es una utilidad separada:

```powershell
.\.venv\Scripts\python.exe listar_voces.py
```

Lista voces instaladas en el sistema mediante pyttsx3. No cambia la voz de gTTS usada por la aplicación.

## 6. Entrenar a partir del CSV existente

No necesitas volver a capturar datos si ya tienes el CSV correcto. Colócalo en:

`datos_señas_palabras_v1/datos_palabras_dos_manos.csv`

El entrenamiento espera una columna `label` y 126 columnas de características: 21 puntos por mano, 3 coordenadas por punto y espacio para 2 manos. En la extracción, una mano ausente se representa con ceros.

> Antes de entrenar, respalda la carpeta `modelos_entrenados_palabras_v1`: el script sobrescribe los archivos de salida del mismo nombre.

Con la aplicación detenida, ejecuta:

```powershell
.\.venv\Scripts\python.exe train_model.py
```

El script divide los datos en entrenamiento (75 %) y prueba (25 %) de forma estratificada, ajusta un `StandardScaler`, entrena un SVC y muestra métricas en la terminal. Genera estos archivos en `modelos_entrenados_palabras_v1/`:

- `modelo_palabras_svc_dos_manos.pkl`
- `scaler_palabras_dos_manos.pkl`
- `confusion_matrix_SVC_dos_manos.png`

Conserva juntos el modelo y el escalador generados en esa ejecución. Reinicia Streamlit para cargar la nueva pareja: la aplicación conserva los objetos cargados en su estado de sesión.

## 7. Capturar nuevas muestras

Esta sección es opcional si solo quieres ejecutar el traductor con los archivos existentes.

1. Cierra el traductor y otras aplicaciones que utilicen la cámara.
2. Respalda el CSV existente: `capture_data.py` sobrescribe `datos_palabras_dos_manos.csv` al finalizar; no añade muestras al archivo anterior.
3. Revisa `SIGNS_TO_COLLECT` en `capture_data.py` y define las palabras que quieres capturar. `NUM_SAMPLES_PER_SIGN` está configurado en 100.
4. Ejecuta el script:

```powershell
.\.venv\Scripts\python.exe capture_data.py
```

5. Sigue la palabra indicada en la terminal. Con la ventana de cámara enfocada, presiona **s** para iniciar las muestras de esa pose.
6. Repite el proceso para todas las palabras y espera a que termine para guardar el CSV.
7. Ejecuta el entrenamiento de la sección 6.

La tecla **q** termina la captura. En el código actual, salir con `q` interrumpe el programa antes de guardar las muestras acumuladas. Completa la captura para conservarlas.

Las muestras corresponden a poses por fotograma. Añadir una palabra que requiere movimiento no convierte al clasificador en un modelo temporal.

## 8. Problemas frecuentes

| Problema | Qué revisar |
| --- | --- |
| No se encuentra `requirements.txt` o `app_palabras.py` | Abre la terminal en `sign_ai`, no dentro de `data` ni de la carpeta de modelos. |
| `ModuleNotFoundError` | Instala y ejecuta con `.\.venv\Scripts\python.exe` para utilizar el mismo entorno. |
| No existe una distribución compatible al instalar | Comprueba Python 3.10 y arquitectura de 64 bits. Usa un entorno nuevo con el archivo de dependencias completo. |
| `mediapipe` no tiene `solutions` | Verifica que estás usando el entorno con `mediapipe==0.10.21`. No actualices MediaPipe de forma aislada. |
| No se encuentran el modelo o el escalador | Revisa los nombres y rutas de la sección 2. Deben estar ambos; si falta el escalador, obtén el original o reentrena la pareja. |
| El escalador espera 63 características | Se está usando una variante de una mano. La configuración actual necesita la pareja de dos manos y 126 características. |
| Advertencia de versión al cargar un `.pkl` | Los dos clasificadores revisados registran scikit-learn `1.6.1`. Conserva esa versión y verifica también la del escalador original. |
| No se puede abrir la cámara | Cierra otras aplicaciones, revisa permisos y conexión. El código usa la cámara de índice `0`; otro dispositivo puede requerir cambiarlo en ambos scripts que capturan video. |
| No se genera audio | Revisa conexión a Internet y el mensaje de gTTS. Para oírlo, utiliza el reproductor del navegador y revisa el volumen. |
| No aparecen usuarios o no se guardan cambios | Revisa los errores de la terminal, permisos de escritura en `data/` y la instalación de PyArrow. |
| El puerto está ocupado | Detén otra instancia o añade `--server.port 8502` al comando de inicio. |

### Detalles del código pendientes de corregir

Estos comportamientos no se resuelven cambiando las versiones de las librerías:

- **Sesiones al recargar:** en `utils.py`, `load_data()` convierte `expires_at` usando por error la columna `created_at`. Esto puede invalidar una sesión al restaurarla. La conversión debe usar la propia columna `expires_at`.
- **Registro de usuarios:** `auth_forms.py` intenta limpiar valores de widgets mediante `st.session_state` después de crearlos. Streamlit puede mostrar un error aunque el usuario ya haya sido guardado. Si sucede, prueba iniciar sesión con la cuenta creada antes de repetir el registro.
- **Estadísticas de predicciones:** el guardado usa `predictions` y la columna `sign`, pero la vista estadística busca `predictions_log` y `predicted_sign`. Además, falta el esquema de predicciones en `utils.COLUMNS_MAP` y el guardado actual reemplaza el archivo con cada predicción. El historial requiere corregir estos puntos para funcionar como registro acumulado.

Esta guía documenta el código recibido; no aplica esas correcciones.

## 9. Compatibilidad comprobada

- Se revisaron los ocho scripts del proyecto y las capturas de su estructura.
- Los dos clasificadores adjuntos contienen el metadato `_sklearn_version = "1.6.1"`, correspondiente a la versión con que se guardaron. `train_model.py` guarda el modelo inmediatamente después de entrenarlo.
- La resolución de dependencias propuesta terminó sin conflictos para Python 3.10 en Windows x86-64. Esto comprueba compatibilidad declarada de paquetes, no una prueba completa del funcionamiento de la aplicación.
- Las otras versiones fijadas son una combinación propuesta; no se recuperaron del entorno original.
- No se verificó el escalador original ni se probó la aplicación con una cámara física durante la preparación de esta guía.

Para compartir el proyecto, incluye el código, `requirements.txt`, esta guía y la pareja correcta de modelo/escalador. El CSV es necesario si el equipo va a reentrenar. Los archivos `data/users.parquet` y `data/sessions.parquet` contienen cuentas y sesiones locales; cada integrante puede iniciar con una carpeta `data/` nueva.
