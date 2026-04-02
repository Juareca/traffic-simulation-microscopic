from PySide6.QtWidgets import QMainWindow
from presentacion.simulation_widget import SimulationWidget


class MainWindow(QMainWindow):
    def __init__(self, simulacion):
        super().__init__()

        self.setWindowTitle("Simulador de Tráfico")
        self.setGeometry(100, 100, 800, 300)

        self.widget = SimulationWidget(simulacion)
        self.setCentralWidget(self.widget)