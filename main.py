import simulacion
import time
from Problema_integrado import *
from scipy.stats import t
import numpy

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

# Poblamos
tiempo1 = time.time()
estaciones = read_json()
s = simulacion.Simulador()
s.estaciones = estaciones
s.prints = False


lista_porcentajes = []
i = 0
tiempo2 = time.time()
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

    # Corremos la simulación, los clusters y el ruteo
    s.run()
    clusters = opti_final(estaciones)
    # aca hacer los subtours para todos
    for grupo in clusters.values():
        #for elem in grupo:
            #print(elem)
        ruteo(grupo, s.estaciones)

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
    if s.prints:
        print('\nLas 3 estaciones con mayor cantidad de satisfaccion de demanda :')
        print(estaciones_dda_satisfecha[-3:])
        print('\nLas 3 estaciones con mayor cantidad de insatisfaccion de demanda :')
        print(estaciones_dda_insatisfecha[-3:])






    i += 1
    #print("Porcentaje de Satisfaccion de la Demanda: " + str(
     #   porcentaje_satisfaccion) + "%")

tiempo3 = time.time()
promedio_satisfaccion = sum(lista_porcentajes)/len(lista_porcentajes)
varianza = round((float(numpy.std(lista_porcentajes).item())**2), 4)

#Intervalo de confianza al 95%

studiante = t.interval(.95, numero_simulaciones - 1)
intervalo_bajo = promedio_satisfaccion + studiante[0] * sqrt(varianza) / sqrt(numero_simulaciones)
intervalo_alto = promedio_satisfaccion + studiante[1] * sqrt(varianza) / sqrt(numero_simulaciones)

#print(lista_porcentajes)
print('--------------------------------------------------------------')
print('Porcentaje Promedio de Satisfaccion de la Demanda: ' + str(
        promedio_satisfaccion) + "%")
print('Varianza de los Porcentajes de Satisfacción de la Demanda: ' + str(
    varianza))
print('Intervalo de confianza al 95% de satisfacción: {} <= X <= {}'.format(intervalo_bajo, intervalo_alto))
print('Tiempo en leer los datos: ' + str(round(tiempo2 - tiempo1, 2))
      + ' segundos.')
print('Tiempo en simular todas las repeticiones: ' + str(round(
    tiempo3 - tiempo2, 2)) + ' segundos.')

