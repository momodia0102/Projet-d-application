# -*- coding: utf-8 -*-
"""
Contrôleur Robot - Pont entre l'interface et le serveur
Gère la conversion des paramètres et l'appel aux fonctions de calcul
"""

import sys
import os
from sympy import pi, var, sympify

# Ajouter les chemins nécessaires
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.robot import Robot
from server.geometry import direct_geometric_fast
from outils import symbolmgr
from outils import tools


class RobotController:
    """
    Contrôleur principal pour gérer les interactions entre
    l'interface graphique et les calculs du serveur
    """
    
    def __init__(self):
        self.robot = None
        self.last_dh_params = None
        
    def create_robot_from_dh_params(self, dh_params):
        """
        Crée une instance Robot à partir des paramètres DH de l'interface
        
        Parameters
        ----------
        dh_params : list of dict
            Liste des paramètres DH pour chaque articulation
            Format: [{'theta': float, 'd': float, 'a': float, 
                     'alpha': float, 'type': 'R' or 'P'}, ...]
        
        Returns
        -------
        Robot
            Instance du robot configuré
        """
        n_joints = len(dh_params)
        
        # Créer l'instance Robot
        robot = Robot(
            name='CustomRobot',
            NL=n_joints,      # Nombre de liens
            NJ=n_joints,      # Nombre de joints
            NF=n_joints,      # Nombre de frames
            is_floating=False,
            structure=tools.SIMPLE
        )
        
        # Configurer les paramètres géométriques
        # Frame 0 = base (toujours à zéro)
        for i in range(1, n_joints + 1):
            params = dh_params[i - 1]
            
            # Type d'articulation (0=rotation, 1=prismatique, 2=fixe)
            robot.sigma[i] = 0 if params['type'] == 'R' else 1
            
            # Antécédent (chaîne simple: i-1)
            robot.ant[i] = i - 1
            
            # Articulation motorisée
            robot.mu[i] = 1
            
            # Paramètres DH (conversion degrés -> radians pour angles)
            robot.gamma[i] = 0  # Paramètre gamma (DH modifié)
            robot.b[i] = 0      # Paramètre b (DH modifié)
            
            # Paramètres DH standard
            robot.alpha[i] = sympify(params['alpha'] * pi / 180)
            robot.d[i] = sympify(params['d'])
            
            if params['type'] == 'R':
                # Articulation en rotation: theta est variable
                robot.theta[i] = var(f'th{i}')
                robot.r[i] = sympify(params['a'])
            else:
                # Articulation prismatique: d est variable
                robot.theta[i] = sympify(params['theta'] * pi / 180)
                robot.r[i] = var(f'r{i}')
        
        self.robot = robot
        self.last_dh_params = dh_params
        return robot
    
    def calculate_mgd(self, dh_params, joint_values=None, from_frame=0, to_frame=None):
        """
        Calcule le Modèle Géométrique Direct
        
        Parameters
        ----------
        dh_params : list of dict
            Paramètres DH
        joint_values : dict, optional
            Valeurs des variables articulaires {var_name: value}
            Ex: {'th1': 0, 'th2': 90, 'th3': -45}
        from_frame : int
            Frame de départ (0 = base)
        to_frame : int, optional
            Frame d'arrivée (None = effecteur final)
        
        Returns
        -------
        dict
            Résultats du MGD avec:
            - 'symo': SymbolManager avec toutes les équations
            - 'matrix': Matrice de transformation finale (si évaluée)
            - 'success': bool
            - 'message': str
            - 'equations': str (représentation textuelle)
        """
        try:
            # Créer le robot si nécessaire
            if self.robot is None or self.last_dh_params != dh_params:
                self.create_robot_from_dh_params(dh_params)
            
            # Frame de destination par défaut = effecteur
            if to_frame is None:
                to_frame = len(dh_params)
            
            # Calculer le MGD
            symo = direct_geometric_fast(self.robot, to_frame, from_frame)
            
            # Extraire les équations
            equations_text = self._format_equations(symo)
            
            # Évaluer numériquement si des valeurs sont fournies
            matrix_numeric = None
            if joint_values:
                matrix_numeric = self._evaluate_transformation(
                    symo, joint_values
                )
            
            return {
                'success': True,
                'symo': symo,
                'matrix': matrix_numeric,
                'equations': equations_text,
                'message': f'MGD calculé avec succès (frame {from_frame} → {to_frame})'
            }
            
        except Exception as e:
            return {
                'success': False,
                'symo': None,
                'matrix': None,
                'equations': '',
                'message': f'Erreur lors du calcul MGD: {str(e)}'
            }
    
    def _format_equations(self, symo):
        """
        Formate les équations du SymbolManager pour affichage
        
        Parameters
        ----------
        symo : SymbolManager
            Instance contenant les équations
        
        Returns
        -------
        str
            Représentation textuelle formatée
        """
        equations = []
        equations.append("=" * 60)
        equations.append("MODÈLE GÉOMÉTRIQUE DIRECT")
        equations.append("=" * 60)
        equations.append("")
        
        # Substitutions trigonométriques
        if symo.sydi:
            equations.append("📐 SUBSTITUTIONS TRIGONOMÉTRIQUES:")
            equations.append("-" * 60)
            for symbol, expression in symo.sydi.items():
                # Éviter les expressions trop complexes dans l'affichage
                expr_str = str(expression)
                if len(expr_str) > 50:
                    expr_str = expr_str[:47] + "..."
                equations.append(f"  {symbol} = {expr_str}")
            equations.append("")
        
        # Matrice de transformation finale
        equations.append("🎯 MATRICE DE TRANSFORMATION FINALE:")
        equations.append("-" * 60)
        
        # Chercher la matrice T dans les symboles
        t_matrices = [s for s in symo.sydi.keys() if str(s).startswith('T')]
        if t_matrices:
            # Prendre la dernière matrice calculée
            final_t = max(t_matrices, key=lambda x: str(x))
            equations.append(f"  Matrice: {final_t}")
            equations.append("")
            
            # Composantes de la matrice
            equations.append("  Structure 4x4:")
            equations.append("  ┌─────────────────────────────────┐")
            equations.append("  │  R₁₁  R₁₂  R₁₃  │  Pₓ           │")
            equations.append("  │  R₂₁  R₂₂  R₂₃  │  Pᵧ           │")
            equations.append("  │  R₃₁  R₃₂  R₃₃  │  Pz           │")
            equations.append("  │   0    0    0   │   1           │")
            equations.append("  └─────────────────────────────────┘")
        else:
            equations.append("  (Voir fichier .fgm pour les détails)")
        
        equations.append("")
        equations.append("💡 Pour évaluer numériquement:")
        equations.append("   Fournissez les valeurs des variables articulaires")
        equations.append("=" * 60)
        
        return "\n".join(equations)
    
    def _evaluate_transformation(self, symo, joint_values):
        """
        Évalue numériquement la matrice de transformation
        
        Parameters
        ----------
        symo : SymbolManager
            Contient les équations symboliques
        joint_values : dict
            Valeurs des variables {var_name: value}
        
        Returns
        -------
        Matrix or None
            Matrice évaluée numériquement
        """
        try:
            # Chercher la matrice T finale dans sydi
            t_matrices = [s for s in symo.sydi.keys() if str(s).startswith('T')]
            if not t_matrices:
                return None
            
            final_t_sym = max(t_matrices, key=lambda x: str(x))
            final_t_expr = symo.sydi[final_t_sym]
            
            # Substituer les valeurs
            # Convertir les angles en radians si nécessaire
            subs_dict = {}
            for var_name, value in joint_values.items():
                var_symbol = var(var_name)
                # Si c'est un angle (theta), convertir en radians
                if 'th' in var_name:
                    subs_dict[var_symbol] = value * pi / 180
                else:
                    subs_dict[var_symbol] = value
            
            # Évaluer
            from sympy import N
            matrix_numeric = final_t_expr.subs(subs_dict)
            matrix_numeric = N(matrix_numeric, 4)  # 4 décimales
            
            return matrix_numeric
            
        except Exception as e:
            print(f"Erreur évaluation numérique: {e}")
            return None
    
    def get_joint_variables(self):
        """
        Retourne la liste des variables articulaires du robot
        
        Returns
        -------
        list
            Liste des noms de variables ['th1', 'th2', ...]
        """
        if self.robot is None:
            return []
        
        variables = []
        for i in range(1, self.robot.NJ + 1):
            if self.robot.sigma[i] == 0:
                variables.append(f'th{i}')
            elif self.robot.sigma[i] == 1:
                variables.append(f'r{i}')
        
        return variables
    
    def get_robot_info(self):
        """
        Retourne les informations sur le robot actuel
        
        Returns
        -------
        dict
            Informations sur le robot
        """
        if self.robot is None:
            return {
                'exists': False,
                'message': 'Aucun robot configuré'
            }
        
        return {
            'exists': True,
            'name': self.robot.name,
            'n_joints': self.robot.NJ - 1,
            'n_links': self.robot.NL - 1,
            'structure': self.robot.structure,
            'joint_types': [
                'R' if self.robot.sigma[i] == 0 else 'P'
                for i in range(1, self.robot.NJ + 1)
            ],
            'variables': self.get_joint_variables()
        }


# Fonction helper pour tests
def test_controller():
    """Fonction de test du contrôleur"""
    # Paramètres DH pour un robot 3R simple
    dh_params = [
        {'theta': 0, 'd': 0, 'a': 1, 'alpha': 0, 'type': 'R'},
        {'theta': 0, 'd': 0, 'a': 1, 'alpha': 0, 'type': 'R'},
        {'theta': 0, 'd': 0, 'a': 0.5, 'alpha': 0, 'type': 'R'}
    ]
    
    controller = RobotController()
    
    # Test création robot
    print("Test 1: Création du robot")
    robot = controller.create_robot_from_dh_params(dh_params)
    print(f"✓ Robot créé: {robot.name}, {robot.NJ-1} articulations")
    
    # Test info robot
    print("\nTest 2: Informations robot")
    info = controller.get_robot_info()
    print(f"✓ Type articulations: {info['joint_types']}")
    print(f"✓ Variables: {info['variables']}")
    
    # Test MGD
    print("\nTest 3: Calcul MGD")
    result = controller.calculate_mgd(dh_params)
    if result['success']:
        print("✓ MGD calculé avec succès")
        print(result['equations'])
    else:
        print(f"✗ Erreur: {result['message']}")


if __name__ == "__main__":
    test_controller()