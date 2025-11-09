"""
Fenêtre principale de l'application Robot Modeler
Version améliorée - Design Centrale Nantes
"""
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
    'border': '#D1D9E6'        # Bordure grise
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


class MainWindow:
    """Fenêtre principale de l'application - Version moderne"""
    
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_styles()
        self.create_header()
        self.create_main_layout()
        self.create_footer()
        
    def setup_window(self):
        """Configuration de la fenêtre principale"""
        self.root.title("Robot Modeler 🤖 - Centrale Nantes")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        self.root.configure(bg=COLORS['bg_light'])
        
        # Centrer la fenêtre
        self.center_window()
        
    def center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_styles(self):
        """Configure les styles ttk personnalisés"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Style pour les LabelFrame
        style.configure('Modern.TLabelframe', 
                       background=COLORS['bg_white'],
                       borderwidth=2,
                       relief='flat')
        style.configure('Modern.TLabelframe.Label',
                       background=COLORS['bg_white'],
                       foreground=COLORS['primary'],
                       font=('Arial', 11, 'bold'))
        
        # Style pour les Entry
        style.configure('Modern.TEntry',
                       fieldbackground=COLORS['bg_white'],
                       borderwidth=1,
                       relief='solid')
        
        # Style pour les Combobox
        style.configure('Modern.TCombobox',
                       fieldbackground=COLORS['bg_white'],
                       background=COLORS['bg_white'])
        
        # Style pour les Notebook
        style.configure('Modern.TNotebook',
                       background=COLORS['bg_white'],
                       borderwidth=0)
        style.configure('Modern.TNotebook.Tab',
                       background=COLORS['bg_light'],
                       foreground=COLORS['text_dark'],
                       padding=[20, 10],
                       font=('Arial', 10, 'bold'))
        style.map('Modern.TNotebook.Tab',
                 background=[('selected', COLORS['secondary'])],
                 foreground=[('selected', COLORS['text_dark'])])
        
    def create_header(self):
        """Crée l'en-tête avec logo et titre"""
        header = tk.Frame(self.root, bg=COLORS['primary'], height=80)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)
        
        # Titre principal
        title_frame = tk.Frame(header, bg=COLORS['primary'])
        title_frame.pack(expand=True)
        
        title_label = tk.Label(title_frame, 
                              text="🤖 ROBOT MODELER",
                              font=('Arial', 24, 'bold'),
                              bg=COLORS['primary'],
                              fg=COLORS['secondary'])
        title_label.pack(side=tk.LEFT, padx=10)
        
        subtitle_label = tk.Label(title_frame,
                                 text="Modélisation de Robots Manipulateurs",
                                 font=('Arial', 12),
                                 bg=COLORS['primary'],
                                 fg=COLORS['text_light'])
        subtitle_label.pack(side=tk.LEFT, padx=10)
        
        # Menu hamburger (simplifié)
        menu_btn = tk.Label(header, text="☰", font=('Arial', 20),
                           bg=COLORS['primary'], fg=COLORS['secondary'],
                           cursor='hand2')
        menu_btn.pack(side=tk.RIGHT, padx=20)
        menu_btn.bind('<Button-1>', lambda e: self.show_menu())
        
    def show_menu(self):
        """Affiche un menu contextuel moderne"""
        menu = tk.Menu(self.root, tearoff=0, 
                      bg=COLORS['bg_white'],
                      fg=COLORS['text_dark'],
                      activebackground=COLORS['secondary'],
                      font=('Arial', 10))
        
        menu.add_command(label="📁 Nouveau robot", command=self.new_robot)
        menu.add_command(label="📂 Charger un robot", command=self.load_robot)
        menu.add_command(label="💾 Sauvegarder", command=self.save_robot)
        menu.add_separator()
        menu.add_command(label="📐 Modèle Géométrique Direct", command=self.calc_mgd)
        menu.add_command(label="🔄 Modèle Géométrique Inverse", command=self.calc_mgi)
        menu.add_command(label="⚡ Modèle Cinématique Direct", command=self.calc_mcd)
        menu.add_command(label="🎯 Modèle Cinématique Inverse", command=self.calc_mci)
        menu.add_separator()
        menu.add_command(label="📚 Documentation", command=self.show_help)
        menu.add_command(label="ℹ️ À propos", command=self.show_about)
        menu.add_separator()
        menu.add_command(label="❌ Quitter", command=self.root.quit)
        
        # Afficher le menu à la position de la souris
        try:
            menu.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery())
        finally:
            menu.grab_release()
        
    def create_main_layout(self):
        """Crée la disposition principale avec 3 zones"""
        
        # Conteneur principal avec padding
        main_container = tk.Frame(self.root, bg=COLORS['bg_light'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # PanedWindow pour redimensionner
        main_paned = tk.PanedWindow(main_container, orient=tk.HORIZONTAL,
                                    bg=COLORS['bg_light'], 
                                    sashwidth=8,
                                    sashrelief=tk.FLAT,
                                    bd=0)
        main_paned.pack(fill=tk.BOTH, expand=True)
        
        # === ZONE GAUCHE : Paramètres DH ===
        left_frame = ttk.LabelFrame(main_paned, 
                                   text="⚙️ Paramètres Denavit-Hartenberg",
                                   style='Modern.TLabelframe',
                                   padding=15)
        main_paned.add(left_frame, minsize=350)
        self.create_dh_parameters_section(left_frame)
        
        # === ZONE CENTRALE : Visualisation ===
        center_frame = ttk.LabelFrame(main_paned,
                                     text="👁️ Visualisation 3D du Robot",
                                     style='Modern.TLabelframe',
                                     padding=15)
        main_paned.add(center_frame, minsize=450)
        self.create_visualization_section(center_frame)
        
        # === ZONE DROITE : Résultats ===
        right_frame = ttk.LabelFrame(main_paned,
                                    text="📊 Résultats et Calculs",
                                    style='Modern.TLabelframe',
                                    padding=15)
        main_paned.add(right_frame, minsize=350)
        self.create_results_section(right_frame)
        
    def create_dh_parameters_section(self, parent):
        """Section de saisie des paramètres DH - Version améliorée"""
        
        # Carte d'information pédagogique
        info_card = tk.Frame(parent, bg=COLORS['accent'], relief=tk.FLAT, bd=0)
        info_card.pack(fill=tk.X, pady=(0, 15))
        
        info_text = tk.Label(info_card,
                            text="💡 Les paramètres DH définissent la géométrie de votre robot.\n"
                                 "Commencez par choisir le nombre d'articulations !",
                            bg=COLORS['accent'],
                            fg=COLORS['text_light'],
                            font=('Arial', 9),
                            justify=tk.LEFT,
                            wraplength=300)
        info_text.pack(padx=10, pady=10)
        
        # Contrôles du nombre d'articulations
        control_frame = tk.Frame(parent, bg=COLORS['bg_white'])
        control_frame.pack(fill=tk.X, pady=(0, 15))
        
        control_label = tk.Label(control_frame,
                                text="🔢 Nombre d'articulations:",
                                bg=COLORS['bg_white'],
                                fg=COLORS['text_dark'],
                                font=('Arial', 10, 'bold'))
        control_label.pack(side=tk.LEFT, padx=5)
        
        self.joint_count = tk.IntVar(value=3)
        
        # Frame pour le spinbox stylisé
        spin_frame = tk.Frame(control_frame, bg=COLORS['bg_white'])
        spin_frame.pack(side=tk.LEFT, padx=10)
        
        joint_spin = tk.Spinbox(spin_frame, from_=1, to=6,
                               textvariable=self.joint_count,
                               width=8,
                               font=('Arial', 12, 'bold'),
                               bg=COLORS['bg_light'],
                               fg=COLORS['primary'],
                               buttonbackground=COLORS['secondary'],
                               relief=tk.FLAT,
                               bd=2)
        joint_spin.pack()
        
        # Bouton de génération moderne
        gen_btn = ModernButton(control_frame, "✨ Générer le tableau",
                              self.update_dh_table,
                              bg_color=COLORS['secondary'],
                              width=160, height=35)
        gen_btn.pack(side=tk.LEFT, padx=10)
        
        # Séparateur
        sep = tk.Frame(parent, height=2, bg=COLORS['border'])
        sep.pack(fill=tk.X, pady=10)
        
        # Frame scrollable pour le tableau DH
        canvas_frame = tk.Frame(parent, bg=COLORS['bg_white'])
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(canvas_frame, bg=COLORS['bg_white'],
                          highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical",
                                 command=canvas.yview)
        self.dh_table_frame = tk.Frame(canvas, bg=COLORS['bg_white'])
        
        self.dh_table_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.dh_table_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.dh_entries = []
        self.update_dh_table()
        
    def update_dh_table(self):
        """Met à jour le tableau des paramètres DH - Version colorée"""
        # Nettoyer le tableau existant
        for widget in self.dh_table_frame.winfo_children():
            widget.destroy()
        
        self.dh_entries = []
        n_joints = self.joint_count.get()
        
        # En-têtes avec style
        headers = [
            ("🔗", "Joint"),
            ("🔄", "θ (deg)"),
            ("📏", "d (m)"),
            ("📐", "a (m)"),
            ("↻", "α (deg)"),
            ("⚙️", "Type")
        ]
        
        for col, (icon, header) in enumerate(headers):
            header_frame = tk.Frame(self.dh_table_frame,
                                   bg=COLORS['primary'],
                                   relief=tk.FLAT)
            header_frame.grid(row=0, column=col, padx=2, pady=2, sticky='ew')
            
            label = tk.Label(header_frame,
                           text=f"{icon}\n{header}",
                           font=('Arial', 9, 'bold'),
                           bg=COLORS['primary'],
                           fg=COLORS['text_light'],
                           pady=8)
            label.pack(fill=tk.BOTH, expand=True)
        
        # Lignes pour chaque articulation avec alternance de couleurs
        for i in range(n_joints):
            joint_entries = {}
            row_bg = COLORS['bg_light'] if i % 2 == 0 else COLORS['bg_white']
            
            # Numéro du joint avec badge coloré
            joint_frame = tk.Frame(self.dh_table_frame, bg=row_bg)
            joint_frame.grid(row=i+1, column=0, padx=2, pady=2, sticky='ew')
            
            joint_badge = tk.Label(joint_frame,
                                  text=f"J{i+1}",
                                  font=('Arial', 10, 'bold'),
                                  bg=COLORS['secondary'],
                                  fg=COLORS['text_dark'],
                                  width=4,
                                  relief=tk.FLAT,
                                  pady=5)
            joint_badge.pack(pady=5)
            
            # Champs de saisie avec style
            for col, param in enumerate(['theta', 'd', 'a', 'alpha'], start=1):
                entry_frame = tk.Frame(self.dh_table_frame, bg=row_bg)
                entry_frame.grid(row=i+1, column=col, padx=2, pady=2, sticky='ew')
                
                entry = tk.Entry(entry_frame,
                               width=10,
                               font=('Arial', 10),
                               bg=COLORS['bg_white'],
                               fg=COLORS['text_dark'],
                               relief=tk.SOLID,
                               bd=1,
                               justify=tk.CENTER)
                entry.pack(pady=5, padx=5)
                entry.insert(0, "0.0")
                joint_entries[param] = entry
                
                # Tooltip au survol
                self.create_tooltip(entry, self.get_param_description(param))
            
            # Type d'articulation avec style
            type_frame = tk.Frame(self.dh_table_frame, bg=row_bg)
            type_frame.grid(row=i+1, column=5, padx=2, pady=2, sticky='ew')
            
            joint_type = ttk.Combobox(type_frame,
                                     values=["R (Rotation)", "P (Prismatique)"],
                                     width=12,
                                     state="readonly",
                                     font=('Arial', 9))
            joint_type.set("R (Rotation)")
            joint_type.pack(pady=5, padx=5)
            joint_entries['type'] = joint_type
            
            self.dh_entries.append(joint_entries)
        
        # Bouton de validation avec style
        validate_frame = tk.Frame(self.dh_table_frame, bg=COLORS['bg_white'])
        validate_frame.grid(row=n_joints+1, column=0, columnspan=6, pady=20)
        
        validate_btn = ModernButton(validate_frame,
                                   "✅ Valider les paramètres",
                                   self.validate_dh_params,
                                   bg_color=COLORS['success'],
                                   fg_color=COLORS['text_light'],
                                   width=200, height=45)
        validate_btn.pack()
        
    def get_param_description(self, param):
        """Retourne la description pédagogique d'un paramètre"""
        descriptions = {
            'theta': "Angle de rotation autour de l'axe Z (en degrés)",
            'd': "Translation le long de l'axe Z (en mètres)",
            'a': "Longueur du segment (en mètres)",
            'alpha': "Angle de torsion autour de l'axe X (en degrés)"
        }
        return descriptions.get(param, "")
        
    def create_tooltip(self, widget, text):
        """Crée une infobulle pour un widget"""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(tooltip, text=text,
                           background=COLORS['primary'],
                           foreground=COLORS['text_light'],
                           relief=tk.SOLID,
                           borderwidth=1,
                           font=('Arial', 9),
                           padx=10, pady=5)
            label.pack()
            
            widget.tooltip = tooltip
            
        def hide_tooltip(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                
        widget.bind('<Enter>', show_tooltip)
        widget.bind('<Leave>', hide_tooltip)
        
    def validate_dh_params(self):
        """Valide et récupère les paramètres DH saisis"""
        try:
            params = []
            for i, joint in enumerate(self.dh_entries):
                param = {
                    'theta': float(joint['theta'].get()),
                    'd': float(joint['d'].get()),
                    'a': float(joint['a'].get()),
                    'alpha': float(joint['alpha'].get()),
                    'type': 'R' if 'R' in joint['type'].get() else 'P'
                }
                params.append(param)
            
            # Message de succès stylisé
            success_msg = f"✅ Paramètres validés avec succès !\n\n"
            success_msg += f"🤖 Robot à {len(params)} articulation(s)\n\n"
            for i, p in enumerate(params, 1):
                success_msg += f"J{i}: θ={p['theta']}°, d={p['d']}m, "
                success_msg += f"a={p['a']}m, α={p['alpha']}°, Type={p['type']}\n"
            
            messagebox.showinfo("Succès", success_msg)
            
        except ValueError as e:
            messagebox.showerror("❌ Erreur de saisie",
                "Veuillez entrer des valeurs numériques valides\n"
                "pour tous les paramètres DH.")
    
    def create_visualization_section(self, parent):
        """Section de visualisation du robot - Version améliorée"""
        
        # Carte d'information
        info_card = tk.Frame(parent, bg=COLORS['accent'], relief=tk.FLAT)
        info_card.pack(fill=tk.X, pady=(0, 10))
        
        info_label = tk.Label(info_card,
            text="🎨 Visualisation 3D interactive de votre robot\n"
                 "La représentation apparaîtra après validation des paramètres",
            bg=COLORS['accent'],
            fg=COLORS['text_light'],
            font=('Arial', 9),
            justify=tk.CENTER)
        info_label.pack(padx=10, pady=10)
        
        # Zone de visualisation avec bordure
        viz_container = tk.Frame(parent, bg=COLORS['border'], relief=tk.FLAT, bd=2)
        viz_container.pack(fill=tk.BOTH, expand=True)
        
        self.viz_canvas = tk.Canvas(viz_container,
                                    bg=COLORS['bg_light'],
                                    highlightthickness=0)
        self.viz_canvas.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Placeholder avec instructions
        placeholder_text = "🤖\n\nVotre robot apparaîtra ici\n\n"
        placeholder_text += "1️⃣ Définissez les paramètres DH\n"
        placeholder_text += "2️⃣ Validez la configuration\n"
        placeholder_text += "3️⃣ Visualisez votre robot en 3D"
        
        self.viz_canvas.create_text(
            self.viz_canvas.winfo_reqwidth() // 2 + 200,
            self.viz_canvas.winfo_reqheight() // 2 + 150,
            text=placeholder_text,
            font=('Arial', 12),
            fill=COLORS['text_dark'],
            justify=tk.CENTER
        )
        
        # Contrôles de visualisation
        controls_frame = tk.Frame(parent, bg=COLORS['bg_white'])
        controls_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(controls_frame, text="🎮 Contrôles:",
                bg=COLORS['bg_white'],
                fg=COLORS['text_dark'],
                font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        ModernButton(controls_frame, "↻ Rotation",
                    lambda: None,
                    bg_color=COLORS['accent'],
                    fg_color=COLORS['text_light'],
                    width=100, height=30).pack(side=tk.LEFT, padx=5)
        
        ModernButton(controls_frame, "🔍 Zoom",
                    lambda: None,
                    bg_color=COLORS['accent'],
                    fg_color=COLORS['text_light'],
                    width=100, height=30).pack(side=tk.LEFT, padx=5)
        
        ModernButton(controls_frame, "🔄 Reset",
                    lambda: None,
                    bg_color=COLORS['accent'],
                    fg_color=COLORS['text_light'],
                    width=100, height=30).pack(side=tk.LEFT, padx=5)
        
    def create_results_section(self, parent):
        """Section d'affichage des résultats - Version améliorée"""
        
        # Carte d'information
        info_card = tk.Frame(parent, bg=COLORS['accent'], relief=tk.FLAT)
        info_card.pack(fill=tk.X, pady=(0, 10))
        
        info_label = tk.Label(info_card,
            text="📈 Résultats des calculs de modélisation\n"
                 "Sélectionnez un onglet pour voir les détails",
            bg=COLORS['accent'],
            fg=COLORS['text_light'],
            font=('Arial', 9),
            justify=tk.CENTER)
        info_label.pack(padx=10, pady=10)
        
        # Notebook pour organiser les différents résultats
        notebook = ttk.Notebook(parent, style='Modern.TNotebook')
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Onglet MGD
        mgd_frame = tk.Frame(notebook, bg=COLORS['bg_white'])
        notebook.add(mgd_frame, text="📐 MGD")
        self.create_result_tab(mgd_frame, "Modèle Géométrique Direct",
                              "Calcule la position de l'effecteur à partir des angles articulaires")
        
        # Onglet MGI
        mgi_frame = tk.Frame(notebook, bg=COLORS['bg_white'])
        notebook.add(mgi_frame, text="🔄 MGI")
        self.create_result_tab(mgi_frame, "Modèle Géométrique Inverse",
                              "Calcule les angles articulaires pour atteindre une position donnée")
        
        # Onglet Cinématique Directe
        mcd_frame = tk.Frame(notebook, bg=COLORS['bg_white'])
        notebook.add(mcd_frame, text="⚡ MCD")
        self.create_result_tab(mcd_frame, "Modèle Cinématique Direct",
                              "Calcule la vitesse de l'effecteur à partir des vitesses articulaires")
        
        # Onglet Cinématique Inverse
        mci_frame = tk.Frame(notebook, bg=COLORS['bg_white'])
        notebook.add(mci_frame, text="🎯 MCI")
        self.create_result_tab(mci_frame, "Modèle Cinématique Inverse",
                              "Calcule les vitesses articulaires pour une vitesse d'effecteur donnée")
        
    def create_result_tab(self, parent, title, description):
        """Crée un onglet de résultats - Version améliorée"""
        
        # En-tête de l'onglet
        header_frame = tk.Frame(parent, bg=COLORS['primary'])
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(header_frame,
                              text=title,
                              font=('Arial', 13, 'bold'),
                              bg=COLORS['primary'],
                              fg=COLORS['secondary'],
                              pady=10)
        title_label.pack()
        
        desc_label = tk.Label(header_frame,
                             text=description,
                             font=('Arial', 9),
                             bg=COLORS['primary'],
                             fg=COLORS['text_light'],
                             pady=5)
        desc_label.pack()
        
        # Zone de texte pour afficher les résultats
        text_frame = tk.Frame(parent, bg=COLORS['bg_white'])
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text = tk.Text(text_frame,
                      wrap=tk.WORD,
                      font=('Courier', 10),
                      bg=COLORS['bg_light'],
                      fg=COLORS['text_dark'],
                      relief=tk.FLAT,
                      padx=10,
                      pady=10)
        scrollbar = ttk.Scrollbar(text_frame, command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)
        
        # Texte placeholder
        placeholder = f"\n📋 Résultats du {title}\n\n"
        placeholder += "Les calculs apparaîtront ici après validation des paramètres.\n\n"
        placeholder += "💡 Astuce: Utilisez le menu ☰ en haut à droite pour lancer les calculs."
        
        text.insert('1.0', placeholder)
        text.configure(state='disabled')
        
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_footer(self):
        """Crée le pied de page"""
        footer = tk.Frame(self.root, bg=COLORS['primary'], height=40)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)
        
        footer_text = tk.Label(footer,
                              text="🎓 Projet d'Application 2025 - Centrale Nantes | "
                                   "Safa Bouzidi & Mohamadou Dia | "
                                   "Encadrants: V. Tourre & A. Chriette",
                              font=('Arial', 9),
                              bg=COLORS['primary'],
                              fg=COLORS['text_light'])
        footer_text.pack(expand=True)
        
    # === Méthodes du menu ===
    def new_robot(self):
        """Créer un nouveau robot"""
        response = messagebox.askyesno("Nouveau robot",
            "🤖 Créer un nouveau robot ?\n\n"
            "Cela réinitialisera tous les paramètres actuels.")
        if response:
            self.joint_count.set(3)
            self.update_dh_table()
            messagebox.showinfo("Succès", "✅ Nouveau robot créé !")
        
    def load_robot(self):
        """Charger un robot"""
        messagebox.showinfo("Charger un robot",
            "📂 Fonctionnalité de chargement\n\n"
            "Vous pourrez bientôt charger des configurations\n"
            "de robots sauvegardées.")
        
    def save_robot(self):
        """Sauvegarder le robot"""
        messagebox.showinfo("Sauvegarder",
            "💾 Fonctionnalité de sauvegarde\n\n"
            "Vous pourrez bientôt sauvegarder votre\n"
            "configuration de robot.")
        
    def calc_mgd(self):
        """Calculer MGD"""
        messagebox.showinfo("MGD",
            "📐 Modèle Géométrique Direct\n\n"
            "Calcul de la position et orientation de l'effecteur\n"
            "à partir des coordonnées articulaires.\n\n"
            "Résultats disponibles dans l'onglet MGD.")
        
    def calc_mgi(self):
        """Calculer MGI"""
        messagebox.showinfo("MGI",
            "🔄 Modèle Géométrique Inverse\n\n"
            "Calcul des coordonnées articulaires nécessaires\n"
            "pour atteindre une position donnée.\n\n"
            "Résultats disponibles dans l'onglet MGI.")
        
    def calc_mcd(self):
        """Calculer MCD"""
        messagebox.showinfo("MCD",
            "⚡ Modèle Cinématique Direct\n\n"
            "Calcul de la vitesse de l'effecteur\n"
            "à partir des vitesses articulaires.\n\n"
            "Résultats disponibles dans l'onglet MCD.")
        
    def calc_mci(self):
        """Calculer MCI"""
        messagebox.showinfo("MCI",
            "🎯 Modèle Cinématique Inverse\n\n"
            "Calcul des vitesses articulaires nécessaires\n"
            "pour obtenir une vitesse d'effecteur donnée.\n\n"
            "Résultats disponibles dans l'onglet MCI.")
        
    def show_help(self):
        """Afficher l'aide"""
        help_window = tk.Toplevel(self.root)
        help_window.title("📚 Documentation - Robot Modeler")
        help_window.geometry("600x500")
        help_window.configure(bg=COLORS['bg_white'])
        
        # En-tête
        header = tk.Frame(help_window, bg=COLORS['primary'])
        header.pack(fill=tk.X)
        
        tk.Label(header, text="📚 Guide d'utilisation",
                font=('Arial', 16, 'bold'),
                bg=COLORS['primary'],
                fg=COLORS['secondary'],
                pady=15).pack()
        
        # Contenu
        text_frame = tk.Frame(help_window, bg=COLORS['bg_white'])
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        help_text = """
🚀 DÉMARRAGE RAPIDE

1️⃣ Définir le nombre d'articulations
   • Utilisez le sélecteur pour choisir entre 1 et 6 articulations
   • Cliquez sur "Générer le tableau"

2️⃣ Remplir les paramètres DH
   • θ (theta): Angle de rotation autour de Z
   • d: Translation le long de Z
   • a: Longueur du segment
   • α (alpha): Angle de torsion autour de X
   • Type: R (Rotation) ou P (Prismatique)

3️⃣ Valider les paramètres
   • Cliquez sur "Valider les paramètres"
   • Vérifiez les valeurs dans le message de confirmation

4️⃣ Lancer les calculs
   • Utilisez le menu ☰ en haut à droite
   • Sélectionnez le type de calcul souhaité
   • Consultez les résultats dans les onglets

📐 PARAMÈTRES DENAVIT-HARTENBERG

Les paramètres DH permettent de décrire la géométrie
d'un robot manipulateur de manière systématique.

💡 ASTUCES

• Survolez les champs pour voir des infobulles
• Les valeurs sont en degrés pour les angles
• Les valeurs sont en mètres pour les distances
• Sauvegardez régulièrement votre configuration

❓ BESOIN D'AIDE ?

Consultez la documentation complète ou contactez
vos encadrants pour plus d'informations.
        """
        
        text = tk.Text(text_frame,
                      wrap=tk.WORD,
                      font=('Arial', 10),
                      bg=COLORS['bg_light'],
                      fg=COLORS['text_dark'],
                      relief=tk.FLAT,
                      padx=15,
                      pady=15)
        text.insert('1.0', help_text)
        text.configure(state='disabled')
        text.pack(fill=tk.BOTH, expand=True)
        
    def show_about(self):
        """Afficher À propos"""
        about_window = tk.Toplevel(self.root)
        about_window.title("ℹ️ À propos - Robot Modeler")
        about_window.geometry("500x400")
        about_window.configure(bg=COLORS['bg_white'])
        
        # Logo/Titre
        header = tk.Frame(about_window, bg=COLORS['primary'])
        header.pack(fill=tk.X)
        
        tk.Label(header, text="🤖",
                font=('Arial', 40),
                bg=COLORS['primary'],
                fg=COLORS['secondary'],
                pady=20).pack()
        
        tk.Label(header, text="ROBOT MODELER",
                font=('Arial', 18, 'bold'),
                bg=COLORS['primary'],
                fg=COLORS['secondary']).pack()
        
        tk.Label(header, text="Version 1.0",
                font=('Arial', 10),
                bg=COLORS['primary'],
                fg=COLORS['text_light'],
                pady=10).pack()
        
        # Informations
        info_frame = tk.Frame(about_window, bg=COLORS['bg_white'])
        info_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        about_text = """
🎓 PROJET D'APPLICATION 2025

👨‍💻 Développé par:
    • Safa Bouzidi
    • Mohamadou Dia

👨‍🏫 Encadrants:
    • M. Vincent Tourre
    • M. Abdelhamid Chriette

🏫 École Centrale de Nantes
    Option INFOSI

📅 Année 2025

🎯 Objectif:
Outil de modélisation et simulation
de robots manipulateurs utilisant
la convention Denavit-Hartenberg.
        """
        
        tk.Label(info_frame,
                text=about_text,
                font=('Arial', 10),
                bg=COLORS['bg_white'],
                fg=COLORS['text_dark'],
                justify=tk.LEFT).pack()
        
        # Bouton fermer
        ModernButton(about_window, "✅ Fermer",
                    about_window.destroy,
                    bg_color=COLORS['secondary'],
                    width=120, height=35).pack(pady=10)


# Point d'entrée
if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()