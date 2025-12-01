# symoro_bridge.py

import numpy as np
from sympy import lambdify, Matrix, N as sympy_N # Utilisation de N pour l'évaluation numérique
import sys
import os

# Assurez-vous que le chemin vers le dossier 'server' (où se trouve robot.py) est inclus
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class SYMOROBridge:
    """
    Classe de pont pour convertir les résultats symboliques SYMORO
    en données numériques pour la visualisation
    """
    
    @staticmethod
    def extract_transformation_matrices(symo):
        """
        Extrait les matrices de transformation symboliques T0Tn du SymbolManager.
        
        Parameters
        ----------
        symo : symbolmgr.SymbolManager
            Résultat du calcul MGD (contient symo.sydi)
            
        Returns
        -------
        T_matrices : dict
            Dictionnaire {frame_idx: Matrix_symbolique}
        """
        T_matrices = {}
        
        # Le SymbolManager stocke les substitutions, y compris les matrices T0Tn
        for symbol, expression in symo.sydi.items():
            symbol_str = str(symbol)
            
            # On cherche les symboles de la forme T0T[n]
            if symbol_str.startswith('T0T'):
                try:
                    # T0T1 -> 1, T0T2 -> 2, etc.
                    frame_idx = int(symbol_str[3:]) 
                    
                    if isinstance(expression, Matrix) and expression.shape == (4, 4):
                        T_matrices[frame_idx] = expression
                except ValueError:
                    continue
        
        return T_matrices
    
    @staticmethod
    def compute_joint_positions_from_symoro(symo, robot, joint_values=None):
        """
        Calcule les positions 3D des joints à partir des résultats SYMORO
        
        Parameters
        ----------
        symo : symbolmgr.SymbolManager
        robot : server.robot.Robot
        joint_values : dict, optional
            Valeurs des variables articulaires {var_symbol: value_radians}
            
        Returns
        -------
        positions : list of np.array, joint_types : list of str, frame_transforms : list of np.array
        """
        # Étape 1: Extraire les matrices symboliques
        T_matrices = SYMOROBridge.extract_transformation_matrices(symo)
        
        if not T_matrices:
            return None, None, None
        
        # Étape 2: Préparer les valeurs articulaires (Configuration Repos si non spécifié)
        if joint_values is None:
            joint_values = {}
            for j in range(1, robot.NJ):
                if robot.sigma[j] == 0:
                    joint_values[robot.theta[j]] = 0.0
                elif robot.sigma[j] == 1:
                    joint_values[robot.r[j]] = 0.0
        
        # Étape 3: Évaluer numériquement chaque matrice
        positions = [np.array([0.0, 0.0, 0.0])]  # Base à l'origine (Frame 0)
        joint_types = []
        frame_transforms = [np.eye(4)]
        
        # Trier les frames par index pour s'assurer de l'ordre T0T1, T0T2...
        sorted_frames = sorted(T_matrices.keys())
        
        for frame_idx in sorted_frames:
            T_sym = T_matrices[frame_idx]
            
            # Substituer les valeurs dans la matrice symbolique
            # Utilisation de sympy_N pour l'évaluation numérique
            T_num_sym = T_sym.subs(joint_values)
            
            # Convertir en tableau NumPy (important d'utiliser .tolist())
            T_num = np.array(T_num_sym.tolist(), dtype=float)
            
            # Extraire la position (dernière colonne, lignes 0, 1, 2)
            position = T_num[:3, 3]
            positions.append(position)
            frame_transforms.append(T_num)
            
            # Type de joint (frame_idx correspond à l'index du joint)
            if frame_idx < robot.NF:
                jtype = 'R' if robot.sigma[frame_idx] == 0 else 'P'
                joint_types.append(jtype)
        
        # joint_types doit avoir NL-1 éléments. S'assurer de la cohérence.
        return positions, joint_types, frame_transforms

    @staticmethod
    def get_joint_variable_names(robot):
        """Retourne les noms des variables articulaires (th1, r2, etc.)"""
        var_names = []
        for j in range(1, robot.NJ):
            if robot.sigma[j] == 0 or robot.sigma[j] == 1:
                var_names.append(str(robot.get_q(j)))
        return var_names