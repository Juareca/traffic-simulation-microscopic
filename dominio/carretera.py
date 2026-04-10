class Carretera:
    def __init__(self, x, y, ancho, alto, direccion=None, num_carriles=2):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.direccion = direccion

        # Crear carriles
        self.carriles = [Carril(i) for i in range(num_carriles)]

class Carril:
    def __init__(self, indice):
        self.indice = indice      # 0 = carril izquierdo, 1 = carril derecho
        self.vehiculos = []       # vehículos en este carril
