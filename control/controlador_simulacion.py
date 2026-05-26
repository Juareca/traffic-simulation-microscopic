from dominio.simulacion import Simulacion


class ControladorSimulacion:
    """Capa de Control: orquesta la aplicación y medía entre GUI y dominio."""

    def __init__(self, ancho, alto, grosor, debug=False, seed=None):
        self.simulacion = Simulacion(ancho, alto, grosor, debug=debug, seed=seed)

    # -----------------------------
    # Control del ciclo de simulación
    # -----------------------------
    def iniciar(self):
        self.simulacion.iniciar()

    def pausar(self):
        self.simulacion.pausar()

    def reiniciar(self):
        self.simulacion.reiniciar()

    def paso(self, dt):
        """Coordina un paso de simulación sin implementar la lógica de tráfico."""
        self.simulacion.paso(dt)

    # -----------------------------
    # Gestión de parámetros
    # -----------------------------
    def cambiar_velocidad(self, factor):
        self.simulacion.cambiar_velocidad(factor)

    # -----------------------------
    # Métricas
    # -----------------------------
    def obtener_metricas_por_via(self):
        return self.simulacion.obtener_metricas_por_via()

