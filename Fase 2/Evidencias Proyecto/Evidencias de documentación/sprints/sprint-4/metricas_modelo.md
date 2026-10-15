# Métricas del modelo de reconocimiento

Generado por `ml/evaluate_model.py` el 2026-10-04 18:44.

- Muestras: 1800
- Clases: 18 (ABURRIDO, ACAMPAR, ACUERDO, ALAMEDA, AMERICA, ANIMAL, APLAUDIR, ATENTO, BIEN, BURLARSE, BURRO, CASA, CINE, COMER, DINOSAURIO, DORMIR, HOLA, TE_QUIERO)
- Personas registradas: equipo_v1

## 1. Modelo en uso (división 75/25)

| Métrica | Valor |
| --- | --- |
| Accuracy | 0.987 |
| F1 macro | 0.987 |

## 2. Comparación de algoritmos (validación cruzada, 5 particiones)

| Algoritmo | Accuracy media | F1 macro media |
| --- | --- | --- |
| SVC (RBF, C=30) — modelo actual | 0.993 | 0.993 |
| k-NN (k=5) | 0.990 | 0.990 |
| Random Forest (200 árboles) | 0.991 | 0.991 |

## 3. División temporal (último 25 % de cada captura como prueba)

| Métrica | Valor |
| --- | --- |
| Accuracy | 1.000 |
| F1 macro | 1.000 |

## 4. Evaluación con una persona nueva

Pendiente: el dataset tiene una sola fuente de muestras. Cuando cada integrante capture
sus señas con `python ml/capture_data.py --persona <nombre>`, este apartado entrena sin
esa persona y mide qué tan bien reconoce sus señas. Es la métrica más cercana al uso real.

## Interpretación

Las muestras son fotogramas consecutivos de una misma sesión de captura, por lo que la división
aleatoria y la validación cruzada mezclan fotogramas casi idénticos entre entrenamiento y prueba.
Por eso los valores de las secciones 1 y 2 son optimistas. La sección 3 es más exigente, y la
sección 4 es la referencia para decidir si el modelo está listo para usuarios nuevos.
