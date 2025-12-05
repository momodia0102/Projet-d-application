# visualization_mixin.py (VERSION OPENGL)

import tkinter as tk
from Interface.style import COLORS, ModernButton
from .base_mixin import BaseMixin
from ..visualization.robot_opengl_renderer import RobotOpenGLRenderer  # ⬅️ NOUVEAU
from ..visualization.dh_visualizer import DHVisualizer
from ..visualization.symoro_bridge import SYMOROBridge


class VisualizationMixin(BaseMixin):
    """Mixin pour la visualisation 3D du robot - Version OpenGL"""
    
    def create_visualization_section(self, parent):
        """Section de visualisation 3D avec OpenGL."""
        
        # Info card
        self.create_info_card(
            parent,
            "Visualisation 3D interactive (OpenGL)\n"
            "Rotation: Clic gauche + Drag | Zoom: Molette",
            icon="🎨"
        )
        
        # Conteneur principal
        viz_container = tk.Frame(parent, bg=COLORS['bg_white'])
        viz_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 🎯 MOTEUR OPENGL (au lieu de Matplotlib)
        self.renderer_3d = RobotOpenGLRenderer(viz_container, width=600, height=600)
        self.renderer_3d.pack(fill=tk.BOTH, expand=True)
        
        # Contrôles
        self._create_visualization_controls(parent)
        
        # Variables pour stocker le MGD calculé
        self.current_symo = None
        self.current_mgd_robot = None
    
    def _create_visualization_controls(self, parent):
        """Crée les contrôles de visualisation."""
        frame = tk.Frame(parent, bg=COLORS['bg_white'])
        frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(
            frame,
            text="🎮 Contrôles:",
            bg=COLORS['bg_white'],
            fg=COLORS['text_dark'],
            font=('Arial', 10, 'bold')
        ).pack(side=tk.LEFT, padx=5)
        
        controls = [
            ("↻ ←", lambda: self.renderer_3d.rotate_view(delta_azim=-10)),
            ("↻ →", lambda: self.renderer_3d.rotate_view(delta_azim=10)),
            ("↻ ↑", lambda: self.renderer_3d.rotate_view(delta_elev=10)),
            ("↻ ↓", lambda: self.renderer_3d.rotate_view(delta_elev=-10)),
            ("🔍 +", lambda: self.renderer_3d.zoom(factor=0.9)),
            ("🔍 -", lambda: self.renderer_3d.zoom(factor=1.1)),
            ("🔄 Reset", self.renderer_3d.reset_view)
        ]
        
        for label, command in controls:
            ModernButton(
                frame,
                label,
                command,
                bg_color=COLORS['accent'],
                fg_color=COLORS['text_light'],
                width=80,
                height=30
            ).pack(side=tk.LEFT, padx=2)
    
    def update_robot_visualization_from_mgd(self, symo, robot, joint_angles_deg=None):
        """
        Met à jour la visualisation OpenGL à partir des résultats MGD SYMORO.
        
        Parameters
        ----------
        symo : SymbolManager
            Résultat du calcul MGD
        robot : Robot
            Instance du robot SYMORO
        joint_angles_deg : dict, optional
            Configuration articulaire {nom_variable: valeur_degrés}
        """
        try:
            # Sauvegarder pour réutilisation
            self.current_symo = symo
            self.current_mgd_robot = robot
            
            # Obtenir les positions via le pont SYMORO
            positions, joint_types, transforms = DHVisualizer.from_symoro_results(
                symo, robot, joint_angles_deg
            )
            
            if positions is None:
                self.renderer_3d.clear()
                return
            
            # ✅ Afficher avec OpenGL
            self.renderer_3d.plot_robot(positions, joint_types, transforms)
            
        except Exception as e:
            print(f"❌ Erreur visualisation OpenGL: {e}")
            import traceback
            traceback.print_exc()
            self.show_error("Erreur", f"Erreur lors du rendu 3D:\n{e}")