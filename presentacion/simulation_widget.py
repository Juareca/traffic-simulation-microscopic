from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPainter, QPen, QBrush
from dominio.config import ESCALA
from presentacion.visual_settings import COLOR_BACKGROUND, COLOR_LIGHT_GREEN, COLOR_LIGHT_RED, COLOR_LIGHT_YELLOW, COLOR_LINES, COLOR_ROAD, COLOR_VEHICLE

class SimulationWidget(QWidget):
    def __init__(self, controlador):
        super().__init__()
        
        self.controlador = controlador
        self.simulacion = controlador.simulacion

        self.setFocusPolicy(Qt.StrongFocus)

        # Timer a 60 FPS (16.67ms por frame)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar)
        self.timer.start(16)

        # Colores
        self.color_fondo = COLOR_BACKGROUND
        self.color_carretera = COLOR_ROAD   
        self.color_vehiculo = COLOR_VEHICLE
        self.color_semaforo_verde = COLOR_LIGHT_GREEN
        self.color_semaforo_amarillo = COLOR_LIGHT_YELLOW
        self.color_semaforo_rojo = COLOR_LIGHT_RED
        self.color_linea = COLOR_LINES

        # Parámetros visuales
        self.ESCALA = ESCALA
        self.ANCHO_CARRIL = 20
        self.LARGO_VEHICULO = 20
        self.ALTO_VEHICULO = 10
        self.RADIO_SEMAFORO = 8
        
        # Pre-crear pinceles y plumas para evitar asignaciones en cada frame
        self.brush_fondo = QBrush(self.color_fondo)
        self.brush_carretera = QBrush(self.color_carretera)
        self.brush_vehiculo = QBrush(self.color_vehiculo)
        self.brush_linea = QBrush(self.color_linea)
        
        self.brush_semaforo_rojo = QBrush(self.color_semaforo_rojo)
        self.brush_semaforo_amarillo = QBrush(self.color_semaforo_amarillo)
        self.brush_semaforo_verde = QBrush(self.color_semaforo_verde)
        
        self.pen_carril = QPen(self.color_linea)
        self.pen_carril.setStyle(Qt.DashLine)
        self.pen_carril.setWidth(1)
        
        self.pen_cebra = QPen(self.color_linea)
        self.pen_cebra.setWidth(2)

        # Parámetros de animación
        self.frame_count = 0

    
    def iniciar(self):
        self.controlador.iniciar()

    def pausar(self):
        self.controlador.pausar()

    def reiniciar(self):
        self.controlador.reiniciar()

    def cambiar_velocidad(self, factor):
        self.controlador.cambiar_velocidad(factor)

    # ------------------------------------------------------------------
    # Actualización
    # ------------------------------------------------------------------
    def actualizar(self):
        self.controlador.paso(0.016) # Simular paso de 16ms (60 FPS)
        self.update()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            QApplication.quit()

    # ------------------------------------------------------------------
    # Helpers de dibujo
    # ------------------------------------------------------------------
    def _brush_semaforo(self, sem):
        """Retorna brush precreado según estado del semáforo."""
        if sem.estado == "rojo":
            return self.brush_semaforo_rojo
        if sem.estado == "amarillo":
            return self.brush_semaforo_amarillo
        return self.brush_semaforo_verde

    def _pos_semaforo(self, carretera, sem):
        centro_x = self.width() // 2
        centro_y = self.height() // 2

        # S-N → semáforo abajo del cruce (vehículos suben)
        if carretera.direccion == "S-N":
            x = centro_x + 10
            y = centro_y + 120

        # N-S → semáforo arriba del cruce (vehículos bajan)
        elif carretera.direccion == "N-S":
            x = centro_x + 10
            y = centro_y - 80

        # O-E → semáforo a la izquierda del cruce (vehículos van →)
        elif carretera.direccion == "O-E":
            x = centro_x - 120
            y = centro_y + 10

        # E-O <- semáforo a la derecha del cruce (vehículos van ←)
        else:  # "E-O"
            x = centro_x + 120
            y = centro_y + 10

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
        """Dibuja las líneas de parada (cebra) de forma optimizada."""
        grosor_linea = 4
        offset = 70  # distancia desde el centro
        ancho_carretera = 120  # ajusta a gusto

        centro_x = self.width() // 2
        centro_y = self.height() // 2
        
        painter.setBrush(self.brush_linea)

        # Dibujar 4 rectángulos (cebra en 4 direcciones)
        rects = [
            # Vertical superior
            (int(centro_x + 8 - ancho_carretera // 2), int(centro_y - offset + 20), int(ancho_carretera), grosor_linea),
            # Vertical inferior
            (int(centro_x + 8 - ancho_carretera // 2), int(centro_y + offset + 20), int(ancho_carretera), grosor_linea),
            # Horizontal izquierda
            (int(centro_x - offset + 8), int(centro_y - ancho_carretera // 2 + 20), grosor_linea, int(ancho_carretera)),
            # Horizontal derecha
            (int(centro_x + offset + 8), int(centro_y - ancho_carretera // 2 + 20), grosor_linea, int(ancho_carretera)),
        ]
        
        for x, y, w, h in rects:
            painter.drawRect(x, y, w, h)

    def _dibujar_lineas_carril(self, painter, carretera):
        painter.setPen(self.pen_carril)

        num = len(carretera.carriles)

        # No dibujar líneas si solo hay 1 carril
        if num <= 1:
            return

        # Distancia entre líneas
        if carretera.direccion in ("O-E", "E-O"):
            # Carretera horizontal
            alto = carretera.alto
            for i in range(1, num):
                y = carretera.y + (i * alto / num)
                painter.drawLine(
                    int(carretera.x),
                    int(y),
                    int(carretera.x + carretera.ancho),
                    int(y)
                )
        else:
            # Carretera vertical
            ancho = carretera.ancho
            for i in range(1, num):
                x = carretera.x + (i * ancho / num)
                painter.drawLine(
                    int(x),
                    int(carretera.y),
                    int(x),
                    int(carretera.y + carretera.alto)
                )


    # ------------------------------------------------------------------
    # Dibujo principal
    # ------------------------------------------------------------------
    def paintEvent(self, event):
        painter = QPainter(self)
        
        # 🚀 OPTIMIZACIÓN 1: Activar anti-aliasing y suavizado
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        # Fondo
        painter.fillRect(self.rect(), self.brush_fondo)

        # Carreteras + líneas de carril
        painter.setBrush(self.brush_carretera)
        painter.setPen(Qt.NoPen)  # Sin borde para mejor rendimiento
        for carretera in self.simulacion.carreteras:
            painter.drawRect(
                int(carretera.x),
                int(carretera.y),
                int(carretera.ancho),
                int(carretera.alto)
            )
        
        # Líneas de carril
        painter.setPen(self.pen_carril)
        for carretera in self.simulacion.carreteras:
            self._dibujar_lineas_carril(painter, carretera)
            
        # Cebra
        painter.setPen(self.pen_cebra)
        self._dibujar_cebra(painter)

        # Semáforos (4)
        painter.setPen(Qt.NoPen)
        for carretera in self.simulacion.carreteras:
            sem = self.simulacion.semaforos[carretera.direccion]
            painter.setBrush(self._brush_semaforo(sem))
            x, y = self._pos_semaforo(carretera, sem)
            painter.drawEllipse(
                x - self.RADIO_SEMAFORO,
                y - self.RADIO_SEMAFORO,
                self.RADIO_SEMAFORO * 2,
                self.RADIO_SEMAFORO * 2
            )

        # Vehículos
        painter.setBrush(self.brush_vehiculo)
        painter.setPen(Qt.NoPen)
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

                    painter.drawRect(
                        x - w // 2,
                        y - h // 2,
                        w,
                        h
                    )
        
        painter.end()

