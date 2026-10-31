# 🌐 Motor de Geometría Hiperdimensional 12D

> **Resumen del Sistema:** Este script genera un politopo cruzado (*Cross-Polytope*) en un espacio de 12 dimensiones, aplica rotaciones entrelazadas simultáneas a través de múltiples hiperplanos, lo colapsa mediante una proyección en cascada con perspectiva real hasta 3D, y lo renderiza de manera optimizada usando **NumPy** y **Matplotlib** en **Linux Mint**.

---

## 🛠️ 1. El Entorno: Linux Mint + Python

Linux Mint destaca por su bajo consumo de recursos de escritorio (Cinnamon / XFCE / MATE) y su excelente gestión del kernel para tareas científicas y de procesamiento en Python.

* **NumPy:** Se encarga de la vectorización matemática masiva y las transformaciones matriciales de alta velocidad necesarias para manipular 12 dimensiones simultáneamente sin cuellos de botella.
* **Matplotlib (`FuncAnimation`):** Gestiona el bucle de renderizado gráfico a 60 FPS, proyectando la malla 3D final de manera fluida mediante la técnica de separación por `np.nan` en las líneas.

---

## 📐 2. Anatomía del Código (Paso a Paso)

### A. Creación del Hiper-Politopo (12D)
```python
DIMENSIONES = 12
```
* **Vértices (24 puntos):** En un *Cross-Polytope* de 12D, existen 12 ejes ortogonales. Cada eje tiene un polo positivo ($+2.0$) y uno negativo ($-2.0$), lo que resulta exactamente en $12 \times 2 = 24$ vértices simétricos puros.
* **Aristas Hiper-Cristalinas:** Se evalúan todas las combinaciones posibles entre los 24 vértices. Se conectan todos con todos, **excepto** los polos opuestos directos (`-vertices[j]`), formando una red cristalina sumamente densa y estructurada.

### B. Rotación Entrelazada en Hiperplanos
La función `rotacion_hiperdimensional` es el corazón del movimiento:
* En lugar de rotar en un solo plano (como en 3D), el script recorre las dimensiones de 2 en 2 (`range(0, DIMENSIONES - 1, 2)`).
* A cada plano hiperdimensional se le asigna un **factor de velocidad único** (`1.0 + (d * 0.15)`). Esto evita que la figura rote de forma rígida o predecible, generando un caos ordenado y orgánico de rotación multidimensional simultánea.

### C. Proyección en Cascada (De 12D a 3D)
El mayor desafío de visualizar 12D en una pantalla de computadora es la pérdida de dimensiones. El script resuelve esto con una **reducción dimensional progresiva**:
* Un bucle inverso (`for d in range(DIMENSIONES - 1, 2, -1)`) reduce la figura paso a paso: de 12D a 11D, a 10D... hasta llegar a 3D.
* En cada paso, aplica un factor de **perspectiva espacial** (`distancia / (distancia - puntos_actuales[:, d] * 0.6)`), lo que simula profundidad real para que los vértices lejanos se vean más pequeños y se eviten distorsiones extremas (asíntotas).

### D. Renderizado de Alto Rendimiento
Para evitar dibujar miles de líneas una por una (lo que congelaría cualquier gráfico):
* Se utiliza una **estrategia de vectorización masiva**: todas las coordenadas de las aristas se agrupan en tres grandes listas (`xs`, `ys`, `zs`).
* Se utiliza `np.nan` para separar los trazos de las aristas individuales dentro de una sola línea continua (`ax.plot`), permitiendo que Matplotlib dibuje toda la malla cristalina (en color Cian Neón `#00ffcc`) en un solo ciclo de CPU por fotograma.

---

## 💻 3. Código Fuente Principal (`dodecaracto.py`)

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 👑 NUEVA CONFIGURACIÓN: EQUILIBRIO PERFECTO 12D 👑
DIMENSIONES = 12  

print(f"🚀 Iniciando motor en {DIMENSIONES}D. Visualizando la geometría pura del hiperespacio.")

# 1. Generamos el Cross-Polytope completo en 12D (24 vértices perfectamente simétricos)
base_vertices = []
for i in range(DIMENSIONES):
    v1 = np.zeros(DIMENSIONES)
    v2 = np.zeros(DIMENSIONES)
    v1[i] = 2.0
    v2[i] = -2.0
    base_vertices.append(v1)
    base_vertices.append(v2)
vertices = np.array(base_vertices, dtype=float)

# 2. Conectar aristas (Estructura hiper-cristalina limpia)
edges = []
num_vertices = len(vertices)
for i in range(num_vertices):
    for j in range(i + 1, num_vertices):
        # Conectamos todos los ejes excepto polos opuestos directos
        if not np.allclose(vertices[i], -vertices[j]):
            edges.append((i, j))

# 3. Rotación entrelazada en múltiples hiperplanos de la 12va dimensión
def rotacion_hiperdimensional(points, angulo):
    R = np.copy(points)
    # Hacemos rotar pares de dimensiones consecutivas a diferentes velocidades
    for d in range(0, DIMENSIONES - 1, 2):
        factor_velocidad = 1.0 + (d * 0.15)
        c = np.cos(angulo * factor_velocidad)
        s = np.sin(angulo * factor_velocidad)
        
        eje_x = R[:, d].copy()
        eje_y = R[:, d + 1].copy()
        
        R[:, d] = eje_x * c - eje_y * s
        R[:, d + 1] = eje_x * s + eje_y * c
    return R

# 4. Proyección en cascada controlada (Desde 12D hasta 3D con perspectiva real)
def proyeccion_12d_a_3d(points, distancia=4.0):
    puntos_actuales = np.copy(points)
    
    # Colapsamos el hiperespacio de la dimensión 11 bajando consecutivamente hasta la 3
    for d in range(DIMENSIONES - 1, 2, -1):
        # Distancia de seguridad para evitar que las asíntotas rompan la figura
        factor = distancia / (distancia - puntos_actuales[:, d] * 0.6)
        puntos_actuales = puntos_actuales[:, :d] * factor[:, None]
        
    return puntos_actuales

# 5. Escena Gráfica limpia
fig = plt.figure(figsize=(9, 9))
ax = fig.add_subplot(111, projection='3d')
plt.title(f"Hiper-Malla Cristalina de {DIMENSIONES} Dimensiones ({len(edges)} aristas)")

# Límites estables para apreciar la profundidad
ax.set_xlim([-3, 3])
ax.set_ylim([-3, 3])
ax.set_zlim([-3, 3])
ax.axis('off')

# Línea ultra fluida indexada por NaNs en color Cian Neón
line, = ax.plot([], [], [], color='#00ffcc', alpha=0.5, lw=1.0)

# 6. Animación principal a 60 FPS
def update(frame):
    angulo = frame * 0.015
    
    # Rotar en el hiperespacio profundo y colapsar a la pantalla
    rotated = rotacion_hiperdimensional(vertices, angulo)
    projected = proyeccion_12d_a_3d(rotated)
    
    # Vectorización masiva instantánea
    xs, ys, zs = [], [], []
    for i, j in edges:
        xs.extend([projected[i, 0], projected[j, 0], np.nan])
        ys.extend([projected[i, 1], projected[j, 1], np.nan])
        zs.extend([projected[i, 2], projected[j, 2], np.nan])
        
    line.set_data(xs, ys)
    line.set_3d_properties(zs)
    
    # Suave paneo de cámara para añadir sensación de volumen tridimensional
    ax.view_init(elev=20 + np.sin(frame * 0.03) * 5, azim=frame * 0.4)
    return line,

# Ejecución de alto rendimiento
ani = FuncAnimation(fig, update, frames=360, interval=20, blit=True)
plt.show()
```

---

## 🚀 4. Guía de Instalación y Ejecución en Linux Mint

Para ejecutar este motor hiperdimensional desde la consola de Linux Mint:

1. **Abrir la terminal:**
   ```bash
   Ctrl + Alt + T
   ```

2. **Instalar dependencias necesarias:**
   ```bash
   pip install numpy matplotlib
   ```

3. **Crear el archivo del script:**
   ```bash
   nano dodecaracto.py
   ```
   *(Pega el código fuente anterior, guarda presionado `Ctrl + O`, presiona `Enter` y sal con `Ctrl + X`)*.

4. **Ejecutar el programa:**
   ```bash
   python3 dodecaracto.py
   ```# Dodecaracto-
