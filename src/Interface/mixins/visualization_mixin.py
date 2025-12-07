# visualization_mixin.py (VERSION OPENGL)

import tkinter as tk
import sys
import os
from Interface.style import COLORS, ModernButton
from .base_mixin import BaseMixin

# ⬅️ CORRECTION IMPORT : Chemin absolu
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'visualization'))
try:
    from ..visualization.robot_opengl_renderer import RobotOpenGLRenderer
except ImportError as e:
    print(f"⚠️ Erreur import RobotOpenGLRenderer: {e}")
    RobotOpenGLRenderer = None


class VisualizationMixin(BaseMixin):
    """Mixin pour la visualisation 3D du robot """
    
    def create_visualization_section(self, parent):
        """Section de visualisation 3D du robot."""
        
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
        if RobotOpenGLRenderer is not None:
            self.renderer_3d = RobotOpenGLRenderer(viz_container, width=600, height=600)
            self.renderer_3d.pack(fill=tk.BOTH, expand=True)
        else:
            # Fallback si OpenGL n'est pas disponible
            tk.Label(viz_container, text="⚠️ OpenGL non disponible", 
                    bg=COLORS['bg_white'], font=('Arial', 12)).pack(expand=True)
            self.renderer_3d = None
        
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
            ("↻ ←", lambda: self.renderer_3d.rotate_view(delta_azim=-10) if self.renderer_3d else None),
            ("↻ →", lambda: self.renderer_3d.rotate_view(delta_azim=10) if self.renderer_3d else None),
            ("↻ ↑", lambda: self.renderer_3d.rotate_view(delta_elev=10) if self.renderer_3d else None),
            ("↻ ↓", lambda: self.renderer_3d.rotate_view(delta_elev=-10) if self.renderer_3d else None),
            ("🔍 +", lambda: self.renderer_3d.zoom(factor=0.9) if self.renderer_3d else None),
            ("🔍 -", lambda: self.renderer_3d.zoom(factor=1.1) if self.renderer_3d else None),
            ("🔄 Reset", self.renderer_3d.reset_view if self.renderer_3d else lambda: None)
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
        [MODIFIÉ] Charge le robot dans le moteur OpenGL et applique les valeurs articulaires.
        """
        if self.renderer_3d is None:
            print("⚠️ Renderer OpenGL non disponible")
            return
            
        try:
            # 1. Charger le robot (construit la hiérarchie JointNode)
            self.renderer_3d.load_robot(robot) 
            
            # 2. Appliquer les valeurs articulaires actuelles ou par défaut
            if joint_angles_deg is None:
                joint_angles_deg = {}
                
            # 3. Appel direct à la méthode du renderer
            self.renderer_3d.set_joint_values(joint_angles_deg)
            
            print(f"✅ Robot visualisé : {robot.name} ({robot.NJ-1} joints)")
            
        except Exception as e:
            print(f"❌ Erreur visualisation OpenGL: {e}")
            import traceback
            traceback.print_exc()
            self.show_error("Erreur", f"Erreur lors du rendu 3D:\n{e}")