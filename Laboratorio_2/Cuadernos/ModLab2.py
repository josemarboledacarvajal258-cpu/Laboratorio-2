"""ModLab2: sistemas lineales (Gauss) y no lineales (Newton-Raphson, punto fijo)."""

import math

__all__ = [
    "resolver_sistema",                                   # Cuaderno 1
    "crear_funcion", "newton_raphson", "punto_fijo",      # Cuaderno 2
    "mostrar_historial", "graficar_errores",
    "comparar_despejes", "ErrorConvergencia",
]


#Sistemas de ecuaciones lineales, método de reducción de Guass-Jordan
def resolver_sistema(A, b, tol=1e-12):
    """
    Resuelve A·x = b con eliminación de Gauss y pivoteo parcial.
    Lanza ValueError si las dimensiones no son válidas o no hay solución única.
    """
    n = len(A)
    if not 2 <= n <= 4:
        raise ValueError("Solo se admiten sistemas de 2x2 hasta 4x4.")
    if any(len(fila) != n for fila in A) or len(b) != n:
        raise ValueError("A debe ser cuadrada (nxn) y b debe tener tamaño n.")

    # Matriz aumentada [A | b]
    M = [list(map(float, A[i])) + [float(b[i])] for i in range(n)]

    # Eliminación hacia adelante
    for col in range(n):
        pivote = max(range(col, n), key=lambda f: abs(M[f][col]))
        if abs(M[pivote][col]) < tol:
            raise ValueError("El sistema no tiene solución única.")
        M[col], M[pivote] = M[pivote], M[col]

        for fila in range(col + 1, n):
            factor = M[fila][col] / M[col][col]
            for k in range(col, n + 1):
                M[fila][k] -= factor * M[col][k]

    # Sustitución hacia atrás
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        suma = sum(M[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (M[i][n] - suma) / M[i][i]
    return x



class ErrorConvergencia(ValueError):
    """Error de convergencia que conserva el historial de iteraciones."""
    def __init__(self, mensaje, historial=None):
        super().__init__(mensaje)
        self.historial = historial or []


def crear_funcion(expresiones, n):
    """Convierte textos como 'x1**2 + x2**2 - 4' en una función F(x) -> [f1, ..., fn]."""
    permitidos = {k: getattr(math, k) for k in
                  ("sin", "cos", "tan", "exp", "log", "sqrt", "pi", "e")}
    codigos = [compile(t.replace("^", "**"), "<ecuacion>", "eval") for t in expresiones]

    def F(x):
        entorno = dict(permitidos)
        for i in range(n):
            entorno[f"x{i + 1}"] = x[i]
        return [float(eval(c, {"__builtins__": {}}, entorno)) for c in codigos]

    return F


def jacobiana_numerica(F, x, h=1e-7):
    """Jacobiana por diferencias centrales (uso interno)."""
    n = len(x)
    J = [[0.0] * n for _ in range(n)]
    for j in range(n):
        xp, xm = list(x), list(x)
        xp[j] += h
        xm[j] -= h
        Fp, Fm = F(xp), F(xm)
        for i in range(n):
            J[i][j] = (Fp[i] - Fm[i]) / (2 * h)
    return J


#Newton-Raphson y Punto fijo
def newton_raphson(F, x0, J=None, tol=1e-8, max_iter=50):
    """
    Resuelve F(x) = 0.
    Retorna (solucion, iteraciones, error, historial)
    historial = lista de tuplas (k, x, error); k=0 es la aproximación inicial.
    """
    x = [float(v) for v in x0]
    historial = [(0, list(x), None)]

    for k in range(1, max_iter + 1):
        Fx = F(x)
        Jx = J(x) if J else jacobiana_numerica(F, x)

        try:
            delta = resolver_sistema(Jx, [-f for f in Fx])
        except ValueError:
            raise ErrorConvergencia(
                "La Jacobiana es singular; prueba otra aproximación inicial.", historial)

        x = [xi + di for xi, di in zip(x, delta)]
        error = max(abs(d) for d in delta)
        historial.append((k, list(x), error))

        if error < tol:
            return x, k, error, historial

    raise ErrorConvergencia(f"No convergió en {max_iter} iteraciones.", historial)


def punto_fijo(G, x0, tol=1e-8, max_iter=100, gauss_seidel=False):
    """
    Resuelve x = G(x).
    Retorna (solucion, iteraciones, error, historial)
    """
    x = [float(v) for v in x0]
    n = len(x)
    historial = [(0, list(x), None)]

    for k in range(1, max_iter + 1):
        try:
            if gauss_seidel:
                x_nuevo = list(x)
                for i in range(n):
                    x_nuevo[i] = G(x_nuevo)[i]
            else:
                x_nuevo = G(x)
        except (OverflowError, ZeroDivisionError, ValueError):
            raise ErrorConvergencia(
                "El método diverge (desbordamiento u operación inválida). "
                "Prueba otro despeje de G(x) u otra aproximación inicial.", historial)

        if any(math.isnan(v) or math.isinf(v) for v in x_nuevo):
            raise ErrorConvergencia("El método diverge. Prueba otro despeje de G(x).", historial)

        error = max(abs(a - b) for a, b in zip(x_nuevo, x))
        x = x_nuevo
        historial.append((k, list(x), error))

        if error < tol:
            return x, k, error, historial

    raise ErrorConvergencia(
        f"No convergió en {max_iter} iteraciones. "
        "Revisa que el despeje G(x) cumpla la condición de convergencia.", historial)


# Graficas e historiales
def mostrar_historial(historial, decimales=8):
    """Imprime en consola la tabla de iteraciones y errores."""
    if not historial:
        print("Sin historial.")
        return

    n = len(historial[0][1])
    ancho = decimales + 6
    encabezado = (f"{'k':>4} | "
                  + " | ".join(f"{'x' + str(i + 1):>{ancho}}" for i in range(n))
                  + f" | {'error':>12}")
    print(encabezado)
    print("-" * len(encabezado))

    for k, x, err in historial:
        valores = " | ".join(f"{v:>{ancho}.{decimales}f}" for v in x)
        texto_err = f"{err:>12.3e}" if err is not None else f"{'---':>12}"
        print(f"{k:>4} | {valores} | {texto_err}")


def graficar_errores(historial, titulo="Historial de errores"):
    """Grafica el error vs. iteración (escala logarítmica). Requiere matplotlib."""
    import matplotlib.pyplot as plt

    datos = [(k, e) for k, _, e in historial if e is not None and e > 0]
    if not datos:
        print("No hay errores para graficar.")
        return

    ks, errores = zip(*datos)
    plt.semilogy(ks, errores, "o-")
    plt.xlabel("Iteración")
    plt.ylabel("Error (máx |Δx|)")
    plt.title(titulo)
    plt.grid(True, which="both", alpha=0.3)
    plt.show()


# ───────────────────────────────────────────────────────────
# 5. Comparación de despejes (punto fijo)
# ───────────────────────────────────────────────────────────
def comparar_despejes(despejes, x0, tol=1e-8, max_iter=100, gauss_seidel=False,
                      tablas=True, graficas=True):
    """
    despejes -- dict {nombre: [g1, ..., gn]} (solo la parte derecha de x_i = g_i(x))
    Retorna una lista con un diccionario por despeje (diagnóstico, iteraciones,
    solución, norma de la Jacobiana, razón de error e historial).
    """
    n = len(x0)
    resultados = []

    for nombre, expresiones in despejes.items():
        if len(expresiones) != n:
            raise ValueError(f"El despeje '{nombre}' tiene {len(expresiones)} ecuaciones, se esperaban {n}.")

        res = {"nombre": nombre, "diagnostico": "", "converge": False, "iteraciones": None,
               "solucion": None, "error_final": None, "norma_J": None, "razon": None,
               "historial": [], "motivo": ""}
        try:
            G = crear_funcion(expresiones, n)
        except SyntaxError as e:
            res.update(diagnostico="Error de sintaxis", motivo=str(e))
            resultados.append(res)
            continue

        punto = list(map(float, x0))
        try:
            sol, it, err, hist = punto_fijo(G, x0, tol=tol, max_iter=max_iter,
                                            gauss_seidel=gauss_seidel)
            res.update(converge=True, iteraciones=it, solucion=sol, error_final=err,
                       historial=hist, diagnostico="Converge")
            punto = sol
        except ErrorConvergencia as e:
            res.update(historial=e.historial, motivo=str(e))
            if e.historial:
                punto = e.historial[-1][1]
                res["error_final"] = e.historial[-1][2]
            res["diagnostico"] = "Diverge" if "diverge" in str(e).lower() else "Lento (no alcanzó tol)"
        except Exception as e:
            res.update(diagnostico="Error de evaluación", motivo=f"{type(e).__name__}: {e}")
            resultados.append(res)
            continue

        # Condición suficiente de convergencia: ||J_G||inf < 1
        try:
            J = jacobiana_numerica(G, punto)
            res["norma_J"] = max(sum(abs(v) for v in fila) for fila in J)
        except Exception:
            pass

        # Razón empírica entre errores consecutivos
        errores = [e for _, _, e in res["historial"] if e is not None and e > 0]
        if len(errores) >= 3:
            ult = errores[-5:]
            razones = [b / a for a, b in zip(ult[:-1], ult[1:])]
            res["razon"] = sum(razones) / len(razones)
        if not res["converge"] and res["razon"] is not None and res["razon"] >= 1:
            res["diagnostico"] = "Diverge"

        resultados.append(res)

    if tablas:
        for r in resultados:
            print(f"\n=== {r['nombre']}: {r['diagnostico']} ===")
            if r["historial"]:
                mostrar_historial(r["historial"])
            if r["motivo"]:
                print(r["motivo"])

    print()
    mostrar_comparacion(resultados)
    if graficas:
        graficar_comparacion(resultados)
    return resultados


def mostrar_comparacion(resultados):
    """Tabla resumen de los despejes (uso interno)."""
    fmt = lambda v, f: format(v, f) if v is not None else "-"
    enc = f"{'Despeje':<16}{'Diagnóstico':<24}{'Iter':>6}{'Error final':>14}{'||J||inf':>11}{'Razón':>9}"
    print(enc)
    print("-" * len(enc))
    for r in resultados:
        it = str(r["iteraciones"]) if r["iteraciones"] is not None else "-"
        print(f"{r['nombre']:<16}{r['diagnostico']:<24}{it:>6}{fmt(r['error_final'], '.3e'):>14}"
              f"{fmt(r['norma_J'], '.3f'):>11}{fmt(r['razon'], '.3f'):>9}")

    conv = [r for r in resultados if r["converge"]]
    if conv:
        mejor = min(conv, key=lambda r: r["iteraciones"])
        print(f"\nDespeje más rápido: {mejor['nombre']} ({mejor['iteraciones']} iteraciones).")
    else:
        print("\nNingún despeje convergió con esta aproximación inicial.")


def graficar_comparacion(resultados, titulo="Comparación de despejes"):
    """Gráfica de errores de todos los despejes en una sola figura (uso interno)."""
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    hay = False
    for r in resultados:
        datos = [(k, e) for k, _, e in r["historial"] if e is not None and e > 0]
        if datos:
            ks, errs = zip(*datos)
            ax.semilogy(ks, errs, "o-", label=f"{r['nombre']} ({r['diagnostico']})")
            hay = True
    if not hay:
        print("No hay errores para graficar.")
        plt.close(fig)
        return
    ax.set_xlabel("Iteración")
    ax.set_ylabel("Error (máx |Δx|)")
    ax.set_title(titulo)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    plt.show()

