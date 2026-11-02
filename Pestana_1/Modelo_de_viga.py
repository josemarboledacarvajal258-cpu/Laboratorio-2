"""Modelos de equilibrio estático para ingeniería civil.

Cada modelo arma el sistema lineal A·x = b de las ecuaciones de equilibrio
(ΣFx = 0, ΣFy = 0, ΣM = 0) cuyas incógnitas son las reacciones en los apoyos.

Convención: x positivo hacia la derecha, y positivo hacia arriba,
momentos positivos en sentido antihorario. Unidades: kN y m.
"""

import math


# ───────────────────────────────────────────────────────────
# Modelos (cada uno devuelve un diccionario con el sistema y la geometría)
# ───────────────────────────────────────────────────────────
def viga_simple(L, a, P):
    """2x2: viga simplemente apoyada con una carga puntual vertical P a la distancia a de A."""
    return {
        "n": 2, "tipo": "viga",
        "titulo": "Viga simplemente apoyada con carga puntual vertical",
        "L": L, "a": a, "P": P,
        "puntos": [(0.0, 0.0), (L, 0.0)],
        "apoyos": [((0.0, 0.0), "fijo"), ((L, 0.0), "movil")],
        "articulaciones": [],
        "carga": {"punto": (a, 0.0), "fx": 0.0, "fy": -P, "etiqueta": f"P = {P:g} kN"},
        "A": [[1.0, 1.0],
              [0.0, L]],
        "b": [P, P * a],
        "incognitas": [("R_A", "Reacción vertical en A", "V", (0.0, 0.0)),
                       ("R_B", "Reacción vertical en B", "V", (L, 0.0))],
        "ecuaciones": ["ΣFy = 0", "ΣM_A = 0"],
        "analitica": [P - P * a / L, P * a / L],
        "Py": P, "idx_Ay": 0,
    }


def viga_inclinada(L, a, F, theta_deg):
    """3x3: viga con apoyo fijo en A y móvil en B bajo una carga F inclinada theta (bajo la horizontal)."""
    th = math.radians(theta_deg)
    Fx, Fy = F * math.cos(th), F * math.sin(th)
    By = Fy * a / L
    return {
        "n": 3, "tipo": "viga",
        "titulo": "Viga con apoyo fijo y móvil bajo carga inclinada",
        "L": L, "a": a, "F": F, "theta": theta_deg, "Fx": Fx, "Fy": Fy,
        "puntos": [(0.0, 0.0), (L, 0.0)],
        "apoyos": [((0.0, 0.0), "fijo"), ((L, 0.0), "movil")],
        "articulaciones": [],
        "carga": {"punto": (a, 0.0), "fx": Fx, "fy": -Fy,
                  "etiqueta": f"F = {F:g} kN, θ = {theta_deg:g}°"},
        "A": [[1.0, 0.0, 0.0],
              [0.0, 1.0, 1.0],
              [0.0, 0.0, L]],
        "b": [-Fx, Fy, Fy * a],
        "incognitas": [("A_x", "Reacción horizontal en A", "H", (0.0, 0.0)),
                       ("A_y", "Reacción vertical en A", "V", (0.0, 0.0)),
                       ("B_y", "Reacción vertical en B", "V", (L, 0.0))],
        "ecuaciones": ["ΣFx = 0", "ΣFy = 0", "ΣM_A = 0"],
        "analitica": [-Fx, Fy - By, By],
        "Py": Fy, "idx_Ay": 1,
    }


def arco_triarticulado(L, h, a, P):
    """4x4: arco triarticulado (articulaciones en A, B y la clave C) con carga vertical P a la distancia a de A."""
    xc = L / 2.0
    m = max(xc - a, 0.0)                       # brazo de la carga respecto a C (si está a la izquierda)
    By = P * a / L
    Ay = P - By
    Ax = (Ay * xc - P * m) / h
    y_carga = h * (a / xc) if a <= xc else h * ((L - a) / xc)
    return {
        "n": 4, "tipo": "arco",
        "titulo": "Arco triarticulado con carga vertical",
        "L": L, "h": h, "a": a, "P": P, "m": m,
        "puntos": [(0.0, 0.0), (xc, h), (L, 0.0)],
        "apoyos": [((0.0, 0.0), "fijo"), ((L, 0.0), "fijo")],
        "articulaciones": [(xc, h)],
        "carga": {"punto": (a, y_carga), "fx": 0.0, "fy": -P, "etiqueta": f"P = {P:g} kN"},
        "A": [[1.0, 0.0, 1.0, 0.0],
              [0.0, 1.0, 0.0, 1.0],
              [0.0, 0.0, 0.0, L],
              [-h, xc, 0.0, 0.0]],
        "b": [0.0, P, P * a, P * m],
        "incognitas": [("A_x", "Reacción horizontal en A", "H", (0.0, 0.0)),
                       ("A_y", "Reacción vertical en A", "V", (0.0, 0.0)),
                       ("B_x", "Reacción horizontal en B", "H", (L, 0.0)),
                       ("B_y", "Reacción vertical en B", "V", (L, 0.0))],
        "ecuaciones": ["ΣFx = 0", "ΣFy = 0", "ΣM_A = 0", "ΣM_C (izq.) = 0"],
        "analitica": [Ax, Ay, -Ax, By],
        "P_izq": P if a < xc else 0.0,
    }


# ───────────────────────────────────────────────────────────
# Análisis de resultados
# ───────────────────────────────────────────────────────────
def residuo(A, b, x):
    """Residuo r = b - A·x de cada ecuación."""
    return [bi - sum(aij * xj for aij, xj in zip(fila, x)) for fila, bi in zip(A, b)]


def sentido(eje, valor, tol=1e-9):
    """Texto con el sentido físico de una reacción según su signo."""
    if abs(valor) < tol:
        return "nula"
    if eje == "V":
        return "hacia arriba ↑" if valor > 0 else "hacia abajo ↓"
    return "hacia la derecha →" if valor > 0 else "hacia la izquierda ←"


def fuerzas_internas(modelo, sol):
    """Lista de (nombre, valor, unidad) con fuerzas internas características."""
    if modelo["tipo"] == "viga":
        Ay, Py, a = sol[modelo["idx_Ay"]], modelo["Py"], modelo["a"]
        datos = [("Cortante a la izquierda de la carga", Ay, "kN"),
                 ("Cortante a la derecha de la carga", Ay - Py, "kN"),
                 ("Momento flector máximo (bajo la carga)", Ay * a, "kN·m")]
        if modelo["n"] == 3:
            datos.append(("Fuerza axial entre A y la carga (+ tracción)", -sol[0], "kN"))
        return datos

    Ax, Ay = sol[0], sol[1]
    h, xc = modelo["h"], modelo["L"] / 2.0
    Mc = -h * Ax + xc * Ay - modelo["P"] * modelo["m"]      # momento en C (debe ser ~0)
    return [("Empuje horizontal en la clave C (H)", abs(Ax), "kN"),
            ("Fuerza vertical en C (cortante)", modelo["P_izq"] - Ay, "kN"),
            ("Momento flector en C (articulación)", Mc, "kN·m")]


def interpretar(modelo, sol):
    """Frases de interpretación física de los resultados."""
    n = modelo["n"]

    if n == 2:
        P, a = modelo["P"], modelo["a"]
        RA, RB = sol
        return [
            f"El apoyo A resiste el {RA / P * 100:.1f} % de la carga y el apoyo B el {RB / P * 100:.1f} %. "
            "Cuanto más cerca está la carga de un apoyo, mayor es la reacción en ese apoyo.",
            f"El momento flector máximo es {RA * a:.2f} kN·m y ocurre bajo la carga (x = {a:g} m): "
            "es la referencia para dimensionar la viga a flexión.",
        ]

    if n == 3:
        Ax, Ay, By = sol
        N = -Ax
        frases = [
            f"A_x = {Ax:.2f} kN ({sentido('H', Ax)}) equilibra la componente horizontal de la carga, "
            f"F·cos θ = {modelo['Fx']:.2f} kN. Solo el apoyo fijo A puede resistirla, porque el apoyo móvil B "
            "no restringe el movimiento horizontal.",
            f"Las reacciones verticales suman {Ay + By:.2f} kN, igual a la componente vertical de la carga, "
            f"F·sen θ = {modelo['Fy']:.2f} kN: A toma {Ay:.2f} kN y B toma {By:.2f} kN.",
        ]
        if abs(N) > 1e-9:
            frases.append(
                f"Entre A y el punto de aplicación de la carga la viga soporta una fuerza axial de {abs(N):.2f} kN "
                f"a {'tracción' if N > 0 else 'compresión'}; a la derecha de la carga la fuerza axial es nula.")
        return frases

    Ax, Ay, Bx, By = sol
    return [
        f"El empuje horizontal en los apoyos es H = {abs(Ax):.2f} kN (A_x {sentido('H', Ax)}, "
        f"B_x {sentido('H', Bx)}). Un arco transmite parte de la carga como empuje horizontal, "
        "algo que una viga simplemente apoyada no hace.",
        f"Como A_x·h es constante, si disminuyes la altura h de la clave el empuje H aumenta en proporción inversa "
        f"(con h = {modelo['h']:g} m, H = {abs(Ax):.2f} kN).",
        "En la articulación C el momento flector es nulo: esa condición adicional completa las 4 ecuaciones "
        "necesarias para las 4 incógnitas (arco isostático).",
    ]