# Sistema de diseño: SignIA

Define cómo se ve y se siente la aplicación. Los valores viven como tokens (variables CSS) en `app/ui.py`, así que un cambio en un token se aplica en todas las pantallas. Responde a las historias HU-16 (interfaz consistente), HU-17 (instrucciones y retroalimentación) y HU-18 (textos grandes y buen contraste).

## 1. Principios

1. **Las manos son las protagonistas.** La cámara muestra tonos de piel cálidos; la interfaz usa un color principal frío para no competir con ellos.
2. **Se lee de lejos.** La seña detectada y la frase son el texto más grande de la pantalla, porque se miran mientras se hace la seña.
3. **El color nunca va solo.** Todo estado (confianza alta, media o baja) también se explica con texto, para personas con daltonismo.
4. **Calma y confianza.** Es una herramienta de comunicación: animaciones cortas, sin elementos que distraigan y sin emojis.

## 2. Color

La paleta toma nombres de Chile: el océano Pacífico, el cobre y la cordillera.

| Familia | Token | Hex | Uso |
| --- | --- | --- | --- |
| Pacífico | `--pacifico-600` | `#0E7C7B` | Color principal: botones primarios, menú activo, barra de confianza alta |
| | `--pacifico-700` | `#0B6463` | Texto de enlaces y botones secundarios, estado presionado |
| | `--pacifico-800` | `#084C4B` | Relieve del botón primario, texto sobre fondo suave |
| | `--pacifico-50` | `#E7F5F4` | Fondo suave: ítem activo del menú, etiquetas de señas |
| Cobre | `--cobre-600` | `#C2522B` | Acento: botón Escuchar y lo que la app "dice" |
| | `--cobre-50` | `#FCEFE8` | Fondo de la frase generada |
| Cordillera | `--cordillera-900` | `#1F2A37` | Texto principal |
| | `--cordillera-600` | `#5B6472` | Texto secundario |
| | `--cordillera-200` | `#E3E8EC` | Bordes |
| | `--cordillera-50` | `#F5F7F8` | Fondo de la barra lateral |
| Estado | `--warning` | `#F2B544` | Confianza media (mantén la seña) |
| | `--error` | `#C93C3C` | Confianza baja |

**Regla del acento:** el cobre se usa solo para la voz y la frase. Así, cuando aparece, la persona sabe que es el resultado de la traducción.

### Contraste (WCAG 2.1)

| Combinación | Contraste | Nivel |
| --- | --- | --- |
| Texto `#1F2A37` sobre blanco | 14,5:1 | AAA |
| Texto secundario `#5B6472` sobre blanco | 6,0:1 | AA |
| Blanco sobre Pacífico 600 (botón primario) | 5,0:1 | AA |
| Blanco sobre Cobre 600 (botón Escuchar) | 4,6:1 | AA |
| Pacífico 700 sobre Pacífico 50 (menú activo) | 6,2:1 | AA |
| Texto principal sobre amarillo de advertencia | 7,9:1 | AAA |

## 3. Tipografía

Una sola familia, **Nunito**, por sus formas redondeadas y su buena lectura en pantalla. La jerarquía sale de una escala de tercera mayor (cada nivel es 1,25 veces el anterior) sobre una base de 16 px.

| Rol | Token | Tamaño | Peso | Uso |
| --- | --- | --- | --- | --- |
| Display | `--fs-display` | 48,8 px | 900 | Título de inicio de sesión y bienvenida |
| Título 1 | `--fs-h1` | 39 px | 900 | Título de página y seña detectada |
| Título 2 | `--fs-h2` | 31,2 px | 800 | Valores de métricas |
| Título 3 | `--fs-h3` | 25 px | 800 | Frase generada, nombre en la barra lateral |
| Título 4 | `--fs-h4` | 20 px | 800 | Títulos de tarjetas |
| Cuerpo grande | `--fs-body-lg` | 18 px | 500 | Bajadas de página |
| Cuerpo | `--fs-body` | 16 px | 500 | Texto general y menú |
| Etiqueta | `--fs-label` | 14 px | 800 | Botones y campos de formulario |
| Leyenda | `--fs-caption` | 12,8 px | 600 | Ayudas y notas |
| Sobretítulo | `--fs-overline` | 12 px | 800, mayúsculas | Sección de la página, etiquetas de tarjetas |

Los botones usan mayúscula inicial (no todo en mayúsculas) para que se lean más rápido.

## 4. Espaciado, radios y elevación

- **Espaciado:** múltiplos de 4 px (`--space-1` = 4 px hasta `--space-12` = 48 px).
- **Radios:** 8 px (etiquetas), 12 px (botones y campos), 20 px (tarjetas) y píldora (chips y control de cámara).
- **Elevación:** las tarjetas usan una sombra suave; los botones tienen un relieve de 3 px que desaparece al presionarlos, como un botón físico.

## 5. Movimiento

- Las páginas y pestañas entran con un desplazamiento corto hacia arriba (0,45 s).
- Cada palabra nueva de la frase aparece con una pequeña escala.
- La seña en vivo no se anima, porque se actualiza varias veces por segundo.
- Si el sistema operativo pide reducir el movimiento, todas las animaciones se desactivan.

## 6. Componentes

| Componente | Función en `app/ui.py` | Descripción |
| --- | --- | --- |
| Encabezado de página | `page_header` | Sobretítulo, título y bajada |
| Tarjeta | `card` | Contenido agrupado con etiqueta opcional |
| Chips de señas | `sign_chips` | Vocabulario que reconoce el modelo |
| Seña detectada | `render_prediction` | Seña en grande, barra de confianza y texto del estado |
| Frase | `render_phrase` | Globo en tono cobre con la frase acumulada |
| Menú lateral | `nav_menu` | Navegación por rol con el ítem activo marcado |
| Logo | `logo_mark`, `brand_html` | Isotipo y logotipo |

## 7. Logo

El isotipo es un globo de diálogo blanco sobre un cuadrado Pacífico, con tres puntos: los dos primeros en Pacífico (la seña que se está "escribiendo") y el último en cobre (la voz). El logotipo escribe "Sign" en el color del texto e "IA" en Pacífico. El ícono de la pestaña del navegador es `app/assets/logo.png`.
