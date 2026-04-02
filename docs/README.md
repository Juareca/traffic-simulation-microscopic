# TrafficSimulator 2.0

**Simulación microscópica de tráfico vehicular usando el Intelligent Driver Model (IDM)**

## 📋 Descripción

TrafficSimulator 2.0 es una simulación microscópica de tráfico que modelea el comportamiento individual de vehículos en una carretera con semáforo. Implementa el **Intelligent Driver Model (IDM)**, un modelo de seguimiento vehicular ampliamente validado en la investigación de transporte.

### Características Principales

- ✅ Modelo IDM con parámetros realistas
- ✅ Comportamiento humano (tiempo de reacción variable)
- ✅ Semáforo con ciclo temporizado (rojo-amarillo-verde)
- ✅ Métricas de desempeño (cola, velocidad, tiempo de espera)
- ✅ Interfaz gráfica interactiva (PySide6)
- ✅ Modo debug configurable
- ✅ Documentación académica completa

---

## 🧠 Teoría del Modelo

### ¿Qué es el Intelligent Driver Model (IDM)?

El IDM es un modelo microscópico de tráfico que describe el comportamiento de aceleración/desaceleración de vehículos basado en tres factores principales:

1. **Velocidad deseada** (v₀): Velocidad que el conductor intenta mantener
2. **Distancia segura**: Brecha mínima respecto al vehículo adelante
3. **Diferencia de velocidades**: Cambio relativo de velocidad

### Ecuación Fundamental del IDM

$$a_n(t) = a_{max} \left[ 1 - \left(\frac{v}{v_0}\right)^{\delta} - \left(\frac{s^*}{s}\right)^2 \right]$$

donde:

- **aₙ(t)**: Aceleración del vehículo n en el tiempo t [m/s²]
- **a_max**: Aceleración máxima [m/s²]
- **v**: Velocidad actual del vehículo [m/s]
- **v₀**: Velocidad deseada [m/s]
- **δ**: Exponente (controla sensibilidad a velocidad)
- **s**: Distancia actual al vehículo adelante [m]
- **s\***: Distancia dinámica deseada [m]

### Distancia Dinámica Deseada (s\*)

$$s^* = s_0 + vT + \frac{v \Delta v}{2\sqrt{a_{max} b}}$$

donde:

- **s₀**: Distancia mínima de parada [m]
- **T**: Tiempo de reacción/brecha temporal [s]
- **Δv = v - v_adelante**: Diferencia de velocidad [m/s]
- **b**: Desaceleración cómoda [m/s²]

### Interpretación Física

El primer término $(1 - (v/v_0)^δ)$ representa la **aceleración en vía libre** (cuando no hay vehículo adelante). El segundo término $((s*/s)^2)$ modela la **desaceleración ante obstáculos cercanos**.

---

## ⚙️ Parámetros del Modelo

### Parámetros del IDM (valores por defecto)

| Parámetro             | Símbolo | Valor     | Rango Típico | Interpretación                        |
| --------------------- | ------- | --------- | ------------ | ------------------------------------- |
| **Velocidad deseada** | **v₀**  | **4 m/s** | **4-15 m/s** | **VINCULADA A: Vehiculo.v0** ✓        |
| Tiempo de reacción    | T       | 1.5 s     | 0.5-2.0 s    | Brecha temporal con vehículo adelante |
| Aceleración máxima    | a_max   | 2 m/s²    | 1-3 m/s²     | Máxima capaz del vehículo             |
| Desaceleración cómoda | b       | 3 m/s²    | 1-5 m/s²     | Desaceleración normal y confortable   |
| Distancia mínima      | s₀      | 2 m       | 1-3 m        | Brecha mínima en parada completa      |
| Exponente             | δ       | 4         | 4-6          | Exponente para término de velocidad   |

#### 🔗 Integración Vehiculo ↔ IDM

La velocidad deseada (v₀) ahora está **vinculada dinámicamente** a la clase `Vehiculo`:

```python
# dominio/vehiculo.py:
class Vehiculo:
    v0 = 5  # ← Atributo de clase global

# dominio/idm.py:
class IDM:
    def __init__(self):
        self.v0 = Vehiculo.v0  # ← Lee el valor global
```

**Ventaja**: Cambiar velocidad deseada sin editar código:

```bash
# En main.py:
Vehiculo.v0 = 10  # Cambiar para TODOS los vehículos
sim = Simulacion(debug=False)
```

**Valores recomendados**:

- `Vehiculo.v0 = 4` → Tráfico urbano lento
- `Vehiculo.v0 = 10` → Tráfico normal
- `Vehiculo.v0 = 15` → Autopista rápida

📘 **Ver [PARAMETROS_GUIA.md](PARAMETROS_GUIA.md) para guía completa de parámetros.**

### Parámetros del Semáforo (valores por defecto)

| Parámetro       | Valor  | Unidad       | Notas                  |
| --------------- | ------ | ------------ | ---------------------- |
| Posición        | 40     | metros       | Ubicación en carretera |
| Fase verde      | 12     | segundos     | Duración luz verde     |
| Fase amarilla   | 2      | segundos     | Duración luz amarilla  |
| Fase roja       | 12     | segundos     | Duración luz roja      |
| **Ciclo total** | **26** | **segundos** | 12+2+12                |

### Parámetros de Simulación

| Parámetro               | Valor           | Unidad   |
| ----------------------- | --------------- | -------- |
| Rango máximo            | 150             | metros   |
| Intervalo de generación | 2-5 (aleatorio) | segundos |
| Paso temporal           | 0.1             | segundos |

---

## 🚀 Instalación y Configuración

### Requisitos

- **Python 3.8+**
- **PySide6** (interfaz gráfica)

### Instalación

```bash
# 1. Crear entorno virtual (si no existe)
python -m venv env

# 2. Activar entorno
# En Windows:
.\env\Scripts\Activate.ps1

# En Linux/Mac:
source env/bin/activate

# 3. Instalar dependencias
pip install PySide6

# 4. Verificar instalación
python -c "import PySide6; print('✓ PySide6 instalado correctamente')"
```

### Estructura del Proyecto

```
TrafficSimulator2.0/
├── main.py                  # Punto de entrada
├── dominio/                 # Lógica de simulación
│   ├── simulacion.py       # Motor principal
│   ├── vehiculo.py         # Clase Vehiculo
│   ├── semaforo.py         # Control de semáforos
│   ├── idm.py              # Modelo IDM
│   └── metricas.py         # Cálculo de métricas
├── presentacion/           # Interfaz gráfica
│   ├── main_window.py      # Ventana principal
│   └── simulation_widget.py # Widget de visualización
├── env/                    # Entorno virtual
└── README.md               # Este archivo
```

---

## 💻 Cómo Ejecutar

### Ejecución Normal (poco output)

```bash
python main.py
```

Genera una ventana gráfica con visualización en tiempo real. Imprime métricas resumidas cada paso.

### Ejecución con Debug Detallado

```bash
# Edita main.py y cambia:
# sim = Simulacion(debug=False)
# a:
# sim = Simulacion(debug=True)

python main.py
```

Muestra información detallada de cada vehículo, estado del semáforo, y cálculos internos. **Advertencia**: Genera mucho output.

### Archivo `main.py`

```python
from PySide6.QtWidgets import QApplication
from dominio.simulacion import Simulacion
from presentacion.main_window import MainWindow
import sys

def main():
    app = QApplication(sys.argv)

    # debug=False: solo métricas resumidas (recomendado)
    # debug=True: información detallada (útil para debugging)
    sim = Simulacion(debug=False)

    window = MainWindow(sim)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

---

## 📊 Resultados Esperados

### Métricas Monitoreadas

Cada paso (0.1 segundos) se imprime:

```
⏱️ 15.2s | 🚦 rojo | Cola: 5 | Vel: 3.45 m/s | Activos: 8
```

Significado:

- **⏱️ 15.2s**: Tiempo de simulación
- **🚦 rojo**: Estado actual del semáforo
- **Cola: 5**: Vehículos detenidos o muy lentos
- **Vel: 3.45 m/s**: Velocidad promedio (escala 0-5 m/s típicamente)
- **Activos: 8**: Vehículos en simulación activa

### Patrones Observables

Con los parámetros por defecto, esperarías ver:

1. **Aceleración inicial**: Vehículos aceleran desde -5m hasta semáforo
2. **Frenada ante semáforo rojo**: Cola forma cuando semáforo se pone rojo
3. **Reacción retrasada**: Debido a tiempo de reacción humano (0.8-1.5s)
4. **Fase amarilla**: Conductores pueden acelerar o frenar
5. **Fase verde**: Se disipa la cola gradualmente

### Visualización Gráfica

En la ventana se ve:

- 🏁 Carretera gris horizontal
- 🚦 Semáforo (verde/amarillo/rojo)
- 🔵 Vehículos azules

---

## 🔄 Reproducibilidad

### Semilla Aleatoria

Para obtener resultados **reproducibles exactamente**, puedes usar una semilla aleatoria fija:

```python
import random

# En main.py, antes de crear Simulacion():
random.seed(42)  # Cualquier número "mágico"

sim = Simulacion(debug=False)
```

Con la misma semilla, obtendrás **exactamente** la misma secuencia de tiempos de reacción, velocidades iniciales, e intervalos de llegada.

### Versiones Requeridas

Para reproducir exactamente los resultados de este proyecto:

```
Python:         3.8 o superior
PySide6:        6.0 o superior
Sistema:        Windows (también funciona en Linux/Mac)
Semilla:        random.seed(42)
```

### Documentación de Ejecución

Cuando reportes resultados, especifica:

```
Configuración de la simulación:
- Semilla aleatoria: 42
- Modo debug: False
- Parámetros IDM: v0=5, T=1.5, a_max=2, b=3
- Ciclo semáforo: 12s verde, 2s amarillo, 12s rojo
- Pasos simulados: 1000 (100 segundos de simulación)
```

---

## 📚 Referencias Bibliográficas

### Referencias Principales

[1] **Kerner, B. S., & Konhäuser, P.** (1993).  
"Structure and assignment of vehicle convoys in multilane traffic flow."  
_Transportation Research Record_, (1408), 22-28.

[2] **Treiber, M., Hennecke, A., & Helbing, D.** (2000).  
"Congested traffic states in empirical observations and microscopic traffic models."  
_Physical Review E_, 62(2), 1805.

[3] **Treiber, M., & Kesting, A.** (2013).  
"Traffic flow dynamics: Data, models and simulation."  
_Springer Science+Business Media_.

### Lecturas Complementarias

- Helbing, D. (2001). "Traffic and related self-driven many-particle systems." _Reviews of Modern Physics_, 73(4), 1067.
- Nagel, K., & Schreckenberg, M. (1992). "A cellular automaton model for freeway traffic." _Journal de Physique I_, 2(12), 2221-2229.
- Gazis, D. C., Herman, R., & Rothery, R. W. (1961). "Nonlinear follow-the-leader models of traffic flow." _Operations Research_, 9(4), 545-567.

---

## 🤝 Contribuciones y Mejoras Futuras

### Posibles Extensiones

- [ ] Múltiples carriles de tráfico
- [ ] Giros e intersecciones complejas
- [ ] Análisis estadístico de resultados (gráficos)
- [ ] Exportación de datos a CSV
- [ ] Diferentes tipos de vehículos
- [ ] Comportamientos agresivos/defensivos
- [ ] Integración con datos reales de tráfico

### Testing

Para validar el modelo (trabajo futuro):

```bash
# Ejecutar tests unitarios
python -m pytest tests/

# Verificar parámetros IDM
pytest tests/test_idm.py -v

# Verificar semáforo
pytest tests/test_semaforo.py -v
```

---

## 📝 Licencia

Proyecto académico para fines de investigación y educación.

---

## ✉️ Contacto

**Autor**: [Tu nombre]  
**Institución**: [Tu universidad]  
**Proyecto**: Trabajo de Grado - Simulación de Tráfico  
**Fecha**: Marzo 2026

---

**Última actualización**: 30 de marzo de 2026
