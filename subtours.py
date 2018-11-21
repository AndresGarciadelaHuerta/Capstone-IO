'''
y _i,j = 1 si existe la ruta
x = carga en cada arco
'''

# cambiar valor de FO cuando entra a subtour!


# identifica si hay subtour
def identifica(m):
    x = []
    y = []
    sirven = []
    sirvene = []
    variables = []
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
            sirvene.append(va[0])
            tot.append(va[0])
            

#def identifica(x,y,sirven):


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
                    #print('Si tiene')
                    ##print(sirven)##
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

                    return final

                else:
                    #print(orden)
                    #print('No tiene')
                    return False

            if ruta[0] == i:
                par.append(ruta)
                sirven.remove(ruta)
                i = ruta[1]
                orden.append(i)


# elimina los arcos que no se usan y crea los otros que si se necesitan
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
    #print(condiciones)
    ##print(v[0])##
    if cb == 'y__':
        del condiciones[cb]
        return (condiciones, par)
    return v

# funcion recursiva que en cuentra si hay mas subtours y los arregla hasta
# que no quede ninguno
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
        for ruta in subtour:
            if ruta[0] == efe and ruta[1] == ini:
                ordenfin.append(ruta)
                subtour.remove(ruta)
                ##print('arr',ordenfin)##
                t = arregla(orden, ordenfin, x, y)
                cond.append(t[0])
                orden = t[1]

                if len(subtour) != 0:
                    ##print('su', subtour)##
                    #print('Tiene otro')
                    ce = otro(orden, subtour, x, y)
                    for k in ce:
                        cond.append(k)

                else:
                    pass
                    # print(orden)
                    #print('No tiene mas de un subtour')
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




'''
sub de 2
x = [('x_0_0', -0.0), ('x_0_12', 0.0), ('x_12_0', 0.0), ('x_12_12', -0.0), ('x_12_16', 0.0), ('x_12_17', 0.0), ('x_12_28', 10.0), ('x_12_31', -0.0), ('x_12_32', -0.0), ('x_12_36', 0.0), ('x_12_38', -0.0), ('x_12_48', -0.0), ('x_12_58', -0.0), ('x_0_16', 0.0), ('x_16_0', 0.0), ('x_16_12', -0.0), ('x_16_16', -0.0), ('x_16_17', -0.0), ('x_16_28', -0.0), ('x_16_31', -0.0), ('x_16_32', -0.0), ('x_16_36', 0.0), ('x_16_38', -0.0), ('x_16_48', -0.0), ('x_16_58', -0.0), ('x_0_17', 0.0), ('x_17_0', 0.0), ('x_17_12', -0.0), ('x_17_16', 19.0), ('x_17_17', -0.0), ('x_17_28', -0.0), ('x_17_31', -0.0), ('x_17_32', -0.0), ('x_17_36', 0.0), ('x_17_38', -0.0), ('x_17_48', -0.0), ('x_17_58', -0.0), ('x_0_28', 0.0), ('x_28_0', 0.0), ('x_28_12', -0.0), ('x_28_16', 0.0), ('x_28_17', 0.0), ('x_28_28', -0.0), ('x_28_31', -0.0), ('x_28_32', -0.0), ('x_28_36', 0.0), ('x_28_38', -0.0), ('x_28_48', -0.0), ('x_28_58', -0.0), ('x_0_31', 0.0), ('x_31_0', 0.0), ('x_31_12', -0.0), ('x_31_16', -0.0), ('x_31_17', 0.0), ('x_31_28', 0.0), ('x_31_31', -0.0), ('x_31_32', -0.0), ('x_31_36', 0.0), ('x_31_38', -0.0), ('x_31_48', -0.0), ('x_31_58', 16.0), ('x_0_32', 0.0), ('x_32_0', 0.0), ('x_32_12', -0.0), ('x_32_16', -0.0), ('x_32_17', -0.0), ('x_32_28', -0.0), ('x_32_31', -0.0), ('x_32_32', -0.0), ('x_32_36', 3.0), ('x_32_38', -0.0), ('x_32_48', -0.0), ('x_32_58', -0.0), ('x_0_36', 0.0), ('x_36_0', 0.0), ('x_36_12', -0.0), ('x_36_16', -0.0), ('x_36_17', -0.0), ('x_36_28', -0.0), ('x_36_31', -0.0), ('x_36_32', -0.0), ('x_36_36', -0.0), ('x_36_38', -0.0), ('x_36_48', -0.0), ('x_36_58', -0.0), ('x_0_38', 0.0), ('x_38_0', 0.0), ('x_38_12', 0.0), ('x_38_16', 0.0), ('x_38_17', 0.0), ('x_38_28', 0.0), ('x_38_31', 15.0), ('x_38_32', 0.0), ('x_38_36', 0.0), ('x_38_38', -0.0), ('x_38_48', -0.0), ('x_38_58', 0.0), ('x_0_48', 0.0), ('x_48_0', 0.0), ('x_48_12', 0.0), ('x_48_16', 0.0), ('x_48_17', 0.0), ('x_48_28', 0.0), ('x_48_31', 0.0), ('x_48_32', 0.0), ('x_48_36', 0.0), ('x_48_38', 12.0), ('x_48_48', -0.0), ('x_48_58', 0.0), ('x_0_58', 0.0), ('x_58_0', 0.0), ('x_58_12', 0.0), ('x_58_16', 0.0), ('x_58_17', 0.0), ('x_58_28', -0.0), ('x_58_31', 0.0), ('x_58_32', 30.0), ('x_58_36', 0.0), ('x_58_38', -0.0), ('x_58_48', -0.0), ('x_58_58', -0.0)]
y = [('y_0_0', 0.0), ('y_0_12', -0.0), ('y_12_0', -0.0), ('y_12_12', 0.0), ('y_12_16', -0.0), ('y_12_17', -0.0), ('y_12_28', 1.0), ('y_12_31', -0.0), ('y_12_32', -0.0), ('y_12_36', 0.0), ('y_12_38', -0.0), ('y_12_48', -0.0), ('y_12_58', -0.0), ('y_0_16', -0.0), ('y_16_0', -0.0), ('y_16_12', -0.0), ('y_16_16', 0.0), ('y_16_17', 1.0), ('y_16_28', -0.0), ('y_16_31', -0.0), ('y_16_32', -0.0), ('y_16_36', -0.0), ('y_16_38', -0.0), ('y_16_48', -0.0), ('y_16_58', -0.0), ('y_0_17', -0.0), ('y_17_0', -0.0), ('y_17_12', -0.0), ('y_17_16', 1.0), ('y_17_17', 0.0), ('y_17_28', -0.0), ('y_17_31', -0.0), ('y_17_32', -0.0), ('y_17_36', -0.0), ('y_17_38', -0.0), ('y_17_48', 0.0), ('y_17_58', -0.0), ('y_0_28', -0.0), ('y_28_0', -0.0), ('y_28_12', 1.0), ('y_28_16', -0.0), ('y_28_17', -0.0), ('y_28_28', 0.0), ('y_28_31', -0.0), ('y_28_32', -0.0), ('y_28_36', 0.0), ('y_28_38', -0.0), ('y_28_48', -0.0), ('y_28_58', 0.0), ('y_0_31', -0.0), ('y_31_0', -0.0), ('y_31_12', -0.0), ('y_31_16', -0.0), ('y_31_17', -0.0), ('y_31_28', -0.0), ('y_31_31', 0.0), ('y_31_32', 0.0), ('y_31_36', -0.0), ('y_31_38', -0.0), ('y_31_48', -0.0), ('y_31_58', 1.0), ('y_0_32', -0.0), ('y_32_0', 0.0), ('y_32_12', -0.0), ('y_32_16', -0.0), ('y_32_17', -0.0), ('y_32_28', -0.0), ('y_32_31', -0.0), ('y_32_32', 0.0), ('y_32_36', 1.0), ('y_32_38', -0.0), ('y_32_48', -0.0), ('y_32_58', 0.0), ('y_0_36', -0.0), ('y_36_0', 1.0), ('y_36_12', -0.0), ('y_36_16', -0.0), ('y_36_17', -0.0), ('y_36_28', -0.0), ('y_36_31', -0.0), ('y_36_32', 0.0), ('y_36_36', 0.0), ('y_36_38', -0.0), ('y_36_48', -0.0), ('y_36_58', -0.0), ('y_0_38', 0.0), ('y_38_0', -0.0), ('y_38_12', -0.0), ('y_38_16', -0.0), ('y_38_17', -0.0), ('y_38_28', -0.0), ('y_38_31', 1.0), ('y_38_32', 0.0), ('y_38_36', -0.0), ('y_38_38', 0.0), ('y_38_48', 0.0), ('y_38_58', -0.0), ('y_0_48', 1.0), ('y_48_0', -0.0), ('y_48_12', -0.0), ('y_48_16', -0.0), ('y_48_17', 0.0), ('y_48_28', -0.0), ('y_48_31', -0.0), ('y_48_32', -0.0), ('y_48_36', 0.0), ('y_48_38', 1.0), ('y_48_48', 0.0), ('y_48_58', -0.0), ('y_0_58', -0.0), ('y_58_0', -0.0), ('y_58_12', -0.0), ('y_58_16', -0.0), ('y_58_17', -0.0), ('y_58_28', 0.0), ('y_58_31', 0.0), ('y_58_32', 1.0), ('y_58_36', -0.0), ('y_58_38', -0.0), ('y_58_48', -0.0), ('y_58_58', 0.0)]


sirven = [['12', '28'], ['16', '17'], ['17', '16'], ['28', '12'], ['31', 
                                                                   '58'], 
          ['32', '36'], ['36', '0'], ['38', '31'], ['0', '48'], ['48', 
                                                                 '38'], 
          ['58', '32']]





sub largo
x = [('x_0_0', -0.0), ('x_0_3', 0.0), ('x_3_0', 0.0), ('x_3_3', -0.0),
    ('x_3_5', 0.0), ('x_3_45', 0.0), ('x_3_60', -0.0), ('x_3_67', 0.0), ('x_3_68', -0.0), ('x_3_83', 17.0), ('x_3_87', 0.0), ('x_3_90', 0.0), ('x_0_5', 0.0), ('x_5_0', 0.0), ('x_5_3', -0.0), ('x_5_5', -0.0), ('x_5_45', -0.0), ('x_5_60', 0.0), ('x_5_67', 0.0), ('x_5_68', -0.0), ('x_5_83', 0.0), ('x_5_87', 13.0), ('x_5_90', -0.0), ('x_0_45', 0.0), ('x_45_0', 0.0), ('x_45_3', -0.0), ('x_45_5', 25.0), ('x_45_45', -0.0), ('x_45_60', 0.0), ('x_45_67', 0.0), ('x_45_68', -0.0), ('x_45_83', 0.0), ('x_45_87', 0.0), ('x_45_90', 0.0), ('x_0_60', 0.0), ('x_60_0', 0.0), ('x_60_3', -0.0), ('x_60_5', 0.0), ('x_60_45', -0.0), ('x_60_60', -0.0), ('x_60_67', 4.0), ('x_60_68', -0.0), ('x_60_83', -0.0), ('x_60_87', 0.0), ('x_60_90', -0.0), ('x_0_67', 0.0), ('x_67_0', 0.0), ('x_67_3', 0.0), ('x_67_5', 0.0), ('x_67_45', 17.0), ('x_67_60', -0.0), ('x_67_67', -0.0), ('x_67_68', 0.0), ('x_67_83', 0.0), ('x_67_87', 0.0), ('x_67_90', -0.0), ('x_0_68', 0.0), ('x_68_0', 0.0), ('x_68_3', 0.0), ('x_68_5', 0.0), ('x_68_45', -0.0), ('x_68_60', 2.0), ('x_68_67', -0.0), ('x_68_68', -0.0), ('x_68_83', -0.0), ('x_68_87', 0.0), ('x_68_90', -0.0), ('x_0_83', 0.0), ('x_83_0', 0.0), ('x_83_3', -0.0), ('x_83_5', 0.0), ('x_83_45', 0.0), ('x_83_60', 0.0), ('x_83_67', 0.0), ('x_83_68', -0.0), ('x_83_83', -0.0), ('x_83_87', 0.0), ('x_83_90', 16.0), ('x_0_87', 0.0), ('x_87_0', 0.0), ('x_87_3', -0.0), ('x_87_5', 0.0), ('x_87_45', -0.0), ('x_87_60', -0.0), ('x_87_67', -0.0), ('x_87_68', -0.0), ('x_87_83', -0.0), ('x_87_87', -0.0), ('x_87_90', -0.0), ('x_0_90', 0.0), ('x_90_0', 0.0), ('x_90_3', -0.0), ('x_90_5', 0.0), ('x_90_45', -0.0), ('x_90_60', -0.0), ('x_90_67', -0.0), ('x_90_68', -0.0), ('x_90_83', -0.0), ('x_90_87', -0.0), ('x_90_90', -0.0)]
y = [('y_0_0', 0.0), ('y_0_3', 1.0), ('y_3_0', -0.0), ('y_3_3', 0.0),
    ('y_3_5', -0.0), ('y_3_45', -0.0), ('y_3_60', -0.0), ('y_3_67', -0.0), ('y_3_68', -0.0), ('y_3_83', 1.0), ('y_3_87', -0.0), ('y_3_90', 0.0), ('y_0_5', -0.0), ('y_5_0', 0.0), ('y_5_3', 0.0), ('y_5_5', 0.0), ('y_5_45', -0.0), ('y_5_60', -0.0), ('y_5_67', -0.0), ('y_5_68', 0.0), ('y_5_83', 0.0), ('y_5_87', 1.0), ('y_5_90', -0.0), ('y_0_45', -0.0), ('y_45_0', -0.0), ('y_45_3', -0.0), ('y_45_5', 1.0), ('y_45_45', 0.0), ('y_45_60', -0.0), ('y_45_67', -0.0), ('y_45_68', -0.0), ('y_45_83', -0.0), ('y_45_87', 0.0), ('y_45_90', 0.0), ('y_0_60', 0.0), ('y_60_0', -0.0), ('y_60_3', -0.0), ('y_60_5', -0.0), ('y_60_45', -0.0), ('y_60_60', 0.0), ('y_60_67', 1.0), ('y_60_68', -0.0), ('y_60_83', -0.0), ('y_60_87', -0.0), ('y_60_90', -0.0), ('y_0_67', -0.0), ('y_67_0', -0.0), ('y_67_3', -0.0), ('y_67_5', -0.0), ('y_67_45', 1.0), ('y_67_60', 0.0), ('y_67_67', 0.0), ('y_67_68', 0.0), ('y_67_83', -0.0), ('y_67_87', -0.0), ('y_67_90', -0.0), ('y_0_68', -0.0), ('y_68_0', -0.0), ('y_68_3', -0.0), ('y_68_5', -0.0), ('y_68_45', -0.0), ('y_68_60', 1.0), ('y_68_67', 0.0), ('y_68_68', 0.0), ('y_68_83', -0.0), ('y_68_87', 0.0), ('y_68_90', -0.0), ('y_0_83', -0.0), ('y_83_0', -0.0), ('y_83_3', 0.0), ('y_83_5', 0.0), ('y_83_45', -0.0), ('y_83_60', -0.0), ('y_83_67', -0.0), ('y_83_68', -0.0), ('y_83_83', 0.0), ('y_83_87', -0.0), ('y_83_90', 1.0), ('y_0_87', -0.0), ('y_87_0', -0.0), ('y_87_3', -0.0), ('y_87_5', 0.0), ('y_87_45', 0.0), ('y_87_60', -0.0), ('y_87_67', -0.0), ('y_87_68', 1.0), ('y_87_83', -0.0), ('y_87_87', 0.0), ('y_87_90', -0.0), ('y_0_90', -0.0), ('y_90_0', 1.0), ('y_90_3', -0.0), ('y_90_5', -0.0), ('y_90_45', -0.0), ('y_90_60', -0.0), ('y_90_67', -0.0), ('y_90_68', -0.0), ('y_90_83', -0.0), ('y_90_87', -0.0), ('y_90_90', 0.0)]
sirven = [['0', '3'], ['3', '83'], ['5', '87'], ['45', '5'], ['60', '67'],
         ['67', '45'], ['68', '60'], ['83', '90'], ['87', '68'], ['90', '0']]


sub de 3
x = [('x_0_0', -0.0), ('x_0_8', 0.0), ('x_8_0', 0.0), ('x_8_8', -0.0), 
    ('x_8_13', -0.0), ('x_8_41', -0.0), ('x_8_43', -0.0), ('x_8_64', -0.0), ('x_8_65', -0.0), ('x_8_69', -0.0), ('x_8_74', -0.0), ('x_8_78', -0.0), ('x_8_81', -0.0), ('x_0_13', 0.0), ('x_13_0', 0.0), ('x_13_8', 0.0), ('x_13_13', -0.0), ('x_13_41', 0.0), ('x_13_43', -0.0), ('x_13_64', 0.0), ('x_13_65', -0.0), ('x_13_69', 20.0), ('x_13_74', -0.0), ('x_13_78', -0.0), ('x_13_81', -0.0), ('x_0_41', 0.0), ('x_41_0', 0.0), ('x_41_8', 4.0), ('x_41_13', -0.0), ('x_41_41', -0.0), ('x_41_43', -0.0), ('x_41_64', -0.0), ('x_41_65', -0.0), ('x_41_69', -0.0), ('x_41_74', -0.0), ('x_41_78', -0.0), ('x_41_81', -0.0), ('x_0_43', 0.0), ('x_43_0', 0.0), ('x_43_8', 0.0), ('x_43_13', -0.0), ('x_43_41', 0.0), ('x_43_43', -0.0), ('x_43_64', -0.0), ('x_43_65', -0.0), ('x_43_69', 0.0), ('x_43_74', 21.0), ('x_43_78', -0.0), ('x_43_81', -0.0), ('x_0_64', 0.0), ('x_64_0', 0.0), ('x_64_8', 0.0), ('x_64_13', -0.0), ('x_64_41', 0.0), ('x_64_43', -0.0), ('x_64_64', -0.0), ('x_64_65', -0.0), ('x_64_69', 0.0), ('x_64_74', -0.0), ('x_64_78', -0.0), ('x_64_81', -0.0), ('x_0_65', 0.0), ('x_65_0', 0.0), ('x_65_8', 0.0), ('x_65_13', -0.0), ('x_65_41', -0.0), ('x_65_43', 0.0), ('x_65_64', -0.0), ('x_65_65', -0.0), ('x_65_69', 0.0), ('x_65_74', 0.0), ('x_65_78', 0.0), ('x_65_81', 26.0), ('x_0_69', 0.0), ('x_69_0', 0.0), ('x_69_8', 0.0), ('x_69_13', -0.0), ('x_69_41', 21.0), ('x_69_43', -0.0), ('x_69_64', -0.0), ('x_69_65', -0.0), ('x_69_69', -0.0), ('x_69_74', -0.0), ('x_69_78', -0.0), ('x_69_81', -0.0), ('x_0_74', 0.0), ('x_74_0', 0.0), ('x_74_8', 0.0), ('x_74_13', -0.0), ('x_74_41', 0.0), ('x_74_43', -0.0), ('x_74_64', 15.0), ('x_74_65', -0.0), ('x_74_69', 0.0), ('x_74_74', -0.0), ('x_74_78', -0.0), ('x_74_81', -0.0), ('x_0_78', 0.0), ('x_78_0', 0.0), ('x_78_8', 0.0), ('x_78_13', 25.0), ('x_78_41', 0.0), ('x_78_43', -0.0), ('x_78_64', 0.0), ('x_78_65', -0.0), ('x_78_69', 0.0), ('x_78_74', -0.0), ('x_78_78', -0.0), ('x_78_81', -0.0), ('x_0_81', 0.0), ('x_81_0', 0.0), ('x_81_8', 0.0), ('x_81_13', 0.0), ('x_81_41', 0.0), ('x_81_43', -0.0), ('x_81_64', 0.0), ('x_81_65', -0.0), ('x_81_69', 0.0), ('x_81_74', 0.0), ('x_81_78', 53.0), ('x_81_81', -0.0)]
y = [('y_0_0', 0.0), ('y_0_8', -0.0), ('y_8_0', 1.0), ('y_8_8', 0.0), 
    ('y_8_13', -0.0), ('y_8_41', 0.0), ('y_8_43', -0.0), ('y_8_64', -0.0), ('y_8_65', -0.0), ('y_8_69', -0.0), ('y_8_74', -0.0), ('y_8_78', -0.0), ('y_8_81', -0.0), ('y_0_13', -0.0), ('y_13_0', -0.0), ('y_13_8', -0.0), ('y_13_13', 0.0), ('y_13_41', 0.0), ('y_13_43', -0.0), ('y_13_64', -0.0), ('y_13_65', -0.0), ('y_13_69', 1.0), ('y_13_74', -0.0), ('y_13_78', 0.0), ('y_13_81', -0.0), ('y_0_41', -0.0), ('y_41_0', 0.0), ('y_41_8', 1.0), ('y_41_13', -0.0), ('y_41_41', 0.0), ('y_41_43', -0.0), ('y_41_64', -0.0), ('y_41_65', -0.0), ('y_41_69', -0.0), ('y_41_74', -0.0), ('y_41_78', -0.0), ('y_41_81', -0.0), ('y_0_43', 0.0), ('y_43_0', -0.0), ('y_43_8', -0.0), ('y_43_13', -0.0), ('y_43_41', -0.0), ('y_43_43', 0.0), ('y_43_64', -0.0), ('y_43_65', 0.0), ('y_43_69', -0.0), ('y_43_74', 1.0), ('y_43_78', -0.0), ('y_43_81', -0.0), ('y_0_64', -0.0), ('y_64_0', 0.0), ('y_64_8', 0.0), ('y_64_13', -0.0), ('y_64_41', -0.0), ('y_64_43', 1.0), ('y_64_64', 0.0), ('y_64_65', -0.0), ('y_64_69', -0.0), ('y_64_74', 0.0), ('y_64_78', -0.0), ('y_64_81', -0.0), ('y_0_65', 1.0), ('y_65_0', -0.0), ('y_65_8', -0.0), ('y_65_13', -0.0), ('y_65_41', -0.0), ('y_65_43', 0.0), ('y_65_64', -0.0), ('y_65_65', 0.0), ('y_65_69', -0.0), ('y_65_74', -0.0), ('y_65_78', -0.0), ('y_65_81', 1.0), ('y_0_69', 0.0), ('y_69_0', -0.0), ('y_69_8', -0.0), ('y_69_13', -0.0), ('y_69_41', 1.0), ('y_69_43', -0.0), ('y_69_64', -0.0), ('y_69_65', -0.0), ('y_69_69', 0.0), ('y_69_74', -0.0), ('y_69_78', -0.0), ('y_69_81', -0.0), ('y_0_74', -0.0), ('y_74_0', -0.0), ('y_74_8', -0.0), ('y_74_13', -0.0), ('y_74_41', -0.0), ('y_74_43', 0.0), ('y_74_64', 1.0), ('y_74_65', -0.0), ('y_74_69', -0.0), ('y_74_74', 0.0), ('y_74_78', -0.0), ('y_74_81', -0.0), ('y_0_78', -0.0), ('y_78_0', -0.0), ('y_78_8', -0.0), ('y_78_13', 1.0), ('y_78_41', -0.0), ('y_78_43', -0.0), ('y_78_64', -0.0), ('y_78_65', -0.0), ('y_78_69', -0.0), ('y_78_74', -0.0), ('y_78_78', 0.0), ('y_78_81', 0.0), ('y_0_81', 0.0), ('y_81_0', -0.0), ('y_81_8', -0.0), ('y_81_13', 0.0), ('y_81_41', -0.0), ('y_81_43', -0.0), ('y_81_64', -0.0), ('y_81_65', -0.0), ('y_81_69', -0.0), ('y_81_74', -0.0), ('y_81_78', 1.0), ('y_81_81', 0.0)]
sirven = [['8', '0'], ['13', '69'], ['41', '8'], ['43', '74'], ['64', '43'], 
    ['0', '65'], ['65', '81'], ['69', '41'], ['74', '64'], ['78', '13'], ['81', '78']]
    
    
    
#dos subtours
x = [('x_0_0', -0.0), ('x_0_7', 0.0), ('x_7_0', 0.0), ('x_7_7', -0.0), 
    ('x_7_15', -0.0), ('x_7_18', -0.0), ('x_7_20', -0.0), ('x_7_25', -0.0), ('x_7_27', -0.0), ('x_7_35', -0.0), ('x_7_40', -0.0), ('x_7_46', -0.0), ('x_7_56', -0.0), ('x_7_57', -0.0), ('x_7_66', -0.0), ('x_7_76', -0.0), ('x_7_91', -0.0), ('x_0_15', 0.0), ('x_15_0', 0.0), ('x_15_7', 0.0), ('x_15_15', -0.0), ('x_15_18', 0.0), ('x_15_20', -0.0), ('x_15_25', -0.0), ('x_15_27', -0.0), ('x_15_35', 0.0), ('x_15_40', -0.0), ('x_15_46', -0.0), ('x_15_56', 8.0), ('x_15_57', -0.0), ('x_15_66', -0.0), ('x_15_76', 0.0), ('x_15_91', -0.0), ('x_0_18', 0.0), ('x_18_0', 0.0), ('x_18_7', 0.0), ('x_18_15', -0.0), ('x_18_18', -0.0), ('x_18_20', -0.0), ('x_18_25', -0.0), ('x_18_27', -0.0), ('x_18_35', 0.0), ('x_18_40', -0.0), ('x_18_46', -0.0), ('x_18_56', -0.0), ('x_18_57', -0.0), ('x_18_66', -0.0), ('x_18_76', 0.0), ('x_18_91', -0.0), ('x_0_20', 0.0), ('x_20_0', 0.0), ('x_20_7', 0.0), ('x_20_15', 0.0), ('x_20_18', 0.0), ('x_20_20', -0.0), ('x_20_25', 25.0), ('x_20_27', -0.0), ('x_20_35', 0.0), ('x_20_40', 0.0), ('x_20_46', -0.0), ('x_20_56', 0.0), ('x_20_57', -0.0), ('x_20_66', -0.0), ('x_20_76', 0.0), ('x_20_91', -0.0), ('x_0_25', 0.0), ('x_25_0', 0.0), ('x_25_7', 0.0), ('x_25_15', 0.0), ('x_25_18', 0.0), ('x_25_20', -0.0), ('x_25_25', -0.0), ('x_25_27', -0.0), ('x_25_35', 0.0), ('x_25_40', 12.0), ('x_25_46', -0.0), ('x_25_56', -0.0), ('x_25_57', -0.0), ('x_25_66', -0.0), ('x_25_76', 0.0), ('x_25_91', -0.0), ('x_0_27', 0.0), ('x_27_0', 0.0), ('x_27_7', 0.0), ('x_27_15', 0.0), ('x_27_18', 0.0), ('x_27_20', 0.0), ('x_27_25', 0.0), ('x_27_27', -0.0), ('x_27_35', 0.0), ('x_27_40', 0.0), ('x_27_46', -0.0), ('x_27_56', 0.0), ('x_27_57', -0.0), ('x_27_66', 0.0), ('x_27_76', 0.0), ('x_27_91', 37.0), ('x_0_35', 0.0), ('x_35_0', 0.0), ('x_35_7', 5.0), ('x_35_15', -0.0), ('x_35_18', 0.0), ('x_35_20', -0.0), ('x_35_25', -0.0), ('x_35_27', -0.0), ('x_35_35', -0.0), ('x_35_40', -0.0), ('x_35_46', -0.0), ('x_35_56', -0.0), ('x_35_57', -0.0), ('x_35_66', -0.0), ('x_35_76', -0.0), ('x_35_91', -0.0), ('x_0_40', 0.0), ('x_40_0', 0.0), ('x_40_7', 0.0), ('x_40_15', -0.0), ('x_40_18', 1.0), ('x_40_20', -0.0), ('x_40_25', -0.0), ('x_40_27', -0.0), ('x_40_35', 0.0), ('x_40_40', -0.0), ('x_40_46', -0.0), ('x_40_56', -0.0), ('x_40_57', -0.0), ('x_40_66', -0.0), ('x_40_76', 0.0), ('x_40_91', -0.0), ('x_0_46', 0.0), ('x_46_0', 0.0), ('x_46_7', 0.0), ('x_46_15', 0.0), ('x_46_18', 0.0), ('x_46_20', -0.0), ('x_46_25', 0.0), ('x_46_27', 21.0), ('x_46_35', 0.0), ('x_46_40', 0.0), ('x_46_46', -0.0), ('x_46_56', 0.0), ('x_46_57', -0.0), ('x_46_66', 0.0), ('x_46_76', 0.0), ('x_46_91', 0.0), ('x_0_56', 0.0), ('x_56_0', 0.0), ('x_56_7', 0.0), ('x_56_15', -0.0), ('x_56_18', 0.0), ('x_56_20', -0.0), ('x_56_25', -0.0), ('x_56_27', -0.0), ('x_56_35', 0.0), ('x_56_40', -0.0), ('x_56_46', -0.0), ('x_56_56', -0.0), ('x_56_57', -0.0), ('x_56_66', -0.0), ('x_56_76', 0.0), ('x_56_91', -0.0), ('x_0_57', 0.0), ('x_57_0', 0.0), ('x_57_7', 0.0), ('x_57_15', 0.0), ('x_57_18', 0.0), ('x_57_20', 0.0), ('x_57_25', 0.0), ('x_57_27', 0.0), ('x_57_35', 0.0), ('x_57_40', 0.0), ('x_57_46', 3.0), ('x_57_56', 0.0), ('x_57_57', -0.0), ('x_57_66', 0.0), ('x_57_76', 0.0), ('x_57_91', 0.0), ('x_0_66', 0.0), ('x_66_0', 0.0), ('x_66_7', 0.0), ('x_66_15', 0.0), ('x_66_18', 0.0), ('x_66_20', 33.0), ('x_66_25', 0.0), ('x_66_27', 0.0), ('x_66_35', 0.0), ('x_66_40', 0.0), ('x_66_46', 0.0), ('x_66_56', 0.0), ('x_66_57', -0.0), ('x_66_66', -0.0), ('x_66_76', 0.0), ('x_66_91', -0.0), ('x_0_76', 0.0), ('x_76_0', 0.0), ('x_76_7', 0.0), ('x_76_15', -0.0), ('x_76_18', -0.0), ('x_76_20', -0.0), ('x_76_25', -0.0), ('x_76_27', -0.0), ('x_76_35', 3.0), ('x_76_40', -0.0), ('x_76_46', -0.0), ('x_76_56', -0.0), ('x_76_57', -0.0), ('x_76_66', -0.0), ('x_76_76', -0.0), ('x_76_91', -0.0), ('x_0_91', 0.0), ('x_91_0', 0.0), ('x_91_7', 0.0), ('x_91_15', 0.0), ('x_91_18', 0.0), ('x_91_20', -0.0), ('x_91_25', 0.0), ('x_91_27', -0.0), ('x_91_35', 0.0), ('x_91_40', 0.0), ('x_91_46', -0.0), ('x_91_56', 0.0), ('x_91_57', -0.0), ('x_91_66', 13.0), ('x_91_76', 0.0), ('x_91_91', -0.0)]
y = [('y_0_0', 0.0), ('y_0_7', -0.0), ('y_7_0', -0.0), ('y_7_7', 0.0), 
    ('y_7_15', -0.0), ('y_7_18', -0.0), ('y_7_20', -0.0), ('y_7_25', -0.0), ('y_7_27', -0.0), ('y_7_35', -0.0), ('y_7_40', -0.0), ('y_7_46', -0.0), ('y_7_56', -0.0), ('y_7_57', -0.0), ('y_7_66', -0.0), ('y_7_76', 1.0), ('y_7_91', -0.0), ('y_0_15', -0.0), ('y_15_0', -0.0), ('y_15_7', -0.0), ('y_15_15', 0.0), ('y_15_18', -0.0), ('y_15_20', -0.0), ('y_15_25', -0.0), ('y_15_27', -0.0), ('y_15_35', -0.0), ('y_15_40', -0.0), ('y_15_46', -0.0), ('y_15_56', 1.0), ('y_15_57', -0.0), ('y_15_66', -0.0), ('y_15_76', -0.0), ('y_15_91', -0.0), ('y_0_18', -0.0), ('y_18_0', 1.0), ('y_18_7', -0.0), ('y_18_15', -0.0), ('y_18_18', 0.0), ('y_18_20', -0.0), ('y_18_25', -0.0), ('y_18_27', -0.0), ('y_18_35', -0.0), ('y_18_40', 0.0), ('y_18_46', -0.0), ('y_18_56', -0.0), ('y_18_57', -0.0), ('y_18_66', -0.0), ('y_18_76', -0.0), ('y_18_91', -0.0), ('y_0_20', -0.0), ('y_20_0', -0.0), ('y_20_7', -0.0), ('y_20_15', -0.0), ('y_20_18', -0.0), ('y_20_20', 0.0), ('y_20_25', 1.0), ('y_20_27', -0.0), ('y_20_35', -0.0), ('y_20_40', -0.0), ('y_20_46', -0.0), ('y_20_56', -0.0), ('y_20_57', -0.0), ('y_20_66', 0.0), ('y_20_76', -0.0), ('y_20_91', -0.0), ('y_0_25', -0.0), ('y_25_0', -0.0), ('y_25_7', -0.0), ('y_25_15', -0.0), ('y_25_18', 0.0), ('y_25_20', -0.0), ('y_25_25', 0.0), ('y_25_27', -0.0), ('y_25_35', -0.0), ('y_25_40', 1.0), ('y_25_46', -0.0), ('y_25_56', -0.0), ('y_25_57', -0.0), ('y_25_66', -0.0), ('y_25_76', -0.0), ('y_25_91', -0.0), ('y_0_27', -0.0), ('y_27_0', -0.0), ('y_27_7', -0.0), ('y_27_15', -0.0), ('y_27_18', -0.0), ('y_27_20', -0.0), ('y_27_25', -0.0), ('y_27_27', 0.0), ('y_27_35', -0.0), ('y_27_40', -0.0), ('y_27_46', -0.0), ('y_27_56', -0.0), ('y_27_57', -0.0), ('y_27_66', 0.0), ('y_27_76', -0.0), ('y_27_91', 1.0), ('y_0_35', 0.0), ('y_35_0', -0.0), ('y_35_7', 1.0), ('y_35_15', -0.0), ('y_35_18', -0.0), ('y_35_20', -0.0), ('y_35_25', -0.0), ('y_35_27', -0.0), ('y_35_35', 0.0), ('y_35_40', -0.0), ('y_35_46', -0.0), ('y_35_56', 0.0), ('y_35_57', -0.0), ('y_35_66', -0.0), ('y_35_76', 0.0), ('y_35_91', -0.0), ('y_0_40', -0.0), ('y_40_0', -0.0), ('y_40_7', -0.0), ('y_40_15', 0.0), ('y_40_18', 1.0), ('y_40_20', -0.0), ('y_40_25', 0.0), ('y_40_27', -0.0), ('y_40_35', -0.0), ('y_40_40', 0.0), ('y_40_46', -0.0), ('y_40_56', -0.0), ('y_40_57', -0.0), ('y_40_66', -0.0), ('y_40_76', -0.0), ('y_40_91', -0.0), ('y_0_46', -0.0), ('y_46_0', -0.0), ('y_46_7', -0.0), ('y_46_15', -0.0), ('y_46_18', -0.0), ('y_46_20', -0.0), ('y_46_25', -0.0), ('y_46_27', 1.0), ('y_46_35', -0.0), ('y_46_40', -0.0), ('y_46_46', 0.0), ('y_46_56', -0.0), ('y_46_57', 0.0), ('y_46_66', -0.0), ('y_46_76', -0.0), ('y_46_91', 0.0), ('y_0_56', -0.0), ('y_56_0', 0.0), ('y_56_7', -0.0), ('y_56_15', 1.0), ('y_56_18', -0.0), ('y_56_20', -0.0), ('y_56_25', -0.0), ('y_56_27', -0.0), ('y_56_35', -0.0), ('y_56_40', -0.0), ('y_56_46', -0.0), ('y_56_56', 0.0), ('y_56_57', -0.0), ('y_56_66', -0.0), ('y_56_76', -0.0), ('y_56_91', -0.0), ('y_0_57', 1.0), ('y_57_0', -0.0), ('y_57_7', -0.0), ('y_57_15', -0.0), ('y_57_18', -0.0), ('y_57_20', -0.0), ('y_57_25', -0.0), ('y_57_27', -0.0), ('y_57_35', -0.0), ('y_57_40', -0.0), ('y_57_46', 1.0), ('y_57_56', -0.0), ('y_57_57', 0.0), ('y_57_66', -0.0), ('y_57_76', -0.0), ('y_57_91', -0.0), ('y_0_66', -0.0), ('y_66_0', -0.0), ('y_66_7', -0.0), ('y_66_15', -0.0), ('y_66_18', -0.0), ('y_66_20', 1.0), ('y_66_25', -0.0), ('y_66_27', 0.0), ('y_66_35', -0.0), ('y_66_40', -0.0), ('y_66_46', -0.0), ('y_66_56', -0.0), ('y_66_57', -0.0), ('y_66_66', 0.0), ('y_66_76', -0.0), ('y_66_91', -0.0), ('y_0_76', -0.0), ('y_76_0', -0.0), ('y_76_7', 0.0), ('y_76_15', -0.0), ('y_76_18', 0.0), ('y_76_20', -0.0), ('y_76_25', -0.0), ('y_76_27', -0.0), ('y_76_35', 1.0), ('y_76_40', -0.0), ('y_76_46', -0.0), ('y_76_56', -0.0), ('y_76_57', -0.0), ('y_76_66', -0.0), ('y_76_76', 0.0), ('y_76_91', -0.0), ('y_0_91', -0.0), ('y_91_0', -0.0), ('y_91_7', -0.0), ('y_91_15', -0.0), ('y_91_18', -0.0), ('y_91_20', 0.0), ('y_91_25', -0.0), ('y_91_27', 0.0), ('y_91_35', -0.0), ('y_91_40', -0.0), ('y_91_46', 0.0), ('y_91_56', -0.0), ('y_91_57', -0.0), ('y_91_66', 1.0), ('y_91_76', -0.0), ('y_91_91', 0.0)]
    
identifica(x,y)
'''



'''
#error
sirven = [['12', '28'], ['15', '38'], ['17', '48'], ['28', '12'], ['31',
    '62'], ['32', '31'], ['0', '36'], ['36', '17'], ['38', '75'], ['44', '15'], ['48', '44'], ['62', '0'], ['75', '32']]
x = [('x_0_0', -0.0), ('x_0_12', 0.0), ('x_12_0', 0.0), ('x_12_12', -0.0),
    ('x_12_15', 0.0), ('x_12_17', -0.0), ('x_12_28', 80.0), ('x_12_31', 0.0), ('x_12_32', -0.0), ('x_12_36', -0.0), ('x_12_38', 0.0), ('x_12_44', 0.0), ('x_12_48', -0.0), ('x_12_62', 0.0), ('x_12_75', 0.0), ('x_0_15', 0.0), ('x_15_0', 0.0), ('x_15_12', -0.0), ('x_15_15', -0.0), ('x_15_17', -0.0), ('x_15_28', -0.0), ('x_15_31', 0.0), ('x_15_32', -0.0), ('x_15_36', -0.0), ('x_15_38', 33.0), ('x_15_44', -0.0), ('x_15_48', -0.0), ('x_15_62', 0.0), ('x_15_75', 0.0), ('x_0_17', 0.0), ('x_17_0', 0.0), ('x_17_12', 0.0), ('x_17_15', 0.0), ('x_17_17', -0.0), ('x_17_28', 0.0), ('x_17_31', 0.0), ('x_17_32', 0.0), ('x_17_36', 0.0), ('x_17_38', 0.0), ('x_17_44', 0.0), ('x_17_48', 21.0), ('x_17_62', 0.0), ('x_17_75', 0.0), ('x_0_28', 0.0), ('x_28_0', 0.0), ('x_28_12', 74.0), ('x_28_15', -0.0), ('x_28_17', -0.0), ('x_28_28', -0.0), ('x_28_31', -0.0), ('x_28_32', -0.0), ('x_28_36', -0.0), ('x_28_38', 0.0), ('x_28_44', 0.0), ('x_28_48', -0.0), ('x_28_62', -0.0), ('x_28_75', 0.0), ('x_0_31', 0.0), ('x_31_0', 0.0), ('x_31_12', -0.0), ('x_31_15', -0.0), ('x_31_17', -0.0), ('x_31_28', -0.0), ('x_31_31', -0.0), ('x_31_32', -0.0), ('x_31_36', -0.0), ('x_31_38', -0.0), ('x_31_44', -0.0), ('x_31_48', -0.0), ('x_31_62', 24.0), ('x_31_75', -0.0), ('x_0_32', 0.0), ('x_32_0', 0.0), ('x_32_12', -0.0), ('x_32_15', -0.0), ('x_32_17', -0.0), ('x_32_28', -0.0), ('x_32_31', 8.0), ('x_32_32', -0.0), ('x_32_36', -0.0), ('x_32_38', -0.0), ('x_32_44', -0.0), ('x_32_48', -0.0), ('x_32_62', -0.0), ('x_32_75', -0.0), ('x_0_36', 0.0), ('x_36_0', 0.0), ('x_36_12', 0.0), ('x_36_15', 0.0), ('x_36_17', 8.0), ('x_36_28', 0.0), ('x_36_31', 0.0), ('x_36_32', -0.0), ('x_36_36', -0.0), ('x_36_38', 0.0), ('x_36_44', 0.0), ('x_36_48', 0.0), ('x_36_62', 0.0), ('x_36_75', 0.0), ('x_0_38', 0.0), ('x_38_0', 0.0), ('x_38_12', -0.0), ('x_38_15', 0.0), ('x_38_17', -0.0), ('x_38_28', -0.0), ('x_38_31', 0.0), ('x_38_32', -0.0), ('x_38_36', -0.0), ('x_38_38', -0.0), ('x_38_44', -0.0), ('x_38_48', -0.0), ('x_38_62', 0.0), ('x_38_75', 29.0), ('x_0_44', 0.0), ('x_44_0', 0.0), ('x_44_12', -0.0), ('x_44_15', 27.0), ('x_44_17', -0.0), ('x_44_28', -0.0), ('x_44_31', 0.0), ('x_44_32', -0.0), ('x_44_36', -0.0), ('x_44_38', 0.0), ('x_44_44', -0.0), ('x_44_48', -0.0), ('x_44_62', 0.0), ('x_44_75', 0.0), ('x_0_48', 0.0), ('x_48_0', 0.0), ('x_48_12', -0.0), ('x_48_15', 0.0), ('x_48_17', -0.0), ('x_48_28', -0.0), ('x_48_31', 0.0), ('x_48_32', -0.0), ('x_48_36', -0.0), ('x_48_38', 0.0), ('x_48_44', 16.0), ('x_48_48', -0.0), ('x_48_62', 0.0), ('x_48_75', 0.0), ('x_0_62', 0.0), ('x_62_0', 0.0), ('x_62_12', -0.0), ('x_62_15', -0.0), ('x_62_17', -0.0), ('x_62_28', -0.0), ('x_62_31', 0.0), ('x_62_32', -0.0), ('x_62_36', -0.0), ('x_62_38', 0.0), ('x_62_44', -0.0), ('x_62_48', -0.0), ('x_62_62', -0.0), ('x_62_75', -0.0), ('x_0_75', 0.0), ('x_75_0', 0.0), ('x_75_12', -0.0), ('x_75_15', 0.0), ('x_75_17', -0.0), ('x_75_28', -0.0), ('x_75_31', 0.0), ('x_75_32', 36.0), ('x_75_36', -0.0), ('x_75_38', 0.0), ('x_75_44', 0.0), ('x_75_48', 0.0), ('x_75_62', 0.0), ('x_75_75', -0.0)]
y =  [('y_0_0', 0.0), ('y_0_12', -0.0), ('y_12_0', -0.0), ('y_12_12', 0.0),
    ('y_12_15', -0.0), ('y_12_17', -0.0), ('y_12_28', 1.0), ('y_12_31', -0.0), ('y_12_32', -0.0), ('y_12_36', 0.0), ('y_12_38', -0.0), ('y_12_44', -0.0), ('y_12_48', -0.0), ('y_12_62', -0.0), ('y_12_75', -0.0), ('y_0_15', -0.0), ('y_15_0', -0.0), ('y_15_12', -0.0), ('y_15_15', 0.0), ('y_15_17', -0.0), ('y_15_28', -0.0), ('y_15_31', -0.0), ('y_15_32', -0.0), ('y_15_36', -0.0), ('y_15_38', 1.0), ('y_15_44', 0.0), ('y_15_48', -0.0), ('y_15_62', -0.0), ('y_15_75', 0.0), ('y_0_17', 0.0), ('y_17_0', -0.0), ('y_17_12', -0.0), ('y_17_15', -0.0), ('y_17_17', 0.0), ('y_17_28', -0.0), ('y_17_31', -0.0), ('y_17_32', -0.0), ('y_17_36', 0.0), ('y_17_38', -0.0), ('y_17_44', -0.0), ('y_17_48', 1.0), ('y_17_62', -0.0), ('y_17_75', -0.0), ('y_0_28', -0.0), ('y_28_0', 0.0), ('y_28_12', 1.0), ('y_28_15', -0.0), ('y_28_17', -0.0), ('y_28_28', 0.0), ('y_28_31', 0.0), ('y_28_32', 0.0), ('y_28_36', 0.0), ('y_28_38', -0.0), ('y_28_44', -0.0), ('y_28_48', -0.0), ('y_28_62', -0.0), ('y_28_75', -0.0), ('y_0_31', -0.0), ('y_31_0', -0.0), ('y_31_12', -0.0), ('y_31_15', -0.0), ('y_31_17', -0.0), ('y_31_28', -0.0), ('y_31_31', 0.0), ('y_31_32', 0.0), ('y_31_36', -0.0), ('y_31_38', -0.0), ('y_31_44', -0.0), ('y_31_48', -0.0), ('y_31_62', 1.0), ('y_31_75', -0.0), ('y_0_32', -0.0), ('y_32_0', -0.0), ('y_32_12', -0.0), ('y_32_15', -0.0), ('y_32_17', -0.0), ('y_32_28', -0.0), ('y_32_31', 1.0), ('y_32_32', 0.0), ('y_32_36', -0.0), ('y_32_38', -0.0), ('y_32_44', -0.0), ('y_32_48', -0.0), ('y_32_62', 0.0), ('y_32_75', -0.0), ('y_0_36', 1.0), ('y_36_0', -0.0), ('y_36_12', -0.0), ('y_36_15', -0.0), ('y_36_17', 1.0), ('y_36_28', 0.0), ('y_36_31', -0.0), ('y_36_32', -0.0), ('y_36_36', 0.0), ('y_36_38', -0.0), ('y_36_44', -0.0), ('y_36_48', -0.0), ('y_36_62', -0.0), ('y_36_75', -0.0), ('y_0_38', -0.0), ('y_38_0', -0.0), ('y_38_12', -0.0), ('y_38_15', 0.0), ('y_38_17', -0.0), ('y_38_28', -0.0), ('y_38_31', -0.0), ('y_38_32', -0.0), ('y_38_36', -0.0), ('y_38_38', 0.0), ('y_38_44', 0.0), ('y_38_48', -0.0), ('y_38_62', -0.0), ('y_38_75', 1.0), ('y_0_44', -0.0), ('y_44_0', -0.0), ('y_44_12', -0.0), ('y_44_15', 1.0), ('y_44_17', -0.0), ('y_44_28', -0.0), ('y_44_31', -0.0), ('y_44_32', -0.0), ('y_44_36', -0.0), ('y_44_38', -0.0), ('y_44_44', 0.0), ('y_44_48', 0.0), ('y_44_62', -0.0), ('y_44_75', -0.0), ('y_0_48', -0.0), ('y_48_0', -0.0), ('y_48_12', -0.0), ('y_48_15', -0.0), ('y_48_17', 0.0), ('y_48_28', -0.0), ('y_48_31', -0.0), ('y_48_32', -0.0), ('y_48_36', -0.0), ('y_48_38', -0.0), ('y_48_44', 1.0), ('y_48_48', 0.0), ('y_48_62', -0.0), ('y_48_75', -0.0), ('y_0_62', -0.0), ('y_62_0', 1.0), ('y_62_12', -0.0), ('y_62_15', -0.0), ('y_62_17', -0.0), ('y_62_28', -0.0), ('y_62_31', -0.0), ('y_62_32', -0.0), ('y_62_36', -0.0), ('y_62_38', -0.0), ('y_62_44', -0.0), ('y_62_48', -0.0), ('y_62_62', 0.0), ('y_62_75', -0.0), ('y_0_75', -0.0), ('y_75_0', -0.0), ('y_75_12', -0.0), ('y_75_15', -0.0), ('y_75_17', -0.0), ('y_75_28', -0.0), ('y_75_31', -0.0), ('y_75_32', 1.0), ('y_75_36', -0.0), ('y_75_38', 0.0), ('y_75_44', -0.0), ('y_75_48', -0.0), ('y_75_62', 0.0), ('y_75_75', 0.0)]

'''

"""
text = []
i = 0
with open('tiempo_camiones799.txt', 'r') as file:
    for line in file:
        text.append(float(line.strip()))


"""
