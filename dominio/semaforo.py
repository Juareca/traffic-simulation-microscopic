"""Control de semáforos y ciclos de tráfico.

Este módulo implementa un semáforo simple con tres estados
(verde → amarillo → rojo) que afecta el comportamiento de los vehículos
cercanos en la simulación.
"""

class Semaforo:
    """Representa un semáforo controlando el flujo de tráfico.
    
    Ciclo de estados:
        VERDE (duración: tiempo_verde) → AMARILLO → ROJO → VERDE
    
    Los vehículos reaccionan al semáforo mediante el modelo IDM,
    tratándolo como un obstáculo con velocidad = 0 cuando está en rojo/amarillo.
    """
    
    def __init__(self, posicion, tiempo_verde, tiempo_amarillo, tiempo_rojo):
        """Inicializa un semáforo con ciclo temporizado.
        
        Args:
            posicion (float): Ubicación en la carretera en metros
            tiempo_verde (float): Duración fase verde en segundos
            tiempo_amarillo (float): Duración fase amarilla en segundos
            tiempo_rojo (float): Duración fase roja en segundos
            
        Ejemplo:
            semaforo = Semaforo(posicion=40, tiempo_verde=25, 
                               tiempo_amarillo=3, tiempo_rojo=22)
        """
        self.posicion = posicion
        self.tiempo_verde = tiempo_verde
        self.tiempo_amarillo = tiempo_amarillo
        self.tiempo_rojo = tiempo_rojo

        self.estado = "verde"  # estado inicial
        self.tiempo_actual = 0  # contador dentro de la fase actual

    def actualizar(self, dt):
        """Avanza el semáforo en el ciclo temporal.
        
        Máquina de estados para ciclo de semáforo:
            - VERDE: dura tiempo_verde segundos
            - AMARILLO: dura tiempo_amarillo segundos  
            - ROJO: dura tiempo_rojo segundos
        
        Args:
            dt (float): Intervalo temporal en segundos
        """
        self.tiempo_actual += dt

        if self.estado == "verde" and self.tiempo_actual >= self.tiempo_verde:
            self.estado = "amarillo"
            self.tiempo_actual = 0

        elif self.estado == "amarillo" and self.tiempo_actual >= self.tiempo_amarillo:
            self.estado = "rojo"
            self.tiempo_actual = 0

        elif self.estado == "rojo" and self.tiempo_actual >= self.tiempo_rojo:
            self.estado = "verde"
            self.tiempo_actual = 0

    def esta_en_rojo(self):
        """Retorna True si el semáforo está en fase roja.
        
        Returns:
            bool: True si estado == "rojo"
        """
        return self.estado == "rojo"

    def esta_en_amarillo(self):
        """Retorna True si el semáforo está en fase amarilla.
        
        Returns:
            bool: True si estado == "amarillo"
        """
        return self.estado == "amarillo"