# primitives.py
import numpy as np
from numpy import sin, cos, pi

class Primitives:
    """Générateur de géométries 3D pour OpenGL"""

    @staticmethod
    def create_cylinder(radius, length, n_segments=16, centered=True):
        """ Crée un cylindre. """
        vertices, indices, normals = [], [], []
        z_start = -length / 2.0 if centered else 0.0

        # Corps du cylindre
        for i in range(n_segments):
            angle = 2 * pi * i / n_segments
            x_n, y_n = cos(angle), sin(angle)
            x, y = radius * x_n, radius * y_n

            vertices.extend([x, y, z_start, x, y, z_start + length])
            normals.extend([x_n, y_n, 0, x_n, y_n, 0])

        num_vertices = 2 * n_segments
        for i in range(num_vertices):
            indices.extend([i, (i + 1) % num_vertices, (i + 2) % num_vertices])

        return np.array(vertices, dtype=np.float32), \
               np.array(indices, dtype=np.uint32), \
               np.array(normals, dtype=np.float32)

    @staticmethod
    def create_sphere(radius, n_lat=16, n_long=16):
        """ Crée une sphère avec des triangles. """
        vertices, indices, normals = [], [], []
        
        for lat in range(n_lat + 1):
            theta = lat * pi / n_lat
            sin_theta = sin(theta)
            cos_theta = cos(theta)
            
            for long in range(n_long + 1):
                phi = long * 2 * pi / n_long
                sin_phi = sin(phi)
                cos_phi = cos(phi)
                
                x = cos_phi * sin_theta
                y = sin_phi * sin_theta
                z = cos_theta
                
                vertices.extend([radius * x, radius * y, radius * z])
                normals.extend([x, y, z])
                
        for lat in range(n_lat):
            for long in range(n_long):
                first = lat * (n_long + 1) + long
                second = first + n_long + 1
                
                indices.extend([first, second, first + 1])
                indices.extend([second, second + 1, first + 1])
        
        return np.array(vertices, dtype=np.float32), \
               np.array(indices, dtype=np.uint32), \
               np.array(normals, dtype=np.float32)

    @staticmethod
    def create_box(width, height, depth):
        """ Crée une boîte. """
        half_w, half_h, half_d = width/2, height/2, depth/2
        
        vertices = [
            # Face avant
            [-half_w, -half_h,  half_d], [ half_w, -half_h,  half_d],
            [ half_w,  half_h,  half_d], [-half_w,  half_h,  half_d],
            # Face arrière
            [-half_w, -half_h, -half_d], [-half_w,  half_h, -half_d],
            [ half_w,  half_h, -half_d], [ half_w, -half_h, -half_d],
        ]
        
        indices = [
            # Face avant
            0, 1, 2, 2, 3, 0,
            # Face arrière
            4, 5, 6, 6, 7, 4,
            # Face gauche
            0, 3, 5, 5, 4, 0,
            # Face droite
            1, 7, 6, 6, 2, 1,
            # Face supérieure
            3, 2, 6, 6, 5, 3,
            # Face inférieure
            0, 4, 7, 7, 1, 0
        ]
        
        normals = [
            [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1],  # Avant
            [0, 0, -1], [0, 0, -1], [0, 0, -1], [0, 0, -1], # Arrière
            [-1, 0, 0], [-1, 0, 0], [-1, 0, 0], [-1, 0, 0], # Gauche
            [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0],    # Droite
            [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0],    # Haut
            [0, -1, 0], [0, -1, 0], [0, -1, 0], [0, -1, 0] # Bas
        ]
        
        # Aplatir les listes
        vertices_flat = [coord for vertex in vertices for coord in vertex]
        normals_flat = [coord for normal in normals for coord in normal]
        
        return np.array(vertices_flat, dtype=np.float32), \
               np.array(indices, dtype=np.uint32), \
               np.array(normals_flat, dtype=np.float32)