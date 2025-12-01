# visualisation_mixin.py

import tkinter as tk
from Interface.style import COLORS, ModernButton
from .base_mixin import BaseMixin
from ..visualization.robot_3d_renderer import Robot3DRenderer # Assurez-vous du chemin relatif
from ..visualization.dh_visualizer import DHVisualizer
from ..visualization.symoro_bridge import SYMOROBridge


class VisualizationMixin(BaseMixin):
    """Mixin pour la visualisation 3D du robot - Version Rigoureuse"""
    
    def create_visualization_section(self, parent):
        """Section de visualisation 3D"""
        
        # Info card
        self.create_info_card(
            parent,
            "Visualisation 3D interactive de votre robot\n"
            "Basée sur les calculs MGD de SYMORO",
            icon="🎨"
        )
        
        # Conteneur principal
        viz_container = tk.Frame(parent, bg=COLORS['bg_white'])
        viz_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Moteur de rendu 3D (Robot3DRenderer)
        self.renderer_3d = Robot3DRenderer(viz_container, width=5, height=5, dpi=80)
        self.renderer_3d.pack(fill=tk.BOTH, expand=True)
        
        # Contrôles
        self._create_visualization_controls(parent)
        
        # Variables pour stocker le MGD calculé
        self.current_symo = None
        self.current_mgd_robot = None
    
    def _create_visualization_controls(self, parent):
        """Crée les contrôles de visualisation (Zoom, Rotation, Reset)."""
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
            ("🔍 +", lambda: self.renderer_3d.zoom(factor=1.2)),
            ("🔍 -", lambda: self.renderer_3d.zoom(factor=0.8)),
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
        Met à jour la visualisation à partir des résultats MGD SYMORO.
        """
        try:
            # Sauvegarder pour réutilisation lors du mouvement des sliders
            self.current_symo = symo
            self.current_mgd_robot = robot
            
            # Obtenir les positions via le pont SYMORO
            positions, joint_types, transforms = DHVisualizer.from_symoro_results(
                symo, robot, joint_angles_deg
            )
            
            if positions is None:
                self.renderer_3d._plot_placeholder()
                return
            
            # Afficher
            self.renderer_3d.plot_robot(positions, joint_types, transforms, frame_size=0.15)
            
        except Exception as e:
            print(f"❌ Erreur visualisation: {e}")
            import traceback
            traceback.print_exc()
            self.show_error("Erreur", "Une erreur est survenue lors du rendu 3D.")