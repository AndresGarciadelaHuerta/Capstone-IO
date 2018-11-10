import simulacion
import time
from Problema_integrado import *
from scipy.stats import t
import numpy
import csv

lista = []
contador_menores = 0


def distribucion_inicial_estacion(estacion, estaciones):
    estacion.probas(estaciones)
    llegan_manana = sum(estacion.probs['manana'].values())
    # print(llegan_manana)
    llegan_mediodia = sum(estacion.probs['mediodia'].values())
    llegan_tarde = sum(estacion.probs['tarde'].values())
    llegan_noche = sum(estacion.probs['noche'].values())
    salen_manana = 3 * estacion.tasa_manana
    # print(salen_manana)
    salen_mediodia = 3 * estacion.tasa_mediodia
    salen_tarde = 3 * estacion.tasa_tarde
    salen_noche = 3 * estacion.tasa_noche
    inicial = 0
    manana = llegan_manana - salen_manana
    mediodia = llegan_mediodia - salen_mediodia
    tarde = llegan_tarde - salen_tarde
    noche = llegan_noche - salen_noche
    suma_ida = manana + mediodia
    suma_vuelta = tarde + noche
    suma = manana + mediodia + tarde + noche
    # if manana < 0:
    #     inicial += manana
    # #print(inicial)
    # if mediodia < 0:
    #     inicial += mediodia
    # if tarde < 0:
    #     inicial += tarde
    # if noche < 0:
    #     inicial += noche
    # #print(inicial)
    # #print('-------------')
    # if suma < 0:
    #     inicial = int(round(suma * -1, 0)) + 40
    # else:
    #     if suma < 5:
    #         inicial = 25
    #     if suma > 5:
    #         inicial = 20
    #     if suma > 10:
    #         inicial = 15
    #     if suma > 15:
    #         inicial = 15
    #     if suma > 20:
    #         inicial = 17
    if suma_ida > 0 and suma_vuelta > 0:
        inicial = max(int(llegan_manana / 3), 2)
    elif suma_ida > 0 and suma_vuelta < 0:
        inicial = int(-suma_ida - suma_vuelta) + max(int(llegan_manana / 3), 2)
    elif suma_ida < 0 and suma_vuelta > 0:
        inicial = int(-suma_ida) + 5
    elif suma_ida < 0 and suma_vuelta < 0:
        inicial = int(-suma_ida - suma_vuelta) + 10

    return max(5, inicial)


if __name__ == '__main__':

    intervalo_bajo = 0

    # Poblamos
    estaciones = read_json()

    for est in estaciones.values():
        est.probas(estaciones)
    s = simulacion.Simulador()
    s.estaciones = estaciones

    # Hacemos listas con las estaciones que reciben y pierden bicis
    pierden = [i.num for i in estaciones.values() if i.flujo_total < 0]
    ganan = [i.num for i in estaciones.values() if i.flujo_total > 0]

    # Creamos la dist inicial
    lista_2 = [7, 21, 12, 12, 29, 32, 10, 17, 18, 10, 11, 10, 22, 11, 11, 33, 12, 12, 27, 19, 26, 11, 27, 11, 38, 11,
               11, 23, 13, 16, 11, 36, 11, 5, 5, 11, 35, 19, 11, 24, 34, 18, 11, 11, 8, 11, 11, 10, 5, 15, 14, 11, 11,
               21, 35, 19, 20, 6, 48, 13, 5, 32, 19, 35, 17, 11, 12, 6, 11, 7, 18, 15, 12, 41, 6, 11, 29, 53, 5, 19, 11,
               11, 11, 11, 20, 11, 33, 19, 11, 22, 34, 66]

    lista_2 = []

    for estacion in s.estaciones.values():
        lista_2.append(distribucion_inicial_estacion(estacion, s.estaciones))
    print(sum(lista_2))
    s.lista_aux = lista_2

    prom_anterior = 0

    # Esto es para buscar base factible
    for i in range(10):
        print(s.lista_aux)
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

            # estaciones_dda_satisfecha = [(e.demanda_satisfecha, e.number) for e in
            #                              s.estaciones.values()]
            # estaciones_dda_insatisfecha = [(e.demanda_insatisfecha, e.number) for e in
            #                                s.estaciones.values()]

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
                                            key=lambda x: (demandas_por_estacion[x]['insatisfechos']))

        if True:
            print('\nLas 5 estaciones con mayor cantidad de satisfaccion de demanda :')
            print(demandas_estacion_ordenada[:5])
            print('\nLas 5 estaciones con mayor cantidad de insatisfaccion de demanda :')
            print(demandas_estacion_ordenada[-5:])

        # if intervalo_bajo < 80:
        #     numero_de_mayores = 2
        #     cambios = 1
        #     aum = demandas_estacion_ordenada[:numero_de_mayores]
        #     dis = demandas_estacion_ordenada[-numero_de_mayores:]
        #     for i in range(numero_de_mayores):
        #         if lista_aux[dis[i] - 1] - cambios < 0:
        #             lista_aux[aum[i] - 1] += lista_aux[dis[i] - 1]
        #             lista_aux[dis[i] - 1] = 0
        #         else:
        #             lista_aux[aum[i] - 1] += cambios
        #             lista_aux[dis[i] - 1] -= cambios
        #     print(lista_aux)

        # print(lista_porcentajes)

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

        # Reacomodo de bicis de acuerdo a estatus
        a_quitar = demandas_estacion_ordenada[0]
        cont = 1
        while a_quitar not in pierden:
            a_quitar = demandas_estacion_ordenada[cont]
            cont += 1

        a_dar = demandas_estacion_ordenada[-1]
        con = -1
        while a_dar not in ganan:
            a_dar = demandas_estacion_ordenada[cont - 1]
            cont -= 1

        s.lista_aux[a_quitar - 1] -= 1
        s.lista_aux[a_dar - 1] += 1
        print(a_quitar, a_dar)
        print('Promedio anterior {}\nNuevo {}'.format(prom_anterior, sum(objetivo) / numero_simulaciones))
        prom_anterior = sum(objetivo) / numero_simulaciones
