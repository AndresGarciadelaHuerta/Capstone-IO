'''
y _i,j = 1 si existe la ruta
x = carga en cada wea
'''

# cambiar valor de FO cuando entra a subtour!

def identifica(m):
    x = []
    y = []
    variables = []
    sirven = []
    tot = []
    orden = []
    vari = []

    for var in m.getVars():
        if 'x' in var.varName:
            x.append((var.varName, var.x))

    for var in m.getVars():
        if 'y' in var.varName:
            y.append((var.varName, var.x))

    for var in y:
        vari.append(list(var))

    for var in vari:
        var[0] = var[0][2:]
        variables.append(var)

    for i in variables:
        i[0] = i[0].split('_')

    # aca se crea la lista de rutas que si se usan
    for va in variables:
        if va[1] != 0.0 and va[1] != -0.0:
            sirven.append(va[0])
            tot.append(va[0])


    # si es que esta el nodo en la lista entonces hay subtour

    i = '0'
    orden.append(i)
    par = []
    con = []
    print('x', x)
    print('y', y)
    print(sirven)
    while len(sirven) != 0:
        for ruta in sirven:
            # si hay alguna  que llega al 0 y quedan hay subtour...
            if ruta[0] == i and ruta[1] == '0':
                par.append(ruta)
                sirven.remove(ruta)
                if len(sirven) != 0:
                    # condiciones que cambian (tengo que cambiarlo pa siempre)
                    r = arregla(par, sirven, x, y)
                    con.append(r[0])
                    par = r[1]
                    print('Si tiene')
                    # aca revisa si hay otros subtours
                    a = otro(par, sirven, x, y)
                    if a != False:
                        for i in a:
                            con.append(i)
                    return con
                else:
                    #print(orden)
                    print('No tiene')
                    return False

            if ruta[0] == i:
                par.append(ruta)
                sirven.remove(ruta)
                i = ruta[1]
                orden.append(i)


def arregla(orden, subtour, x, y):
    print('orden', orden)
    print('subtour', subtour)
    print('x', x)

    a = orden[-1][0]
    b = ''
    c = ''
    variables = []
    vari = []
    condiciones = {}
    par = orden

    for var in x:
        vari.append(list(var))

    for var in vari:
        var[0] = var[0][2:]
        variables.append(var)

    for i in variables:
        i[0] = i[0].split('_')

    sirve = []

    for ruta in variables:
        if ruta[0] in subtour:
            sirve.append(ruta)

    for ruta in sirve:
        if ruta[1] == 0.0:
            b = ruta[0][1]
            c = ruta[0][0]

    cb = 'y_{}_{}'.format(c, b)
    a0 = 'y_{}_{}'.format(a, '0')
    ab = 'y_{}_{}'.format(a, b)
    c0 = 'y_{}_{}'.format(c, '0')

    # par es el orden hasta ahora que termina en (x,0)
    par.pop()
    par.append(['{}, {}'.format(c,'0')])

    #ir camiando los x e y al final mandar solo un cambio

    """y1 = []
    for var in y:
        if var[0] == cb:
            y1.append((cb, 0.0))
        elif var[0] == a0:
            y1.append((a0, 0.0))
        elif var[0] == ab:
            y1.append((ab, 1.0))
        elif var[0] == c0:
            y1.append((c0, 1.0))
        else:
            y1.append(var)"""

    condiciones[cb] = 0.0
    condiciones[a0] = 0.0
    condiciones[ab] = 1.0
    condiciones[c0] = 1.0

    print(par)

    return (condiciones, par)


def otro(orden, subtour, x, y):
    orden1 = []
    cond = []
    print(subtour)
    # aca buscamos cual es el inicio del subtour
    inicio = subtour[0][0]
    e = subtour[0][0]
    """for ruta in subtour:
        i = ruta[0]
        for rutas in subtour:
            # se repite el inico de una al final de otra
            if i == rutas[1]:
                inicio = i
                e = ruta[1]
                orden1.append(ruta)"""


    while len(subtour) != 0:
        for ruta in subtour:
            if ruta[0] == e and ruta[1] == inicio:
                orden1.append(ruta)
                subtour.remove(ruta)
                if len(subtour) != 0:
                    print('Tiene mas de un subtour')
                    t = arregla(orden, subtour, x, y)
                    cond.append(t[0])
                    ord = t[1]
                    # mas de 2 subtours
                    a = otro(ord, subtour, x, y)
                    if a != False:
                        for i in a:
                            cond.append(i)
                    return cond
                else:
                    # print(orden)
                    print('No tiene mas de un subtour')
                    return False

            elif ruta[0] == e:
                orden1.append(ruta)
                subtour.remove(ruta)
                e = ruta[1]


x = [('x_0_0', -0.0), ('x_0_3', 0.0), ('x_3_0', 0.0), ('x_3_3', -0.0), ('x_3_5', 0.0), ('x_3_37', -0.0), ('x_3_45', 0.0), ('x_3_52', -0.0), ('x_3_60', -0.0), ('x_3_67', -0.0), ('x_3_68', -0.0), ('x_3_83', 4.0), ('x_3_87', -0.0), ('x_3_88', -0.0), ('x_0_5', 0.0), ('x_5_0', 0.0), ('x_5_3', 3.0), ('x_5_5', -0.0), ('x_5_37', -0.0), ('x_5_45', -0.0), ('x_5_52', -0.0), ('x_5_60', -0.0), ('x_5_67', -0.0), ('x_5_68', -0.0), ('x_5_83', 0.0), ('x_5_87', 0.0), ('x_5_88', -0.0), ('x_0_37', 0.0), ('x_37_0', 0.0), ('x_37_3', 0.0), ('x_37_5', 0.0), ('x_37_37', -0.0), ('x_37_45', 0.0), ('x_37_52', -0.0), ('x_37_60', -0.0), ('x_37_67', -0.0), ('x_37_68', 0.0), ('x_37_83', 0.0), ('x_37_87', 0.0), ('x_37_88', 0.0), ('x_0_45', 0.0), ('x_45_0', 0.0), ('x_45_3', 0.0), ('x_45_5', 0.0), ('x_45_37', -0.0), ('x_45_45', -0.0), ('x_45_52', -0.0), ('x_45_60', -0.0), ('x_45_67', -0.0), ('x_45_68', -0.0), ('x_45_83', -0.0), ('x_45_87', 29.0), ('x_45_88', -0.0), ('x_0_52', 0.0), ('x_52_0', 0.0), ('x_52_3', 0.0), ('x_52_5', 0.0), ('x_52_37', 24.0), ('x_52_45', -0.0), ('x_52_52', -0.0), ('x_52_60', -0.0), ('x_52_67', -0.0), ('x_52_68', -0.0), ('x_52_83', 0.0), ('x_52_87', 0.0), ('x_52_88', -0.0), ('x_0_60', 0.0), ('x_60_0', 0.0), ('x_60_3', 0.0), ('x_60_5', 0.0), ('x_60_37', 0.0), ('x_60_45', 0.0), ('x_60_52', 0.0), ('x_60_60', -0.0), ('x_60_67', 0.0), ('x_60_68', 0.0), ('x_60_83', 0.0), ('x_60_87', 0.0), ('x_60_88', 19.0), ('x_0_67', 0.0), ('x_67_0', 0.0), ('x_67_3', 0.0), ('x_67_5', 0.0), ('x_67_37', 0.0), ('x_67_45', 0.0), ('x_67_52', 14.0), ('x_67_60', -0.0), ('x_67_67', -0.0), ('x_67_68', 0.0), ('x_67_83', 0.0), ('x_67_87', 0.0), ('x_67_88', 0.0), ('x_0_68', 0.0), ('x_68_0', 0.0), ('x_68_3', 0.0), ('x_68_5', 0.0), ('x_68_37', -0.0), ('x_68_45', 19.0), ('x_68_52', -0.0), ('x_68_60', -0.0), ('x_68_67', -0.0), ('x_68_68', -0.0), ('x_68_83', 0.0), ('x_68_87', 0.0), ('x_68_88', -0.0), ('x_0_83', 0.0), ('x_83_0', 0.0), ('x_83_3', -0.0), ('x_83_5', -0.0), ('x_83_37', -0.0), ('x_83_45', -0.0), ('x_83_52', -0.0), ('x_83_60', -0.0), ('x_83_67', -0.0), ('x_83_68', -0.0), ('x_83_83', -0.0), ('x_83_87', -0.0), ('x_83_88', -0.0), ('x_0_87', 0.0), ('x_87_0', 0.0), ('x_87_3', -0.0), ('x_87_5', 6.0), ('x_87_37', -0.0), ('x_87_45', -0.0), ('x_87_52', -0.0), ('x_87_60', -0.0), ('x_87_67', -0.0), ('x_87_68', -0.0), ('x_87_83', -0.0), ('x_87_87', -0.0), ('x_87_88', -0.0), ('x_0_88', 0.0), ('x_88_0', 0.0), ('x_88_3', 0.0), ('x_88_5', 0.0), ('x_88_37', -0.0), ('x_88_45', 0.0), ('x_88_52', -0.0), ('x_88_60', -0.0), ('x_88_67', -0.0), ('x_88_68', 11.0), ('x_88_83', 0.0), ('x_88_87', 0.0), ('x_88_88', -0.0)]
y = [('y_0_0', 0.0), ('y_0_3', -0.0), ('y_3_0', -0.0), ('y_3_3', 0.0), ('y_3_5', -0.0), ('y_3_37', -0.0), ('y_3_45', 0.0), ('y_3_52', -0.0), ('y_3_60', -0.0), ('y_3_67', -0.0), ('y_3_68', -0.0), ('y_3_83', 1.0), ('y_3_87', -0.0), ('y_3_88', -0.0), ('y_0_5', -0.0), ('y_5_0', -0.0), ('y_5_3', 1.0), ('y_5_5', 0.0), ('y_5_37', -0.0), ('y_5_45', 0.0), ('y_5_52', -0.0), ('y_5_60', -0.0), ('y_5_67', -0.0), ('y_5_68', -0.0), ('y_5_83', 0.0), ('y_5_87', 0.0), ('y_5_88', -0.0), ('y_0_37', -0.0), ('y_37_0', 0.0), ('y_37_3', -0.0), ('y_37_5', -0.0), ('y_37_37', 0.0), ('y_37_45', -0.0), ('y_37_52', 0.0), ('y_37_60', -0.0), ('y_37_67', 1.0), ('y_37_68', -0.0), ('y_37_83', -0.0), ('y_37_87', -0.0), ('y_37_88', -0.0), ('y_0_45', -0.0), ('y_45_0', -0.0), ('y_45_3', 0.0), ('y_45_5', -0.0), ('y_45_37', -0.0), ('y_45_45', 0.0), ('y_45_52', -0.0), ('y_45_60', -0.0), ('y_45_67', -0.0), ('y_45_68', -0.0), ('y_45_83', -0.0), ('y_45_87', 1.0), ('y_45_88', -0.0), ('y_0_52', -0.0), ('y_52_0', -0.0), ('y_52_3', -0.0), ('y_52_5', -0.0), ('y_52_37', 1.0), ('y_52_45', 0.0), ('y_52_52', 0.0), ('y_52_60', -0.0), ('y_52_67', 0.0), ('y_52_68', -0.0), ('y_52_83', -0.0), ('y_52_87', -0.0), ('y_52_88', -0.0), ('y_0_60', 1.0), ('y_60_0', -0.0), ('y_60_3', -0.0), ('y_60_5', -0.0), ('y_60_37', -0.0), ('y_60_45', -0.0), ('y_60_52', -0.0), ('y_60_60', 0.0), ('y_60_67', 0.0), ('y_60_68', 0.0), ('y_60_83', -0.0), ('y_60_87', -0.0), ('y_60_88', 1.0), ('y_0_67', 0.0), ('y_67_0', -0.0), ('y_67_3', -0.0), ('y_67_5', -0.0), ('y_67_37', -0.0), ('y_67_45', 0.0), ('y_67_52', 1.0), ('y_67_60', -0.0), ('y_67_67', 0.0), ('y_67_68', -0.0), ('y_67_83', -0.0), ('y_67_87', -0.0), ('y_67_88', 0.0), ('y_0_68', -0.0), ('y_68_0', -0.0), ('y_68_3', -0.0), ('y_68_5', -0.0), ('y_68_37', -0.0), ('y_68_45', 1.0), ('y_68_52', -0.0), ('y_68_60', -0.0), ('y_68_67', -0.0), ('y_68_68', 0.0), ('y_68_83', -0.0), ('y_68_87', -0.0), ('y_68_88', 0.0), ('y_0_83', -0.0), ('y_83_0', 1.0), ('y_83_3', 0.0), ('y_83_5', 0.0), ('y_83_37', -0.0), ('y_83_45', -0.0), ('y_83_52', -0.0), ('y_83_60', -0.0), ('y_83_67', -0.0), ('y_83_68', -0.0), ('y_83_83', 0.0), ('y_83_87', -0.0), ('y_83_88', -0.0), ('y_0_87', -0.0), ('y_87_0', -0.0), ('y_87_3', -0.0), ('y_87_5', 1.0), ('y_87_37', -0.0), ('y_87_45', 0.0), ('y_87_52', -0.0), ('y_87_60', -0.0), ('y_87_67', -0.0), ('y_87_68', -0.0), ('y_87_83', 0.0), ('y_87_87', 0.0), ('y_87_88', -0.0), ('y_0_88', -0.0), ('y_88_0', -0.0), ('y_88_3', -0.0), ('y_88_5', -0.0), ('y_88_37', -0.0), ('y_88_45', -0.0), ('y_88_52', -0.0), ('y_88_60', -0.0), ('y_88_67', 0.0), ('y_88_68', 1.0), ('y_88_83', -0.0), ('y_88_87', -0.0), ('y_88_88', 0.0)]
sirven = [['3', '83'], ['5', '3'], ['37', '67'], ['45', '87'], ['52', '37'], ['0', '60'], ['60', '88'], ['67', '52'], ['68', '45'], ['83', '0'], ['87', '5'], ['88', '68']]

orden = [['0', '60'], ['60', '88'], ['88', '68'], ['68', '45'], ['45', '87'], ['87', '5'], ['5', '3'], ['3', '83'], ['83', '0']]
subtour = [['37', '67'], ['52', '37'], ['67', '52']]