# robot_3d_renderer.py

import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D

# --- Couleurs pour la visualisation ---
RENDER_COLORS = {
    'link': 'blue',
    'revolute': 'red',
    'prismatic': 'green',
    'base': 'gray',
    'x_axis': 'r',
    'y_axis': 'g',
    'z_axis': 'b'
}

class Robot3DRenderer:
    """
    Moteur de rendu 3D pour un robot manipulateur.
    Utilise Matplotlib pour l'affichage 3D dans un widget Tkinter.
    """
    
    def __init__(self, parent_widget, width=5, height=5, dpi=80):
        """
        Initialise le moteur de rendu 3D.
        
        Parameters
        ----------
        parent_widget : tk.Widget
            Widget parent Tkinter (le conteneur du canvas).
        """
        self.parent = parent_widget
        
        # Créer la figure Matplotlib
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # Canvas Tkinter (Pont Matplotlib → Tkinter)
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent_widget)
        self.canvas_widget = self.canvas.get_tk_widget()
        
        # Configuration initiale de l'affichage
        self._setup_axes()
        self._setup_view()
        self._plot_placeholder()

    def _setup_axes(self):
        """Configure les étiquettes et le style des axes 3D."""
        self.ax.set_xlabel('X (m)', fontsize=10)
        self.ax.set_ylabel('Y (m)', fontsize=10)
        self.ax.set_zlabel('Z (m)', fontsize=10)
        self.ax.grid(True, linestyle='--', alpha=0.3)
        
        # Rendre le fond transparent (ou blanc uni)
        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False
        self.ax.xaxis.pane.set_edgecolor('w')
        self.ax.yaxis.pane.set_edgecolor('w')
        self.ax.zaxis.pane.set_edgecolor('w')

    def _setup_view(self):
        """Configure la vue par défaut (perspective)."""
        self.ax.view_init(elev=20, azim=45)
        
    def pack(self, **kwargs):
        """Empaqueter le canvas dans le parent."""
        self.canvas_widget.pack(**kwargs)

    def clear(self):
        """Efface le contenu actuel et réinitialise les axes."""
        self.ax.clear()
        self._setup_axes()
        
    def _plot_placeholder(self):
        """Affiche un message placeholder dans la zone de visualisation."""
        self.ax.text2D(0.5, 0.5, 
                       "🤖 Robot en attente\n\nLancez le calcul MGD pour visualiser",
                       transform=self.ax.transAxes, 
                       fontsize=12, ha='center', va='center', 
                       color='gray')
        self.canvas.draw()
        
    def plot_robot(self, joint_positions, joint_types=None, frame_transforms=None, frame_size=0.15):
        """
        Affiche le robot à partir des positions des joints.
        
        Parameters
        ----------
        joint_positions : list of np.array (3,)
            Liste des positions 3D de chaque frame.
        joint_types : list of str, optional
            Types de joints ('R' ou 'P') (pour la couleur/forme).
        frame_transforms : list of np.array (4,4), optional
            Matrices de transformation pour chaque frame (pour les axes).
        frame_size : float
            Taille des repères de coordonnées.
        """
        self.clear()
        
        if not joint_positions or len(joint_positions) < 2:
            self._plot_placeholder()
            return
            
        positions = np.array(joint_positions)
        
        # 1. Tracer les segments (liens)
        self._plot_links(positions)
        
        # 2. Tracer les joints (Sphères ou Cubes)
        self._plot_joints(positions, joint_types)
        
        # 3. Tracer les repères de coordonnées
        if frame_transforms is not None:
            for i, T in enumerate(frame_transforms):
                origin = T[:3, 3]
                rotation = T[:3, :3]
                # Le Frame 0 (base) est plus grand
                size = frame_size * 1.5 if i == 0 else frame_size
                self._plot_frame(origin, rotation, size=size, label=f'F{i}' if i > 0 else 'Base')
        
        # 4. Ajuster les limites des axes
        self._auto_scale(positions)
        
        # 5. Rafraîchir l'affichage
        self.canvas.draw()
        
    def _plot_links(self, positions):
        """Trace les liens entre les joints."""
        
        # Matplotlib est lent avec beaucoup de segments séparés.
        # Nous traçons une seule ligne épaisse.
        
        x_vals = positions[:, 0]
        y_vals = positions[:, 1]
        z_vals = positions[:, 2]
        
        # Ligne principale du robot
        self.ax.plot(x_vals, y_vals, z_vals, 
                     color=RENDER_COLORS['link'], 
                     linestyle='-', 
                     linewidth=6, 
                     alpha=0.8)

    def _plot_joints(self, positions, joint_types):
        """Trace les joints."""
        if joint_types is None:
            joint_types = ['R'] * len(positions)
            
        # Le premier point (Frame 0) est la base, pas un joint mobile
        
        # Positions des joints mobiles (à partir de l'index 1)
        mobile_positions = positions[1:]
        
        for i, (pos, jtype) in enumerate(zip(mobile_positions, joint_types)):
            if jtype == 'R':
                # Joint rotatif: sphère rouge
                self.ax.scatter(*pos, c=RENDER_COLORS['revolute'], s=250, marker='o', 
                                edgecolors='black', linewidths=1.5, alpha=0.9)
            elif jtype == 'P':
                # Joint prismatique: cube vert
                self.ax.scatter(*pos, c=RENDER_COLORS['prismatic'], s=250, marker='s', 
                                edgecolors='black', linewidths=1.5, alpha=0.9)

        # Base fixe (Frame 0)
        self.ax.scatter(*positions[0], c=RENDER_COLORS['base'], s=300, marker='D',
                        edgecolors='k', linewidths=1.5, alpha=0.9)

    def _plot_frame(self, origin, rotation_matrix, size=0.1, label=''):
        """Trace un repère de coordonnées 3D."""
        
        colors = [RENDER_COLORS['x_axis'], RENDER_COLORS['y_axis'], RENDER_COLORS['z_axis']]  # X, Y, Z
        
        for i in range(3):
            axis = rotation_matrix[:, i] * size
            # Utilisation de quiver pour dessiner des flèches
            self.ax.quiver(origin[0], origin[1], origin[2], 
                          axis[0], axis[1], axis[2], 
                          color=colors[i], arrow_length_ratio=0.3,
                          linewidth=2, alpha=0.8)
                          
        # Optionnel: ajouter un label pour identifier le frame
        # self.ax.text(origin[0] + size, origin[1], origin[2], label, fontsize=8, color=colors[2])
                          
    def _auto_scale(self, positions):
        """Ajuste automatiquement les limites des axes en assurant un ratio d'aspect égal."""
        
        if positions.shape[0] == 0:
            return

        x_min, x_max = positions[:, 0].min(), positions[:, 0].max()
        y_min, y_max = positions[:, 1].min(), positions[:, 1].max()
        z_min, z_max = positions[:, 2].min(), positions[:, 2].max()

        # Inclure l'origine (0, 0, 0) dans l'étendue
        x_min, x_max = min(x_min, 0), max(x_max, 0)
        y_min, y_max = min(y_min, 0), max(y_max, 0)
        z_min, z_max = min(z_min, 0), max(z_max, 0)

        x_range = x_max - x_min
        y_range = y_max - y_min
        z_range = z_max - z_min

        # Déterminer la plage maximale pour assurer un aspect ratio égal
        max_range = max(x_range, y_range, z_range)
        
        # Ajouter une petite marge (ex: 20%) et centrer
        padding = max_range * 0.2
        
        mid_x = (x_max + x_min) / 2
        mid_y = (y_max + y_min) / 2
        mid_z = (z_max + z_min) / 2

        limit = max_range / 2 + padding
        
        self.ax.set_xlim(mid_x - limit, mid_x + limit)
        self.ax.set_ylim(mid_y - limit, mid_y + limit)
        self.ax.set_zlim(mid_z - limit, mid_z + limit)
        
        # Forcer le ratio d'aspect égal (nécessaire pour la 3D)
        self.ax.set_box_aspect([1, 1, 1])
        
    def rotate_view(self, delta_azim=0, delta_elev=0):
        """Rotation de la vue (azim = horizontal, elev = vertical)."""
        elev, azim = self.ax.elev, self.ax.azim
        self.ax.view_init(elev=elev + delta_elev, azim=azim + delta_azim)
        self.canvas.draw()
        
    def reset_view(self):
        """Réinitialise la vue aux paramètres par défaut."""
        self.ax.view_init(elev=20, azim=45)
        self.canvas.draw()
        
    def zoom(self, factor=1.1):
        """Zoom in/out en ajustant les limites des axes."""
        # Note: Le zoom est plus complexe avec l'aspect ratio fixe.
        # On peut simuler le zoom en réduisant (zoom +) ou augmentant (zoom -) l'étendue des limites.
        
        xlim = self.ax.get_xlim()
        x_mid = (xlim[0] + xlim[1]) / 2
        x_range = (xlim[1] - xlim[0]) / factor
        
        self.ax.set_xlim(x_mid - x_range/2, x_mid + x_range/2)
        self.ax.set_ylim(x_mid - x_range/2, x_mid + x_range/2) # Maintien du ratio
        self.ax.set_zlim(x_mid - x_range/2, x_mid + x_range/2)
        
        self.canvas.draw()