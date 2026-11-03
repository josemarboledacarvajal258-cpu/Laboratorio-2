"""Datos y comparación común Lagrange / Newton / spline (cuaderno 5 y pestaña 4 usan este mismo código)."""
import numpy as np, pandas as pd, os
from interpolacion import (coef_newton, evaluar_newton, lagrange_eval,
                           spline_natural_eval, spline_natural_scipy)
import metricas

CFS_A_M3S = 0.028316846592

def cargar_usgs_rdb(ruta, parametro="00060"):
    """Lee un archivo RDB de USGS Water Data (descarga 'Tab-separated'). Omite '#' y la fila de formatos.
    Devuelve DataFrame(fecha, valor) con la primera columna cuyo nombre contenga `parametro`
    (00060 = caudal, ft³/s). Elimina duplicados y filas sin dato numérico."""
    df = pd.read_csv(ruta, sep="\t", comment="#", dtype=str).iloc[1:]
    cf = [c for c in df.columns if c in ("datetime", "dateTime")]
    cv = [c for c in df.columns if parametro in c and not c.endswith("_cd")]
    if not cf or not cv:
        raise ValueError(f"El archivo no contiene fecha y parámetro {parametro}: columnas {list(df.columns)}")
    out = pd.DataFrame({"fecha": pd.to_datetime(df[cf[0]]), "valor": pd.to_numeric(df[cv[0]], errors="coerce")})
    # valores no numéricos (Ice, Eqp, Ssn, …) y vacíos se EXCLUYEN (no se rellenan); se cuentan en attrs
    out.attrs["excluidos_no_numericos"] = int(out["valor"].isna().sum())
    out.attrs["site_no"] = str(df["site_no"].iloc[0]) if "site_no" in df.columns and len(df) else None
    out = out.dropna().drop_duplicates("fecha").sort_values("fecha").reset_index(drop=True)
    out.attrs.update({"site_no": df["site_no"].iloc[0] if "site_no" in df.columns and len(df) else None})
    return out

def datos_sinteticos(n=36, semilla=7):
    """SINTÉTICO (solo ilustrativo / pruebas): hidrograma con dos crecidas. NO sustituye la base real."""
    rng = np.random.default_rng(semilla); t = np.arange(n, dtype=float)
    q = 40 + 120 * np.exp(-((t - 10) / 3.0) ** 2) + 70 * np.exp(-((t - 25) / 4.0) ** 2) + rng.normal(0, 2, n)
    return pd.DataFrame({"fecha": pd.Timestamp("2026-01-01") + pd.to_timedelta(t, "D"), "valor": q})

def cargar(ruta_real="data/usgs_caudal_diario.rdb", n_recorte=36, inicio=0, guardar=True):
    """Devuelve (df, es_real): recorte de n_recorte días desde `inicio`. Si existe el archivo, escribe
    la copia procesada data/usgs_procesado.csv (serie completa limpia); si no, usa sintético marcado."""
    if os.path.exists(ruta_real):
        full = cargar_usgs_rdb(ruta_real)
        if guardar:
            try: full.to_csv(os.path.join(os.path.dirname(ruta_real) or ".", "usgs_procesado.csv"), index=False)
            except OSError: pass
        out = full.iloc[inicio:inicio + n_recorte].reset_index(drop=True); out.attrs.update(full.attrs)
        return out, True
    return datos_sinteticos(n_recorte), False

def control_calidad(df):
    """Indicadores simples de calidad de la serie (para documentar y detectar anomalías)."""
    y = df["valor"].to_numpy(float)
    return {"n": len(y), "mínimo": y.min(), "mediana": float(np.median(y)), "máximo": y.max(),
            "huecos de fecha": int((df["fecha"].diff().dt.days.dropna() != 1).sum()),
            "duplicados": int(df["fecha"].duplicated().sum()), "valores ≤ 0": int((y <= 0).sum()),
            "std(Δy)/std(y) (suavidad)": float(np.std(np.diff(y)) / np.std(y)),
            "2ª diferencias casi constantes (fracción)": fraccion_regular(y)}

def fraccion_regular(y):
    """Fracción de segundas diferencias |Δ²y| < 0.1 % de la mediana. Una serie hidrológica real, con ruido,
    da valores cercanos a 0; valores > 0.3 indican una serie sospechosamente regular (posiblemente generada)."""
    y = np.asarray(y, float); return float(np.mean(np.abs(np.diff(y, 2)) < 1e-3 * np.median(y))) if len(y) > 3 else float("nan")

def codigos_calificacion(ruta):
    """Conteo de códigos de calificación del RDB (A=aprobado, P=provisional, Eqp=equipo, etc.)."""
    raw = pd.read_csv(ruta, sep="\t", comment="#", dtype=str).iloc[1:]
    return raw[[c for c in raw.columns if c.endswith("_cd") and c != "agency_cd"][0]].value_counts()

def particion_comun(n, paso=4, hueco=0):
    """Índices de construcción (nodos) y validación (reservados). Los extremos siempre son nodos.
    Reserva cada `paso`-ésima observación interior (omisiones aisladas) y, si hueco>0, `hueco`
    puntos consecutivos en el centro (hueco interior corto). Nada se rellena previamente."""
    val = set(range(paso, n - 1, paso))
    if hueco > 0:
        c = n // 2; val |= set(range(c, min(c + hueco, n - 1)))
    val -= {0, n - 1}
    val = np.array(sorted(val)); nodos = np.array([i for i in range(n) if i not in set(val)])
    return nodos, val

def comparar(df, nodos, val, unidad="ft³/s"):
    """Mismos nodos y mismas reservas para todos. Tiempo normalizado a [0,1] (condicionamiento)."""
    t = (df["fecha"] - df["fecha"].iloc[0]).dt.total_seconds().to_numpy() / 86400.0
    y = df["valor"].to_numpy(float); u = t / t[-1]
    xn, yn, xv, yv = u[nodos], y[nodos], u[val], y[val]
    c = coef_newton(xn, yn)
    pred = {"Lagrange": lagrange_eval(xn, yn, xv), "Newton": evaluar_newton(xn, c, xv),
            "Spline natural (propio)": spline_natural_eval(xn, yn, xv),
            "Spline natural (SciPy)": spline_natural_scipy(xn, yn, xv)}
    filas = [{"Método": k, **{kk: vv for kk, vv in metricas.resumen(v, yv, unidad).items() if kk != "unidad"}} for k, v in pred.items()]
    rep = {"Lagrange": np.max(np.abs(lagrange_eval(xn, yn, xn) - yn)), "Newton": np.max(np.abs(evaluar_newton(xn, c, xn) - yn)),
           "Spline natural (propio)": np.max(np.abs(spline_natural_eval(xn, yn, xn) - yn)),
           "Spline natural (SciPy)": np.max(np.abs(spline_natural_scipy(xn, yn, xn) - yn))}
    uu = np.linspace(0, 1, 400)
    curvas = {"Lagrange": lagrange_eval(xn, yn, uu), "Newton": evaluar_newton(xn, c, uu),
              "Spline natural (propio)": spline_natural_eval(xn, yn, uu)}
    return dict(t=t, y=y, nodos=nodos, val=val, pred=pred, y_val=yv, t_val=t[val], t_curva=uu * t[-1],
                curvas=curvas, metricas=pd.DataFrame(filas).set_index("Método"),
                reproduccion_nodos=rep,
                acuerdo={"|Lagrange−Newton|máx": float(np.max(np.abs(pred["Lagrange"] - pred["Newton"]))),
                         "|Spline propio−SciPy|máx": float(np.max(np.abs(pred["Spline natural (propio)"] - pred["Spline natural (SciPy)"])))})
