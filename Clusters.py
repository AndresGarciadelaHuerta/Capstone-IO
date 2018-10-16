from gurobipy import *
from simulacion import *
import grafvicho as pl

num_camiones = 2
M = 3000


def opti(estaciones, dic, param=False):
    m = Model('cluster')
    m.update()
    N = {}
    S = {}
    vars = {}
    n = {}
    s = {}
    distancias = {}
    for estacion in dic:
        N[estacion] = dic[estacion]['n']
        S[estacion] = dic[estacion]['s']
        vars[estacion] = {}
        n[estacion] = {}
        s[estacion] = {}
        distancias[estacion] = {}
        for j in range(num_camiones):
            vars[estacion][j] = m.addVar(name='Z_{}_{}'.format(estacion, j), vtype=GRB.BINARY)
            m.update()
            n[estacion][j] = m.addVar(name='n_{}_{}'.format(estacion, j), vtype=GRB.INTEGER)
            s[estacion][j] = m.addVar(name='s_{}_{}'.format(estacion, j), vtype=GRB.INTEGER)
            m.update()

    m.addConstrs(quicksum((n[i][j] - s[i][j]) for i in vars) == 0 for j in range(num_camiones))
    m.update()
    m.addConstrs(M * vars[i][j] >= n[i][j] + s[i][j] for i in vars for j in range(num_camiones))
    m.update()
    m.addConstrs(quicksum(n[i][j] for j in range(num_camiones)) == N[i] for i in vars)
    m.update()
    m.addConstrs(quicksum(s[i][j] for j in range(num_camiones)) == S[i] for i in vars)
    m.update()
    m.addConstrs(quicksum(vars[i][j] for i in vars) <= len(dic) / 2 + len(dic) * .1 for j in range(num_camiones))
    m.update()
    m.addConstrs(s[i][j] >= 0 for i in vars for j in range(num_camiones))
    m.update()
    m.addConstrs(n[i][j] >= 0 for i in vars for j in range(num_camiones))
    m.update()

    m.setObjective(quicksum(
        vars[i][j] * vars[k][j] * estaciones['Estación {}'.format(i)].distancias_cuadrado[k] for i in vars for k in vars
        for j in range(num_camiones)))
    m.update()
    m.Params.MIPGap = .02
    m.Params.timeLimit = 20
    m.optimize()
    resultados = {i: {} for i in range(num_camiones)}
    for z in m.getVars():
        if z.X > 0 and 'Z' in z.varName:
            lista = z.varName.split('_')
            est = int(lista[1])
            cam = int(lista[2])
            if est not in resultados[cam]:
                resultados[cam][est] = {}
            resultados[cam][est]['n'] = n[est][cam].X
            resultados[cam][est]['s'] = s[est][cam].X
            cam2 = 0 if cam == 1 else 1
            if vars[est][cam].x == 1 and vars[est][cam2].x == 1:
                print('Tiene doble {} -> sobra: {} -> n: {}'.format(vars[est][cam].varName, S[est], N[est]))

        elif z.X == 0 and 'Z' in z.varName:
            lista = z.varName.split('_')
            est = int(lista[1])
            cam = int(lista[2])
            cam2 = 0 if cam == 1 else 1

    for grupo in resultados:
        if param:
            print('*' * 20)
            print('GRUPO {}->{}'.format(grupo, len(resultados[grupo])))
        n = 0
        s = 0
        for estacion in resultados[grupo]:
            if param:
                print('Estacion {}; necesidad {}; sobra {}'.format(estacion, resultados[grupo][estacion]['n'],
                                                                   resultados[grupo][estacion]['s']))
            n += resultados[grupo][estacion]['n']
            s += resultados[grupo][estacion]['s']

    return resultados

def opti_final(estaciones):
    N = {}
    S = {}
    final = {i: {} for i in range(8)}
    for estacion in estaciones.values():
        valor = estacion.inv_manana - estacion.inventario
        N[estacion.num] = valor if valor > 0 else 0
        S[estacion.num] = -valor if valor < 0 else 0

    dic = {estacion.num: {'n': N[estacion.num], 's': S[estacion.num]} for estacion in estaciones.values()}
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
        s_1 = 0
        n = 0
        print('*' * 20)
        print('Grupo {}->{}'.format(grupo, len(final[grupo])))
        for estacion in final[grupo]:
            print('Estacion {}->s:{}->n:{}'.format(estacion, final[grupo][estacion]['s'], final[grupo][estacion]['n']))
            s_1 += final[grupo][estacion]['s']
            n += final[grupo][estacion]['n']
        print('s: {}-> n: {}'.format(s_1, n))

    return final



if __name__ == '__main__':
    estaciones = poblar()
    s = Simulador()
    s.estaciones = estaciones
    s.run()
    final = opti_final(estaciones)
    pl.graficar(s.estaciones, final)
