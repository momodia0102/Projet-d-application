# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
from Interface.style import COLORS, ModernButton

class DialogDefinition(tk.Toplevel):
    """Dialog box for robot definition in Tkinter - Version Centrale Nantes"""
    
    def __init__(self, parent, current_name="", current_nl=0, current_nj=0, 
                 current_structure="", current_floating=False, current_mobile=False):
        super().__init__(parent)
        self.parent = parent
        self.result = None
        
        self.title("🤖 Nouveau Robot - SYMORO")
        # Rendu plus compact : Taille réduite
        self.geometry("600x500") 
        self.resizable(False, False)
        self.configure(bg=COLORS['bg_light'])
        self.transient(parent)
        self.grab_set()
        
        # Center the dialog
        self.center_window()
        
        # Variables pour stocker les valeurs
        self.current_name = current_name
        self.current_nl = current_nl
        self.current_nj = current_nj
        self.current_structure = current_structure
        self.current_floating = current_floating
        self.current_mobile = current_mobile
        
        self.init_ui()
        
    def center_window(self):
        """Center the dialog on the screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def init_ui(self):
        """Initialize the user interface"""
        main_frame = tk.Frame(self, bg=COLORS['bg_light'], padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=COLORS['primary'])
        header_frame.pack(fill=tk.X, pady=(0, 10)) # PADY RÉDUIT
        
        title_label = tk.Label(header_frame,
                              text="🎯 CRÉATION D'UN NOUVEAU ROBOT",
                              font=('Arial', 16, 'bold'),
                              bg=COLORS['primary'],
                              fg=COLORS['secondary'],
                              pady=15)
        title_label.pack()
        
        # Robot Information Section
        # NOTE : Utiliser expand=True ici pour que ce frame absorbe l'espace et maintienne les boutons visibles.
        info_frame = ttk.LabelFrame(main_frame, 
                                   text="📝 Informations de Base",
                                   style='Modern.TLabelframe',
                                   padding=15)
        info_frame.pack(fill=tk.X, expand=True, pady=(0, 10)) 
        
        # Robot Name
        name_frame = tk.Frame(info_frame, bg=COLORS['bg_white'])
        name_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(name_frame, text="Nom du robot:",
                font=('Arial', 10, 'bold'),
                bg=COLORS['bg_white'],
                fg=COLORS['text_dark']).pack(side=tk.LEFT, padx=(0, 10))
        
        self.name_var = tk.StringVar(value=self.current_name or "MonRobot")
        name_entry = tk.Entry(name_frame, 
                             textvariable=self.name_var,
                             font=('Arial', 10),
                             width=30,
                             bg=COLORS['bg_light'],
                             relief=tk.SOLID,
                             bd=1)
        name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Structure Parameters (NL is enough for serial robots)
        struct_frame = tk.Frame(info_frame, bg=COLORS['bg_white'])
        struct_frame.pack(fill=tk.X, pady=10)
        
        # Number of Links (NL) - Combined input label
        links_frame = tk.Frame(struct_frame, bg=COLORS['bg_white'])
        links_frame.pack(fill=tk.X, expand=True) 
        
        # Remplacement par "Nombre d'articulations:"
        tk.Label(links_frame, text="Nombre d'articulations:",
                font=('Arial', 9, 'bold'),
                bg=COLORS['bg_white'],
                fg=COLORS['text_dark']).pack(side=tk.LEFT, padx=(0, 10)) 

        self.nl_var = tk.IntVar(value=self.current_nl or 6)
        nl_spin = tk.Spinbox(links_frame, 
                            from_=1, to=20,
                            textvariable=self.nl_var,
                            width=8,
                            font=('Arial', 10),
                            bg=COLORS['bg_light'])
        nl_spin.pack(side=tk.LEFT)
        
        # Robot Type Section

        
        # We enforce "Série"
        self.structure_var = tk.StringVar(value="Série")
        


        
        # Base Configuration Section
        base_frame = ttk.LabelFrame(main_frame, 
                                   text="🏗️ Configuration de Base",
                                   style='Modern.TLabelframe',
                                   padding=15)
        base_frame.pack(fill=tk.X, pady=(0, 10)) # PADY RÉDUIT
        
        # Floating Base
        base_options_frame = tk.Frame(base_frame, bg=COLORS['bg_white'])
        base_options_frame.pack(fill=tk.X, pady=5)
        
        self.floating_var = tk.BooleanVar(value=self.current_floating)
        floating_cb = tk.Checkbutton(base_options_frame,
                                    text="Base flottante",
                                    variable=self.floating_var,
                                    font=('Arial', 10),
                                    bg=COLORS['bg_white'],
                                    fg=COLORS['text_dark'],
                                    selectcolor=COLORS['secondary'])
        floating_cb.pack(anchor=tk.W)
        
        # Mobile Robot
        self.mobile_var = tk.BooleanVar(value=self.current_mobile)
        mobile_cb = tk.Checkbutton(base_options_frame,
                                  text="Robot mobile",
                                  variable=self.mobile_var,
                                  font=('Arial', 10),
                                  bg=COLORS['bg_white'],
                                  fg=COLORS['text_dark'],
                                  selectcolor=COLORS['secondary'])
        mobile_cb.pack(anchor=tk.W, pady=(5, 0))

        
        # Buttons Section (DOIT ÊTRE VISIBLE)
        buttons_frame = tk.Frame(main_frame, bg=COLORS['bg_light'])
        buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Cancel Button
        cancel_btn = ModernButton(buttons_frame,
                                 "❌ Annuler",
                                 self.on_cancel,
                                 bg_color=COLORS['warning'],
                                 fg_color=COLORS['text_dark'],
                                 width=120, height=45)
        cancel_btn.pack(side=tk.LEFT, padx=(0, 20))
        
        # Create Button
        create_btn = ModernButton(buttons_frame,
                                 "✅ Créer le Robot",
                                 self.on_create,
                                 bg_color=COLORS['success'],
                                 fg_color=COLORS['text_light'],
                                 width=150, height=45)
        create_btn.pack(side=tk.RIGHT)
        
    def on_create(self):
        """Handle create button click"""
        if not self.name_var.get().strip():
            messagebox.showerror("Erreur", "Veuillez entrer un nom pour le robot.")
            return
        
        # Logique simplifiée pour robot série: NL = NJ = NF
        num_links = self.nl_var.get()
            
        self.result = {
            'name': self.name_var.get().strip(),
            'num_links': num_links,
            'num_joints': num_links,
            'num_frames': num_links,
            'structure': self.structure_var.get(),
            'is_floating': self.floating_var.get(),
            'is_mobile': self.mobile_var.get()
        }
        self.destroy()
        
    def on_cancel(self):
        """Handle cancel button click"""
        self.result = None
        self.destroy()
        
    def get_values(self):
        """Return the dialog values"""
        return self.result