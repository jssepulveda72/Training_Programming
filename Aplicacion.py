import pandas as pd
import numpy as np
import dataframe_image as dfi

#Lectura de bases de datos
Ejercicios = pd.read_excel("Ejercicios.xlsx")
Planeacion = pd.read_excel("Planeacion.xlsx")
RutinasCiclos = pd.DataFrame()
Patronesdemovimiento = ["One Arm Handstand", "Straight Arm Strenght", 
                        "Bent Arm Strenght", "Handstand", "Pierna",
                        "Mobility"]

VolumenPorMusculoMIM = [[224,224,168,252,280,168,112,168,224],
                        [392,420,280,420,448,224,224,280,336],
                        [560,616,392,588,616,392,336,448,504]]

def Sobrecargaprogresiva():
    pass

def Dificultad(RepsMax,Unidad):
    if Unidad == "segundos":
        if RepsMax >= 60:
            return 1
        elif RepsMax in range(45,60):
            return 2
        elif RepsMax in range(30,45):
            return 3
        elif RepsMax in range(15,30):
            return 4
        elif RepsMax in range(1,15):
            return 5
        
    if Unidad == "repeticiones":
        if RepsMax >= 20:
            return 1
        elif RepsMax in range(15,20):
            return 2
        elif RepsMax in range(10,15):
            return 3
        elif RepsMax in range(5,10):
            return 4
        elif RepsMax in range(1,5):
            return 5

def Series(Ejercicio,PatrondeMovimiento,dia):
    
    if "Handstand" in PatrondeMovimiento or "Mobility" in PatrondeMovimiento:
        return 2
    else:
        if dia in ["Miercoles","Martes"]:
            return 1
        else:
            return 2
    

def Escritor(Glosario,series):
    if Glosario.loc["Extra"] == 0:
        Escrito = """{} 
    {}X{}\n""".format(Glosario.loc["Ejercicio"],
                  series,
                  Glosario.loc["Repeticiones maximas"])
    
    else:
        Escrito = """{} + {} Kg 
    {}X{}\n""".format(Glosario.loc["Ejercicio"],Glosario.loc["Extra"],
                  series,
                  Glosario.loc["Repeticiones maximas"])
    
    return Escrito
    
    
    
def VolumenEjercicio(Ejercicio,Repeticiones,Unidad,Palanca):
    dificultad = Dificultad(Repeticiones,Unidad)
    repeticionesreales = dificultad * Repeticiones
    
    if Unidad == "segundos":
        
        return (1/Palanca)*repeticionesreales/3
    
    elif Unidad == "repeticiones":
        
        return 1.4*repeticionesreales


def SumadeVolumen(VolumenEjercicio,patrondemovimiento,intencion):
    if patrondemovimiento == "One Arm Handstand":
        
        VolumenPorMusculo["Deltoide"] += 0.2*VolumenEjercicio
        VolumenPorMusculo["Escapula"] += 0.2*VolumenEjercicio
        
    elif patrondemovimiento in ["Mobility","Handstand"]:
        
        VolumenPorMusculo["Deltoide"] += 0.1*VolumenEjercicio
        VolumenPorMusculo["Escapula"] += 0.1*VolumenEjercicio
        
    elif patrondemovimiento in ["Pierna"]:
        
        VolumenPorMusculo["Gluteos"] += 1*VolumenEjercicio
        VolumenPorMusculo["Isquios"] += 1*VolumenEjercicio
        VolumenPorMusculo["Cuadriceps"] += 1*VolumenEjercicio
        
    elif patrondemovimiento == "Straight Arm Strenght":
        
        if intencion  == "Full press":
            VolumenPorMusculo["Deltoide"] += 0.2*VolumenEjercicio
            VolumenPorMusculo["Triceps"] += 0.1*VolumenEjercicio
            VolumenPorMusculo["Escapula"] += 0.6*VolumenEjercicio
        
        elif intencion == "Swing Up":
            VolumenPorMusculo["Deltoide"] += 0.4*VolumenEjercicio
            VolumenPorMusculo["Triceps"] += 0.2*VolumenEjercicio
            VolumenPorMusculo["Escapula"] += 0.8*VolumenEjercicio
            
        elif intencion == "Plancha":
            VolumenPorMusculo["Pectoral"] += 0.3*VolumenEjercicio
            VolumenPorMusculo["Triceps"] += 0.4*VolumenEjercicio
            VolumenPorMusculo["Escapula"] += 1*VolumenEjercicio
            VolumenPorMusculo["Deltoide"] += 0.8*VolumenEjercicio
            
        elif intencion == "Front Lever":
            VolumenPorMusculo["Espalda"] += 1*VolumenEjercicio
            
    elif patrondemovimiento == "Bent Arm Strenght":
        
        if intencion == "Handstand Push Up":
            VolumenPorMusculo["Deltoide"] += 1*VolumenEjercicio
            VolumenPorMusculo["Triceps"] += 1*VolumenEjercicio
            VolumenPorMusculo["Escapula"] += 0.6*VolumenEjercicio
            
        elif intencion == "Empuje Vertical":
            VolumenPorMusculo["Deltoide"] += 1*VolumenEjercicio
            VolumenPorMusculo["Triceps"] += 1*VolumenEjercicio
            VolumenPorMusculo["Escapula"] += 0.4*VolumenEjercicio
            
        elif intencion == "Empuje Horizontal":
            VolumenPorMusculo["Pectoral"] += 1*VolumenEjercicio
            VolumenPorMusculo["Triceps"] += 0.6*VolumenEjercicio
            VolumenPorMusculo["Escapula"] += 0.5*VolumenEjercicio
            VolumenPorMusculo["Deltoide"] += 0.6*VolumenEjercicio
            
        elif intencion == "Tiron Horizontal":
            VolumenPorMusculo["Espalda"] += 1*VolumenEjercicio
            VolumenPorMusculo["Biceps"] += 0.5*VolumenEjercicio
            
        elif intencion == "Tiron Vertical":
            VolumenPorMusculo["Espalda"] += 1*VolumenEjercicio
            VolumenPorMusculo["Biceps"] += 0.8*VolumenEjercicio
            
        elif intencion == "Biceps":
            VolumenPorMusculo["Biceps"] += 1*VolumenEjercicio

        

Semana = 1


for dia in Planeacion.columns:      #Desarrollar la rutina dia por dia

    if "Lunes" in dia:
        VolumenPorMusculo = {"Pectoral": 0,
        "Deltoide": 0,
        "Triceps": 0,
        "Escapula": 0,
        "Espalda": 0,
        "Biceps": 0,
        "Gluteos": 0,
        "Isquios": 0,
        "Cuadriceps": 0,
        }
        
    
        
    
    Entrenamiento = Planeacion[dia] 
    PatrondeMovimiento = Entrenamiento[0] #Patron de movimiento a trabajar durante el dia
    EjerciciosPosibles = Ejercicios[Ejercicios["Patron de movimiento"].isin([PatrondeMovimiento])] 
    ListadeEjercicios = []
    Indicerepetido=[]
    Intencionanterior = ""
    for intencion in Entrenamiento[1:]: #Recorrer cada intencion y seleccionar ejercicio por intencion
        if isinstance(intencion, str):
            intencion = intencion.strip()
        if intencion in Patronesdemovimiento: #En caso de que haya mas de un patron de movimiento durante el dia
            EjerciciosPosibles = Ejercicios[Ejercicios["Patron de movimiento"].isin([intencion])]
            PatrondeMovimiento = intencion
            continue
        
        if pd.isna(intencion): #Solucion de errores en caso de que existan celdas vacias
            continue
        
        if intencion == ".":
            
            Ejercicio = "NA"            
        
            ListadeEjercicios.append(Ejercicio)
            
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
        
        VE = VolumenEjercicio(Ejercicio.loc["Ejercicio"],
                              Ejercicio.loc["Repeticiones maximas"], 
                              Ejercicio.loc["Unidad"], 
                              Ejercicio.loc["Palanca"])*Series(Ejercicio.loc["Ejercicio"], 
                                                               PatrondeMovimiento, 
                                                               dia)
        
        
        SumadeVolumen(VE, PatrondeMovimiento, intencion)
        
        
        
        EjercicioStr = Escritor(Ejercicio,
                                Series(Ejercicio.loc["Ejercicio"], 
                                       PatrondeMovimiento, 
                                       dia))
    
        ListadeEjercicios.append(EjercicioStr)
        
    RutinasCiclos[dia] = pd.Series(ListadeEjercicios) #Anotar ejercicios en la hoja
    
   
    if "Sabado" in dia:

        RutinasCiclos[f"Volumen Semana {Semana}"] = pd.Series(VolumenPorMusculo.keys())
        RutinasCiclos[f"Valor {Semana}"] = pd.Series(map(round,VolumenPorMusculo.values()))
        #RutinasCiclos[f"Minimo {Semana}"] = pd.Series(VolumenPorMusculoMIM[0])
        RutinasCiclos[f"Ideal {Semana}"] = pd.Series(VolumenPorMusculoMIM[1])
        RutinasCiclos[f"Maximo {Semana}"] = pd.Series(VolumenPorMusculoMIM[2])
        Semana += 1
    
#Agregar todas las rutinas al excel
Escritor = pd.ExcelWriter("Rutinas del ciclo.xlsx" , engine='xlsxwriter') 
RutinasCiclos.to_excel(Escritor,sheet_name="main")
worksheet = Escritor.sheets["main"]
#Cambios esteticos/formato a la hoja de excel
Formato = Escritor.book.add_format()
Formato.set_align('center')
Formato.set_align('vcenter')
Formato.set_font_name("arial")
Formato.set_text_wrap()
(max_row,max_col) = RutinasCiclos.shape
worksheet.set_column(1,max_col,25,Formato)
for i in range(1,max_row+1):    
    worksheet.set_row(i,60,Formato)
Escritor.close()


       
        
    
