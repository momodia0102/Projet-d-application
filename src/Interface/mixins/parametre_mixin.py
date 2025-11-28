from Interface import tk, ttk, messagebox, COLORS, ModernButton
from .base_mixin import BaseMixin

class ParameterMixin(BaseMixin):

     """Mixin pour la gestion des paramètres DH avec la validation """
    
     MIN_JOINTS = 1   
     MAX_JOINTS = 6
     DEFAULT_JOINTS = 3

     PARAM_DESCRIPTIONS = {
        'theta': "Angle de rotation autour de l'axe Z (en degrés)",
        'd': "Translation le long de l'axe Z (en mètres)",
        'r': "Longueur du segment (en mètres)",
        'alpha': "Angle de torsion autour de l'axe X (en degrés)"
     }
     
     DH_HEADERS = [
        ("🔗", "Joint"),
        ("🔄", "θ (deg)"),
        ("📏", "d (m)"),
        ("📐", "r (m)"),
        ("↻", "α (deg)"),
        ("⚙️", "Type")
     ]

     def create_dh_parameters_section(self, parent):

        """Section de saisie des paramètres DH"""
        
        # Info card réutilisable
        self.create_info_card(
            parent,
            "Les paramètres DH définissent la géométrie de votre robot.\n"
            "Commencez par choisir le nombre d'articulations !"
        )
        
        # Contrôles
        self._create_joint_controls(parent)
        
        # Séparateur
        self.create_separator(parent)
        
        # Table scrollable
        self._create_scrollable_table(parent)
        
        # Initialisation
        self.dh_entries = []
        self.update_dh_table()  
    
     def _create_joint_controls(self, parent):
        
        """Crée les contrôles du nombre d'articulations (méthode privée)"""
        control_frame = tk.Frame(parent, bg=COLORS['bg_white'])
        control_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            control_frame,
            text="🔢 Nombre d'articulations:",
            bg=COLORS['bg_white'],
            fg=COLORS['text_dark'],
            font=('Arial', 10, 'bold')
        ).pack(side=tk.LEFT, padx=5)
        
        # ✅ Variable d'instance initialisée proprement
        self.joint_count = tk.IntVar(value=self.DEFAULT_JOINTS)
        
        tk.Spinbox(
            control_frame,
            from_=self.MIN_JOINTS,
            to=self.MAX_JOINTS,
            textvariable=self.joint_count,
            width=8,
            font=('Arial', 12, 'bold'),
            bg=COLORS['bg_light'],
            fg=COLORS['primary']
        ).pack(side=tk.LEFT, padx=10)
        
        ModernButton(
            control_frame,
            "✨ Générer le tableau",
            self.update_dh_table,
            bg_color=COLORS['secondary'],
            width=160,
            height=35
        ).pack(side=tk.LEFT, padx=10)

     def _create_scrollable_table(self, parent):

        """Crée le conteneur scrollable pour le tableau DH"""
        canvas_frame = tk.Frame(parent, bg=COLORS['bg_white'])
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(canvas_frame, bg=COLORS['bg_white'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        
        self.dh_table_frame = tk.Frame(canvas, bg=COLORS['bg_white'])
        
        # ✅ Lambda évite les problèmes de référence
        self.dh_table_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.dh_table_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

     def update_dh_table(self):

        """Met à jour le tableau DH"""
        # Nettoyage
        for widget in self.dh_table_frame.winfo_children():
            widget.destroy()
        
        self.dh_entries = []
        n_joints = self.joint_count.get()
        
        # Créer en-têtes
        self._create_table_headers()
        
        # Créer lignes
        for i in range(n_joints):
            self._create_joint_row(i)
        
        # Bouton validation
        self._create_validation_button(n_joints)

     def _create_table_headers(self):

        """Crée les en-têtes du tableau (méthode privée)"""
        for col, (icon, header) in enumerate(self.DH_HEADERS):
            frame = tk.Frame(self.dh_table_frame, bg=COLORS['primary'])
            frame.grid(row=0, column=col, padx=0, pady=2, sticky='ew')
            
            tk.Label(
                frame,
                text=f"{icon}\n{header}",
                font=('Arial', 9, 'bold'),
                bg=COLORS['primary'],
                fg=COLORS['text_light'],
                pady=4
            ).pack(fill=tk.BOTH, expand=True)

     def _create_joint_row(self, joint_index):
        """Crée une ligne pour une articulation (méthode privée)"""
        joint_entries = {}
        row = joint_index + 1
        row_bg = COLORS['bg_light'] if joint_index % 2 == 0 else COLORS['bg_white']
        
        # Badge du joint
        self._create_joint_badge(row, row_bg, joint_index)
        
        # Champs de paramètres
        for col, param in enumerate(['theta', 'd', 'r', 'alpha'], start=1):
            entry = self._create_parameter_entry(row, col, row_bg, param)
            joint_entries[param] = entry
        
        # Combobox type
        joint_type = self._create_joint_type_selector(row, row_bg)
        joint_entries['type'] = joint_type
        
        self.dh_entries.append(joint_entries)

     def _create_joint_badge(self, row, bg_color, index):
        """Crée le badge d'identification du joint"""
        frame = tk.Frame(self.dh_table_frame, bg=bg_color)
        frame.grid(row=row, column=0, padx=0, pady=2, sticky='ew')
        
        tk.Label(
            frame,
            text=f"J{index + 1}",
            font=('Arial', 10, 'bold'),
            bg=COLORS['secondary'],
            fg=COLORS['text_dark'],
            width=4,
            pady=5
        ).pack(pady=5)

     def _create_parameter_entry(self, row, col, bg_color, param):
        """Crée un champ de saisie pour un paramètre"""
        frame = tk.Frame(self.dh_table_frame, bg=bg_color)
        frame.grid(row=row, column=col, padx=0, pady=2, sticky='ew')
        
        entry = tk.Entry(
            frame,
            width=10,
            font=('Arial', 10),
            bg=COLORS['bg_white'],
            justify=tk.CENTER
        )
        entry.pack(pady=5, padx=5)
        entry.insert(0, "0.0")
        
        # Tooltip
        self.create_tooltip(entry, self.PARAM_DESCRIPTIONS[param])
        
        return entry

     def _create_joint_type_selector(self, row, bg_color):

        """Crée le sélecteur de type d'articulation"""
        frame = tk.Frame(self.dh_table_frame, bg=bg_color)
        frame.grid(row=row, column=5, padx=2, pady=2, sticky='ew')
        
        combo = ttk.Combobox(
            frame,
            values=["R (Rotation)", "P (Prismatique)"],
            width=12,
            state="readonly",
            font=('Arial', 9)
        )
        combo.set("R (Rotation)")
        combo.pack(pady=5, padx=5)
        
        return combo
     
     def _create_validation_button(self, n_joints):

        """Crée le bouton de validation"""
        frame = tk.Frame(self.dh_table_frame, bg=COLORS['bg_white'])
        frame.grid(row=n_joints + 1, column=0, columnspan=6, pady=20)
        
        ModernButton(
            frame,
            "✅ Valider les paramètres",
            self.validate_dh_params,
            bg_color=COLORS['success'],
            fg_color=COLORS['text_light'],
            width=200,
            height=45
        ).pack() 

     def validate_dh_params(self):
        """Valide les paramètres DH avec gestion d'erreurs robuste"""
        try:
            params = self._extract_parameters()
            
            # ✅ Validation supplémentaire
            if not self._validate_parameters(params):
                return
            
            # Message de succès
            self.show_success("Succès", self._format_success_message(params))
            
        except ValueError as e:
            self.show_error(
                "Erreur de saisie",
                "Veuillez entrer des valeurs numériques valides"
            )
        except Exception as e:
            self.show_error("Erreur", f"Erreur inattendue: {e}")
    
     def _extract_parameters(self):
        """Extrait les paramètres des champs de saisie"""
        params = []
        for joint in self.dh_entries:
            param = {
                'theta': joint['theta'].get(),
                'd': joint['d'].get(),
                'r': joint['r'].get(),
                'alpha': joint['alpha'].get(),
                'type': 'R' if 'R' in joint['type'].get() else 'P'
            }
            params.append(param)
        return params

     def _validate_parameters(self, params):
        """Validation métier des paramètres"""
        # Ajoutez ici vos règles de validation
        # Exemple : vérifier que les valeurs sont dans des plages acceptables
        for i, param in enumerate(params):
            for key in ['theta', 'd', 'r', 'alpha']:
                try:
                    float(param[key])
                except ValueError:
                    # C'est une variable symbolique, c'est OK
                    pass
        return True
    
     def _format_success_message(self, params):
        """Formate le message de succès"""
        msg = f"Paramètres validés avec succès !\n\n"
        msg += f"🤖 Robot à {len(params)} articulation(s)\n\n"
        for i, p in enumerate(params, 1):
            msg += f"J{i}: θ={p['theta']}°, d={p['d']}m, "
            msg += f"a={p['r']}m, α={p['alpha']}°, Type={p['type']}\n"
        return msg