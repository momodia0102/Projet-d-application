#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Générateur de script robot (cinématique directe)
Compatible SYMORO – Version pédagogique & recherche

Auteur : Projet Robot_Modeler
"""

from datetime import datetime


class RobotScriptGenerator:
    """
    Génère un script Python autonome pour la visualisation
    et l'étude cinématique d'un robot série.
    """

    def __init__(self, robot_name, dh_table, sigmas, constants):
        """
        Parameters
        ----------
        robot_name : str
            Nom du robot
        dh_table : list of list
            [[theta, d, r, alpha], ...] (numériques)
        sigmas : list
            0 = rotatif, 1 = prismatique
        constants : dict
            {"D3": 1.0, "RL4": 1.0, ...}
        """
        self.robot_name = robot_name
        self.dh_table = dh_table
        self.sigmas = sigmas
        self.constants = constants

    # ==========================================================
    # 🧾 GÉNÉRATION DU SCRIPT
    # ==========================================================
    def generate(self, output_path):
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(self._header())
            f.write(self._imports())
            f.write(self._constants_section())
            f.write(self._dh_section())
            f.write(self._core_functions())
            f.write(self._visualisation())
            f.write(self._main())

    # ==========================================================
    # 🧾 SECTIONS
    # ==========================================================

    def _header(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        return f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Robot : {self.robot_name}
Script généré automatiquement
Date : {now}

-------------------------------------------------
🧪 UTILISATION :

1️⃣ Modifier les constantes géométriques si nécessaire
2️⃣ Lancer : python robot_{self.robot_name.lower()}.py
3️⃣ Utiliser les sliders pour tester le modèle

⚠️ Ne pas modifier les fonctions de calcul
-------------------------------------------------
"""
'''

    def _imports(self):
        return '''
import numpy as np
from numpy import pi
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
'''

    def _constants_section(self):
        txt = '''
# =================================================
# 🔧 CONSTANTES GÉOMÉTRIQUES (MODIFIABLES)
# =================================================
'''
        for name, value in self.constants.items():
            txt += f"{name} = {float(value)}\n"
        return txt + "\n"

    def _dh_section(self):
        txt = '''
# =================================================
# 📐 TABLE DH
# theta : remplacé par q[i] si SIGMA = 0
# d     : remplacé par q[i] si SIGMA = 1
# =================================================

DH_TABLE = [
'''
        for row in self.dh_table:
            theta, d, r, alpha = row
            txt += f"    [{theta}, {d}, {r}, {alpha}],\n"
        txt += ''']

# 0 = rotation, 1 = translation
SIGMAS = [
'''
        for s in self.sigmas:
            txt += f"    {s},\n"
        txt += ''']
\n'''
        return txt

    def _core_functions(self):
        return '''
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
'''

    def _visualisation(self):
        return '''
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
    ax.set_title("Robot : ''' + self.robot_name + '''")

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
'''

    def _main(self):
        return '''
# =================================================
# 🚀 LANCEMENT
# =================================================

if __name__ == "__main__":
    main_visualization()
'''
