# ToDo.md — Workshop 2 · Sistemas de ecuaciones e interpolación

**Equipo:** Jose Manuel Arboleda Carvajal · Gabriel David Castaño **Asignatura:** Algoritmos Numéricos — Ingeniería Civil, Universidad del Quindío **Última actualización:** 3 de noviembre de 2026

---

## 1\. Resumen del estado

| Entregable de la guía | Estado | Observación breve |
| :---- | :---- | :---- |
| 5 cuadernos Jupyter | `[~]` | Existen los 5, pero 1 y 2 usan `input()` y casi ninguno guarda salidas |
| Módulos compartidos | `[~]` | Funcionan, pero están duplicados en `app/` y `Cuadernos/` |
| Aplicativo Streamlit (4 pestañas) | `[x]` | `app/app.py` \+ una pestaña por módulo; falta ampliar `requirements.txt` |
| Datos originales y procesados | `[ ]` | El `.rdb` local parece sintético; faltan los CSV que cita el informe |
| Informe en Markdown, PDF y Word | `[~]` | Hay `.md` y `.pdf`; **no hay Word**; el `.md` tiene residuos de edición |
| 12 desarrollos manuales por integrante | `[~]` | Hay evidencia, pero faltan escaneos (Anexo D) y hay huecos de cobertura |
| Registro de IA y prompts por caso | `[~]` | Hay 3 prompts en el informe; faltan campos exigidos por la guía |
| Reflexión por integrante | `[~]` | B tiene dos momentos concretos; A necesita reforzarse |
| PLAN.md, ToDo.md, history.md | `[~]` | `plan_de_trabajo.md` debe renombrarse a `PLAN.md` |

---

## 2\. 🔴 Críticos (bloquean la entrega o la validez de los resultados)

### 2.1 Datos reales (Cuarta parte, criterio de "Validación e interpretación")

- [x] **Reemplazar `app/data/usgs_caudal_diario.rdb` por una descarga real** de USGS (estación 01646500, parámetro 00060, estadístico 00003\) desde `waterdata.usgs.gov`. *(AB, prioridad máxima)*  
  - El archivo actual muestra rampas casi perfectas con reinicios periódicos, valores con decimales (p. ej. 5451.5) y el encabezado dice «UPPER DAMSITE». El propio informe reconoce estas anomalías.  
  - La guía indica que la comparación **requiere la base real**; con datos sintéticos el análisis no cumple.  
- [x] Guardar el original intacto en `data/original/` y la copia limpia en `data/procesado/`, con institución, URL o consulta, **fecha de acceso**, variables, unidades y condiciones de uso. *(B)*  
- [x] Crear `data/usgs_valores_excluidos.csv`: el informe lo cita, pero ningún código lo genera y no está en el ZIP. *(B)*  
- [x] Confirmar si `data/usgs_procesado.csv` se genera al ejecutar `datos.cargar(guardar=True)` y entregarlo ya generado. *(B)*  
- [x] Revisar los códigos de calidad tras la nueva descarga. El informe menciona un valor provisional (código P, 10 de junio), pero el `.rdb` actual **no contiene ninguna fila con código P**; solo tiene tres filas `Eqp` (15–17 de marzo). *(B)*  
- [x] **Re-ejecutar todo y actualizar cifras** del informe: tabla de MAE/RMSE/E\_max, residuales en nodos, conclusiones sobre Runge y mediana/rango de la serie. *(B)*

### 2.2 Reproducibilidad desde kernel limpio (30 % de la nota)

- [x] **Cuadernos 1 y 2:** reemplazar los `input()` por casos definidos en el código (o una celda de parámetros), para que se ejecuten sin intervención. *(A)*  
- [x] **Cuadernos 3, 4 y 5:** `datos.cargar()` usa la ruta relativa `data/usgs_caudal_diario.rdb`, y `Cuadernos/` no tiene carpeta `data/`. Desde ahí el código cae a datos **sintéticos** sin avisar en el cuaderno. Unificar las rutas (por ejemplo, ruta relativa a la raíz del repositorio). *(B)*  
- [x] Ejecutar **Kernel → Restart & Run All** en los 5 cuadernos y **guardarlos con salidas** (hoy solo el Cuaderno 1 tiene alguna). *(AB)*  
- [x] Una sola implementación de cada método: hoy `ModLab2.py`, `ModLab3.py`, `datos.py`, `interpolacion.py` y `metricas.py` están **duplicados** en `app/` y `Cuadernos/`. Moverlos a una carpeta común (p. ej. `modulos/`) e importarlos desde ambos sitios. *(AB)*  
- [x] Completar `app/requirements.txt`: hoy lista `streamlit`, `numpy`, `matplotlib`, pero el código también importa **`pandas`** y **`scipy`**. Añadir `jupyter`/`nbformat` si se ejecutan cuadernos. *(AB)*  
- [x] Escribir un `README.md` con instrucciones de ejecución, dependencias, entradas, tolerancias y condiciones de salida (lo pide la guía en "Entregables"). *(AB)*

### 2.3 Informe

- [x] **Generar la versión Word** (`informe.docx`) desde el mismo Markdown y revisar ecuaciones, tablas y figuras. *(AB)*  
- [x] **Eliminar las 75 marcas residuales `[cite: …]`** del `informe.md` (aparecen en el anexo del Integrante B). *(B)*  
- [x] Añadir sección de **Referencias** (guía, diapositivas de clase 07–10, USGS, SciPy, Streamlit y cualquier otra fuente usada). No existe hoy. *(AB)*  
- [x] Regenerar `informe.pdf` después de todos los cambios y comprobar que las tres versiones comuniquen las mismas cifras. *(AB)*

---

## 3\. 🟠 Importantes (afectan la nota individual o la coherencia)

### 3.1 Desarrollo manual (20 % individual)

- [x] Incluir los **escaneos o fotos** de los desarrollos a mano: el informe remite a un "Anexo D" que no existe en el ZIP. Cada hoja debe estar identificada por autor y ejercicio. *(A y B)*  
- [x] **Bloque 10 del Integrante B:** la tabla del informe lista dos casos de Newton (Ej. 10 con 3 nodos y Ej. 11 que agrega un nodo) y un spline (Ej. 12). La guía pide **tres casos de Newton** (3 nodos, 4 nodos y uno que incorpore un nodo). Falta el caso de 4 nodos, o aclarar que el spline va aparte. *(B)*  
- [x] **Bloque 07 del Integrante A:** el informe describe sustitución (2×2), Cramer (3×3) y Gauss-Jordan (4×4). La guía exige que **un caso requiera intercambio de filas** y que se muestre la elección del pivote. Verificar que esté en la evidencia de A o agregarlo. *(A)*  
- [x] **Bloque 08:** confirmar que cada integrante tiene al menos **3 actualizaciones** por método o trayectoria, o justificar la parada anticipada. *(A y B)*  
- [x] **Numeración inconsistente:** el informe numera Lagrange como Ej. 7–9 y Newton como 10–12, pero el Cuaderno 3 habla de "Ej. 7 (2 nodos)", "Ej. 10 (2 nodos, x=3)" y el Cuaderno 4 de "Ej. 12, 13, 14". Alinear la numeración en informe, cuadernos y anexos. *(B)*  
- [x] En cada ejercicio, dejar explícito: fuente, enunciado original, qué se ajustó, por qué y cómo se comprobó. *(A y B)*

### 3.2 Registro de IA (parte de la rúbrica compartida)

- [x] Crear `registro_ia.md` (o un anexo) con, **por caso**: fecha, autor, archivos afectados, herramienta y modelo tal como se muestran (o "no informado"), propósito, contexto suministrado, **prompt exacto**, respuesta o fragmento usado, qué se aceptó/modificó/descartó, **verificación independiente** y pendientes. *(A: bloques 07–08 · B: bloques 09–10 y spline)*  
- [x] Hoy el informe documenta tres prompts (lineales, no lineales y diseño de la app). Faltan los de Lagrange, Newton, spline, datos USGS y redacción del informe, **o declarar "Sin uso de IA"** en cada uno. *(A y B)*  
- [x] Si no se conserva el prompt literal, decirlo y **no reconstruirlo de memoria**. Retirar credenciales y datos personales. *(A y B)*  
- [x] Declarar si se usó IA para preparar las reflexiones. *(A y B)*

### 3.3 Reflexión individual (10 %)

- [x] **Integrante A:** hoy describe el uso de la IA en general. La guía pide **dos momentos concretos** del laboratorio, qué decidió personalmente, cómo verificó, qué dudas quedaron, el efecto de las condiciones de trabajo y hasta dónde sostiene su conclusión. *(A)*  
- [x] **Integrante B:** ya tiene dos momentos (Newton Ej. 4 y radio espectral Ej. 6). Falta decir qué dudas permanecieron y hasta dónde se sostiene su conclusión con la experiencia realizada. *(B)*  
- [x] Revisar la voz: "Yo asumí…" aparece en la sección de roles sin nombre. Firmar cada texto con el autor. *(A y B)*

### 3.4 Aplicativo

- [x] Verificar que el aplicativo identifique, en cada pestaña, **qué cuaderno la respalda**. *(AB)*  
- [x] Confirmar que la extrapolación esté **desactivada** en la comparación principal y se muestre aparte. *(B)*  
- [x] Las capturas de `ejemplo_de_ejecucion/` solo muestran la pestaña 1 (sistema 2×2). Añadir al menos una captura por cada una de las otras tres pestañas. *(AB)*  
- [x] Comprobar que, al modificar una entrada, la app muestre qué cambia y si coincide con lo esperado. *(AB)*

---

## 4\. 🟡 Mejoras y limpieza

- [x] Renombrar `plan_de_trabajo.md` → `PLAN.md` (nombre que pide la guía).  
- [x] Añadir `.gitignore` (`__pycache__/`, `*.pyc`, `.ipynb_checkpoints/`) y **borrar** las carpetas `__pycache__` de la raíz y de `app/` (compiladas con Python 3.14).  
- [x] **Git:** hay cambios sin confirmar. `git status` muestra `Cuaderno_1.ipynb`, `Cuaderno_2.ipynb` y `ModLab2.py` como eliminados de la raíz, y `app/`, `Cuadernos/`, `informe.*` y `ejemplo_de_ejecucion/` sin seguimiento. Hacer un commit con mensaje descriptivo y confirmar que los dos integrantes aparecen como autores. Hoy solo hay dos commits, ambos de Jose.  
- [x] Corregir erratas del informe: "Intitución", "Faculdad", "Guss-Jordan", "consisite", "presición", "estenso", "pesatañas", "Rflección", "Newthon", "triaticulado", "carva", "Sleccionar", "nungún", "datoa", "Linelaes" (títulos del Cuaderno 2), "Intrepretacion", "excato".  
- [x] Ajustar `\\` sueltos en la portada del `.md`, que pueden imprimirse como texto en PDF o Word.  
- [x] En el informe, el anexo de Lagrange del Integrante A y el de Newton usan formatos de tabla distintos; unificar.  
- [x] Revisar la redacción de que la IA cometió "menos de 10" errores: respaldar la cifra con el registro o suavizarla.  
- [x] Añadir una sentencia en las conclusiones indicando que los hallazgos sobre Runge dependen de la partición elegida y de la base real definitiva.

---

## 5\. ✅ Hecho (con evidencia localizada)

**Sistemas (A)**

- [x] Módulo `ModLab2.py`: sistemas lineales, punto fijo, Newton para sistemas, historial, errores personalizados y gráficas.  
- [x] `modelos_estructurales.py` y `graficos_estructurales.py` (modelos de ingeniería de la app).  
- [x] Cuaderno 1 (lineales) con sección de análisis del residuo y evidencias de A y B.  
- [x] Cuaderno 2 (no lineales) con análisis de tolerancia y control de actualizaciones.  
- [x] Pestañas 1 y 2 de la app (`pestana_lineales.py`, `pestana_no_lineales.py`).

**Interpolación (B)**

- [x] Módulos `interpolacion.py`, `datos.py`, `metricas.py` y `ModLab3.py` (Lagrange, diferencias divididas, inserción de nodos, spline natural y contraste con SciPy).  
- [x] Cuadernos 3, 4 y 5, con contraste frente a bibliotecas, reproducción de nodos, errores con signo y partición común.  
- [x] Spline manual con 3 nodos (momentos M₀=M₂=0, M₁=−3) incorporado una sola vez en el Cuaderno 5\.  
- [x] Control de calidad automático de la serie (`datos.control_calidad`), que detectó las tres anomalías del archivo.  
- [x] Pestañas 3 y 4 con datos compartidos (`bloque_datos_compartidos` en `app.py`).

**Conjunto**

- [x] `app/app.py` con cuatro pestañas y barra lateral compartida.  
- [x] Informe en Markdown y PDF con anexos de Lagrange y Newton.  
- [x] Secuencia de capturas de ejecución (`ejemplo_de_ejecucion/1.png`–`10.png`).  
- [x] Plan de trabajo con roles y reparto de módulos.

---

## 6\. Lista de verificación final (antes de entregar)

Basada en la sección "Entregables" de la guía.

- [x] Carpeta ordenada con cuadernos, módulos, app, datos, informe, evidencias y registros.  
- [x] Los 5 cuadernos se ejecutan desde kernel limpio y quedan guardados con salidas.  
- [x] Un solo juego de módulos; instrucciones de ejecución, dependencias, entradas, tolerancias y condiciones de salida.  
- [x] La app arranca con `streamlit run app.py` en un entorno nuevo (`pip install -r requirements.txt`).  
- [x] Datos **reales** originales y procesados, con fuentes, ajustes y partición construcción/validación.  
- [x] Informe en **`.md`, `.pdf` y `.docx`** con las mismas cifras y sin marcas residuales.  
- [x] 12 desarrollos manuales por integrante, legibles e identificados.  
- [x] Reflexión de cada integrante dentro del informe o sus anexos.  
- [x] Registro de IA y prompts por caso, con verificaciones, o declaración de "Sin uso de IA".  
- [x] `PLAN.md`, `ToDo.md` e `history.md` actualizados.  
- [x] Cada integrante puede **explicar una decisión y reproducir un paso** con sus evidencias.