import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont




# Palette de couleurs Centrale Nantes
COLORS = {
    'primary': '#0F2847',      # Bleu marine foncé
    'secondary': '#F5B800',    # Jaune/Or
    'accent': '#1E4D7B',       # Bleu moyen
    'bg_light': '#F5F7FA',     # Fond clair
    'bg_white': '#FFFFFF',     # Blanc
    'text_dark': '#0F2847',    # Texte foncé
    'text_light': '#FFFFFF',   # Texte clair
    'success': '#28A745',      # Vert succès
    'warning': '#FFC107',      # Orange avertissement
    'border': '#D1D9E6' ,       # Bordure grise
    'error': '#DC3545'         # Rouge erreur
}


class ModernButton(tk.Canvas):
    """Bouton moderne avec effet hover"""
    
    def __init__(self, parent, text, command, bg_color=COLORS['secondary'], 
                 fg_color=COLORS['text_dark'], width=150, height=40):
        super().__init__(parent, width=width, height=height, 
                        highlightthickness=0, bg=parent['bg'])
        
        self.command = command
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.text = text
        
        # Créer le rectangle arrondi
        self.rect = self.create_rounded_rect(2, 2, width-2, height-2, 
                                             radius=10, fill=bg_color, outline='')
        self.text_id = self.create_text(width//2, height//2, text=text, 
                                       fill=fg_color, font=('Arial', 10, 'bold'))
        
        # Événements
        self.bind('<Button-1>', lambda e: self.command())
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        
    def create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        """Crée un rectangle aux coins arrondis"""
        points = [x1+radius, y1,
                 x1+radius, y1,
                 x2-radius, y1,
                 x2-radius, y1,
                 x2, y1,
                 x2, y1+radius,
                 x2, y1+radius,
                 x2, y2-radius,
                 x2, y2-radius,
                 x2, y2,
                 x2-radius, y2,
                 x2-radius, y2,
                 x1+radius, y2,
                 x1+radius, y2,
                 x1, y2,
                 x1, y2-radius,
                 x1, y2-radius,
                 x1, y1+radius,
                 x1, y1+radius,
                 x1, y1]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def on_enter(self, e):
        """Effet hover"""
        self.itemconfig(self.rect, fill=self.lighten_color(self.bg_color))
        
    def on_leave(self, e):
        """Retour à la normale"""
        self.itemconfig(self.rect, fill=self.bg_color)
        
    def lighten_color(self, color):
        """Éclaircit une couleur"""
        # Simplifié pour l'exemple
        return color
