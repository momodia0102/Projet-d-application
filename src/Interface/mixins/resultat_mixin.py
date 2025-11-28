from Interface import tk, ttk, COLORS
from .base_mixin import BaseMixin


class ResultMixin(BaseMixin):
    """Mixin pour la gestion des résultats avec architecture extensible"""
    
    # ✅ Configuration centralisée des onglets
    RESULT_TABS = [
        {
            'id': 'mgd',
            'icon': '🔍',
            'title': 'MGD',
            'full_name': 'Modèle Géométrique Direct',
            'description': "Calcule la position de l'effecteur à partir des angles articulaires"
        },
        {
            'id': 'mgi',
            'icon': '🔄',
            'title': 'MGI',
            'full_name': 'Modèle Géométrique Inverse',
            'description': "Calcule les angles articulaires pour atteindre une position donnée"
        },
        {
            'id': 'mcd',
            'icon': '⚡',
            'title': 'MCD',
            'full_name': 'Modèle Cinématique Direct',
            'description': "Calcule la vitesse de l'effecteur à partir des vitesses articulaires"
        },
        {
            'id': 'mci',
            'icon': '🎯',
            'title': 'MCI',
            'full_name': 'Modèle Cinématique Inverse',
            'description': "Calcule les vitesses articulaires pour une vitesse d'effecteur donnée"
        }
    ]
    
    def create_results_section(self, parent):
        """Section d'affichage des résultats"""
        # Info card
        self.create_info_card(
            parent,
            "Résultats des calculs de modélisation\n"
            "Sélectionnez un onglet pour voir les détails",
            icon="📈"
        )
        
        # Notebook
        notebook = ttk.Notebook(parent, style='Modern.TNotebook')
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # ✅ Dictionnaire pour stocker les widgets (meilleure pratique)
        self.result_widgets = {}
        
        # Créer les onglets dynamiquement
        for tab_config in self.RESULT_TABS:
            frame = tk.Frame(notebook, bg=COLORS['bg_white'])
            notebook.add(frame, text=f"{tab_config['icon']} {tab_config['title']}")
            
            # Créer et stocker le widget texte
            text_widget = self._create_result_tab(
                frame,
                tab_config['full_name'],
                tab_config['description']
            )
            self.result_widgets[tab_config['id']] = text_widget
        
        # ✅ Rétrocompatibilité (à supprimer progressivement)
        self.mgd_text_widget = self.result_widgets.get('mgd')
        self.mgi_text_widget = self.result_widgets.get('mgi')
        self.mcd_text_widget = self.result_widgets.get('mcd')
        self.mci_text_widget = self.result_widgets.get('mci')
    
    def _create_result_tab(self, parent, title, description):
        """Crée un onglet de résultats avec structure standardisée"""
        # En-tête
        self._create_tab_header(parent, title, description)
        
        # Zone de texte
        text_widget = self._create_text_area(parent, title)
        
        return text_widget
    
    def _create_tab_header(self, parent, title, description):
        """Crée l'en-tête d'un onglet"""
        header = tk.Frame(parent, bg=COLORS['primary'])
        header.pack(fill=tk.X)
        
        tk.Label(
            header,
            text=title,
            font=('Arial', 13, 'bold'),
            bg=COLORS['primary'],
            fg=COLORS['secondary'],
            pady=10
        ).pack()
        
        tk.Label(
            header,
            text=description,
            font=('Arial', 9),
            bg=COLORS['primary'],
            fg=COLORS['text_light'],
            pady=5
        ).pack()
    
    def _create_text_area(self, parent, title):
        """Crée la zone de texte avec scrollbar"""
        frame = tk.Frame(parent, bg=COLORS['bg_white'])
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text = tk.Text(
            frame,
            wrap=tk.WORD,
            font=('Courier', 10),
            bg=COLORS['bg_light'],
            fg=COLORS['text_dark'],
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        
        scrollbar = ttk.Scrollbar(frame, command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)
        
        # Placeholder
        placeholder = self._create_placeholder_text(title)
        text.insert('1.0', placeholder)
        text.configure(state='disabled')
        
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        return text
    
    def _create_placeholder_text(self, title):
        """Génère le texte placeholder"""
        return (
            f"\n📋 Résultats du {title}\n\n"
            "Les calculs apparaîtront ici après validation des paramètres.\n\n"
            "💡 Astuce: Utilisez le menu ☰ en haut à droite pour lancer les calculs."
        )
    
    # ✅ Méthode publique pour mettre à jour les résultats
    def update_result(self, result_id, content):
        """
        Met à jour le contenu d'un résultat.
        
        Args:
            result_id (str): 'mgd', 'mgi', 'mcd', ou 'mci'
            content (str): Contenu à afficher
        """
        if result_id not in self.result_widgets:
            self.show_error("Erreur", f"Onglet '{result_id}' non trouvé")
            return
        
        widget = self.result_widgets[result_id]
        widget.configure(state='normal')
        widget.delete('1.0', tk.END)
        widget.insert('1.0', content)
        widget.configure(state='disabled')
