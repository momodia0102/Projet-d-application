# visualization_mixin.py (VERSION SCRIPT PYTHON)

import tkinter as tk
from tkinter import messagebox, filedialog
import os
from Interface.style import COLORS, ModernButton
from .base_mixin import BaseMixin


class VisualizationMixin(BaseMixin):
    """Mixin pour la visualisation via script Python généré"""
    
    def create_visualization_section(self, parent):
        """Section d'information sur la visualisation via script Python."""
        
        # Conteneur principal avec fond dégradé
        viz_container = tk.Frame(parent, bg=COLORS['bg_white'])
        viz_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Zone d'information centrale
        info_frame = tk.Frame(viz_container, bg=COLORS['bg_light'], relief=tk.FLAT, bd=2)
        info_frame.place(relx=0.5, rely=0.5, anchor='center', width=500, height=400)
        
        # Icône et titre
        tk.Label(
            info_frame,
            text="🎨",
            font=('Arial', 48),
            bg=COLORS['bg_light'],
            fg=COLORS['primary']
        ).pack(pady=(30, 10))
        
        tk.Label(
            info_frame,
            text="VISUALISATION 3D",
            font=('Arial', 18, 'bold'),
            bg=COLORS['bg_light'],
            fg=COLORS['primary']
        ).pack(pady=5)
        
        # Message informatif
        info_text = (
            "La visualisation 3D interactive dans l'interface\n"
            "n'est pas encore opérationnelle.\n\n"
            "Cependant, vous pouvez générer un script Python\n"
            "autonome pour visualiser votre robot avec :\n\n"
            "✅ Visualisation 3D complète\n"
            "✅ Sliders interactifs pour les articulations\n"
            "✅ Rotation et zoom de la vue\n"
            "✅ Basé sur Matplotlib (léger et portable)"
        )
        
        tk.Label(
            info_frame,
            text=info_text,
            font=('Arial', 10),
            bg=COLORS['bg_light'],
            fg=COLORS['text_dark'],
            justify=tk.CENTER,
            wraplength=450
        ).pack(pady=20)
        
        # Bouton de génération
        ModernButton(
            info_frame,
            "🐍 Générer Script Python",
            self.generate_visualization_script,
            bg_color=COLORS['success'],
            fg_color=COLORS['text_light'],
            width=250,
            height=50
        ).pack(pady=(20, 10))
        
        # Note technique
        tk.Label(
            info_frame,
            text="💡 Le script généré est totalement autonome et ne nécessite\n"
                 "que NumPy et Matplotlib pour fonctionner.",
            font=('Arial', 8, 'italic'),
            bg=COLORS['bg_light'],
            fg=COLORS['text_dark'],
            justify=tk.CENTER
        ).pack(pady=(10, 20))
        
        # Variables pour stocker le MGD calculé (compatibilité)
        self.current_symo = None
        self.current_mgd_robot = None
        self.renderer_3d = None  # Pour compatibilité avec le reste du code

    def generate_visualization_script(self):
        """Génère le script Python de visualisation du robot"""
        if not hasattr(self, 'robo') or not self.robo:
            messagebox.showerror(
                "Erreur", 
                "Aucun robot chargé.\n\n"
                "Veuillez d'abord créer ou charger un robot."
            )
            return
        
        # Synchroniser DH si le tableau existe
        if hasattr(self, 'dh_entries') and self.dh_entries:
            try:
                self._sync_robot_from_dh()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur synchronisation DH:\n{e}")
                return
        
        # Nom du fichier par défaut
        safe_name = self.robo.name.lower().replace(" ", "_")
        default_name = f"visualize_{safe_name}.py"
        
        # Demander où sauvegarder
        output_path = filedialog.asksaveasfilename(
            title="💾 Sauvegarder le script de visualisation",
            initialfile=default_name,
            defaultextension=".py",
            filetypes=[("Script Python", "*.py"), ("Tous les fichiers", "*.*")]
        )
        
        if not output_path:
            return
        
        try:
            # Générer le script
            self._generate_script_content(output_path)
            
            # Message de succès avec instructions
            messagebox.showinfo(
                "✅ Script généré !",
                f"Script de visualisation créé avec succès !\n\n"
                f"📄 Fichier: {os.path.basename(output_path)}\n\n"
                f"🚀 Pour lancer la visualisation:\n"
                f"   python {os.path.basename(output_path)}\n\n"
                f"📦 Dépendances requises:\n"
                f"   • NumPy\n"
                f"   • Matplotlib\n\n"
                f"Installez-les avec:\n"
                f"   pip install numpy matplotlib"
            )
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erreur", f"Échec de la génération:\n{e}")

    def _generate_script_content(self, output_path):
        """Génère le contenu du script de visualisation"""
        from exportation_python import generateur
        import numpy as np
        
        # Préparer les données DH
        dh_table = []
        for i in range(1, self.robo.NJ):
            row = []
            for param in ['theta', 'd', 'r', 'alpha']:
                value = self.robo.get_val(i, param)
                
                # Convertir en numérique si possible
                try:
                    if hasattr(value, '__float__'):
                        value = float(value)
                    elif isinstance(value, str):
                        # Essayer d'évaluer comme expression
                        try:
                            value = float(eval(value, {"pi": np.pi}))
                        except:
                            value = 0.0
                    else:
                        value = float(value)
                except:
                    value = 0.0
                
                row.append(value)
            
            dh_table.append(row)
        
        # Types d'articulations
        sigmas = [int(self.robo.get_val(i, 'sigma')) for i in range(1, self.robo.NJ)]
        
        # Constantes (si définies)
        constants = getattr(self.robo, 'constants', {})
        
        # Générer le script
        generator = generateur.RobotScriptGenerator(
            robot_name=self.robo.name,
            dh_table=dh_table,
            sigmas=sigmas,
            constants=constants
        )
        
        generator.generate(output_path)

    def update_robot_visualization_from_mgd(self, symo, robot, joint_angles_deg=None):
        """
        [STUB] Méthode de compatibilité pour l'ancien système.
        Ne fait rien mais évite les erreurs dans le code existant.
        """
        self.current_symo = symo
        self.current_mgd_robot = robot
        
        # Informer l'utilisateur qu'il peut générer un script
        print(f"ℹ️ Robot '{robot.name}' prêt pour la visualisation via script Python.")
        print(f"   Utilisez le bouton '🐍 Générer Script Python' pour créer le visualiseur.")

    def _sync_robot_from_dh(self):
        """Synchronise le robot avec les paramètres DH saisis"""
        if not hasattr(self, 'dh_entries') or not self.dh_entries:
            return
        
        try:
            for i, joint in enumerate(self.dh_entries, 1):
                frame_idx = i
                
                # Récupérer les valeurs
                theta_val = self._parse_dh_value(joint['theta'].get())
                d_val = self._parse_dh_value(joint['d'].get())
                r_val = self._parse_dh_value(joint['r'].get())
                alpha_val = self._parse_dh_value(joint['alpha'].get())
                joint_type = joint['type'].get()
                
                # Mettre à jour le robot
                self.robo.put_val(frame_idx, 'theta', theta_val)
                self.robo.put_val(frame_idx, 'd', d_val)
                self.robo.put_val(frame_idx, 'r', r_val)
                self.robo.put_val(frame_idx, 'alpha', alpha_val)
                
                sigma = 0 if 'R' in joint_type else 1
                self.robo.put_val(frame_idx, 'sigma', sigma)
            
            print("✅ Paramètres DH synchronisés")
        except Exception as e:
            print(f"❌ Erreur synchronisation DH: {e}")
            raise

    def _parse_dh_value(self, value_str):
        """Parse une valeur DH (numérique ou symbolique)"""
        if not value_str or value_str.strip() == "":
            return 0.0
        
        value_str = value_str.strip()
        
        try:
            return float(value_str)
        except ValueError:
            return value_str