# modelo de ruteo

from gurobipy import *
from math import sqrt
import networkx as nx


def ruteo(grupo, estaciones):
    m = Model('Modelo_ruteo')
    q = 80

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
            c[estacion][destino] = .013 * sqrt(estaciones['Estación {}'.format(estacion)].distancias_cuadrado[str(destino)])
        c[0][estacion] = 0
        c[estacion][0] = 0
        s[0] = 0
        n[0] = 0

    # crear variables
    y = {}
    y[0] = {}
    x = {}
    x[0] = {}
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
    m.addConstrs(
        quicksum(x[origen][estacion] for origen in grupo) - quicksum(x[estacion][destino] for destino in grupo) == n[
            estacion] - s[estacion] for estacion in grupo)


    m.addConstrs(x[i][j] <= q * y[i][j] for i in grupo for j in grupo)
    m.addConstrs(x[0][i] == 0 for i in grupo)
    m.addConstrs(x[i][0] == 0 for i in grupo)

    m.addConstrs(quicksum(y[i][j] for i in grupo) - quicksum(y[j][k] for k in grupo) == 0 for j in grupo)
    m.addConstr(quicksum(y[0][nodo] for nodo in grupo) == 1)
    m.addConstr(quicksum(y[nodo][0] for nodo in grupo) == 1)

    for i in grupo:
        for j in grupo:
            m.addConstr(x[i][j], GRB.GREATER_EQUAL, 0, 'c4')

    # resolver
    m.optimize()

    #for v in m.getVars():
     #   print(v.varName, v.x)

    #print(m.objVal)
    Grafo = nx.DiGraph()
    
    return m.objVal
