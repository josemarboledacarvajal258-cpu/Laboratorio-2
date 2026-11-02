"""Pestaña 3: interpolación de Lagrange para reconstruir caudal diario."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

from ModLab3 import bases_lagrange, ventana_nodos, U, COL, graficar_serie, ficha
import ModLab3 as metricas   # el código usa metricas.errores, metricas.mae, etc.


def _lagrange_local(tn, yn, tv, k):
    """Lagrange local de k nodos evaluado en cada punto de tv."""
    sal = []
    for t in tv:
        idx = ventana_nodos(tn, t, k)
        xs, ys = tn[idx], yn[idx]
        sal.append(sum(ys[j] * bases_lagrange(xs, j, t) for j in range(k)))
    return np.array(sal, float)


def _interpretar(k, n_nodos, m_glob, e_loc, p, y_real):
    rm_loc = metricas.rmse(e_loc)
    rm_glob = m_glob["RMSE"]
    puntos = []

    if rm_glob > 2 * rm_loc:
        puntos.append(
            f"**Global vs local:** el polinomio global (grado {n_nodos - 1}) tiene un RMSE de "
            f"{rm_glob:.2f} {U}, frente a {rm_loc:.2f} {U} del local de {k} nodos. Es el "
            "**fenómeno de Runge**: un grado alto oscila entre nodos aunque pase por todos los datos.")
    elif rm_loc > 2 * rm_glob:
        puntos.append(
            f"**Global vs local:** aquí el global (RMSE {rm_glob:.2f} {U}) supera al local de {k} nodos "
            f"({rm_loc:.2f} {U}). Con pocos nodos o una serie muy suave el grado alto no oscila, "
            "pero eso no se mantiene si se agregan nodos.")
    else:
        puntos.append(
            f"**Global vs local:** ambos tienen errores comparables (RMSE {rm_glob:.2f} y "
            f"{rm_loc:.2f} {U}). Con pocos nodos el grado global aún es moderado.")

    if y_real is not None:
        puntos.append(
            f"**Punto consultado:** la interpolación estima {p:.2f} {U} y la medición reservada es "
            f"{y_real:.2f} {U} (error de {p - y_real:+.2f} {U}, {100 * abs(p - y_real) / abs(y_real):.1f} %).")

    puntos.append(
        "**Límites:** pasar por los nodos solo garantiza reproducir los datos. Las discrepancias son "
        "frente a mediciones con incertidumbre, no una cota del error físico, y reconstruir datos "
        "interiores no demuestra capacidad de pronóstico. No se garantiza positividad ni monotonía.")
    st.markdown("\n".join(f"- {t}" for t in puntos))


def mostrar(ctx):
    R = ctx["R"]
    tn, yn = R["t"][ctx["nodos"]], R["y"][ctx["nodos"]]

    # 1. Contexto ------------------------------------------------------------
    st.header("1. Contexto en ingeniería civil")
    st.markdown(
        "En hidrología e hidráulica, una serie de caudales con días sin dato (falla del sensor, "
        "mantenimiento) debe completarse antes de calcular volúmenes, caudales de diseño o balances. "
        f"Aquí se **reconstruyen observaciones interiores reservadas** a partir de los demás días, en **{U}**.")
    ficha(ctx)
    st.markdown("Dados los nodos $(t_i, Q_i)$, el polinomio de Lagrange es una suma ponderada de bases "
                "que valen 1 en su nodo y 0 en los demás:")
    st.latex(r"P(t)=\sum_{i=0}^{n}Q_i\,L_i(t),\qquad "
             r"L_i(t)=\prod_{k\ne i}\frac{t-t_k}{t_i-t_k},\qquad L_i(t_j)=\delta_{ij}")
    st.markdown("*Supuesto: el caudal entre nodos varía de forma suave. Los datos deben verificarse contra la fuente.*")

    # 2. Datos ---------------------------------------------------------------
    st.header("2. Datos y partición")
    c = st.columns(3)
    c[0].metric("Nodos de construcción", len(ctx["nodos"]))
    c[1].metric("Observaciones reservadas", len(ctx["val"]))
    c[2].metric("Grado del polinomio global", len(ctx["nodos"]) - 1)
    fig, ax = plt.subplots(figsize=(8, 3))
    graficar_serie(ax, R)
    ax.legend(fontsize=7)
    ax.set_title("Serie, nodos y observaciones reservadas")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    # 3. Entradas ------------------------------------------------------------
    st.header("3. Entradas")
    c = st.columns(2)
    k = int(c[0].radio("Nodos locales alrededor de la consulta", [2, 3, 4],
                       horizontal=True, index=1, key="lg_k"))
    t = c[1].slider("Día de consulta t", float(tn[0]), float(tn[-1]),
                    float(R["t_val"][0]), 0.25, key="lg_t")
    idx = ventana_nodos(tn, t, k)
    xs, ys = tn[idx], yn[idx]

    # 4. Resultados ----------------------------------------------------------
    st.header("4. Resultados")
    Lt = np.array([bases_lagrange(xs, j, t) for j in range(k)])
    tabla = pd.DataFrame({"i": range(k), "t_i [día]": xs, f"Q_i [{U}]": ys,
                          "L_i(t)": Lt, f"Q_i·L_i(t) [{U}]": ys * Lt})
    st.dataframe(tabla.style.format({"t_i [día]": "{:.0f}", f"Q_i [{U}]": "{:.3f}", "L_i(t)": "{:.5f}",
                                     f"Q_i·L_i(t) [{U}]": "{:.3f}"}),
                 hide_index=True, use_container_width=True)

    p = float(Lt @ ys)
    j = np.where(np.isclose(R["t_val"], t))[0]
    y_real = float(R["y_val"][j[0]]) if len(j) else None
    c = st.columns(3)
    c[0].metric(f"P(t={t:g}) [{U}]", f"{p:.3f}")
    c[1].metric("ΣL_i(t) (debe ser 1)", f"{Lt.sum():.6f}")
    if y_real is not None:
        c[2].metric(f"Error e = ŷ − y [{U}]", f"{p - y_real:+.3f}",
                    help="Contra la medición reservada de ese día")
    else:
        c[2].metric("Medición reservada", "no hay en ese día")

    with st.expander("Ver comprobación de reproducción de nodos: L_i(t_j) = δ_ij"):
        st.dataframe(pd.DataFrame([[bases_lagrange(xs, i, xj) for xj in xs] for i in range(k)],
                                  index=[f"L_{i}" for i in range(k)],
                                  columns=[f"t_{q}={x:.0f}" for q, x in enumerate(xs)]).round(12))

    loc = _lagrange_local(tn, yn, R["t_val"], k)
    e_loc = metricas.errores(loc, R["y_val"])
    m_glob = R["metricas"].loc["Lagrange"]
    m1, m2 = st.columns(2)
    m1.markdown(f"**Local de {k} nodos** (en las {len(ctx['val'])} reservadas)  \n"
                f"MAE = {metricas.mae(e_loc):.3f} · RMSE = {metricas.rmse(e_loc):.3f} · "
                f"E_máx = {metricas.emax(e_loc):.3f} {U}")
    m2.markdown(f"**Global** ({len(tn)} nodos, grado {len(tn) - 1})  \n"
                f"MAE = {m_glob['MAE']:.3f} · RMSE = {m_glob['RMSE']:.3f} · "
                f"E_máx = {m_glob['E_max']:.3f} {U}")

    # 5. Gráficas ------------------------------------------------------------
    st.header("5. Gráficas")
    g1, g2 = st.columns(2)
    uu = np.linspace(xs[0], xs[-1], 200)

    with g1:
        fig, ax = plt.subplots(figsize=(5, 3.4))
        graficar_serie(ax, R)
        ax.plot(uu, sum(ys[i] * bases_lagrange(xs, i, uu) for i in range(k)),
                color=COL["Lagrange"], lw=1.6, label=f"local {k} nodos")
        ax.plot([t], [p], "*", color="gold", ms=14, mec="k", label="consulta")
        ax.legend(fontsize=7)
        ax.set_title("Interpolante local y consulta")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with g2:
        fig, ax = plt.subplots(figsize=(5, 3.4))
        for i in range(k):
            ax.plot(uu, bases_lagrange(xs, i, uu), label=f"L_{i}")
        ax.axhline(0, color="k", lw=0.5)
        ax.plot([t] * k, Lt, "ko", ms=4)
        ax.set_xlabel("Día")
        ax.grid(alpha=0.3)
        ax.legend(fontsize=7)
        ax.set_title("Bases de Lagrange")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 3))
    w, x = 0.38, np.arange(len(ctx["val"]))
    ax.bar(x - w / 2, metricas.errores(R["pred"]["Lagrange"], R["y_val"]), w,
           label="global", color=COL["Lagrange"])
    ax.bar(x + w / 2, e_loc, w, label=f"local {k}", color="#9467bd")
    ax.axhline(0, color="k", lw=0.6)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{v:.0f}" for v in R["t_val"]], fontsize=7)
    ax.set_xlabel("Día reservado")
    ax.set_ylabel(f"e = ŷ − y [{U}]")
    ax.legend(fontsize=7)
    ax.set_title("Errores con signo en las reservadas")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    # 6. Interpretación ------------------------------------------------------
    st.header("6. Interpretación de los resultados")
    _interpretar(k, len(tn), m_glob, e_loc, p, y_real)