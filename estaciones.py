from random import expovariate

class Estacion:

    def __init__(self, number, x, y):
        self.number = number
        self.x = x
        self.y = y
        self.demanda_satisfecha = 0
        self.demanda_insatisfecha = 0
        self.inventario = 0
        self.diccionario_manana = {}
        self.diccionario_mediodia = {}
        self.diccionario_tarde = {}
        self.diccionario_noche = {}
        self.proxima_llegada = 0
        self.tasa_manana = 0
        self.tasa_mediodia = 0
        self.tasa_tarde = 0
        self.tasa_noche = 0

    def proxima_llegada_manana(self):
        self.proxima_llegada = expovariate(float(
                1/self.tasa_manana))

    def proxima_llegada_mediodia(self):
        self.proxima_llegada = expovariate(float(
                1/self.tasa_mediodia))

    def proxima_llegada_tarde(self):
        self.proxima_llegada = expovariate(float(
                1/self.tasa_tarde))

    def proxima_llegada_noche(self):
        self.proxima_llegada = expovariate(float(
                1/self.tasa_noche))

    def __repr__(self):
        return str(self.number)
