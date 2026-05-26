from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PySide6.QtGui import QGuiApplication, QSurfaceFormat, QIcon
from PySide6.QtCore import Qt

from presentacion.simulation_widget import SimulationWidget
from dominio.config import GROSOR_CARRETERA
from control.controlador_simulacion import ControladorSimulacion

class MainWindow(QMainWindow):
    def __init__(self, debug=False, seed=None):
        super().__init__()

        self.setWindowTitle("Simulador de Tráfico")

        # ================================
        # ⚙️ CONFIGURACIÓN GRÁFICA
        # ================================
        fmt = QSurfaceFormat()
        fmt.setSwapInterval(1)
        fmt.setVersion(3, 3)
        fmt.setProfile(QSurfaceFormat.CoreProfile)
        QSurfaceFormat.setDefaultFormat(fmt)

        # Tamaño de la ventana y parámetros de carretera
        screen_size = QGuiApplication.primaryScreen().size()
        ancho = screen_size.width()
        alto = screen_size.height()
        grosor = GROSOR_CARRETERA

        # Crear controlador de simulación
        self.controlador = ControladorSimulacion(ancho, alto, grosor, debug=debug, seed=seed)

        # Crear widget de simulación usando el controlador
        self.widget = SimulationWidget(self.controlador)

        # ================================
        # 🖥️ LAYOUT PRINCIPAL (solo simulación)
        # ================================
        layout_principal = QVBoxLayout()
        layout_principal.addWidget(self.widget)

        contenedor = QWidget()
        contenedor.setLayout(layout_principal)
        self.setCentralWidget(contenedor)

        # Pantalla completa
        self.showFullScreen()

        # ================================
        # 🧭 MENÚ SUPERIOR (MENUBAR)
        # ================================
        menu = self.menuBar()
        menu_archivo = menu.addMenu("Archivo")
        menu_simulacion = menu.addMenu("Simulación")
        menu_trafico = menu.addMenu("Tráfico")
        menu_semaforos = menu.addMenu("Semáforos")
        menu_vista = menu.addMenu("Vista")
        menu_ayuda = menu.addMenu("Ayuda")

        # Acciones principales
        accion_iniciar = menu_simulacion.addAction("Iniciar")
        accion_iniciar.setIcon(QIcon("icons/play.png"))

        accion_pausar = menu_simulacion.addAction("Pausar")
        accion_pausar.setIcon(QIcon("icons/pause.png"))

        accion_reiniciar = menu_simulacion.addAction("Reiniciar")
        accion_reiniciar.setIcon(QIcon("icons/restart.png"))

        # ================================
        # 📌 SUBMENÚ VELOCIDAD
        # ================================
        menu_velocidad = menu_simulacion.addMenu("Velocidad")
        menu_velocidad.setIcon(QIcon("icons/speed.png"))

        accion_05 = menu_velocidad.addAction("0.5x")
        accion_1 = menu_velocidad.addAction("1x")
        accion_2 = menu_velocidad.addAction("2x")
        accion_4 = menu_velocidad.addAction("4x")

        # ================================
        # 🔗 CONEXIONES DEL MENÚ
        # ================================
        accion_iniciar.triggered.connect(self.controlador.iniciar)
        accion_pausar.triggered.connect(self.controlador.pausar)
        accion_reiniciar.triggered.connect(self.controlador.reiniciar)

        accion_05.triggered.connect(lambda: self.cambiar_velocidad(0.5))
        accion_1.triggered.connect(lambda: self.cambiar_velocidad(1.0))
        accion_2.triggered.connect(lambda: self.cambiar_velocidad(2.0))
        accion_4.triggered.connect(lambda: self.cambiar_velocidad(4.0))

        # ================================
        # 🎨 ESTILO DEL MENÚ
        # ================================
        self.setStyleSheet("""
            QMainWindow {
                background-color: black;
            }
            QMenuBar {
                background-color: #2c2c2c;
                color: white;
                font-size: 12px;
                padding: 0px;
            }
            QMenuBar::item:selected {
                background-color: #444444;
            }
            QMenu {
                background-color: #2c2c2c;
                color: white;
            }
            QMenu::item:selected {
                background-color: #555555;
            }
        """)

    # ================================
    # 🔥 MÉTODO REAL DE CAMBIO DE VELOCIDAD
    # ================================
    def cambiar_velocidad(self, factor):
        self.controlador.cambiar_velocidad(factor)
        print(f"[INFO] Velocidad cambiada a x{factor}")
