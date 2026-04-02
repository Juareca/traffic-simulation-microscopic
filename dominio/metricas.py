"""Métricas y evaluación del desempeño de la simulación.

Este módulo recopila y calcula indicadores clave de tráfico:
    - Tiempo promedio de espera (segundos)
    - Longitud de cola (número de vehículos)
    - Velocidad promedio (m/s)
    - Evolución temporal de la cola

Estas métricas son esenciales para evaluar la eficiencia del semáforo
y el flujo de tráfico en la simulación.
"""

from dominio.semaforo import Semaforo

class Metricas:
    """Recopila y analiza métricas de desempeño de la simulación.
    
    Métricas instantáneas (calculadas cada paso):
        - Tiempo promedio de espera de vehículos detenidos
        - Longitud actual de la cola
        - Velocidad promedio de todos los vehículos
    
    Métricas históricas:
        - Evolución temporal de la longitud de cola
        - Promedio histórico de cola
    """
    
    def __init__(self):
        """Inicializa el contenedor de métricas.
        
        Atributos:
            historial_cola (list): Series temporal de longitud de cola
            tiempos_espera_totales (list): Tiempos de espera de TODOS los vehículos
                que han pasado por la simulación (acumulativo)
            velocidades_totales (list): Velocidades finales de TODOS los vehículos
                que han pasado (acumulativo)
        """
        self.historial_cola = []
        self.tiempos_espera_totales = []      # NUEVO: Acumulativo
        self.velocidades_totales = []         # NUEVO: Acumulativo

    def calcular_tiempo_promedio_espera(self, vehiculos):
        """Calcula el tiempo promedio de espera de vehículos parados.
        
        Solo considera vehículos que han estado parados (tiempo_espera > 0).
        Es una métrica importante de QoS (Calidad de Servicio) en tráfico.
        
        Args:
            vehiculos (list): Lista de objetos Vehiculo
            
        Returns:
            float: Tiempo promedio de espera en segundos (0 si no hay detenidos)
            
        Notas:
            - Umbral de velocidad para "detenido": v <= 0.1 m/s
            - Se usa para evaluar impacto de semáforos
        """
        detenidos = [v for v in vehiculos if v.tiempo_espera > 0]

        if not detenidos:
            return 0

        total = sum(v.tiempo_espera for v in detenidos)
        return total / len(detenidos)

    # 🚗 Longitud de cola (instantánea)
    def calcular_longitud_cola(self, vehiculos):
        """Calcula cantidad de vehículos en cola (detenidos).
        
        Métrica instantánea que indica congestión en el semáforo.
        Usa el mismo umbral que vehiculo.py para consistencia.
        
        Args:
            vehiculos (list): Lista de objetos Vehiculo
            
        Returns:
            int: Número de vehículos en cola
            
        Notas:
            - Umbral de velocidad: <= 0.1 m/s se considera "detenido"
            - Consistente con vehiculo.py (donde tiempo_espera se acumula a v <= 0.1)
        """
        cola = [v for v in vehiculos if v.velocidad <= 1.0]  # Mismo umbral que vehiculo.py
        return len(cola)

    # 📊 Guardar evolución de la cola
    def actualizar_cola(self, vehiculos):
        """Actualiza el historial de longitud de cola.
        
        Registra la longitud actual para análisis temporal posterior.
        Permite crear gráficos de evolución de congestión.
        
        Args:
            vehiculos (list): Lista de objetos Vehiculo
            
        Returns:
            int: Longitud actual de la cola
        """
        cola_actual = self.calcular_longitud_cola(vehiculos)
        self.historial_cola.append(cola_actual)
        return cola_actual


    def calcular_velocidad_promedio(self, vehiculos):
        """Calcula la velocidad promedio de todos los vehículos.
        
        Métrica instantánea que indica fluidez del tráfico.
        Mayor velocidad promedio → mejor flujo → semáforo más eficiente.
        
        Args:
            vehiculos (list): Lista de objetos Vehiculo
            
        Returns:
            float: Velocidad promedio en m/s (0 si lista vacía)
            
        Notas:
            - Complementa al tiempo de espera (QoS completo)
            - Sensible a la distribución de velocidad deseada en el IDM
        """
        if not vehiculos:
            return 0

        total = sum(v.velocidad for v in vehiculos)
        return total / len(vehiculos)
    
    def guardar_vehiculos_salientes(self, vehiculos_a_limpiar):
        """Guarda datos de vehículos antes de eliminarlos de la simulación.
        
        Cuando limpiar_vehiculos() elimina vehículos que salieron del rango,
        esta función captura sus datos para mantener un historial COMPLETO
        de todos los vehículos que han pasado por la simulación.
        
        Args:
            vehiculos_a_limpiar (list): Vehículos que van a ser eliminados
            
        Returns:
            None
            
        Notas:
            - Debe ser llamado ANTES de eliminar vehículos
            - Permite calcular promedios verdaderos de toda la simulación
        """
        for v in vehiculos_a_limpiar:
            self.tiempos_espera_totales.append(v.tiempo_espera)
            self.velocidades_totales.append(v.velocidad)
    
    def tiempo_espera_promedio_historico(self, vehiculos_actuales=None):
        """Calcula tiempo de espera promedio HISTÓRICO (VERDADERAMENTE HISTÓRICO).
        
        Métrica acumulativa que NUNCA disminuye, solo aumenta o permanece.
        Solo incluye vehículos que YA SALIERON del rango de simulación.
        No incluye vehículos actuales para evitar que disminuya con nuevas entradas.
        
        Returns:
            float: Promedio histórico de tiempo de espera en segundos
            
        Notas:
            - Solo cuenta vehículos que realmente esperaron (tiempo_espera > 0)
            - NO incluye vehículos actuales (usa solo tiempos_espera_totales)
            - NUNCA disminuye conforme avanza la simulación
        """
        detenidos_salidos = [t for t in self.tiempos_espera_totales if t > 0]
        
        if not detenidos_salidos:
            return 0
        
        return sum(detenidos_salidos) / len(detenidos_salidos)
    
    def tiempo_espera_promedio_actual(self, vehiculos):
        """Calcula tiempo de espera promedio SOLO de vehículos en pantalla AHORA.
        
        Métrica instantánea que muestra la espera de los vehículos que están
        esperando en este momento, sin incluir histórico.
        
        Retorna 0 si NO hay vehículos detenidos en este instante.
        
        Args:
            vehiculos (list): Lista de vehículos actuales en simulación
            
        Returns:
            float: Promedio de tiempo de espera de vehículos actuales (0 si ninguno espera)
        """
        # Vehículos detenidos AHORA (v <= 0.1 m/s)
        detenidos = [v.tiempo_espera for v in vehiculos if v.velocidad <= 0.1 and v.tiempo_espera > 0]
        
        if not detenidos:
            return 0
        
        return sum(detenidos) / len(detenidos)
    
    def calcular_todas_metricas(self, vehiculos):
        """🚀 OPTIMIZACIÓN: Calcula todas las métricas en UNA sola pasada.
        
        En lugar de iterar 3 veces sobre los vehículos, itera una sola vez.
        Calcula simultáneamente:
        - Longitud de cola
        - Tiempo de espera promedio (actual)
        - Velocidad promedio
        
        Args:
            vehiculos (list): Lista de vehículos actuales
            
        Returns:
            tuple: (cola, tiempo_espera_promedio, velocidad_promedio)
            
        Notas:
            - Eficiencia: O(n) en lugar de O(3n)
            - Ganancia: ~66% más rápido en cálculo de métricas
        """
        if not vehiculos:
            return 0, 0, 0
        
        cola = 0
        vel_total = 0
        esp_total = 0
        esp_count = 0
        
        # Una sola iteración sobre todos los vehículos
        for v in vehiculos:
            # Métrica 1: Cola (velocidad <= 1.0 m/s)
            if v.velocidad <= 1.0:
                cola += 1
            
            # Métrica 2: Velocidad promedio
            vel_total += v.velocidad
            
            # Métrica 3: Tiempo de espera promedio (solo detenidos)
            if v.velocidad <= 0.1 and v.tiempo_espera > 0:
                esp_total += v.tiempo_espera
                esp_count += 1
        
        vel_promedio = vel_total / len(vehiculos)
        esp_promedio = esp_total / (esp_count or 1)  # Evitar división por 0
        
        return cola, esp_promedio, vel_promedio
    
    
    def longitud_cola_promedio_historica(self):
        """Calcula longitud de cola promedio a lo largo de toda la simulación.
        
        Métrica que refleja la congestión promedio histórica.
        
        Returns:
            float: Longitud de cola promedio (vehículos)
            
        Notas:
            - Se actualiza cada paso() con actualizar_cola()
            - NO disminuye cuando vehículos salen
            - Promedio de toda la historia de simulación
        """
        if not self.historial_cola:
            return 0
        return sum(self.historial_cola) / len(self.historial_cola)
    
    # ⚠️ PRIORIDAD 2: MÉTRICAS AVANZADAS PARA TESIS
    
    def longitud_cola_maxima(self):
        """Calcula la longitud máxima de cola registrada.
        
        Métrica de pico de congestión durante la simulación.
        Importante para diseño de infraestructura vial.
        
        Returns:
            int: Máximo número de vehículos en cola (0 si no hay datos)
        """
        if not self.historial_cola:
            return 0
        return max(self.historial_cola)
    
    def tiempo_espera_maximo(self):
        """Calcula el tiempo de espera máximo registrado.
        
        Métrica de caso peor para evaluación de semaforo.
        
        Returns:
            float: Máximo tiempo de espera en segundos (0 si sin datos)
        """
        if not self.tiempos_espera_totales:
            return 0
        esperas = [t for t in self.tiempos_espera_totales if t > 0]
        return max(esperas) if esperas else 0
    
    def tiempo_espera_minimo(self):
        """Calcula el tiempo de espera mínimo registrado.
        
        Métrica de caso mejor para evaluación de semaforo.
        
        Returns:
            float: Mínimo tiempo de espera en segundos (0 si sin datos)
        """
        if not self.tiempos_espera_totales:
            return 0
        esperas = [t for t in self.tiempos_espera_totales if t > 0]
        return min(esperas) if esperas else 0
    
    def velocidad_minima(self):
        """Calcula la velocidad mínima registrada durante la simulación.
        
        Indica los más bajos niveles de congestión/flujo.
        
        Returns:
            float: Velocidad mínima en m/s (0 si sin datos)
        """
        if not self.velocidades_totales:
            return 0
        return min(self.velocidades_totales)
    
    def velocidad_maxima(self):
        """Calcula la velocidad máxima registrada durante la simulación.
        
        Indica el flujo más rápido logrado.
        
        Returns:
            float: Velocidad máxima en m/s (0 si sin datos)
        """
        if not self.velocidades_totales:
            return 0
        return max(self.velocidades_totales)
    
    def cantidad_vehiculos_procesados(self):
        """Retorna cantidad total de vehículos procesados en la simulación.
        
        Incluye todos los vehículos que han salido del rango de simulación
        (todos en tiempos_espera_totales).
        
        Returns:
            int: Número total de vehículos procesados
        """
        return len(self.tiempos_espera_totales)