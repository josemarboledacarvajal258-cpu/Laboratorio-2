"""Gráficos de las estructuras: esquema con cargas y reacciones, y diagramas de cortante y momento."""

import math

import matplotlib.pyplot as plt

AZUL = "#1f77b4"
ROJO = "#d62728"
GRIS = "#555555"


def _flecha(ax, ini, fin, color, lw=2.4, estilo="-"):
    ax.annotate("", xy=fin, xytext=ini,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, linestyle=estilo,
                                shrinkA=0, shrinkB=0, mutation_scale=16))


def _cota(ax, x0, x1, y, texto):
    ax.annotate("", xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="<->", color=GRIS, lw=1.2, shrinkA=0, shrinkB=0))
    ax.text((x0 + x1) / 2, y, texto, ha="center", va="bottom", fontsize=9, color=GRIS)


def dibujar_estructura(modelo, valores=None, titulo=None):
    """
    Esquema de la estructura con la carga y las reacciones.
    valores=None  -> reacciones desconocidas, dibujadas en su sentido positivo supuesto.
    valores=[...] -> reacciones calculadas: la flecha cambia de sentido según el signo.
    """
    L = modelo["L"]
    puntos = modelo["puntos"]
    ref = max(L, max(p[1] for p in puntos))
    u = 0.20 * ref
    fig, ax = plt.subplots(figsize=(7.5, 3.9))
    pts = list(puntos)

    ax.plot([p[0] for p in puntos], [p[1] for p in puntos],
            color="black", lw=4, solid_capstyle="round", zorder=2)

    for (x, y), tipo in modelo["apoyos"]:
        ax.plot(x, y - 0.045 * ref, marker="^" if tipo == "fijo" else "o", ms=13, ls="",
                mfc=GRIS if tipo == "fijo" else "white", mec=GRIS, zorder=3)
        pts.append((x, y - 0.10 * ref))
    for x, y in modelo["articulaciones"]:
        ax.plot(x, y, "o", ms=9, mfc="white", mec="black", mew=2, zorder=4)

    # Carga
    c = modelo["carga"]
    px, py = c["punto"]
    mag = math.hypot(c["fx"], c["fy"]) or 1.0
    ux, uy = c["fx"] / mag, c["fy"] / mag
    cola = (px - ux * 1.4 * u, py - uy * 1.4 * u)
    _flecha(ax, cola, (px, py), ROJO, lw=3)
    # La etiqueta va del lado contrario al que avanza la flecha, para no cruzarla
    ha_carga = "right" if ux > 0.2 else ("left" if ux < -0.2 else "center")
    ax.text(cola[0], cola[1] + 0.03 * ref, c["etiqueta"], color=ROJO, ha=ha_carga, va="bottom", fontsize=10)
    pts += [cola, (px, py + 1.6 * u * (uy < 0))]

    # Reacciones
    vmax = max((abs(v) for v in valores), default=0.0) if valores else 0.0
    desplaz_h = 0.07 * ref if modelo["tipo"] == "viga" else 0.0
    for i, (simb, _desc, eje, (x0, y0)) in enumerate(modelo["incognitas"]):
        if valores is None:
            signo, largo, etiqueta = 1.0, u, f"${simb}$"
        else:
            v = valores[i]
            if abs(v) < 1e-9:
                ax.text(x0 + 0.03 * ref, y0 + 0.5 * u, f"${simb}$ = 0", color=AZUL, fontsize=10)
                continue
            signo = 1.0 if v > 0 else -1.0
            largo = u * max(abs(v) / vmax, 0.3)
            etiqueta = f"${simb}$ = {round(v, 2) + 0.0:.2f} kN"

        if eje == "V":
            ini, fin = (x0, y0), (x0, y0 + signo * largo)
            _flecha(ax, ini, fin, AZUL, estilo="--" if valores is None else "-")
            ax.text(fin[0], fin[1] + signo * 0.02 * ref, etiqueta, color=AZUL, fontsize=10,
                    ha="center", va="bottom" if signo > 0 else "top")
        else:
            ini, fin = (x0, y0 + desplaz_h), (x0 + signo * largo, y0 + desplaz_h)
            _flecha(ax, ini, fin, AZUL, estilo="--" if valores is None else "-")
            ax.text(fin[0] + signo * 0.02 * ref, fin[1], etiqueta, color=AZUL, fontsize=10,
                    ha="left" if signo > 0 else "right", va="center")
        pts += [ini, fin]

    # Cotas
    ymin = min(p[1] for p in pts)
    yd = ymin - 0.10 * ref
    _cota(ax, 0, L, yd, f"L = {L:g} m")
    a = modelo["a"]
    if 0 < a < L:
        _cota(ax, 0, a, yd - 0.12 * ref, f"a = {a:g} m")
    pts += [(0, yd - 0.2 * ref), (L, yd)]

    xs_all, ys_all = [p[0] for p in pts], [p[1] for p in pts]
    mx = 0.12 * ref
    ax.set_xlim(min(xs_all) - mx, max(xs_all) + mx * 2.2)
    ax.set_ylim(min(ys_all) - mx * 0.5, max(ys_all) + mx * 1.6)
    ax.set_aspect("equal")
    ax.axis("off")
    if titulo:
        ax.set_title(titulo, fontsize=11)
    fig.tight_layout()
    return fig


def dibujar_diagramas_viga(modelo, sol):
    """Diagramas de fuerza cortante V(x) y momento flector M(x) de la viga."""
    L, a, Py = modelo["L"], modelo["a"], modelo["Py"]
    Ay = sol[modelo["idx_Ay"]]

    xv = [0, a, a, L]
    V = [Ay, Ay, Ay - Py, Ay - Py]
    xm = [0, a, L]
    M = [0.0, Ay * a, Ay * L - Py * (L - a)]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.5, 5.2), sharex=True)
    ax1.plot(xv, V, color=AZUL, lw=2)
    ax1.fill_between(xv, 0, V, color=AZUL, alpha=0.2)
    ax1.axhline(0, color="black", lw=1)
    vmax_abs = max(abs(v) for v in V) or 1.0
    ax1.set_ylim(min(min(V), 0) - 0.3 * vmax_abs, max(max(V), 0) + 0.3 * vmax_abs)
    ax1.set_ylabel("V (kN)")
    ax1.set_title("Fuerza cortante")
    ax1.grid(alpha=0.3)
    if a > 0:
        ax1.annotate(f"{Ay:.2f}", (a / 2, Ay), textcoords="offset points", xytext=(0, 6), ha="center")
    if a < L:
        ax1.annotate(f"{Ay - Py:.2f}", ((a + L) / 2, Ay - Py), textcoords="offset points",
                     xytext=(0, -14), ha="center")

    ax2.plot(xm, M, color=ROJO, lw=2)
    ax2.fill_between(xm, 0, M, color=ROJO, alpha=0.2)
    ax2.axhline(0, color="black", lw=1)
    ax2.set_ylabel("M (kN·m)")
    ax2.set_xlabel("x (m)")
    ax2.set_title("Momento flector (positivo = tracción en la fibra inferior)")
    ax2.grid(alpha=0.3)
    ax2.annotate(f"M máx = {Ay * a:.2f} kN·m", (a, Ay * a), textcoords="offset points",
                 xytext=(0, 8), ha="center")
    ax2.set_ylim(top=max(M) * 1.25 if max(M) > 0 else 1)
    fig.tight_layout()
    return fig