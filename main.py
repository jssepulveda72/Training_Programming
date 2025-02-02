import streamlit as st
import pandas as pd
from datetime import datetime
from func import *

st.set_page_config(layout="wide")

conn = init_connection()

st.title("Aplicacion de entrenamiento")

hoy_index = datetime.today().weekday()
dias = ["Lunes","Martes","Miercoles","Jueves","Viernes","Sabado","Domingo"]

if "hoy" not in st.session_state:
    st.session_state.hoy = dias[hoy_index]



train_display, planning_section, excersice_glosary = st.tabs(["Entrenamiento",
                                                               "Planeador semanal",
                                                               "Glosario de ejercicios"])

def on_change_sb():
    st.session_state.hoy = st.session_state.new_day

with train_display:
    st.selectbox(
        "Dia", 
        options=dias,
        key = 'new_day',
        on_change = on_change_sb,
        placeholder="Elegir dia",
        index = None
    )

    excersice_printing(st.session_state.hoy,conn)
    



with planning_section:
    planner_display(conn)



with excersice_glosary:
    history_display()

