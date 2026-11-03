"""ModLab3: interpolación (Lagrange, Newton, spline natural), datos USGS y utilidades de las pestañas 3 y 4."""
import io
import os
from functools import lru_cache

import numpy as np
import pandas as pd
import streamlit as st

U = "ft³/s"
COL = {"Lagrange": "#1f77b4", "Newton": "#ff7f0e",
       "Spline natural (propio)": "#2ca02c", "Spline natural (SciPy)": "#d62728"}
RUTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "usgs_caudal_diario.rdb")


# ═════════════════════════ 1. Lagrange ═════════════════════════
def bases_lagrange(xs, j, t):
    """L_j(t) = prod_{k≠j} (t - x_k)/(x_j - x_k). Acepta escalar o arreglo."""
    xs = np.asarray(xs, float)
    t = np.asarray(t, float)
    L = np.ones_like(t, dtype=float)
    for k, xk in enumerate(xs):
        if k != j:
            L = L * (t - xk) / (xs[j] - xk)
    return float(L) if L.ndim == 0 else L


def lagrange_eval(xs, ys, t):
    """P(t) = sum y_j L_j(t) evaluado en un arreglo de puntos."""
    xs, ys = np.asarray(xs, float), np.asarray(ys, float)
    t = np.atleast_1d(np.asarray(t, float))
    return sum(ys[j] * bases_lagrange(xs, j, t) for j in range(len(xs)))


def ventana_nodos(tn, t, k):
    """Índices de k nodos consecutivos que rodean al punto t."""
    tn = np.asarray(tn, float)
    i = int(np.searchsorted(tn, t, side="right") - 1)
    ini = int(np.clip(i - (k - 1) // 2, 0, len(tn) - k))
    return np.arange(ini, ini + k)


# ═════════════════════════ 2. Newton ═════════════════════════
def diferencias_divididas(xs, ys):
    """Tabla T (m×m): T[i, j] = f[x_i, ..., x_{i+j}]; NaN donde no aplica."""
    xs, ys = np.asarray(xs, float), np.asarray(ys, float)
    m = len(xs)
    T = np.full((m, m), np.nan)
    T[:, 0] = ys
    for j in range(1, m):
        for i in range(m - j):
            T[i, j] = (T[i + 1, j - 1] - T[i, j - 1]) / (xs[i + j] - xs[i])
    return T


def coef_newton(xs, ys):
    return diferencias_divididas(xs, ys)[0]


def evaluar_newton(xs, coef, t):
    """Polinomio de Newton con esquema de Horner."""
    xs = np.asarray(xs, float)
    t = np.atleast_1d(np.asarray(t, float))
    p = np.full_like(t, coef[-1], dtype=float)
    for j in range(len(coef) - 2, -1, -1):
        p = coef[j] + (t - xs[j]) * p
    return p


def agregar_nodo(xs, ys, x_nuevo, y_nuevo):
    """Retorna (xs2, ys2, coef2, ok); ok=True si los coeficientes previos no cambian."""
    c_old = coef_newton(xs, ys)
    x2, y2 = np.append(xs, x_nuevo), np.append(ys, y_nuevo)
    c2 = coef_newton(x2, y2)
    return x2, y2, c2, bool(np.allclose(c2[:-1], c_old, rtol=1e-9, atol=1e-9))


# ═════════════════════════ 3. Spline cúbico natural ═════════════════════════
def spline_natural_momentos(xs, ys):
    """Momentos M_i = S''(x_i) con M_0 = M_n = 0."""
    xs, ys = np.asarray(xs, float), np.asarray(ys, float)
    n = len(xs)
    M = np.zeros(n)
    if n <= 2:
        return M
    h = np.diff(xs)
    delta = np.diff(ys) / h
    A = np.zeros((n - 2, n - 2))
    rhs = np.zeros(n - 2)
    for r in range(n - 2):
        A[r, r] = 2 * (h[r] + h[r + 1])
        if r > 0:
            A[r, r - 1] = h[r]
        if r < n - 3:
            A[r, r + 1] = h[r + 1]
        rhs[r] = 6 * (delta[r + 1] - delta[r])
    M[1:-1] = np.linalg.solve(A, rhs)
    return M


def tramo_spline(xs, ys, i, M):
    """Coeficientes (a, b, c, d) de S_i(t) = a + b(t-x_i) + c(t-x_i)^2 + d(t-x_i)^3."""
    h = xs[i + 1] - xs[i]
    b = (ys[i + 1] - ys[i]) / h - h * (2 * M[i] + M[i + 1]) / 6
    return float(ys[i]), float(b), float(M[i] / 2), float((M[i + 1] - M[i]) / (6 * h))


def spline_eval(xs, ys, M, t):
    xs, ys = np.asarray(xs, float), np.asarray(ys, float)
    t = np.atleast_1d(np.asarray(t, float))
    i = np.clip(np.searchsorted(xs, t, side="right") - 1, 0, len(xs) - 2)
    h = xs[i + 1] - xs[i]
    dx = t - xs[i]
    b = (ys[i + 1] - ys[i]) / h - h * (2 * M[i] + M[i + 1]) / 6
    return ys[i] + b * dx + (M[i] / 2) * dx**2 + ((M[i + 1] - M[i]) / (6 * h)) * dx**3


# ═════════════════════════ 4. Métricas (e = ŷ − y) ═════════════════════════
def errores(pred, y):
    return np.asarray(pred, float) - np.asarray(y, float)


def mae(e):
    return float(np.mean(np.abs(e)))


def rmse(e):
    return float(np.sqrt(np.mean(np.square(e))))


def emax(e):
    return float(np.max(np.abs(e)))


# ═════════════════════════ 5. Datos USGS ═════════════════════════
@lru_cache(maxsize=1)
def _leer_rdb():
    with open(RUTA, encoding="utf-8") as f:
        lineas = [l for l in f if not l.startswith("#")]
    bruto = pd.read_csv(io.StringIO("".join(lineas)), sep="\t", skiprows=[1], dtype=str)
    col = [c for c in bruto.columns if "00060" in c and not c.endswith("_cd")][0]
    df = pd.DataFrame({"fecha": pd.to_datetime(bruto["datetime"]),
                       "valor": pd.to_numeric(bruto[col], errors="coerce")}).dropna().reset_index(drop=True)
    df.attrs["site_no"] = str(bruto["site_no"].iloc[0]) if "site_no" in bruto else "desconocida"
    return df


def _sintetica(n=365):
    rng = np.random.default_rng(0)
    t = np.arange(n)
    q = 300 + 120 * np.sin(2 * np.pi * t / 120) + rng.normal(0, 12, n)
    for t0 in rng.choice(n - 20, 6, replace=False):
        q[t0:t0 + 20] += rng.uniform(150, 400) * np.exp(-np.arange(20) / 5)
    df = pd.DataFrame({"fecha": pd.date_range("2020-01-01", periods=n), "valor": np.clip(q, 20, None)})
    df.attrs["site_no"] = "sintética"
    return df


def cargar(n_recorte=36, inicio=0):
    """Retorna (df, real). real=False si los datos son sintéticos."""
    real = os.path.exists(RUTA)
    serie = _leer_rdb() if real else _sintetica()
    df = serie.iloc[inicio:inicio + n_recorte].reset_index(drop=True)
    df.attrs["site_no"] = serie.attrs.get("site_no")
    return df, real


def control_calidad(df):
    saltos = df["fecha"].diff().dropna() != pd.Timedelta(days=1)
    return {"n": len(df), "faltantes": int(df["valor"].isna().sum()),
            "duplicadas": int(df["fecha"].duplicated().sum()), "saltos": int(saltos.sum())}


def fraccion_regular(valores):
    """Fracción de pasos con la misma variación no nula que el anterior (detecta series generadas)."""
    d = np.diff(np.asarray(valores, float))
    if len(d) < 2:
        return 0.0
    return float(np.mean(np.isclose(d[1:], d[:-1]) & (d[1:] != 0)))


def particion_comun(N, paso, hueco):
    """Retorna (nodos, reservadas) como índices. Los extremos siempre son nodos."""
    val = {i for i in range(1, N - 1) if i % paso == paso // 2}
    if hueco > 0:
        c = N // 2 - hueco // 2
        val |= {i for i in range(c, c + hueco) if 1 <= i <= N - 2}
    val = np.array(sorted(val), dtype=int)
    nodos = np.array([i for i in range(N) if i not in set(val)], dtype=int)
    return nodos, val


def comparar(df, nodos, val, unidad=""):
    """Construye los cuatro interpolantes con los nodos y los evalúa en las reservadas."""
    from scipy.interpolate import CubicSpline

    t = np.arange(len(df), dtype=float)
    y = df["valor"].to_numpy(float)
    tn, yn, tv, yv = t[nodos], y[nodos], t[val], y[val]
    t_curva = np.linspace(tn[0], tn[-1], 600)

    cf = coef_newton(tn, yn)
    M = spline_natural_momentos(tn, yn)
    cs = CubicSpline(tn, yn, bc_type="natural")
    f = {"Lagrange": lambda u: lagrange_eval(tn, yn, u),
         "Newton": lambda u: evaluar_newton(tn, cf, u),
         "Spline natural (propio)": lambda u: spline_eval(tn, yn, M, u),
         "Spline natural (SciPy)": lambda u: cs(u)}

    pred = {k: np.asarray(g(tv), float) for k, g in f.items()}
    met = pd.DataFrame({k: {"MAE": mae(errores(p, yv)), "RMSE": rmse(errores(p, yv)),
                            "E_max": emax(errores(p, yv))} for k, p in pred.items()}).T
    repro = {k: float(np.max(np.abs(np.asarray(g(tn)) - yn))) for k, g in f.items()}
    curvas = {k: np.asarray(f[k](t_curva), float)
              for k in ("Lagrange", "Newton", "Spline natural (propio)")}
    acuerdo = {"Newton vs Lagrange": float(np.max(np.abs(curvas["Newton"] - curvas["Lagrange"]))),
               "Spline propio vs SciPy": float(np.max(np.abs(curvas["Spline natural (propio)"] - cs(t_curva))))}
    return dict(t=t, y=y, nodos=nodos, val=val, t_val=tv, y_val=yv, t_curva=t_curva,
                curvas=curvas, pred=pred, metricas=met, reproduccion_nodos=repro,
                acuerdo=acuerdo, unidad=unidad)


# ═════════════════════════ 6. Interfaz compartida (pestañas 3 y 4) ═════════════════════════
def bloque_datos_compartidos():
    """Barra lateral que alimenta las pestañas 3 y 4 (mismos nodos y reservadas)."""
    sb = st.sidebar
    sb.header("Datos compartidos (pestañas 3 y 4)")
    n = sb.slider("Días del recorte (n)", 20, 120, 36, key="sb_n")
    completa = cargar(n_recorte=10**6)[0]
    ini = sb.slider("Día de inicio en la serie", 0, max(1, len(completa) - n), 0, key="sb_ini")
    paso = sb.slider("Reservar 1 de cada p días", 3, 8, 4, key="sb_paso")
    hueco = sb.slider("Hueco interior (días consecutivos)", 0, 5, 2, key="sb_hueco")

    df, real = cargar(n_recorte=n, inicio=ini)
    if not real:
        sb.warning("Datos SINTÉTICOS: falta data/usgs_caudal_diario.rdb")
    elif fraccion_regular(completa["valor"]) > 0.3:
        sb.error("Serie sospechosamente regular (posible dato generado): verifique la descarga en USGS.")

    nodos, val = particion_comun(len(df), paso, hueco)
    R = comparar(df, nodos, val, U)
    sb.caption(f"Nodos: {len(nodos)} · reservadas: {len(val)} · extrapolación: desactivada")
    return dict(df=df, real=real, nodos=nodos, val=val, R=R)


def graficar_serie(ax, R, nodos=True):
    ax.plot(R["t"], R["y"], color="#bbbbbb", lw=0.8, zorder=1)
    if nodos:
        ax.plot(R["t"][R["nodos"]], R["y"][R["nodos"]], "o", color="k", ms=4, label="nodos", zorder=3)
    ax.plot(R["t_val"], R["y_val"], "s", color="#e41a1c", ms=5, label="reservadas", zorder=3)
    ax.set_xlabel("Día desde el inicio")
    ax.set_ylabel(f"Q [{U}]")
    ax.grid(alpha=0.3)


def ficha(ctx):
    """Procedencia y control de calidad de los datos."""
    df = ctx["df"]
    if not ctx["real"]:
        st.error("Datos SINTÉTICOS ilustrativos: coloque el archivo USGS en `data/usgs_caudal_diario.rdb`.")
        return
    q = control_calidad(df)
    st.markdown(f"**Fuente:** USGS Water Data (NWIS), estación {df.attrs.get('site_no')}, caudal medio "
                f"diario (parámetro 00060, estadístico 00003), {U}. Recorte de **{q['n']}** días: "
                f"{df['fecha'].iloc[0].date()} → {df['fecha'].iloc[-1].date()}.")
    if q["faltantes"] or q["saltos"] or q["duplicadas"]:
        st.warning(f"Control de calidad: {q['faltantes']} faltantes, {q['saltos']} saltos de fecha, "
                   f"{q['duplicadas']} fechas duplicadas.")