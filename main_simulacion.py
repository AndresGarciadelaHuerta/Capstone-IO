import numpy
import simulacion

a = True
while a:

    try:
        numero_simulaciones = int(
            input('Ingrese el número de repeticiones de la '
                  'simulacion que quiere realizar '
                  '(debe ser un número entero): '))
        a = False

    except ValueError:
        print('Por favor ingrese un número entero.')

# Leemos excel y poblamos
estaciones = simulacion.poblar()
s = simulacion.Simulador()
s.estaciones = estaciones
s.prints = False


lista_porcentajes = []
i = 0
while i < numero_simulaciones:

    print('\nCorriendo repetición {}.'.format(str(i + 1)))

    # Reseteamos
    s.tiempo_actual = 0
    s.cola = []
    s.contador_dias = 0
    s.demanda_insatisfecha = 0
    s.demanda_satisfecha = 0

    # Resetear cada estacion
    for estacion in s.estaciones.values():
        estacion.demanda_satisfecha = 0
        estacion.demanda_insatisfecha = 0

    # Corremos la simulación
    s.run()

    # Obtenemos las medidas de desempeño

    porcentaje_satisfaccion = round(
        (s.demanda_satisfecha/(s.demanda_insatisfecha +
                               s.demanda_satisfecha))*100, 2)
    lista_porcentajes.append(porcentaje_satisfaccion)

    estaciones_dda_satisfecha = [(e.demanda_satisfecha, e.number) for e in
                                 s.estaciones.values()]
    estaciones_dda_insatisfecha = [(e.demanda_insatisfecha, e.number) for e in
                                  s.estaciones.values()]

    estaciones_dda_insatisfecha.sort()
    estaciones_dda_satisfecha.sort()
    print('\nLas 3 estaciones con mayor cantidad de satisfaccion de demanda :')
    print(estaciones_dda_satisfecha[-3:])
    print('\nLas 3 estaciones con mayor cantidad de insatisfaccion de demanda :')
    print(estaciones_dda_insatisfecha[-3:])






    i += 1
    #print("Porcentaje de Satisfaccion de la Demanda: " + str(
     #   porcentaje_satisfaccion) + "%")


promedio_satisfaccion = sum(lista_porcentajes)/len(lista_porcentajes)
varianza = round((float(numpy.std(lista_porcentajes).item())**2), 4)
print(lista_porcentajes)
print('--------------------------------------------------------------')
print('Porcentaje Promedio de Satisfaccion de la Demanda: ' + str(
        promedio_satisfaccion) + "%")
print('Varianza de los Porcentajes de Satisfacción de la Demanda: ' + str(
    varianza))