from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPainter, QColor


class SimulationWidget(QWidget):
    def __init__(self, simulacion):
        super().__init__()
        self.simulacion = simulacion

        # Timer a 60 FPS
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar)
        self.timer.start(16)

        # Colores
        self.color_fondo = QColor("white")
        self.color_carretera = QColor("gray")
        self.color_vehiculo = QColor("blue")
        self.color_semaforo_verde = QColor("green")
        self.color_semaforo_amarillo = QColor("yellow")
        self.color_semaforo_rojo = QColor("red")
        self.color_linea = QColor(255, 255, 255)

        # Parámetros visuales
        self.ESCALA = 5.0
        self.ANCHO_CARRIL = 20
        self.LARGO_VEHICULO = 20
        self.ALTO_VEHICULO = 10
        self.RADIO_SEMAFORO = 8

    # ------------------------------------------------------------------
    # Actualización
    # ------------------------------------------------------------------
    def actualizar(self):
        self.simulacion.paso(0.016)
        self.update()

    # ------------------------------------------------------------------
    # Helpers de dibujo
    # ------------------------------------------------------------------
    def _color_semaforo(self, sem):
        if sem.estado == "rojo":
            return self.color_semaforo_rojo
        if sem.estado == "amarillo":
            return self.color_semaforo_amarillo
        return self.color_semaforo_verde

    def _pos_semaforo(self, carretera, sem):
        centro_x = self.width() // 2
        centro_y = self.height() // 2

        # S-N → semáforo abajo del cruce (vehículos suben)
        if carretera.direccion == "S-N":
            x = centro_x
            y = centro_y + 160

        # N-S → semáforo arriba del cruce (vehículos bajan)
        elif carretera.direccion == "N-S":
            x = centro_x
            y = centro_y - 120

        # O-E → semáforo a la derecha del cruce (vehículos van →)
        elif carretera.direccion == "O-E":
            x = centro_x - 120
            y = centro_y + 35

        # E-O → semáforo a la izquierda del cruce (vehículos van ←)
        else:  # "E-O"
            x = centro_x + 120
            y = centro_y + 35

        return int(x), int(y)

    def _pos_vehiculo(self, carretera, carril, veh):
        pos = veh.posicion * self.ESCALA
        num = len(carretera.carriles)

        # HORIZONTALES (O-E, E-O)
        if carretera.direccion in ("O-E", "E-O"):
            # centro del carril usando el ALTO real de la carretera
            lane_center_y = carretera.y + ( (carril.indice + 0.5) * (carretera.alto / num) )

            if carretera.direccion == "O-E":
                x = carretera.x + pos
            else:
                x = carretera.x + carretera.ancho - pos

            y = lane_center_y

        # VERTICALES (N-S, S-N)
        else:
            # centro del carril usando el ANCHO real de la carretera
            lane_center_x = carretera.x + ( (carril.indice + 0.5) * (carretera.ancho / num) )

            if carretera.direccion == "S-N":
                y = carretera.y + carretera.alto - pos
            else:
                y = carretera.y + pos

            x = lane_center_x

        return int(x), int(y)

    def _dibujar_cebra(self, painter):
        painter.setBrush(self.color_linea)
        painter.setPen(self.color_linea)

        grosor_linea = 4
        offset = 70  # distancia desde el centro
        ancho_carretera = 120  # ajusta a gusto

        centro_x = self.width() // 2
        centro_y = self.height() // 2

        # Vertical superior
        painter.drawRect(
            int(centro_x - ancho_carretera // 2),
            int(centro_y - offset) + 30,
            int(ancho_carretera),
            grosor_linea
        )

        # Vertical inferior
        painter.drawRect(
            int(centro_x - ancho_carretera // 2),
            int(centro_y + offset) + 36,
            int(ancho_carretera),
            grosor_linea
        )

        # Horizontal izquierda
        painter.drawRect(
            int(centro_x - offset) - 5,
            int(centro_y - ancho_carretera // 2) + 33,
            grosor_linea,
            int(ancho_carretera)
        )

        # Horizontal derecha
        painter.drawRect(
            int(centro_x + offset) + 5,
            int(centro_y - ancho_carretera // 2) + 33,
            grosor_linea,
            int(ancho_carretera)
        )

    def _dibujar_lineas_carril(self, painter, carretera):
        painter.setPen(self.color_linea)
        painter.setPen(Qt.DashLine)

        if carretera.direccion in ("O-E", "E-O"):
            y = carretera.y + carretera.alto / 2
            painter.drawLine(
                int(carretera.x),
                int(y),
                int(carretera.x + carretera.ancho),
                int(y)
            )
        else:
            x = carretera.x + carretera.ancho / 2
            painter.drawLine(
                int(x),
                int(carretera.y),
                int(x),
                int(carretera.y + carretera.alto)
            )

        painter.setPen(Qt.SolidLine)

    # ------------------------------------------------------------------
    # Dibujo principal
    # ------------------------------------------------------------------
    def paintEvent(self, event):
        painter = QPainter(self)

        # Fondo
        painter.fillRect(self.rect(), self.color_fondo)

        # Carreteras + líneas de carril
        painter.setBrush(self.color_carretera)
        for carretera in self.simulacion.carreteras:
            painter.drawRect(
                int(carretera.x),
                int(carretera.y),
                int(carretera.ancho),
                int(carretera.alto)
            )
            
            self._dibujar_lineas_carril(painter, carretera)
        # Cebra
        self._dibujar_cebra(painter)

        # Semáforos (4)
        for carretera in self.simulacion.carreteras:
            sem = self.simulacion.semaforos[carretera.direccion]
            painter.setBrush(self._color_semaforo(sem))
            x, y = self._pos_semaforo(carretera, sem)
            painter.drawEllipse(
                x - self.RADIO_SEMAFORO,
                y - self.RADIO_SEMAFORO,
                self.RADIO_SEMAFORO * 2,
                self.RADIO_SEMAFORO * 2
            )

        # Vehículos
        for carretera in self.simulacion.carreteras:
            for carril in carretera.carriles:
                for v in carril.vehiculos:
                    x, y = self._pos_vehiculo(carretera, carril, v)

                    # Forma según dirección
                    if carretera.direccion in ("O-E", "E-O"):
                        w = self.LARGO_VEHICULO
                        h = self.ALTO_VEHICULO
                    else:  # S-N, N-S
                        w = self.ALTO_VEHICULO
                        h = self.LARGO_VEHICULO

                    painter.setBrush(self.color_vehiculo)
                    painter.drawRect(
                        x - w // 2,
                        y - h // 2,
                        w,
                        h
                    )

