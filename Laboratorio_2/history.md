# history.md — Bitácora de decisiones, correcciones y comprobaciones

**Proyecto:** Workshop 2 · Sistemas de ecuaciones e interpolación (2026-2) **Equipo:** Jose Manuel Arboleda Carvajal · Gabriel David Castaño **Docente:** Mg. Mario Hernán López Arbeláez **Última actualización:** 3 de noviembre de 2026

---

## 1\. Línea de tiempo

### 1 de noviembre de 2026

- **18:40 (Git, commit 1\)** — Jose Arboleda: *"Subir módulo y cuadernos del laboratorio 2"*. Primera versión de `ModLab2.py`, `Cuaderno_1.ipynb` y `Cuaderno_2.ipynb`. **\[Verificado\]**  
- **21:01 (Git, commit 2\)** — Jose Arboleda: *"Se agregaron los ejercicios de Gabriel"*. Se incorporan los ejercicios del segundo integrante al repositorio. **\[Verificado\]**  
  - Es el último commit del repositorio. Todo lo posterior está sin confirmar. **\[Pendiente\]**

### 2 de noviembre de 2026

- **Madrugada** — Se ajusta `ModLab2.py` (sistemas lineales, punto fijo y Newton para sistemas) y se crean `modelos_estructurales.py`, `graficos_estructurales.py` y `pestana_lineales.py`. **\[Verificado, por fechas de archivo\]**  
- **Madrugada** — Se crea `app/requirements.txt` con `streamlit`, `numpy` y `matplotlib`. El código actual también importa `pandas` y `scipy`, que no figuran en ese archivo. **\[Pendiente\]**  
- **Noche** — Se crea `ModLab3.py` (Lagrange, diferencias divididas, inserción de nodos y utilidades para la app) y `app.py` con cuatro pestañas y barra lateral compartida. **\[Verificado\]**  
- **Noche** — Se descarga y guarda `app/data/usgs_caudal_diario.rdb`. El informe fija la consulta el **2 de noviembre de 2026**, estación USGS 01646500, parámetro 00060, estadístico 00003, año 2025\. **\[Informe\]**  
- **Noche** — Se crean `pestana_no_lineales.py`, `pestana_lagrange.py` y `pestana_newton_spline.py`. **\[Verificado\]**

### 3 de noviembre de 2026

- **Madrugada** — Se escriben `datos.py`, `interpolacion.py` y `metricas.py`, y los Cuadernos 3, 4 y 5\. Los módulos se copian a `Cuadernos/`. **\[Verificado\]**  
- **Madrugada** — Se ejecuta la app con Python 3.14 (se generan `__pycache__` con la etiqueta `cpython-314`). **\[Verificado\]**  
- **Mañana** — Se redacta `plan_de_trabajo.md` con los roles A/B. **\[Verificado\]**  
- **Mediodía** — Se reorganizan y actualizan los Cuadernos 1 y 2 (con evidencias de los dos integrantes y análisis del residuo y de tolerancias). **\[Verificado\]**  
- **Mediodía** — Se toman las 10 capturas de `ejemplo_de_ejecucion/` mostrando la pestaña 1\. **\[Verificado\]**  
- **Tarde** — Se completa `informe.md` y se exporta `informe.pdf`. **\[Verificado\]**  
- **Tarde** — Se crean `ToDo.md` e `history.md`. Queda pendiente renombrar `plan_de_trabajo.md` a `PLAN.md`. **\[Pendiente\]**

---

## 2\. Decisiones de diseño

| \# | Decisión | Motivo | Dónde queda |
| :---- | :---- | :---- | :---- |
| D1 | Repartir el trabajo en **A (sistemas)** y **B (interpolación y datos reales)**, con tareas conjuntas para app, informe y registros | Equilibrar la carga y cumplir 70 % compartido / 30 % individual | `plan_de_trabajo.md` |
| D2 | Módulos separados: `ModLab2` (sistemas), `ModLab3` (Lagrange/Newton y utilidades), `interpolacion`, `datos`, `metricas` | Evitar un archivo extenso y poder revisar errores por partes | `app/`, `Cuadernos/` |
| D3 | Una pestaña de Streamlit por módulo y un `app.py` corto (≈31 líneas) que solo las ensambla | Facilitar la depuración y mantener la app legible | `app/` |
| D4 | Problemas de ingeniería civil **nuevos** para la app: viga simplemente apoyada (2×2), viga con apoyo fijo y móvil y carga inclinada (3×3), arco triarticulado (4×4); edificios de 2, 3 y 4 pisos con rigidez no lineal para sistemas no lineales | Cumplir la tercera parte (problemas distintos a los de clase) con ecuaciones de equilibrio | `modelos_estructurales.py`, pestañas 1 y 2 |
| D5 | Serie de caudal diario USGS como problema de interpolación compartido entre las pestañas 3 y 4 | Comparación justa de Lagrange, Newton y spline con los mismos nodos y observaciones reservadas | `datos.py`, `bloque_datos_compartidos` |
| D6 | Recorte de **36 días** (1 ene–5 feb 2025); extremos fijos como nodos; **26 nodos** de construcción y **10 observaciones reservadas** (días 2, 6, 10, 14, 17, 18, 22, 26, 30 y 34\) | Un recorte abordable que permite examinar omisiones aisladas y un hueco interior corto | `datos.particion_comun` |
| D7 | **Normalizar el tiempo a \[0, 1\]** antes de interpolar con polinomios de alto grado | Reducir problemas de condicionamiento en grado 25 | `informe.md`, `ModLab3.py` |
| D8 | **Spline natural** (segunda derivada nula en los extremos), contrastado con `scipy.interpolate.CubicSpline` con la misma condición de frontera | Cumplir el contraste con biblioteca exigido por la guía | `interpolacion.py`, Cuaderno 5 |
| D9 | Agregar **Lagrange local** con 2, 3 y 4 nodos como referencia intermedia entre polinomio global y spline | Mostrar el efecto del grado y de la localidad | Cuaderno 3, pestaña 3 |
| D10 | No rellenar los puntos reservados ni extrapolar en la comparación principal | Evitar fuga de información y cumplir la guía | `datos.py` |
| D11 | Los registros con código **Eqp** (15, 16 y 17 de marzo) se descartan sin rellenar | Mantener la validación honesta | informe, sección "Los datos" |
| D12 | Incluir el **vector residual Ax − b** en la app y en el Cuaderno 1 | Verificación independiente del equilibrio estático (ΣF \= 0\) | `ModLab2.py`, Cuaderno 1 |
| D13 | Criterio de parada para el control adimensional: cambio y residual ≤ 10⁻⁴ y máximo de 100 actualizaciones | Es el criterio fijado por la guía para la clase 08 | `ModLab2.py`, Cuaderno 2 |

---

## 3\. Correcciones documentadas (desarrollo manual vs. código)

Todas **\[Informe\]**; las cifras de Newton coinciden con el ejemplo clásico de textos de métodos numéricos.

| \# | Ejercicio | Error inicial | Corrección | Qué se aprendió |
| :---- | :---- | :---- | :---- | :---- |
| C1 | **Newton para sistemas (Ej. 4\)**, x₀ \= (1.5, 3.5), F₁ \= x² \+ xy − 10, F₂ \= y \+ 3xy² − 57 | A mano: (2.03528, 2.84377). Se arrastró Δy \= −0.65623 | Δy \= **0.65613**; el código da (2.03603, 2.84388) | Un pequeño error al dividir cambia el resultado: hay sensibilidad a la Jacobiana |
| C2 | **Punto fijo (Ej. 6\)** con 2x − y² \= 0 y x − 3y \+ 2 \= 0 | Se evaluó ρ(J\_g) \= 0.57735 en (1, 1\) y se concluyó que convergía | (1, 1\) **no es solución**. En las raíces reales: ρ \= 0.5046 en (0.2918, 0.7639) y ρ \= 1.3212 en (13.708, 5.236) | Un número "bonito" no sirve si el punto de evaluación es incorrecto |
| C3 | **Gauss-Jordan 4×4 (Ej. 3\)** | Se anotó 2.27777 a mano | Redondeo correcto: 2.27778 | Cuidar la regla de redondeo |
| C4 | **Punto fijo (Ej. 5\)** | Denominador de g₂ mal escrito en las notas | La evaluación sí se hizo con 4 | Revisar la transcripción de despejes |
| C5 | **Lagrange (Ej. 7\)**, P(2) \= −4/3 | — (no es un error) | Con datos positivos, el polinomio global da un valor negativo | El polinomio global no garantiza positividad |
| C6 | **Sistema 3×3 con F₁ de pivote cero (Ej. 1\)** | Pivote en F₁ igual a cero | Intercambio F₁ ↔ F₂ y comprobación en las ecuaciones | La elección del pivote es una decisión, no un detalle |

---

## 4\. Comprobaciones realizadas

| Comprobación | Resultado | Fuente |
| :---- | :---- | :---- |
| Solución 2×2 por sustitución: (31/10, 8/5) satisface ambas ecuaciones | ✔ | Informe, Sist. lineales |
| Lagrange: P(x\_i) \= y\_i en los nodos de cada ejercicio manual (2, 3 y 4 nodos) | ✔ | Anexos del informe |
| Newton: diferencias divididas y polinomio verificados en los nodos; coeficientes previos se conservan al agregar un nodo | ✔ | Anexos, Cuaderno 4 |
| Spline natural con 3 nodos: M₁ \= −3, S₀(x) \= −½x³ \+ 3⁄2x (ecuación 4M₁ \= 6(δ₁ − δ₀) con h \= 1\) | ✔ (recalculado) | Informe, Ej. 12 |
| Lagrange propio vs. `BarycentricInterpolator` de SciPy | Se contrasta en los Cuadernos 3 y 4 | Cuadernos 3 y 4 |
| Spline propio vs. `CubicSpline` natural de SciPy | Diferencia ≈ 1.8×10⁻¹² ft³/s | Informe, Resultados **\[Informe\]** |
| Residual en nodos | Lagrange 0 · spline ≈ 2×10⁻¹² · Newton ≈ 1.44×10⁻³ ft³/s | Informe, Resultados **\[Informe\]** |
| Métricas sobre 10 observaciones reservadas | Spline natural MAE 347.2, RMSE 544.8, E\_max 1,375.2 ft³/s. Polinomio global (grado 25): MAE 3.3×10⁶, E\_max 3.2×10⁷ ft³/s | Informe **\[Informe\]** |
| Control de calidad de la serie | **Tres anomalías**: segundas diferencias casi constantes, decimales atípicos y encabezado «UPPER DAMSITE» | `datos.control_calidad`, informe |
| Registros faltantes en el `.rdb` local | 365 filas, 3 con código Eqp | **\[Verificado\]** |
| Valor provisional (código P) del 10 de junio | **No aparece** en el `.rdb` local | **\[Verificado\]** → **\[Pendiente\]** |

> **Advertencia.** Las métricas y las conclusiones sobre el fenómeno de Runge se calcularon con el archivo local, que muestra señales de no ser una descarga oficial. Hay que repetirlas con la base real antes de la entrega final (`ToDo.md`, §2.1).

---

## 5\. Hallazgos y problemas abiertos

1. **Datos con apariencia sintética.** El informe ya lo admite; falta reemplazarlos por la descarga oficial y actualizar las cifras.  
2. **Archivos citados pero ausentes del ZIP:** `data/usgs_procesado.csv`, `data/usgs_valores_excluidos.csv`, `reporte_resultados.py` y los escaneos del "Anexo D".  
3. **Cuadernos 1 y 2 con `input()`**: no se ejecutan sin intervención en un kernel limpio.  
4. **Rutas de datos en Cuadernos 3–5:** desde `Cuadernos/` no se encuentra `data/` y el código cae a datos sintéticos.  
5. **Módulos duplicados** en `app/` y `Cuadernos/` (idénticos hoy, pero pueden desincronizarse).  
6. **`requirements.txt` incompleto** (faltan `pandas` y `scipy`).  
7. **Informe:** 75 marcas `[cite: …]` residuales, sin Referencias, sin versión Word.  
8. **Cobertura manual:** el Integrante B lista solo dos casos de Newton y la numeración de ejercicios difiere entre informe y cuadernos.  
9. **Git sin actualizar:** cambios no confirmados desde el commit del 1 de noviembre.

---

## 6\. Uso de IA (resumen; el registro detallado debe ir en `registro_ia.md`)

| Caso | Uso declarado en el informe | Verificación declarada | Estado del registro |
| :---- | :---- | :---- | :---- |
| Sistemas lineales | Revisar los tres ejercicios manuales (sustitución, Cramer, Gauss-Jordan), detectar errores y comprobar soluciones | Comparación contra el desarrollo manual | Prompt incluido; falta fecha, herramienta y modelo |
| Sistemas no lineales | Revisar el manejo conceptual de Newton, punto fijo y comparación de despejes | Contraste con el desarrollo propio y el código | Prompt incluido; falta fecha, herramienta y modelo |
| Diseño de la app | Mejorar las pestañas (paneles, entradas interactivas y espacio de interpretación) | Ejecución de la app; el equipo reporta menos de 10 errores, de notación, librerías faltantes o archivos en distintas carpetas | Prompt incluido; falta fecha, herramienta y modelo |
| Lagrange, Newton, spline, datos USGS, redacción del informe | **No documentado** | — | **\[Pendiente\]**: documentar o declarar "Sin uso de IA" |

Postura del Integrante B: la IA es un copiloto de productividad pero no reemplaza el criterio ingenieril; la usará en tareas repetitivas o borradores y exigirá verificación manual o con bibliotecas formales. Postura del Integrante A: útil como crítico que revisa los procesos y para acelerar el diseño de la app.

---

## 7\. Próximos pasos inmediatos

1. Descargar la serie oficial de USGS y repetir cuadernos, app e informe.  
2. Quitar `input()` de los Cuadernos 1 y 2, unificar rutas y módulos, y guardar las salidas.  
3. Limpiar el informe, agregar Referencias y exportar a Word y PDF.  
4. Completar el registro de IA y las reflexiones individuales.  
5. Hacer commit de todo y revisar la lista final de `ToDo.md` (§6).