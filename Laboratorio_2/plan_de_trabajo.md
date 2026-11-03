# Plan de Trabajo y Distribución de Roles - Workshop 02

Propuesta para la división de trabajo del workshop entre **2 personas (Integrante A e Integrante B)**, equilibrando las cargas compartidas (código, aplicación, informe) y las responsabilidades individuales (ejercicios manuales y reflexión).

---

## 👥 Asignación de Roles Generales

- **Integrante A:** Líder del bloque computacional de **Sistemas (Lineales y No Lineales)** y responsable del desarrollo de la mitad de los ejercicios manuales.
- **Integrante B:** Líder del bloque computacional de **Interpolación (Lagrange, Newton y Spline con datos reales)** y responsable de la otra mitad de los ejercicios manuales.
- **Tareas Conjuntas:** Definición de la estructura de carpetas, el aplicativo en Streamlit, el informe final (Markdown, PDF, Word) y los registros de progreso (`PLAN.md`, `ToDo.md`, `history.md`).

---

## 📋 Distribución Detallada por Fases y Componentes

### 1. Desarrollo Manual (12 ejercicios por persona = 24 en total)

Cada integrante realiza sus propios 12 ejercicios (3 por cada bloque de clase: 07, 08, 09 y 10), asegurando incluir los controles de clase y documentando sus correcciones.

#### Integrante A:
- **Bloque 07 (Sistemas Lineales):** 3 ejercicios (orden 2, 3 y 4; incluyendo intercambio de filas).
- **Bloque 08 (Sistemas No Lineales):** 3 ejercicios (punto fijo, Newton y comparación de despejes/puntos iniciales).
- **Bloque 09 (Lagrange):** 3 ejercicios (2, 3 y 4 nodos, con consulta interior).
- **Bloque 10 (Newton Interpolador):** 3 ejercicios (3 nodos, 4 nodos y adición de un nodo).
- Realiza su respectivo documento de evidencia manuscrita o digital.

#### Integrante B:
- **Bloque 07 (Sistemas Lineales):** 3 ejercicios independientes o adaptados (orden 2, 3 y 4; con pivoteo).
- **Bloque 08 (Sistemas No Lineales):** 3 ejercicios independientes o adaptados (punto fijo, Newton y análisis).
- **Bloque 09 (Lagrange):** 3 ejercicios independientes o adaptados (2, 3 y 4 nodos).
- **Bloque 10 (Newton Interpolador):** 3 ejercicios independientes o adaptados (3 nodos, 4 nodos y adición de nodos).
- Realiza su respectivo documento de evidencia manuscrita o digital.

---

### 2. Implementación Modular y Cuadernos Python (5 Cuadernos en total)

El desarrollo del código se divide por módulos temáticos para que ambos trabajen de forma fluida:

#### Integrante A (Módulos y Cuadernos de Sistemas):
- Construcción de los módulos y funciones reutilizables para **Sistemas Lineales** y **Sistemas No Lineales** (punto fijo y Newton para sistemas, incluyendo historial de iteraciones y manejo de errores).
- Redacción y ejecución del **Cuaderno 1:** Sistemas Lineales (enlazando evidencias manuales y análisis del residual $Ax-b$).
- Redacción y ejecución del **Cuaderno 2:** Sistemas No Lineales (aplicando tolerancias $\le 10^{-4}$ y control de actualizaciones).

#### Integrante B (Módulos y Cuadernos de Interpolación):
- Construcción de los módulos y funciones reutilizables para **Lagrange**, **Newton** (diferencias divididas y evaluación), **Spline cúbico** y **métricas de error** (MAE, RMSE, Error Máx).
- Redacción y ejecución del **Cuaderno 3:** Lagrange.
- Redacción y ejecución del **Cuaderno 4:** Newton Interpolador.
- Redacción y ejecución del **Cuaderno 5:** Spline y comparación con datos reales (USGS u otra fuente, partición de construcción/validación y cálculo de métricas).

---

### 3. Aplicativo Interactivo en Streamlit (4 Pestañas)

El diseño de la aplicación web se divide por pestañas reutilizando los módulos creados:

#### Integrante A se encarga de:
- **Pestaña 1:** Sistemas Lineales (contexto de ingeniería, modelo, entradas y análisis de resultados).
- **Pestaña 2:** Sistemas No Lineales (contexto, controles de entrada y validación de convergencia).

#### Integrante B se encarga de:
- **Pestaña 3:** Lagrange (problema aplicado de ingeniería compartido con la pestaña 4).
- **Pestaña 4:** Newton con comparación de Spline (utilizando exactamente los mismos datos y nodos para una comparación justa).

---

### 4. Gestión, Informe y Registros (Trabajo Conjunto / Dividido)

#### Integrante A:
- Redacción de las secciones del informe asociadas a la formulación matemática, sistemas lineales y no lineales.
- Consolidación del registro de uso de IA y prompts para los bloques 07 y 08.

#### Integrante B:
- Redacción de las secciones del informe asociadas a la selección de datos reales (ej. USGS), interpolación y conclusiones generales.
- Consolidación del registro de uso de IA y prompts para los bloques 09, 10 y Spline.

#### Ambos (Conjunto):
- Actualización constante y conjunta de los archivos de seguimiento: `PLAN.md`, `ToDo.md` y `history.md`.
- Exportación final del informe en formatos **Markdown, PDF y Word**, verificando la correcta visualización de ecuaciones, tablas y figuras.
- Ejecución integral del proyecto desde un kernel limpio para asegurar la reproducibilidad de todo el repositorio antes de la entrega.

---

### 5. Reflexión Individual

- **Integrante A:** Redacción de su propia reflexión crítica/argumentada basada en sus 2 momentos concretos del workshop y su experiencia con o sin herramientas de IA.
- **Integrante B:** Redacción de su propia reflexión crítica/argumentada basada en sus 2 momentos concretos del workshop y su experiencia con o sin herramientas de IA.