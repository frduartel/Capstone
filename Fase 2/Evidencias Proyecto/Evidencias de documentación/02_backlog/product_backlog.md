# Product Backlog priorizado: SignIA

Única fuente de requisitos del proyecto. Lo mantiene el Product Owner (Khaeil Parga) y se refina en cada Sprint Review.

- **Prioridad:** MoSCoW (M = debe, S = debería, C = podría, W = no en esta versión).
- **Estimación:** puntos de historia, escala Fibonacci (1, 2, 3, 5, 8, 13).
- **Estado:** Hecho (implementado y verificado), Por hacer, En curso.
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
| HU-01 | EP-07 | Como desarrollador, quiero un entorno reproducible (Python 3.10 y dependencias fijadas) para ejecutar la app igual en cualquier equipo. | M | 3 | Hecho | 3 |
| HU-02 | EP-01 | Como persona sorda, quiero que la app detecte mis manos en la cámara para que pueda reconocer mis señas. | M | 5 | Hecho | 3 |
| HU-03 | EP-06 | Como usuario, quiero que la cámara se capture desde mi navegador para usar la app sin instalar nada. | M | 8 | Hecho (falta probar en la nube) | 3 |
| HU-04 | EP-01 | Como persona sorda, quiero que la app reconozca la seña que hago y muestre su nivel de confianza para saber si me entendió. | M | 5 | Hecho | 4 |
| HU-05 | EP-01 | Como equipo, queremos capturar nuevas muestras y ampliar el vocabulario para reconocer más palabras. | S | 5 | Herramienta lista | 4 |
| HU-06 | EP-01 | Como equipo, queremos reentrenar y evaluar el modelo con métricas (accuracy, F1 por clase, matriz de confusión) para medir su calidad. | M | 5 | Hecho (línea base) | 4 |
| HU-07 | EP-02 | Como persona sorda, quiero que las señas reconocidas formen una frase para comunicar una idea completa. | M | 3 | Hecho | 5 |
| HU-08 | EP-02 | Como persona oyente, quiero escuchar la frase en voz alta para entender sin leer la pantalla. | M | 3 | Hecho | 5 |
| HU-09 | EP-02 | Como usuario, quiero limpiar la frase para empezar una nueva. | M | 1 | Hecho | 5 |
| HU-10 | EP-03 | Como visitante, quiero registrarme con usuario, correo y contraseña para tener mi cuenta. | M | 3 | Hecho | 3 |
| HU-11 | EP-03 | Como usuario, quiero iniciar y cerrar sesión de forma segura para proteger mi cuenta. | M | 3 | Hecho | 3 |
| HU-12 | EP-03 | Como administrador, quiero que las contraseñas se guarden con un hash seguro y sin credenciales por defecto para proteger a los usuarios. | M | 3 | Hecho | 3 |
| HU-13 | EP-04 | Como administrador, quiero activar, desactivar y cambiar el rol de usuarios para controlar el acceso. | S | 3 | Hecho | 5 |
| HU-14 | EP-04 | Como administrador, quiero ver estadísticas de uso y de predicciones para conocer cómo se usa la app. | S | 5 | Hecho | 5 |
| HU-15 | EP-04 | Como administrador, quiero cargar un nuevo modelo y su escalador desde el panel para actualizar el reconocimiento sin tocar el código. | C | 3 | Hecho | 5 |
| HU-16 | EP-05 | Como usuario, quiero una interfaz consistente (colores, tipografía, íconos) para orientarme fácilmente. | S | 5 | Hecho | 2, 5 |
| HU-17 | EP-05 | Como usuario, quiero instrucciones claras y retroalimentación (cámara activa, sin manos detectadas, baja confianza) para saber qué hacer. | S | 3 | Hecho | 5 |
| HU-18 | EP-05 | Como usuario con baja visión, quiero textos grandes y buen contraste para leer la traducción. | S | 3 | Por hacer | 6 |
| HU-19 | EP-06 | Como equipo, queremos publicar la app en Streamlit Community Cloud para que el docente y los usuarios la prueben con una URL. | M | 5 | Por hacer | 4 |
| HU-20 | EP-07 | Como equipo, queremos pruebas unitarias de la extracción de landmarks, el modelo y la persistencia para detectar regresiones. | S | 5 | En curso (9 pruebas) | 7 |
| HU-21 | EP-07 | Como equipo, queremos validar la app con usuarios reales y registrar sus observaciones para mejorarla. | S | 5 | Por hacer | 8 |
| HU-22 | EP-08 | Como aprendiz, quiero consejos, videos y enlaces de LSCh para aprender por mi cuenta. | C | 2 | Hecho | 5 |
| HU-23 | EP-02 | Como persona oyente, quiero hablar y que mi voz se transcriba a texto para responder a la persona sorda. | C | 8 | Por hacer | 6 |
| HU-24 | EP-01 | Como persona sorda, quiero que se reconozcan señas con movimiento (por ejemplo "¿cómo estás?") para usar el vocabulario básico de una conversación. | S | 13 | Por hacer | 5 |
| HU-25 | EP-04 | Como administrador, quiero grabar señas nuevas, entrenar el modelo y activarlo desde la web para ampliar el vocabulario sin usar la terminal. | M | 8 | Hecho | 4 |
| HU-26 | EP-06 | Como administrador, quiero que los usuarios, sesiones y predicciones se guarden en una base de datos en la nube para no perderlos cuando la app se reinicia. | M | 5 | En curso | 6 |

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
