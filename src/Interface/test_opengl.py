# test_opengl.py

import tkinter as tk
from visualization.robot_opengl_renderer import RobotOpenGLRenderer
import numpy as np

root = tk.Tk()
root.title("Test OpenGL")

renderer = RobotOpenGLRenderer(root, width=800, height=600)
renderer.pack(fill=tk.BOTH, expand=True)

# Données de test
positions = [
    np.array([0.0, 0.0, 0.0]),
    np.array([0.5, 0.0, 0.0]),
    np.array([0.5, 0.5, 0.0]),
    np.array([0.5, 0.5, 0.5])
]

joint_types = ['R', 'R', 'R']

renderer.plot_robot(positions, joint_types)

root.mainloop()