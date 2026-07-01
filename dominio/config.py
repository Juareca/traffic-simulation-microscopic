# ==================================================================================
# 📏 ESCALA Y CONVERSIÓN
# ==================================================================================
ESCALA = 5  # pixeles por metro


# ==================================================================================
# 🚗 PARÁMETROS VEHICULARES — VELOCIDAD Y DIMENSIONES
# ==================================================================================
# Velocidad mínima y máxima permitida (km/h)
VELOCIDAD_MIN_KMH = 20   
VELOCIDAD_MAX_KMH = 30  

# Conversión a m/s
KMH_A_MS = 1000 / 3600

V0_MIN = VELOCIDAD_MIN_KMH * KMH_A_MS
V0_MAX = VELOCIDAD_MAX_KMH * KMH_A_MS

# Dimensiones físicas del vehículo
LARGO_VEHICULO = 4.5  # metros


# ==================================================================================
# 🚗 PARÁMETROS INDIVIDUALES DEL MODELO IDM (Variabilidad del conductor)
# ==================================================================================
# Tiempo de reacción (T)
T_MIN = 1.2
T_MAX = 2.0
T_SPAWN_MIN = 1.2
T_SPAWN_MAX = 1.8

# Aceleración máxima (a_max)
A_MAX_MIN = 0.5
A_MAX_MAX = 1.2
A_MAX_SPAWN_MIN = 0.8
A_MAX_SPAWN_MAX = 1.5

# Desaceleración máxima (b)
B_MIN = 2.0
B_MAX = 3.5

# Tiempo de reacción humano (para comportamiento de parada)
TIEMPO_REACCION_MIN = 0.8
TIEMPO_REACCION_MAX = 1.5


# ==================================================================================
# 🚦 PARÁMETROS IDM — VALORES BASE (fallback)
# ==================================================================================
IDM_V0 = 6.0      # velocidad deseada (m/s)
IDM_T = 1.5       # tiempo de reacción (s)
IDM_A_MAX = 2.0   # aceleración máxima (m/s²)
IDM_B = 5.0       # desaceleración máxima (m/s²)
IDM_S0 = 4.0      # distancia mínima segura (m)
IDM_DELTA = 4     # exponente de aceleración


# ==================================================================================
# 🚦 SEMÁFOROS — INTERSECCIÓN REAL
# ==================================================================================
# Tiempos de fases (segundos)
NORTE_SUR_TIEMPO_VERDE = 28
SUR_NORTE_TIEMPO_VERDE = 33
ESTE_OESTE_TIEMPO_VERDE = 30
OESTE_ESTE_TIEMPO_VERDE = 36

SEMAFORO_TIEMPO_AMARILLO = 3  # segundos

# Posición del semáforo respecto al origen de la carretera (m)
SEMAFORO_POSICION = 40

# Orden de fases
FASES_SEMAFORO = ["N-S", "S-N", "E-O", "O-E"]


# ==================================================================================
# 🚗 GENERACIÓN DE VEHÍCULOS
# ==================================================================================
# Tasa de tráfico por dirección (veh/min)
TRAFICO_NORTE_SUR = 35.71
TRAFICO_SUR_NORTE = 34.54
TRAFICO_ESTE_OESTE = 18.56
TRAFICO_OESTE_ESTE = 22.67

# Velocidad mínima permitida (m/s)
VELOCIDAD_MINIMA = 2.0

# Tiempo de separación en spawn (s)
T_SPAWN = 1.5

# Limpieza de vehículos fuera de pantalla (px)
MARGEN_LIMPIEZA_VEHICULOS = 50

# Distancia desde el cruce hasta la cebra/detector (px)
DISTANCIA_DETECTOR_CEBRA_PX = 70


# ==================================================================================
# 🛣️ CARRETERA Y GEOMETRÍA
# ==================================================================================
# Número de carriles por carretera
CARRILES_POR_CARRETERA = 2

# Distancia adicional de frenado ante cebra (m)
DISTANCIA_FRENADO_CEBRA = 3.0

# grosor de la carretera en píxeles 
GROSOR_CARRETERA = 65 


# ==================================================================================
# 🎮 SIMULACIÓN GENERAL
# ==================================================================================
# Velocidad de simulación (1.0 = tiempo real)
VELOCIDAD_SIMULACION = 1.0

# Umbral para considerar vehículo "parado" (m/s)
VELOCIDAD_PARADA_UMBRAL = 0.1

# Umbral para detectar vehículos en "cola" (m/s)
VELOCIDAD_COLA_UMBRAL = 0.5
