class Carretera:
    def __init__(self, x, y, ancho, alto, direccion=None):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.direccion = direccion  # opcional (N, S, E, O)