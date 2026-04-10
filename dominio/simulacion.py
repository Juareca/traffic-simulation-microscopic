"""Simulación microscópica de tráfico usando el modelo IDM.

Arquitectura por capas:
- Dominio: Vehiculo, Carretera, Carril, Semaforo, IDM, Métricas
- Aplicación: Simulacion (orquestador)
"""

import random
from dominio.carretera import Carretera
from dominio.vehiculo import Vehiculo
from dominio.idm import IDM
from dominio.metricas import Metricas
from dominio.semaforo import Semaforo


class Obstaculo:
    """Obstáculo fijo usado por el IDM (p.ej. semáforo en rojo)."""
    def __init__(self):
        self.velocidad = 0.0
        self.largo = 0.0


class Simulacion:
    """Controlador principal de la simulación microscópica."""

    RANGO_MAXIMO_POSICION = 150.0  # metros

    def __init__(self, ancho, alto, grosor, debug=False, seed=None):
        if seed is not None:
            random.seed(seed)

        self.debug = debug
        self.seed = seed
        self.tiempo = 0.0

        # Intervalo entre llegadas de vehículos
        self.intervalo_llegada = 1.0
        self.tiempo_ultimo_vehiculo = 0.0
        self.contador_ids = 1

        # Dominio
        self.idm = IDM()
        self.metricas = Metricas()
        self.obstaculo_fijo = Obstaculo()

        # Carreteras (4) con 2 carriles cada una
        self.carreteras = self._crear_carreteras(ancho, alto, grosor)

        # 4 semáforos: uno por dirección de carretera
        self.semaforos = {
            "S-N": Semaforo(40, 20, 2, 20),
            "N-S": Semaforo(40, 20, 2, 20),
            "O-E": Semaforo(40, 20, 2, 20),
            "E-O": Semaforo(40, 20, 2, 20),
        }

        # Lista global de vehículos (para métricas)
        self.vehiculos = []

        self._inicio_impreso = False

    # ------------------------------------------------------------------
    # Construcción de carreteras
    # ------------------------------------------------------------------
    def _crear_carreteras(self, ancho, alto, grosor):
        centro_x = ancho // 2
        centro_y = alto // 2

        return [
            # NORTE → SUR (vertical derecha)            
            Carretera(
                x=centro_x - grosor,
                y=0,
                ancho=grosor,
                alto=alto,
                direccion="N-S",
                num_carriles=2
            ),

            # SUR → NORTE (vertical izquierda)
            Carretera(
                x=centro_x,
                y=0,
                ancho=grosor,
                alto=alto,
                direccion="S-N",
                num_carriles=2
            ),

            # ESTE → OESTE (horizontal arriba)
            Carretera(
                x=0,
                y=centro_y - grosor,
                ancho=ancho,
                alto=grosor,
                direccion="E-O",
                num_carriles=2
            ),

            # OESTE → ESTE (horizontal abajo)
            Carretera(
                x=0,
                y=centro_y,
                ancho=ancho,
                alto=grosor,
                direccion="O-E",
                num_carriles=2
            ),
        ]

    # ------------------------------------------------------------------
    # Generación de vehículos
    # ------------------------------------------------------------------
    def _generar_vehiculo(self):
        carretera = random.choice(self.carreteras)
        carril = random.choice(carretera.carriles)

        nuevo = Vehiculo(
            id=self.contador_ids,
            posicion= -5.0,
            velocidad= random.uniform(1.0, 3.0)
        )
        nuevo.carril = carril

        carril.vehiculos.append(nuevo)
        self.vehiculos.append(nuevo)
        self.contador_ids += 1

    # ------------------------------------------------------------------
    # Limpieza de vehículos fuera de rango
    # ------------------------------------------------------------------
    def _limpiar_vehiculos(self):
        vehiculos_dentro = []
        vehiculos_salientes = []

        for v in self.vehiculos:
            if v.posicion > self.RANGO_MAXIMO_POSICION:
                vehiculos_salientes.append(v)
            else:
                vehiculos_dentro.append(v)

        self.vehiculos = vehiculos_dentro

        if vehiculos_salientes:
            self.metricas.guardar_vehiculos_salientes(vehiculos_salientes)
            ids_salientes = {v.id for v in vehiculos_salientes}

            for carretera in self.carreteras:
                for carril in carretera.carriles:
                    carril.vehiculos = [
                        v for v in carril.vehiculos if v.id not in ids_salientes
                    ]

    # ------------------------------------------------------------------
    # Debug
    # ------------------------------------------------------------------
    def _imprimir_info_inicio(self):
        if self._inicio_impreso:
            return
        self._inicio_impreso = True

        print("\n" + "=" * 60)
        print("🚗 TrafficSimulator IDM - Simulación Iniciada")
        print("=" * 60)
        print(f"Modo debug: {'ACTIVO' if self.debug else 'INACTIVO'}")
        print(f"Semilla: {self.seed}")
        print(f"IDM v₀={self.idm.v0} m/s | T={self.idm.T}s | a_max={self.idm.a_max} m/s²")
        print("=" * 60 + "\n")

    # ------------------------------------------------------------------
    # Paso de simulación
    # ------------------------------------------------------------------
    def paso(self, dt):
        if not self._inicio_impreso:
            self._imprimir_info_inicio()

        self.tiempo += dt

        # Actualizar todos los semáforos
        for sem in self.semaforos.values():
            sem.actualizar(dt)

        # Generar vehículos según intervalo
        if self.tiempo - self.tiempo_ultimo_vehiculo >= self.intervalo_llegada:
            self._generar_vehiculo()
            self.tiempo_ultimo_vehiculo = self.tiempo

        # Actualizar dinámica por carretera y carril
        for carretera in self.carreteras:
            semaforo = self.semaforos[carretera.direccion]
            semaforo_activo = semaforo.estado in ("rojo", "amarillo")

            for carril in carretera.carriles:
                vehs = carril.vehiculos
                vehs.sort(key=lambda v: v.posicion)

                for i, v in enumerate(vehs):
                    # Líder o seguidor
                    if i == len(vehs) - 1:
                        veh_adelante = None
                        distancia = float("inf")
                    else:
                        v_adelante = vehs[i + 1]
                        distancia = max(
                            v_adelante.posicion - v.posicion - v_adelante.largo,
                            0.1,
                        )
                        veh_adelante = v_adelante

                    # Semáforo como obstáculo (para esta carretera)
                    if semaforo_activo:
                        d = semaforo.posicion - v.posicion - v.largo
                        if 0 < d < distancia:
                            distancia = d
                            veh_adelante = self.obstaculo_fijo

                    # Aceleración IDM
                    v.aceleracion = self.idm.calcular_aceleracion(
                        v, veh_adelante, distancia
                    )

                # Actualizar estado de cada vehículo
                for v in vehs:
                    v.actualizar(dt)

        # Métricas
        self.metricas.actualizar_cola(self.vehiculos)
        cola, t_espera_actual, vel_prom = self.metricas.calcular_todas_metricas(
            self.vehiculos
        )
        t_espera_hist = self.metricas.tiempo_espera_promedio_historico()

        print(
            f"t={self.tiempo:5.1f}s | "
            f"Espera act={t_espera_actual:5.2f}s | "
            f"Hist={t_espera_hist:5.2f}s | "
            f"Cola={cola:4.1f} | "
            f"Vel={vel_prom:5.2f} m/s"
        )

        # Limpiar vehículos fuera de rango
        self._limpiar_vehiculos()
