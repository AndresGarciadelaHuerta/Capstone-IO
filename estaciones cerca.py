from gurobipy import *
from simulacion import *
import grafvicho as pl

num_camiones = 2
M = 3000


def opti(estaciones, dic, param=True):
    m = Model('cluster')
    m.update()
    vars = {}
    for estacion in dic:
        vars[estacion] = {}
        for j in range(num_camiones):
            vars[estacion][j] = m.addVar(name='Z_{}_{}'.format(estacion, j), vtype=GRB.BINARY)
            m.update()
    m.addConstrs(quicksum(vars[i][j] for j in range(num_camiones)) >= 1 for i in vars)
    m.update()
    m.addConstr(quicksum(vars[i][0] for i in vars) - 1 <= quicksum(vars[i][1] for i in vars))
    m.addConstr(quicksum(vars[i][0] for i in vars) >= quicksum(vars[i][1] for i in vars) - 1)
    m.setObjective(quicksum(
        vars[i][j] * vars[k][j] * estaciones['Estación {}'.format(i)].distancias_cuadrado[k] for i in vars for k in vars
        for j in range(num_camiones)))
    m.update()
    m.Params.timeLimit = 20
    m.optimize()
    resultados = {i: {} for i in range(num_camiones)}
    for z in m.getVars():
        if z.X > 0 and 'Z' in z.varName:
            lista = z.varName.split('_')
            est = int(lista[1])
            cam = int(lista[2])
            if est not in resultados[cam]:
                resultados[cam][est] = 1
    return resultados


def opti_final(estaciones):
    final = {i: {} for i in range(8)}

    dic = {estacion.num: 0 for estacion in estaciones.values()}
    res = opti(s.estaciones, dic)
    cont = 0
    for i in res.values():
        res2 = opti(s.estaciones, i)
        for j in res2.values():
            res3 = opti(s.estaciones, j)
            for z in res3.values():
                final[cont] = z
                cont += 1

    for grupo in final:
        print('*' * 20)
        print('Grupo {}->{}'.format(grupo, len(final[grupo])))
        for estacion in final[grupo]:
            print('Estacion {}'.format(estacion))

    return final


if __name__ == '__main__':
    estaciones = poblar()
    s = Simulador()
    s.estaciones = estaciones
    s.run()
    final = opti_final(estaciones)
    pl.graficar(s.estaciones, final)
