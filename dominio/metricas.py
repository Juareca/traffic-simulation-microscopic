class Metricas:

    def __init__(self, carreteras):
        self.datos_carriles = {}

        for carretera in carreteras:
            for carril in carretera.carriles:
                cid = self._id_carril(carretera, carril)
                self.datos_carriles[cid] = {
                    "hist_cola": [],
                    "hist_espera": [],
                    "conteo_detector": 0,
                    # valor promedio de espera por carril en el instante actual
                    "espera_congelada": 0.0,
                    "vehiculos_parados": 0,
                }

    def _id_carril(self, carretera, carril):
        return f"{carretera.direccion}_{carril.indice}"

    def registrar_cola_y_espera(self, carretera, carril, cola, tiempo_espera):
        cid = self._id_carril(carretera, carril)
        datos = self.datos_carriles[cid]

        # Si hay cola, guardamos el promedio de espera del carril.
        # Si no hay cola, se restablece a cero para evitar valores antiguos.
        if cola > 0:
            datos["espera_congelada"] = tiempo_espera
        else:
            datos["espera_congelada"] = 0.0

        datos["vehiculos_parados"] = cola

        datos["hist_cola"].append(cola)
        datos["hist_espera"].append(datos["espera_congelada"])

    def registrar_paso_detector(self, carretera, carril):
        cid = self._id_carril(carretera, carril)
        self.datos_carriles[cid]["conteo_detector"] += 1

    def obtener_historial_cola(self, carretera, carril):
        cid = self._id_carril(carretera, carril)
        return self.datos_carriles[cid]["hist_cola"]

    def obtener_historial_espera(self, carretera, carril):
        cid = self._id_carril(carretera, carril)
        return self.datos_carriles[cid]["hist_espera"]

    def obtener_conteo_flujo(self, carretera, carril):
        cid = self._id_carril(carretera, carril)
        return self.datos_carriles[cid]["conteo_detector"]
