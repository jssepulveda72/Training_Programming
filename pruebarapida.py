import streamlit as st
import pandas as pd
import pymysql
import numpy as np
import io

buffer = io.BytesIO()
uploaded_file = st.file_uploader("Sube tu archivo")

if uploaded_file is not None:

    dataframe = pd.read_excel(uploaded_file)

    bd = dataframe
    n_items = int(bd.max().max())

    new_bd = {i : [bd[col].value_counts(normalize=True).round(2).loc[i] 
               if i in bd[col].value_counts(normalize=True).round(2).index
               else 0
               for col in bd.columns
              ]
                for i in range(n_items)}

    new_bd = pd.DataFrame(new_bd)
    new_bd["Item"] = bd.columns
    new_bd = new_bd.iloc[:,[-1,0,1,2,3]]
    new_bd["Promedio"] = [round(bd[col].mean(),2) for col in bd.columns]
    new_bd["Desviacion estandar"] = [round(bd[col].std(ddof=1),2) for col in bd.columns]
    new_bd["Media"] = [bd[col].median() for col in bd.columns]

    st.dataframe(new_bd)

    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        new_bd.to_excel(writer)
        writer.save()

        st.download_button(
            label = "Descargar",
            data=buffer,
            file_name = "new_bd.xlsx",
            mime="application/vnd.ms-excel"
        )





# data =st.data_editor(planeador,
#                      column_config = {
#                          "dia" : st.column_config.SelectboxColumn(
#                              "dia", 
#                              options = dias
#                          ),
#                          "bloque" : st.column_config.SelectboxColumn(
#                              "Super serie",
#                              options = [1,2,3,4,5,6]
#                          ),
#                          "patron de movimiento" : st.column_config.SelectboxColumn(
#                              "patron/musculo",
#                              options= Patronesdemovimiento
#                          ),
#                          "ejercicio" : st.column_config.SelectboxColumn(
#                              "ejercicio",
#                              options = ejercicios.loc[ejercicios[""],]
#                          ),
#                          "series" : st.column_config.NumberColumn(
#                              "series"
#                          ),
#                          "repeticiones" : st.column_config.NumberColumn(
#                              "repeticiones"
#                          ),
#                          "unidad" : st.column_config.SelectboxColumn(
#                              "unidad", 
#                              options = ["repeticiones","segundos"]
#                          ),
#                          "peso extra" : st.column_config.NumberColumn(
#                              "peso del ejercicio"
#                          ),
#                      }
                     
                     
                     
                     
#                      , num_rows="dynamic")

