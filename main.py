"""Punto de entrada de TrafficSimulator 2.0.

Ejecuta la simulación microscópica de tráfico con interfaz gráfica.
Permite configuración de:
    - Reproducibilidad mediante semilla aleatoria
    - Parámetros globales (velocidad deseada, etc.)

Uso:
    python main.py              # Simulación normal (defaults)
    
Para reproducibilidad:
    random.seed(42)             # Descomenta en main()
    
Para cambiar velocidad deseada:
    Vehiculo.v0 = 10           # Descomenta en main()
"""

import sys
import random
from PySide6.QtWidgets import QApplication
from dominio.vehiculo import Vehiculo
from dominio.simulacion import Simulacion
from presentacion.main_window import MainWindow


def main():
    """Inicializa y ejecuta la simulación.
    
    Parámetros configurables ANTES de crear Simulacion:
        - Semilla: random.seed(42)
        - Velocidad deseada: Vehiculo.v0 = 10
        - Debug: Simulacion(debug=True)
    
    Ejemplos:
        # Reproducible con v0=5:
        random.seed(42)
        sim = Simulacion(debug=False, seed=42)
        
        # Autopista con v0=15:
        Vehiculo.v0 = 15
        sim = Simulacion(debug=False)
        
        # Debug detallado:
        sim = Simulacion(debug=True, seed=42)
    """
    # ========== CONFIGURACIÓN DE REPRODUCIBILIDAD ==========
    # Para obtener resultados reproducibles, descomenta la siguiente línea:
    # random.seed(42)
    
    # ========== CONFIGURACIÓN DE PARÁMETROS GLOBALES ==========
    # Para cambiar la velocidad deseada (v0) para TODOS los vehículos:
    # Vehiculo.v0 = 15  # Autopista rápida (por defecto es 5 m/s)
    
    # Ejemplos:
    # Vehiculo.v0 = 5    # Tráfico urbano lento
    # Vehiculo.v0 = 10   # Tráfico normal
    # Vehiculo.v0 = 15   # Autopista rápida
    # Vehiculo.v0 = 20   # Autopista muy rápida
    
    app = QApplication(sys.argv)

    # ========== CREAR SIMULACIÓN ==========
    # Parámetros configurables:
    # - debug=False: Solo métricas resumidas (recomendado para presentación)
    # - debug=True: Información detallada de cada vehículo (útil para debugging)
    # - seed=None: Resultados aleatorios cada ejecución
    # - seed=42: Resultados reproducibles (cambiar número según necesites)
    
    sim = Simulacion(debug=True, seed=None)
    
    window = MainWindow(sim)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()