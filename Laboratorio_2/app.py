"""Aplicación web: métodos numéricos aplicados a la ingeniería civil (usa las funciones de ModLab2).

Ejecutar con:  streamlit run app.py
"""

import streamlit as st

import pestana_lineales
import pestana_no_lineales

st.set_page_config(page_title="Métodos numéricos en ingeniería civil", layout="wide")

st.title("Métodos numéricos aplicados a la ingeniería civil")
st.caption("Laboratorio 2 · Funciones del módulo ModLab2")

tab_lineales, tab_no_lineales = st.tabs(["Sistemas lineales", "Sistemas no lineales"])

with tab_lineales:
    pestana_lineales.mostrar()

with tab_no_lineales:
    pestanas_no_lineales.mostrar()
