# modelo de ruteo

from gurobipy import *
from math import sqrt
import networkx as nx
import matplotlib.pyplot as plt
from subtours import *

q = 80



def ruteo(grupo, estaciones, prints=True):

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
    c[0][0] = 0
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

    # Cumplimiento de la demanda
    m.addConstrs(
        quicksum(x[origen][estacion] for origen in auxiliar) - quicksum(x[estacion][destino] for destino in auxiliar) ==
        n[estacion] - s[estacion] for estacion in auxiliar)

    # Restriccion de carga del camion
    m.addConstrs(x[i][j] <= q * y[i][j] for i in grupo for j in grupo)

    # Rutas de HOME
    m.addConstrs(x[0][i] == 0 for i in grupo)
    m.addConstrs(x[i][0] == 0 for i in grupo)

    # Viajar a si mismo es cero
    m.addConstrs(y[nodo][nodo] == 0 for nodo in auxiliar)

    # Si entra a un nodo, entonces sale
    m.addConstrs(quicksum(y[i][j] for i in auxiliar) - quicksum(y[j][k] for k in auxiliar) == 0 for j in auxiliar)

    # Restricciones de flujo una sola vez a HOME
    m.addConstr(quicksum(y[0][nodo] for nodo in grupo) == 1)
    m.addConstr(quicksum(y[nodo][0] for nodo in grupo) == 1)

    for i in grupo:
        for j in grupo:
            m.addConstr(x[i][j], GRB.GREATER_EQUAL, 0, 'c4')

    # resolver
    m.Params.OutputFlag = 0
    m.optimize()
    a = identifica(m)

    if prints:
        if a != False:
            # con subtour
            if len(a) > 0:
                graficar_ruteo(grupo, estaciones, m, c, 0)
                # sin subtour
                graficar_ruteo(grupo, estaciones, m, c, a)
        else:
            #graficar_ruteo(grupo, estaciones, m, c, 0)
            pass


    for numero in grupo:
        estaciones['Estación {}'.format(numero)].inventario += round(grupo[numero]['n'], 0) - round(grupo[numero]['s'],
                                                                                                    0)

    tiempo = 0
    for inicio in y:
        for final in y[inicio]:
            tiempo += c[inicio][final] / .013 / 60 * y[inicio][final].x

    #with open('tiempo_camiones799.txt', 'a') as file:
    #    file.write(str(tiempo) + '\n')

    #if tiempo > 12:
    #    print('*' * 100)
    #    print('Tiempo')
    #    print('*' * 100)
    #print(tiempo)

    #if tiempo > 12:
        #print('*' * 100)
        #print('Tiempo')
        #print('*' * 100)
    #print(tiempo)

    print('Tiempo camiones: {}'.format(tiempo))
    with open('tiempo_16.csv', 'a') as file:
        file.write('{}\n'.format(tiempo))

    if tiempo > 12:
        print('*' * 100)
        print('Tiempo')
        print('*' * 100)


    return m.objVal

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


def graficar_ruteo(grupo, estaciones, m, c, con):
    Grafo = nx.DiGraph()
    x = []
    y = []
    costotot = 0
    for var in m.getVars():
        if 'x' in var.varName:
            x.append((var.varName, var.x))
        elif 'y' in var.varName:
            y.append((var.varName, var.x))

    for estacion in grupo:
        pos = (float(estaciones['Estación {}'.format(estacion)].x), float(estaciones['Estación {}'.format(estacion)].y))
        Grafo.add_node(estacion, pos=pos)
    # home
    #Grafo.add_node(0, pos=(0.0, 0.0))
    labels_pencils = {}
    for var in m.getVars():
        if con == 0:
            if 'y' in var.varName and var.x > 0 and '_0' not in var.varName:
            #if 'y' in var.varName and var.x > 0:

                lista = var.varName.split('_')
                i = int(lista[1])
                j = int(lista[2])
                Grafo.add_edge(i, j, cap=q)
                Grafo[i][j]['cost'] = round(c[i][j], 2)
                costotot += round(c[i][j], 2)
                if '_0' in var.varName:
                    for variable in m.getVars():
                        if 'x_{}_{}'.format(i, j) in variable.varName:
                            labels_pencils[i, j] = 'home'
                # else:
                #     name = var.varName.split('_')
                #     inicio = int(name[1])
                #     final = int(name[2])
                #     labels_pencils[inicio, final] = round(c[inicio][final], 2)

            if 'x' in var.varName and var.x > 0:
                lista = var.varName.split('_')
                i = int(lista[1])
                j = int(lista[2])
                labels_pencils[i, j] = '{}'.format(var.x)
        else:
            if var.varName in con and '_0' not in var.varName:
                nombre = var.varName
                print('editando')
                if con[var.varName] > 0:
                    lista = var.varName.split('_')
                    i = int(lista[1])
                    j = int(lista[2])
                    Grafo.add_edge(i, j, cap=q)
                    na = 'x' + nombre[1:]
                    Grafo[i][j]['cost'] = round(c[i][j], 2)
                    for nam in x:
                        if nam[0] == na:
                            labels_pencils[i, j] = '{}'.format(nam[1])
                    costotot += round(c[i][j], 2)

            elif 'y' in var.varName and var.x > 0 and var.varName not in \
                    con and '_0' not in var.varName:
                lista = var.varName.split('_')
                i = int(lista[1])
                j = int(lista[2])
                Grafo.add_edge(i, j, cap=q)
                Grafo[i][j]['cost'] = round(c[i][j], 2)
                costotot += round(c[i][j], 2)
                if '_0' in var.varName:
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
    nx.draw(Grafo, pos, with_labels=True, node_size=500, node_color="pink")

    nx.draw_networkx_edge_labels(Grafo, pos, edge_labels=labels_pencils)
    plt.show()

    # el costotot es el resultado real del ruteo con los subtours arreglados...
    # print('obj', m.objVal)
    # print('tot',costotot)
    # return m.objVal
    return costotot
