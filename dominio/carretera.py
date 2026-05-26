from dominio.config import ESCALA


class Carretera:
    """
    Representa una carretera en la simulación.
    Maneja geometría, dirección, carriles y posición del cruce.
    """

    def __init__(self, x, y, ancho, alto, num_carriles, direccion=None):
        self.x = x                  # posición en pantalla (px)
        self.y = y
        self.ancho = ancho          # tamaño en pantalla (px)
        self.alto = alto
        self.direccion = direccion  # "N-S", "S-N", "E-O", "O-E"

        # ============================================================
        # LARGO REAL DE LA CARRETERA EN METROS (PASO 2)
        # ============================================================
        if direccion in ("N-S", "S-N"):
            self.largo = self.alto / ESCALA
        else:
            self.largo = self.ancho / ESCALA

        # ============================================================
        # INICIO Y FIN EN METROS (PASO 3)
        # ============================================================
        self.inicio_metros = 0.0
        self.fin_metros = self.largo

        # Posición del cruce en PIXELES (centro de la carretera)
        self.pos_cruce = self._calcular_pos_cruce()

        # Crear carriles con referencia a la carretera
        self.carriles = [
            Carril(i, self.direccion, self)
            for i in range(num_carriles)
        ]

    def _calcular_pos_cruce(self):
        """Devuelve la posición del cruce en PIXELES."""
        if self.direccion in ("N-S", "S-N"):
            return self.alto / 2
        else:
            return self.ancho / 2


class Carril:
    """
    Representa un carril dentro de una carretera.
    """

    def __init__(self, indice, direccion, carretera):
        self.indice = indice
        self.direccion = direccion   # O-E, E-O, S-N, N-S
        self.carretera = carretera   # referencia necesaria para limpieza y dibujo
        self.vehiculos = []

    def ordenar_vehiculos(self):
        """
        Ordena los vehículos según su posición en el carril.
        """
        if self.direccion in ("O-E", "S-N"):
            # posición crece hacia adelante
            self.vehiculos.sort(key=lambda v: v.posicion)
        else:
            # posición decrece hacia adelante
            self.vehiculos.sort(key=lambda v: -v.posicion)

    def obtener_lider(self, vehiculo):
        """
        Devuelve el vehículo inmediatamente adelante del dado.
        """
        self.ordenar_vehiculos()

        idx = self.vehiculos.index(vehiculo)
        if idx == 0:
            return None  # no hay líder

        return self.vehiculos[idx - 1]
