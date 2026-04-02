# 📘 GUÍA RÁPIDA: Parámetros del Modelo en TrafficSimulator 2.0

## Estructura de Parámetros

```
TrafficSimulator 2.0
│
├── Vehiculo (dominio/vehiculo.py)
│   └── v0 = 4  [ATRIBUTO DE CLASE]
│       ↓ (usado por)
│
├── IDM (dominio/idm.py)
│   ├── self.v0 = Vehiculo.v0    [← tomado de Vehiculo]
│   ├── self.T = 1.5
│   ├── self.a_max = 2
│   ├── self.b = 3
│   ├── self.s0 = 2
│   └── self.delta = 4
│
├── Semaforo (dominio/semaforo.py)
│   ├── tiempo_verde = 12
│   ├── tiempo_amarillo = 2
│   └── tiempo_rojo = 12
│
└── main.py
    └── Punto donde cambiar parámetros GLOBALES
```

---

## 🎯 Cómo Cambiar Parámetros

### 1. **Velocidad Deseada (v0) - GLOBAL**

**Ubicación**: Clase `Vehiculo`, atributo de clase

**Valor por defecto**: 4 m/s

**Cómo cambiar**:

```python
# En main.py, ANTES de crear Simulacion():
from dominio.vehiculo import Vehiculo

Vehiculo.v0 = 10  # Nuevo valor global
sim = Simulacion(debug=False)
```

**Efecto**: Todos los vehículos usarán v0=10 en su cálculo de aceleración IDM

**Casos de uso**:

- Vehiculo.v0 = 4 → Tráfico urbano lento
- Vehiculo.v0 = 10 → Tráfico normal
- Vehiculo.v0 = 15 → Autopista rápida
- Vehiculo.v0 = 20 → Autopista muy rápida

---

### 2. **Parámetros del IDM**

**Ubicación**: Clase `IDM`, método `__init__`

**Parámetros actuales**:

| Parámetro         | Símbolo | Valor | Rango Típico | Nota                        |
| ----------------- | ------- | ----- | ------------ | --------------------------- |
| Velocidad deseada | v₀      | 4     | 4-20         | **TOMADO DE Vehiculo.v0** ✓ |
| Tiempo reacción   | T       | 1.5   | 0.5-2.0      | Hardcodeado en IDM          |
| Aceleración máx   | a_max   | 2     | 1-3          | Hardcodeado en IDM          |
| Desaceleración    | b       | 3     | 1-5          | Hardcodeado en IDM          |
| Distancia mínima  | s₀      | 2     | 1-3          | Hardcodeado en IDM          |
| Exponente         | δ       | 4     | 4-6          | Hardcodeado en IDM          |

**Cómo cambiar otros parámetros IDM** (si lo necesitas):

Edita directamente en `dominio/idm.py`, línea ~50:

```python
def __init__(self):
    self.v0 = Vehiculo.v0    # Dinámico (vinculado a Vehiculo)
    self.T = 2.0             # ← Cambiar aquí si necesitas
    self.a_max = 3           # ← Cambiar aquí si necesitas
    self.b = 4               # ← Cambiar aquí si necesitas
    ...
```

---

### 3. **Parámetros del Semáforo**

**Ubicación**: Clase `Semaforo`, método `__init__`

**Valores actuales**:

```python
self.semaforo = Semaforo(40, 12, 2, 12)
# argumentos:     (posición, verde, amarillo, rojo)
```

**Cómo cambiar** (en `dominio/simulacion.py`, línea ~87):

```python
# Cambiar ciclo del semáforo:
# Semaforo(posicion, tiempo_verde, tiempo_amarillo, tiempo_rojo)

# Actual:
self.semaforo = Semaforo(40, 12, 2, 12)  # 26s de ciclo total

# Semáforo más rápido:
self.semaforo = Semaforo(40, 8, 2, 8)    # 18s de ciclo total

# Semáforo más lento:
self.semaforo = Semaforo(40, 20, 3, 20)  # 43s de ciclo total

# Cambiar posición:
self.semaforo = Semaforo(50, 12, 2, 12)  # Más lejos (en lugar de 40m)
```

---

## 📋 Combinaciones Recomendadas para Experimentos

### Experimento 1: Tráfico Urbano (Congestionado)

```python
# main.py
Vehiculo.v0 = 5    # Velocidad lenta
sim = Simulacion(debug=False, seed=42)
# Resultado esperado: Mucha congestión
```

### Experimento 2: Tráfico Intermedio (Normal)

```python
# main.py
Vehiculo.v0 = 10   # Velocidad normal
sim = Simulacion(debug=False, seed=42)
# Resultado esperado: Congestión moderada
```

### Experimento 3: Autopista (Fluido)

```python
# main.py
Vehiculo.v0 = 15   # Velocidad rápida
sim = Simulacion(debug=False, seed=42)
# Resultado esperado: Poco congestión
```

### Experimento 4: Optimización de Semáforo

```python
# main.py
Vehiculo.v0 = 10

# Prueba 1: Ciclo corto (verde=8, rojo=8)
# Edita en simulacion.py:
self.semaforo = Semaforo(40, 8, 2, 8)
sim = Simulacion(debug=False, seed=42)

# Prueba 2: Ciclo largo (verde=20, rojo=20)
self.semaforo = Semaforo(40, 20, 2, 20)
sim = Simulacion(debug=False, seed=42)

# Compara métricas: ¿cuál tiene menos armonía en cola?
```

---

## 🔗 Flujo de Parámetros en la Simulación

```
main.py
  ├─ define: Vehiculo.v0 = 10
  ├─ crea: Simulacion(debug=False, seed=42)
  │
  └─ Simulacion.__init__()
      ├─ crea: self.idm = IDM()
      │   └─ IDM.__init__()
      │       └─ self.v0 = Vehiculo.v0  ← ✓ Lee el valor global
      │
      ├─ crea: self.semaforo = Semaforo(40, 12, 2, 12)
      │
      └─ paso(dt) [cada 0.1s]
          ├─ para cada vehículo v:
          │   └─ aceleración = idm.calcular_aceleracion(v, ...)
          │       └─ usa: self.v0 (que es 10)
          │
          └─ imprime métricas
```

---

## ⚠️ Notas Importantes

1. **Cambios antes de crear Simulacion()**

   ```python
   Vehiculo.v0 = 15
   sim = Simulacion()  # ✓ Correcto
   ```

2. **Cambios después de crear Simulacion()**

   ```python
   sim = Simulacion()
   Vehiculo.v0 = 15    # ⚠️ Funciona pero solo para nuevos vehículos
   ```

3. **Para reproducibilidad exacta**
   ```python
   import random
   random.seed(42)      # Fija tiempos de reacción
   sim = Simulacion(seed=42)  # Fija generación de vehículos
   ```

---

## 📊 Variables de Experimento para Tu Tesis

Para un análisis académico riguroso, varía UNA variable a la vez:

**Variable independiente**: Vehiculo.v0
**Variables dependientes** (métricas):

- Velocidad promedio
- Tiempo promedio de espera
- Longitud máxima de cola
- Eficiencia del semáforo

Ejemplo de ejecutable:

```python
resultados = {}

for v0 in [5, 10, 15, 20]:
    Vehiculo.v0 = v0
    sim = Simulacion(debug=False, seed=42)
    # Corre simulación
    # Registra métricas en resultados[v0]

# Análisis: ¿Cómo varía congestión con v0?
```

---

**Actualizado**: Marzo 2026
