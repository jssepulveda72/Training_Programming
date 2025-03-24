import pandas as pd
import pymysql
import streamlit as st
import numpy as np


# Initialize connection.
def init_connection():
    config = st.secrets["tidb"]
    return pymysql.connect(
        host=config["host"],
        port=config["port"],
        user=config["username"],
        password=config["password"],
        database=config["database"],
        ssl_verify_cert=True,
        ssl_verify_identity=True,
        ssl_ca= config["ssl_ca"]
    ) 

def fetch_data(conn, query, cols=None):
    cursor = conn.cursor()
    cursor.execute(query)

    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=cols)
    return df

def update_date(conn, query, cols):
    pass


def create_plan(data,conn):
    df = data.loc[:, ["dia","bloque","ejercicio","series","repeticiones maximas","unidad"]]

    cur = conn.cursor()

    data = [tuple(row) for row in df.itertuples(index=False)]

    query_clean = 'DELETE FROM plan_semanal'
    cur.execute(query_clean)

    query = 'INSERT INTO plan_semanal (dia, bloque, ejercicio, series, repeticiones, unidad) VALUES (  %s,  %s,  %s,  %s, %s,  %s);'
    cur.executemany(query, data)

    # commit the changes
    conn.commit()
    cur.close()
    conn.close()


def excersice_printing_desktop(dia, conn):
    
    st.header(dia)

    query = f'SELECT bloque, ejercicio, series, repeticiones, unidad FROM plan_semanal WHERE dia = \'{dia}\' '
    columnas = ["bloque","ejercicio","series","repeticiones","unidad"]

    if "rutina" not in st.session_state:

        st.session_state.rutina = fetch_data(conn,query,columnas)

    if st.session_state.rutina.empty:
        st.title("Regalate 10.000 pasos.")

    else:

        numbers = dict()

        for bloque in st.session_state.rutina["bloque"].unique():
            
            ejer_per_block = st.session_state.rutina.loc[st.session_state.rutina["bloque"] == bloque].reset_index()
            n_ejer_per_block = len(ejer_per_block)

            series = ejer_per_block["series"].unique()[0]

            for serie in range(series):

                with st.container():
                    cols = st.columns(n_ejer_per_block+1,vertical_alignment="center")

                    if serie == 0:
                        
                        cols[0].subheader("Super set")
                        for i in range(n_ejer_per_block):

                            ejercicio = ejer_per_block["ejercicio"][i]
                            cols[i+1].subheader(ejercicio.capitalize())

                            continue

                    cols[0].checkbox(f"Serie {serie+1}", 
                                key = f"Serie {bloque}{serie+1}")


                    for i in range(n_ejer_per_block):
                        
                        
                        ejercicio = ejer_per_block["ejercicio"][i]
                        repeticiones = ejer_per_block["repeticiones"][i]
                        unidad = ejer_per_block["unidad"][i]
                    
                        numbers[f"{ejercicio}"] = numbers.get(f"{ejercicio}",[]) + [cols[i+1].number_input(f"{unidad}",
                                                                        key=f"{ejercicio}{i}{serie}",
                                                                        value=repeticiones)]

        if st.button("Terminar", key=f"button{dia}"):
            

            df = pd.DataFrame(dict([(key, pd.Series(value)) for key, value in numbers.items()]))
            df = df.mean(axis=0,skipna=True)
        
            
            st.dataframe(df)
            st.snow()    

def on_change_sb(conn):

    st.session_state.hoy = st.session_state.new_day
    query = f'SELECT bloque, ejercicio, series, repeticiones, unidad FROM plan_semanal WHERE dia = \'{st.session_state.hoy}\' '
    columnas = ["bloque","ejercicio","series","repeticiones","unidad"]

    st.session_state.rutina = fetch_data(conn,query,columnas)

    


def excersice_printing_mobile(dia,conn):

    if "counter" not in st.session_state:

        st.session_state.counter = 1

    st.header(dia)

    query = f'SELECT bloque, ejercicio, series, repeticiones, unidad FROM plan_semanal WHERE dia = \'{dia}\' '
    columnas = ["bloque","ejercicio","series","repeticiones","unidad"]

    if "rutina" not in st.session_state:
        
        st.session_state.rutina = fetch_data(conn,query,columnas)

    if st.session_state.rutina.empty:
        st.title("Regalate 10.000 pasos.")

    else:


        numbers = dict()

        

        n_bloques = len(st.session_state.rutina["bloque"].unique())

        ejer_per_block = st.session_state.rutina.loc[st.session_state.rutina["bloque"] == st.session_state.counter].reset_index()

        n_ejer_per_block = len(ejer_per_block)

        series = ejer_per_block["series"].unique()[0]

        placeholder = st.empty()


        with placeholder.container():

            st.header(f"Super set {st.session_state.counter}")

            for i in range(n_ejer_per_block):

                ejercicio = ejer_per_block["ejercicio"][i]
                repeticiones = ejer_per_block["repeticiones"][i]
                unidad = ejer_per_block["unidad"][i]

                st.subheader(ejercicio)
                for serie in range(series):


                    st.checkbox(f"Serie {serie+1}", 
                                        key = f"Serie {i}{serie+1}")

                    numbers[f"{ejercicio}"] = numbers.get(f"{ejercicio}",[]) + [st.number_input(f"{unidad}",
                                                                                key=f"{ejercicio}{i}{serie}",
                                                                                value=repeticiones)]

        if st.session_state.counter < n_bloques:

            if st.button("continuar"):
                st.session_state.counter += 1

        else:

            if st.button("Terminar", key=f"button{dia}"):
                        
                st.session_state.counter = 1
                df = pd.DataFrame(dict([(key, pd.Series(value)) for key, value in numbers.items()]))
                df = df.mean(axis=0,skipna=True)
                    
                        
                st.dataframe(df)
                st.balloons()



def planner_display(conn):

    query = 'SELECT * FROM ejercicios'
    columnas = ["ejercicio",
                "repeticiones maximas",
                "unidad",
                "extra",
                "unidad extra",
                "patron de movimiento",
                "disciplina",
                "intencion"]

    if "ejercicios" not in st.session_state:

        st.session_state.ejercicios = fetch_data(conn,query,columnas)


    if "plan_semanal" not in st.session_state:

        st.session_state.plan_semanal = pd.DataFrame({})

    def table_change():

        st.session_state.plan_semanal = edited_plan

    cols = st.columns(5)
    
    disciplinas = st.session_state.ejercicios["disciplina"].unique()

    with cols[0]:
        disciplina = st.selectbox(
            "Disciplina",
            disciplinas
        )


    Patronesdemovimiento = st.session_state.ejercicios.loc[st.session_state.ejercicios["disciplina"] == disciplina,
                                                           "patron de movimiento"].unique()

    with cols[1]:
        patron_de_movimiento = st.selectbox(
            "Patron de movimiento",
            Patronesdemovimiento
        )



    dias = ["Lunes","Martes","Miercoles","Jueves","Viernes","Sabado","Domingo"]
   
    with cols[2]:
        dia_selector = st.selectbox(
            "Dia",
            dias
        )

    with cols[3]:
         series_selector = st.number_input(
             "Series",
             value=3,
             step=1
         )

    with cols[4]:
         bloque_selector = st.number_input(
             "Super-set",
             value=1,
             step=1
         )

    df = st.session_state.ejercicios.loc[(st.session_state.ejercicios["patron de movimiento"] == patron_de_movimiento)
                                         &
                                         (st.session_state.ejercicios["disciplina"] == disciplina)]


    result = st.dataframe(df[["ejercicio","intencion"]]
                ,hide_index=True,
                use_container_width=True,
                on_select="rerun",
                selection_mode="single-row")



    aux_df =  df.iloc[result.selection["rows"]][["ejercicio",
                                                    "repeticiones maximas",
                                                    "unidad",
                                                    ]]

    aux_df["dia"] = [dia_selector]
    aux_df["bloque"] = [bloque_selector]
    aux_df["series"] = [series_selector]

    aux_df = aux_df.iloc[:,[-3,-2,0,-1,1,2]]

    if st.button("Añadir"):

        st.session_state.plan_semanal = pd.concat([st.session_state.plan_semanal,
                                                aux_df],ignore_index=True)

    edited_plan = st.data_editor(st.session_state.plan_semanal,
                                column_config ={
                                    "dia" : st.column_config.SelectboxColumn(
                                        "dia",
                                        options = dias,
                                        required = True
                                    ),
                                    "bloque" : st.column_config.NumberColumn(
                                        "bloque",
                                        step =1
                                    ),
                                    "series" : st.column_config.NumberColumn(
                                        "series",
                                        step = 1 
                                    ),
                                    "repeticiones maximas" : st.column_config.NumberColumn(
                                        "repeticiones maximas",
                                    )
                                },
                                #on_change = table_change(),
                                use_container_width = True,
                                hide_index = True,
                                disabled = ["ejercicio", "unidad"])
            
    contra = st.text_input("Password")

    if st.button("Terminar"):
        
        if contra == st.secrets["password"]["pass"]:
            st.session_state.plan_semanal = edited_plan
            create_plan(st.session_state.plan_semanal,conn)
            st.success("Plan actualizado!!")
            st.snow()
        else:
            st.balloons()



def history_display():


    x = np.linspace(0.1,10,100)

    y = [np.sin,np.cos,np.tan,np.log,np.exp]

    data = pd.DataFrame({
        "funciones" : ["Sin","Cos","Tan","Ln","Exp"],
        "f(x)" : [y[i](x) for i in range(len(y))]
    })

    


    frame = st.dataframe(data,
                    column_config = {
                        "f(x)" : st.column_config.LineChartColumn(
                        "f(x)",
                            width = "large",
                        )
                    },
                    hide_index=True,
                    on_select="rerun",
                    selection_mode="single-row",
                    use_container_width=True)


    @st.dialog("History")
    def plot_line():
        indice = frame.selection["rows"]
        excersice = data.iloc[indice]["funciones"].values[0]    
        st.title(f"{excersice}")    
        y = data.iloc[indice]["f(x)"].explode()
        aux_df = pd.DataFrame({
            "x" : np.arange(len(y)),
            "y" : y
        })
            
        st.line_chart(data=aux_df,  
                        x = "x",
                        y = "y" 
                    )
        


    if frame.selection["rows"]:

        plot_line()
