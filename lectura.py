import xlrd
from xlrd import open_workbook
from estaciones import Estacion

wb = open_workbook('Datos-2.xlsx')
sheet_names = wb.sheet_names()

i = 0
for sheet in wb.sheets():
    number_of_rows = sheet.nrows
    number_of_columns = sheet.ncols
    estaciones = {}
    j = 1
    if number_of_rows == 95:
        for row in range(1, number_of_rows):
            values = []
            i = 0
            for col in range(number_of_columns):
                if i >= 1:
                    value = (sheet.cell(row, col).value)
                    try:
                        value = str(int(value))
                    except ValueError:
                        pass
                    finally:
                        values.append(value)
                i += 1
            j += 1
            if j >= 4:
                estaciones[values[0]] = Estacion(values[0], values[1], values[2])

    if i == 4:

    i += 1

            #print(values)

    print(estaciones)