import simulacion
import time
from Problema_integrado import *
from scipy.stats import t
import numpy
import csv

if __name__ == '__main__':
    lista_aux = []
    with open('hola.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=',')
        for i in csv_reader:
            lista_aux.append(int(i[0].strip('\ufeff')))

    # lista_aux = [27, 15, 27, 19, 4, 6, 26, 21, 4, 21, 22, 27, 15, 23, 25, 9, 13, 20, 4, 15, 4, 26, 2, 25, 10, 27, 25, 6,
    #              12, 9, 24, 11, 10, 41, 42, 31, 4, 5, 13, 1, 10, 22, 26, 36, 29, 29, 19, 46, 23, 6, 11, 37, 45, 6, 5,
    #              11, 12, 36, 0, 19, 33, 2, 5, 5, 11, 26, 19, 50, 19, 25, 3, 7, 21, 0, 26, 10, 6, 3, 35, 9, 39, 42, 21,
    #              15, 4, 13, 8, 14, 40, 10, 4, 29]

    # lista_aux = [27, 15, 28, 19, 4, 5, 26, 21, 4, 23, 21, 27, 13, 26, 25, 9, 13, 20, 4, 14, 4, 26, 1, 26, 8, 27, 26, 5,
    #              11, 7, 23, 10, 8, 42, 44, 31, 4, 5, 13, 0, 10, 22, 26, 35, 30, 29, 18, 47, 25, 6, 11, 37, 45, 6, 4, 11,
    #              9, 36, 0, 17, 36, 2, 4, 5, 11, 27, 19, 52, 19, 27, 3, 7, 21, 0, 27, 10, 6, 3, 37, 9, 39, 40, 22, 15, 4,
    #              13, 8, 13, 40, 9, 4, 32]

    print(lista_aux)
    print(sum(lista_aux))

    intervalo_bajo = 0

    # Poblamos
    estaciones = read_json()
    for est in estaciones.values():
        est.probas(estaciones)
    s = simulacion.Simulador()

    if intervalo_bajo < 80:
        tiempo1 = time.time()
        s.lista_aux = lista_aux
        s.estaciones = estaciones
        s.prints = False
        lista_porcentajes = []
        i = 0
        numero_simulaciones = 0
        intervalo_alto = 999999999
        intervalo_bajo = 0
        tiempo2 = time.time()

        # Reajuste por sobra/necesidad
        # demandas_por_estacion = {i: 0 for i in range(1, 93)}

        # Reajuste por satisfaccion
        demandas_por_estacion = {
            i: {j: 0 for j in ('satisfechos', 'insatisfechos', 'manana', 'mediodia', 'tarde', 'noche')} for i in
            range(1, 93)}

        while (intervalo_alto - intervalo_bajo) > 2 or numero_simulaciones < 10:
            numero_simulaciones += 1

            # print('\nCorriendo repetición {}.'.format(str(numero_simulaciones)))
            # print(intervalo_alto - intervalo_bajo, numero_simulaciones, '\n')
            # print(intervalo_bajo, intervalo_alto)

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
            if False:
                clusters = opti_final(estaciones)
                for grupo in clusters.values():
                    ruteo(grupo, s.estaciones)

            # Obtenemos las medidas de desempeño

            porcentaje_satisfaccion = round(
                (s.demanda_satisfecha / (s.demanda_insatisfecha +
                                         s.demanda_satisfecha)) * 100, 2)
            lista_porcentajes.append(porcentaje_satisfaccion)

            estaciones_dda_satisfecha = [(e.demanda_satisfecha, e.number) for e in
                                         s.estaciones.values()]
            estaciones_dda_insatisfecha = [(e.demanda_insatisfecha, e.number) for e in
                                           s.estaciones.values()]

            # Reajuste por satisfaccion
            for estacion in s.estaciones.values():
                demandas_por_estacion[estacion.num]['satisfechos'] += estacion.demanda_satisfecha
                demandas_por_estacion[estacion.num]['insatisfechos'] += estacion.demanda_insatisfecha
                demandas_por_estacion[estacion.num]['manana'] += estacion.demanda_insatisfecha_manana
                demandas_por_estacion[estacion.num]['mediodia'] += estacion.demanda_insatisfecha_mediodia
                demandas_por_estacion[estacion.num]['tarde'] += estacion.demanda_insatisfecha_tarde
                demandas_por_estacion[estacion.num]['noche'] += estacion.demanda_insatisfecha_noche

            # Reajuste por sobras/necesidad
            # for estacion in s.estaciones.values():
            #     demandas_por_estacion[estacion.num] += estacion.inventario - estacion.inv_manana

            promedio_satisfaccion = sum(lista_porcentajes) / len(lista_porcentajes)
            varianza = round((float(numpy.std(lista_porcentajes).item()) ** 2), 4)

            # Intervalo de confianza al 95%

            studiante = t.interval(.95, numero_simulaciones - 1)
            intervalo_bajo = promedio_satisfaccion + studiante[0] * sqrt(varianza) / sqrt(numero_simulaciones)
            intervalo_alto = promedio_satisfaccion + studiante[1] * sqrt(varianza) / sqrt(numero_simulaciones)

        tiempo3 = time.time()
        promedio_satisfaccion = sum(lista_porcentajes) / len(lista_porcentajes)
        varianza = round((float(numpy.std(lista_porcentajes).item()) ** 2), 4)

        # Intervalo de confianza al 95%

        studiante = t.interval(.95, numero_simulaciones - 1)
        intervalo_bajo = promedio_satisfaccion + studiante[0] * sqrt(varianza) / sqrt(numero_simulaciones)
        intervalo_alto = promedio_satisfaccion + studiante[1] * sqrt(varianza) / sqrt(numero_simulaciones)

        # reajuste por satisfaccion
        demandas_estacion_ordenada = sorted(demandas_por_estacion,
                                            key=lambda est: -(demandas_por_estacion[est]['manana'] * .7 +
                                                              demandas_por_estacion[est]['mediodia'] * .3))

        # Reajuste por sobras/necesidad
        # demandas_estacion_ordenada = sorted(demandas_por_estacion, key=lambda est: demandas_por_estacion[est])

        if True:
            print('\nLas 5 estaciones con mayor cantidad de satisfaccion de demanda :')
            print(demandas_estacion_ordenada[-5:])
            print('\nLas 5 estaciones con mayor cantidad de insatisfaccion de demanda :')
            print(demandas_estacion_ordenada[:5])
        #
        # book = open('satisfacciones.csv', 'w')
        #
        # book.write('Estacion, inventario, manana, mediodia, tarde, noche\n')
        #
        # for est in estaciones.keys():
        #     num = estaciones[est].num
        #     book.write('{}, {}, {}, {}, {}, {}\n'.format(num, lista_aux[num - 1], demandas_por_estacion[num]['manana'],
        #                                                  demandas_por_estacion[num]['mediodia'],
        #                                                  demandas_por_estacion[num]['tarde'],
        #                                                  demandas_por_estacion[num]['noche']))
        #
        # book.close()

        if intervalo_bajo < 80:
            numero_de_mayores = 2
            cambios = 1
            aum = demandas_estacion_ordenada[:numero_de_mayores]
            dis = demandas_estacion_ordenada[-numero_de_mayores:]
            for i in range(numero_de_mayores):
                if lista_aux[dis[i] - 1] - cambios < 0:
                    lista_aux[aum[i] - 1] += lista_aux[dis[i] - 1]
                    lista_aux[dis[i] - 1] = 0
                else:
                    lista_aux[aum[i] - 1] += cambios
                    lista_aux[dis[i] - 1] -= cambios
            print(lista_aux)

        # print(lista_porcentajes)
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
