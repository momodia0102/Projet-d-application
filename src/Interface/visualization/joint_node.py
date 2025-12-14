# joint_node.py

import numpy as np
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from sympy import Expr

try:
    from OpenGL.GLUT import glutSolidCube, glutSolidSphere
    HAS_GLUT = True
except ImportError:
    HAS_GLUT = False
    print("⚠️ GLUT non disponible - géométries simplifiées")

from .primitives import Primitives

# Couleurs pour le rendu direct
COLORS_ROBOT = {
    'link': (0.2, 0.4, 0.8, 1.0),
    'revolute': (0.8, 0.2, 0.2, 1.0), 
    'prismatic': (0.2, 0.8, 0.2, 1.0),
    'frame_x': (1.0, 0.0, 0.0, 1.0),
    'frame_y': (0.0, 1.0, 0.0, 1.0),
    'frame_z': (0.0, 0.0, 1.0, 1.0),
}


class JointNode:
    """
    Nœud dans la hiérarchie du robot. Modélise un joint/frame
    et applique ses transformations DH.
    """
    # ... (le reste reste identique jusqu'à _draw_joint_geometry) ...
    def __init__(self, index, parent=None,
                 theta=0, r=0, alpha=0, d=0, gamma=0, b=0,
                 sigma=0, length_scale=0.1):

        self.index = index
        self.parent = parent
        self.children = []

        # Paramètres DH
        self.theta = theta
        self.r_base = r
        self.alpha = alpha
        self.d = d
        self.gamma = gamma
        self.b = b
        self.sigma = sigma  # 0 = rotation, 1 = prisme, 2 = base fixe

        # Valeur articulaire courante
        self.q = 0.0

        # Échelle locale
        self.length_scale = length_scale

        # Si un parent existe, on le rattache
        if parent is not None:
            parent.children.append(self)

    def init_geometry(self, length_scale):
        """Initialise l’échelle locale."""
        self.length_scale = length_scale

    def set_q(self, value):
        """Met à jour la valeur articulée."""
        self.q = value

    def _get_numeric_value(self, v):
        """Convertit sympy/str en float si possible."""
        try:
            return float(v)
        except Exception:
            return 0.0

    def draw_recursive(self):
        """Dessine ce nœud + ses enfants."""
        print(f"[draw] Joint idx={self.index} sigma={self.sigma} q={self.q}")
        glPushMatrix()

        # Transformation DH
        self._apply_transform()

        # Géométrie du joint
        self._draw_joint_geometry()

        # Récursion
        for child in self.children:
            child.draw_recursive()

        glPopMatrix()

    def _apply_transform(self):
        """Transformation DH simplifiée."""
        theta = self.theta
        d = self.d
        r = self.r_base
        alpha = self.alpha

        # Articulation dépendante du type
        if self.sigma == 0:  # Rotation
            theta += self.q
        elif self.sigma == 1:  # Prisme
            d += self.q

        # Transformation DH standard
        glRotatef(np.degrees(theta), 0, 0, 1)
        glTranslatef(r, 0, d)
        glRotatef(np.degrees(alpha), 1, 0, 0)

    
    def _draw_joint_geometry(self):
        """Dessine la géométrie du joint (sphère/cube)."""
        glPushMatrix()

        # Pour debug local : dessiner un petit repère si tu veux
        # glDisable(GL_LIGHTING)
        # glBegin(GL_LINES)
        # glColor3f(1,0,0); glVertex3f(0,0,0); glVertex3f(0.1,0,0)
        # glColor3f(0,1,0); glVertex3f(0,0,0); glVertex3f(0,0.1,0)
        # glColor3f(0,0,1); glVertex3f(0,0,0); glVertex3f(0,0,0.1)
        # glEnd()
        # glEnable(GL_LIGHTING)

        glColor4f(1.0, 1.0, 0.0, 1.0) # Jaune vif
        self._draw_simple_cube_with_normals(1.0)

        if self.sigma == 0:  # Rotation
            # utiliser couleur RGBA
            glColor4f(*COLORS_ROBOT['revolute'])
            # utiliser GLU quadric avec normales
            quadric = gluNewQuadric()
            gluQuadricNormals(quadric, GLU_SMOOTH)
            gluQuadricDrawStyle(quadric, GLU_FILL)
            gluSphere(quadric, self.length_scale / 6.0, 24, 24)
            gluDeleteQuadric(quadric)

        elif self.sigma == 1:  # Prismatique
            glColor4f(*COLORS_ROBOT['prismatic'])
            # Dessiner cube simple : pour l'éclairage, on fournit des normales manuelles
            self._draw_simple_cube_with_normals(self.length_scale / 4.0)

        elif self.sigma == 2:  # Fixe (Base)
            glColor4f(0.3, 0.3, 0.3, 1.0)
            quadric = gluNewQuadric()
            gluQuadricNormals(quadric, GLU_SMOOTH)
            gluQuadricDrawStyle(quadric, GLU_FILL)
            gluSphere(quadric, self.length_scale / 4.0, 24, 24)
            gluDeleteQuadric(quadric)

        glPopMatrix()

    def _draw_simple_cube(self, size):
        """Dessine un cube simple sans GLUT."""
        half = size / 2.0
        
        glBegin(GL_QUADS)
        # Face avant
        glVertex3f(-half, -half, half)
        glVertex3f(half, -half, half)
        glVertex3f(half, half, half)
        glVertex3f(-half, half, half)
        
        # Face arrière
        glVertex3f(-half, -half, -half)
        glVertex3f(-half, half, -half)
        glVertex3f(half, half, -half)
        glVertex3f(half, -half, -half)
        
        # Face gauche
        glVertex3f(-half, -half, -half)
        glVertex3f(-half, -half, half)
        glVertex3f(-half, half, half)
        glVertex3f(-half, half, -half)
        
        # Face droite
        glVertex3f(half, -half, -half)
        glVertex3f(half, half, -half)
        glVertex3f(half, half, half)
        glVertex3f(half, -half, half)
        
        # Face supérieure
        glVertex3f(-half, half, -half)
        glVertex3f(-half, half, half)
        glVertex3f(half, half, half)
        glVertex3f(half, half, -half)
        
        # Face inférieure
        glVertex3f(-half, -half, -half)
        glVertex3f(half, -half, -half)
        glVertex3f(half, -half, half)
        glVertex3f(-half, -half, half)
        glEnd()
    
    # ... (le reste du fichier reste identique) ...

    def _draw_simple_cube_with_normals(self, size):
        """Cube avec normales par face pour que l'éclairage fonctionne."""
        half = size / 2.0

        glBegin(GL_QUADS)
        # face avant (z positive)
        glNormal3f(0, 0, 1)
        glVertex3f(-half, -half, half)
        glVertex3f(half, -half, half)
        glVertex3f(half, half, half)
        glVertex3f(-half, half, half)

        # face arrière (z negative)
        glNormal3f(0, 0, -1)
        glVertex3f(-half, -half, -half)
        glVertex3f(-half, half, -half)
        glVertex3f(half, half, -half)
        glVertex3f(half, -half, -half)

        # face gauche (x negative)
        glNormal3f(-1, 0, 0)
        glVertex3f(-half, -half, -half)
        glVertex3f(-half, -half, half)
        glVertex3f(-half, half, half)
        glVertex3f(-half, half, -half)

        # face droite (x positive)
        glNormal3f(1, 0, 0)
        glVertex3f(half, -half, -half)
        glVertex3f(half, half, -half)
        glVertex3f(half, half, half)
        glVertex3f(half, -half, half)

        # face supérieure (y positive)
        glNormal3f(0, 1, 0)
        glVertex3f(-half, half, -half)
        glVertex3f(-half, half, half)
        glVertex3f(half, half, half)
        glVertex3f(half, half, -half)

        # face inférieure (y negative)
        glNormal3f(0, -1, 0)
        glVertex3f(-half, -half, -half)
        glVertex3f(half, -half, -half)
        glVertex3f(half, -half, half)
        glVertex3f(-half, -half, half)
        glEnd()
