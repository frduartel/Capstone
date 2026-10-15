# Visión del producto: SignIA

| Campo | Detalle |
| --- | --- |
| Proyecto | SignIA, traductor de Lengua de Señas Chilena (LSCh) a texto y voz |
| Asignatura | Capstone, Portafolio de Título (APT122), Ingeniería en Informática |
| Institución | Duoc UC, sede Padre Alonso de Ovalle |
| Product Owner | Khaeil Parga |
| Scrum Master | Franco Duarte |
| Developers | Khaeil Parga, Franco Duarte, Joaquín González |
| Metodología | Scrum, sprints de 2 semanas |
| Versión del documento | 1.0 (Sprint 1) |

## 1. Análisis del caso

Las personas sordas que se comunican en LSCh enfrentan barreras diarias con quienes no conocen la lengua: en atención de público, salud, educación y trámites. La Ley 21.303 (2021) reconoce la LSCh como lengua oficial de las personas sordas en Chile, pero la disponibilidad de intérpretes es baja y su costo limita el acceso.

Hoy la comunicación depende de un intérprete, de escribir en papel o en el teléfono, o de gestos improvisados. Ninguna de estas alternativas es inmediata ni natural para la persona sorda.

## 2. Declaración de visión

> Para personas sordas que usan LSCh y las personas oyentes que interactúan con ellas, que necesitan comunicarse sin depender de un intérprete, **SignIA** es una aplicación web que reconoce señas por cámara y las traduce en tiempo real a texto y voz. A diferencia de los diccionarios y cursos de LSCh, que solo enseñan, SignIA traduce en el momento con un navegador y una cámara web, sin instalar nada.

## 3. Usuarios y actores

| Actor | Necesidad principal |
| --- | --- |
| Persona sorda usuaria de LSCh | Ser entendida por personas oyentes de forma inmediata |
| Persona oyente (interlocutor) | Entender lo que se le comunica en LSCh, en texto o voz |
| Aprendiz de LSCh | Practicar señas y acceder a recursos confiables |
| Administrador | Gestionar usuarios, modelos de IA y ver métricas de uso |
| Equipo de desarrollo y docente | Evidenciar avance, calidad y decisiones del proyecto |

## 4. Objetivos del producto

**Objetivo general.** Desarrollar una aplicación web que traduzca señas de la LSCh a texto y voz en tiempo real, facilitando la comunicación entre personas sordas y oyentes.

**Objetivos específicos.**
1. Implementar un modelo de reconocimiento de señas basado en visión por computador (MediaPipe) y aprendizaje automático, con métricas de desempeño medibles.
2. Diseñar una interfaz web accesible y simple, mejorando la experiencia de usuario de la versión 1.0.
3. Integrar la conversión de texto a voz para entregar retroalimentación auditiva inmediata.
4. Desplegar la aplicación en una plataforma gratuita en la nube, accesible desde un navegador.

## 5. Alcance

**Incluye**
- Reconocimiento de un vocabulario acotado de señas estáticas (actualmente 18 palabras), ampliable por el administrador desde la web.
- Reconocimiento de frases básicas con movimiento (por ejemplo "¿cómo estás?"), planificado para el Sprint 5.
- Traducción a texto con nivel de confianza y armado de frases.
- Lectura en voz alta de la frase (gTTS).
- Registro, inicio de sesión y roles usuario y administrador.
- Panel de administración: usuarios, métricas, carga de modelos y consultas SQL.
- Recursos de aprendizaje de LSCh (consejos, videos y enlaces).
- Despliegue en la nube con captura de cámara desde el navegador.

**No incluye**
- Traducción de conversaciones completas o de vocabulario abierto.
- Reconocimiento de expresiones faciales o de más de una persona a la vez.
- Aplicación móvil nativa.
- Traducción de voz a LSCh (avatar o animación).

## 6. Restricciones y supuestos

- Stack tecnológico: Python 3.10, Streamlit, OpenCV, MediaPipe, scikit-learn, DuckDB y gTTS.
- La nube debe ser gratuita, por lo que el almacenamiento puede ser efímero y los recursos de cómputo son limitados.
- La precisión depende de la iluminación, la cámara y la calidad del dataset propio.
- El calendario se planifica por sprints numerados; las fechas exactas se ajustan con el docente.

## 7. Métricas de éxito

| Métrica | Meta |
| --- | --- |
| Exactitud (accuracy) del modelo en el conjunto de prueba | ≥ 90 % |
| F1 macro por clase | ≥ 0,85 |
| Tiempo desde la seña hasta el texto | < 1 segundo |
| Vocabulario reconocido | ≥ 18 palabras (meta 25) |
| Aplicación disponible en la nube | URL pública operativa |
| Satisfacción en pruebas de usuario (escala 1 a 5) | ≥ 4 |

## 8. Riesgos principales

| Riesgo | Prob. | Impacto | Mitigación |
| --- | --- | --- | --- |
| Dataset propio pequeño o poco variado | Alta | Alto | Capturar con los tres integrantes y en distintas condiciones de luz |
| La captura de cámara no funciona en la nube | Media | Alto | Capturar desde el navegador (streamlit-webrtc) en lugar de OpenCV en el servidor |
| Límites del plan gratuito (RAM, suspensión) | Media | Medio | Modelos livianos (SVC), dependencias mínimas, documentar el arranque en frío |
| Pérdida de datos por disco efímero | Alta | Medio | Documentarlo como limitación; evaluar almacenamiento externo gratuito |
| Poca disponibilidad del equipo por otras asignaturas | Media | Medio | Sprints con objetivos acotados y registro de impedimentos |
