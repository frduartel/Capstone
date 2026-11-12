# Product Backlog priorizado: SignIA

Fuente de requisitos del proyecto. Product Owner según el plan: Khaeil Parga. Joaquín actualiza documentalmente los estados al 9 de noviembre con las evidencias disponibles; esta actualización no acredita una Sprint Review formal ni una aprobación nueva del PO. El cierre de períodos y los pendientes P-01 a P-10 están en [roadmap](roadmap.md).

- **Prioridad:** MoSCoW (M = debe, S = debería, C = podría, W = no en esta versión).
- **Estimación:** puntos de historia, escala Fibonacci (1, 2, 3, 5, 8, 13).
- **Estado al cierre documental:** alcance efectivamente observado o probado y pendientes asociados. Estos estados no acreditan aceptación completa ni cambian la Definition of Done.
- **Sprint:** sprint planificado según el roadmap.

## Épicas

| ID | Épica | Objetivo de negocio |
| --- | --- | --- |
| EP-01 | Reconocimiento de señas | Detectar las manos y clasificar la seña con confianza medible |
| EP-02 | Traducción a texto y voz | Convertir las señas reconocidas en frases legibles y audibles |
| EP-03 | Cuentas y acceso | Proteger el acceso y diferenciar usuario y administrador |
| EP-04 | Administración y métricas | Gestionar la plataforma y medir su uso |
| EP-05 | Experiencia de usuario y accesibilidad | Interfaz clara, consistente y accesible |
| EP-06 | Despliegue en la nube | Aplicación disponible desde cualquier navegador |
| EP-07 | Calidad y pruebas | Asegurar que cada incremento funciona y es mantenible |
| EP-08 | Recursos de aprendizaje LSCh | Apoyar a quien quiere aprender LSCh |

## Historias de usuario

| ID | Épica | Historia de usuario | Prioridad | Puntos | Estado | Sprint |
| --- | --- | --- | --- | --- | --- | --- |
| HU-01 | EP-07 | Como desarrollador, quiero un entorno reproducible (Python 3.10 y dependencias fijadas) para ejecutar la app igual en cualquier equipo. | M | 3 | Entorno local ejecutado; portabilidad completa pendiente P-02 | 3 |
| HU-02 | EP-01 | Como persona sorda, quiero que la app detecte mis manos en la cámara para que pueda reconocer mis señas. | M | 5 | Detección observada HOLA/CASA; aceptación general pendiente P-08 | 3 |
| HU-03 | EP-06 | Como usuario, quiero que la cámara se capture desde mi navegador para usar la app sin instalar nada. | M | 8 | Cámara local observada; nube y latencia pendientes P-02/P-04/P-07 | 3 |
| HU-04 | EP-01 | Como persona sorda, quiero que la app reconozca la seña que hago y muestre su nivel de confianza para saber si me entendió. | M | 5 | Predicción estática observada; generalización pendiente P-03/P-08 | 4 |
| HU-05 | EP-01 | Como equipo, queremos capturar nuevas muestras y ampliar el vocabulario para reconocer más palabras. | S | 5 | 100 HOLA añadidas; ampliación de vocabulario pendiente P-03 | 4 |
| HU-06 | EP-01 | Como equipo, queremos reentrenar y evaluar el modelo con métricas (accuracy, F1 por clase, matriz de confusión) para medir su calidad. | M | 5 | Entrenamiento 1900 y métricas 75/25; evaluación por persona pendiente P-03 | 4 |
| HU-07 | EP-02 | Como persona sorda, quiero que las señas reconocidas formen una frase para comunicar una idea completa. | M | 3 | Acumulación Hola Casa observada; sin traducción gramatical | 5 |
| HU-08 | EP-02 | Como persona oyente, quiero escuchar la frase en voz alta para entender sin leer la pantalla. | M | 3 | Audio Hola Casa confirmado por Joaquín; requiere Internet | 5 |
| HU-09 | EP-02 | Como usuario, quiero limpiar la frase para empezar una nueva. | M | 1 | Limpieza de frase observada | 5 |
| HU-10 | EP-03 | Como visitante, quiero registrarme con usuario, correo y contraseña para tener mi cuenta. | M | 3 | Registro validado en AppTest; fallo de persistencia corregido | 3 |
| HU-11 | EP-03 | Como usuario, quiero iniciar y cerrar sesión de forma segura para proteger mi cuenta. | M | 3 | Sesiones verificadas en regresión; retorno manual pendiente P-02 | 3 |
| HU-12 | EP-03 | Como administrador, quiero que las contraseñas se guarden con un hash seguro y sin credenciales por defecto para proteger a los usuarios. | M | 3 | Hash con sal y verificación probados; sin auditoría completa | 3 |
| HU-13 | EP-04 | Como administrador, quiero activar, desactivar y cambiar el rol de usuarios para controlar el acceso. | S | 3 | Roles y desactivación verificados en regresión | 5 |
| HU-14 | EP-04 | Como administrador, quiero ver estadísticas de uso y de predicciones para conocer cómo se usa la app. | S | 5 | Persistencia local probada; exactitud de gráficos sin validar | 5 |
| HU-15 | EP-04 | Como administrador, quiero cargar un nuevo modelo y su escalador desde el panel para actualizar el reconocimiento sin tocar el código. | C | 3 | Par de modelos validado por función; file_uploader manual pendiente | 5 |
| HU-16 | EP-05 | Como usuario, quiero una interfaz consistente (colores, tipografía, íconos) para orientarme fácilmente. | S | 5 | Interfaz implementada; aceptación de diseño pendiente P-01 | 2, 5 |
| HU-17 | EP-05 | Como usuario, quiero instrucciones claras y retroalimentación (cámara activa, sin manos detectadas, baja confianza) para saber qué hacer. | S | 3 | Estados observados parcialmente; cobertura manual pendiente P-02/P-08 | 5 |
| HU-18 | EP-05 | Como usuario con baja visión, quiero textos grandes y buen contraste para leer la traducción. | S | 3 | Pendiente trasladado P-06 | 6 |
| HU-19 | EP-06 | Como equipo, queremos publicar la app en Streamlit Community Cloud para que el docente y los usuarios la prueben con una URL. | M | 5 | Pendiente trasladado P-04 | 4 |
| HU-20 | EP-07 | Como equipo, queremos pruebas unitarias de la extracción de landmarks, el modelo y la persistencia para detectar regresiones. | S | 5 | 31 regresiones históricas; suite integrada actual 27 pruebas correctas; revisión por compañero pendiente P-09 | 7 |
| HU-21 | EP-07 | Como equipo, queremos validar la app con usuarios reales y registrar sus observaciones para mejorarla. | S | 5 | Protocolo preparado; aceptación pendiente P-08 | 8 |
| HU-22 | EP-08 | Como aprendiz, quiero consejos, videos y enlaces de LSCh para aprender por mi cuenta. | C | 2 | Contenido implementado; validación lingüística pendiente P-08 | 5 |
| HU-23 | EP-02 | Como persona oyente, quiero hablar y que mi voz se transcriba a texto para responder a la persona sorda. | C | 8 | Opcional sin implementar; pendiente P-06 | 6 |
| HU-24 | EP-01 | Como persona sorda, quiero que se reconozcan señas con movimiento (por ejemplo "¿cómo estás?") para usar el vocabulario básico de una conversación. | S | 13 | Secuencias implementadas y modelo activado el 11/11; accuracy 80,6 %, F1 0,779; validación pendiente P-05 | 5 |
| HU-25 | EP-04 | Como administrador, quiero grabar señas nuevas, entrenar el modelo y activarlo desde la web para ampliar el vocabulario sin usar la terminal. | M | 8 | Capturas de secuencias, entrenamiento y activación del 11/11 acreditados; límites en anexo K | 4 |
| HU-26 | EP-06 | Como administrador, quiero que los usuarios, sesiones y predicciones se guarden en una base de datos en la nube para no perderlos cuando la app se reinicia. | M | 5 | Parquet/DuckDB locales probados; MotherDuck remoto pendiente P-04 | 6 |

## Criterios de aceptación de las historias prioritarias

**HU-03, captura desde el navegador**
- Dado un usuario con sesión iniciada, cuando presiona "Iniciar cámara", el navegador pide permiso y muestra la imagen en la página.
- Los landmarks se dibujan sobre la imagen y la predicción aparece en menos de 1 segundo.
- Funciona igual en local y desplegada en la nube.

**HU-06, evaluación del modelo**
- El entrenamiento genera accuracy, F1 por clase y matriz de confusión con división estratificada 75/25.
- Los resultados quedan registrados en `docs/fase2/sprints/sprint-4/`.
- El modelo y su escalador se guardan juntos y la app los carga sin errores.

**HU-12, seguridad de contraseñas**
- Las contraseñas nuevas se guardan con bcrypt o PBKDF2 con sal.
- La cuenta administradora inicial se crea con una contraseña tomada de una variable de entorno o de los secretos de Streamlit.

**HU-25, entrenamiento desde la web**
- El administrador graba muestras de una seña con la cámara del navegador, con cuenta regresiva y barra de avance, y puede guardarlas o descartarlas.
- Las muestras se agregan al dataset con el nombre de quien hace la seña y se respalda el dataset anterior.
- El entrenamiento muestra accuracy, F1 macro, detalle por seña y matriz de confusión, y avisa qué señas tienen bajo desempeño.
- El modelo nuevo solo reemplaza al actual cuando el administrador lo activa; el anterior queda respaldado y todas las sesiones lo cargan sin reiniciar la app.
- Se puede descargar un .zip con el dataset y el modelo para subirlos al repositorio.

**HU-24, señas con movimiento**
- El modelo analiza una secuencia de fotogramas (aproximadamente 1 segundo) en vez de una sola imagen.
- Se graban y reconocen al menos 5 frases básicas con movimiento (por ejemplo, "¿cómo estás?").
- Se mantiene el stack (MediaPipe y scikit-learn) y la grabación desde el panel de administrador.

**HU-19, despliegue**
- La app abre desde una URL pública con el modelo cargado.
- El README documenta los pasos para volver a desplegar.

## Definition of Done

Una historia está terminada cuando:
1. El código está en la rama `main` del repositorio, revisado por otro integrante.
2. Cumple todos sus criterios de aceptación.
3. Se probó manualmente en local (y en la nube si aplica) sin errores críticos.
4. La documentación asociada (README o docs del sprint) está actualizada.
5. Se presentó en la Sprint Review.
