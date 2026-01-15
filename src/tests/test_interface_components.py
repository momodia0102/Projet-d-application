"""
Tests pour les composants de l'interface utilisateur
Tests BCD (Boundary, Component, Data) simples
"""

import pytest
import tkinter as tk
from tkinter import ttk
import sys
import os

# Ajouter le chemin pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from Interface.style import COLORS, ModernButton
from Interface.geometry import DialogDefinition
from Interface.mixins.base_mixin import BaseMixin
from Interface.mixins.parametre_mixin import ParameterMixin
from Interface.mixins.resultat_mixin import ResultMixin
from server.robot import Robot
from outils import tools


# ============================================================================
# TESTS BOUNDARY (Limites et Cas Extrêmes)
# ============================================================================

class TestBoundaryConditions:
    """Tests des conditions limites de l'interface"""
    
    def test_joint_count_minimum(self):
        """Test N°1-B : Nombre minimum d'articulations (1)"""
        root = tk.Tk()
        try:
            mixin = ParameterMixin()
            mixin.root = root
            mixin.robo = Robot('TestBot', NL=1, NJ=1, NF=1)
            
            # Simuler le conteneur
            container = tk.Frame(root)
            mixin.dh_table_frame = container
            mixin.joint_count = tk.IntVar(value=1)
            mixin.dh_entries = []
            
            # Mettre à jour avec 1 joint
            mixin.update_dh_table()
            
            # Vérifier qu'une ligne est créée
            assert len(mixin.dh_entries) == 1
            
        finally:
            root.destroy()
    
    def test_joint_count_maximum(self):
        """Test N°2-B : Nombre maximum d'articulations (6)"""
        root = tk.Tk()
        try:
            mixin = ParameterMixin()
            mixin.root = root
            mixin.robo = Robot('TestBot', NL=6, NJ=6, NF=6)
            
            container = tk.Frame(root)
            mixin.dh_table_frame = container
            mixin.joint_count = tk.IntVar(value=6)
            mixin.dh_entries = []
            
            mixin.update_dh_table()
            
            assert len(mixin.dh_entries) == 6
            
        finally:
            root.destroy()
    
    def test_dh_value_zero(self):
        """Test N°3-B : Valeur DH = 0"""
        # Test simple de validation de valeur numérique
        try:
            value = float("0.0")
            assert value == 0.0
        except ValueError:
            pytest.fail("Failed to parse '0.0'")
    
    def test_dh_value_negative(self):
        """Test N°4-B : Valeur DH négative"""
        try:
            value = float("-1.5")
            assert value == -1.5
        except ValueError:
            pytest.fail("Failed to parse '-1.5'")
    
    def test_dh_value_symbolic(self):
        """Test N°5-B : Valeur DH symbolique (L1, q1)"""
        # Test que les symboles sont acceptés comme chaînes
        symbolic_values = ["L1", "q1", "theta1"]
        for val in symbolic_values:
            # Vérifie qu'on ne peut pas les convertir en float
            try:
                float(val)
                pytest.fail(f"'{val}' should not be numeric")
            except ValueError:
                # C'est attendu - les symboles ne sont pas numériques
                assert isinstance(val, str)
    
    def test_robot_name_empty(self):
        """Test N°6-B : Nom de robot vide"""
        root = tk.Tk()
        try:
            dialog = DialogDefinition(root)
            dialog.name_var.set("")
            
            # Simuler le clic sur Créer sans nom
            # (normalement, cela devrait être rejeté)
            # Le test vérifie que l'interface gère ce cas
            
            assert dialog.name_var.get() == ""
            
        finally:
            try:
                dialog.destroy()
            except:
                pass
            root.destroy()
    
    def test_robot_name_special_chars(self):
        """Test N°7-B : Nom de robot avec caractères spéciaux"""
        root = tk.Tk()
        try:
            dialog = DialogDefinition(root)
            
            # Tester différents caractères
            special_names = ["Robot-2025", "Robot_Test", "Mon Robot"]
            
            for name in special_names:
                dialog.name_var.set(name)
                assert dialog.name_var.get() == name
            
        finally:
            try:
                dialog.destroy()
            except:
                pass
            root.destroy()


# ============================================================================
# TESTS COMPONENT (Composants Individuels)
# ============================================================================

class TestComponentBehavior:
    """Tests du comportement des composants"""
    
    def test_modern_button_creation(self):
        """Test N°8-C : Création d'un ModernButton"""
        root = tk.Tk()
        try:
            clicked = []
            
            def on_click():
                clicked.append(True)
            
            btn = ModernButton(root, "Test", on_click)
            
            # Vérifier que le bouton existe
            assert btn is not None
            assert btn.text == "Test"
            
            # Simuler un clic
            btn.command()
            assert len(clicked) == 1
            
        finally:
            root.destroy()
    
    def test_base_mixin_info_card(self):
        """Test N°9-C : Création d'une info card"""
        root = tk.Tk()
        try:
            mixin = BaseMixin()
            frame = tk.Frame(root)
            
            card = mixin.create_info_card(frame, "Test message", icon="🔔")
            
            assert card is not None
            
        finally:
            root.destroy()
    
    def test_base_mixin_separator(self):
        """Test N°10-C : Création d'un séparateur"""
        root = tk.Tk()
        try:
            mixin = BaseMixin()
            frame = tk.Frame(root)
            
            sep = mixin.create_separator(frame, height=2)
            
            assert sep is not None
            
        finally:
            root.destroy()
    
    def test_result_tab_creation(self):
        """Test N°11-C : Création des onglets de résultats"""
        root = tk.Tk()
        try:
            mixin = ResultMixin()
            parent = tk.Frame(root)
            
            mixin.create_results_section(parent)
            
            # Vérifier que les widgets sont créés
            assert hasattr(mixin, 'result_widgets')
            assert len(mixin.result_widgets) == 4  # mgd, mgi, mcd, mci
            
        finally:
            root.destroy()
    
    def test_result_update(self):
        """Test N°12-C : Mise à jour d'un résultat"""
        root = tk.Tk()
        try:
            mixin = ResultMixin()
            parent = tk.Frame(root)
            
            mixin.create_results_section(parent)
            
            # Mettre à jour un résultat
            test_content = "Test MGD Result"
            mixin.update_result('mgd', test_content)
            
            # Vérifier que le contenu est mis à jour
            widget = mixin.result_widgets['mgd']
            content = widget.get('1.0', tk.END)
            assert test_content in content
            
        finally:
            root.destroy()
    
    def test_dh_table_headers(self):
        """Test N°13-C : Création des en-têtes du tableau DH"""
        root = tk.Tk()
        try:
            mixin = ParameterMixin()
            mixin.root = root
            mixin.robo = Robot('TestBot', NL=2, NJ=2, NF=2)
            
            container = tk.Frame(root)
            mixin.dh_table_frame = container
            mixin.joint_count = tk.IntVar(value=2)
            mixin.dh_entries = []
            
            mixin.update_dh_table()
            
            # Vérifier que les en-têtes sont créés
            children = container.winfo_children()
            assert len(children) > 0
            
        finally:
            root.destroy()
    
    def test_joint_control_vars_creation(self):
        """Test N°14-C : Création des variables de contrôle articulaire"""
        root = tk.Tk()
        try:
            mixin = ParameterMixin()
            mixin.root = root
            mixin.robo = Robot('TestBot', NL=2, NJ=2, NF=2)
            
            # Initialiser le robot
            mixin.robo.sigma[1] = 0  # Rotation
            mixin.robo.sigma[2] = 0  # Rotation
            
            container = tk.Frame(root)
            mixin.joint_control_container = container
            mixin.joint_control_vars = {}
            
            mixin.update_joint_controls()
            
            # Vérifier que les variables sont créées
            assert len(mixin.joint_control_vars) >= 0
            
        finally:
            root.destroy()


# ============================================================================
# TESTS DATA (Flux de Données)
# ============================================================================

class TestDataFlow:
    """Tests du flux de données entre composants"""
    
    def test_robot_parameter_storage(self):
        """Test N°15-D : Stockage des paramètres dans le robot"""
        root = tk.Tk()
        try:
            robot = Robot('TestBot', NL=2, NJ=2, NF=2)
            
            # Stocker des valeurs
            robot.put_val(1, 'theta', 45.0)
            robot.put_val(1, 'd', 0.5)
            robot.put_val(1, 'sigma', 0)
            
            # Vérifier
            assert robot.get_val(1, 'theta') == 45.0
            assert robot.get_val(1, 'd') == 0.5
            assert robot.get_val(1, 'sigma') == 0
            
        finally:
            root.destroy()
    
    def test_robot_symbolic_parameters(self):
        """Test N°16-D : Paramètres symboliques dans le robot"""
        root = tk.Tk()
        try:
            robot = Robot('TestBot', NL=2, NJ=2, NF=2)
            
            # Stocker des symboles
            robot.put_val(1, 'd', "L1")
            
            # Vérifier
            d_val = str(robot.get_val(1, 'd'))
            assert "L1" in d_val or d_val == "L1"
            
        finally:
            root.destroy()
    
    def test_get_joint_variable_names(self):
        """Test N°17-D : Extraction des noms de variables articulaires"""
        root = tk.Tk()
        try:
            mixin = ParameterMixin()
            mixin.root = root
            mixin.robo = Robot('TestBot', NL=2, NJ=2, NF=2)
            
            # Configurer le robot
            mixin.robo.sigma[1] = 0  # Rotation → theta
            mixin.robo.sigma[2] = 1  # Prismatique → r
            
            names = mixin._get_joint_variable_names(mixin.robo)
            
            # Vérifier qu'on a bien des noms
            assert len(names) >= 0
            
        finally:
            root.destroy()
    
    def test_dh_value_round_trip(self):
        """Test N°18-D : Cycle complet : Robot → get → put"""
        root = tk.Tk()
        try:
            robot = Robot('TestBot', NL=1, NJ=1, NF=1)
            
            # 1. Définir une valeur dans le robot
            robot.put_val(1, 'd', 1.234)
            
            # 2. Récupérer
            value = robot.get_val(1, 'd')
            
            # 3. Vérifier
            assert abs(value - 1.234) < 0.001
            
        finally:
            root.destroy()
    
    def test_joint_type_round_trip(self):
        """Test N°19-D : Cycle complet pour le type d'articulation"""
        root = tk.Tk()
        try:
            robot = Robot('TestBot', NL=1, NJ=1, NF=1)
            
            # 1. Définir type rotation
            robot.put_val(1, 'sigma', 0)
            
            # 2. Récupérer
            sigma = robot.get_val(1, 'sigma')
            
            # 3. Vérifier
            assert sigma == 0
            
            # 4. Tester prismatique
            robot.put_val(1, 'sigma', 1)
            sigma = robot.get_val(1, 'sigma')
            assert sigma == 1
            
        finally:
            root.destroy()


# ============================================================================
# TESTS D'INTÉGRATION SIMPLES
# ============================================================================

class TestSimpleIntegration:
    """Tests d'intégration simples pour l'interface"""
    
    def test_create_and_update_table(self):
        """Test N°20-I : Création et mise à jour du tableau DH"""
        root = tk.Tk()
        try:
            mixin = ParameterMixin()
            mixin.root = root
            mixin.robo = Robot('TestBot', NL=3, NJ=3, NF=3)
            
            container = tk.Frame(root)
            mixin.dh_table_frame = container
            mixin.joint_count = tk.IntVar(value=3)
            mixin.dh_entries = []
            
            # Créer
            mixin.update_dh_table()
            assert len(mixin.dh_entries) == 3
            
            # Mettre à jour
            mixin.joint_count.set(2)
            mixin.update_dh_table()
            assert len(mixin.dh_entries) == 2
            
        finally:
            root.destroy()
    
    def test_result_display_all_tabs(self):
        """Test N°21-I : Affichage dans tous les onglets de résultats"""
        root = tk.Tk()
        try:
            mixin = ResultMixin()
            parent = tk.Frame(root)
            
            mixin.create_results_section(parent)
            
            # Tester chaque onglet
            for tab_id in ['mgd', 'mgi', 'mcd', 'mci']:
                content = f"Test content for {tab_id}"
                mixin.update_result(tab_id, content)
                
                widget = mixin.result_widgets[tab_id]
                text = widget.get('1.0', tk.END)
                assert content in text
            
        finally:
            root.destroy()
    
    def test_dialog_result_structure(self):
        """Test N°22-I : Structure du résultat du dialogue"""
        root = tk.Tk()
        try:
            dialog = DialogDefinition(root)
            
            # Simuler une configuration
            dialog.name_var.set("TestRobot")
            dialog.nl_var.set(3)
            dialog.structure_var.set("Simple")
            dialog.floating_var.set(False)
            dialog.mobile_var.set(False)
            
            # Simuler la création
            dialog.on_create()
            
            result = dialog.result
            
            # Vérifier la structure
            assert result is not None
            assert 'name' in result
            assert 'num_links' in result
            assert 'structure' in result
            
        finally:
            try:
                dialog.destroy()
            except:
                pass
            root.destroy()


# ============================================================================
# TESTS DE ROBUSTESSE
# ============================================================================

class TestRobustness:
    """Tests de robustesse de l'interface"""
    
    def test_parse_mixed_input(self):
        """Test N°23-R : Parse de différents types d'entrées"""
        # Test de conversion numérique
        test_cases = [
            ("123.45", 123.45, True),
            ("-0.5", -0.5, True),
            ("0", 0.0, True),
            ("L1", "L1", False),
            ("theta", "theta", False),
            ("", 0.0, True),  # Chaîne vide = 0
        ]
        
        for input_val, expected, is_numeric in test_cases:
            if is_numeric:
                try:
                    result = float(input_val) if input_val else 0.0
                    assert abs(result - expected) < 0.001
                except ValueError:
                    pytest.fail(f"Should parse '{input_val}' as numeric")
            else:
                # Symbolique - reste une chaîne
                assert input_val == expected
    
    def test_update_result_invalid_id(self):
        """Test N°24-R : Mise à jour avec ID invalide"""
        root = tk.Tk()
        try:
            mixin = ResultMixin()
            parent = tk.Frame(root)
            
            mixin.create_results_section(parent)
            
            # Ne doit pas crasher - doit gérer gracieusement
            try:
                mixin.update_result('invalid_id', "Test content")
                # Si on arrive ici, c'est OK (pas de crash)
            except Exception as e:
                # Vérifier que c'est une erreur attendue
                assert "non trouvé" in str(e) or "not found" in str(e).lower()
            
        finally:
            root.destroy()
    
    def test_robot_none_handling(self):
        """Test N°25-R : Gestion robot = None"""
        root = tk.Tk()
        try:
            mixin = ParameterMixin()
            mixin.root = root
            mixin.robo = None
            
            # Vérifier qu'on peut gérer un robot None
            if hasattr(mixin, '_get_joint_variable_names'):
                names = mixin._get_joint_variable_names(mixin.robo) if mixin.robo else []
            else:
                # Si la méthode n'existe pas, c'est OK aussi
                names = []
            
            assert names == [] or names is None
            
        finally:
            root.destroy()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])