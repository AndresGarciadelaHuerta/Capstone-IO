from random import expovariate


class Estacion:

    def __init__(self, number):
        self.number = number
        self.x = 0
        self.y = 0
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
        self.distancias_cuadrado = {}
        self.num = int(number.split()[1])
        self.inv_manana = 17 if self.num % 2 == 0 else 18
        self.demanda_insatisfecha_manana = 0
        self.demanda_insatisfecha_mediodia = 0
        self.demanda_insatisfecha_tarde = 0
        self.demanda_insatisfecha_noche = 0

    def probas(self, diccionarios):
        self.probs = {}
        self.probs['manana'] = {i.num: i.tasa_manana * 3 * i.diccionario_manana[self.number] for i in
                                diccionarios.values()}
        self.probs['mediodia'] = {i.num: i.tasa_mediodia * 3 * i.diccionario_mediodia[self.number] for i in
                                  diccionarios.values()}
        self.probs['tarde'] = {i.num: i.tasa_tarde * 3 * i.diccionario_tarde[self.number] for i in
                               diccionarios.values()}
        self.probs['noche'] = {i.num: i.tasa_noche * 3 * i.diccionario_noche[self.number] for i in
                               diccionarios.values()}

    def proxima_llegada_manana(self):
        self.proxima_llegada = expovariate(float(
            1 / self.tasa_manana))

    def proxima_llegada_mediodia(self):
        self.proxima_llegada = expovariate(float(
            1 / self.tasa_mediodia))

    def proxima_llegada_tarde(self):
        self.proxima_llegada = expovariate(float(
            1 / self.tasa_tarde))

    def proxima_llegada_noche(self):
        self.proxima_llegada = expovariate(float(
            1 / self.tasa_noche))

    def __repr__(self):
        return str(self.number)
