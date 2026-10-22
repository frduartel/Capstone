# SignIA · Capstone Grupo 2

![Duoc UC](https://img.shields.io/badge/Duoc%20UC-Ingenier%C3%ADa%20en%20Inform%C3%A1tica-FFB81C?style=flat-square)
![Asignatura](https://img.shields.io/badge/Asignatura-APT122-1F4E79?style=flat-square)
![Metodología](https://img.shields.io/badge/Metodolog%C3%ADa-Scrum-2E7D32?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=flat-square&logo=python&logoColor=white)

Repositorio de evidencias del Capstone (Portafolio de Título, APT122) de **SignIA**, un traductor de Lengua de Señas Chilena (LSCh) a texto y voz, desarrollado como aplicación web.

## Contexto

La Ley 21.303 (2021) reconoce la LSCh como lengua oficial de las personas sordas en Chile, pero la disponibilidad de intérpretes es baja y su costo limita el acceso. SignIA reconoce señas mediante la cámara del navegador y las traduce en tiempo real a texto y voz, sin instalar nada.

## Equipo

| Integrante | Rol |
| --- | --- |
| Khaeil Parga | Product Owner |
| Franco Duarte | Scrum Master |
| Joaquín González | Developer |

Sede Padre Alonso de Ovalle, Duoc UC. Metodología Scrum con sprints de 2 semanas.

## Tecnologías

| Área | Herramienta |
| --- | --- |
| Interfaz web | Streamlit, streamlit-webrtc |
| Visión por computador | MediaPipe |
| Modelo de reconocimiento | Clasificador SVC (scikit-learn) |
| Lenguaje | Python 3.10 |

## Estructura del repositorio

```text
Capstone/
├── Fase 1/                      Definición del proyecto
│   ├── Evidencias Grupales/
│   └── Evidencias Individuales/
├── Fase 2/                      Desarrollo del proyecto
│   ├── Evidencias Grupales/
│   ├── Evidencias Individuales/
│   └── Evidencias Proyecto/
│       ├── Evidencias de documentación/   Artefactos ágiles
│       └── Evidencias de sistema/         Aplicación y base de datos
└── Fase 3/                      Cierre del proyecto
    ├── Evidencias Grupales/
    └── Evidencias Individuales/
```

## Estado por fase

| Fase | Descripción | Estado |
| --- | --- | --- |
| [Fase 1](Fase%201) | Definición del proyecto | Entregada (versión corregida) |
| [Fase 2](Fase%202) | Desarrollo del proyecto | Documentada hasta el Sprint 4 |
| [Fase 3](Fase%203) | Cierre e informe final | Pendiente |

## Convenciones

- Cada fase separa las **evidencias grupales** de las **individuales**.
- Los entregables individuales siguen el patrón `Apellido_Nombre_<n°>_APT122_<Título>.docx`.
- La documentación técnica y ágil está en Markdown; los diagramas se guardan en PNG y SVG.
- Cada carpeta incluye su propio `README.md` con el detalle de su contenido.

> El código fuente de la aplicación vive en un repositorio aparte (SignIA-APT). Este repositorio contiene únicamente las evidencias y su documentación.
