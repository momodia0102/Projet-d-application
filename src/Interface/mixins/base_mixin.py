class BaseMixin:
    """
    Mixin de base avec méthodes utilitaires communes.
    Évite la duplication de code entre les mixins.
    """
    def create_info_card(self, parent, text, icon="💡"):
        """Factory method pour créer des cartes d'information standardisées"""
        from Interface import COLORS, tk
        
        info_card = tk.Frame(parent, bg=COLORS['accent'], relief=tk.FLAT)
        info_card.pack(fill=tk.X, pady=(0, 10))
        
        info_label = tk.Label(
            info_card,
            text=f"{icon} {text}",
            bg=COLORS['accent'],
            fg=COLORS['text_light'],
            font=('Arial', 9),
            justify=tk.CENTER
        )
        info_label.pack(padx=10, pady=10)
        
        return info_card
    
    def create_separator(self, parent, height=2):
        """Factory method pour créer des séparateurs standardisés"""
        from Interface import COLORS, tk
        
        sep = tk.Frame(parent, height=height, bg=COLORS['border'])
        sep.pack(fill=tk.X, pady=10)
        return sep
    
    def show_error(self, title, message):
        """Gestion standardisée des erreurs"""
        from Interface import messagebox
        messagebox.showerror(title, f"❌ {message}")
    
    def show_success(self, title, message):
        """Gestion standardisée des succès"""
        from Interface import messagebox
        messagebox.showinfo(title, f"✅ {message}")