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
        self.geometry("600x700")
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
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(header_frame,
                              text="🎯 CRÉATION D'UN NOUVEAU ROBOT",
                              font=('Arial', 16, 'bold'),
                              bg=COLORS['primary'],
                              fg=COLORS['secondary'],
                              pady=15)
        title_label.pack()
        
        # Robot Information Section
        info_frame = ttk.LabelFrame(main_frame, 
                                   text="📝 Informations de Base",
                                   style='Modern.TLabelframe',
                                   padding=15)
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
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
        
        # Structure Parameters
        struct_frame = tk.Frame(info_frame, bg=COLORS['bg_white'])
        struct_frame.pack(fill=tk.X, pady=10)
        
        # Number of Links
        links_frame = tk.Frame(struct_frame, bg=COLORS['bg_white'])
        links_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        tk.Label(links_frame, text="Nombre de liens (NL):",
                font=('Arial', 9, 'bold'),
                bg=COLORS['bg_white'],
                fg=COLORS['text_dark']).pack(anchor=tk.W)
        
        self.nl_var = tk.IntVar(value=self.current_nl or 6)
        nl_spin = tk.Spinbox(links_frame, 
                            from_=1, to=20,
                            textvariable=self.nl_var,
                            width=8,
                            font=('Arial', 10),
                            bg=COLORS['bg_light'])
        nl_spin.pack(pady=5)
        
        # Number of Joints
        joints_frame = tk.Frame(struct_frame, bg=COLORS['bg_white'])
        joints_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        tk.Label(joints_frame, text="Nombre de joints (NJ):",
                font=('Arial', 9, 'bold'),
                bg=COLORS['bg_white'],
                fg=COLORS['text_dark']).pack(anchor=tk.W)
        
        self.nj_var = tk.IntVar(value=self.current_nj or 6)
        nj_spin = tk.Spinbox(joints_frame, 
                            from_=1, to=20,
                            textvariable=self.nj_var,
                            width=8,
                            font=('Arial', 10),
                            bg=COLORS['bg_light'])
        nj_spin.pack(pady=5)
        
        # Number of Frames
        frames_frame = tk.Frame(struct_frame, bg=COLORS['bg_white'])
        frames_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(frames_frame, text="Nombre de frames (NF):",
                font=('Arial', 9, 'bold'),
                bg=COLORS['bg_white'],
                fg=COLORS['text_dark']).pack(anchor=tk.W)
        
        self.nf_var = tk.IntVar(value=max((self.current_nj or 6) + 1, 7))
        nf_spin = tk.Spinbox(frames_frame, 
                            from_=2, to=21,
                            textvariable=self.nf_var,
                            width=8,
                            font=('Arial', 10),
                            bg=COLORS['bg_light'])
        nf_spin.pack(pady=5)
        
        # Robot Type Section
        type_frame = ttk.LabelFrame(main_frame, 
                                   text="🔧 Type de Structure",
                                   style='Modern.TLabelframe',
                                   padding=15)
        type_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.structure_var = tk.StringVar(value=self.current_structure or "Série")
        structures = ["Série"]
        
        for i, struct in enumerate(structures):
            rb = tk.Radiobutton(type_frame,
                               text=struct,
                               variable=self.structure_var,
                               value=struct,
                               font=('Arial', 10),
                               bg=COLORS['bg_white'],
                               fg=COLORS['text_dark'],
                               selectcolor=COLORS['secondary'])
            rb.pack(anchor=tk.W, pady=2)
        
        # Base Configuration Section
        base_frame = ttk.LabelFrame(main_frame, 
                                   text="🏗️ Configuration de Base",
                                   style='Modern.TLabelframe',
                                   padding=15)
        base_frame.pack(fill=tk.X, pady=(0, 15))
        
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

        
        # Buttons Section
        buttons_frame = tk.Frame(main_frame, bg=COLORS['bg_light'])
        buttons_frame.pack(fill=tk.X, pady=20)
        
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
            
        self.result = {
            'name': self.name_var.get().strip(),
            'num_links': self.nl_var.get(),
            'num_joints': self.nj_var.get(),
            'num_frames': self.nf_var.get(),
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