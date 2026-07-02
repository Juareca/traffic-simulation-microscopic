<h1 align="center">🚦 Simulador Microscópico de Tráfico</h1>
<h3 align="center">Proyecto de grado aprobado — Universidad Cooperativa de Colombia</h3>

<!-- 📌 Banner principal -->
<p align="center">
  <img src="./img/banner.png" width="90%">
</p>

<p align="center">
<b>Título:</b> Desarrollo de un Simulador Microscópico de Tráfico Para el Análisis de Tiempos Semafóricos en Intersecciones Críticas de Santa Marta, Colombia<br>
<b>Autor:</b> Juan Alberto Arévalo Cáceres
</p>

<hr>

<h2>📘 Descripción General</h2>
<p>
Este proyecto implementa un <b>simulador microscópico de tráfico vehicular</b>, capaz de modelar el comportamiento individual de cada vehículo en una vía, considerando aceleración, interacción con el líder, distancia de seguridad, velocidad objetivo y dinámica de flujo.
</p>

<p>
El objetivo principal es desarrollar un simulador basado en un <b>modelo matemático de comportamiento vehicular</b> que permita analizar el desempeño de <b>intersecciones semaforizadas</b> bajo configuraciones de tiempos fijos.
</p>

<p>Este repositorio público contiene:</p>
<ul>
  <li>Arquitectura del sistema</li>
  <li>Código no sensible (GUI, control, loaders, configuración, semáforos, métricas)</li>
  <li>Resultados y visualizaciones</li>
  <li>Material multimedia del simulador funcionando</li>
</ul>

<p><b>⚠️ Nota:</b> El motor matemático completo (IDM, ecuaciones internas y algoritmos) no se incluye para proteger la propiedad intelectual del autor.</p>

<hr>

<h2>🧠 Modelo Microscópico (IDM)</h2>
<p>
El simulador se basa en el <b>Intelligent Driver Model (IDM)</b>, donde cada vehículo es una entidad independiente con:
</p>

<ul>
  <li>Posición</li>
  <li>Velocidad</li>
  <li>Aceleración</li>
  <li>Distancia objetivo</li>
  <li>Tiempo de reacción</li>
  <li>Velocidad deseada</li>
</ul>

<p>El modelo utiliza:</p>
<ul>
  <li>Ecuaciones diferenciales discretizadas</li>
  <li>Actualización por pasos de tiempo</li>
  <li>Funciones de aceleración dependientes del entorno local</li>
  <li>Control de colisiones y estabilidad numérica</li>
</ul>

<p>
La documentación completa se encuentra en el repositorio institucional de la UCC.  
Este repositorio presenta un resumen técnico y la arquitectura general del sistema.
</p>

<hr>

<h2>🏗️ Arquitectura del Sistema</h2>

<h3>Arquitectura en Capas</h3>
<p>El simulador está diseñado siguiendo una arquitectura modular en capas:</p>

<ol>
  <li><b>Capa de Presentación (GUI):</b> Visualización gráfica del entorno, vehículos, semáforos y métricas en tiempo real.</li>
  <li><b>Capa de Control:</b> Coordina el ciclo de simulación, gestiona semáforos y acciones del usuario.</li>
  <li><b>Capa de Dominio (Núcleo del Simulador):</b> Vehículos, semáforos, carretera y modelos matemáticos (IDM).  
      <br><b>Esta capa no se incluye en el repositorio público.</b></li>
  <li><b>Capa de Persistencia:</b> Carga de escenarios, parámetros y exportación de resultados.</li>
</ol>

<h3>Componentes Principales</h3>
<ul>
  <li><b>Simulación:</b> Control general del ciclo de actualización.</li>
  <li><b>Vehículos:</b> Entidades independientes que implementan el modelo IDM.</li>
  <li><b>Semáforos:</b> Fases, tiempos y sincronización.</li>
  <li><b>Carretera:</b> Carriles, intersecciones y conexiones.</li>
  <li><b>Métricas:</b> Flujo, densidad, tiempos de espera, velocidad promedio.</li>
  <li><b>GUI:</b> Visualización en tiempo real.</li>
  <li><b>Loaders:</b> Carga de escenarios y parámetros.</li>
</ul>

<h3>Diagrama General</h3>

<!-- 📌 Imagen del diagrama -->
<p align="center">
  <img src="./img/capas.png" width="85%">
</p>

<pre>
+------------------------------+
|        Interfaz (GUI)        |
+---------------+--------------+
                |
                v
+------------------------------+
|         Controlador          |
|  (Simulación + Semáforos)    |
+---------------+--------------+
                |
                v
+------------------------------+
|         Modelo IDM           |
|  (Vehículos + Interacciones) |
+---------------+--------------+
                |
                v
+------------------------------+
|          Métricas            |
+------------------------------+
                |
                v
+------------------------------+
|          Resultados          |
+------------------------------+
</pre>

<hr>

<h2>📊 Resultados y Visualizaciones</h2>

<h3>Panel Futuro (en construcción)</h3>
<p align="center">
  <img src="./img/futuro.jpg" width="80%">
</p>

<h3>Panel Actual (versión operativa)</h3>
<p align="center">
  <img src="./img/actual.png" width="80%">
</p>

<h3>Demostración del Simulador</h3>
<p align="center">
  <img src="./img/demo.png" width="80%">
</p>

<hr>

<h2>📁 Estructura del Proyecto</h2>

<pre>
/traffic-simulation-microscopic
│
├── control/                
├── presentacion/            
├── persistencia/              
├── main.py  
└── README.md
</pre>

<p><b>Nota:</b> La carpeta <code>dominio/</code> no se incluye en este repositorio público.</p>

<hr>

<h2>🐍 Instalación del Entorno Virtual</h2>

<ol>
  <li>Crear entorno virtual:<br><code>python -m venv env</code></li>
  <li>Activar entorno virtual:<br><code>env\Scripts\activate</code></li>
  <li>Desactivar:<br><code>deactivate</code></li>
</ol>

<h2>📦 Instalar Dependencias</h2>
<pre>pip install -r requirements.txt</pre>

<h2>▶️ Ejecutar el Simulador</h2>
<pre>python main.py</pre>

<hr>

<h2>📄 Acceso al Código Completo</h2>
<p>
El motor de simulación completo (IDM, ecuaciones internas y algoritmos) se encuentra en un repositorio privado del autor.  
Disponible únicamente para revisión profesional bajo solicitud.
</p>

<hr>

<h2>✉️ Contacto</h2>
<p>
<b>Juan Alberto Arévalo Cáceres</b><br>
📧 alberjuan2411@gmail.com<br>
📞 +57 3016482354 🇨🇴
</p>
