# robot_opengl_renderer.py

import numpy as np
import tkinter as tk
from OpenGL.GL import *
from OpenGL.GLU import *
import math

try:
    from pyopengltk import OpenGLFrame
    USE_PYOPENGLTK = True
except ImportError:
    USE_PYOPENGLTK = False
    print("⚠️ pyopengltk non disponible, Tkinter Canvas basique utilisé.")

try:
    from OpenGL.GLUT import glutSolidCube, glutSolidSphere
    HAS_GLUT = True
except ImportError:
    HAS_GLUT = False
    print("⚠️ GLUT non disponible, utiliser des primitives alternatives")

from .joint_node import JointNode

# Couleurs du robot
COLORS_ROBOT = {
    'base': (0.5, 0.5, 0.5, 1.0), 
    'link': (0.2, 0.4, 0.8, 1.0), 
    'revolute': (0.8, 0.2, 0.2, 1.0),
    'prismatic': (0.2, 0.8, 0.2, 1.0), 
    'x_axis': (1.0, 0.0, 0.0, 1.0),
    'y_axis': (0.0, 1.0, 0.0, 1.0),
    'z_axis': (0.0, 0.0, 1.0, 1.0),
}


class RobotOpenGLWidget(OpenGLFrame):
    """Widget OpenGL qui hérite correctement de OpenGLFrame."""
    
    def __init__(self, parent, renderer, **kwargs):
        self.renderer = renderer
        super().__init__(parent, **kwargs)
    
    def initgl(self):
        """Configuration OpenGL initiale."""
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        
        glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 5.0, 1.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.3, 0.3, 0.3, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
        
        glLightfv(GL_LIGHT1, GL_POSITION, [-5.0, 5.0, 5.0, 1.0])
        glLightfv(GL_LIGHT1, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        
        glClearColor(1.0, 1.0, 1.0, 1.0) # Fond blanc
        
        # Projection (mise à jour lors du premier rendu)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(40.0, 1.0, 0.1, 50.0) # Valeurs initiales
        glMatrixMode(GL_MODELVIEW)
    
    def redraw(self):
        """Appelée à chaque frame."""
        self.renderer._render_scene()


class RobotOpenGLRenderer:
    """
    Moteur de rendu OpenGL V2. Approche SYMORO : hiérarchie de nœuds.
    """
    
    def __init__(self, parent_widget, width=600, height=600):
        self.parent = parent_widget
        self.width = width
        self.height = height
        self.camera_distance = 10.0
        self.camera_azimuth = 45.0
        self.camera_elevation = 30.0
        self.center_x, self.center_y, self.center_z = 0.0, 0.0, 0.0
        self.root_node = None # Racine de la hiérarchie JointNode
        self.joint_nodes = {}
        self.length_scale = 0.1
        self.mouse_down = False
        self.last_mouse_x, self.last_mouse_y = 0, 0
        
        self._create_opengl_widget()
    
    def _create_opengl_widget(self):
        if USE_PYOPENGLTK:
            self.gl_widget = RobotOpenGLWidget(
                self.parent, renderer=self,
                width=self.width, height=self.height
            )
            self.gl_widget.pack(fill=tk.BOTH, expand=True)
            # Bindings souris
            self.gl_widget.bind("<Button-1>", self._on_mouse_down)
            self.gl_widget.bind("<B1-Motion>", self._on_mouse_drag)
            self.gl_widget.bind("<ButtonRelease-1>", self._on_mouse_up)
            self.gl_widget.bind("<MouseWheel>", self._on_mouse_wheel)
            self.gl_widget.bind("<Button-4>", self._on_mouse_wheel)
            self.gl_widget.bind("<Button-5>", self._on_mouse_wheel)
        else:
            self.canvas = tk.Canvas(self.parent, width=self.width, height=self.height, bg='#2E2E2E')
            self.canvas.pack(fill=tk.BOTH, expand=True)
            self.canvas.create_text(self.width//2, self.height//2, 
                                   text="⚠️ OpenGL non disponible", 
                                   fill='white', font=('Arial', 12), justify=tk.CENTER)

    # 🆕 MÉTHODES DE RENDU MANQUANTES
    def _apply_camera_transform(self):
        """Applique la transformation de caméra."""
        glLoadIdentity()
        
        # Calcul position caméra
        theta = math.radians(self.camera_azimuth)
        phi = math.radians(self.camera_elevation)
        
        cam_x = self.camera_distance * math.cos(phi) * math.cos(theta)
        cam_y = self.camera_distance * math.cos(phi) * math.sin(theta)
        cam_z = self.camera_distance * math.sin(phi)
        
        gluLookAt(
            cam_x, cam_y, cam_z,            # Position caméra
            self.center_x, self.center_y, self.center_z,  # Point cible
            0, 0, 1                         # Up vector
        )
    
    def _draw_grid(self, size=10, step=1):
        """Dessine une grille au sol."""
        glDisable(GL_LIGHTING)
        glColor4f(0.7, 0.7, 0.7, 0.5)
        glLineWidth(1.0)
        
        glBegin(GL_LINES)
        for i in np.arange(-size, size + 1, step):
            glVertex3f(i, -size, 0)
            glVertex3f(i, size, 0)
            glVertex3f(-size, i, 0)
            glVertex3f(size, i, 0)
        glEnd()
        glEnable(GL_LIGHTING)
    
    def _draw_main_axes(self, length=1.0):
        """Dessine les axes principaux (X, Y, Z)."""
        glDisable(GL_LIGHTING)
        glLineWidth(3.0)
        
        glBegin(GL_LINES)
        # X (Rouge)
        glColor4f(1.0, 0.0, 0.0, 1.0)
        glVertex3f(0, 0, 0)
        glVertex3f(length, 0, 0)
        
        # Y (Vert)
        glColor4f(0.0, 1.0, 0.0, 1.0)
        glVertex3f(0, 0, 0)
        glVertex3f(0, length, 0)
        
        # Z (Bleu)
        glColor4f(0.0, 0.0, 1.0, 1.0)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, length)
        glEnd()
        
        glLineWidth(1.0)
        glEnable(GL_LIGHTING)
    
    def _render_scene(self):
        """Méthode principale de rendu."""
        if not USE_PYOPENGLTK or self.root_node is None:
            return
        
        # Effacer les buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Configuration de la vue
        glViewport(0, 0, self.width, self.height)
        
        # Projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = self.width / self.height if self.height > 0 else 1.0
        gluPerspective(40.0, aspect, 0.1, 50.0)
        
        # Vue modèle
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Appliquer la caméra
        self._apply_camera_transform()
        
        # Dessiner la grille
        self._draw_grid(size=5, step=0.5)
        
        # Dessiner les axes principaux
        self._draw_main_axes(length=0.5)
        
        # Dessiner le robot (rendu récursif)
        if self.root_node:
            glPushMatrix()
            glEnable(GL_LIGHTING)
            self.root_node.draw_recursive()
            glPopMatrix()
        
        # Échange des buffers
        if hasattr(self.gl_widget, 'swap_buffers'):
            self.gl_widget.swap_buffers()

    def load_robot(self, robot):
        """Construit la hiérarchie de nœuds (JointNode) depuis un robot SYMORO."""
        self.robot = robot
        self.joint_nodes = {}
        
        # 1. Créer le nœud racine (base)
        self.root_node = JointNode(index=0, sigma=2) 
        self.joint_nodes[0] = self.root_node
        
        # 2. Construire l'arbre récursivement
        self._build_tree_recursive(0)
        
        # 3. Calculer l'échelle et initialiser les géométries
        self._compute_auto_scale()
        for node in self.joint_nodes.values():
            node.init_geometry(self.length_scale)
            
        self.refresh()

    def _build_tree_recursive(self, parent_idx):
        """Construit l'arbre récursivement en lisant les paramètres DH."""
        parent_node = self.joint_nodes[parent_idx]

        # Trouver les enfants directs (basé sur la structure du robot)
        children_indices = []
        for j in range(1, self.robot.NF):
            if hasattr(self.robot, 'ant') and j < len(self.robot.ant):
                if self.robot.ant[j] == parent_idx:
                    children_indices.append(j)

        print(f"[build_tree] parent={parent_idx} -> children={children_indices}")

        for child_idx in children_indices:
            # Récupérer les paramètres DH
            theta = self.robot.theta[child_idx] if hasattr(self.robot, 'theta') else 0
            r = self.robot.r[child_idx] if hasattr(self.robot, 'r') else 0
            alpha = self.robot.alpha[child_idx] if hasattr(self.robot, 'alpha') else 0
            d = self.robot.d[child_idx] if hasattr(self.robot, 'd') else 0
            gamma = self.robot.gamma[child_idx] if hasattr(self.robot, 'gamma') else 0
            b = self.robot.b[child_idx] if hasattr(self.robot, 'b') else 0
            sigma = self.robot.sigma[child_idx] if hasattr(self.robot, 'sigma') else 0

            child_node = JointNode(
                index=child_idx, parent=parent_node,
                theta=theta, r=r, alpha=alpha, d=d, gamma=gamma, b=b,
                sigma=sigma
            )
            self.joint_nodes[child_idx] = child_node


            self._build_tree_recursive(child_idx)

    def _compute_auto_scale(self):
        """Calcul de l'échelle automatique (longueur des tiges)."""
        min_dist = float('inf')
        for node in self.joint_nodes.values():
            if node.index == 0: 
                continue
            # On cherche le paramètre r ou d le plus petit > 0
            r_val = node._get_numeric_value(node.r_base)
            d_val = node._get_numeric_value(node.d)
            dist = max(abs(r_val), abs(d_val))
            if dist > 0 and dist < min_dist:
                min_dist = dist
        
        if min_dist == float('inf') or min_dist == 0: 
            min_dist = 1.0
        self.length_scale = 0.4 * min_dist

    def set_joint_values(self, joint_angles_deg):
        """Met à jour les valeurs articulaires."""
        if self.root_node is None or not hasattr(self, 'robot'): 
            return
        
        for j in range(1, self.robot.NJ):
            node = self.joint_nodes.get(j)
            if node is None: 
                continue
                
            var_sym = self.robot.get_q(j) if hasattr(self.robot, 'get_q') else 0
            if var_sym == 0: 
                continue
                
            var_name = str(var_sym)
            
            if var_name in joint_angles_deg:
                value = joint_angles_deg[var_name]
                
                if node.sigma == 0: # Rotation → deg to rad
                    node.set_q(np.deg2rad(value))
                elif node.sigma == 1: # Prismatique → mètres
                    node.set_q(value)
                    
        self.refresh()

    # Gestion des événements souris
    def _on_mouse_down(self, event):
        print(f"[DEBUG MOUSE] DOWN: x={event.x}, y={event.y}")
        self.mouse_down = True
        self.last_mouse_x = event.x
        self.last_mouse_y = event.y
        if hasattr(self.gl_widget, 'CaptureMouse'):
            self.gl_widget.CaptureMouse()

    def _on_mouse_drag(self, event):
        if not self.mouse_down:
            return
        
        dx = event.x - self.last_mouse_x
        dy = event.y - self.last_mouse_y
        
        print(f"[DEBUG MOUSE] DRAG: dx={dx}, dy={dy}. Elevation={self.camera_elevation:.1f}")
        self.last_mouse_x = event.x
        self.last_mouse_y = event.y
        
        # Rotation
        sensitivity = 0.5
        self.camera_azimuth += dx * sensitivity
        self.camera_elevation += dy * sensitivity
        self.camera_elevation = max(-89, min(89, self.camera_elevation))
        
        self.refresh()

    def _on_mouse_up(self, event):
        self.mouse_down = False
        if hasattr(self.gl_widget, 'HasCapture') and self.gl_widget.HasCapture():
            self.gl_widget.ReleaseMouse()

    def _on_mouse_wheel(self, event):
        # Windows/MacOS
        print(f"[DEBUG MOUSE] WHEEL: event.delta={getattr(event, 'delta', 'N/A')}")
        if hasattr(event, 'delta'):
            delta = event.delta
        # Linux
        elif event.num == 4:
            delta = 120
        elif event.num == 5:
            delta = -120
        else:
            return
        
        if delta > 0:
            self.zoom(0.9)
        else:
            self.zoom(1.1)

    def rotate_view(self, delta_azim=0, delta_elev=0):
        """Rotation programmatique"""
        self.camera_azimuth += delta_azim
        self.camera_elevation += delta_elev
        self.camera_elevation = max(-89, min(89, self.camera_elevation))
        self.refresh()

    def zoom(self, factor=1.1):
        """Zoom"""
        self.camera_distance *= factor
        self.camera_distance = max(0.5, min(20.0, self.camera_distance))
        self.refresh()

    def reset_view(self):
        """Réinitialise la vue"""
        self.camera_distance = 3.0
        self.camera_azimuth = 45.0
        self.camera_elevation = 30.0
        self.center_x = 0.0
        self.center_y = 0.0
        self.center_z = 0.0
        self.refresh()

    def refresh(self):
        """Force un rafraîchissement"""
        if USE_PYOPENGLTK and hasattr(self, 'gl_widget'):
            self.gl_widget.redraw()

    def clear(self):
        """Efface le robot"""
        self.root_node = None
        self.joint_nodes = {}
        self.refresh()

    def pack(self, **kwargs):
        """Empaquetage (déjà fait dans __init__)"""
        pass