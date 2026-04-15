from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QGuiApplication

from presentacion.simulation_widget import SimulationWidget
from control.simulacion import Simulacion

print(">>> Simulacion importada desde:", Simulacion.__module__)
print(">>> Archivo real:", Simulacion.__dict__.get('__file__'))
print(">>> Métodos disponibles:", [m for m in dir(Simulacion) if not m.startswith('_')])


class MainWindow(QMainWindow):
    def __init__(self, debug=False, seed=None):
        super().__init__()

        self.setWindowTitle("Simulador de Tráfico")

        # 📏 Obtener tamaño real de la pantalla
        screen_size = QGuiApplication.primaryScreen().size()

        ancho = screen_size.width()
        alto = screen_size.height()
        grosor = 70  # grosor de carretera (ajústalo si quieres)

        # 🚗 Crear simulación con tamaño dinámico
        # Aquí creamos la instancia REAL de Simulacion
        simulacion = Simulacion(ancho, alto, grosor, debug=debug, seed=seed)

        # 🎮 Crear widget de simulación pasándole la instancia
        self.widget = SimulationWidget(simulacion)
        self.setCentralWidget(self.widget)

        # 🖥️ Pantalla completa
        self.showFullScreen()
