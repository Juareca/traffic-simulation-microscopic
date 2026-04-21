import math
from dominio.vehiculo import Vehiculo


class IDM:
    """Implementación optimizada del Intelligent Driver Model."""

    def __init__(self):
        # parámetros base (fallback / referencia)
        self.v0 = Vehiculo.v0
        self.T = 1.5
        self.a_max = 2.0
        self.b = 5.0
        self.s0 = 6.0
        self.delta = 4

    # ------------------------------------------------------------------
    # Aceleración IDM
    # ------------------------------------------------------------------
    def calcular_aceleracion(self, vehiculo, vehiculo_adelante, s):
        v = vehiculo.velocidad

        # parámetros individuales (si existen)
        v0 = getattr(vehiculo, "v0", self.v0)
        T = getattr(vehiculo, "T", self.T)
        a_max = getattr(vehiculo, "a_max", self.a_max)
        b = getattr(vehiculo, "b", self.b)

        # proteger valores extremos
        v0 = max(v0, 0.1)
        b = max(b, 0.1)

        # -------------------------------
        # 🔹 1. Movimiento libre
        # -------------------------------
        if vehiculo_adelante is None:
            return a_max * (1 - (v / v0) ** self.delta)

        # -------------------------------
        # 🔹 2. Interacción con líder
        # -------------------------------
        delta_v = v - vehiculo_adelante.velocidad

        # evitar sqrt repetido innecesario
        sqrt_term = 2 * math.sqrt(a_max * b)

        # distancia deseada dinámica
        s_star = self.s0 + v * T + (v * delta_v) / sqrt_term

        # evitar división peligrosa
        s = max(s, 0.1)
        s_star = max(s_star, self.s0)

        # -------------------------------
        # 🔹 3. Ecuación IDM
        # -------------------------------
        a = a_max * (
            1
            - (v / v0) ** self.delta
            - (s_star / s) ** 2
        )

        # -------------------------------
        # 🔹 4. Clamp físico (MUY IMPORTANTE)
        # -------------------------------
        return max(-b * 2, min(a, a_max))

    # ------------------------------------------------------------------
    # Distancia mínima para generación
    # ------------------------------------------------------------------
    def distancia_deseada_minima(self, velocidad, T=1.2):
        """
        Distancia segura sin interacción (Δv = 0).
        Usada para generación de vehículos.

        T más bajo que el real → evita bloqueos en spawn.
        """
        return self.s0 + velocidad * T