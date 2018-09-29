from lectura import poblar
from random import expovariate
import numpy
from math import sqrt




class Simulador:

    def __init__(self):
        self.tiempo_anterior = 0
        self.tiempo_actual = 0
        self.contador_dias = 0
        self.cola = []
        self.estaciones = {}
        self.velocidad_bicicleta = 40
        self.demanda_insatisfecha = 0
        self.demanda_satisfecha = 0
        self.prints = False

    def definir_distribucion_manana(self):
        i = 0
        for estacion in self.estaciones.keys():
            if i // 2 == 0:
                self.estaciones[estacion].inventario = 17
                i += 1
            else:
                self.estaciones[estacion].inventario = 18
                i += 1

    def llegadas_personas_manana(self):

        for estacion in self.estaciones.keys():
            self.estaciones[estacion].proxima_llegada = int((8 * 60) + expovariate(
                float(1/self.estaciones[estacion].tasa_manana)))
            self.cola.append((int(self.estaciones[estacion].proxima_llegada),
                              "Inicio persona", estacion))
            self.cola.sort()

    def tiempo_viaje_persona(self, estacion1, estacion2):
        a = [float(self.estaciones[estacion1].x), float(self.estaciones[estacion1].y)]
        b = [float(self.estaciones[estacion2].x), float(self.estaciones[estacion2].y)]
        #distancia = numpy.linalg.norm(a-b)
        # Esta en Kms/Hora
        distancia = float(sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2))
        tiempo_en_llegar = int((distancia/self.velocidad_bicicleta) * 60)
        return (self.tiempo_actual + tiempo_en_llegar, "Fin persona",
                                                                    estacion2)


    def run(self):
        """
                Metodo que hace la simulacion.
                Retorna None
        """
        self.definir_distribucion_manana()
        self.llegadas_personas_manana()

        while self.contador_dias < 1:

            if len(self.cola) == 0:
                self.contador_dias = 1
                return

            evento = self.cola[0]
            self.tiempo_actual = evento[0]

            #if self.tiempo_actual > 1200:
             #   self.contador_dias = 1
              #  return

            if evento[1] == "Inicio persona":
                if self.estaciones[evento[2]].inventario == 0:
                    if self.prints:
                        print(str(evento) + "Demanda Insatisfecha")
                    self.estaciones[evento[2]].demanda_insatisfecha += 1
                    self.demanda_insatisfecha += 1
                    self.cola.pop(0)
                    if self.tiempo_actual < (11 * 60):
                        self.estaciones[evento[2]].proxima_llegada_manana()
                        tiempo_nueva_llegada = int(self.tiempo_actual + \
                                               self.estaciones[
                                                   evento[2]].proxima_llegada)
                    elif self.tiempo_actual < (14 * 60):
                        self.estaciones[evento[2]].proxima_llegada_mediodia()
                        tiempo_nueva_llegada = int(self.tiempo_actual + \
                                               self.estaciones[
                                                   evento[2]].proxima_llegada)
                    elif self.tiempo_actual < (17 * 60):
                        self.estaciones[evento[2]].proxima_llegada_tarde()
                        tiempo_nueva_llegada = int(self.tiempo_actual + \
                                               self.estaciones[
                                                   evento[2]].proxima_llegada)
                    else:
                        self.estaciones[evento[2]].proxima_llegada_noche()
                        tiempo_nueva_llegada = int(self.tiempo_actual + \
                                               self.estaciones[
                                                   evento[2]].proxima_llegada)
                elif self.estaciones[evento[2]].inventario > 0:
                    if self.prints:
                        print(str(evento) + "Demanda Satisfecha")
                    if self.tiempo_actual < (11 * 60):
                        estacion_llegada = numpy.random.choice(
                            list(self.estaciones.keys()), 1, p=list(self.estaciones[
                                evento[2]].diccionario_manana.values()))
                        self.estaciones[evento[2]].proxima_llegada_manana()
                        tiempo_nueva_llegada = int(self.tiempo_actual + \
                                               self.estaciones[
                                                   evento[2]].proxima_llegada)
                    elif self.tiempo_actual < (14 * 60):
                        estacion_llegada = numpy.random.choice(
                            list(self.estaciones.keys()), 1, p=list(self.estaciones[
                                evento[2]].diccionario_mediodia.values()))
                        self.estaciones[evento[2]].proxima_llegada_mediodia()
                        tiempo_nueva_llegada = int(self.tiempo_actual + \
                                               self.estaciones[
                                                   evento[2]].proxima_llegada)
                    elif self.tiempo_actual < (17 * 60):
                        estacion_llegada = numpy.random.choice(
                            list(self.estaciones.keys()), 1, p=list(self.estaciones[
                                evento[2]].diccionario_tarde.values()))
                        self.estaciones[evento[2]].proxima_llegada_tarde()
                        tiempo_nueva_llegada = int(self.tiempo_actual + \
                                               self.estaciones[
                                                   evento[2]].proxima_llegada)
                    #Ahora el caso en que self.tiempo_actual < (20 * 60)
                    ##### CAMBIAR DE TARDE A NOCHE CUANDO ESTE LISTO
                    else:
                        estacion_llegada = numpy.random.choice(
                            list(self.estaciones.keys()), 1, p=list(self.estaciones[
                                evento[2]].diccionario_noche.values()))
                        self.estaciones[evento[2]].proxima_llegada_noche()
                        tiempo_nueva_llegada = int(self.tiempo_actual + \
                                               self.estaciones[
                                                   evento[2]].proxima_llegada)

                    self.estaciones[evento[2]].inventario -= 1
                    self.estaciones[evento[2]].demanda_satisfecha += 1
                    self.demanda_satisfecha += 1
                    #print(estacion_llegada)
                    tupla = self.tiempo_viaje_persona(evento[2],
                                                      str(estacion_llegada[0]))
                    self.cola.pop(0)
                    self.cola.append(tupla)
                    self.cola.sort()


                # Definimos nueva llegada
                if self.tiempo_actual < 1200 and tiempo_nueva_llegada <= 1200:
                    tupla = (tiempo_nueva_llegada, "Inicio persona", evento[2])
                    self.cola.append(tupla)
                    self.cola.sort()



            elif evento[1] == "Fin persona":
                if self.prints:
                    print(str(evento) + "Persona Finaliza")
                self.estaciones[evento[2]].inventario += 1
                self.cola.pop(0)



#estaciones = poblar()
#s = Simulador()
#s.estaciones = estaciones
#s.prints = True
#s.run()
#print(s.demanda_satisfecha/(s.demanda_insatisfecha + s.demanda_satisfecha))
