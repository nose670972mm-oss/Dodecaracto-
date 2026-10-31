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

