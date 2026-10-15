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
