class Estacion:
    demanda = 0

    def __init__(self, num, x, y, b):
        self.num = num
        self.x = x
        self.y = y
        self.b = b
        self.distancias = {}