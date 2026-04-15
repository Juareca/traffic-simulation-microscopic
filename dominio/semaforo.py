class Semaforo:
    
    def __init__(self, posicion: float):
        self.posicion = posicion
    
        self.estado = "rojo"  # estado inicial
        