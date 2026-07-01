import math
from dominio.vehiculo import Vehiculo
from dominio.config import IDM_T, IDM_A_MAX, IDM_B, IDM_S0, IDM_DELTA


class IDM:
    """Implementación optimizada del Intelligent Driver Model."""

    def __init__(self):
        # parámetros base (fallback / referencia)
        self.T = IDM_T
        self.a_max = IDM_A_MAX
        self.b = IDM_B
        self.s0 = IDM_S0
        self.delta = IDM_DELTA

    # ------------------------------------------------------------------
    # Aceleración IDM
    # ------------------------------------------------------------------
    def calcular_aceleracion(self, vehiculo, vehiculo_adelante, s):
        v = vehiculo.velocidad

        # parámetros individuales (si existen)
        v0 = getattr(vehiculo, "v0", 6.0)  # fallback razonable
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

        sqrt_term = 2 * math.sqrt(a_max * b)

        s_star = self.s0 + v * T + (v * delta_v) / sqrt_term

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
        # 🔹 4. Clamp físico
        # -------------------------------
        return max(-b * 2, min(a, a_max))

    # ------------------------------------------------------------------
    # Distancia mínima para generación
    # ------------------------------------------------------------------
    def distancia_deseada_minima(self, velocidad, T=1.2):
        return self.s0 + velocidad * T
