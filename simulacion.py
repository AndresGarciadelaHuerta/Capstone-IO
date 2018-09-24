from random import expovariate
import numpy






class Simulador:

    def __init__(self):
        self.tiempo_anterior = 0
        self.tiempo_actual = 0
        self.contador_dias = 0
        self.cola = []
        self.estaciones = {}
        self.velocidad_bicicleta = 40
        self.demanda_insatisfecha = 0
        self.demanda_satisfecha = 1


    def llegadas_personas_manana(self):

        for estacion in self.estaciones.keys():
            self.estaciones[estacion].proxima_llegada = (8 * 60) + expovariate(
                float(1/self.estaciones[estacion].tasa_manana))
            self.cola.append((int(self.estaciones[estacion].proxima_llegada),
                              "Inicio persona", estacion))
            self.cola.sort()

    def tiempo_viaje_persona(self, estacion1, estacion2):
        a = (self.estaciones[estacion1].x, self.estaciones[estacion1].y)
        b = (self.estaciones[estacion2].x, self.estaciones[estacion2].y)
        distancia = numpy.linalg.norm(a-b)
        # Esta en Metros/Hora
        tiempo_en_llegar = int((distancia/self.velocidad_bicicleta) * 60)
        return (self.tiempo_actual + tiempo_en_llegar, "Fin persona",
                                                                    estacion2)


    def run(self):
        """
                Metodo que hace la simulacion.
                Retorna None
        """


        while self.contador_dias < 1:

            if len(self.cola) == 0:
                self.contador_dias = 1
                return

            evento = self.cola[0]
            self.tiempo_actual = evento[0]

            if evento[1] == "Inicio persona":
                if self.estaciones[evento[2]].inventario == 0:
                    self.demanda_insatisfecha += 1
                    self.cola.pop(0)
                    if self.tiempo_actual < (11 * 60):
                        self.estaciones[evento[2]].proxima_llegada_manana()
                        tiempo_nueva_llegada = self.tiempo_actual + \
                                               self.estaciones[
                                                   evento[2]].proxima_llegada
                    elif self.tiempo_actual < (14 * 60):
                        self.estaciones[evento[2]].proxima_llegada_mediodia()
                        tiempo_nueva_llegada = self.tiempo_actual + \
                                               self.estaciones[
                                                   evento[2]].proxima_llegada
                    elif self.tiempo_actual < (17 * 60):
                        self.estaciones[evento[2]].proxima_llegada_tarde()
                        tiempo_nueva_llegada = self.tiempo_actual + \
                                               self.estaciones[
                                                   evento[2]].proxima_llegada
                    else:
                        self.estaciones[evento[2]].proxima_llegada_noche()
                        tiempo_nueva_llegada = self.tiempo_actual + \
                                               self.estaciones[
                                                   evento[2]].proxima_llegada
                elif self.estaciones[evento[2]].inventario > 0:
                    if self.tiempo_actual < (11 * 60):
                        estacion_llegada = numpy.random.choice(
                            self.estaciones.keys(), 1, p=self.estaciones[
                                evento[2]].diccionario_manana.values())
                        self.estaciones[evento[2]].proxima_llegada_manana()
                        tiempo_nueva_llegada = self.tiempo_actual + \
                                               self.estaciones[
                                                   evento[2]].proxima_llegada
                    elif self.tiempo_actual < (14 * 60):
                        estacion_llegada = numpy.random.choice(
                            self.estaciones.keys(), 1, p=self.estaciones[
                                evento[2]].diccionario_manana.values())
                        self.estaciones[evento[2]].proxima_llegada_mediodia()
                        tiempo_nueva_llegada = self.tiempo_actual + \
                                               self.estaciones[
                                                   evento[2]].proxima_llegada
                    elif self.tiempo_actual < (17 * 60):
                        estacion_llegada = numpy.random.choice(
                            self.estaciones.keys(), 1, p=self.estaciones[
                                evento[2]].diccionario_manana.values())
                        self.estaciones[evento[2]].proxima_llegada_tarde()
                        tiempo_nueva_llegada = self.tiempo_actual + \
                                               self.estaciones[
                                                   evento[2]].proxima_llegada
                    #Ahora el caso en que self.tiempo_actual < (20 * 60)
                    else:
                        estacion_llegada = numpy.random.choice(
                            self.estaciones.keys(), 1, p=self.estaciones[
                                evento[2]].diccionario_manana.values())
                        self.estaciones[evento[2]].proxima_llegada_noche()
                        tiempo_nueva_llegada = self.tiempo_actual + \
                                               self.estaciones[
                                                   evento[2]].proxima_llegada

                    self.estaciones[evento[2]].inventario -= 1
                    self.demanda_satisfecha += 1
                    tupla = self.tiempo_viaje_persona(evento[1],
                                                      estacion_llegada)
                    self.cola.pop(0)
                    self.cola.append(tupla)
                    self.cola.sort()


                # Definimos nueva llegada
                tupla = (tiempo_nueva_llegada, "Inicio persona", evento[2])
                self.cola.append(tupla)
                self.cola.sort()



            elif evento[1] == "Fin persona":
                self.estaciones[evento[2]].inventario += 1
                self.cola.pop(0)





