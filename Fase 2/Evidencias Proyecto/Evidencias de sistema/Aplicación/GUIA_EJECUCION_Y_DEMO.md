# Guía de ejecución y demostración: SignIA

Pasos para instalar, correr y mostrar SignIA en clases. Todos los comandos se ejecutan en **PowerShell**, dentro de la carpeta del proyecto (`SignIA-APT`).

## 1. Instalación (solo la primera vez)

Requiere Python 3.10 de 64 bits. Hay dos caminos; usa el que tengas.

**A. Con Anaconda** (el equipo de Franco ya quedó listo así)

```powershell
& "C:\ProgramData\anaconda3\Scripts\conda.exe" create -y -p .\.venv python=3.10
.\.venv\python.exe -m pip install -r requirements.txt
```

**B. Con Python 3.10 instalado desde python.org**

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

> Con Anaconda el ejecutable es `.\.venv\python.exe`; con python.org es `.\.venv\Scripts\python.exe`. En el resto de la guía se usa `.\.venv\python.exe`; cámbialo si usaste el camino B.

**Contraseña del administrador.** Copia `.streamlit\secrets.toml.example` como `.streamlit\secrets.toml` y define `ADMIN_PASSWORD`. La primera vez que corre la app se crea el usuario `admin` con esa contraseña. Este archivo no se sube a GitHub.

## 2. Correr la aplicación

```powershell
.\.venv\python.exe -m streamlit run app/app_palabras.py
```

Se abre el navegador en `http://localhost:8501`. Para detener la app, vuelve a PowerShell y presiona `Ctrl+C`.

## 3. Guion para la demo en clases (unos 5 minutos)

1. **Registro (Sprint 3).** Pestaña *Crear cuenta*: crea un usuario. Muestra el mensaje de éxito y que el formulario se limpia.
2. **Inicio de sesión.** Entra con ese usuario. En *Inicio* presiona **Empezar a traducir** (o usa el menú lateral).
3. **Traductor con la cámara del navegador (Sprint 3).** Deja seleccionado *Navegador*, presiona **Encender cámara** y acepta el permiso. Si se abre otra cámara, usa **Elegir cámara**. Explica que así funcionará en la nube: el navegador envía el video y el servidor reconoce la seña.
4. **Reconocimiento (Sprint 4).** Haz 2 o 3 señas del vocabulario (por ejemplo HOLA, TE_QUIERO, CASA). Muestra la tarjeta *Seña detectada* con su barra de confianza y cómo se arma la frase.
5. **Voz.** Presiona **Detener** y luego **Escuchar**: la frase se lee en voz alta. Requiere Internet.
6. **Panel de administración.** Cierra sesión y entra como `admin`. Muestra *Usuarios* y *Estadísticas* (pestaña *Predicciones*: señas más usadas y confianza promedio).
7. **Enseñar una seña nueva (Sprint 4).** En *Entrenar*, graba una seña nueva, entrena, muestra las métricas y actívala. Abre *Traductor* y muestra que ya la reconoce.
8. **Métricas del modelo (Sprint 4).** Abre `docs/fase2/sprints/sprint-4/metricas_modelo.md` y explica la diferencia entre la exactitud con datos conocidos y la evaluación con una persona nueva.
9. **Evidencias ágiles.** Recorre `docs/fase2/` en GitHub: visión, backlog, roadmap, mapas, arquitectura, sprints e impedimentos.

**Plan B si la cámara del navegador falla** (red de la universidad o permisos): selecciona *Este equipo*, elige la cámara y presiona **Encender**. Funciona porque la app corre en el mismo computador.

**Consejos para que reconozca bien:** buena luz de frente, manos completas dentro del cuadro, fondo simple y poses quietas parecidas a las del entrenamiento.

## 4. Pruebas y métricas

```powershell
# Pruebas unitarias (contraseñas, frase, modelo y procesamiento de video)
.\.venv\python.exe -m unittest discover -s tests -v

# Informe de métricas del modelo
.\.venv\python.exe ml/evaluate_model.py
```

## 5. Ampliar el dataset y reentrenar (Sprint 4)

### Desde la web (recomendado)

1. Entra como `admin` y abre **Entrenar** en el menú lateral.
2. Pestaña **1. Grabar señas**: presiona **Encender cámara**, escribe el nombre de la seña (por ejemplo `GRACIAS`) y quién la hace, y presiona **Grabar**. Tienes 3 segundos para poner la seña y mantenerla quieta mientras se graban las muestras. Revisa y presiona **Guardar**.
3. Repite con cada seña nueva y con cada integrante, con distinta luz y ropa.
4. Pestaña **2. Entrenar y activar**: presiona **Entrenar modelo**. Revisa la exactitud y las señas con bajo desempeño; si están bien, presiona **Activar este modelo en el traductor**. El traductor lo usa de inmediato y el modelo anterior queda respaldado.
5. Pestaña **Dataset**: muestra cuántas muestras hay por seña y por persona, permite borrar una seña mal grabada y descargar un .zip con el dataset y el modelo. En la nube, descarga ese .zip y súbelo al repositorio, porque los archivos se borran al reiniciar la app.

El modelo reconoce poses quietas. Para una seña con movimiento, graba la pose más característica; el reconocimiento de movimiento está planificado para el Sprint 5 (HU-24).

### Desde la terminal

Cada integrante captura sus propias muestras; se **agregan** al CSV y se guarda un respaldo.

```powershell
# Todas las señas, 100 muestras cada una
.\.venv\python.exe ml/capture_data.py --persona franco

# Solo algunas señas o señas nuevas
.\.venv\python.exe ml/capture_data.py --persona khaeil --senas HOLA,CASA,GRACIAS --muestras 80
```

En la ventana de la cámara, presiona **s** para empezar cada seña y **q** para terminar antes (lo capturado se guarda igual). Después:

```powershell
.\.venv\python.exe ml/train_model.py      # reentrena y reemplaza modelo y escalador
.\.venv\python.exe ml/evaluate_model.py   # actualiza el informe, con evaluación por persona
```

Reinicia la app para que cargue el modelo nuevo.

## 6. Publicar en Streamlit Community Cloud (gratis)

1. Sube el repositorio a GitHub (debe incluir `requirements.txt` y `packages.txt`).
2. Entra a https://share.streamlit.io con tu cuenta de GitHub y elige **Create app**.
3. Repositorio: `SignIA-APT`, rama `main`, archivo principal `app/app_palabras.py`.
4. En **Advanced settings**: Python **3.10**; en **Secrets** pega `ADMIN_PASSWORD = "..."` y `MOTHERDUCK_TOKEN = "..."` (token de app.motherduck.com, en *Settings > Access tokens*).
5. Presiona **Deploy**. La primera instalación tarda varios minutos.

Con `MOTHERDUCK_TOKEN` los usuarios, sesiones y predicciones quedan guardados en MotherDuck; sin él se borran cuando la app se reinicia (disco temporal). Los modelos entrenados desde el panel también se borran: descarga el .zip y súbelo al repositorio. La app se suspende si nadie la usa por varios días. En algunas redes la cámara del navegador necesita un servidor TURN; se configura en *Secrets* con la sección `[turn]` del archivo de ejemplo.

## 7. Problemas frecuentes

| Problema | Solución |
| --- | --- |
| `No module named ...` | Usa siempre `.\.venv\python.exe`, no `python` a secas |
| La cámara del navegador queda en negro | Revisa el permiso de cámara del navegador (ícono del candado) o usa la cámara local |
| *No se pudo acceder a la cámara web* (modo local) | Cierra Zoom, Teams u otra app que use la cámara |
| No puedo entrar como admin | Revisa `ADMIN_PASSWORD` en `.streamlit\secrets.toml`. Si el admin ya existía, borra la carpeta `data\` para recrearlo (se borran los usuarios locales) |
| No suena la frase | gTTS necesita Internet |
| El puerto está ocupado | Agrega `--server.port 8502` al comando |
