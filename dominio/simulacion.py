"""Simulación microscópica de tráfico usando el modelo IDM.

Este módulo implementa la lógica principal de una simulación de tráfico
utilizando el Intelligent Driver Model (IDM), un modelo de seguimiento
de vehículos ampliamente aceptado en la investigación de transporte.

Attributes:
    Para cada vehículo en la simulación se registran:
    - Posición (metros)
    - Velocidad (m/s)
    - Aceleración (m/s²)
    - Tiempo de espera (segundos)
"""

import random
from dominio.vehiculo import Vehiculo
from dominio.semaforo import Semaforo
from dominio.idm import IDM
from dominio.metricas import Metricas
class Obstaculo:
    """Representa un obstáculo fijo (semáforo en rojo u otro vehículo detenido).
    
    Usado por el modelo IDM para simular comportamiento ante semáforos
    sin necesidad de crear instancias de vehículos reales.
    """
    def __init__(self):
        self.velocidad = 0  # m/s
        self.largo = 0      # metros
class Simulacion:
    """Simulación microscópica de tráfico usando modelo IDM."""
    
    # Rango máximo permitido para vehículos en la simulación
    # Vehículos que pasan esta posición se eliminarán para liberar memoria
    RANGO_MAXIMO_POSICION = 150  # metros
    
    def __init__(self, debug=False, seed=None):
        """Inicializa la simulación.
        
        Args:
            debug (bool): Si True, imprime información detallada en cada paso.
                         Si False, solo imprime métricas resumidas.
            seed (int|None): Semilla aleatoria para reproducibilidad.
                            Si es None, resultados son aleatorios.
                            Si es un número (ej: 42), siempre genera los
                            mismos resultados (mismo tiempo de reacción,
                            velocidades iniciales, intervalos de llegada).
                            
        Ejemplo:
            # Resultados aleatorios:
            sim = Simulacion(debug=False)
            
            # Resultados reproducibles:
            sim = Simulacion(debug=False, seed=42)
        """
        # Fijar semilla aleatoria si se especifica
        if seed is not None:
            random.seed(seed)
        
        self.intervalo_llegada = random.uniform(2, 5)  # tiempo entre llegadas de vehículos (2 a 5 segundos)
        self.tiempo_ultimo_vehiculo = 0
        self.contador_ids = 1
        self.debug = debug
        self.seed = seed  # Guardar para referencia

        self.idm = IDM()
        self.metricas = Metricas()
        
        # Obstáculo fijo reutilizable (para representar semáforos)
        self.obstaculo_fijo = Obstaculo()

        # Semáforo en posición 40m con ciclo: verde, amarillo, rojo
        self.semaforo = Semaforo(40, 20, 2, 20)
        self.vehiculos = []

        self.tiempo = 0
        self._inicio_impreso = False  # Control para imprimir info de inicio una sola vez

    def generar_vehiculo(self):
        """Crea un nuevo vehículo con parámetros aleatorios."""
        nuevo = Vehiculo(
            id=self.contador_ids,
            posicion=-5,   # aparece fuera de la vía visible
            velocidad= 2
        )

        self.vehiculos.append(nuevo)
        self.contador_ids += 1

    def limpiar_vehiculos(self):
        """Elimina vehículos que han salido del rango de simulación.
        
        Esto previene consumo indefinido de memoria al mantener solo
        los vehículos activos en la simulación.
        
        Antes de eliminar, guarda los datos en metricas para historial acumulativo.
        
        🚀 OPTIMIZADO: Una sola pasada sobre la lista en lugar de dos.
        """
        # Separar en una sola pasada: dentro vs fuera del rango
        vehiculos_dentro = []
        vehiculos_a_limpiar = []
        
        for v in self.vehiculos:
            if v.posicion > self.RANGO_MAXIMO_POSICION:
                vehiculos_a_limpiar.append(v)
            else:
                vehiculos_dentro.append(v)
        
        # Guardar sus datos antes de eliminar
        if vehiculos_a_limpiar:
            self.metricas.guardar_vehiculos_salientes(vehiculos_a_limpiar)
        
        # Actualizar lista (una sola asignación)
        self.vehiculos = vehiculos_dentro

    def _print_debug(self, *args, **kwargs):
        """Imprime mensaje de debug solo si el modo debug está activado."""
        if self.debug:
            print(*args, **kwargs)

    def _imprimir_info_inicio(self):
        """Imprime información de reproducibilidad al iniciar la simulación."""
        if self._inicio_impreso:
            return
        
        self._inicio_impreso = True
        
        print("\n" + "="*60)
        print("🚗 TrafficSimulator 2.0 - Simulación Iniciada")
        print("="*60)
        print(f"Modo debug: {'ACTIVO' if self.debug else 'INACTIVO'}")
        
        if self.seed is not None:
            print(f"Semilla aleatoria: {self.seed} (Resultados reproducibles)")
        else:
            print(f"Semilla aleatoria: NO FIJADA (Resultados aleatorios)")
        
        print("\nParámetros del modelo:")
        print(f"  IDM v₀: {self.idm.v0} m/s")
        print(f"  IDM T: {self.idm.T} s")
        print(f"  IDM a_max: {self.idm.a_max} m/s²")
        print(f"  Semáforo: Verde={self.semaforo.tiempo_verde}s, Amarillo={self.semaforo.tiempo_amarillo}s, Rojo={self.semaforo.tiempo_rojo}s")
        print("="*60 + "\n")

    def paso(self, dt):
        self.tiempo += dt

        # 🚦 actualizar semáforo
        self.semaforo.actualizar(dt)

        # 🚗 generar vehículos automáticamente
        if self.tiempo - self.tiempo_ultimo_vehiculo >= self.intervalo_llegada:
            self.generar_vehiculo()
            self.tiempo_ultimo_vehiculo = self.tiempo

        # 🚨 OPTIMIZACIÓN: Pre-calcular estado del semáforo una sola vez
        semaforo_activo = self.semaforo.esta_en_rojo() or self.semaforo.estado == "amarillo"
        
        for i in range(len(self.vehiculos)):
            v = self.vehiculos[i]

            # 🚗 vehículo adelante (acceso O(1) por índice)
            if i > 0:
                v_adelante = self.vehiculos[i - 1]

                distancia_vehiculo = (
                    v_adelante.posicion - v.posicion - v_adelante.largo
                )
                distancia_vehiculo = max(distancia_vehiculo, 0.1)

                # ⏱️ reacción humana (cola realista)
                if v.velocidad == 0 and v_adelante.velocidad > 0:
                    if v.tiempo_parado < v.tiempo_reaccion:
                        v.aceleracion = 0
                        v.actualizar(dt)
                        continue
            else:
                v_adelante = None
                distancia_vehiculo = float("inf")

            # 🚦 semáforo como obstáculo - OPTIMIZADO
            distancia_semaforo = float("inf")

            if semaforo_activo:
                offset = v.largo
                d = self.semaforo.posicion - v.posicion - offset

                if d > 0:
                    distancia_semaforo = d

            # 🔥 elegir obstáculo más cercano
            if distancia_semaforo < distancia_vehiculo:
                v_adelante = self.obstaculo_fijo
                distancia = distancia_semaforo
            else:
                distancia = distancia_vehiculo

            # 🧠 IDM
            v.aceleracion = self.idm.calcular_aceleracion(
                v, v_adelante, distancia
            )

            # actualizar vehículo
            v.actualizar(dt)

        # 🖨️ DEBUG (solo si está activado) - OPTIMIZADO
        if self.debug:
            print(f"\n⏱️ Tiempo: {self.tiempo:.1f}s")
            print(f"🚦 Semáforo: {self.semaforo.estado}")
            print("🚗 Vehículos:")
            for v in self.vehiculos:
                print(
                    f"  ID {v.id} | "
                    f"pos={v.posicion:.2f} m | "
                    f"vel={v.velocidad:.2f} m/s | "
                    f"espera={v.tiempo_espera:.1f}s"
                )

        # 📊 métricas (HISTÓRICAS - no disminuyen cuando vehículos salen)
        self.metricas.actualizar_cola(self.vehiculos)  # Registrar historial
        
        # 🚀 OPTIMIZACIÓN: Una sola pasada sobre vehículos en lugar de 3
        cola, t_espera_actual, vel_prom = self.metricas.calcular_todas_metricas(self.vehiculos)
        t_espera_hist = self.metricas.tiempo_espera_promedio_historico()  # Sin parámetros (verdaderamente histórico)

        # 📊 Mostrar métricas: espera actual vs histórica + cola + velocidad
        print(f"Espera (actual): {t_espera_actual:.2f}s | Espera (hist): {t_espera_hist:.2f}s | Cola: {cola:.2f} veh | Vel: {vel_prom:.2f} m/s")
        
        # 🗑️ Limpiar vehículos que salieron del rango - OPTIMIZADO
        self.limpiar_vehiculos()