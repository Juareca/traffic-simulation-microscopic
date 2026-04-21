import random

class Vehiculo:
    """Representa un vehículo en la simulación de tráfico."""

    # Velocidad deseada global (m/s)
    v0 = 6.0  # 🔥 4–8 m/s urbano realista

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
        self.T = random.uniform(1.2, 2.0)        # reacción conductor
        self.a_max = random.uniform(0.5, 1.2)    # 🔥 MÁS LENTO (clave)
        self.b = random.uniform(2.0, 3.5)

        # 🔥 IMPORTANTE: tiempo de reacción humano
        self.tiempo_reaccion = random.uniform(0.8, 1.5)

        # Métricas
        self.tiempo_parado = 0.0
        self.tiempo_espera = 0.0

        # Dimensión física
        self.largo = 4.5  # 🚗 más realista que 2m

    def actualizar(self, dt):
        self.posicion_anterior = self.posicion

        # Integración
        self.velocidad += self.aceleracion * dt
        self.velocidad = max(0.0, self.velocidad)

        self.posicion += self.velocidad * dt

        # Estado de parada
        if self.velocidad <= 0.1:
            self.tiempo_parado += dt
            self.tiempo_espera += dt
        else:
            self.tiempo_parado = 0.0