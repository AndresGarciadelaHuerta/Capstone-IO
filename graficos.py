from simulacion import *
import matplotlib.pyplot as plot


def graph(estaciones):

    x = [estacion.x for estacion in estaciones.values()]
    y = [estacion.y for estacion in estaciones.values()]
    cantidades = [(20 * (estacion.inventario - estacion.inv_manana)) for estacion in estaciones.values()]
    colores = []
    cantidades_bien = []
    x1 = []
    y1 = []
    i = 0
    for cantidad in cantidades:
        if cantidad > 100:
            cantidades_bien.append(abs(cantidad))
            x1.append(x[i])
            y1.append(y[i])
            colores.append("g")
            i += 1
        elif cantidad < -100:
            cantidades_bien.append(abs(cantidad))
            x1.append(x[i])
            y1.append(y[i])
            colores.append("r")
            i += 1
        else:
            cantidades_bien.append(abs(cantidad))
            x1.append(x[i])
            y1.append(y[i])
            colores.append("grey")
            i += 1
            continue
    #print(cantidades)
    #print([(abs(cantidad) + 1) for cantidad in cantidades])
    print(len(colores))
    print(cantidades_bien)
    plot.scatter(x1, y1, c=colores, s=cantidades_bien)
    plot.xlabel("Posicion en x")
    plot.ylabel("Posicion en y")
    plot.title("Excesos o Faltas al final del dia")
    plot.show()



if __name__ == '__main__':
    estaciones = poblar()
    s = Simulador()
    s.estaciones = estaciones
    s.run()
    graph(s.estaciones)