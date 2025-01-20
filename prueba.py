import pandas as pd


Rutinas = pd.read_excel("Prueba.xlsx")
print(Rutinas[Rutinas["Dia"] == "Lunes"]["Ejercicio"])