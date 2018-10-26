# modelo de ruteo

from gurobipy import *
from math import sqrt
import networkx as nx
import matplotlib.pyplot as plt
from subtours import *


q = 80

def ruteo(grupo, estaciones, prints=False):
    lista_aux = []
    for estacion in grupo:
        grupo[estacion]['n'] = int(round(grupo[estacion]['n'], 1))
        grupo[estacion]['s'] = int(round(grupo[estacion]['s'], 1))
        if grupo[estacion]['n'] + grupo[estacion]['s'] == 0:
            lista_aux.append(estacion)
    for estacion in lista_aux:
        del grupo[estacion]
    m = Model('Modelo_ruteo')

    # model.addvariables

    # diferencias
    s = {}
    n = {}

    # costos
    c = {}
    c[0] = {}
    for estacion in grupo:
        c[estacion] = {}
        s[estacion] = grupo[estacion]['s']
        n[estacion] = grupo[estacion]['n']
        for destino in grupo:
            c[estacion][destino] = .013 * sqrt(
                estaciones['Estación {}'.format(estacion)].distancias_cuadrado[str(destino)])
        c[0][estacion] = 0
        c[estacion][0] = 0
    s[0] = 0
    n[0] = 0

    # crear variables
    y = {}
    y[0] = {}
    x = {}
    x[0] = {}
    x[0][0] = m.addVar(vtype=GRB.INTEGER, name='x_{}_{}'.format(0, 0))
    y[0][0] = m.addVar(vtype=GRB.BINARY, name='y_{}_{}'.format(0, 0))
    for i in grupo:
        x[0][i] = m.addVar(vtype=GRB.INTEGER, name='x_{}_{}'.format(0, i))
        y[0][i] = m.addVar(vtype=GRB.BINARY, name='y_{}_{}'.format(0, i))
        e = {}
        r = {}
        e[0] = m.addVar(vtype=GRB.BINARY, name='y_{}_{}'.format(i, 0))
        r[0] = m.addVar(vtype=GRB.INTEGER, name='x_{}_{}'.format(i, 0))
        for j in grupo:
            e[j] = m.addVar(vtype=GRB.BINARY, name='y_{}_{}'.format(i, j))
            r[j] = m.addVar(vtype=GRB.INTEGER, name='x_{}_{}'.format(i, j))
        y[i] = e
        x[i] = r

    m.update()

    # F.O
    m.setObjective(quicksum(c[estacion][destino] * y[estacion][destino] for estacion in grupo for destino in grupo),
                   GRB.MINIMIZE)

    # restricciones

    auxiliar = {0: ''}
    auxiliar.update(grupo)

    m.addConstrs(
        quicksum(x[origen][estacion] for origen in auxiliar) - quicksum(x[estacion][destino] for destino in auxiliar) ==
        n[
            estacion] - s[estacion] for estacion in auxiliar)

    m.addConstrs(x[i][j] <= q * y[i][j] for i in grupo for j in grupo)
    m.addConstrs(x[0][i] == 0 for i in grupo)
    m.addConstrs(x[i][0] == 0 for i in grupo)

    m.addConstrs(y[nodo][nodo] == 0 for nodo in auxiliar)

    m.addConstrs(quicksum(y[i][j] for i in auxiliar) - quicksum(y[j][k] for k in auxiliar) == 0 for j in auxiliar)
    m.addConstr(quicksum(y[0][nodo] for nodo in grupo) == 1)
    m.addConstr(quicksum(y[nodo][0] for nodo in grupo) == 1)

    for i in grupo:
        for j in grupo:
            m.addConstr(x[i][j], GRB.GREATER_EQUAL, 0, 'c4')

    # resolver
    m.Params.OutputFlag = 0
    m.optimize()

    if prints:
        a = identifica(m)
        if a != False:
            graficar_ruteo(grupo, estaciones, m, c, a)
        else:
            graficar_ruteo(grupo, estaciones, m, c, 0)


    # for var in m.getVars():
    #   if 'x' in var.varName:
    #      print('Estación {}-> {}'.format(var.varName, var.x))

    # for var in m.getVars():
    #   if 'y' in var.varName:
    #      print('Estación {}-> {}'.format(var.varName, var.x))


    # print(m.objVal)

    # for estacion in grupo:
    #     print('Estacion {}-> n: {}-> s: {}'.format(estacion, grupo[estacion]['n'], grupo[estacion]['s']))

    # Grafo dibujado
    # Grafo dibujado

    # for v in m.getVars():
    #   print(v.varName, v.x)

    # print(m.objVal)


def graficar_ruteo(grupo, estaciones, m, c, cond):
    Grafo = nx.DiGraph()
    for estacion in grupo:
        pos = (float(estaciones['Estación {}'.format(estacion)].x), float(estaciones['Estación {}'.format(estacion)].y))
        Grafo.add_node(estacion, pos=pos)
    Grafo.add_node(0, pos=(0.0, 0.0))
    labels_pencils = {}
    for var in m.getVars():
        if cond == 0:
            if 'y' in var.varName and var.x > 0:
                lista = var.varName.split('_')
                i = int(lista[1])
                j = int(lista[2])
                Grafo.add_edge(i, j, cap=q)
                Grafo[i][j]['cost'] = round(c[i][j], 2)
                if '0' in var.varName:
                    for variable in m.getVars():
                        if 'x_{}_{}'.format(i, j) in variable.varName:
                            labels_pencils[i, j] = 'home'

            if 'x' in var.varName and var.x > 0:
                lista = var.varName.split('_')
                i = int(lista[1])
                j = int(lista[2])
                labels_pencils[i, j] = '{}'.format(var.x)
        else:
            if var.varName in cond:
                if cond[var.varName] > 0:
                    lista = var.varName.split('_')
                    i = int(lista[1])
                    j = int(lista[2])
                    Grafo.add_edge(i, j, cap=q)
                    Grafo[i][j]['cost'] = round(c[i][j], 2)

            elif 'y' in var.varName and var.x > 0:
                lista = var.varName.split('_')
                i = int(lista[1])
                j = int(lista[2])
                Grafo.add_edge(i, j, cap=q)
                Grafo[i][j]['cost'] = round(c[i][j], 2)
                if '0' in var.varName:
                    for variable in m.getVars():
                        if 'x_{}_{}'.format(i, j) in variable.varName:
                            labels_pencils[i, j] = 'home'

            if 'x' in var.varName and var.x > 0:
                lista = var.varName.split('_')
                i = int(lista[1])
                j = int(lista[2])
                labels_pencils[i, j] = '{}'.format(var.x)

    pos = nx.get_node_attributes(Grafo, 'pos')
    plt.figure("Grafo red")
    nx.draw(Grafo, pos, with_labels=True, node_size=500, node_color="blue")

    nx.draw_networkx_edge_labels(Grafo, pos, edge_labels=labels_pencils)
    plt.show()
    return m.objVal
