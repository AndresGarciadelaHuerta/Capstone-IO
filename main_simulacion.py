import simulacion

estaciones = simulacion.poblar()
s = simulacion.Simulador()
s.estaciones = estaciones
s.prints = True
s.run()
print("Porcentaje de Satisfaccion de la Demanda: " + str(round(
    (s.demanda_satisfecha/(s.demanda_insatisfecha + s.demanda_satisfecha))*100,
    2)) + "%")