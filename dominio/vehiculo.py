"""Modelado de comportamiento vehicular y dinámica.

Este módulo define la clase Vehiculo que representa un vehículo
individual en la simulación, incluyendo su estado dinámico y
comportamiento de reacción ante obstáculos.
"""

import random

class Vehiculo:
    """Representa un vehículo en la simulación de tráfico.
    
    Atributos de clase (parámetros globales del vehículo):
        - v0: Velocidad deseada en m/s (shared por todos los vehículos)
    
    Atributos de instancia (estado individual):
        - Posición y velocidad
        - Aceleración (calculada por modelo IDM)
        - Tiempos de parada y espera (para métricas)
        - Tiempo de reacción humano (variable aleatoria)
    """
    v0 = 9  # Velocidad deseada (m/s) - parámetro global compartido
    
    def __init__(self, id, posicion=0, velocidad=0):
        """Inicializa un nuevo vehículo.
        
        Args:
            id (int): Identificador único del vehículo
            posicion (float): Posición inicial en metros (default: 0)
            velocidad (float): Velocidad inicial en m/s (default: 0)
        
        Note:
            Cada vehículo hereda v0 de la clase, pero puede tener su propia
            velocidad inicial diferente.
        """
        self.id = id
        self.posicion = posicion  # metros
        self.posicion_anterior = posicion
        self.velocidad = velocidad  # m/s
        self.aceleracion = 0  # m/s^2 (calculada por IDM)

        # comportamiento humano - tiempo de reacción variable
        # rango típico: 0.8-1.5 segundos (Reaction Time Studies)
        self.tiempo_reaccion = random.uniform(1.5, 2.0)
        self.tiempo_parado = 0  # segundos en parada actual
        self.tiempo_espera = 0  # acumulado total de espera

        # dimensiones físicas
        self.largo = 2  # metros (tamaño típico de automóvil)

    def actualizar(self, dt):
        """Actualiza estado del vehículo en un paso temporal.
        
        Implementa integración numérica simple (Euler) de ecuaciones de movimiento:
            v(t+dt) = v(t) + a(t)*dt
            x(t+dt) = x(t) + v(t+dt)*dt
        
        Args:
            dt (float): Intervalo temporal en segundos
            
        Notas:
            - La velocidad nunca puede ser negativa (v >= 0)
            - Registra tiempos de parada para cálculo de métricas
            - Compatible con integradores más sofisticados si es necesario
        """
        # dinámica
        self.velocidad += self.aceleracion * dt
        self.velocidad = max(self.velocidad, 0)

        self.posicion += self.velocidad * dt

        # tiempo parado (para reacción)
        if self.velocidad <= 0.1:
            self.tiempo_parado += dt
            self.tiempo_espera += dt
        else:
            self.tiempo_parado = 0