# robot_opengl_renderer.py

import numpy as np
import tkinter as tk
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

try:
    # Essayer d'importer pyopengltk (recommandé pour Tkinter)
    from pyopengltk import OpenGLFrame
    USE_PYOPENGLTK = True
except ImportError:
    USE_PYOPENGLTK = False
    print("⚠️ pyopengltk non disponible, utilisation de Tkinter Canvas basique")

# Couleurs du robot
COLORS_ROBOT = {
    'base': (0.5, 0.5, 0.5, 1.0),      # Gris
    'link': (0.2, 0.4, 0.8, 1.0),      # Bleu
    'revolute': (0.8, 0.2, 0.2, 1.0),  # Rouge
    'prismatic': (0.2, 0.8, 0.2, 1.0), # Vert
    'x_axis': (1.0, 0.0, 0.0, 1.0),    # Rouge
    'y_axis': (0.0, 1.0, 0.0, 1.0),    # Vert
    'z_axis': (0.0, 0.0, 1.0, 1.0),    # Bleu
}


class RobotOpenGLRenderer:
    """
    Moteur de rendu OpenGL pour robot manipulateur.
    Compatible avec Tkinter via pyopengltk ou Canvas OpenGL basique.
    """
    
    def __init__(self, parent_widget, width=600, height=600):
        """
        Initialise le rendu OpenGL.
        
        Parameters
        ----------
        parent_widget : tk.Widget
            Conteneur Tkinter parent
        width, height : int
            Dimensions du widget
        """
        self.parent = parent_widget
        self.width = width
        self.height = height
        
        # État de visualisation
        self.robot_data = None
        self.camera_distance = 3.0
        self.camera_azimuth = 45.0
        self.camera_elevation = 30.0
        
        # Variables pour la rotation interactive
        self.mouse_down = False
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        
        # Créer le widget OpenGL
        self._create_opengl_widget()
        
    def _create_opengl_widget(self):
        """Crée le widget OpenGL approprié."""
        
        if USE_PYOPENGLTK:
            # Utiliser pyopengltk (recommandé)
            self.gl_frame = OpenGLFrame(
                self.parent,
                width=self.width,
                height=self.height
            )
            self.gl_frame.pack(fill=tk.BOTH, expand=True)
            
            # Connexion des callbacks
            self.gl_frame.bind("<Button-1>", self._on_mouse_down)
            self.gl_frame.bind("<B1-Motion>", self._on_mouse_drag)
            self.gl_frame.bind("<ButtonRelease-1>", self._on_mouse_up)
            self.gl_frame.bind("<MouseWheel>", self._on_mouse_wheel)
            
            # Initialisation OpenGL
            self.gl_frame.after(100, self._init_opengl)
            
        else:
            # Fallback: Canvas Tkinter simple
            self.canvas = tk.Canvas(
                self.parent,
                width=self.width,
                height=self.height,
                bg='#2E2E2E'
            )
            self.canvas.pack(fill=tk.BOTH, expand=True)
            
            # Message d'avertissement
            self.canvas.create_text(
                self.width // 2,
                self.height // 2,
                text="⚠️ OpenGL non disponible\nInstallez pyopengltk:\npip install pyopengltk",
                fill='white',
                font=('Arial', 12),
                justify=tk.CENTER
            )
    
    def _init_opengl(self):
        """Initialise le contexte OpenGL."""
        
        if not USE_PYOPENGLTK:
            return
        
        self.gl_frame.tkMakeCurrent()
        
        # Configuration OpenGL
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        
        # Lumière
        glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 5.0, 1.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.3, 0.3, 0.3, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
        
        # Couleur de fond
        glClearColor(0.18, 0.18, 0.18, 1.0)  # Gris foncé
        
        # Viewport
        glViewport(0, 0, self.width, self.height)
        
        # Projection
        self._setup_projection()
        
        # Dessiner la scène initiale
        self._render()
    
    def _setup_projection(self):
        """Configure la projection perspective."""
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, self.width / self.height, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
    
    def _render(self):
        """Fonction principale de rendu."""
        
        if not USE_PYOPENGLTK:
            return
        
        self.gl_frame.tkMakeCurrent()
        
        # Effacer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Positionner la caméra
        self._apply_camera_transform()
        
        # Dessiner la grille
        self._draw_grid()
        
        # Dessiner le robot
        if self.robot_data:
            self._draw_robot()
        else:
            self._draw_placeholder()
        
        # Afficher
        self.gl_frame.tkSwapBuffers()
    
    def _apply_camera_transform(self):
        """Applique la transformation de caméra orbitale."""
        
        # Position de la caméra en coordonnées sphériques
        cam_x = self.camera_distance * math.cos(math.radians(self.camera_elevation)) * math.cos(math.radians(self.camera_azimuth))
        cam_y = self.camera_distance * math.cos(math.radians(self.camera_elevation)) * math.sin(math.radians(self.camera_azimuth))
        cam_z = self.camera_distance * math.sin(math.radians(self.camera_elevation))
        
        gluLookAt(
            cam_x, cam_y, cam_z,  # Position caméra
            0, 0, 0,               # Point visé
            0, 0, 1                # Vecteur "up"
        )
    
    def _draw_grid(self):
        """Dessine une grille de référence."""
        
        glDisable(GL_LIGHTING)
        glColor3f(0.3, 0.3, 0.3)
        glBegin(GL_LINES)
        
        size = 5.0
        step = 0.5
        
        # Lignes horizontales (plan XY)
        for i in np.arange(-size, size + step, step):
            glVertex3f(i, -size, 0)
            glVertex3f(i, size, 0)
            glVertex3f(-size, i, 0)
            glVertex3f(size, i, 0)
        
        glEnd()
        glEnable(GL_LIGHTING)
        
        # Axes principaux (plus épais)
        self._draw_main_axes()
    
    def _draw_main_axes(self):
        """Dessine les axes X, Y, Z principaux."""
        
        glDisable(GL_LIGHTING)
        glLineWidth(3.0)
        
        glBegin(GL_LINES)
        
        # Axe X (rouge)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(0, 0, 0)
        glVertex3f(1.5, 0, 0)
        
        # Axe Y (vert)
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 1.5, 0)
        
        # Axe Z (bleu)
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 1.5)
        
        glEnd()
        glLineWidth(1.0)
        glEnable(GL_LIGHTING)
    
    def _draw_placeholder(self):
        """Dessine un message placeholder."""
        
        glDisable(GL_LIGHTING)
        glColor3f(0.7, 0.7, 0.7)
        
        # Dessiner un cube simple au centre
        self._draw_cube(0, 0, 0, 0.3)
        
        glEnable(GL_LIGHTING)
    
    def _draw_robot(self):
        """Dessine le robot à partir des données."""
        
        positions = self.robot_data.get('positions')
        joint_types = self.robot_data.get('joint_types', [])
        transforms = self.robot_data.get('transforms', [])
        
        if not positions or len(positions) < 2:
            self._draw_placeholder()
            return
        
        # 1. Dessiner les liens (cylindres)
        self._draw_links(positions)
        
        # 2. Dessiner les joints (sphères/cubes)
        self._draw_joints(positions, joint_types)
        
        # 3. Dessiner les repères de coordonnées
        if transforms:
            self._draw_frames(transforms)
    
    def _draw_links(self, positions):
        """Dessine les segments entre les joints."""
        
        glColor4fv(COLORS_ROBOT['link'])
        
        for i in range(len(positions) - 1):
            p1 = positions[i]
            p2 = positions[i + 1]
            
            self._draw_cylinder(p1, p2, radius=0.02)
    
    def _draw_joints(self, positions, joint_types):
        """Dessine les joints."""
        
        # Base (premier point)
        glColor4fv(COLORS_ROBOT['base'])
        self._draw_sphere(positions[0], radius=0.06)
        
        # Joints mobiles
        for i in range(1, len(positions)):
            jtype = joint_types[i - 1] if i - 1 < len(joint_types) else 'R'
            
            if jtype == 'R':
                glColor4fv(COLORS_ROBOT['revolute'])
                self._draw_sphere(positions[i], radius=0.05)
            else:
                glColor4fv(COLORS_ROBOT['prismatic'])
                self._draw_cube(*positions[i], size=0.08)
    
    def _draw_frames(self, transforms):
        """Dessine les repères de coordonnées."""
        
        glDisable(GL_LIGHTING)
        glLineWidth(2.0)
        
        for T in transforms:
            origin = T[:3, 3]
            rotation = T[:3, :3]
            
            size = 0.15
            
            glBegin(GL_LINES)
            
            for i, color in enumerate([COLORS_ROBOT['x_axis'], COLORS_ROBOT['y_axis'], COLORS_ROBOT['z_axis']]):
                axis = rotation[:, i] * size
                glColor3fv(color[:3])
                glVertex3fv(origin)
                glVertex3f(origin[0] + axis[0], origin[1] + axis[1], origin[2] + axis[2])
            
            glEnd()
        
        glLineWidth(1.0)
        glEnable(GL_LIGHTING)
    
    def _draw_sphere(self, position, radius=0.05):
        """Dessine une sphère."""
        glPushMatrix()
        glTranslatef(*position)
        
        quadric = gluNewQuadric()
        gluSphere(quadric, radius, 16, 16)
        gluDeleteQuadric(quadric)
        
        glPopMatrix()
    
    def _draw_cube(self, x, y, z, size=0.1):
        """Dessine un cube."""
        glPushMatrix()
        glTranslatef(x, y, z)
        glScalef(size, size, size)
        
        # Faces du cube
        vertices = [
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
            [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
        ]
        
        faces = [
            [0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4],
            [2, 3, 7, 6], [0, 3, 7, 4], [1, 2, 6, 5]
        ]
        
        glBegin(GL_QUADS)
        for face in faces:
            for vertex in face:
                glVertex3fv(vertices[vertex])
        glEnd()
        
        glPopMatrix()
    
    def _draw_cylinder(self, p1, p2, radius=0.02):
        """Dessine un cylindre entre deux points."""
        
        p1 = np.array(p1)
        p2 = np.array(p2)
        
        direction = p2 - p1
        length = np.linalg.norm(direction)
        
        if length < 1e-6:
            return
        
        direction /= length
        
        # Vecteur up arbitraire
        up = np.array([0, 0, 1])
        if abs(direction[2]) > 0.99:
            up = np.array([1, 0, 0])
        
        # Calcul des axes
        side = np.cross(up, direction)
        side /= np.linalg.norm(side)
        up = np.cross(direction, side)
        
        # Matrice de rotation
        rot_matrix = np.eye(4)
        rot_matrix[:3, 0] = side
        rot_matrix[:3, 1] = up
        rot_matrix[:3, 2] = direction
        rot_matrix[:3, 3] = p1
        
        glPushMatrix()
        glMultMatrixf(rot_matrix.T.flatten())
        
        quadric = gluNewQuadric()
        gluCylinder(quadric, radius, radius, length, 16, 1)
        gluDeleteQuadric(quadric)
        
        glPopMatrix()
    
    # --- Événements souris ---
    
    def _on_mouse_down(self, event):
        """Début du drag."""
        self.mouse_down = True
        self.last_mouse_x = event.x
        self.last_mouse_y = event.y
    
    def _on_mouse_drag(self, event):
        """Rotation avec la souris."""
        if not self.mouse_down:
            return
        
        dx = event.x - self.last_mouse_x
        dy = event.y - self.last_mouse_y
        
        self.camera_azimuth += dx * 0.5
        self.camera_elevation += dy * 0.5
        
        # Limiter l'élévation
        self.camera_elevation = max(-89, min(89, self.camera_elevation))
        
        self.last_mouse_x = event.x
        self.last_mouse_y = event.y
        
        self._render()
    
    def _on_mouse_up(self, event):
        """Fin du drag."""
        self.mouse_down = False
    
    def _on_mouse_wheel(self, event):
        """Zoom avec la molette."""
        if event.delta > 0:
            self.zoom(0.9)
        else:
            self.zoom(1.1)
    
    # --- API publique ---
    
    def plot_robot(self, joint_positions, joint_types=None, frame_transforms=None):
        """
        Affiche le robot.
        
        Parameters
        ----------
        joint_positions : list of np.array
        joint_types : list of str
        frame_transforms : list of np.array (4x4)
        """
        self.robot_data = {
            'positions': joint_positions,
            'joint_types': joint_types or [],
            'transforms': frame_transforms or []
        }
        
        self._render()
    
    def clear(self):
        """Efface le robot."""
        self.robot_data = None
        self._render()
    
    def rotate_view(self, delta_azim=0, delta_elev=0):
        """Rotation programmatique."""
        self.camera_azimuth += delta_azim
        self.camera_elevation += delta_elev
        self.camera_elevation = max(-89, min(89, self.camera_elevation))
        self._render()
    
    def zoom(self, factor=1.1):
        """Zoom."""
        self.camera_distance *= factor
        self.camera_distance = max(0.5, min(10.0, self.camera_distance))
        self._render()
    
    def reset_view(self):
        """Réinitialise la vue."""
        self.camera_distance = 3.0
        self.camera_azimuth = 45.0
        self.camera_elevation = 30.0
        self._render()
    
    def pack(self, **kwargs):
        """Empaqueter le widget."""
        # Déjà fait dans __init__
        pass