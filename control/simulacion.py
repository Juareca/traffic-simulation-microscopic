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
from control.controlador_semaforos import ControladorSemaforos
from dominio.config import ESCALA

class Obstaculo:
    """Obstáculo fijo usado por el IDM (p.ej. semáforo en rojo o línea de cebra)."""
    def __init__(self):
        self.velocidad = 0.0
        self.largo = 0.0


class Simulacion:
    """Controlador principal de la simulación microscópica."""

    ESCALA = ESCALA  # pixeles por metro CONFIG.PY
    DISTANCIA_FRENADO_CEBRA = 3.0  # metros antes de la línea blanca

    def __init__(self, ancho, alto, grosor, debug=False, seed=None):
        # Guardar tamaño de pantalla
        self.ancho_pantalla = ancho
        self.alto_pantalla = alto

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
            "S-N": Semaforo(40),
            "N-S": Semaforo(40),
            "O-E": Semaforo(40),
            "E-O": Semaforo(40),
        }

        # Controlador de fases semafóricas
        self.controlador_semaforos = ControladorSemaforos(
            semaforos={
                "NS": self.semaforos["N-S"],
                "SN": self.semaforos["S-N"],
                "EO": self.semaforos["E-O"],
                "OE": self.semaforos["O-E"],
            },
            tiempos={
                "NS": {"verde": 20, "amarillo": 3},
                "SN": {"verde": 20, "amarillo": 3},
                "EO": {"verde": 20, "amarillo": 3},
                "OE": {"verde": 20, "amarillo": 3},
            }
        )

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
            Carretera(centro_x - grosor, 0, grosor, alto, "N-S", 2),
            Carretera(centro_x, 0, grosor, alto, "S-N", 2),
            Carretera(0, centro_y - grosor, ancho, grosor, "E-O", 2),
            Carretera(0, centro_y, ancho, grosor, "O-E", 2),
        ]

    # ------------------------------------------------------------------
    # Generación de vehículos
    # ------------------------------------------------------------------
    def _generar_vehiculo(self):
        carretera = random.choice(self.carreteras)
        carril = random.choice(carretera.carriles)

        nuevo = Vehiculo(
            id=self.contador_ids,
            posicion=-5.0,
            velocidad=Vehiculo.v0
        )
        nuevo.carril = carril

        carril.vehiculos.append(nuevo)
        self.vehiculos.append(nuevo)
        self.contador_ids += 1

    # ------------------------------------------------------------------
    # Limpieza de vehículos fuera de pantalla
    # ------------------------------------------------------------------
    def _limpiar_vehiculos(self):
        vehiculos_dentro = []
        vehiculos_salientes = []

        for v in self.vehiculos:
            carril = v.carril
            carretera = carril.carretera
            direccion = carretera.direccion

            pos_px = v.posicion * self.ESCALA

            # POSICIÓN EN PANTALLA
            if direccion == "N-S":
                x_px = carretera.x + carretera.ancho // 2
                y_px = carretera.y + pos_px

            elif direccion == "S-N":
                x_px = carretera.x + carretera.ancho // 2
                y_px = carretera.y + carretera.alto - pos_px

            elif direccion == "E-O":
                x_px = carretera.x + pos_px
                y_px = carretera.y + carretera.alto // 2

            else:  # "O-E"
                x_px = carretera.x + carretera.ancho - pos_px
                y_px = carretera.y + carretera.alto // 2

            # ELIMINACIÓN SEGÚN PANTALLA
            if (
                x_px < -50 or x_px > self.ancho_pantalla + 50 or
                y_px < -50 or y_px > self.alto_pantalla + 50
            ):
                vehiculos_salientes.append(v)
            else:
                vehiculos_dentro.append(v)

        # Actualizar listas
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

        # Actualizar semáforos
        self.controlador_semaforos.actualizar(dt)

        # Generar vehículos
        if self.tiempo - self.tiempo_ultimo_vehiculo >= self.intervalo_llegada:
            self._generar_vehiculo()
            self.tiempo_ultimo_vehiculo = self.tiempo

        # Dinámica por carretera
        for carretera in self.carreteras:
            semaforo = self.semaforos[carretera.direccion]

            for carril in carretera.carriles:
                vehs = carril.vehiculos
                vehs.sort(key=lambda v: v.posicion)

                for i, v in enumerate(vehs):
                    # Líder
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

                    # Frenado por cebra
                    pos_cruce_pixeles = carretera.pos_cruce
                    pos_cruce_metros = pos_cruce_pixeles / self.ESCALA

                    offset_pixeles = 70
                    offset_metros = offset_pixeles / self.ESCALA

                    pos_linea_blanca = pos_cruce_metros - offset_metros
                    pos_parada = pos_linea_blanca - self.DISTANCIA_FRENADO_CEBRA

                    d_cebra = pos_parada - v.posicion - v.largo

                    if semaforo.estado == "rojo" and 0 < d_cebra < distancia:
                        distancia = d_cebra
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

        # Limpiar vehículos fuera de pantalla
        self._limpiar_vehiculos()
