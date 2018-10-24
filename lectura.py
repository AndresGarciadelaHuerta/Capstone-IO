import xlrd
from xlrd import open_workbook
from estaciones import Estacion


def poblar():
    wb = open_workbook('Datos con matrices final.xlsx')
    sheet_names = wb.sheet_names()


    estaciones = {}
    k = 0
    for sheet in wb.sheets():
        number_of_rows = sheet.nrows
        number_of_columns = sheet.ncols


        if k == 0:
            j = 1
            for row in range(1, number_of_rows):
                values = []
                i = 0
                for col in range(number_of_columns):
                    if i >= 1:
                        value = sheet.cell(row, col).value
                        try:
                            value = str(int(value))
                        except ValueError:
                            pass
                        finally:
                            values.append(value)
                    i += 1
                j += 1
                if j >= 4:
                    estaciones[values[0]] = Estacion(values[0])
                    estaciones[values[0]].x = values[1]
                    estaciones[values[0]].y = values[2]
                    estaciones[values[0]].diccionario_manana = {}

        elif k == 3:
            j = 1
            for row in range(1, number_of_rows):
                values = []
                i = 0
                for col in range(number_of_columns):
                    if i >= 1:
                        value = sheet.cell(row, col).value
                        try:
                            value = str(float(value))
                        except ValueError:
                            pass
                        finally:
                            values.append(value)
                    i += 1
                if j >= 2:
                    #print(values)
                    estaciones[values[0]].tasa_manana = float(values[1])
                    #print(estaciones[values[0]].tasa_manana)
                    estaciones[values[0]].tasa_mediodia = float(values[2])
                    estaciones[values[0]].tasa_tarde = float(values[3])
                    estaciones[values[0]].tasa_noche = float(values[4])
                    #print('Bien')
                j += 1
        elif k == 8:
            j = 1
            for row in range(1, number_of_rows):
                values = []
                i = 0
                for col in range(number_of_columns):
                    if i >= 1:
                        value = sheet.cell(row, col).value
                        try:
                            value = str(float(value))
                        except ValueError:
                            pass
                        finally:
                            values.append(value)
                    i += 1

                if j >= 1:
                    estacion = "Estación " + str(j)
                    n = 0
                    for value in values:
                        #print(value)
                        if n >= 1:
                            estacion2 = "Estación " + str(n)
                            estaciones[estacion].diccionario_manana[
                                estacion2] = float(values[n])
                            #print(n)
                        n += 1
                j += 1

        elif k == 10:
            j = 1
            for row in range(1, number_of_rows):
                values = []
                i = 0
                for col in range(number_of_columns):
                    if i >= 1:
                        value = sheet.cell(row, col).value
                        try:
                            value = str(float(value))
                        except ValueError:
                            pass
                        finally:
                            values.append(value)
                    i += 1

                if j >= 1:
                    estacion = "Estación " + str(j)
                    n = 0
                    for value in values:
                        #print(value)
                        if n >= 1:
                            estacion2 = "Estación " + str(n)
                            estaciones[estacion].diccionario_mediodia[
                                estacion2] = float(values[n])
                            #print(n)
                        n += 1
                j += 1

        elif k == 11:
            j = 1
            for row in range(1, number_of_rows):
                values = []
                i = 0
                for col in range(number_of_columns):
                    if i >= 1:
                        value = sheet.cell(row, col).value
                        try:
                            value = str(float(value))
                        except ValueError:
                            pass
                        finally:
                            values.append(value)
                    i += 1

                if j >= 1:
                    estacion = "Estación " + str(j)
                    n = 0
                    for value in values:
                        #print(value)
                        if n >= 1:
                            estacion2 = "Estación " + str(n)
                            estaciones[estacion].diccionario_tarde[
                                estacion2] = float(values[n])
                            #print(n)
                        n += 1
                j += 1

        elif k == 12:
            j = 1
            for row in range(1, number_of_rows):
                values = []
                i = 0
                for col in range(number_of_columns):
                    if i >= 1:
                        value = sheet.cell(row, col).value
                        try:
                            value = str(float(value))
                        except ValueError:
                            pass
                        finally:
                            values.append(value)
                    i += 1
    
                if j >= 1:
                    estacion = "Estación " + str(j)
                    n = 0
                    for value in values:
                        #print(value)
                        if n >= 1:
                            estacion2 = "Estación " + str(n)
                            estaciones[estacion].diccionario_noche[
                                estacion2] = float(values[n])
                            #print(n)
                        n += 1
                j += 1

        k += 1

                #print(values)

    #print(estaciones['Estación 1'].diccionario_manana)
    #print(estaciones['Estación 92'].diccionario_manana)
    #print('\n' + str(estaciones['Estación 1'].diccionario_mediodia))
    #print(estaciones['Estación 92'].diccionario_mediodia)
    #print('\n' + str(estaciones['Estación 1'].diccionario_tarde))
    #print(estaciones['Estación 92'].diccionario_tarde)
    #print('\n' + estaciones['Estación 1'].diccionario_noche)
    #print(estaciones['Estación 92'].diccionario_noche)

    #print(estaciones['Estación 1'].tasa_manana)
    #print(estaciones['Estación 1'].tasa_mediodia)
    #print(estaciones['Estación 1'].tasa_tarde)
    #print(estaciones['Estación 1'].tasa_noche)

    for estacion in estaciones.values():
            estacion.distancias_cuadrado = {estacion2.num: (float(estacion.x) - float(estacion2.x)) ** 2 + (float(estacion.y)
                                                    - float(estacion2.y)) ** 2 for estacion2 in estaciones.values()}

    #print(estaciones['Estación 1'].distancias_cuadrado)


    return estaciones


