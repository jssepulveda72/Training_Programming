import streamlit as st
import pandas as pd


Rutinas = pd.read_excel("Prueba.xlsx")

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

def excersice_printing():
        st.header(select_day)
        rutina = Rutinas[Rutinas["Semana"] == select_week]
        rutina = rutina[rutina["Dia"] == select_day].set_index("Ejercicio")
        for excersice in rutina.index:
                st.subheader(excersice)
                for set in range(rutina.loc[excersice,"Sets"]):
                        with st.container():
                            exer,reps,effort,col1,col2,col3 = st.columns([0.5,0.5,0.5,1,1,1],vertical_alignment="center")
                            exer.checkbox(f"Set {set+1}",key=f"echeck {excersice}{set}")
                            reps.number_input("Reps",min_value=0,key=f"ejercicio {excersice}{set}",
                                              value=rutina.loc[excersice,"Reps"])
                            effort.number_input("Esfuerzo",min_value=0,max_value=10,key=f"eejericio{excersice}{set}")


excersice_printing()












""" # Input fields for reps, weight, and perceived effort
reps = st.number_input("Reps", min_value=0)
weight = st.number_input("Weight (kg)", min_value=0.0, step=0.5)
effort = st.slider("Perceived Effort (1-10)", min_value=1, max_value=10)

# Button to submit the data
if st.button("Save Entry"):
    # Create a dataframe to store the data
    try:
        # Attempt to load existing data from session state
        training_data = st.session_state.training_data
    except AttributeError:
        # If it doesn't exist, initialize an empty dataframe
        training_data = pd.DataFrame(columns=["Date", "Reps", "Weight", "Effort"])

    # Append the new entry to the dataframe
    new_entry = {
        "Date": selected_date,
        "Reps": reps,
        "Weight": weight,
        "Effort": effort,
    }
    training_data = training_data.append(new_entry, ignore_index=True)

    # Save the updated dataframe back to session state
    st.session_state.training_data = training_data

    # Provide feedback to the user
    st.success("Entry saved!")

# Display the training data in a table if it exists
if 'training_data' in st.session_state:
    st.subheader("Training Data")
    st.dataframe(st.session_state.training_data) """




""" st.header(select_week)
with exer:
    st.header(select_day)
    for i in ejercicios[select_day]:
        st.markdown(i)



with reps:
    st.header("")
    for i in range(len(ejercicios[select_day])):
       st.number_input("Reps", min_value=0, key=f"ejercicio {i}")

with effort:
   st.header("")
   for i in range(len(ejercicios[select_day])):
       st.slider("Perceived Effort (1-10)", min_value=1, max_value=10, key=f"eejercicio {i}")  """ 