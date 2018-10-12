from simulacion import *
import statistics as stats
import numpy as np
from scipy.stats import kurtosis, skew, normaltest
import matplotlib.pyplot as plt

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
            if e == 1:
                print(lug)
            tot.append(e ** 0.5)

ma = max(distancias.items(), key=lambda k: k[1])
mi = min(distancias.items(), key=lambda k: k[1])
print(ma)
print(mi)
print(stats.mean(tot))
print(stats.median(tot))
print(stats.stdev(tot))
print(skew(tot))
print(kurtosis(tot))


# separando en trayectos:
tramos = []
tot.sort()
for i in range(int(ma[1])//5):
    e = []
    for elem in tot:
        if elem < 5 * i:
            r = tot.pop(0)
            e.append(r)
    tramos.append(e)
tramos.append(tot)

cant = []
for elem in tramos:
    cant.append(len(elem))

print(normaltest(cant))
lista1 = cant
plt.plot(lista1)   # Dibuja el gráfico
plt.title("Distancias")   # Establece el título del gráfico
plt.xlabel("Distancia")   # Establece el título del eje x
plt.ylabel("Cantidad")   # Establece el título del eje y
plt.show()

