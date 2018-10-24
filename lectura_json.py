import json
from lectura import poblar
from estaciones import Estacion



def create_json(estaciones):
    with open('estaciones_iniciales.json', 'w') as e:
        for estacion in estaciones.keys():
            estaciones[estacion] = estaciones[estacion].__dict__
        json.dump(estaciones, e)


def read_json():
    with open('estaciones_iniciales.json', 'r') as e:
        estaciones = json.load(e)
    for estacion in estaciones.keys():
        est = Estacion(estacion)
        est.__dict__ = estaciones[estacion]
        estaciones[estacion] = est
    return estaciones



if __name__ == '__main__':
    estaciones = read_json()
    #print(estaciones["Estación 92"].distancias_cuadrado)