"""Pestaña de sistemas lineales: equilibrio y reacciones en apoyos (ingeniería civil)."""

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

import graficos_estructurales as ge
import modelos_estructurales as me
from ModLab2 import resolver_sistema

DESCRIPCION = {
    2: "Viga simplemente apoyada con una carga vertical. Incógnitas: R_A y R_B.",
    3: "Viga con apoyo fijo en A y móvil en B, bajo una carga inclinada. Incógnitas: A_x, A_y y B_y.",
    4: "Arco triarticulado con una carga vertical. Incógnitas: A_x, A_y, B_x y B_y "
       "(la articulación en C aporta la cuarta ecuación).",
}

LATEX = {
    2: {
        "ecuaciones": [r"\sum F_y = 0:\quad R_A + R_B = P",
                       r"\sum M_A = 0:\quad L\,R_B = P\,a"],
        "matriz": r"\begin{bmatrix}1&1\\0&L\end{bmatrix}"
                  r"\begin{bmatrix}R_A\\R_B\end{bmatrix}="
                  r"\begin{bmatrix}P\\P\,a\end{bmatrix}",
    },
    3: {
        "ecuaciones": [r"\sum F_x = 0:\quad A_x = -F\cos\theta",
                       r"\sum F_y = 0:\quad A_y + B_y = F\sin\theta",
                       r"\sum M_A = 0:\quad L\,B_y = F\sin\theta\;a"],
        "matriz": r"\begin{bmatrix}1&0&0\\0&1&1\\0&0&L\end{bmatrix}"
                  r"\begin{bmatrix}A_x\\A_y\\B_y\end{bmatrix}="
                  r"\begin{bmatrix}-F\cos\theta\\F\sin\theta\\F\sin\theta\;a\end{bmatrix}",
    },
    4: {
        "ecuaciones": [r"\sum F_x = 0:\quad A_x + B_x = 0",
                       r"\sum F_y = 0:\quad A_y + B_y = P",
                       r"\sum M_A = 0:\quad L\,B_y = P\,a",
                       r"\sum M_C^{izq} = 0:\quad -h\,A_x + \tfrac{L}{2}A_y = P\left(\tfrac{L}{2}-a\right)"],
        "matriz": r"\begin{bmatrix}1&0&1&0\\0&1&0&1\\0&0&0&L\\-h&L/2&0&0\end{bmatrix}"
                  r"\begin{bmatrix}A_x\\A_y\\B_x\\B_y\end{bmatrix}="
                  r"\begin{bmatrix}0\\P\\P\,a\\P\,m\end{bmatrix}",
        "nota": "m = L/2 − a si la carga está a la izquierda de la clave (a < L/2); en caso contrario m = 0.",
    },
}


def _fmt(valor, decimales=3):
    """Formatea evitando el '-0.000'."""
    return f"{round(valor, decimales) + 0.0:.{decimales}f}"


def _pedir_entradas(n):
    """Muestra los campos de entrada del modelo y devuelve el modelo, o None si hay datos inválidos."""
    c1, c2, c3, c4 = st.columns(4)

    if n == 2:
        L = c1.number_input("Luz L (m)", min_value=0.5, value=6.0, step=0.5, key="n2_L")
        a = c2.number_input("Posición de la carga a (m)", min_value=0.0, value=2.0, step=0.5, key="n2_a")
        P = c3.number_input("Carga P (kN)", min_value=0.1, value=30.0, step=1.0, key="n2_P")
        if a > L:
            st.error("La posición de la carga `a` no puede ser mayor que la luz `L`.")
            return None
        return me.viga_simple(L, a, P)

    if n == 3:
        L = c1.number_input("Luz L (m)", min_value=0.5, value=6.0, step=0.5, key="n3_L")
        a = c2.number_input("Posición de la carga a (m)", min_value=0.0, value=2.0, step=0.5, key="n3_a")
        F = c3.number_input("Carga F (kN)", min_value=0.1, value=40.0, step=1.0, key="n3_F")
        theta = c4.number_input("Ángulo θ bajo la horizontal (°)", min_value=0.0, max_value=90.0,
                                value=30.0, step=5.0, key="n3_theta")
        if a > L:
            st.error("La posición de la carga `a` no puede ser mayor que la luz `L`.")
            return None
        return me.viga_inclinada(L, a, F, theta)

    L = c1.number_input("Luz L (m)", min_value=0.5, value=8.0, step=0.5, key="n4_L")
    h = c2.number_input("Altura de la clave h (m)", min_value=0.1, value=3.0, step=0.5, key="n4_h")
    a = c3.number_input("Posición de la carga a (m)", min_value=0.0, value=2.0, step=0.5, key="n4_a")
    P = c4.number_input("Carga P (kN)", min_value=0.1, value=40.0, step=1.0, key="n4_P")
    if a > L:
        st.error("La posición de la carga `a` no puede ser mayor que la luz `L`.")
        return None
    return me.arco_triarticulado(L, h, a, P)


def mostrar():
    st.header("Sistemas lineales: equilibrio y reacciones en los apoyos")

    # ── 1. Contexto ─────────────────────────────────────────
    st.subheader("1. Contexto en ingeniería civil")
    st.markdown(
        "Para diseñar una viga, un pórtico o un arco, el primer paso es conocer las **reacciones en los apoyos** "
        "y, a partir de ellas, las **fuerzas internas** (cortante, momento flector y fuerza axial). "
        "Ambas salen del **equilibrio estático** de la estructura: "
        "$\\sum F_x = 0,\\; \\sum F_y = 0,\\; \\sum M = 0$.\n\n"
        "Cuando la estructura es isostática, el número de ecuaciones coincide con el de incógnitas y el equilibrio "
        "se convierte en un **sistema lineal** $A\\,x = b$, donde $x$ son las reacciones. "
        "Aquí se resuelve con `resolver_sistema` de `ModLab2` (eliminación de Gauss con pivoteo parcial).\n\n"
        "*Convención: $x$ positivo hacia la derecha, $y$ positivo hacia arriba, momentos positivos antihorarios. "
        "Unidades: kN y m.*"
    )

    # ── 2. Tamaño del sistema y modelo ──────────────────────
    st.subheader("2. Tamaño del sistema y modelo")
    n = st.radio("Tamaño del sistema (número de incógnitas)", [2, 3, 4], index=0, horizontal=True,
                 format_func=lambda k: f"{k} × {k}", key="lin_n")
    st.caption(DESCRIPCION[n])
    contenedor_modelo = st.container()

    # ── 3. Entradas ─────────────────────────────────────────
    st.subheader("3. Entradas")
    modelo = _pedir_entradas(n)
    if modelo is None:
        return

    with contenedor_modelo:
        st.markdown(f"**{modelo['titulo']}**")
        col_fig, col_eq = st.columns([3, 2])
        fig = ge.dibujar_estructura(modelo, titulo="Modelo (reacciones en su sentido positivo supuesto)")
        col_fig.pyplot(fig)
        plt.close(fig)
        with col_eq:
            st.markdown("**Ecuaciones de equilibrio**")
            for ecuacion in LATEX[n]["ecuaciones"]:
                st.latex(ecuacion)
            st.markdown("**Forma matricial** $A\\,x = b$")
            st.latex(LATEX[n]["matriz"])
            if "nota" in LATEX[n]:
                st.caption(LATEX[n]["nota"])

    # ── 4. Resultados ───────────────────────────────────────
    st.subheader("4. Resultados")
    try:
        sol = resolver_sistema(modelo["A"], modelo["b"])
    except ValueError as error:
        st.error(f"No se pudo resolver el sistema: {error}")
        return

    st.markdown("**Sistema numérico** (matriz $A$ y vector $b$)")
    df_sistema = pd.DataFrame(modelo["A"], columns=[s for s, _, _, _ in modelo["incognitas"]],
                              index=modelo["ecuaciones"])
    df_sistema["b"] = modelo["b"]
    st.dataframe(df_sistema)

    st.markdown("**Reacciones calculadas**")
    filas = [{"Incógnita": simb, "Descripción": desc, "Valor (kN)": _fmt(v), "Sentido": me.sentido(eje, v)}
             for (simb, desc, eje, _), v in zip(modelo["incognitas"], sol)]
    st.dataframe(pd.DataFrame(filas), hide_index=True)

    fig = ge.dibujar_estructura(modelo, valores=sol, titulo="Reacciones calculadas")
    st.pyplot(fig)
    plt.close(fig)

    # ── 5. Análisis de resultados ───────────────────────────
    st.subheader("5. Análisis de resultados")

    st.markdown("**5.1 Verificación del equilibrio (residuo $r = b - A\\hat{x}$)**")
    r = me.residuo(modelo["A"], modelo["b"], sol)
    escala = max(1.0, max(abs(v) for v in modelo["b"]))
    r_max = max(abs(v) for v in r)
    st.dataframe(pd.DataFrame({"Ecuación": modelo["ecuaciones"], "Residuo": [f"{v:.2e}" for v in r]}),
                 hide_index=True)
    if r_max < 1e-9 * escala:
        st.success(f"‖r‖∞ = {r_max:.2e} ≈ 0: la solución satisface todas las ecuaciones de equilibrio.")
    else:
        st.warning(f"‖r‖∞ = {r_max:.2e}: el residuo no es despreciable, revisa los datos de entrada.")

    st.markdown("**5.2 Comparación con la solución analítica**")
    dif = [abs(s - an) for s, an in zip(sol, modelo["analitica"])]
    st.dataframe(pd.DataFrame({
        "Incógnita": [s for s, _, _, _ in modelo["incognitas"]],
        "ModLab2 (kN)": [_fmt(v, 4) for v in sol],
        "Analítica (kN)": [_fmt(v, 4) for v in modelo["analitica"]],
        "Diferencia": [f"{d:.2e}" for d in dif],
    }), hide_index=True)
    st.caption(f"Diferencia máxima: {max(dif):.2e} kN. La solución analítica sale de despejar las ecuaciones a mano.")

    st.markdown("**5.3 Fuerzas internas**")
    datos = me.fuerzas_internas(modelo, sol)
    st.dataframe(pd.DataFrame({
        "Fuerza interna": [d[0] for d in datos],
        "Valor": [_fmt(d[1], 2) for d in datos],
        "Unidad": [d[2] for d in datos],
    }), hide_index=True)
    if modelo["tipo"] == "viga":
        fig = ge.dibujar_diagramas_viga(modelo, sol)
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.caption("En una articulación el momento flector es nulo; las fuerzas en C son las que "
                   "transmite una mitad del arco a la otra.")

    st.markdown("**5.4 Interpretación**")
    for frase in me.interpretar(modelo, sol):
        st.markdown(f"- {frase}")
