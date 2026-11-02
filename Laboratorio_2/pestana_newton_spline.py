"""Pestaña 4: interpolación de Newton comparada con spline cúbico natural."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

from ModLab3 import (diferencias_divididas, evaluar_newton, agregar_nodo,
                     spline_natural_momentos, tramo_spline, lagrange_eval,
                     U, COL, graficar_serie, ficha)
import ModLab3 as metricas


def _interpretar(R):
    mn = R["metricas"].loc["Newton"]
    ms = R["metricas"].loc["Spline natural (propio)"]
    ac = R["acuerdo"]
    puntos = []

    if mn["E_max"] > 2 * ms["E_max"]:
        puntos.append(
            f"**Comparación:** el E_máx de Newton es {mn['E_max']:.1f} {U} y el del spline "
            f"{ms['E_max']:.1f} {U}. El polinomio global de grado {len(R['nodos']) - 1} oscila entre nodos, "
            "mientras el spline, al ser por tramos cúbicos, se mantiene cerca de los datos.")
    elif ms["E_max"] > 2 * mn["E_max"]:
        puntos.append(
            f"**Comparación:** con esta partición Newton (E_máx {mn['E_max']:.1f} {U}) supera al spline "
            f"({ms['E_max']:.1f} {U}). Ocurre cuando hay pocos nodos y la serie es muy suave; no implica "
            "que el polinomio global sea mejor en general.")
    else:
        puntos.append(
            f"**Comparación:** los errores máximos son comparables (Newton {mn['E_max']:.1f} {U}, "
            f"spline {ms['E_max']:.1f} {U}). No se presupone un método ganador.")

    puntos.append(
        f"**Consistencia numérica:** Newton y Lagrange difieren como máximo en {ac['Newton vs Lagrange']:.1e} {U} "
        "(son el mismo polinomio; la diferencia mide la implementación, no el error frente al río). "
        f"El spline propio coincide con SciPy hasta {ac['Spline propio vs SciPy']:.1e} {U}.")

    puntos.append(
        "**Límites:** el spline no garantiza positividad ni monotonía, reconstruir datos interiores no "
        "demuestra pronóstico y la extrapolación está desactivada. Cambie *p*, el hueco o el recorte en "
        "la barra lateral y observe cómo cambian las métricas.")
    st.markdown("\n".join(f"- {t}" for t in puntos))


def mostrar(ctx):
    R = ctx["R"]
    tn, yn = R["t"][ctx["nodos"]], R["y"][ctx["nodos"]]

    st.title("Interpolación de Newton y spline: comparación de métodos en caudales")

    # 1. Contexto ------------------------------------------------------------
    st.header("1. Contexto en ingeniería civil")
    st.markdown(
        "Se usa **la misma base y la misma partición** que la pestaña de Lagrange para una comparación "
        "justa: un polinomio global (Newton) frente a una construcción por tramos (spline), evaluados "
        "sobre las mismas observaciones reservadas.")
    ficha(ctx)
    st.latex(r"P(t)=f[t_0]+f[t_0,t_1](t-t_0)+\dots+f[t_0,\dots,t_n]\prod_{i<n}(t-t_i)")
    st.latex(r"h_{i-1}M_{i-1}+2(h_{i-1}+h_i)M_i+h_iM_{i+1}=6(\delta_i-\delta_{i-1}),\quad M_0=M_n=0")

    # 2. Tamaño --------------------------------------------------------------
    st.header("2. Tamaño de la tabla y nodos")
    c = st.columns(2)
    m = int(c[0].radio("Número de nodos de la tabla de diferencias", [3, 4, 5, 6],
                       horizontal=True, index=1, key="ns_m"))
    i0 = c[1].slider("Primer nodo de la ventana (índice entre los nodos)", 0,
                     max(1, len(tn) - m - 1), 0, key="ns_i0")
    xs, ys = tn[i0:i0 + m], yn[i0:i0 + m]

    # 3. Newton --------------------------------------------------------------
    st.header("3. Resultados: Newton")
    T = diferencias_divididas(xs, ys)
    tabla = pd.DataFrame(T, columns=["f[ ]"] + [f"orden {j}" for j in range(1, m)])
    tabla.insert(0, "t_i", xs)
    st.dataframe(tabla.style.format(na_rep="", precision=5), hide_index=True, use_container_width=True)
    cf = T[0]
    st.markdown("Coeficientes de Newton (fila 0): " + ", ".join(f"`{v:.4f}`" for v in cf))

    if st.checkbox("Incorporar el siguiente nodo y ver qué coeficientes se conservan",
                   value=True, key="ns_add") and i0 + m < len(tn):
        _, _, c2, ok = agregar_nodo(xs, ys, tn[i0 + m], yn[i0 + m])
        st.success(f"Coeficientes previos conservados: **{ok}**. Solo se agrega el de orden {m}: `{c2[-1]:.5f}`.")

    t = st.slider("Día de consulta", float(xs[0]), float(xs[-1]),
                  float(xs[0] + (xs[-1] - xs[0]) / 2), 0.25, key="ns_t")
    pn = float(evaluar_newton(xs, cf, [t])[0])
    pl = float(lagrange_eval(xs, ys, [t])[0])
    c = st.columns(3)
    c[0].metric(f"P_Newton(t={t:g}) [{U}]", f"{pn:.3f}")
    c[1].metric("|Newton − Lagrange| (misma ventana)", f"{abs(pn - pl):.2e}")
    c[2].metric("Residual en nodos", f"{np.max(np.abs(evaluar_newton(xs, cf, xs) - ys)):.2e}")

    # 4. Spline --------------------------------------------------------------
    st.header("4. Resultados: spline natural en la misma ventana")
    M = spline_natural_momentos(xs, ys)
    st.dataframe(pd.DataFrame({"t_i": xs, "M_i = S''(t_i)": M}).style.format(precision=5),
                 hide_index=True, use_container_width=True)
    ii = min(int(np.searchsorted(xs, t, side="right") - 1), m - 2)
    a, b, cc, d = tramo_spline(xs, ys, ii, M)
    x_i = f"{xs[ii]:.0f}"
    st.latex(rf"S_{{{ii}}}(t)={a:.3f}{b:+.4f}(t-{x_i}){cc:+.4f}(t-{x_i})^2{d:+.5f}(t-{x_i})^3")
    st.caption("Spline natural: S'' = 0 en los extremos de la ventana (se aplana la curvatura en los bordes).")

    # 5. Comparación ---------------------------------------------------------
    st.header("5. Comparación con los mismos nodos y reservadas")
    mt = R["metricas"].rename(columns={"MAE": f"MAE [{U}]", "RMSE": f"RMSE [{U}]", "E_max": f"E_máx [{U}]"})
    st.dataframe(mt.style.format(precision=3), use_container_width=True)
    c = st.columns(2)
    c[0].write("Residual en nodos")
    c[0].dataframe(pd.Series({k: f"{v:.2e}" for k, v in R["reproduccion_nodos"].items()}).to_frame(U))
    c[1].write("Acuerdo entre implementaciones")
    c[1].dataframe(pd.Series({k: f"{v:.2e}" for k, v in R["acuerdo"].items()}).to_frame(U))

    # 6. Gráficas ------------------------------------------------------------
    st.header("6. Gráficas")
    sel = st.multiselect("Curvas a mostrar", ["Lagrange", "Newton", "Spline natural (propio)"],
                         default=["Newton", "Spline natural (propio)"], key="ns_sel")
    recorte = st.checkbox("Limitar el eje Q al rango de los datos", value=True, key="ns_rec")

    fig, ax = plt.subplots(figsize=(8, 3.6))
    graficar_serie(ax, R)
    for s in sel:
        ax.plot(R["t_curva"], R["curvas"][s], lw=1.3, color=COL[s], label=s)
    if recorte:
        ax.set_ylim(R["y"].min() - 40, R["y"].max() + 40)
    ax.legend(fontsize=7)
    ax.set_title("Newton vs spline sobre toda la serie")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 3))
    w, x = 0.2, np.arange(len(ctx["val"]))
    for j, (nombre, v) in enumerate(R["pred"].items()):
        ax.bar(x + (j - 1.5) * w, metricas.errores(v, R["y_val"]), w, label=nombre, color=COL[nombre])
    ax.axhline(0, color="k", lw=0.6)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{v:.0f}" for v in R["t_val"]], fontsize=7)
    ax.set_xlabel("Día reservado")
    ax.set_ylabel(f"e = ŷ − y [{U}]")
    ax.legend(fontsize=6)
    ax.set_title("Errores con signo")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    # 7. Interpretación ------------------------------------------------------
    st.header("7. Interpretación de los resultados")
    _interpretar(R)
