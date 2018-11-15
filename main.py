import simulacion
import time
from Problema_integrado import *
from scipy.stats import t
import numpy

lista = []
contador_menores = 0


def distribucion_inicial_estacion(estacion, estaciones):
    estacion.probas(estaciones)
    pond = .8
    llegan_manana = sum(estacion.probs['manana'].values()) * pond
    llegan_mediodia = sum(estacion.probs['mediodia'].values()) * pond
    llegan_tarde = sum(estacion.probs['tarde'].values()) * pond
    llegan_noche = sum(estacion.probs['noche'].values()) * pond
    salen_manana = 3 * estacion.tasa_manana * pond
    salen_mediodia = 3 * estacion.tasa_mediodia * pond
    salen_tarde = 3 * estacion.tasa_tarde * pond
    salen_noche = 3 * estacion.tasa_noche * pond
    inicial = 0
    manana = llegan_manana - salen_manana
    mediodia = llegan_mediodia - salen_mediodia
    tarde = llegan_tarde - salen_tarde
    noche = llegan_noche - salen_noche
    suma_ida = manana + mediodia
    suma_vuelta = tarde + noche
    suma = manana + mediodia + tarde + noche
    if suma_ida > 0 and suma_vuelta > 0:
        inicial = 11
    elif suma_ida > 0 and suma_vuelta < 0:
        inicial = int(-suma_ida - suma_vuelta + 10)
    elif suma_ida < 0 and suma_vuelta > 0:
        inicial = int(-suma_ida) + 11
    elif suma_ida < 0 and suma_vuelta < 0:
        inicial = int(-suma_ida - suma_vuelta) + 15

    return max(5, inicial)


if __name__ == '__main__':

    intervalo_bajo = 0

    # Poblamos
    estaciones = read_json()

    for est in estaciones.values():
        est.probas(estaciones)

    # Hacemos listas con las estaciones que reciben y pierden bicis
    pierden = [i.num for i in estaciones.values() if i.flujo_total < 0]
    ganan = [i.num for i in estaciones.values() if i.flujo_total > 0]

    # Distribucion que cumple con el 80% por si sola
    lista_2 = [2, 20, 5, 10, 33, 31, 7, 14, 19, 7, 3, 5, 19, 5, 5, 33, 6, 6, 25, 20, 29, 4, 30, 4, 39, 5, 5, 25, 11, 16,
               5, 36, 6, 2, 2, 5, 35, 20, 6, 27, 34, 16, 5, 3, 3, 5, 6, 6, 2, 18, 13, 5, 0, 18, 36, 16, 21, 2, 52, 10,
               2, 36, 20, 35, 17, 5, 5, 2, 6, 3, 19, 15, 9, 47, 2, 6, 27, 57, 2, 15, 6, 3, 5, 9, 21, 10, 32, 21, 1, 24,
               34, 60]

    # Distribucion que no cumple sola el 80 %
    # lista_2 = [0, 11, 0, 1, 24, 22, 0, 5, 10, 0, 0, 0, 10, 0, 0, 24, 0, 0, 16, 11, 20, 0, 21, 0, 30, 0, 0, 16, 2, 7, 0,
    #            27, 0, 0, 0, 0, 26, 11, 0, 18, 25, 7, 0, 0, 0, 0, 0, 0, 0, 9, 4, 0, 0, 9, 27, 7, 12, 0, 43, 1, 0, 27, 11,
    #            26, 8, 0, 0, 0, 0, 0, 10, 6, 0, 38, 0, 0, 18, 48, 0, 6, 0, 0, 0, 0, 12, 1, 23, 12, 0, 15, 25, 51]


    with open('dist_inicial_minima.csv', 'w') as file:
        file.write('Estacion, Minimo\n')
        for est in estaciones.values():
            file.write('{},{}\n'.format(est.num, lista_2[est.num - 1]))

    s = simulacion.Simulador(lista_2)
    s.estaciones = estaciones
    s.definir_distribucion_manana()

    print(sum(lista_2))
    s.lista_aux = lista_2

    prom_anterior = 0

    intervalo_bajo = 100

    # Esto es para buscar base factible
    for j in range(3):
        print(s.lista_aux)
        print(sum(s.lista_aux))
        objetivo = []
        tiempo1 = time.time()
        s.prints = False
        lista_porcentajes = []
        i = 0
        numero_simulaciones = 0
        intervalo_alto = 999999999
        intervalo_bajo = 0
        tiempo2 = time.time()

        demandas_por_estacion = {
            i: {j: 0 for j in ('satisfechos', 'insatisfechos', 'manana', 'mediodia', 'tarde', 'noche')} for i in
            range(1, 93)}

        while (intervalo_alto - intervalo_bajo) > 2 or numero_simulaciones < 5:
            numero_simulaciones += 1

            print('\nCorriendo repetición {}.'.format(str(numero_simulaciones)))
            print(intervalo_alto - intervalo_bajo, numero_simulaciones, '\n')
            print(intervalo_bajo, intervalo_alto)

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
            if 1:
                clusters = opti_final(estaciones)
                for grupo in clusters.values():
                    objetivo.append(ruteo(grupo, s.estaciones))

            # Obtenemos las medidas de desempeño

            porcentaje_satisfaccion = round(
                (s.demanda_satisfecha / (s.demanda_insatisfecha +
                                         s.demanda_satisfecha)) * 100, 2)
            lista_porcentajes.append(porcentaje_satisfaccion)

            # Reajuste por satisfaccion
            for estacion in s.estaciones.values():
                demandas_por_estacion[estacion.num]['satisfechos'] += estacion.demanda_satisfecha
                demandas_por_estacion[estacion.num]['insatisfechos'] += estacion.demanda_insatisfecha
                demandas_por_estacion[estacion.num]['manana'] += estacion.demanda_insatisfecha_manana
                demandas_por_estacion[estacion.num]['mediodia'] += estacion.demanda_insatisfecha_mediodia
                demandas_por_estacion[estacion.num]['tarde'] += estacion.demanda_insatisfecha_tarde
                demandas_por_estacion[estacion.num]['noche'] += estacion.demanda_insatisfecha_noche

            promedio_satisfaccion = sum(lista_porcentajes) / len(lista_porcentajes)
            varianza = round((float(numpy.std(lista_porcentajes).item()) ** 2), 4)

            # Intervalo de confianza al 95%

            studiante = t.interval(.95, numero_simulaciones - 1)
            intervalo_bajo = promedio_satisfaccion + studiante[0] * sqrt(varianza) / sqrt(numero_simulaciones)
            intervalo_alto = promedio_satisfaccion + studiante[1] * sqrt(varianza) / sqrt(numero_simulaciones)

        tiempo3 = time.time()
        promedio_satisfaccion = sum(lista_porcentajes) / len(lista_porcentajes)
        varianza = round((float(numpy.std(lista_porcentajes).item()) ** 2), 4)
        var_objetivo = round((float(numpy.std(objetivo).item()) ** 2), 4)

        # Intervalo de confianza al 95%

        studiante = t.interval(.95, numero_simulaciones - 1)
        intervalo_bajo = promedio_satisfaccion + studiante[0] * sqrt(varianza) / sqrt(numero_simulaciones)
        intervalo_alto = promedio_satisfaccion + studiante[1] * sqrt(varianza) / sqrt(numero_simulaciones)
        bajo_objetivo = sum(objetivo) / numero_simulaciones + studiante[0] * sqrt(var_objetivo) / sqrt(
            numero_simulaciones)
        alto_objetivo = sum(objetivo) / numero_simulaciones + studiante[1] * sqrt(var_objetivo) / sqrt(
            numero_simulaciones)

        # reajuste por satisfaccion
        demandas_estacion_ordenada = sorted(demandas_por_estacion,
                                            key=lambda x: (demandas_por_estacion[x]['satisfechos'] / (
                                                    demandas_por_estacion[x]['insatisfechos'] +
                                                    demandas_por_estacion[x]['satisfechos'])))

        if True:
            print('\nLas 5 estaciones con mayor cantidad de satisfaccion de demanda :')
            print(demandas_estacion_ordenada[:5])
            print('\nLas 5 estaciones con mayor cantidad de insatisfaccion de demanda :')
            print(demandas_estacion_ordenada[-5:])

        print('--------------------------------------------------------------')
        print('Porcentaje Promedio de Satisfaccion de la Demanda: ' + str(
            promedio_satisfaccion) + "%")
        print('Varianza de los Porcentajes de Satisfacción de la Demanda: ' + str(
            varianza))
        print('Intervalo de confianza al 95% de satisfacción: {} <= X <= {}'.format(intervalo_bajo, intervalo_alto))
        print('Funcion Objetivo: {}'.format(sum(objetivo) / numero_simulaciones))
        print('Intervalo al 95%: {} <= X <= {}'.format(bajo_objetivo, alto_objetivo))
        print('Tiempo en leer los datos: ' + str(round(tiempo2 - tiempo1, 2))
              + ' segundos.')
        print('Tiempo en simular todas las repeticiones: ' + str(round(
            tiempo3 - tiempo2, 2)) + ' segundos.')


        with open('satisfaccion.csv', 'w') as file:
            file.write('Estacion, Satisfaccion\n')
            for estacion in estaciones.values():
                sat = demandas_por_estacion[estacion.num]['satisfechos'] / (
                        demandas_por_estacion[estacion.num]['satisfechos'] + demandas_por_estacion[estacion.num][
                    'insatisfechos'])
                file.write('{},{}\n'.format(estacion.num, sat))

        with open('resultados.txt', 'w') as file:
            file.write('Satisfaccion de demanda:\n{} <= {} <= {}\n'.format(intervalo_bajo, promedio_satisfaccion,
                                                                           intervalo_alto))
            file.write(
                'Costos:\n{} <= {} <= {}\n'.format(bajo_objetivo, sum(objetivo) / numero_simulaciones, alto_objetivo))

        break


