from gurobipy import *
from simulacion import *
from lectura_json import read_json
import grafvicho as pl

num_camiones = 2
M = 3000


def opti(estaciones, dic, params=False):
    m = Model('cluster')
    m.update()
    N = {}
    S = {}
    vars = {}
    n = {}
    s = {}
    distancias = {}
    for estacion in dic:
        N[estacion] = round(dic[estacion]['n'], 1)
        S[estacion] = round(dic[estacion]['s'], 1)
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

    # Restriccion de neteo de demanda
    m.addConstrs(quicksum((n[i][j] - s[i][j]) for i in vars) == 0 for j in range(num_camiones))
    m.update()

    # Restriccion de cero n y s si no se asigna
    m.addConstrs(M * vars[i][j] >= n[i][j] + s[i][j] for i in vars for j in range(num_camiones))
    m.update()

    # Suma igual a la necesidad
    m.addConstrs(quicksum(n[i][j] for j in range(num_camiones)) == N[i] for i in vars)
    m.update()
    m.addConstrs(quicksum(s[i][j] for j in range(num_camiones)) <= S[i] for i in vars)
    m.update()

    # Naturaleza de las variables
    m.addConstrs(s[i][j] >= 0 for i in vars for j in range(num_camiones))
    m.update()
    m.addConstrs(n[i][j] >= 0 for i in vars for j in range(num_camiones))
    m.update()

    m.setObjective(quicksum(
        vars[i][j] * vars[k][j] * estaciones['Estación {}'.format(i)].distancias_cuadrado[str(k)] for i in vars for k in
        vars
        for j in range(num_camiones)))
    m.update()
    if params:
        m.Params.MIPGap = .1
        m.Params.timeLimit = 60
        m.Params.OutputFlag = 0
    else:
        m.Params.OutputFlag = 0
    m.optimize()
    resultados = {i: {} for i in range(num_camiones)}
    for z in m.getVars():
        if z.X > 0 and 'Z' in z.varName:
            lista = z.varName.split('_')
            est = int(lista[1])
            cam = int(lista[2])
            if est not in resultados[cam]:
                resultados[cam][est] = {}
            resultados[cam][est]['n'] = int(round(n[est][cam].X, 0))
            resultados[cam][est]['s'] = int(round(s[est][cam].X, 0))

    for grupo in resultados:
        n = 0
        s = 0
        for estacion in resultados[grupo]:
            n += resultados[grupo][estacion]['n']
            s += resultados[grupo][estacion]['s']
        if (n - s) != 0:
            print('VERGA DE PUTAS\n')

    return resultados


def opti_final(estaciones, prints=False):
    N = {}
    S = {}

    for estacion in estaciones.values():
        valor = estacion.inv_manana - estacion.inventario
        N[estacion.num] = valor if valor > 0 else 0
        S[estacion.num] = -valor if valor < 0 else 0

    dic = {estacion.num: {'n': N[estacion.num], 's': S[estacion.num]} for estacion in estaciones.values()}
    res = opti(estaciones, dic, True)
    cont = 0

    # 2 camiones
    # final = {i: {} for i in range(1)}
    # for i in res.values():
    #     final[cont] = i
    #     cont += 1

    # 4 camiones
    # final = {i: {} for i in range(4)}
    # for i in res.values():
    #     res2 = opti(estaciones, i)
    #     for j in res2.values():
    #         final[cont] = j
    #         cont += 1

    # 8 camiones
    final = {i: {} for i in range(8)}
    for i in res.values():
        res2 = opti(estaciones, i)
        for j in res2.values():
            res3 = opti(estaciones, j)
            for z in res3.values():
                final[cont] = z
                cont += 1

    # 16 camiones
    # final = {i: {} for i in range(16)}
    # for i in res.values():
    #     res2 = opti(estaciones, i)
    #     for j in res2.values():
    #         res3 = opti(estaciones, j)
    #         for z in res3.values():
    #             res4 = opti(estaciones, z)
    #             for num in res4.values():
    #                 final[cont] = num
    #                 cont += 1

    if prints:
        total = 0

        for estacion in estaciones.values():
            print('Estación {}: n-> {}: s-> {}'.format(estacion.num, N[estacion.num], S[estacion.num]))

        for grupo in final:
            total += len(final[grupo])
            s_1 = 0
            n = 0
            print('*' * 20)
            print('Grupo {}->{}'.format(grupo, len(final[grupo])))
            for estacion in final[grupo]:
                print('Estacion {}->s:{}->n:{}'.format(estacion, final[grupo][estacion]['s'],
                                                       final[grupo][estacion]['n']))
                s_1 += final[grupo][estacion]['s']
                n += final[grupo][estacion]['n']
            print('s: {}-> n: {}'.format(s_1, n))

        print('*' * 20)
        print('Total Estaciones -> {}'.format(total))
        print('Duplicados')
        for grupo in final:
            for estacion in final[grupo]:
                booleano = False
                for numero in final:
                    if grupo != numero:
                        if estacion in final[numero]:
                            booleano = True
                if booleano:
                    print('Estacion {}-> Grupo {}'.format(estacion, grupo))

        print('*' * 20 + '\nNo estan en niun lado:')

        for estacion in estaciones.values():
            bool = False
            for grupo in final.values():
                if estacion.num in grupo:
                    bool = True
            if not bool:
                print('Estación {}'.format(estacion.num))
        pl.graficar(estaciones, final)
    return final


def inicio(prints=False):
    estaciones = read_json()
    s = Simulador()
    s.estaciones = estaciones
    s.run()
    final = opti_final(estaciones)
    if prints:
        pl.graficar(s.estaciones, final)
    return final, s


if __name__ == '__main__':
    inicio()
