from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QGuiApplication

from presentacion.simulation_widget import SimulationWidget
from dominio.simulacion import Simulacion


class MainWindow(QMainWindow):
    def __init__(self, debug=False, seed=None):
        super().__init__()

        self.setWindowTitle("Simulador de Tráfico")

        # 📏 Obtener tamaño real de la pantalla
        screen_size = QGuiApplication.primaryScreen().size()

        ancho = screen_size.width()
        alto = screen_size.height()
        grosor = 70  # puedes ajustarlo luego

        # 🚗 Crear simulación con tamaño dinámico
        self.simulacion = Simulacion(ancho, alto, grosor, debug=debug, seed=seed)

        # 🎮 Widget principal
        self.widget = SimulationWidget(self.simulacion)
        self.setCentralWidget(self.widget)

        # 🖥️ Pantalla completa
        self.showMaximized()