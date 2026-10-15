# Sprint 4: Modelo de reconocimiento (IA) y primera versión en la nube

| Campo | Detalle |
| --- | --- |
| Semanas | 7 y 8 (Fase 2) |
| Responsables | Franco Duarte, Khaeil Parga |
| Sprint Goal | Tener un modelo reentrenado con más personas, evaluado con métricas realistas, y la app publicada en una URL pública |
| Capacidad | 36 h (se agregaron 8 h por la HU-25, pedida por el equipo durante el sprint) |
| Historias | HU-04, HU-05, HU-06, HU-19, HU-25 |
| Estado | Herramientas listas; falta la captura con el equipo y la publicación en la nube |

## 1. Sprint Planning: Sprint Backlog

| ID | Tarea | HU | Responsable | Estimación (h) | Estado |
| --- | --- | --- | --- | --- | --- |
| T4.1 | Modificar `capture_data.py` para agregar muestras sin sobrescribir el CSV y registrar quién las graba | HU-05 | Khaeil Parga | 3 | Hecho |
| T4.2 | Capturar las 18 señas con los tres integrantes, con distinta luz y fondo | HU-05 | Equipo | 6 | Por hacer |
| T4.3 | Capturar al menos 4 señas nuevas (meta: 22 o más) | HU-05 | Equipo | 4 | Por hacer |
| T4.4 | Evaluación por persona: entrenar con dos integrantes y probar con el tercero | HU-06 | Khaeil Parga | 4 | Hecho (script; se activa al capturar por persona) |
| T4.5 | Reentrenar SVC y comparar con k-NN y Random Forest; registrar accuracy, F1 y matriz de confusión | HU-04, HU-06 | Franco Duarte | 5 | Hecho (comparación con el dataset actual) |
| T4.6 | Guardar el modelo y escalador elegidos y verificar que la app los carga | HU-04 | Franco Duarte | 2 | Por hacer |
| T4.7 | Preparar el repo para la nube: `requirements`, `packages.txt`, `.streamlit/config.toml` y secretos de ejemplo | HU-19 | Franco Duarte | 4 | Hecho |
| T4.8 | Publicar en Streamlit Community Cloud desde GitHub y configurar `st.secrets` | HU-19 | Franco Duarte | 3 | Por hacer |
| T4.9 | Probar la URL pública desde otro equipo y un celular | HU-19 | Joaquín González | 3 | Por hacer |
| T4.10 | Informe de métricas del modelo en `docs/fase2/sprints/sprint-4/` | HU-06 | Khaeil Parga | 2 | Hecho (línea base; se regenera tras capturar) |
| T4.11 | Página "Entrenar Modelo" en el panel admin: grabar con la cámara del navegador, entrenar, ver métricas, activar y descargar | HU-25 | Franco Duarte | 8 | Hecho |
| | **Total** | | | **44** | |

## 2. Scrumboard

| Por hacer | En curso | En revisión | Hecho |
| --- | --- | --- | --- |
| T4.2, T4.3, T4.6, T4.8, T4.9 | | | T4.1, T4.4, T4.5, T4.7, T4.10, T4.11 |

## 3. Burndown

| Día | D0 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Ideal | 44 | 39,6 | 35,2 | 30,8 | 26,4 | 22 | 17,6 | 13,2 | 8,8 | 4,4 | 0 |
| Real | | | | | | | | | | | |

## 4. Línea base del modelo (antes del sprint)

| Métrica | Valor | Comentario |
| --- | --- | --- |
| Clases | 18 | ABURRIDO a TE_QUIERO |
| Muestras | 1.800 | 100 por clase |
| Accuracy (prueba 25 %) | 98,7 % | Fotogramas de las mismas personas en entrenamiento y prueba |
| F1 macro | 0,987 | |
| Validación cruzada (5 particiones): SVC / k-NN / Random Forest | 0,993 / 0,990 / 0,991 | Ver `metricas_modelo.md` |
| División temporal (último 25 % de cada captura) | 1,000 | Más exigente que la aleatoria, pero misma sesión |
| Accuracy con una persona nueva | Por medir (T4.4) | Métrica realista que se usará para decidir |

Meta del sprint: accuracy ≥ 90 % y F1 macro ≥ 0,85 en la evaluación por persona.

## 5. Registro de dailies

| Día | Integrante | Qué hice | Qué haré | Impedimentos |
| --- | --- | --- | --- | --- |
| | | | | |

## 6. Sprint Review

- **Incremento entregado:**
- **URL pública:**
- **Métricas finales del modelo:**
- **Historias aceptadas por el PO:**
- **Cambios al Product Backlog:**

## 7. Retrospectiva

| Qué funcionó | Qué no funcionó | Acción de mejora |
| --- | --- | --- |
| | | |

## Riesgos del sprint

| Riesgo | Mitigación |
| --- | --- |
| MediaPipe 0.10.21 o `streamlit-webrtc` no instalan en la nube gratuita | Probar el despliegue temprano (día 2) con una app mínima |
| Memoria insuficiente en el plan gratuito | Modelo SVC liviano; cargar el modelo una sola vez con `st.cache_resource` |
| La precisión con personas nuevas es baja | Más muestras por persona y normalizar los landmarks respecto a la muñeca |
