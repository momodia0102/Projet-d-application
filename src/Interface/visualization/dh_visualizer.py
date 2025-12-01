# dh_visualizer.py

import numpy as np
from .symoro_bridge import SYMOROBridge


class DHVisualizer:
    """
    Visualiseur qui prépare les données d'entrée pour le Pont SYMORO.
    """
    
# dh_visualizer.py: Méthode from_symoro_results

    @staticmethod
    def from_symoro_results(symo, robot, joint_angles_deg=None):
        """
        Prépare et lance le calcul des positions 3D à partir des résultats MGD SYMORO.
        """
        
        # ✅ CORRECTION: S'assurer que joint_angles_deg est un dictionnaire
        if joint_angles_deg is None:
            joint_angles_deg = {}
            
        # --- Conversion des angles en radians et préparation du dictionnaire de substitution ---
        joint_values = {}
        
        # Parcourir tous les joints du robot
        for j in range(1, robot.NJ):
            var = robot.get_q(j) # Symbole articulaire
            var_name = str(var)  # Nom du symbole (ex: 'th1', 'r2')

            # La vérification est maintenant sécurisée
            if var_name in joint_angles_deg: 
                value = joint_angles_deg[var_name]
                
                if robot.sigma[j] == 0: # Joint Rotatif (theta, alpha, gamma)
                    # Convertir les degrés en radians
                    joint_values[var] = np.deg2rad(value)
                elif robot.sigma[j] == 1: # Joint Prismatique (d, r, b)
                    # La valeur est déjà en mètres
                    joint_values[var] = value
                
        # --- Appel du pont ---
        return SYMOROBridge.compute_joint_positions_from_symoro(
            symo, robot, joint_values
        )