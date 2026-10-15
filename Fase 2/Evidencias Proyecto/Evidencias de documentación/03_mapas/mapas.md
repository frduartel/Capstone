# Mapas del producto: SignIA

Artefactos de planificación visual creados en los Sprints 1 y 2. Los diagramas usan Mermaid, que GitHub muestra como imagen.

## 1. Mapa mental

```mermaid
mindmap
  root((SignIA))
    Reconocimiento
      Cámara web
      MediaPipe Hands
      Modelo SVC
      Dataset propio LSCh
    Traducción
      Texto con confianza
      Frase acumulada
      Voz gTTS
    Usuarios
      Registro e inicio de sesión
      Roles usuario y admin
    Administración
      Gestión de usuarios
      Estadísticas
      Carga de modelos
      Consultas SQL
    Aprendizaje LSCh
      Consejos
      Videos
      Enlaces y cursos
    Nube
      Streamlit Community Cloud
      Captura en el navegador
```

## 2. Mapa de actores

```mermaid
flowchart LR
    S[Persona sorda<br/>usuaria de LSCh] -->|hace señas| APP((SignIA))
    APP -->|texto y voz| O[Persona oyente]
    A[Aprendiz de LSCh] -->|consulta recursos| APP
    ADM[Administrador] -->|gestiona usuarios y modelos| APP
    EQ[Equipo de desarrollo] -->|entrena y despliega| APP
    APP -->|voz| G[(Servicio gTTS)]
    APP -->|publicada en| C[(Streamlit Cloud)]
    DOC[Docente Capstone] -.->|evalúa avances| EQ
```

| Actor | Tipo | Interés |
| --- | --- | --- |
| Persona sorda | Primario | Comunicarse sin intérprete |
| Persona oyente | Primario | Entender a la persona sorda |
| Aprendiz de LSCh | Secundario | Aprender y practicar |
| Administrador | Secundario | Operar la plataforma |
| Equipo de desarrollo | Interno | Construir y mejorar el producto |
| Docente | Externo | Evaluar el proyecto APT |
| gTTS y Streamlit Cloud | Sistemas externos | Voz y hosting |

## 3. Impact Mapping

Conecta el objetivo con los actores, los cambios de comportamiento esperados (impactos) y las funcionalidades (entregables).

```mermaid
flowchart LR
    G[["¿Por qué?<br/>Que una persona sorda se comunique con una oyente<br/>sin intérprete en una conversación breve"]]
    G --> A1(Persona sorda)
    G --> A2(Persona oyente)
    G --> A3(Administrador)
    G --> A4(Equipo)
    A1 --> I1[Usa la app desde cualquier navegador]
    A1 --> I2[Confía en la traducción]
    A2 --> I3[Entiende el mensaje sin saber LSCh]
    A3 --> I4[Mantiene la plataforma operativa]
    A4 --> I5[Mejora el modelo con nuevos datos]
    I1 --> D1[HU-03 Captura en el navegador]
    I1 --> D2[HU-19 Despliegue en la nube]
    I2 --> D3[HU-04 Predicción con confianza]
    I2 --> D4[HU-17 Retroalimentación clara]
    I3 --> D5[HU-07 Frase generada]
    I3 --> D6[HU-08 Voz]
    I4 --> D7[HU-13 Gestión de usuarios]
    I4 --> D8[HU-14 Estadísticas]
    I5 --> D9[HU-05 Ampliar dataset]
    I5 --> D10[HU-06 Evaluar modelo]
```

## 4. User Story Map

La fila superior es el recorrido del usuario (actividades). Debajo, las historias ordenadas por prioridad; cada franja horizontal es una entrega (release).

| | Acceder | Preparar cámara | Hacer señas | Comunicar | Aprender | Administrar |
| --- | --- | --- | --- | --- | --- | --- |
| **Release 1: MVP local (Fase 1)** | HU-10 Registro<br/>HU-11 Inicio de sesión | HU-02 Detectar manos | HU-04 Predicción con confianza | HU-07 Frase<br/>HU-08 Voz<br/>HU-09 Limpiar | HU-22 Recursos LSCh | HU-13 Usuarios<br/>HU-15 Cargar modelo |
| **Release 2: Nube (Sprints 3 y 4)** | HU-12 Contraseñas seguras | HU-03 Cámara en el navegador<br/>HU-01 Entorno reproducible | HU-05 Más vocabulario<br/>HU-06 Modelo evaluado | HU-19 URL pública | | |
| **Release 3: Experiencia (Sprints 5 y 6)** | HU-16 Interfaz consistente | HU-17 Retroalimentación | | HU-23 Voz a texto | HU-18 Alto contraste | HU-14 Estadísticas corregidas |
| **Release 4: Calidad (Sprints 7 y 8)** | | | HU-20 Pruebas unitarias | HU-21 Validación con usuarios | | |
