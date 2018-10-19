from Clusters import *
from Modelo_buti import *

def simulacion_completa():
    clusters, s = inicio()
    for grupo in clusters.values():
        ruteo(grupo, s.estaciones)


if __name__ == '__main__':
    simulacion_completa()
