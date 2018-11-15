import matplotlib.pyplot as plot


def graficar(estaciones, resultados):
    x = []
    y = []
    colores = []
    posibles = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray']
    for grupo in resultados:
        for estacion in resultados[grupo]:
            x.append(int(estaciones['Estación {}'.format(estacion)].x))
            y.append(int(estaciones['Estación {}'.format(estacion)].y))
            colores.append(posibles[grupo])

    plot.scatter(x, y, c=colores)
    plot.xlabel("Posicion en x")
    plot.ylabel("Posicion en y")
    plot.title("Composición Geográfica de las Zonas")
    plot.show()
