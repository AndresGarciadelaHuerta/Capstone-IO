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


if __name__ == '__main__':

    # Poblamos
    tiempo1 = time.time()
    estaciones = read_json()
    tiempoleer = time.time()

    for est in estaciones.values():
        est.probas(estaciones)

    # Hacemos listas con las estaciones que reciben y pierden bicis
    pierden = [i.num for i in estaciones.values() if i.flujo_total < 0]
    ganan = [i.num for i in estaciones.values() if i.flujo_total > 0]

    # Distribución uniforme
    # lista_2 = [17 if i < 3 else 18 for i in range(92)]

    # Distribucion definida por la funcion arriba
    # lista_2 = [distribucion_inicial_estacion(est, estaciones) for est in estaciones.values()]
    # lista_2[0] -= 1
    # print(sum(lista_2))
    # for i in range(1653 % sum(lista_2)):
    #     lista_2[lista_2.index(min(lista_2))] += 1

    # Distribucion inicial
    # lista_2 = [6, 23, 3, 17, 33, 22, 14, 22, 17, 14, 61, 13, 27, 1, 12, 26, 11, 3, 25, 20, 25, 8, 26, 9, 26, 12, 7, 25,
    #            18, 14, 15, 25, 10, 5, 8, 10, 25, 17, 6, 24, 26, 23, 5, 18, 13, 5, 10, 14, 12, 17, 11, 24, 28, 25, 25,
    #            23, 21, 13, 23, 18, 12, 25, 21, 23, 15, 6, 10, 12, 8, 13, 18, 15, 16, 29, 12, 6, 27, 26, 11, 21, 45, 53,
    #            3, 16, 21, 10, 28, 22, 27, 24, 25, 14]

    # Distribución b prima
    lista_2 = []
    with open('dist_b_p.csv', 'r') as file:
        file.readline()
        file.readline()
        for linea in file:
            line = linea.split(',')
            lista_2.append(int(line[2]))
            file.readline()

    s = simulacion.Simulador(lista_2)
    s.estaciones = estaciones
    s.definir_distribucion_manana()

    print(sum(lista_2))
    print(lista_2)
    s.lista_aux = lista_2

    intervalo_bajo = 100

    # Esto es para buscar base factible
    while intervalo_bajo > 80:
        objetivo = []
        ganancia = []
        s.prints = False
        lista_porcentajes = []
        numero_simulaciones = 0
        intervalo_alto = 999999999
        intervalo_bajo = 0
        tiempo2 = time.time()

        demandas_por_estacion = {
            i: {j: 0 for j in ('satisfechos', 'insatisfechos', 'manana', 'mediodia', 'tarde', 'noche')} for i in
            range(1, 93)}

        distribuciones_finales = {i: [0 for j in range(92)] for i in ('manana', 'mediodia', 'tarde', 'noche', 'total')}

        while (intervalo_alto - intervalo_bajo) > 2 or numero_simulaciones < 7:
            numero_simulaciones += 1
            print('\nCorriendo repetición {}.'.format(str(numero_simulaciones)))
            print(intervalo_alto - intervalo_bajo, numero_simulaciones, '\n')
            print(intervalo_bajo, intervalo_alto)
            if len(objetivo) > 1:
                print(sum(objetivo[-8:]))

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
            for esta in estaciones.values():
                distribuciones_finales['manana'][esta.num - 1] += esta.manana
                distribuciones_finales['mediodia'][esta.num - 1] += esta.mediodia
                distribuciones_finales['tarde'][esta.num - 1] += esta.tarde
                distribuciones_finales['noche'][esta.num - 1] += esta.noche
                distribuciones_finales['total'][esta.num - 1] += esta.manana + esta.mediodia + esta.tarde + esta.noche
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

            # Print demandas por tiempo
            for tiempo in ('manana', 'mediodia', 'tarde', 'noche'):
                suma = 0
                for estacion in estaciones.values():
                    suma += demandas_por_estacion[estacion.num][tiempo]

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

        # Prints medidas de desempeño
        if True:
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
        print('Tiempo en leer los datos: ' + str(round(tiempoleer - tiempo1, 2))
              + ' segundos.')
        print('Tiempo en simular todas las repeticiones: ' + str(round(
            tiempo3 - tiempo2, 2)) + ' segundos.')

        with open('heuristica_3.csv', 'a') as file:
            pp = sum(objetivo) / numero_simulaciones
            file.write(
                '{},{},{},{},{},{},{}\n'.format(intervalo_bajo, promedio_satisfaccion, intervalo_alto, bajo_objetivo, pp,
                                              alto_objetivo, lista_2))

        with open('satisfaccion.csv', 'w') as file:
            file.write('Estacion, Satisfaccion\n')
            for estacion in estaciones.values():
                sat = demandas_por_estacion[estacion.num]['satisfechos'] / (
                        demandas_por_estacion[estacion.num]['satisfechos'] + demandas_por_estacion[estacion.num][
                    'insatisfechos'])
                file.write('{},{}\n'.format(estacion.num, sat))
        #
        # with open('resultados.txt', 'w') as file:
        #     file.write('Satisfaccion de demanda:\n{} <= {} <= {}\n'.format(intervalo_bajo, promedio_satisfaccion,
        #                                                                    intervalo_alto))
        #     file.write(
        #         'Costos:\n{} <= {} <= {}\n'.format(bajo_objetivo, sum(objetivo) / numero_simulaciones, alto_objetivo))

        # Reasignamos bicis de acuerdo a su diferencia de inventarios
        lista = sorted(distribuciones_finales['total'])
        cont = 0
        while s.lista_aux[distribuciones_finales['total'].index(lista[cont])] == 0:
            cont += 1
        s.lista_aux[distribuciones_finales['total'].index(lista[cont])] -= 1
        s.lista_aux[distribuciones_finales['total'].index(lista[-1])] += 1
        print(distribuciones_finales['total'].index(lista[cont]), distribuciones_finales['total'].index(lista[-1]))
        cont += 1
        while s.lista_aux[distribuciones_finales['total'].index(lista[cont])] == 0:
            cont += 1
        s.lista_aux[distribuciones_finales['total'].index(lista[cont])] -= 1
        s.lista_aux[distribuciones_finales['total'].index(lista[-2])] += 1
        print(distribuciones_finales['total'].index(lista[cont]), distribuciones_finales['total'].index(lista[-2]))
        cont += 1
        while s.lista_aux[distribuciones_finales['total'].index(lista[cont])] == 0:
            cont += 1
        s.lista_aux[distribuciones_finales['total'].index(lista[cont])] -= 1
        s.lista_aux[distribuciones_finales['total'].index(lista[-3])] += 1
        print(distribuciones_finales['total'].index(lista[cont]), distribuciones_finales['total'].index(lista[-3]))
