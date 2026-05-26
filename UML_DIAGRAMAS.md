# UML - Arquitectura de Software

Este documento contiene los diagramas UML que muestran tu diseño modular actual.

## 1. Diagrama de Clases

```plantuml
@startuml
class MainWindow {
  +MainWindow(debug=False, seed=None)
  +widget: SimulationWidget
}

class SimulationWidget {
  +SimulationWidget(simulacion)
  +actualizar()
  +paintEvent(event)
  +_pos_vehiculo(carretera, carril, veh)
  +_pos_semaforo(carretera, sem)
}

class Simulacion {
  +Simulacion(ancho, alto, grosor, debug=False, seed=None)
  +paso(dt)
  +_generar_vehiculo_en_carretera(carretera)
  +_crear_vehiculo(velocidad, carril)
  +_limpiar_vehiculos()
  +obtener_metricas_por_via()
  +idm: IDM
  +carreteras: List<Carretera>
  +semaforos: Map<String, Semaforo>
  +controlador_semaforos: ControladorSemaforos
}

class ControladorSemaforos {
  +ControladorSemaforos(semaforos, tiempos)
  +actualizar(dt)
  +semaforos: Map<String, Semaforo>
}

class Carretera {
  +Carretera(x, y, ancho, alto, direccion, num_carriles)
  +carriles: List<Carril>
  +pos_cruce: float
  +direccion: String
}

class Carril {
  +Carril(indice, direccion, carretera)
  +ordenar_vehiculos()
  +obtener_lider(vehiculo)
  +vehiculos: List<Vehiculo>
}

class Vehiculo {
  +Vehiculo(id, posicion=0.0, velocidad=0.0)
  +actualizar(dt)
  +posicion: float
  +velocidad: float
  +aceleracion: float
}

class Semaforo {
  +Semaforo(posicion)
  +estado: String
  +posicion: float
}

class IDM {
  +IDM()
  +calcular_aceleracion(vehiculo, vehiculo_adelante, s)
  +distancia_deseada_minima(velocidad, T=1.2)
}

class Metricas {
  +Metricas(carreteras)
  +registrar_cola_y_espera(carretera, carril, cola, tiempo_espera)
  +registrar_paso_detector(carretera, carril)
}

MainWindow --> SimulationWidget : crea
MainWindow --> Simulacion : crea
SimulationWidget --> Simulacion : usa
Simulacion --> ControladorSemaforos : usa
Simulacion --> Carretera : crea
Simulacion --> Semaforo : crea
Simulacion --> IDM : usa
Simulacion --> Metricas : usa
Carretera --> Carril : crea
Carril --> Vehiculo : contiene
ControladorSemaforos --> Semaforo : controla
Vehiculo --> IDM : calcula
@enduml
```

## 2. Diagrama de Secuencia

```plantuml
@startuml
actor App as "main.py"
participant Main as "MainWindow"
participant Widget as "SimulationWidget"
participant Sim as "Simulacion"
participant SemC as "ControladorSemaforos"
participant Car as "Carretera"
participant Carr as "Carril"
participant Veh as "Vehiculo"
participant IDM as "IDM"
participant Sem as "Semaforo"

App -> Main : main()
Main -> Sim : Simulacion(ancho, alto, grosor, debug, seed)
Main -> Widget : SimulationWidget(simulacion)
Widget -> Widget : timer.start(16)

loop ciclo de animación
    Widget -> Widget : actualizar()
    Widget -> Sim : paso(0.016)
    Sim -> SemC : actualizar(dt)
    SemC -> Sem : set estado
    Sim -> Car : iterar carreteras
    Car -> Carr : iterar carriles
    Carr -> Veh : iterar vehiculos
    Veh -> IDM : calcular_aceleracion(...)
    IDM --> Veh : aceleracion
    Veh -> Veh : actualizar(dt)
    Sim -> Sim : _limpiar_vehiculos()
    Sim -> Metricas : registrar datos
    Widget -> Widget : update()
    Widget -> Widget : paintEvent()
end
@enduml
```

## 3. Notas de diseño modular

- **`presentacion/`** contiene solo UI y refresco visual.
- **`control/`** orquesta el ciclo de simulación y la lógica de actualización.
- **`dominio/`** define entidades de negocio: `Vehiculo`, `Carretera`, `Carril`, `Semaforo`, `IDM` y `Metricas`.
- El acoplamiento se mantiene bajo gracias a que `Simulacion` usa el dominio y expone una interfaz simple a la UI.
- El flujo de datos va de la UI hacia el dominio a través de `Simulacion.paso()`, y luego retorna al widget para dibujar el estado actualizado.

## 4. Diagrama de Arquitectura por Capas

```plantuml
@startuml
package "Presentacion" {
  [MainWindow]
  [SimulationWidget]
}

package "Control / Aplicación" {
  [Simulacion]
  [ControladorSemaforos]
}

package "Dominio" {
  [Carretera]
  [Carril]
  [Vehiculo]
  [Semaforo]
  [IDM]
  [Metricas]
}

[MainWindow] --> [SimulationWidget]
[MainWindow] --> [Simulacion]
[SimulationWidget] --> [Simulacion]
[Simulacion] --> [ControladorSemaforos]
[Simulacion] --> [Carretera]
[Simulacion] --> [Semaforo]
[Simulacion] --> [IDM]
[Simulacion] --> [Metricas]
[Carretera] --> [Carril]
[Carril] --> [Vehiculo]
[ControladorSemaforos] --> [Semaforo]
[Vehiculo] --> [IDM]
@enduml
```
