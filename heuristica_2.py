import simulacion
import time
from Problema_integrado import *
from scipy.stats import t
import numpy


def distribucion_inicial_estacion(estacion, estaciones):
    estacion.probas(estaciones)
    pond = 1
    llegan_manana = sum(estacion.probs['manana'].values()) * pond
    llegan_mediodia = sum(estacion.probs['mediodia'].values()) * pond
    llegan_tarde = sum(estacion.probs['tarde'].values()) * pond
    llegan_noche = sum(estacion.probs['noche'].values()) * pond
    salen_manana = 3 * estacion.tasa_manana
    salen_mediodia = 3 * estacion.tasa_mediodia
    salen_tarde = 3 * estacion.tasa_tarde
    salen_noche = 3 * estacion.tasa_noche
    manana = llegan_manana - salen_manana
    mediodia = llegan_mediodia - salen_mediodia
    tarde = llegan_tarde - salen_tarde
    noche = llegan_noche - salen_noche
    suma = llegan_manana + llegan_mediodia + llegan_tarde + llegan_noche
    suma_ida = manana + mediodia
    suma_vuelta = tarde + noche
    pond = .2
    if suma_ida > 0 and suma_vuelta > 0:
        inicial = salen_manana * pond - 1
    elif suma_ida > 0 and suma_vuelta < 0:
        inicial = salen_manana * pond - min(suma_ida + suma_vuelta, 0) + salen_tarde * pond
        inicial += inicial * .15 + 4
    elif suma_ida < 0 and suma_vuelta > 0:
        inicial = salen_manana * pond - suma_ida + salen_tarde * pond
        inicial += inicial * .15
    elif suma_ida < 0 and suma_vuelta < 0:
        inicial = int(salen_manana * pond + salen_manana + salen_mediodia + salen_tarde + salen_noche) - (
                llegan_manana + llegan_mediodia + llegan_mediodia + llegan_noche) + salen_tarde * pond
    return max(0, int(inicial * .81))


def heuristica_2(lista_aux, demandas_ordenadas, cont=-1):
    while lista_aux[demandas_ordenadas[cont]] == 0: cont -= 1
    lista_aux[demandas_ordenadas[cont]] -= 1
    lista_aux[demandas_ordenadas[0] - 1] += 1


if __name__ == '__main__':

    # Poblamos
    estaciones = read_json()

    for est in estaciones.values():
        est.probas(estaciones)

    # Hacemos listas con las estaciones que reciben y pierden bicis
    pierden = [i.num for i in estaciones.values() if i.flujo_total < 0]
    ganan = [i.num for i in estaciones.values() if i.flujo_total > 0]

    # Distribucion que cumple con el 80% por si sola
    # lista_2 = [2, 20, 5, 10, 33, 31, 7, 14, 19, 7, 3, 5, 19, 5, 5, 33, 6, 6, 25, 20, 29, 4, 30, 4, 39, 5, 5, 25, 11, 16,
    #            5, 36, 6, 2, 2, 5, 35, 20, 6, 27, 34, 16, 5, 3, 3, 5, 6, 6, 2, 18, 13, 5, 0, 18, 36, 16, 21, 2, 52, 10,
    #            2, 36, 20, 35, 17, 5, 5, 2, 6, 3, 19, 15, 9, 47, 2, 6, 27, 57, 2, 15, 6, 3, 5, 9, 21, 10, 32, 21, 1, 24,
    #            34, 60]

    # Distribucion que no cumple sola el 80 %
    # lista_2 = [0, 11, 0, 1, 24, 22, 0, 5, 10, 0, 0, 0, 10, 0, 0, 24, 0, 0, 16, 11, 20, 0, 21, 0, 30, 0, 0, 16, 2, 7, 0,
    #            27, 0, 0, 0, 0, 26, 11, 0, 18, 25, 7, 0, 0, 0, 0, 0, 0, 0, 9, 4, 0, 0, 9, 27, 7, 12, 0, 43, 1, 0, 27, 11,
    #            26, 8, 0, 0, 0, 0, 0, 10, 6, 0, 38, 0, 0, 18, 48, 0, 6, 0, 0, 0, 0, 12, 1, 23, 12, 0, 15, 25, 51]

    # lista_2 = [1, 18, 6, 18, 34, 37, 14, 20, 16, 16, 2, 16, 28, 6, 2, 40, 6, 4,
    #            32, 20, 30, 1, 30, 1, 49, 0, 3, 26, 18, 16, 2, 42, 8, 6, 5, 1,
    #            41, 17, 5, 28, 40, 24, 4, 1, 12, 1, 2, 16, 9, 17, 14, 0, 1, 14,
    #            42, 22, 24, 13, 58, 24, 12, 33, 26, 41, 13, 1, 11, 12, 9, 13, 15,
    #            15, 16, 47, 10, 6, 36, 64, 11, 9, 2, 0, 8, 15, 19, 14, 40, 24, 1, 25, 41, 61]

    # lista_2 = [1, 29, 4, 17, 36, 37, 14, 22, 17, 14, 2, 13, 28, 3, 2, 39,
    #            8, 3, 30, 20, 29, 2, 31, 2, 49, 3, 4, 25, 18, 14, 4, 42, 8, 4,
    #            8, 7,
    #            41, 17, 5, 28, 40, 25, 3, 2, 13, 3, 6, 14, 12, 17, 12, 4, 2, 25,
    #            45, 24, 21, 13, 59, 18, 12, 39, 21, 41, 15, 3, 10, 12, 7, 13,
    #            18, 15, 16, 52, 12, 7, 34, 60, 10, 16, 3, 4, 5, 14, 21, 10, 31,
    #            23, 2, 24, 32, 33]

    # lista_2 = [distribucion_inicial_estacion(est, estaciones) for est in estaciones.values()]
    # lista_2[0] -= 1
    # print(sum(lista_2))
    # for i in range(1653 % sum(lista_2)):
    #     lista_2[lista_2.index(min(lista_2))] += 1

    with open('dist_inicial_heuristica_2.csv', 'r') as file:
        lista_2 = []
        file.readline()
        for line in file:
            line = line.split(',')
            lista_2.append(int(line[1]))
        lista_2 = lista_2[:-1]

    # lista_2 = [17 for i in range(92)]
    # for i in range(1653 % sum(lista_2)):
    #     lista_2[lista_2.index(min(lista_2))] += 1

    with open('dist_inicial_minima.csv', 'w') as file:
        file.write('Estacion, Minimo\n')
        for est in estaciones.values():
            file.write('{},{}\n'.format(est.num, lista_2[est.num - 1]))

    s = simulacion.Simulador(lista_2)
    s.estaciones = estaciones
    s.definir_distribucion_manana()

    #print(sum(lista_2))
    #print(lista_2)
    s.lista_aux = lista_2

    prom_anterior = 0

    intervalo_bajo = 100

    # Esto es para buscar base factible
    for repeticion in range(1):
        #print(s.lista_aux)
        #print(sum(s.lista_aux))
        objetivo = []
        ganancia = []
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

        while (intervalo_alto - intervalo_bajo) > 2 or numero_simulaciones < 50:
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
            ganancia.append(s.ganancia)
            if True:
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

            # Print demandas por tiempo
            for tiempo in ('manana', 'mediodia', 'tarde', 'noche'):
                suma = 0
                for estacion in estaciones.values():
                    suma += demandas_por_estacion[estacion.num][tiempo]
                #print('{} -> {}'.format(tiempo, suma))

        tiempo3 = time.time()
        promedio_satisfaccion = sum(lista_porcentajes) / len(lista_porcentajes)
        varianza = round((float(numpy.std(lista_porcentajes).item()) ** 2), 4)
        var_objetivo = round((float(numpy.std(objetivo).item()) ** 2), 4)
        var_ganancia = round((float(numpy.std(ganancia).item()) ** 2), 4)

        # Intervalo de confianza al 95%

        studiante = t.interval(.95, numero_simulaciones - 1)
        intervalo_bajo = promedio_satisfaccion + studiante[0] * sqrt(varianza) / sqrt(numero_simulaciones)
        intervalo_alto = promedio_satisfaccion + studiante[1] * sqrt(varianza) / sqrt(numero_simulaciones)
        bajo_objetivo = sum(objetivo) / numero_simulaciones + studiante[0] * sqrt(var_objetivo) / sqrt(
            numero_simulaciones)
        alto_objetivo = sum(objetivo) / numero_simulaciones + studiante[1] * sqrt(var_objetivo) / sqrt(
            numero_simulaciones)
        bajo_ganancia = sum(ganancia) / numero_simulaciones + studiante[0] * sqrt(var_ganancia) / sqrt(
            numero_simulaciones)
        alto_ganancia = sum(ganancia) / numero_simulaciones + studiante[1] * sqrt(var_ganancia) / sqrt(
            numero_simulaciones)

        # reajuste por satisfaccion
        demandas_estacion_ordenada = sorted(demandas_por_estacion,
                                            key=lambda x: (demandas_por_estacion[x]['satisfechos'] / (
                                                    demandas_por_estacion[x]['insatisfechos'] +
                                                    demandas_por_estacion[x]['satisfechos'])))

        if False:
            print('\nLas 5 estaciones con mayor cantidad de insatisfaccion de demanda :')
            for num in range(5):
                a = demandas_estacion_ordenada[num]
                print('{} -> {}'.format(a, demandas_por_estacion[a]['satisfechos'] / (
                        demandas_por_estacion[a]['insatisfechos'] + demandas_por_estacion[a]['satisfechos'])))
            print('\nLas 5 estaciones con mayor cantidad de satisfaccion de demanda :')
            for x in range(5):
                a = demandas_estacion_ordenada[-x - 1]
                print('{} -> {}'.format(demandas_estacion_ordenada[-x - 1], demandas_por_estacion[a]['satisfechos'] / (
                        demandas_por_estacion[a]['insatisfechos'] +
                        demandas_por_estacion[a]['satisfechos'])))
            for i in range(92):
                print('{} -> {}'.format(i + 1, lista_2[i]))

        ### Corremos la heuristica 2 para obtener nueva distribución inicial ###
        heuristica_2(s.lista_aux, demandas_estacion_ordenada)

        print('--------------------------------------------------------------')
        print('Porcentaje Promedio de Satisfaccion de la Demanda: ' + str(
            promedio_satisfaccion) + "%")
        print('Varianza de los Porcentajes de Satisfacción de la Demanda: ' + str(
            varianza))
        print('Intervalo de confianza al 95% de satisfacción: {} <= X <= {}'.format(intervalo_bajo, intervalo_alto))
        print('Funcion Objetivo: {}'.format(sum(objetivo) / numero_simulaciones))
        print('Intervalo al 95%: {} <= X <= {}'.format(bajo_objetivo, alto_objetivo))
        print('Ingreso: {}'.format(sum(ganancia) / len(ganancia)))
        print('Intervalo: {} <= {} <= {}'.format(bajo_ganancia / 1000000, sum(ganancia) / len(ganancia) / 1000000,
                                                 alto_ganancia / 1000000))
        print('Utilidad: {}'.format(sum(ganancia) / len(ganancia) / 1000000 - sum(objetivo) / numero_simulaciones))
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

        with open('resultados_1.txt', 'a') as file:
            file.write('Satisfaccion de demanda:\n{} <= {} <= {}\n'.format(intervalo_bajo, promedio_satisfaccion,
                                                                           intervalo_alto))
            file.write('Distribución Inicial:' + str(s.lista_aux) + '\n')
            file.write(
                'Costos:\n{} <= {} <= {}\n'.format(bajo_objetivo, sum(objetivo) / numero_simulaciones, alto_objetivo))


