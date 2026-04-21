class ControladorSemaforos:
    """
    Controlador de fases semafóricas.
    Capa CONTROL: coordina semáforos del dominio.
    """

    def __init__(self, semaforos, tiempos):

        self.semaforos = semaforos
        self.tiempos = tiempos

        self.fases = ["N-S", "S-N", "E-O", "O-E"]
        self.fase_actual = 0
        self.tiempo_fase = 0.0

    def actualizar(self, dt):
        fase = self.fases[self.fase_actual]
        t_verde = self.tiempos[fase]["verde"]
        t_amarillo = self.tiempos[fase]["amarillo"]
        t_total = t_verde + t_amarillo

        self.tiempo_fase += dt

        # Estado del semáforo activo
        if self.tiempo_fase < t_verde:
            estado = "verde"
        elif self.tiempo_fase < t_total:
            estado = "amarillo"
        else:
            estado = "rojo"

        # Aplicar estado al semáforo activo
        for key, sem in self.semaforos.items():
            if key == fase:
                sem.estado = estado
            else:
                sem.estado = "rojo"

        # Cambio de fase
        if self.tiempo_fase >= t_total:
            self.fase_actual = (self.fase_actual + 1) % len(self.fases)
            self.tiempo_fase = 0.0
