from simulacion import *
import statistics as stats

estaciones = poblar()
distancias = {}
tot = []

# distancias
for estacion in estaciones:
    for dis in estaciones[estacion].distancias_cuadrado:
        e = estaciones[estacion].distancias_cuadrado[dis]
        if e != 0:
            lug = estacion + ' a ' + str(dis)
            distancias[lug] = e ** 0.5
            tot.append(e ** 0.5)


print(max(distancias.items(), key=lambda k: k[1]))
print(min(distancias.items(), key=lambda k: k[1]))
print(stats.mean(tot))
print(stats.median(tot))
print(stats.stdev(tot))


