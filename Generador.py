import pandas as pd
import numpy as np


Ejercicios = pd.read_excel("Ejercicios.xlsx")
Planeacion = pd.read_excel("Planeacion.xlsx")
RutinasCiclos = pd.DataFrame({"Dia":[],
                              "Ejercicio":[],
                              "Sets":[],
                              "Reps":[]})


Patronesdemovimiento = ["One Arm Handstand", "Straight Arm Strenght", 
                        "Bent Arm Strenght", "Handstand", "Pierna",
                        "Mobility"]

def Series(Ejercicio,PatrondeMovimiento,dia,intencion):
    
    if "Handstand" in PatrondeMovimiento or "Mobility" in PatrondeMovimiento:
        if intencion in ["Strenght","Endurance","Flag"]:
            return 2
        else:
            return 3
    else:
        if dia in ["Miercoles","Martes","Sabado"]:
            return 2
        else:
            return 3

Semana = "Handstand"


for dia in Planeacion.columns:      #Desarrollar la rutina dia por dia
    RutinaDia = pd.DataFrame()
    Entrenamiento = Planeacion[dia] 
    PatrondeMovimiento = Entrenamiento[0] #Patron de movimiento a trabajar durante el dia
    EjerciciosPosibles = Ejercicios[Ejercicios["Patron de movimiento"].isin([PatrondeMovimiento])] 
    ListadeEjercicios = []
    lista_de_series = []
    lista_de_repeticiones = []
    Indicerepetido=[]
    Intencionanterior = ""
    for intencion in Entrenamiento[1:]: #Recorrer cada intencion y seleccionar ejercicio por intencion
        if dia == "Lunes 2":
            Semana = "Strenght"

        if isinstance(intencion, str):
            intencion = intencion.strip()
        if intencion in Patronesdemovimiento: #En caso de que haya mas de un patron de movimiento durante el dia
            EjerciciosPosibles = Ejercicios[Ejercicios["Patron de movimiento"].isin([intencion])]
            PatrondeMovimiento = intencion
            continue
        
        if pd.isna(intencion): #Solucion de errores en caso de que existan celdas vacias
            continue
        
        if intencion == ".":
            continue
            Ejercicio = "NA"            
        
            ListadeEjercicios.append(Ejercicio)
            lista_de_repeticiones.append(0)
            lista_de_series.append(0)

            
            continue

        Selecciondeejercicios = EjerciciosPosibles[EjerciciosPosibles["Intencion"].isin([intencion])]
        IndiceAleatorio = np.random.randint(0,len(Selecciondeejercicios))
        
         
        
        if intencion != Intencionanterior: #Evitar que se repitan ejercicios durante el entrenamiento
            Indicerepetido = []
                    
        else:
            while IndiceAleatorio in Indicerepetido:
                IndiceAleatorio = np.random.randint(0,len(Selecciondeejercicios))
        
        Indicerepetido.append(IndiceAleatorio)        
        Ejercicio = Selecciondeejercicios.iloc[IndiceAleatorio]
        Intencionanterior = intencion
        ListadeEjercicios.append(Ejercicio["Ejercicio"])
        lista_de_repeticiones.append(Ejercicio["Repeticiones maximas"])
        lista_de_series.append(Series(Ejercicio["Ejercicio"],
                                      PatrondeMovimiento,
                                      dia,
                                      intencion))
    


    RutinaDia["Semana"] = pd.Series([Semana]*len(ListadeEjercicios))
    RutinaDia["Dia"] = pd.Series([dia.strip(" 2")]*len(ListadeEjercicios))
    RutinaDia["Ejercicio"] = pd.Series(ListadeEjercicios)
    RutinaDia["Sets"] = pd.Series(lista_de_series)
    RutinaDia["Reps"] = pd.Series(lista_de_repeticiones)

    
    RutinasCiclos = pd.concat([RutinasCiclos,RutinaDia])

RutinasCiclos["Sets"] = RutinasCiclos["Sets"].astype("int")
RutinasCiclos["Reps"] = RutinasCiclos["Reps"].astype("int")


RutinasCiclos.to_excel("Prueba.xlsx")