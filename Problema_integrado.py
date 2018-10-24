from Clusters import *
from Modelo_buti import *

def simulacion_completa(prints=False):
    clusters, s = inicio(prints)
    for grupo in clusters.values():
        ruteo(grupo, s.estaciones, True)


if __name__ == '__main__':
    simulacion_completa(True)
