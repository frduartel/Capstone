## Actualización vigente al 11 de noviembre de 2026

HU-24 tiene implementación de secuencias y entrenamiento real, integrados desde la rama de Franco. Se activó el modelo de Joaquín: 60 clases, accuracy 80,6 % y F1 macro 0,779, con 527 clips seleccionados y datos estáticos. Las pruebas tienen soporte para 57 clases. El anexo K del informe 2.6 conserva resultados y límites. Pasaron 27 pruebas de integración; no se ejecutó aceptación humana completa del modelo activado.

P-05 cambia de implementación pendiente a validación pendiente del reconocimiento de secuencias. P-09 tiene ahora un commit publicado de código y modelo (SIGNIA 0cc3a4d), pero la revisión por otro integrante no se presume. Continúan pendientes REPOSO (omitido por Joaquín), depuración de alias, vocabulario omitido, calidad objetivo y aceptación independiente. Los apartados con corte al 9 de noviembre se conservan como antecedente histórico del cierre documental.

# Roadmap y cierre documental de SignIA

## Cierre vigente de la entrega local al 9 de noviembre de 2026

Cierre documental de los ocho sprints para la entrega local de Fase 2, solicitado por Joaquín el 9 de noviembre de 2026. Cada período se registra como cerrado con el alcance demostrado; lo incompleto permanece en el backlog P-01 a P-10. Cerrar el período no convierte esas historias en Hecho ni sustituye su Definition of Done.

El cierre es documental y operativo para preparar la presentación local. La aceptación formal del PO/docente y los criterios pendientes se conservan abiertos. La Definition of Done histórica se mantiene: revisión por otro integrante, criterios satisfechos, pruebas, documentación y Sprint Review. La declaración general de participación no acredita por sí sola cada requisito.

| Sprint | Alcance | Estado del período | Seguimiento |
| --- | --- | --- | --- |
| 1 | Definición y planificación | Cerrado documentalmente | Histórico |
| 2 | Arquitectura y diseño | Cerrado documentalmente | P-01 |
| 3 | Entorno y cámara del navegador | Cerrado documentalmente | P-02 |
| 4 | Dataset y entrenamiento | Cerrado documentalmente | P-03, P-04 |
| 5 | Reconocimiento e interfaz | Cerrado documentalmente | P-03, P-05, P-08 |
| 6 | Voz y almacenamiento | Cerrado documentalmente | P-04, P-06 |
| 7 | Integración y pruebas | Cerrado documentalmente | P-09 |
| 8 | Pruebas manuales y entrega | Cerrado documentalmente | P-07, P-08, P-10 |

### Sprint 1 Definición y planificación

**Resultado:** Visión, backlog, mapas, definición y entregables de Fase 1 disponibles. El registro histórico ya declaraba cierre retroactivo.

**Pendientes trasladados:** Los objetivos y requisitos originales se conservan; no se reconstruyen horas ni reuniones.

### Sprint 2 Arquitectura y diseño

**Resultado:** Arquitecturas actual y objetivo, modelo lógico de datos y sistema de diseño documentados en anexos C, D y E.

**Pendientes trasladados:** Mockups Figma y aceptación específica del diseño no acreditados; trasladados a P-01.

### Sprint 3 Entorno y cámara del navegador

**Resultado:** Cámara y controles observados el 9 de noviembre; registro, acceso, roles y sesiones verificados mediante AppTest. Bloqueo de PyAV resuelto reinstalando la misma versión.

**Pendientes trasladados:** Matriz Chrome/Edge/otros equipos y retorno ocasional al acceso pendientes: P-02.

### Sprint 4 Dataset y entrenamiento

**Resultado:** Joaquín añadió 100 HOLA: 1.900 muestras y 18 clases. Entrenamiento 1.425/prueba 475; accuracy 98,7 % y F1 macro 0,987. Activación y recuperación del par probadas.

**Pendientes trasladados:** No hubo nuevas palabras ni evaluación por persona; URL pública no acreditada: P-03 y P-04. Capacidad base 36 h y tareas 44 h: sobreplanificación de 8 h, no horas reales.

### Sprint 5 Reconocimiento e interfaz

**Resultado:** Reconocedor de poses estáticas e interfaz implementados. Limpieza y acumulación Hola Casa observadas; carga de modelos validada por función de integración.

**Pendientes trasladados:** Movimiento, aceptación lingüística y discrepancia CINE en primer HOLA siguen pendientes: P-03, P-05 y P-08.

### Sprint 6 Voz y almacenamiento

**Resultado:** Joaquín confirmó audio claro de Hola Casa. Parquet y DuckDB locales recuperaron datos ficticios desde procesos nuevos. Texto a voz requiere Internet.

**Pendientes trasladados:** MotherDuck remoto, accesibilidad ampliada y voz a texto no acreditados: P-04 y P-06.

### Sprint 7 Integración y pruebas

**Resultado:** Cuatro hallazgos corregidos; 31 casos de regresión y 14 unitarias correctos el 6 de noviembre. Repetición del 9: 31 correctos, 0 fallidos, 0 bloqueados y 14 unitarias correctas.

**Pendientes trasladados:** No equivale a cobertura total. Revisión de código por otro integrante y publicación de correcciones locales de SIGNIA sin acreditar: P-09.

### Sprint 8 Pruebas manuales y entrega

**Resultado:** Cámara, HOLA/CASA, acumulación y voz documentadas; capturas y video de pantalla de 79,7 s analizados. Los tres Word se publicaron en Capstone en a0d3ef6.

**Pendientes trasladados:** Validación con colaborador, satisfacción, latencia válida y entrega oral/video final pendientes: P-07, P-08 y P-10.

## Backlog posterior al cierre documental

Los puntos siguientes continúan pendientes; su traslado es una decisión operativa de documentación solicitada por Joaquín, sin aprobación docente o del PO acreditada. No se eliminan del alcance original ni se les asignan fechas, prioridades o responsables individuales nuevos sin acuerdo. Coordinación propuesta: revisar con el PO y Scrum Master; las pruebas de QA se coordinan con Joaquín.

| ID | Área | Trabajo pendiente | Evidencia para terminar |
| --- | --- | --- | --- |
| P-01 | Diseño | Revisar diseño implementado y documentar si se requieren mockups adicionales. | Revisión del equipo registrada; no sustituir Figma por una aprobación inventada. |
| P-02 | Cámara e incidencias | Probar Chrome y Edge y reproducir el retorno al acceso con pasos/versiones. | Matriz de pruebas y resultado real por navegador e incidencia. |
| P-03 | Datos y evaluación | Capturar participantes/sesiones separados, validar etiquetas y ampliar vocabulario. | Evaluación independiente por persona; nuevas clases realmente capturadas. |
| P-04 | Nube y datos remotos | Desplegar URL y verificar MotherDuck cuando se retome el alcance remoto. | Acceso desde otro equipo y persistencia remota probada. |
| P-05 | Movimiento | Implementar y evaluar secuencias si se mantiene el requisito. | Reconocimiento temporal; una pose aislada no lo cumple. |
| P-06 | Accesibilidad y voz a texto | Validar contraste, lectura, teclado y decidir la función opcional de voz a texto. | Pruebas registradas con usuarios y decisión de alcance explícita. |
| P-07 | Latencia | Instrumentar captura/predicción/presentación con marcas correlacionadas. | Mediciones válidas, repeticiones, mediana y máximo; no tiempos del chat. |
| P-08 | Aceptación y reconocimiento | Ejecutar protocolo y cuestionario con colaborador; repetir transiciones y CINE adicional. | Intentos nuevos y respuestas reales, sin mezclar datos de entrenamiento. |
| P-09 | Proceso y código | Revisar correcciones en equipo y comprobar su versión publicada en SIGNIA. | Evidencia de revisión y commit de código; este commit de Capstone es documental. |
| P-10 | Presentación y evaluación | Franco prepara PPT; identificar video final y completar evaluación académica. | Entrega oral/video y revisión docente/PO registradas cuando ocurran. |

## Participación y resultados de verificación

Según declaración de Joaquín, los tres integrantes participaron en la revisión previa: Joaquín González, Franco Duarte y Khaeil Parga. Fecha y acuerdos por persona no precisados. En la nueva sesión solo Joaquín está presente: solicita y supervisa las pruebas; Codex asiste en ejecución automática y documentación. No se atribuye esta corrida a Franco ni a Khaeil.

Repetición automatizada del 9 de noviembre: 31/31 casos de regresión correctos, cero fallidos y cero bloqueados. Las 14 unitarias pasaron en el reintento autorizado fuera del aislamiento; el primer intento tuvo un PermissionError al reemplazar un archivo temporal. CSV, modelos y Parquet reales conservaron sus hashes. Los métodos, límites y resultados se consolidan en el anexo J del informe 2.6; la evidencia bruta permanece local.

El sprint 4 tenía 36 h de capacidad base y 44 h de tareas tras añadir HU-25: diferencia de planificación de 8 h. No se declara como tiempo realmente trabajado.

Los registros históricos de sprints 1 a 4 se conservan debajo de su actualización vigente. Los sprints 5 a 8 quedan detallados aquí y en los Word 2.4 y 2.6, sin multiplicar archivos.

## Plan histórico de referencia

# Roadmap del producto: SignIA

Plan ágil de 8 sprints (15 semanas): 7 sprints de 2 semanas y un sprint final de 1 semana. Se planifica por sprint numerado; las fechas de calendario se fijan con el docente.

Los sprints de desarrollo avanzan de forma incremental sobre la versión 1.0 (MVP local) y se enfocan en: captura desde el navegador, evaluación del modelo, mejoras de UX/UI y despliegue gratuito en la nube.

| Sprint | Semanas | Fase APT | Sprint Goal | Incremento esperado | Responsable | HU |
| --- | --- | --- | --- | --- | --- | --- |
| 1. Documentación y definición | 1-2 | Fase 1 | Definir el proyecto y su Product Backlog inicial | Visión, backlog priorizado, épicas e HU, Impact Map | Khaeil Parga | — |
| 2. Arquitectura y diseño | 3-4 | Fase 1 | Definir la arquitectura, el modelo de datos y la nueva UI | Arquitectura documentada, modelo de datos, mockups | Equipo | HU-16 |
| 3. Entorno base y captura de video | 5-6 | Fase 2 | Entorno reproducible y captura de cámara desde el navegador | Repo nuevo, captura con streamlit-webrtc, bugs de sesión y registro corregidos, contraseñas seguras | Franco Duarte | HU-01, 02, 03, 10, 11, 12 |
| 4. Modelo de reconocimiento (IA) | 7-8 | Fase 2 | Modelo reentrenado y evaluado, publicado en la nube | Entrenamiento desde el panel admin, dataset ampliado, reporte de métricas, app en Streamlit Cloud | Franco Duarte, Khaeil Parga | HU-04, 05, 06, 19, 25 |
| 5. Señas con movimiento y UX/UI | 9-10 | Fase 2 | Reconocer frases básicas con movimiento e interfaz renovada | Modelo de secuencias, nueva UI, retroalimentación al usuario | Franco Duarte | HU-07, 08, 09, 13, 14, 15, 16, 17, 22, 24 |
| 6. Texto ↔ voz y accesibilidad | 11-12 | Fase 2 | Comunicación bidireccional y accesibilidad | Voz a texto (si se confirma), modo alto contraste, datos persistentes en MotherDuck | Franco Duarte, Joaquín González | HU-18, 23, 26 |
| 7. Integración y pruebas unitarias | 13-14 | Fase 2 | Módulos integrados y probados | Suite de pruebas unitarias, informe de avance Fase 2 | Joaquín González | HU-20 |
| 8. Testing, ajustes y entrega | 15 | Fase 3 | Validar con usuarios y entregar | Errores críticos corregidos, informe final, presentación | Joaquín González, Khaeil Parga | HU-21 |

## Hitos

| Hito | Semana |
| --- | --- |
| Product Backlog inicial | 2 |
| Mockups e informe de avance Fase 1 | 4 |
| Primera versión pública en la nube | 8 |
| Informe de avance Fase 2 | 14 |
| Informe final y presentación | 15 |

## Artefactos por sprint

● se crea, ○ se actualiza.

| Artefacto | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Visión del producto | ● | | | | | | | |
| Product Backlog | ● | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| Épicas e historias de usuario | ● | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| Impact Map y User Story Map | ● | ● | | | | | | |
| Modelo de datos y arquitectura | | ● | ○ | ○ | ○ | ○ | ○ | ○ |
| Sprint Backlog y Scrumboard | ● | ● | ● | ● | ● | ● | ● | ● |
| Burndown chart | ● | ● | ● | ● | ● | ● | ● | ● |
| Registro de dailies | ● | ● | ● | ● | ● | ● | ● | ● |
| Registro de impedimentos | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| Review y Retrospectiva | ● | ● | ● | ● | ● | ● | ● | ● |

## Cambios respecto a la planificación de Fase 1

- De 9 sprints en 18 semanas a 8 sprints en 15 semanas: el Sprint 9 de cierre se integra al Sprint 8.
- El modelo es un clasificador SVC de scikit-learn, no una red Keras: el SVC ya funciona, es liviano para la nube gratuita y se evalúa con métricas en el Sprint 4.
- Se agrega el despliegue en la nube (Sprint 4) y la captura desde el navegador (Sprint 3), que la Fase 1 dejaba fuera.
- La UX/UI pasa a ser un objetivo explícito (Sprints 2 y 5).
- La traducción de voz a texto queda como "podría" (HU-23) y se confirma en el Sprint 5.
