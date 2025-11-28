from Interface import tk, COLORS, ModernButton
from .base_mixin import BaseMixin


class VisualizationMixin(BaseMixin):
    """Mixin pour la visualisation 3D du robot"""
    
    PLACEHOLDER_TEXT = (
        "🤖\n\n"
        "Votre robot apparaîtra ici\n\n"
        "1️⃣ Définissez les paramètres DH\n"
        "2️⃣ Validez la configuration\n"
        "3️⃣ Visualisez votre robot en 3D"
    )
    
    CONTROL_BUTTONS = [
        ("↻ Rotation", lambda: None),
        ("🔍 Zoom", lambda: None),
        ("🔄 Reset", lambda: None)
    ]
    
    def create_visualization_section(self, parent):
        """Section de visualisation 3D"""
        # Info card
        self.create_info_card(
            parent,
            "Visualisation 3D interactive de votre robot\n"
            "La représentation apparaîtra après validation des paramètres",
            icon="🎨"
        )
        
        # Canvas de visualisation
        self._create_visualization_canvas(parent)
        
        # Contrôles
        self._create_visualization_controls(parent)
    
    def _create_visualization_canvas(self, parent):
        """Crée le canvas de visualisation"""
        container = tk.Frame(parent, bg=COLORS['border'], relief=tk.FLAT, bd=2)
        container.pack(fill=tk.BOTH, expand=True)
        
        self.viz_canvas = tk.Canvas(
            container,
            bg=COLORS['bg_light'],
            highlightthickness=0
        )
        self.viz_canvas.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Placeholder
        self.viz_canvas.create_text(
            200,  # Position relative fixe
            150,
            text=self.PLACEHOLDER_TEXT,
            font=('Arial', 12),
            fill=COLORS['text_dark'],
            justify=tk.CENTER,
            tags='placeholder'  # ✅ Tag pour faciliter la suppression
        )
    
    def _create_visualization_controls(self, parent):
        """Crée les contrôles de visualisation"""
        frame = tk.Frame(parent, bg=COLORS['bg_white'])
        frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(
            frame,
            text="🎮 Contrôles:",
            bg=COLORS['bg_white'],
            fg=COLORS['text_dark'],
            font=('Arial', 10, 'bold')
        ).pack(side=tk.LEFT, padx=5)
        
        # Créer les boutons dynamiquement
        for label, command in self.CONTROL_BUTTONS:
            ModernButton(
                frame,
                label,
                command,
                bg_color=COLORS['accent'],
                fg_color=COLORS['text_light'],
                width=100,
                height=30
            ).pack(side=tk.LEFT, padx=5)
    
    # ✅ Méthode pour supprimer le placeholder et afficher le robot
    def display_robot_3d(self, robot_data):
        """
        Affiche le robot en 3D (à implémenter).
        
        Args:
            robot_data: Données du robot à visualiser
        """
        # Supprimer le placeholder
        self.viz_canvas.delete('placeholder')
        
        # TODO: Implémenter la visualisation 3D réelle
        self.viz_canvas.create_text(
            200, 150,
            text="🤖 Visualisation 3D\n(À implémenter)",
            font=('Arial', 14, 'bold'),
            fill=COLORS['primary']
        )

