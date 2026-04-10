"""Modelo Intelligent Driver Model (IDM) para comportamiento vehicular.

El IDM es un modelo microscópico de tráfico que describe el comportamiento
de aceleración/desaceleración de vehículos basado en:
    1. Velocidad deseada (v0) - TOMADA DE LA CLASE VEHICULO
    2. Distancia al vehículo adelante
    3. Diferencia de velocidades

Ecuación IDM:
    a_n(t) = a_max * [1 - (v/v0)^δ - (s*/s)^2]

Donde:
    s* = distancia deseada = s0 + v*T + (v*Δv)/(2*√(a_max*b))

Referencia:
    Treiber, M., Hennecke, A., & Helbing, D. (2000).
    "Congested traffic states in empirical observations and microscopic traffic models."
    Physical Review E, 62(2), 1805.

Integración con Vehiculo:
    - v0 se obtiene de Vehiculo.v0 (parámetro global compartido)
    - Para cambiar v0: editar Vehiculo.v0 = nuevo_valor
"""

import math
from dominio.vehiculo import Vehiculo

class IDM:
    """Implementación del Intelligent Driver Model.
    
    Parámetros integrados con la clase Vehiculo.
    """
    
    def __init__(self):
        """Inicializa los parámetros del modelo IDM.
        
        Los parámetros se toman de:
        - v0: De la clase Vehiculo (Vehiculo.v0 - parámetro global)
        - Resto: Valores típicos para tráfico urbano
        
        Atributos:
            v0 (float): Velocidad deseada en m/s (DESDE Vehiculo.v0)
            T (float): Tiempo de reacción/brecha temporal en segundos
            a_max (float): Aceleración máxima en m/s² (típico: 1-3)
            b (float): Desaceleración cómoda en m/s² (típico: 1-5)
            s0 (float): Distancia mínima segura en metros
            delta (float): Exponente para término de velocidad (típico: 4)
        
        Ejemplo de cambio global:
            # Cambiar v0 para TODOS los vehículos:
            Vehiculo.v0 = 10
            idm = IDM()  # Ahora usa v0=10
        """
        # Obtener v0 de la clase Vehiculo (parámetro global compartido)
        self.v0 = Vehiculo.v0         # velocidad deseada (m/s) 
        self.T = 1.5                  # tiempo de reacción (s)
        self.a_max = 2                # aceleración máxima (m/s^2)
        self.b = 5                    # desaceleración cómoda (m/s^2)
        self.s0 = 6                   # distancia mínima (m)
        self.delta = 4                # exponente
        
        # 🚀 CACHÉ para evitar recálculos costosos
        self._sqrt_cache = 2 * math.sqrt(self.a_max * self.b)  # Pre-calcular sqrt una sola vez

    def calcular_aceleracion(self, vehiculo, vehiculo_adelante, s):
        """Calcula la aceleración del vehículo usando el modelo IDM.
        
        Args:
            vehiculo (Vehiculo): Vehículo para el cual calcular aceleración
            vehiculo_adelante (Vehiculo|Obstaculo|None): Vehículo adelante o None
            s (float): Distancia al obstáculo adelante en metros
            
        Returns:
            float: Aceleración en m/s²
            
        Notas:
            - Si s=∞ (vía libre), el segundo término = 0
            - Si vehiculo_adelante=None, retorna aceleración libre
            - Maneja casos numéricos extremos con safety margins
            - 🚀 USA CACHÉ DE SQRT PARA OPTIMIZACIÓN
        """
        v = vehiculo.velocidad

        # vía libre
        if vehiculo_adelante is None:
            return self.a_max * (1 - (v / self.v0) ** self.delta)

        # Δv = v_n - v_n-1
        delta_v = v - vehiculo_adelante.velocidad

        # s* (distancia dinámica deseada) - OPTIMIZADO: usa sqrt cacheado
        s_star = self.s0 + v * self.T + (v * delta_v) / self._sqrt_cache

        # evitar errores numéricos
        s = max(s, 0.1)

        # ecuación IDM
        a = self.a_max * (
            1 - (v / self.v0) ** self.delta
            - (s_star / s) ** 2
        )

        return a