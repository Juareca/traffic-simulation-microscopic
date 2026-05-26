import random
from dominio.config import (
    T_MIN, T_MAX,
    A_MAX_MIN, A_MAX_MAX,
    B_MIN, B_MAX,
    TIEMPO_REACCION_MIN, TIEMPO_REACCION_MAX,
    LARGO_VEHICULO, V0_MAX, V0_MIN,
    VELOCIDAD_PARADA_UMBRAL,
    VELOCIDAD_SIMULACION
)


class Vehiculo:
    """Representa un vehículo en la simulación de tráfico."""

    # Velocidad deseada global (m/s)
    v0 = random.uniform(V0_MIN, V0_MAX)

    def __init__(self, id, posicion=0.0, velocidad=0.0):
        self.id = id

        # Estado dinámico
        self.posicion = posicion
        self.posicion_anterior = posicion
        self.velocidad = velocidad
        self.aceleracion = 0.0

        # Referencias
        self.carril = None

        # Parámetros individuales (IDM)
        self.v0 = Vehiculo.v0
        self.T = random.uniform(T_MIN, T_MAX)                          # reacción conductor
        self.a_max = random.uniform(A_MAX_MIN, A_MAX_MAX)              # aceleración máxima
        self.b = random.uniform(B_MIN, B_MAX)                          # desaceleración máxima

        # 🔥 IMPORTANTE: tiempo de reacción humano
        self.tiempo_reaccion = random.uniform(TIEMPO_REACCION_MIN, TIEMPO_REACCION_MAX)

        # Métricas
        self.tiempo_parado = 0.0
        self.tiempo_espera = 0.0

        # Dimensión física
        self.largo = LARGO_VEHICULO

        # Medida de flujo: ya cruzó la línea/cebra
        self.ha_cruzado_detector = False

    def actualizar(self, dt):

        dt_sim = dt 

        self.posicion_anterior = self.posicion

        # Integración
        self.velocidad += self.aceleracion * dt_sim
        self.velocidad = max(0.0, self.velocidad)

        self.posicion += self.velocidad * dt_sim

        # Estado de parada
        if self.velocidad <= VELOCIDAD_PARADA_UMBRAL:
            self.tiempo_parado += dt_sim
            self.tiempo_espera += dt_sim
        else:
            self.tiempo_parado = 0.0