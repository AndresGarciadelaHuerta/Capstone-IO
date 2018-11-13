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
    while len(sirven) != 0:
        for ruta in sirven:
            # si hay alguna  que llega al 0 y quedan hay subtour...
            if ruta[0] == i and ruta[1] == '0':
                par.append(ruta)
                sirven.remove(ruta)
                if len(sirven) != 0:
                    print('Si tiene')
                    #r = arregla(par, sirven, x, y)
                    #con.append(r[0])
                    #par = r[1]

                    # aca revisa si hay otros subtours
                    #print(par)
                    a = otro(par, sirven, x, y)
                    #print('a', a)
                    if a != False:
                        for i in a:
                            con.append(i)
                    final = {}
                    for dict in con:
                        for cambio in dict.keys():
                            final[cambio] = dict[cambio]
                    print(final)

                    return final
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
        if ruta[1] == 0.0 or ruta[1] == -0.0:
            b = ruta[0][1]
            c = ruta[0][0]
            break

    cb = 'y_{}_{}'.format(c, b)
    a0 = 'y_{}_{}'.format(a, '0')
    ab = 'y_{}_{}'.format(a, b)
    c0 = 'y_{}_{}'.format(c, '0')

    # par es el orden hasta ahora que termina en (x,0)
    par.pop()
    par.append(['{}'.format(a), '{}'.format(b)])
    par.append(['{}'.format(c), '{}'.format('0')])


    condiciones[cb] = 0.0
    condiciones[a0] = 0.0
    condiciones[ab] = 1.0
    condiciones[c0] = 1.0

    v = (condiciones, par)
    return v


def otro(orden, subtoura, x, y):
    subtour = subtoura
    orden1 = []
    cond = []
    ordenfin = []
    # aca buscamos cual es el inicio del subtour
    inicio = subtour[0][0]
    e = subtour[0][0]

    inin = False
    # armamos el subtour
    for subto in subtour:
        if subto[0] == '0':
            inin = True
            break
        else:
            pass
    if not inin:
        ini = subtour[0][0]
    else:
        ini = '0'
    efe = subtour[0][0]
    while len(subtour) != 0:
        print(subtour)
        for ruta in subtour:
            if ruta[0] == efe and ruta[1] == ini:
                ordenfin.append(ruta)
                subtour.remove(ruta)
                print(ordenfin)
                t = arregla(orden, ordenfin, x, y)
                cond.append(t[0])
                orden = t[1]

                if len(subtour) != 0:
                    print('Tiene otro')
                    otro(orden, subtour, x, y)

                else:
                    # print(orden)
                    print('No tiene mas de un subtour')
                break

            elif ruta[0] == efe:
                ordenfin.append(ruta)
                subtour.remove(ruta)
                efe = ruta[1]
    """

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
                    e = ruta[1]"""

    return cond



"""
x = [('x_0_0', -0.0), ('x_0_12', 0.0), ('x_12_0', 0.0), ('x_12_12', -0.0), ('x_12_16', 0.0), ('x_12_17', 0.0), ('x_12_28', 10.0), ('x_12_31', -0.0), ('x_12_32', -0.0), ('x_12_36', 0.0), ('x_12_38', -0.0), ('x_12_48', -0.0), ('x_12_58', -0.0), ('x_0_16', 0.0), ('x_16_0', 0.0), ('x_16_12', -0.0), ('x_16_16', -0.0), ('x_16_17', -0.0), ('x_16_28', -0.0), ('x_16_31', -0.0), ('x_16_32', -0.0), ('x_16_36', 0.0), ('x_16_38', -0.0), ('x_16_48', -0.0), ('x_16_58', -0.0), ('x_0_17', 0.0), ('x_17_0', 0.0), ('x_17_12', -0.0), ('x_17_16', 19.0), ('x_17_17', -0.0), ('x_17_28', -0.0), ('x_17_31', -0.0), ('x_17_32', -0.0), ('x_17_36', 0.0), ('x_17_38', -0.0), ('x_17_48', -0.0), ('x_17_58', -0.0), ('x_0_28', 0.0), ('x_28_0', 0.0), ('x_28_12', -0.0), ('x_28_16', 0.0), ('x_28_17', 0.0), ('x_28_28', -0.0), ('x_28_31', -0.0), ('x_28_32', -0.0), ('x_28_36', 0.0), ('x_28_38', -0.0), ('x_28_48', -0.0), ('x_28_58', -0.0), ('x_0_31', 0.0), ('x_31_0', 0.0), ('x_31_12', -0.0), ('x_31_16', -0.0), ('x_31_17', 0.0), ('x_31_28', 0.0), ('x_31_31', -0.0), ('x_31_32', -0.0), ('x_31_36', 0.0), ('x_31_38', -0.0), ('x_31_48', -0.0), ('x_31_58', 16.0), ('x_0_32', 0.0), ('x_32_0', 0.0), ('x_32_12', -0.0), ('x_32_16', -0.0), ('x_32_17', -0.0), ('x_32_28', -0.0), ('x_32_31', -0.0), ('x_32_32', -0.0), ('x_32_36', 3.0), ('x_32_38', -0.0), ('x_32_48', -0.0), ('x_32_58', -0.0), ('x_0_36', 0.0), ('x_36_0', 0.0), ('x_36_12', -0.0), ('x_36_16', -0.0), ('x_36_17', -0.0), ('x_36_28', -0.0), ('x_36_31', -0.0), ('x_36_32', -0.0), ('x_36_36', -0.0), ('x_36_38', -0.0), ('x_36_48', -0.0), ('x_36_58', -0.0), ('x_0_38', 0.0), ('x_38_0', 0.0), ('x_38_12', 0.0), ('x_38_16', 0.0), ('x_38_17', 0.0), ('x_38_28', 0.0), ('x_38_31', 15.0), ('x_38_32', 0.0), ('x_38_36', 0.0), ('x_38_38', -0.0), ('x_38_48', -0.0), ('x_38_58', 0.0), ('x_0_48', 0.0), ('x_48_0', 0.0), ('x_48_12', 0.0), ('x_48_16', 0.0), ('x_48_17', 0.0), ('x_48_28', 0.0), ('x_48_31', 0.0), ('x_48_32', 0.0), ('x_48_36', 0.0), ('x_48_38', 12.0), ('x_48_48', -0.0), ('x_48_58', 0.0), ('x_0_58', 0.0), ('x_58_0', 0.0), ('x_58_12', 0.0), ('x_58_16', 0.0), ('x_58_17', 0.0), ('x_58_28', -0.0), ('x_58_31', 0.0), ('x_58_32', 30.0), ('x_58_36', 0.0), ('x_58_38', -0.0), ('x_58_48', -0.0), ('x_58_58', -0.0)]
y = [('y_0_0', 0.0), ('y_0_12', -0.0), ('y_12_0', -0.0), ('y_12_12', 0.0), ('y_12_16', -0.0), ('y_12_17', -0.0), ('y_12_28', 1.0), ('y_12_31', -0.0), ('y_12_32', -0.0), ('y_12_36', 0.0), ('y_12_38', -0.0), ('y_12_48', -0.0), ('y_12_58', -0.0), ('y_0_16', -0.0), ('y_16_0', -0.0), ('y_16_12', -0.0), ('y_16_16', 0.0), ('y_16_17', 1.0), ('y_16_28', -0.0), ('y_16_31', -0.0), ('y_16_32', -0.0), ('y_16_36', -0.0), ('y_16_38', -0.0), ('y_16_48', -0.0), ('y_16_58', -0.0), ('y_0_17', -0.0), ('y_17_0', -0.0), ('y_17_12', -0.0), ('y_17_16', 1.0), ('y_17_17', 0.0), ('y_17_28', -0.0), ('y_17_31', -0.0), ('y_17_32', -0.0), ('y_17_36', -0.0), ('y_17_38', -0.0), ('y_17_48', 0.0), ('y_17_58', -0.0), ('y_0_28', -0.0), ('y_28_0', -0.0), ('y_28_12', 1.0), ('y_28_16', -0.0), ('y_28_17', -0.0), ('y_28_28', 0.0), ('y_28_31', -0.0), ('y_28_32', -0.0), ('y_28_36', 0.0), ('y_28_38', -0.0), ('y_28_48', -0.0), ('y_28_58', 0.0), ('y_0_31', -0.0), ('y_31_0', -0.0), ('y_31_12', -0.0), ('y_31_16', -0.0), ('y_31_17', -0.0), ('y_31_28', -0.0), ('y_31_31', 0.0), ('y_31_32', 0.0), ('y_31_36', -0.0), ('y_31_38', -0.0), ('y_31_48', -0.0), ('y_31_58', 1.0), ('y_0_32', -0.0), ('y_32_0', 0.0), ('y_32_12', -0.0), ('y_32_16', -0.0), ('y_32_17', -0.0), ('y_32_28', -0.0), ('y_32_31', -0.0), ('y_32_32', 0.0), ('y_32_36', 1.0), ('y_32_38', -0.0), ('y_32_48', -0.0), ('y_32_58', 0.0), ('y_0_36', -0.0), ('y_36_0', 1.0), ('y_36_12', -0.0), ('y_36_16', -0.0), ('y_36_17', -0.0), ('y_36_28', -0.0), ('y_36_31', -0.0), ('y_36_32', 0.0), ('y_36_36', 0.0), ('y_36_38', -0.0), ('y_36_48', -0.0), ('y_36_58', -0.0), ('y_0_38', 0.0), ('y_38_0', -0.0), ('y_38_12', -0.0), ('y_38_16', -0.0), ('y_38_17', -0.0), ('y_38_28', -0.0), ('y_38_31', 1.0), ('y_38_32', 0.0), ('y_38_36', -0.0), ('y_38_38', 0.0), ('y_38_48', 0.0), ('y_38_58', -0.0), ('y_0_48', 1.0), ('y_48_0', -0.0), ('y_48_12', -0.0), ('y_48_16', -0.0), ('y_48_17', 0.0), ('y_48_28', -0.0), ('y_48_31', -0.0), ('y_48_32', -0.0), ('y_48_36', 0.0), ('y_48_38', 1.0), ('y_48_48', 0.0), ('y_48_58', -0.0), ('y_0_58', -0.0), ('y_58_0', -0.0), ('y_58_12', -0.0), ('y_58_16', -0.0), ('y_58_17', -0.0), ('y_58_28', 0.0), ('y_58_31', 0.0), ('y_58_32', 1.0), ('y_58_36', -0.0), ('y_58_38', -0.0), ('y_58_48', -0.0), ('y_58_58', 0.0)]
sirven = [['12', '28'], ['16', '17'], ['17', '16'], ['28', '12'], ['31', '58'], ['32', '36'], ['36', '0'], ['38', '31'], ['0', '48'], ['48', '38'], ['58', '32']]




identifica(x,y, sirven)"""

