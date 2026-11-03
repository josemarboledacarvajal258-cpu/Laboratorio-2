"""Aplicación web: métodos numéricos aplicados a la ingeniería civil (usa las funciones de ModLab2).

Ejecutar con:  streamlit run app.py
"""

import streamlit as st

import pestana_lineales
import pestana_no_lineales
import pestana_lagrange
import pestana_newton_spline
from ModLab3 import bloque_datos_compartidos

st.set_page_config(page_title="Métodos numéricos en ingeniería civil", layout="wide")

st.title("Métodos numéricos aplicados a la ingeniería civil")
st.caption("Laboratorio 2 · Sistemas de ecuaciones e interpolación")

ctx = bloque_datos_compartidos()   # barra lateral compartida por las pestañas 3 y 4

tab1, tab2, tab3, tab4 = st.tabs(
    ["Sistemas lineales", "Sistemas no lineales", "Lagrange", "Newton + Spline"])

with tab1:
    pestana_lineales.mostrar()
with tab2:
    pestana_no_lineales.mostrar()
with tab3:
    pestana_lagrange.mostrar(ctx)
with tab4:
    pestana_newton_spline.mostrar(ctx)

    