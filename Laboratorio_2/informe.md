# Informe Laboratorio 2 - Workshop 02: Sistemas de Ecuaciones e Interpolación

## Introducción

En el presente informe se describen los métodos empleados para resolver los ejercicios del Workshop 02, abordando sistemas de ecuaciones lineales y no lineales, así como los interpoladores de Lagrange y Newton. Asimismo, se analiza la importancia de las tolerancias, el residuo, el control de las actualizaciones en métodos iterativos y los criterios de convergencia como elementos fundamentales para interpretar y evaluar la precisión de las soluciones obtenidas.

Adicionalmente, se presenta una breve descripción del desarrollo de la aplicación web, explicando cómo se implementan los métodos numéricos y su aplicación en diferentes contextos de la ingeniería civil. Se destacan sus ventajas para resolver problemas de manera eficiente y precisa, proporcionando ejemplos relacionados con los ejercicios planteados en la guía del Workshop 02.

Se destaca que la implementación modular permitió mantener una estructura organizada durante el desarrollo de la aplicación, simplificando el proceso de programación y facilitando la creación de una herramienta funcional y eficiente.

También se incluye un análisis del uso de la inteligencia artificial durante el desarrollo del Workshop 02, especificando sus aplicaciones, su utilidad en el proceso de elaboración y las reflexiones individuales de cada integrante sobre su experiencia y aprovechamiento.

Finalmente, se presenta un ejemplo de ejecución de la aplicación web, mostrando ejercicios previamente seleccionados y los resultados obtenidos.

---

## Sistemas lineales

Uno de los puntos principales dentro del Workshop 02 es resolver ejercicios manualmente, en este espacio se explica como se llevaron a cabo los ejercicios de sistemas lineales, resolviendo ecuaciones de tamaño $2 \times 2,\quad 3 \times 3 \quad$ y $\quad 4 \times 4$, aplicando distintos métodos vistos en clase.

### Sistemas $2 \times 2$:

En el análisis de los sistemas $2 \times 2$, las soluciones a dichos sistemas se determinaron con métodos simples, como el de sustitución, este consiste en despejar una incógnita de una de las dos ecuaciones, reemplazarla en la ecuación restante, aplicar operaciones simples para determinar el valor de una incógnita, reemplazar ese valor hallado en cualquiera de las ecuaciones y determinar la incógnita restante. Para contextualizar mejor este procedimiento, se mostrará su uso en el siguiente ejemplo:

Considerando el sistema de ecuaciones lineales hecho manualmente:

$$
\begin{cases}
2x + 3y = 11 \quad \text{--- (Ecuación 1)} \\
4x + y = 14 \quad \text{--- (Ecuación 2)}
\end{cases}
$$

#### **Paso 1: Despejar una variable**
Elegimos la variable más sencilla de despejar. En este caso, despejamos $y$ en la **Ecuación 2**:

$$
4x + y = 14 \implies y = 14 - 4x \quad \text{--- (Ecuación 3)}
$$

#### **Paso 2: Sustituir la variable despejada**
Sustituimos la expresión de $y$ (Ecuación 3) en la **Ecuación 1**:

$$
2x + 3(14 - 4x) = 11
$$

#### **Paso 3: Resolver la ecuación lineal resultante**
Desarrollamos y agrupamos términos semejantes para encontrar el valor de $x$:

$$
\begin{aligned}
2x + 42 - 12x &= 11 \\
-10x + 42 &= 11 \\
-10x &= 11 - 42 \\
-10x &= -31 \\
x &= \frac{-31}{-10} \implies \mathbf{x = \frac{31}{10}}
\end{aligned}
$$

#### **Paso 4: Encontrar la segunda variable**
Sustituimos el valor hallado $x = \frac{31}{10}$ en la **Ecuación 3** (la que ya teníamos despejada):

$$
y = 14 - 4(\frac{31}{10}) \implies y = 14 - \frac{62}{5} \implies \mathbf{y = \frac{8}{5}} 
$$

#### **Paso 5: Verificación del resultado**
Comprobamos que el punto $(x, y) = (\frac{31}{10}, \frac{8}{5})$ satisface ambas ecuaciones originales:

* **Ecuación 1:** $2(\frac{31}{10}) + 3(\frac{8}{5}) = \frac{31}{5} + \frac{24}{5} = 11 \quad \checkmark$
* **Ecuación 2:** $4(\frac{31}{10}) + (\frac{8}{5}) = \frac{62}{5} + \frac{8}{5} = 14 \quad \checkmark$

**Solución del sistema:**

$$
\mathbf{(x, y) = (\frac{31}{10}, \frac{8}{5})}
$$

Este sistema se destaca por ser sencillo de resolver, ya que no necesita más que operaciones simples (despejes, suma, resta, multiplicación o división) para ser resuelto.

---

### Sistemas $3 \times 3$

Para los sistemas $3 \times 3$ existen diversos métodos para encontrar sus soluciones, uno de ellos es el método de cofactores implementando la regla de Cramer, este consisite en calcular el determinante de una matriz, luego se reemplaza el vector de valores independientes por la columna respectiva para hallar la incognita deseada,para $x$ se reemplaza la columna 1, para $y$ la columna 2 y para $z$ la columna 3, se calcula determianante de la nueva matriz generada y se divide entre el determinante de la matriz original previamente calculado, esto se explica detalladamente a continuación:    

$$
\begin{bmatrix}
a_{11} & a_{12} & \cdots & a_{1n} \\
a_{21} & a_{22} & \cdots & a_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
a_{n1} & a_{n2} & \cdots & a_{nn}
\end{bmatrix}
\begin{bmatrix}
x_1 \\
x_2 \\
\vdots \\
x_n
\end{bmatrix}
= \begin{bmatrix}
b_1 \\
b_2 \\
\vdots \\
b_n
\end{bmatrix}
$$

El valor de cada incógnita $x_i$ se calcula como la razón de dos determinantes:

$$
x_i = \frac{\det(A_i)}{\det(A)}
$$

Donde $A_i$ es la matriz formada al reemplazar la $i$-ésima columna de la matriz $A$ por el vector de términos independientes $\mathbf{b}$:

$$
A_i = 
\begin{bmatrix}
a_{11} & \cdots & b_1 & \cdots & a_{1n} \\
a_{21} & \cdots & b_2 & \cdots & a_{2n} \\
\vdots & \ddots & \vdots & \ddots & \vdots \\
a_{n1} & \cdots & b_n & \cdots & a_{nn}
\end{bmatrix}
$$

**Ejemplo para un sistema $3 \times 3$:**

$$
x_1 = \frac{\begin{vmatrix} b_1 & a_{12} & a_{13} \\ b_2 & a_{22} & a_{23} \\ b_3 & a_{32} & a_{33} \end{vmatrix}}{\det(A)}, \quad
x_2 = \frac{\begin{vmatrix} a_{11} & b_1 & a_{13} \\ a_{21} & b_2 & a_{23} \\ a_{31} & b_3 & a_{33} \end{vmatrix}}{\det(A)}, \quad
x_3 = \frac{\begin{vmatrix} a_{11} & a_{12} & b_1 \\ a_{21} & a_{22} & b_2 \\ a_{31} & a_{32} & b_3 \end{vmatrix}}{\det(A)}
$$

Este método fue empleado para resolver uno de los ejercicios realizados manualmente, se observo que este método es un poco más extenso que el anterior, sin embargo, también se destaca por su sencillez a la hora de resolverlo, si se tiene buen conocimiento del cálculo de determinantes, o se cuenta con un software que pueda realizarlo, es sencillo llegar las soluciones del sistema.

---

### Sistemas $4 \times 4$:

Para los sistemas $4 \times 4$ el cálculo de sus soluciones se vuelve más complejo, ya que los métodos vistos anterioremente son más difíciles de aplicar o directamente no se pueden hacer, como los métodos de cofactores con regla de Cramer y sustitución respectivamente.

Para dar solución a estos sistemas existe el método de reducción Guss-Jordan, este consisite en igualar la matriz de coeficientes e igularla al vector de variables independientes, reducir la matriz de coeficientes a la matriz identidad mediante operaciones elementales (suma, resta, multiplicación o división) entre sus filas, luego se comparan con los valores obtenidos en el vector de variables independientes, los cuales serán las soluciones del sistema, como se ve a continuación:

Dado el sistema de ecuaciones $4 \times 4$:

$$
\begin{bmatrix}
a_{11} & a_{12} & a_{13} & a_{14} & \mid & b_1 \\
a_{21} & a_{22} & a_{23} & a_{24} & \mid & b_2 \\
a_{31} & a_{32} & a_{33} & a_{34} & \mid & b_3 \\
a_{41} & a_{42} & a_{43} & a_{44} & \mid & b_4
\end{bmatrix}
$$

**Estructura Algorítmica (Paso a Paso)**

1. **Pivote 1 ($a_{11}$):**
   * Se normaliza la Fila 1 dividiendo por el pivote: $F_1 \to \frac{F_1}{a_{11}}$.
   * Se hacen cero todos los elementos debajo de $a_{11}$ en la Columna 1:
     $$F_i \to F_i - a_{i1} F_1 \quad \text{para } i = 2, 3, 4$$

2. **Pivote 2 ($a_{22}$):**
   * Se normaliza la Fila 2 dividiendo por el nuevo pivote: $F_2 \to \frac{F_2}{a_{22}}$.
   * Se hacen cero los elementos por encima y por debajo de $a_{22}$ en la Columna 2:
     $$F_i \to F_i - a_{i2} F_2 \quad \text{para } i = 1, 3, 4$$

3. **Pivote 3 ($a_{33}$):**
   * Se normaliza la Fila 3: $F_3 \to \frac{F_3}{a_{33}}$.
   * Se hacen cero los elementos restantes de la Columna 3:
     $$F_i \to F_i - a_{i3} F_3 \quad \text{para } i = 1, 2, 4$$

4. **Pivote 4 ($a_{44}$):**
   * Se normaliza la Fila 4: $F_4 \to \frac{F_4}{a_{44}}$.
   * Se hacen cero los elementos por encima de $a_{44}$ en la Columna 4:
     $$F_i \to F_i - a_{i4} F_4 \quad \text{para } i = 1, 2, 3$$


**Forma Matricial Final**

Al finalizar las operaciones de eliminación, el sistema adopta la siguiente forma reducida:

$$
\begin{bmatrix}
1 & 0 & 0 & 0 & \mid & x_1 \\
0 & 1 & 0 & 0 & \mid & x_2 \\
0 & 0 & 1 & 0 & \mid & x_3 \\
0 & 0 & 0 & 1 & \mid & x_4
\end{bmatrix}
$$

Donde los valores del vector solución se leen de forma directa sin necesidad de sustitución hacia atrás:

$$
\mathbf{x} = \begin{bmatrix} x_1 \\ x_2 \\ x_3 \\ x_4 \end{bmatrix}
$$

El método de reducción Gauss-Jordan se aplicó para resolver varios ejercicios manualmente, se observó que este método es un poco estenso, ya que para algunos fue necesario hacer más de 15 operaciones elementales, este llega a ser más complejo ya que se debe tener mucho cuidado con que operacios aplicar a las filas, pero se destaca por su confiabilidad y presición para hallar las soluciones de sistmeas de ecuaciones complejos. 

---

## Sistemas no lineales

Los métodos numéricos para resolver sistemas no lineales son procedimientos iterativos que permiten encontrar soluciones aproximadas a sistemas en los que las variables están relacionadas mediante funciones no lineales. Estos métodos generan sucesivas aproximaciones hasta alcanzar un nivel de precisión establecido mediante una tolerancia.

Al igual que en los sistemas lineales, existen diversos métodos para resolver sistemas de ecuaciones no lineales, destacando Newton-Raphson y Punto Fijo, los cuales se emplearon para solucionar manualmente ejercicios de sistemas de dimensiones $2 \times 2,\quad 3 \times 3 \quad$ y $\quad 4 \times 4$. 

### Newton-Raphson:

Este método emplea las derivadas de las funciones del sistema para calcular nuevas aproximaciones a partir de valores iniciales, buscando reducir el error hasta cumplir cun una tolerancia hasta llegar a la solución con la precisión deseada. Este proceso se explica de mejor manera a continuación:

**Resumen del proceso en 3 Pasos**

1. **Linealización Local mediante Series de Taylor:** 
   Debido a la complejidad analítica de las superficies no lineales, el método aproxima localmente el sistema de funciones en la vecindad del punto iterativo actual $\mathbf{x}^{(k)}$. Se utiliza una expansión en Serie de Taylor multivariable truncada en su término de primer orden, sustituyendo el sistema curvo por un plano tangente hiperbólico.

2. **Operador de Cambio: La Matriz Jacobiana ($J$):** 
   La matriz Jacobiana actúa como el operador diferencial del sistema. Representa la transformación de derivadas parciales de primer orden, definiendo la dirección de máxima pendiente y la sensibilidad de cada ecuación respecto al cambio en las variables independientes.

3. **Corrección Vectorial e Iteración:** 
   Se resuelve el sistema lineal generado para determinar el vector de desplazamiento o incremento $\Delta \mathbf{x}^{(k)}$. Este vector ajusta la aproximación actual proyectándola hacia la intersección de los planos tangentes. El proceso se repite sucesivamente mediante la relación de recurrencia $\mathbf{x}^{(k+1)} = \mathbf{x}^{(k)} + \Delta \mathbf{x}^{(k)}$ hasta alcanzar la convergencia numérica según la tolerancia especificada.

**Esquema del Proceso**

$$
\text{Punto Nuevo} = \text{Punto Actual} + \text{Paso de Corrección}
$$

$$
\begin{bmatrix} x_{k+1} \\ y_{k+1} \end{bmatrix} = \begin{bmatrix} x_k \\ y_k \end{bmatrix} + \begin{bmatrix} \Delta x \\ \Delta y \end{bmatrix}
$$

**Pasos para Resolver un Ejercicio en la Práctica**

- **Paso 1: Armar la Jacobiana $J(x,y)$**
  Derivar cada función respecto a cada variable:

  ```math
  J(x,y) = \begin{bmatrix}
  \frac{\partial f_1}{\partial x} & \frac{\partial f_1}{\partial y} \\
  \frac{\partial f_2}{\partial x} & \frac{\partial f_2}{\partial y}
  \end{bmatrix}
  ```

- **Paso 3: Encontrar los incrementos ($\Delta x, \Delta y$)**
  Resolver el sistema de ecuaciones lineales:

  ```math
  J \cdot \begin{bmatrix} \Delta x \\ \Delta y \end{bmatrix} = -\begin{bmatrix} f_1 \\ f_2 \end{bmatrix}
  ```

- **Paso 4: Actualizar y repetir**
  Sumar los incrementos del punto anterior para obtener $(x_1, y_1)$. Si los incrementos son casi cero (menores a una tolerancia establecida), el método se detiene ya que ha econtrado una solución.

El método de Newton-Raphson destaca por su rápida convergencia, cuando se realizaron los ejercicios manuales, se pudo observar que este método cumplió con la tolerancia en una iteración, máximo dos, aunque esto no se pueda asegurar que esto sea igual para todos los casos.

### Punto fijo:

Este método transforma las ecuaciones del sistema en expresiones donde las variables dependen de si mismas, al igual que Newton-Raphson, este utiliza valores inciales para calcular sucesivas aproximaciones hasta que los cambios entre iteraciones cumplan con un criterio de parada establecido.

En este método se realizan despejes de las incógnitas de las funciones según el tamaño del sistema, luego se derivan parcialmente estos despejes, se evaluan los valores iniciales y se hace su criterio de convergencia, esto se explica mejor a continuación:

**1. Estructura General de Despejes**

Dado el sistema original de $n$ ecuaciones no lineales:

$$
\begin{cases}
f_1(x_1, x_2, \dots, x_n) = 0 \\
f_2(x_1, x_2, \dots, x_n) = 0 \\
\quad \vdots \\
f_n(x_1, x_2, \dots, x_n) = 0
\end{cases}
$$

Se despeja la variable $x_i$ de la $i$-ésima ecuación para construir las **funciones de iteración** $g_i$:

$$
\begin{aligned}
\text{De } f_1(x_1, x_2, \dots, x_n) = 0 &\implies x_1 = g_1(x_1, x_2, \dots, x_n) \\
\text{De } f_2(x_1, x_2, \dots, x_n) = 0 &\implies x_2 = g_2(x_1, x_2, \dots, x_n) \\
&\ \ \vdots \\
\text{De } f_n(x_1, x_2, \dots, x_n) = 0 &\implies x_n = g_n(x_1, x_2, \dots, x_n)
\end{aligned}
$$

El esquema iterativo de evaluación adopta la forma:

$$
\begin{aligned}
x_1^{(k+1)} &= g_1(x_1^{(k)}, x_2^{(k)}, \dots, x_n^{(k)}) \\
x_2^{(k+1)} &= g_2(x_1^{(k)}, x_2^{(k)}, \dots, x_n^{(k)}) \\
&\ \ \vdots \\
x_n^{(k+1)} &= g_n(x_1^{(k)}, x_2^{(k)}, \dots, x_n^{(k)})
\end{aligned}
$$

**2. Criterio de Evaluación de Convergencia**

La convergencia del método depende directamente de la elección de las funciones de despeje $g_i$. Para garantizar que el proceso iterativo converja hacia la solución, la suma del valor absoluto de las derivadas parciales de cada función debe ser estrictamente menor a 1 en la vecindad del punto evaluado:

$$
\sum_{j=1}^{n} \left| \frac{\partial g_i}{\partial x_j} \right| < 1 \quad \text{para todo } i = 1, 2, \dots, n
$$

**3. Caso Particular: Sistemas $2 \times 2$**

Para un sistema no lineal bidimensional de variables $(x, y)$:

$$
\begin{cases}
f_1(x, y) = 0 \implies x = g_1(x, y) \\
f_2(x, y) = 0 \implies y = g_2(x, y)
\end{cases}
$$

**Esquema Iterativo:**

$$
\begin{cases}
x_{k+1} = g_1(x_k, y_k) \\
y_{k+1} = g_2(x_k, y_k)
\end{cases}
$$

**Condiciones de Convergencia:**

$$
\left| \frac{\partial g_1}{\partial x} \right| + \left| \frac{\partial g_1}{\partial y} \right| < 1
$$

$$
\text{y}
$$

$$
\left| \frac{\partial g_2}{\partial x} \right| + \left| \frac{\partial g_2}{\partial y} \right| < 1
$$

Este se destaca por simplicidad de implementación, realizando los ejercicios se notó que este es más extenso a comparación del método de Newton-Raphson, pero esto se compensa con facilidad para entenderlo, ya que solo se necesita hacer los depejes y las derivadas una sola vez, luego se evalúan los valores iniciales, se observa que función cumple con el criterio de convergencia, actualizar los valores y repetir el proceso hasta cumplir con la tolerancia establecida.

### Control de actualizaciones

Algo importante a destacar en estos métodos es el control de actualizaciones, esto hace referencia al cambio de valores ingresados para calcular las aproximaciones, su control es esencial para supervisar los cambios de las variables en cada iteración y determinar si las aproximaciones están convergiendo hacia una solución. Su importancia radica en que permite evaluar la estabilidad del procedimiento, detectar posibles divergencias y establecer cuándo se ha alcanzado una precisión aceptable. De esta manera, se evitan iteraciones innecesarias y se mejora la confiabilidad de los resultados numéricos.

---

### Análisis del residuo $Ax - b$

El residuo $Ax - b$ (denotado matemáticamente como $\mathbf{r}$) es un vector que mide el error o la diferencia entre una solución aproximada y la solución exacta de un sistema de ecuaciones lineales de la forma $Ax = b$.

En términos prácticos, cunado se intenta resolver un sistema mediante métodos numéricos o aproximados (como Gauss-Seidel o Gauss-Jordan con decimales), es común que no se encuentren los valores precisos de las incógnitas debido a errores de aproximación o truncamiento. El residuo cuantifica que tan lejos está la respuesta correcta.

Este permite verificar la calidad de las soluciones obtenidas, identificando errores en los cálculos, facilitando el control de la presición.

Este tiene diversas aplicaciones, como se explicó anteriormente, este es utilizado en el método de Gauss-Seidel y Gauss-Jordan con decimales, mientras que en la ingeniería civil se aplica en muchas situaciones donde se necesita comprobar la confiabilidad del análisis numérico, donde se destaca su uso en el análisis estructural.

Este se agregó dentro de la aplicación, en la pestaña de sistemas no lineales para dar un criterio de confianza para los calculos realizados por el programa. 

---

### Desarrollo de la app web

El desarrollo de la app fue sencillo, en la guía del Workshop 02 se establece como debe ser el diseño, este debe contar con 4 pesatañas que se dividen de la siguiente forma:

- **Pestaña 1:** En esta pestaña implementamos las funciones de sistemas de ecuaciones lineales, planteamos tres situaciones de ingeniería para sistemas de ecuaciones de tamaño $\quad 2 \times 2 \quad$, $3 \times 3 \quad$ y $\quad 4 \times 4 \quad$, para el sistema $\quad 2 \times 2 \quad$ planteamos el diseño de una viga simplemente apoyada a la que se le aplica una carga puntual, para el sistema $\quad 3 \times 3 \quad$ planteamos el diseño de una viga con un apoyo fijo y otro movil a la cual se le palica una carga inclinada, y para el sistema $\quad 4 \times 4 \quad$ un arco triaticulado al que se le aplica una carva vertical, las funciones se construyeron partir de las ecuaciones de equilibrio, ya que estás cuentan con la particularidad de que siempre están igualadas a 0. El usuario puede modificar parámetros como la longitud de la viga, la magnitud de la fuerza que se le aplica y el programa devolverá la magnitud de sus reacciones.

- **Pestaña 2:** En esta pestaña implementamos las funciones de sistemas de ecuaciones no lineales, planteamos al análisis estrucutral de estructuras grandes, escogimos el análisis de edificios de 2, 3 y 4 pisos para representar los sistemas de ecuaciones de distintos tamaños, las funciones se construyeron al rededor de las ecuaciones de equilibrio. El usuario puede modificar parámetros como la magnitud de las cargas laterales, el coeficiente de rigidización no lineal, el método que desea emplear para resolver el sistema y la tolerancia que se debe cumplir, el programa devolverá un historial iterativo, gráficas comparando el error en cada iteración y el residuo obtenido.

- **Pestaña 3:** En esta pestaña implementamos el método de interpolación de Lagrange aplicado a la reconstrucción de series de caudal diario con datos faltantes. Planteamos la evaluación mediante un enfoque global y local en ventanas de $k$ nodos. Las bases del polinomio se construyeron a partir del producto de diferencias finitas en los nodos conocidos. El usuario puede interactuar seleccionando la cantidad de nodos locales alrededor de la consulta, así como modificar el día $t$ a evaluar dentro del rango de la serie. El programa devuelve la tabla detallada del cálculo de los coeficientes $L_i(t)$, métricas globales y locales de error (MAE, RMSE, $E_{\text{máx}}$), un análisis del fenómeno de Runge para evaluar la estabilidad de grados altos y gráficas comparativas de las bases de interpolación y el comportamiento del caudal.

- **Pestaña 4:** En esta pestaña implementamos la interpolación polinomial de Newton mediante la tabla de diferencias divididas y la comparamos con el método de splines cúbicos naturales por tramos. El análisis se planteó sobre la misma serie de caudales e igual partición de datos para garantizar una comparación equitativa entre una aproximación global y una construcción por segmentos. El usuario puede modificar el número de nodos de la tabla, definir el nodo inicial de la ventana, cambiar el día de consulta e incorporar nodos adicionales en tiempo real para verificar la conservación de coeficientes. El programa devuelve las tablas de diferencias divididas, los momentos y ecuaciones de tramo del spline cúbico, la cuantificación del acuerdo numérico con otras implementaciones y gráficas comparativas de los errores residuales frente a las observaciones reservadas.

Para hacer más simple el diseño de la app construimos el código haciendo uso de un sistema modular, con el fin de no implementar el código en un solo archivo que fuera muy extenso y difícil de desarrollar, creamos dos módulos principales, el módulo "ModLab2.py" contiene las funciones de los sistemas lineales y no lineales, así como las funciones necesarias para gráficar, el módulo "ModLab3.py" contiene las funciones de interpolador de Lagrange y el interpolador de Newton, y también cuentan con funciones para gráficar. Diseñamos 4 módulos para cada pestaña, cada módulo contiene el diseño de las pestañas, por ejemplo, para la pesatña de sistemas de ecuaciones lineales, el módulo "pestanas_lineales.py" importa las funciones que solucionan sistemas lineales del módulo "ModLab2.py", se diseña la pestaña dentro del módulo, una vez hecho el diseño, el módulo "pestanas_lineales.py" se importa al main principal que diseña la app, llamado "app.py", este proceso se repitió pra las 4 pesatñas.

La implementación de este sistema modular fue de gran importancia ya que nos permitió revisar los códigos en archivos apartes, logrando reconocer errores de manera más sencilla y poder corregirlos fácilmente, contrario a lo que hubiese sido si todo estuviera en el mismo archivo. También permitió que el main principal "app.py" sea un archivo corto y sencillo, ya que solo nos tomó 31 líneas de código programarlo.

Con esto logramos tener una estructura organizada que facilitó el desarrollo de la app.

### Uso de la IA

La IA fue implementada para comprobar las soluciones obtenidas en los ejercicios hechos a mano, comprobar si los métodos estaban correctamente implementados y si no se cometieron errores en el proceso que puedan ocasionar soluciones que no satisfagan las condiciones. Estos fueron los prompts:

- **Para sistemas lineales:**
  "En este archivo realicé tres ejercicios de sistemas de ecuaciones lineales de tamaño $\quad 2 \times 2 \quad$, $3 \times 3 \quad$ y $\quad 4 \times 4 \quad$, para el sistema $\quad 2 \times 2 \quad$ apliqué el método de sustitución, para el sistema $\quad 3 \times 3 \quad$ apliqué el método de cofactores integrando la regla de Cramer, por último, para el sistema $\quad 4 \times 4 \quad$ apliqé el método de reducción Gauss-Jordan, quiero que analices cada problema y su solución, identifica errores algebraícos o aritméticos en los procesos de los métodos que puedan causar errores en las soluciones halladas, si todo lo anterior es correcto, comprueba las soluciones."

- **Para sistemas no lineales:**
  "En este archivo realicé tres ejercicios de sistemas de ecuaciones no lineales, dos de ellos los resolví con los métodos de Newton-Raphson y punto fijo, el último es una comparación de despejes y su convergencia, quiero que revises el manejo conceptual de los procesos de cada método aplicado a los ejercicios para solucionarlos, si las soluciones a las que llegué son correctas, dame una breve explicación del ejercicio y por qué cumple con la teoría de los métods."

La IA también se utilizó para el diseño de la app, ya que nuestro conocimiento en diseño de páginas web es poco, nos apoyamos de la IA para mejorar el diseño y lograr que se vea mejor y sea fácil de comprender para quien la use. Este fue el prompt excato:

- **Diseño de la app:**
  "Los archivos que te adjunte son el módulo donde implementamos las funciones para resolver problemas de sistemas de ecuaciones lineales, sistemas de ecuaciones no lineales, interpolador de Lagrange y Newthon + spline, además, en el módulo principal incluimos funciones para gráficar los errores obtenidos en las iteraciones y gráficas que representan los datos del problema, el último archivo es un diseño previo para las pestañas que queremos diseñar para una app web, el diseño es simple, queremos que nos ayudes a mejorar las pestañas de la app para que estas incluyan paneles y casillas interactivas, que permitan al usuario modificar los valores de entrada y al final se incluya un espacio donde podamos incluir una interpretación al las soluciones obtenidas, que los mensajes incluyan las respectivas soluciones obtenidas según las modificaciones de los parámetros."     

- **Reflexión:** El uso de la IA en el desarrollo del Workshop 02 fue de gran ayuda, está nos permitió corroborar los ejercicios rápidamente, pidiendole que actúe como crítico frente a los procesos utilizados, contando con una opinión extra para asegurar que las soluciones obtenidas eran correctas y que los métodos de solución fueron correctamente implementados. Su uso para el diseño de la app web fue signifivativamente mayor, ya que está fue empleada para diseñar e implementar las funciones de los módulos a las pestañas de la app, lo que nos facilitó el proceso de diseñar paso a paso la página, cometiendo errores sucesivamente, lo que nos quitaría mucho tiempo, mientras que con el apoyo de la IA estos errores fueron contados, menos de 10, y en su mayoría eran errores de notación, por no tener una librería instalada o por no tener los módulos y el main guardados en la misma carpeta.
