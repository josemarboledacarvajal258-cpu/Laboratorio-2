import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from ModLab2 import (resolver_sistema, crear_funcion, newton_raphson,
                     punto_fijo, ErrorConvergencia)


# ─────────────────────────────────────────────────────────────
# Construcción del modelo estructural
# ─────────────────────────────────────────────────────────────
def _deriva(i):
    """Texto de la deriva del entrepiso i (u_0 = 0, empotrado en la base)."""
    return "x1" if i == 1 else f"(x{i} - x{i - 1})"


def _fuerza_entrepiso(i, k, c):
    d = _deriva(i)
    return f"({k[i - 1]!r}*{d} + {c!r}*{d}**3)"


def _ecuaciones_equilibrio(n, k, c, P):
    """F_i(x) = 0 : equilibrio del piso i."""
    eqs = []
    for i in range(1, n + 1):
        f = _fuerza_entrepiso(i, k, c)
        if i < n:
            f += f" - {_fuerza_entrepiso(i + 1, k, c)}"
        eqs.append(f"{f} - ({P[i - 1]!r})")
    return eqs


def _despeje_directo(n, k, c, P):
    """x_i = g_i(x): se despeja u_i de la parte lineal y la parte cúbica queda como corrección."""
    gs = []
    for i in range(1, n + 1):
        num = f"({P[i - 1]!r})"
        if i > 1:
            num += f" + {k[i - 1]!r}*x{i - 1}"
        num += f" - {c!r}*{_deriva(i)}**3"
        if i < n:
            num += f" + {k[i]!r}*x{i + 1} + {c!r}*{_deriva(i + 1)}**3"
        den = k[i - 1] + (k[i] if i < n else 0.0)
        gs.append(f"({num})/{den!r}")
    return gs


def _despeje_relajacion(n, k, c, P, w):
    """x_i = x_i - w * F_i / K_ii  (relajación con la rigidez lineal como diagonal)."""
    eqs = _ecuaciones_equilibrio(n, k, c, P)
    gs = []
    for i in range(1, n + 1):
        den = k[i - 1] + (k[i] if i < n else 0.0)
        gs.append(f"x{i} - {w!r}*({eqs[i - 1]})/{den!r}")
    return gs


def _jacobiana_analitica(n, k, c):
    """Matriz de rigidez tangente K_t(u)."""
    def J(x):
        u = [0.0] + list(x)
        kt = [k[i] + 3 * c * (u[i + 1] - u[i]) ** 2 for i in range(n)]
        M = [[0.0] * n for _ in range(n)]
        for i in range(n):
            M[i][i] = kt[i] + (kt[i + 1] if i < n - 1 else 0.0)
            if i > 0:
                M[i][i - 1] = -kt[i]
            if i < n - 1:
                M[i][i + 1] = -kt[i + 1]
        return M
    return J


# ─────────────────────────────────────────────────────────────
# Pestaña
# ─────────────────────────────────────────────────────────────
def mostrar():

    # 1. Contexto ------------------------------------------------------------
    st.header("1. Contexto en ingeniería civil")
    st.markdown(
        "En el análisis estructural lineal se supone que los desplazamientos son pequeños "
        "y que la rigidez es constante: $K\\,u = P$. Cuando las **deformaciones son grandes** "
        "(edificios esbeltos, cables, arcos, estructuras bajo sismo severo) la geometría cambia "
        "durante la carga y la rigidez **depende de los propios desplazamientos**. El equilibrio "
        "deja de ser un sistema lineal y pasa a ser un **sistema no lineal** $F(u)=0$."
    )
    st.markdown(
        "Se modela un **edificio de cortante de $n$ pisos**. La fuerza cortante del entrepiso $i$, "
        "con deriva $d_i = u_i - u_{i-1}$ y $u_0 = 0$, incluye un término cúbico que representa "
        "la rigidización por grandes deformaciones:"
    )
    st.latex(r"V_i(d_i) = k_i\,d_i + c\,d_i^{3}")
    st.markdown("El equilibrio de cada piso ($\\sum F_x = 0$) da el sistema no lineal:")
    st.latex(r"F_i(u) = V_i(d_i) - V_{i+1}(d_{i+1}) - P_i = 0, \qquad i = 1,\dots,n \quad (V_{n+1}=0)")
    st.markdown(
        "Se resuelve con `newton_raphson` y `punto_fijo` de `ModLab2`, y se compara con la "
        "solución lineal obtenida con `resolver_sistema`."
    )
    st.markdown(
        "*Convención: $u$ positivo hacia la derecha, cargas laterales $P_i$ positivas hacia la "
        "derecha. Unidades: kN y m ($k$ en kN/m, $c$ en kN/m³).*"
    )

    # 2. Tamaño --------------------------------------------------------------
    st.header("2. Tamaño del sistema y modelo")
    n = st.radio("Tamaño del sistema (número de incógnitas)", [2, 3, 4], index=1,
                 horizontal=True, format_func=lambda v: f"{v} × {v}", key="nl_n")
    st.caption(f"Edificio de {n} pisos: {n} desplazamientos laterales $u_1,\\dots,u_{n}$ como incógnitas.")

    # 3. Parámetros ----------------------------------------------------------
    st.header("3. Parámetros de la estructura")
    c = st.number_input("Coeficiente de rigidización no lineal c (kN/m³)",
                        min_value=0.0, value=5000.0, step=500.0, key="nl_c")
    cols = st.columns(n)
    k, P = [], []
    for i in range(n):
        with cols[i]:
            k.append(st.number_input(f"k{i + 1} (kN/m)", min_value=1.0, value=1000.0,
                                     step=100.0, key=f"nl_k{i}"))
            P.append(st.number_input(f"P{i + 1} (kN)", value=30.0, step=5.0, key=f"nl_P{i}"))

    eqs = _ecuaciones_equilibrio(n, k, c, P)
    with st.expander("Ver ecuaciones de equilibrio generadas"):
        st.code("\n".join(f"F{i + 1}(x) = {e}" for i, e in enumerate(eqs)), language="python")

    # 4. Método --------------------------------------------------------------
    st.header("4. Método de solución")
    metodo = st.radio("Método numérico", ["Newton-Raphson", "Punto fijo"],
                      horizontal=True, key="nl_metodo")

    c1, c2 = st.columns(2)
    with c1:
        tol = st.select_slider("Tolerancia", options=[1e-4, 1e-6, 1e-8, 1e-10, 1e-12],
                               value=1e-8, format_func=lambda v: f"{v:.0e}", key="nl_tol")
    with c2:
        max_iter = st.number_input("Máximo de iteraciones", min_value=5, max_value=1000,
                                   value=100, step=5, key="nl_maxit")

    st.markdown("**Aproximación inicial $u^{(0)}$ (m)**")
    cx = st.columns(n)
    x0 = [cx[i].number_input(f"u{i + 1}", value=0.0, format="%.4f", step=0.01,
                             key=f"nl_x0_{i}") for i in range(n)]

    usar_jac, despeje, gs_flag, w = False, None, False, 1.0
    if metodo == "Newton-Raphson":
        usar_jac = st.checkbox("Usar Jacobiana analítica (matriz de rigidez tangente)",
                               value=True, key="nl_jac")
        st.caption("Si se desactiva, la Jacobiana se calcula por diferencias centrales.")
    else:
        despeje = st.radio("Despeje x = G(x)",
                           ["A: despeje directo de cada $u_i$", "B: relajación  $u - \\omega F/K_{ii}$"],
                           key="nl_despeje")
        gs_flag = st.checkbox("Usar Gauss-Seidel (actualizar con los valores más recientes)",
                              value=True, key="nl_gs")
        if despeje.startswith("B"):
            w = st.slider("Factor de relajación ω", 0.1, 1.5, 0.8, 0.05, key="nl_w")

    # 5. Resolución ----------------------------------------------------------
    st.header("5. Resultados")
    F = crear_funcion(eqs, n)
    sol, hist, mensaje = None, [], None
    try:
        if metodo == "Newton-Raphson":
            J = _jacobiana_analitica(n, k, c) if usar_jac else None
            sol, it, err, hist = newton_raphson(F, x0, J=J, tol=tol, max_iter=int(max_iter))
        else:
            gx = (_despeje_directo(n, k, c, P) if despeje.startswith("A")
                  else _despeje_relajacion(n, k, c, P, w))
            with st.expander("Ver despeje G(x) generado"):
                st.code("\n".join(f"g{i + 1}(x) = {g}" for i, g in enumerate(gx)), language="python")
            G = crear_funcion(gx, n)
            sol, it, err, hist = punto_fijo(G, x0, tol=tol, max_iter=int(max_iter),
                                            gauss_seidel=gs_flag)
    except ErrorConvergencia as e:
        mensaje, hist = str(e), e.historial
    except Exception as e:
        st.error(f"Error al evaluar el sistema: {type(e).__name__}: {e}")
        return

    if sol is None:
        st.error(f"❌ {mensaje}")
    else:
        resid = max(abs(v) for v in F(sol))
        st.success(f"✅ Convergió en {it} iteraciones.")
        m1, m2, m3 = st.columns(3)
        m1.metric("Iteraciones", it)
        m2.metric("Error final (máx |Δu|)", f"{err:.2e}")
        m3.metric("Residuo máx |F(u)| (kN)", f"{resid:.2e}")

        # Solución lineal de comparación con resolver_sistema
        K = [[0.0] * n for _ in range(n)]
        for i in range(n):
            K[i][i] = k[i] + (k[i + 1] if i < n - 1 else 0.0)
            if i < n - 1:
                K[i][i + 1] = K[i + 1][i] = -k[i + 1]
        try:
            u_lin = resolver_sistema(K, P)
        except ValueError:
            u_lin = [float("nan")] * n

        u = [0.0] + list(sol)
        deriva = [u[i + 1] - u[i] for i in range(n)]
        cortante = [k[i] * deriva[i] + c * deriva[i] ** 3 for i in range(n)]
        df_res = pd.DataFrame({
            "Piso": [f"{i + 1}" for i in range(n)],
            "u lineal (mm)": [v * 1000 for v in u_lin],
            "u no lineal (mm)": [v * 1000 for v in sol],
            "Diferencia (%)": [100 * (s - l) / l if l else 0.0 for s, l in zip(sol, u_lin)],
            "Deriva (mm)": [d * 1000 for d in deriva],
            "Cortante V (kN)": cortante,
        })
        st.dataframe(df_res.style.format({
            "u lineal (mm)": "{:.3f}", "u no lineal (mm)": "{:.3f}",
            "Diferencia (%)": "{:+.2f}", "Deriva (mm)": "{:.3f}", "Cortante V (kN)": "{:.2f}"}),
            hide_index=True, use_container_width=True)
        st.caption("La rigidización por grandes deformaciones hace que los desplazamientos "
                   "no lineales resulten menores que los del análisis lineal.")

    # 6. Gráficas ------------------------------------------------------------
    st.header("6. Gráficas")
    g1, g2 = st.columns(2)

    with g1:
        datos = [(k_, e) for k_, _, e in hist
                 if e is not None and e > 0 and np.isfinite(e)]
        if datos:
            ks, errs = zip(*datos)
            fig, ax = plt.subplots(figsize=(5, 3.6))
            ax.semilogy(ks, errs, "o-", color="tab:red")
            ax.axhline(tol, color="gray", ls="--", label=f"tol = {tol:.0e}")
            ax.set_xlabel("Iteración")
            ax.set_ylabel("Error (máx |Δu|)")
            ax.set_title(f"Historial de errores: {metodo}")
            ax.grid(True, which="both", alpha=0.3)
            ax.legend()
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
        else:
            st.info("No hay errores para graficar.")

    with g2:
        if sol is not None:
            fig, ax = plt.subplots(figsize=(5, 3.6))
            pisos = list(range(n + 1))
            ax.plot([0.0] + [v * 1000 for v in u_lin], pisos, "s--", label="Lineal")
            ax.plot([0.0] + [v * 1000 for v in sol], pisos, "o-", label="No lineal")
            ax.axvline(0, color="k", lw=0.8)
            ax.set_xlabel("Desplazamiento lateral (mm)")
            ax.set_ylabel("Nivel (piso)")
            ax.set_yticks(pisos)
            ax.set_title("Configuración deformada")
            ax.grid(True, alpha=0.3)
            ax.legend()
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

    # 7. Historial -----------------------------------------------------------
    st.header("7. Historial iterativo")
    if hist:
        filas = [{"k": k_, **{f"u{i + 1} (m)": v for i, v in enumerate(x)},
                  "Error": e if e is not None else np.nan} for k_, x, e in hist]
        df_h = pd.DataFrame(filas)
        formato = {f"u{i + 1} (m)": "{:.8f}" for i in range(n)}
        formato["Error"] = "{:.3e}"
        st.dataframe(df_h.style.format(formato, na_rep="---"),
                     hide_index=True, use_container_width=True)
    else:
        st.info("Sin historial de iteraciones.")
