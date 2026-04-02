from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPainter, QColor


class SimulationWidget(QWidget):
    def __init__(self, simulacion):
        super().__init__()
        self.simulacion = simulacion

        # 🚀 OPTIMIZACIÓN: Aumentar FPS de 10 a 60 (16ms vs 100ms)
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar)
        self.timer.start(16)  # 16ms ≈ 60 FPS (fluido)
        
        # 🎨 Caché de colores para evitar crear objetos repetidamente
        self.color_fondo = QColor("white")
        self.color_carretera = QColor("gray")
        self.color_semaforo_verde = QColor("green")
        self.color_semaforo_rojo = QColor("red")
        self.color_semaforo_amarillo = QColor("yellow")
        self.color_vehiculo = QColor("blue")
        
        # Constantes de escala y dibujado
        self.ESCALA = 10
        self.ANCHO_CARRETERA = 50
        self.ALTURA_VEHICULO = 20
        self.LARGO_VEHICULO = 20
        self.Y_CARRETERA = 100
        self.Y_VEHICULO_OFFSET = 10
        self.RADIO_SEMAFORO = 15

    def actualizar(self):
        # 🧠 OPTIMIZACIÓN: Usar dt variable para sincronizar con el timer
        # 16ms = 0.016 segundos
        self.simulacion.paso(0.016)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        # fondo
        painter.fillRect(self.rect(), self.color_fondo)

        # dibujar carretera
        painter.setBrush(self.color_carretera)
        painter.drawRect(0, self.Y_CARRETERA, self.width(), self.ANCHO_CARRETERA)

        # dibujar semáforo - OPTIMIZADO: caché de colores
        semaforo = self.simulacion.semaforo
        if semaforo.estado == "rojo":
            color = self.color_semaforo_rojo
        elif semaforo.estado == "amarillo":
            color = self.color_semaforo_amarillo
        else:
            color = self.color_semaforo_verde

        painter.setBrush(color)
        x_semaforo = int(semaforo.posicion * self.ESCALA)
        painter.drawEllipse(x_semaforo - self.RADIO_SEMAFORO, 
                          self.Y_CARRETERA - 50, 
                          self.RADIO_SEMAFORO * 2, 
                          self.RADIO_SEMAFORO * 2)

        # dibujar vehículos - OPTIMIZADO: reutilizar color
        painter.setBrush(self.color_vehiculo)
        for v in self.simulacion.vehiculos:
            x = int(v.posicion * self.ESCALA)
            painter.drawRect(x, self.Y_CARRETERA + self.Y_VEHICULO_OFFSET, 
                           self.LARGO_VEHICULO, self.ALTURA_VEHICULO)