#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Robot : RX90
Script généré automatiquement
Date : 2025-12-14 18:56

-------------------------------------------------
🧪 UTILISATION :

1️⃣ Modifier les constantes géométriques si nécessaire
2️⃣ Lancer : python robot_rx90.py
3️⃣ Utiliser les sliders pour tester le modèle

⚠️ Ne pas modifier les fonctions de calcul
-------------------------------------------------
"""

import numpy as np
from numpy import pi
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# =================================================
# 🔧 CONSTANTES GÉOMÉTRIQUES (MODIFIABLES)
# =================================================


# =================================================
# 📐 TABLE DH
# theta : remplacé par q[i] si SIGMA = 0
# d     : remplacé par q[i] si SIGMA = 1
# =================================================

DH_TABLE = [
    [45 ,0.0, 0.0, 0.0],
    [45, 0.0, 0.0, pi/2],
    [45, 4, 0.0, 0.0],
    [45, 0.0, 4, -pi/2],
    [45, 0.0, 0.0, pi/2],
    [45, 0.0, 0.0, -pi/2],
]

# 0 = rotation, 1 = translation
SIGMAS = [
    0,
    0,
    0,
    0,
    0,
    0,
]


# =================================================
# 🧮 NOYAU CINÉMATIQUE (NE PAS MODIFIER)
# =================================================

def dh_transform(theta, d, r, alpha):
    ct, st = np.cos(theta), np.sin(theta)
    ca, sa = np.cos(alpha), np.sin(alpha)

    return np.array([
        [ct, -st*ca,  st*sa, r*ct],
        [st,  ct*ca, -ct*sa, r*st],
        [0,   sa,     ca,    d   ],
        [0,   0,      0,     1   ]
    ], dtype=float)


def compute_skeleton(q):
    points = [[0.0, 0.0, 0.0]]
    T = np.eye(4)

    for i, (row, sigma) in enumerate(zip(DH_TABLE, SIGMAS)):
        theta, d, r, alpha = row

        if sigma == 0:   # articulation rotative
            theta = q[i]
        else:            # articulation prismatique
            d = q[i]

        T = T @ dh_transform(theta, d, r, alpha)
        points.append(T[:3, 3])

    return np.array(points)

# =================================================
# 🎨 VISUALISATION
# =================================================

def main_visualization():
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    plt.subplots_adjust(left=0.1, bottom=0.3)

    n = len(DH_TABLE)
    q0 = [0.0] * n

    pts = compute_skeleton(q0)
    line, = ax.plot(pts[:,0], pts[:,1], pts[:,2], "o-", lw=2)

    limit = max(2.0, n)
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_zlim(0, limit * 1.5)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("Robot : RX90")

    sliders = []

    def update(val):
        qs = [s.val for s in sliders]
        pts = compute_skeleton(qs)
        line.set_data(pts[:,0], pts[:,1])
        line.set_3d_properties(pts[:,2])
        fig.canvas.draw_idle()

    for i in range(n):
        ax_s = plt.axes([0.2, 0.25 - i*0.04, 0.6, 0.03])

        if SIGMAS[i] == 0:
            s = Slider(ax_s, f"θ{i+1}", -pi, pi, valinit=0.0)
        else:
            s = Slider(ax_s, f"d{i+1}", 0.0, 2.0, valinit=0.0)

        s.on_changed(update)
        sliders.append(s)

    plt.show()

# =================================================
# 🚀 LANCEMENT
# =================================================

if __name__ == "__main__":
    main_visualization()
