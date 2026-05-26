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
from dominio import config


class Obstaculo:
    """Obstáculo fijo usado por el IDM (p.ej. semáforo en rojo o línea de cebra)."""
    def __init__(self):
        self.velocidad = 0.0
        self.largo = 0.0

class Simulacion():

    ESCALA = config.ESCALA
    DISTANCIA_FRENADO_CEBRA = config.DISTANCIA_FRENADO_CEBRA

    def __init__(self, ancho, alto, grosor, debug=False, seed=None):

        self.ancho_pantalla = ancho
        self.alto_pantalla = alto

        if seed is not None:
            random.seed(seed)

        self.en_ejecucion = True

        self.debug = debug
        self.seed = seed
        self.tiempo = 0.0

        self.contador_ids = 1

        self.idm = IDM()

        self.carreteras = self._crear_carreteras(ancho, alto, grosor)
        self.metricas = Metricas(self.carreteras)

        self.obstaculo_fijo = Obstaculo()

        # Semáforos
        self.semaforos = {
            "S-N": Semaforo(config.SEMAFORO_POSICION),
            "N-S": Semaforo(config.SEMAFORO_POSICION),
            "O-E": Semaforo(config.SEMAFORO_POSICION),
            "E-O": Semaforo(config.SEMAFORO_POSICION),
        }

        # 🔥 Tasa de tráfico (veh/min por dirección) - DATOS REALES PARA GEH
        self.trafico_por_direccion = {
            "N-S": config.TRAFICO_NORTE_SUR,
            "S-N": config.TRAFICO_SUR_NORTE,
            "E-O": config.TRAFICO_ESTE_OESTE,
            "O-E": config.TRAFICO_OESTE_ESTE
        }

        self.acumulador_generacion = {
            d: 0.0 for d in self.trafico_por_direccion
        }

        self.controlador_semaforos = ControladorSemaforos(
            semaforos={
                "N-S": self.semaforos["N-S"],
                "S-N": self.semaforos["S-N"],
                "E-O": self.semaforos["E-O"],
                "O-E": self.semaforos["O-E"],
            },
            tiempos={
                "N-S": {"verde": config.NORTE_SUR_TIEMPO_VERDE, "amarillo": config.SEMAFORO_TIEMPO_AMARILLO},
                "S-N": {"verde": config.SUR_NORTE_TIEMPO_VERDE, "amarillo": config.SEMAFORO_TIEMPO_AMARILLO},
                "E-O": {"verde": config.ESTE_OESTE_TIEMPO_VERDE, "amarillo": config.SEMAFORO_TIEMPO_AMARILLO},
                "O-E": {"verde": config.OESTE_ESTE_TIEMPO_VERDE, "amarillo": config.SEMAFORO_TIEMPO_AMARILLO},
            }
        )

        self.vehiculos = []
        self._inicio_impreso = False
    
    def iniciar(self):
        self.en_ejecucion = True

    def pausar(self):
        self.en_ejecucion = False

    def reiniciar(self):
        self.tiempo = 0.0
        self.vehiculos = []

        for carretera in self.carreteras:
            for carril in carretera.carriles:
                carril.vehiculos = []

        self.metricas.reiniciar()

        for sem in self.semaforos.values():
            sem.reiniciar()

        self.en_ejecucion = True   

    def cambiar_velocidad(self, factor):
        """Actualiza la velocidad de simulación en la capa de dominio."""
        config.VELOCIDAD_SIMULACION = factor

    # -------------------------------------------------------------
    def _crear_carreteras(self, ancho, alto, grosor):
        cx = ancho // 2
        cy = alto // 2

        return [
            Carretera(cx - grosor, 0, grosor, alto,  config.CARRILES_POR_CARRETERA, "N-S"),
            Carretera(cx, 0, grosor, alto, config.CARRILES_POR_CARRETERA, "S-N"),
            Carretera(0, cy - grosor, ancho, grosor, config.CARRILES_POR_CARRETERA, "E-O"),
            Carretera(0, cy, ancho, grosor, config.CARRILES_POR_CARRETERA, "O-E"),
        ]

    # -------------------------------------------------------------
    def _crear_vehiculo(self, velocidad, carril, v0=None):

        if v0 is None:
            v0 = random.uniform(config.V0_MIN, config.V0_MAX)

        nuevo = Vehiculo(
            id=self.contador_ids,
            posicion=0.0,
            velocidad=velocidad
        )

        nuevo.v0 = v0
        nuevo.T = random.uniform(config.T_SPAWN_MIN, config.T_SPAWN_MAX)
        nuevo.a_max = random.uniform(config.A_MAX_SPAWN_MIN, config.A_MAX_SPAWN_MAX)
        nuevo.b = random.uniform(config.B_MIN, config.B_MAX)

        nuevo.carril = carril

        carril.vehiculos.append(nuevo)
        self.vehiculos.append(nuevo)
        self.contador_ids += 1

        return True

    # -------------------------------------------------------------
    def _generar_vehiculo_en_carretera(self, carretera):
        carriles = carretera.carriles[:]
        random.shuffle(carriles)

        for carril in carriles:

            if not carril.vehiculos:
                v0 = random.uniform(config.V0_MIN, config.V0_MAX)
                return self._crear_vehiculo(v0, carril, v0=v0)

            primer = min(carril.vehiculos, key=lambda v: v.posicion)

            v0 = random.uniform(config.V0_MIN, config.V0_MAX)
            velocidad = min(primer.velocidad, v0)
            velocidad = max(config.VELOCIDAD_MINIMA, velocidad)

            gap = self.idm.s0 + velocidad * config.T_SPAWN

            if primer.posicion <= gap:
                continue

            return self._crear_vehiculo(velocidad, carril, v0=v0)

        return False

    # -------------------------------------------------------------
    def _evaluar_cambio_de_carril(self, vehiculo):
        pass

    # -------------------------------------------------------------
    def _limpiar_vehiculos(self):

        dentro = []
        fuera = []

        for v in self.vehiculos:
            carril = v.carril
            carretera = carril.carretera
            d = carretera.direccion

            pos_px = v.posicion * self.ESCALA

            if d == "N-S":
                x = carretera.x + carretera.ancho // 2
                y = carretera.y + pos_px
            elif d == "S-N":
                x = carretera.x + carretera.ancho // 2
                y = carretera.y + carretera.alto - pos_px
            elif d == "E-O":
                x = carretera.x + pos_px
                y = carretera.y + carretera.alto // 2
            else:
                x = carretera.x + carretera.ancho - pos_px
                y = carretera.y + carretera.alto // 2

            if (x < -config.MARGEN_LIMPIEZA_VEHICULOS or 
                x > self.ancho_pantalla + config.MARGEN_LIMPIEZA_VEHICULOS or 
                y < -config.MARGEN_LIMPIEZA_VEHICULOS or 
                y > self.alto_pantalla + config.MARGEN_LIMPIEZA_VEHICULOS):
                fuera.append(v)
            else:
                dentro.append(v)

        self.vehiculos = dentro

        if fuera:
            ids = {v.id for v in fuera}
            for carretera in self.carreteras:
                for carril in carretera.carriles:
                    carril.vehiculos = [v for v in carril.vehiculos if v.id not in ids]

    # -------------------------------------------------------------
    def obtener_metricas_por_via(self):
        resultados = {}

        for carretera in self.carreteras:
            direccion = carretera.direccion
            carriles = carretera.carriles

            cola_total = 0
            flujo_total = 0
            espera_total_vehiculos = 0.0
            vehiculos_parados_total = 0

            for carril in carriles:
                hist_cola = self.metricas.obtener_historial_cola(carretera, carril)
                cola_actual = hist_cola[-1] if hist_cola else 0
                cola_total += cola_actual

                cid = f"{carretera.direccion}_{carril.indice}"
                espera_promedio_carril = self.metricas.datos_carriles[cid]["espera_congelada"]
                parados_carril = self.metricas.datos_carriles[cid]["vehiculos_parados"]
                espera_total_vehiculos += espera_promedio_carril * parados_carril
                vehiculos_parados_total += parados_carril

                flujo = self.metricas.obtener_conteo_flujo(carretera, carril)
                flujo_total += flujo

            resultados[direccion] = {
                "cola": cola_total,
                "espera": espera_total_vehiculos / vehiculos_parados_total if vehiculos_parados_total > 0 else 0.0,
                "flujo": flujo_total
            }

        return resultados

    # -------------------------------------------------------------
    def paso(self, dt):

        if not self.en_ejecucion:
            return

        dt_real = dt
        dt_simulado = dt_real * config.VELOCIDAD_SIMULACION
        self.tiempo += dt_simulado
        self.controlador_semaforos.actualizar(dt_simulado)

        # ---------------------------------------------------------
        # GENERACIÓN DE VEHÍCULOS (veh/h → veh/s)
        # ---------------------------------------------------------
        for carretera in self.carreteras:
            d = carretera.direccion
            tasa = self.trafico_por_direccion[d] / 60.0

            self.acumulador_generacion[d] += tasa * dt_simulado

            while self.acumulador_generacion[d] >= 1.0:

                self.acumulador_generacion[d] = min(
                    self.acumulador_generacion[d], 3.0
                )

                if self._generar_vehiculo_en_carretera(carretera):
                    self.acumulador_generacion[d] -= 1.0
                else:
                    break

        # ---------------------------------------------------------
        # DINÁMICA + REGISTRO DE MÉTRICAS
        # ---------------------------------------------------------
        for carretera in self.carreteras:

            semaforo = self.semaforos[carretera.direccion]

            pos_cruce = carretera.pos_cruce / self.ESCALA
            pos_parada = pos_cruce - (70 / self.ESCALA) - self.DISTANCIA_FRENADO_CEBRA

            for carril in carretera.carriles:

                vehs = carril.vehiculos
                vehs.sort(key=lambda v: v.posicion)

                # Calcular aceleraciones
                for i, v in enumerate(vehs):

                    if v.velocidad <= config.VELOCIDAD_PARADA_UMBRAL and v.tiempo_parado < v.tiempo_reaccion:
                        v.aceleracion = 0.0
                        continue

                    if i == len(vehs) - 1:
                        veh_adelante = None
                        distancia = float("inf")
                    else:
                        va = vehs[i + 1]
                        distancia = max(va.posicion - v.posicion - va.largo, 0.1)
                        veh_adelante = va

                    d_cebra = pos_parada - v.posicion - v.largo

                    if (semaforo.estado in ["rojo", "amarillo"]) and 0 < d_cebra < distancia:
                        distancia = d_cebra
                        veh_adelante = self.obstaculo_fijo

                    v.aceleracion = self.idm.calcular_aceleracion(
                        v, veh_adelante, distancia
                    )

                # Actualizar vehículos
                for v in vehs:
                    pos_anterior = v.posicion

                    v.actualizar(dt_simulado)
                    self._evaluar_cambio_de_carril(v)

                    # Detector de flujo en la línea peatonal
                    pos_detector = pos_cruce - (config.DISTANCIA_DETECTOR_CEBRA_PX / self.ESCALA)

                    if not v.ha_cruzado_detector and pos_anterior < pos_detector <= v.posicion:
                        self.metricas.registrar_paso_detector(carretera, carril)
                        v.ha_cruzado_detector = True

                # -------------------------------------------------
                # REGISTRO DE MÉTRICAS POR CARRIL
                # -------------------------------------------------
                cola = sum(1 for v in vehs if v.velocidad < config.VELOCIDAD_COLA_UMBRAL)
                espera_total = sum(
                    v.tiempo_parado for v in vehs if v.velocidad < config.VELOCIDAD_COLA_UMBRAL
                )
                espera_promedio = espera_total / cola if cola > 0 else 0.0

                self.metricas.registrar_cola_y_espera(
                    carretera, carril, cola, espera_promedio
                )

        self._limpiar_vehiculos()

        # ---------------------------------------------------------
        # IMPRESIÓN DE MÉTRICAS POR VÍA
        # ---------------------------------------------------------
        metricas_via = self.obtener_metricas_por_via()

        for direccion, datos in metricas_via.items():
            print(
                f"[VÍA {direccion}] cola={datos['cola']} | "
                f"espera_prom={round(datos['espera'])}s | flujo={datos['flujo']}"
            )

