# Prueba de humo de la versión 1.0

Prueba de humo hecha al inicio de la Fase 2 sobre la versión 1.0 (MVP local), antes de los cambios de los Sprints 3 y 4, para confirmar qué funciona y qué se debe corregir.

- **Fecha:** 2026-10-04
- **Entorno:** Windows 11, Python 3.10.22 (entorno conda en `.venv`), dependencias de `requirements.txt` (`pip check` sin conflictos)
- **Versión:** commit `910dda0` del repositorio SignIA-APT

## Resultados

| # | Caso de prueba | Resultado | Observación |
| --- | --- | --- | --- |
| 1 | Instalar dependencias en Python 3.10 | OK | MediaPipe 0.10.21 con `mp.solutions`, scikit-learn 1.6.1, OpenCV 4.11 |
| 2 | Cargar modelo SVC y escalador de dos manos | OK | 18 clases, 126 características; versiones de scikit-learn coinciden |
| 3 | Evaluar el modelo con la división 75/25 del entrenamiento | OK | Accuracy 98,7 %, F1 macro 0,987 |
| 4 | Iniciar la app (`streamlit run app/app_palabras.py`) | OK | Carga en `localhost` sin errores |
| 5 | Registrar un usuario nuevo | OK con observación | Se guarda, pero no muestra confirmación clara; al reenviar dice que ya existe |
| 6 | Iniciar sesión como usuario | OK | Abre el traductor; el token de sesión queda visible en la URL |
| 7 | Iniciar y detener la cámara | OK | Muestra el video y ejecuta predicciones (MediaPipe + SVC) |
| 8 | Generar voz con gTTS | OK | Requiere Internet |
| 9 | Iniciar sesión como administrador | OK | Usa la cuenta por defecto `admin` del código |
| 10 | Ver estadísticas de uso | OK con observación | Usuarios y sesiones se muestran; las predicciones no aparecen (error conocido de tabla y columnas) |

## Hallazgos para el backlog

| Hallazgo | Tipo | HU |
| --- | --- | --- |
| Botones blancos con texto casi invisible en el tema oscuro (formularios de acceso) | UX/UI | HU-16 |
| Sin mensaje de éxito claro tras el registro | UX/UI | HU-10, HU-17 |
| Token de sesión expuesto en la URL (`?lsch_auth_token=`) | Seguridad | HU-11, HU-12 |
| Contraseñas con SHA-256 sin sal y cuenta `admin/admin123` por defecto | Seguridad | HU-12 |
| Estadísticas de predicciones vacías | Error | HU-14 |
| La cámara se abre en el servidor (`cv2.VideoCapture`), no sirve en la nube | Arquitectura | HU-03 |
| Advertencia de scikit-learn por nombres de columnas en el escalador | Calidad | HU-20 |
| El 98,7 % se mide con fotogramas consecutivos de las mismas personas; la precisión con usuarios nuevos será menor | IA | HU-05, HU-06 |

## Conclusión

La versión 1.0 funciona de punta a punta en local. Los Sprints 3 y 4 se enfocan en la captura desde el navegador, la seguridad, la ampliación del dataset con más personas y una evaluación más realista del modelo.
