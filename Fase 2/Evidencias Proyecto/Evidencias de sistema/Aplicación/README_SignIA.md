# SignIA

Traductor de Lengua de Señas Chilena (LSCh) a texto y voz. Proyecto APT (Capstone) de Ingeniería en Informática, Duoc UC sede Padre Alonso de Ovalle.

Equipo: Khaeil Parga (Product Owner), Franco Duarte (Scrum Master) y Joaquín González (Developer).

## Estructura

| Carpeta | Contenido |
| --- | --- |
| `app/` | Aplicación Streamlit: traductor, autenticación, panel de administración |
| `ml/` | Captura de muestras, entrenamiento, evaluación, datasets y modelos entrenados |
| `tests/` | Pruebas unitarias (`python -m unittest discover -s tests`) |
| `docs/fase1/` | Evidencias de la Fase 1 |
| `docs/fase2/` | Artefactos ágiles: visión, backlog, mapas, arquitectura, sprints e impedimentos |
| `docs/fase3/` | Cierre e informe final |

## Ejecutar en local

Requiere Python 3.10 de 64 bits. Con Anaconda:

```powershell
& "C:\ProgramData\anaconda3\Scripts\conda.exe" create -y -p .\.venv python=3.10
.\.venv\python.exe -m pip install -r requirements.txt
copy .streamlit\secrets.toml.example .streamlit\secrets.toml   # y define ADMIN_PASSWORD
.\.venv\python.exe -m streamlit run app/app_palabras.py
```

La guía completa (instalación sin Anaconda, guion de demo, reentrenamiento y despliegue en Streamlit Community Cloud) está en [`docs/GUIA_EJECUCION_Y_DEMO.md`](docs/GUIA_EJECUCION_Y_DEMO.md).

## Estado por sprint

| Sprint | Estado | Evidencia |
| --- | --- | --- |
| 1. Documentación y definición | Cerrado | `docs/fase2/01_vision`, `02_backlog`, `03_mapas` |
| 2. Arquitectura y diseño | Cerrado (mockups pasan al 3) | `docs/fase2/04_arquitectura` |
| 3. Entorno base y captura de video | Código terminado | Cámara del navegador, seguridad, `tests/` |
| 4. Modelo de reconocimiento | Entrenamiento desde el panel admin listo; falta capturar con el equipo y publicar | Página *Entrenar Modelo*, `ml/evaluate_model.py`, `metricas_modelo.md` |

Los usuarios, sesiones y predicciones se guardan en `data/` (ignorado por git).
