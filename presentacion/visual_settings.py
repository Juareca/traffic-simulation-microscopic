"""
⚙️ CONFIGURACIÓN VISUAL AVANZADA
================================
Parámetros para ajustar la fluidez y rendimiento visual de la simulación.
"""

# ============================================================================
# 🎨 RENDERIZADO
# ============================================================================
# Activar anti-aliasing (suaviza bordes, usa más CPU pero se ve mejor)
ANTIALIASING_ENABLED = True

# Activar suavizado de texturas (mejor para escalado)
SMOOTH_PIXMAP_TRANSFORM = True

# ============================================================================
# 🎯 RENDIMIENTO
# ============================================================================
# Período del timer en milisegundos (16 = 60 FPS, 33 = 30 FPS)
# Reducir para mayor suavidad (más CPU), aumentar para menos uso
TIMER_INTERVAL_MS = 16

# Cantidad de vehículos antes de activar "modo económico" de renderizado
VEHICLE_COUNT_THRESHOLD = 500

# Si está activado, renderiza solo los vehículos visibles (fuera de pantalla se saltan)
CULL_OFFSCREEN_VEHICLES = True

# ============================================================================
# 🎥 VISUAL
# ============================================================================
# Tamaño del vehículo (píxeles)
VEHICLE_WIDTH = 20
VEHICLE_HEIGHT = 10

# Radio del semáforo (píxeles)
TRAFFIC_LIGHT_RADIUS = 8

# Grosor de las líneas de carril (píxeles)
LANE_LINE_WIDTH = 1

# Grosor de la cebra (píxeles)
ZEBRA_LINE_WIDTH = 2

# ============================================================================
# 🚦 COLORES
# ============================================================================
COLOR_BACKGROUND = "black"
COLOR_ROAD = "gray"
COLOR_VEHICLE = "white"
COLOR_LIGHT_RED = "red"
COLOR_LIGHT_YELLOW = "yellow"
COLOR_LIGHT_GREEN = "green"
COLOR_LINES = "white"  

# ============================================================================
# ⚡ TIPS DE OPTIMIZACIÓN
# ============================================================================
"""
1. REDUCIR COMPLEJIDAD VISUAL:
   - Disminuir VEHICLE_WIDTH/HEIGHT si hay muchos vehículos
   - Activar CULL_OFFSCREEN_VEHICLES para evitar dibujar fuera de pantalla

2. MEJORAR FLUIDEZ:
   - Aumentar TIMER_INTERVAL_MS para reducir carga de CPU
   - Reducir la tasa de tráfico en config.py (TRAFICO_TASA_POR_DIRECCION)

3. MEJOR CALIDAD VISUAL:
   - ANTIALIASING_ENABLED = True (costo: ~5-10% de CPU)
   - SMOOTH_PIXMAP_TRANSFORM = True (para escalados)

4. PROFILING:
   - Usar: python -m cProfile -s cumtime main.py
   - Esto mostrará qué métodos usan más CPU

5. VSYNC (para evitar tearing):
   - En main_window.py, usar QSurfaceFormat para forzar vsync
"""
