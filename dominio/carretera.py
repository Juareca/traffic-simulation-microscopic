class Carretera:
    def __init__(self, x, y, ancho, alto, direccion=None, num_carriles=3):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.direccion = direccion

        # Posición del cruce en PIXELES
        self.pos_cruce = self._calcular_pos_cruce()

        self.carriles = [Carril(i, self.direccion) for i in range(num_carriles)]

    def _calcular_pos_cruce(self):
        if self.direccion in ("N-S", "S-N"):
            return self.alto / 2
        else:
            return self.ancho / 2


class Carril:
    def __init__(self, indice, direccion):
        self.indice = indice
        self.direccion = direccion   # O-E, E-O, S-N, N-S
        self.vehiculos = []

    def ordenar_vehiculos(self):
        # Posición crece hacia adelante
        if self.direccion in ("O-E", "S-N"):
            self.vehiculos.sort(key=lambda v: v.posicion)
        else:  # E-O, N-S → posición decrece hacia adelante
            self.vehiculos.sort(key=lambda v: -v.posicion)

    def obtener_lider(self, vehiculo):
        self.ordenar_vehiculos()

        idx = self.vehiculos.index(vehiculo)
        if idx == 0:
            return None  # no hay líder

        return self.vehiculos[idx - 1]


