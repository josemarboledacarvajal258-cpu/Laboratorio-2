"""Interpolación: Newton (diferencias divididas), Lagrange y spline cúbico natural (propio y SciPy).
Fuera del rango de los nodos se devuelve NaN (la extrapolación está desactivada por defecto)."""
import numpy as np
from scipy.interpolate import CubicSpline

def _chk(x, y=None):
    x = np.asarray(x, float)
    if x.ndim != 1 or len(x) < 2 or len(np.unique(x)) != len(x):
        raise ValueError("Se requieren >=2 nodos x distintos (1D).")
    if y is not None and len(np.asarray(y)) != len(x):
        raise ValueError("x e y deben tener igual longitud.")
    return x

def _enmascarar(xq, x, v, extrapolar):
    xq = np.asarray(xq, float)
    if not extrapolar:
        v = np.where((xq < x.min()) | (xq > x.max()), np.nan, v)
    return v

# ---------------- Newton ----------------
def diferencias_divididas(x, y):
    """Tabla n×n: columna j = diferencias de orden j. Coeficientes de Newton = fila 0."""
    x = _chk(x, y); n = len(x)
    T = np.full((n, n), np.nan); T[:, 0] = np.asarray(y, float)
    for j in range(1, n):
        for i in range(n - j):
            T[i, j] = (T[i + 1, j - 1] - T[i, j - 1]) / (x[i + j] - x[i])
    return T

def coef_newton(x, y):
    return diferencias_divididas(x, y)[0, :]

def evaluar_newton(x, coef, xq, extrapolar=False):
    """Horner anidado: P(t)=c0+(t-x0)(c1+(t-x1)(c2+...))."""
    x = _chk(x); xq = np.asarray(xq, float); p = np.full_like(xq, coef[-1], dtype=float)
    for k in range(len(coef) - 2, -1, -1):
        p = coef[k] + (xq - x[k]) * p
    return _enmascarar(xq, x, p, extrapolar)

def agregar_nodo(x, y, x_nuevo, y_nuevo):
    """Añade un nodo al final: los coeficientes previos se conservan; solo se agrega uno nuevo."""
    x2, y2 = np.append(x, x_nuevo), np.append(y, y_nuevo)
    c_ant, c_nuevo = coef_newton(x, y), coef_newton(x2, y2)
    return x2, y2, c_nuevo, bool(np.allclose(c_ant, c_nuevo[:-1]))

# ---------------- Lagrange ----------------
def lagrange_eval(x, y, xq, extrapolar=False):
    """Forma baricéntrica: P(t)=Σ w_j y_j/(t-x_j) / Σ w_j/(t-x_j), w_j=1/Π_{k≠j}(x_j-x_k)."""
    x = _chk(x, y); y = np.asarray(y, float); xq = np.atleast_1d(np.asarray(xq, float))
    w = np.array([1.0 / np.prod(x[j] - np.delete(x, j)) for j in range(len(x))])
    out = np.empty_like(xq)
    for i, t in enumerate(xq):
        d = t - x
        if np.any(d == 0): out[i] = y[np.argmin(np.abs(d))]
        else: out[i] = np.sum(w * y / d) / np.sum(w / d)
    return _enmascarar(xq, x, out, extrapolar)

def bases_lagrange(x, j, xq):
    """L_j(xq) explícita (para desarrollos y comprobación de L_j(x_i)=δ_ij)."""
    x = _chk(x); xq = np.asarray(xq, float)
    return np.prod([(xq - x[k]) / (x[j] - x[k]) for k in range(len(x)) if k != j], axis=0)

# ---------------- Spline cúbico natural ----------------
def spline_natural_momentos(x, y):
    """Momentos M_i=S''(x_i) con M_0=M_{n-1}=0:
    h_{i-1}M_{i-1}+2(h_{i-1}+h_i)M_i+h_i M_{i+1}=6(δ_i-δ_{i-1})."""
    x = _chk(x, y); y = np.asarray(y, float); n = len(x)
    if np.any(np.diff(x) <= 0): raise ValueError("x debe ser estrictamente creciente.")
    h, dlt = np.diff(x), np.diff(y) / np.diff(x); M = np.zeros(n)
    if n > 2:
        A = np.zeros((n - 2, n - 2)); b = 6 * (dlt[1:] - dlt[:-1])
        for i in range(n - 2):
            A[i, i] = 2 * (h[i] + h[i + 1])
            if i > 0: A[i, i - 1] = h[i]
            if i < n - 3: A[i, i + 1] = h[i + 1]
        M[1:-1] = np.linalg.solve(A, b)
    return M

def spline_natural_eval(x, y, xq, extrapolar=False, M=None):
    x = _chk(x, y); y = np.asarray(y, float); xq = np.atleast_1d(np.asarray(xq, float))
    M = spline_natural_momentos(x, y) if M is None else M
    i = np.clip(np.searchsorted(x, xq, side="right") - 1, 0, len(x) - 2)
    h = x[i + 1] - x[i]; a, b = x[i + 1] - xq, xq - x[i]
    S = M[i] * a**3 / (6 * h) + M[i + 1] * b**3 / (6 * h) + (y[i] / h - M[i] * h / 6) * a + (y[i + 1] / h - M[i + 1] * h / 6) * b
    return _enmascarar(xq, x, S, extrapolar)

def spline_natural_scipy(x, y, xq, extrapolar=False):
    """Contraste con SciPy: CubicSpline(bc_type='natural') (S''=0 en los extremos)."""
    x = _chk(x, y)
    return np.asarray(CubicSpline(x, y, bc_type="natural", extrapolate=extrapolar)(xq), float)

# ---------------- Utilidades para la app y los cuadernos ----------------
def ventana_nodos(x, t, k):
    """Índices de k nodos consecutivos alrededor de t (interpolación local con k nodos)."""
    x = np.asarray(x, float); j = int(np.searchsorted(x, t))
    ini = int(np.clip(j - k // 2, 0, len(x) - k)); return np.arange(ini, ini + k)

def tramo_spline(x, y, i, M=None):
    """Coeficientes (a,b,c,d) de S_i(x)=a+b(x-x_i)+c(x-x_i)^2+d(x-x_i)^3 en [x_i,x_{i+1}]."""
    x = _chk(x, y); y = np.asarray(y, float); M = spline_natural_momentos(x, y) if M is None else M
    h = x[i + 1] - x[i]; dl = (y[i + 1] - y[i]) / h
    return y[i], dl - h * (2 * M[i] + M[i + 1]) / 6, M[i] / 2, (M[i + 1] - M[i]) / (6 * h)
