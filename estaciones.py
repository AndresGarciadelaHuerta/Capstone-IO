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
        # Diccionario con las llegadas esperadas de cada estacion
        self.probs = {}
        self.probs['manana'] = {i.num: i.tasa_manana * 3 * i.diccionario_manana[self.number] for i in
                                diccionarios.values()}
        self.probs['mediodia'] = {i.num: i.tasa_mediodia * 3 * i.diccionario_mediodia[self.number] for i in
                                  diccionarios.values()}
        self.probs['tarde'] = {i.num: i.tasa_tarde * 3 * i.diccionario_tarde[self.number] for i in
                               diccionarios.values()}
        self.probs['noche'] = {i.num: i.tasa_noche * 3 * i.diccionario_noche[self.number] for i in
                               diccionarios.values()}

        # flujo la resta entre llegadas y salidas
        self.flujo_manana = sum(self.probs['manana'].values()) - 3 * self.tasa_manana
        self.flujo_mediodia = sum(self.probs['mediodia'].values()) - 3 * self.tasa_mediodia
        self.flujo_tarde = sum(self.probs['tarde'].values()) - 3 * self.tasa_tarde
        self.flujo_noche = sum(self.probs['noche'].values()) - 3 * self.tasa_noche
        self.flujo_total = self.flujo_manana + self.flujo_mediodia + self.flujo_tarde + self.flujo_noche

    def proxima_llegada_manana(self):
        self.proxima_llegada = expovariate(self.tasa_manana / 60)

    def proxima_llegada_mediodia(self):
        self.proxima_llegada = expovariate(self.tasa_mediodia / 60)

    def proxima_llegada_tarde(self):
        self.proxima_llegada = expovariate(self.tasa_tarde / 60)

    def proxima_llegada_noche(self):
        self.proxima_llegada = expovariate(self.tasa_noche / 60)

    def __repr__(self):
        return str(self.number)
