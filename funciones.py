import streamlit as st
import pandas as pd


Rutinas = pd.read_csv("Prueba.csv")

if "Rutinas" not in st.session_state:
       st.session_state.Rutinas = Rutinas


st.set_page_config(layout="wide")

# Title of the app
st.title("Training App")

# Create a date input for selecting the training day
select_week = st.sidebar.selectbox("Semana",["Handstand",
                                             "Strenght"])


select_day = st.sidebar.selectbox("Dia",["Lunes",
                                    "Martes",
                                    "Miercoles",
                                    "Jueves",
                                    "Viernes",
                                    "Sabado"])




st.header(select_week)

def excersice_printing(Rutinas):
        st.header(select_day)
        rutina = Rutinas[Rutinas["Semana"] == select_week]
        rutina = rutina[rutina["Dia"] == select_day].set_index("Ejercicio")
        for excersice in rutina.index:
                st.subheader(excersice)
                try:
                       prueba = range(rutina.loc[excersice,"Sets"])
                except:
                       print(rutina.loc[excersice,"Sets"])
                       continue
                
                for set in range(rutina.loc[excersice,"Sets"]):
                        with st.container():
                            exer,reps = st.columns([0.5,0.5],vertical_alignment="center")
                            exer.checkbox(f"Set {set+1}",key=f"echeck {excersice}{set}")
                            reps.number_input("Reps",min_value=0,key=f"ejercicio {excersice}{set}",
                                              value=rutina.loc[excersice,"Reps"])
                            #effort.number_input("Esfuerzo",min_value=0,max_value=10,key=f"eejericio{excersice}{set}")


day_display, daframe_display = st.tabs(["Day","Table"])

with day_display:
    excersice_printing(st.session_state.Rutinas)

with daframe_display:
    day_table = st.session_state.Rutinas
    day_table = day_table.loc[(day_table["Dia"] == select_day) & (day_table["Semana"] == select_week),
                               "Ejercicio":"Reps"]
    actual_table = st.data_editor(day_table,use_container_width = True)
    if st.button("Guardar"):
          st.session_state.Rutinas.loc[(st.session_state.Rutinas["Dia"] == select_day) 
                                       & (st.session_state.Rutinas["Semana"] == select_week),
                               "Ejercicio":"Reps"] = actual_table