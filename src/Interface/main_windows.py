"""
Fenêtre principale de l'application Robot Modeler
Centrale Nantes - 2025
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Interface.geometry import DialogDefinition
from server.robot import Robot
from server import geometry
from outils import filemgr, parfile, tools, configfile
from Interface.style import COLORS, ModernButton
from Interface.mixins.parametre_mixin import ParameterMixin
from Interface.mixins.resultat_mixin import ResultMixin
from Interface.mixins.visualization_mixin import VisualizationMixin


class MainWindow(ParameterMixin, VisualizationMixin, ResultMixin):
    """Fenêtre principale de l'application Robot Modeler"""
    
    def __init__(self, root):
        self.root = root
        self.robo = None
        self.sidebar_visible = False
        
        self._init_robot()
        self._setup_window()
        self._create_ui()

    def _init_robot(self):
        """Initialise le robot par défaut (RX90)"""
        try:
            from outils import samplerobots
            self.robo = samplerobots.rx90()
            self.robo.set_defaults(base=True, joint=True, geom=True)
        except Exception as e:
            print(f'❌ Erreur création robot: {e}')
            self.robo = Robot(name="MonRobot", NL=6, NJ=6, NF=6, structure="Simple")
            self.robo.set_defaults(base=True, joint=True, geom=True)

    def _setup_window(self):
        """Configure la fenêtre principale"""
        self.root.title("Robot Modeling 🤖 - Centrale Nantes")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        self.root.configure(bg=COLORS['bg_light'])
        self._center_window()
        self._setup_styles()

    def _center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.root.update_idletasks()
        w, h = self.root.winfo_width(), self.root.winfo_height()
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f'{w}x{h}+{x}+{y}')

    def _setup_styles(self):
        """Configure les styles ttk"""
        style = ttk.Style()
        style.theme_use('clam')
        
        styles_config = {
            'Modern.TLabelframe': {
                'background': COLORS['bg_white'],
                'borderwidth': 2,
                'relief': 'flat'
            },
            'Modern.TLabelframe.Label': {
                'background': COLORS['bg_white'],
                'foreground': COLORS['primary'],
                'font': ('Arial', 11, 'bold')
            },
            'Modern.TNotebook': {
                'background': COLORS['bg_white'],
                'borderwidth': 0
            },
            'Modern.TNotebook.Tab': {
                'background': COLORS['bg_light'],
                'foreground': COLORS['text_dark'],
                'padding': [20, 10],
                'font': ('Arial', 10, 'bold')
            }
        }
        
        for style_name, config in styles_config.items():
            style.configure(style_name, **config)
        
        style.map('Modern.TNotebook.Tab',
                 background=[('selected', COLORS['secondary'])],
                 foreground=[('selected', COLORS['text_dark'])])

    def _create_ui(self):
        """Crée l'interface utilisateur complète"""
        self._create_header()
        self._create_main_layout()
        self._create_footer()

    def _create_header(self):
        """Crée l'en-tête avec titre et menu"""
        header = tk.Frame(self.root, bg=COLORS['primary'], height=80)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)
        
        title_frame = tk.Frame(header, bg=COLORS['primary'])
        title_frame.pack(expand=True)
        
        tk.Label(title_frame, text="🤖 ROBOT MODELING",
                font=('Arial', 24, 'bold'),
                bg=COLORS['primary'],
                fg=COLORS['secondary']).pack(side=tk.LEFT, padx=10)
        
        tk.Label(title_frame, text="Modélisation de Robots Manipulateurs",
                font=('Arial', 12),
                bg=COLORS['primary'],
                fg=COLORS['text_light']).pack(side=tk.LEFT, padx=10)
        
        menu_btn = tk.Label(header, text="☰", font=('Arial', 20),
                           bg=COLORS['primary'], fg=COLORS['secondary'],
                           cursor='hand2')
        menu_btn.pack(side=tk.RIGHT, padx=20)
        menu_btn.bind('<Button-1>', lambda e: self._show_menu())

    def _show_menu(self):
        """Affiche le menu contextuel"""
        menu = tk.Menu(self.root, tearoff=0,
                      bg=COLORS['bg_white'],
                      fg=COLORS['text_dark'],
                      activebackground=COLORS['secondary'],
                      font=('Arial', 10))
        
        menu_items = [
            ("📁 Nouveau robot", self.new_robot),
            ("📂 Charger un robot", self.load_robot),
            ("💾 Sauvegarder", self.save_robot),
            None,
            ("🐍 Exporter MGD en Python", self.export_mgd_python),
            None,
            ("📐 Modèle Géométrique Direct", self.calculate_mgd),
            ("🔄 Modèle Géométrique Inverse", self._calc_mgi_stub),
            ("⚡ Modèle Cinématique Direct", self.calculate_mcd),
            ("🎯 Modèle Cinématique Inverse", self._calc_mci_stub),
            None,
            ("📚 Documentation", self._show_help),
            ("ℹ️ À propos", self._show_about),
            None,
            ("❌ Quitter", self.root.quit)
        ]
        
        for item in menu_items:
            if item is None:
                menu.add_separator()
            else:
                menu.add_command(label=item[0], command=item[1])
        
        try:
            menu.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery())
        finally:
            menu.grab_release()

    def _create_main_layout(self):
        """Crée la disposition principale"""
        main_container = tk.Frame(self.root, bg=COLORS['bg_light'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        self._create_sidebar(main_container)
        self._create_center_panel(main_container)

    def _create_sidebar(self, parent):
        """Crée la barre latérale"""
        self.sidebar_frame = tk.Frame(parent, bg=COLORS['bg_white'], width=380)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar_frame.pack_forget()
        
        sidebar_content = tk.Frame(self.sidebar_frame, bg=COLORS['bg_white'])
        sidebar_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ModernButton(sidebar_content, "✕ Fermer", self._toggle_sidebar,
                    bg_color=COLORS['error'], width=100, height=30
                    ).pack(anchor='ne', pady=(0, 10))
        
        tk.Label(sidebar_content, text="⚙️ Paramètres DH",
                font=('Arial', 14, 'bold'),
                bg=COLORS['bg_white'],
                fg=COLORS['primary']).pack(pady=(0, 10))
        
        self.create_dh_parameters_section(sidebar_content)
        self.create_joint_control_section(sidebar_content)

    def _create_center_panel(self, parent):
        """Crée le panneau central"""
        center = tk.Frame(parent, bg=COLORS['bg_light'])
        center.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self._create_action_buttons(center)
        self._create_paned_view(center)

    def _create_action_buttons(self, parent):
        """Crée les boutons d'action"""
        btn_frame = tk.Frame(parent, bg=COLORS['bg_light'])
        btn_frame.pack(fill=tk.X, pady=(0, 10))
        
        ModernButton(btn_frame, "📋 Voir paramètres robot", self._toggle_sidebar,
                    bg_color=COLORS['secondary'], width=200, height=40
                    ).pack(side=tk.LEFT)
        
        ModernButton(btn_frame, "🤖 Nouveau robot", self.new_robot,
                    bg_color=COLORS['accent'], width=150, height=40
                    ).pack(side=tk.LEFT, padx=10)

    def _create_paned_view(self, parent):
        """Crée la vue avec panneaux redimensionnables"""
        paned = tk.PanedWindow(parent, orient=tk.HORIZONTAL,
                              bg=COLORS['bg_light'], sashwidth=8, bd=0)
        paned.pack(fill=tk.BOTH, expand=True)
        
        viz_frame = ttk.LabelFrame(paned, text="👁️ Visualisation 3D du Robot",
                                  style='Modern.TLabelframe', padding=15)
        paned.add(viz_frame, minsize=500)
        self.create_visualization_section(viz_frame)
        
        result_frame = ttk.LabelFrame(paned, text="📊 Résultats",
                                     style='Modern.TLabelframe', padding=15)
        paned.add(result_frame, minsize=350)
        self.create_results_section(result_frame)

    def _create_footer(self):
        """Crée le pied de page"""
        footer = tk.Frame(self.root, bg=COLORS['primary'], height=40)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)
        
        tk.Label(footer,
                text="🎓 Projet d'Application 2025 - Centrale Nantes | "
                     "Safa Bouzidi & Mohamadou Dia | "
                     "Encadrants: V. Tourre & A. Chriette",
                font=('Arial', 9),
                bg=COLORS['primary'],
                fg=COLORS['text_light']).pack(expand=True)

    def _toggle_sidebar(self):
        """Affiche/masque la barre latérale"""
        if self.sidebar_visible:
            self.sidebar_frame.pack_forget()
            self.sidebar_visible = False
        else:
            self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y,
                                   before=self.sidebar_frame.master.winfo_children()[1])
            self.sidebar_visible = True

    def calculate_mgd(self):
        """Calcule le Modèle Géométrique Direct"""
        try:
            # Synchroniser DH si le tableau existe
            if hasattr(self, 'dh_entries') and self.dh_entries:
                self._sync_robot_from_dh()
            
            if not self.robo:
                messagebox.showerror("Erreur", "Aucun robot chargé")
                return
            
            frames = [(0, self.robo.NF - 1)]
            symo = geometry.direct_geometric(self.robo, frames, trig_subs=True)
            
            result_text = self._read_output(symo.file_out.name)
            self._display_result('mgd', "🔍 MODÈLE GÉOMÉTRIQUE DIRECT", result_text)
            
            if hasattr(self, 'renderer_3d') and self.renderer_3d:
                self.renderer_3d.load_robot(self.robo)
                self.update_joint_controls()
            
            messagebox.showinfo("Succès", "✅ MGD calculé et robot visualisé !")
            
        except Exception as e:
            print(f"❌ Erreur MGD: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erreur", f"Erreur lors du calcul MGD:\n{e}")

    def calculate_mcd(self):
        """Calcule le Modèle Cinématique Direct"""
        try:
            # Synchroniser DH si le tableau existe
            if hasattr(self, 'dh_entries') and self.dh_entries:
                self._sync_robot_from_dh()
            
            if not self.robo:
                messagebox.showerror("Erreur", "Aucun robot chargé.")
                return
            
            qdot = [0.5 if self.robo.sigma[j] == 0 else 0.1
                   for j in range(1, self.robo.NJ)]
            
            from server.geometry import direct_kinematic
            J, twist = direct_kinematic(self.robo, qdot)
            
            if J.shape[1] != len(qdot):
                raise ValueError(f"Incohérence dimensions: J={J.shape}, qdot={len(qdot)}")
            
            result_text = (
                f"Nombre d'articulations: {len(qdot)}\n\n"
                f"Vitesses articulaires q̇:\n{qdot}\n\n"
                f"Jacobien J(q):\n{J}\n\n"
                f"Twist (vitesse effecteur):\n{twist}\n"
            )
            
            self._display_result('mcd', "⚡ MODÈLE CINÉMATIQUE DIRECT", result_text)
            messagebox.showinfo("Succès", "✅ MCD calculé avec succès.")
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erreur", f"Erreur MCD:\n{e}")

    def _calc_mgi_stub(self):
        """Stub pour MGI (non implémenté)"""
        messagebox.showinfo("MGI",
            "🔄 Modèle Géométrique Inverse\n\n"
            "Fonctionnalité en développement.")

    def _calc_mci_stub(self):
        """Stub pour MCI (non implémenté)"""
        messagebox.showinfo("MCI",
            "🎯 Modèle Cinématique Inverse\n\n"
            "Fonctionnalité en développement.")

    def _read_output(self, file_path):
        """Lit le contenu d'un fichier"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"❌ Erreur lecture: {e}\n\nChemin: {file_path}"

    def _display_result(self, result_id, title, content):
        """Affiche un résultat dans un onglet"""
        formatted = f"{title}\n\n{'='*60}\n\n{content}"
        self.update_result(result_id, formatted)

    def _sync_robot_from_dh(self):
        """Synchronise le robot avec les paramètres DH saisis"""
        if not self.robo or not hasattr(self, 'dh_entries') or not self.dh_entries:
            return
        
        try:
            for i, joint in enumerate(self.dh_entries, 1):
                frame_idx = i
                
                # Récupérer les valeurs
                theta_val = self._parse_dh_value(joint['theta'].get())
                d_val = self._parse_dh_value(joint['d'].get())
                r_val = self._parse_dh_value(joint['r'].get())
                alpha_val = self._parse_dh_value(joint['alpha'].get())
                joint_type = joint['type'].get()
                
                # Mettre à jour le robot
                self.robo.put_val(frame_idx, 'theta', theta_val)
                self.robo.put_val(frame_idx, 'd', d_val)
                self.robo.put_val(frame_idx, 'r', r_val)
                self.robo.put_val(frame_idx, 'alpha', alpha_val)
                
                sigma = 0 if 'R' in joint_type else 1
                self.robo.put_val(frame_idx, 'sigma', sigma)
            
            print("✅ Paramètres DH synchronisés")
        except Exception as e:
            print(f"❌ Erreur synchronisation DH: {e}")
            raise

    def _parse_dh_value(self, value_str):
        """Parse une valeur DH (numérique ou symbolique)"""
        if not value_str or value_str.strip() == "":
            return 0.0
        
        value_str = value_str.strip()
        
        try:
            return float(value_str)
        except ValueError:
            return value_str

    def new_robot(self):
        """Crée un nouveau robot"""
        current = {
            'name': self.robo.name if self.robo else "MonRobot",
            'nl': self.robo.NL - 1 if self.robo else 6,
            'nj': self.robo.NJ - 1 if self.robo else 6,
            'structure': self.robo.structure if self.robo else "Simple",
            'floating': self.robo.is_floating if self.robo else False,
            'mobile': self.robo.is_mobile if self.robo else False
        }
        
        dialog = DialogDefinition(self.root,
                                 current_name=current['name'],
                                 current_nl=current['nl'],
                                 current_nj=current['nj'],
                                 current_structure=current['structure'],
                                 current_floating=current['floating'],
                                 current_mobile=current['mobile'])
        
        self.root.wait_window(dialog)
        result = dialog.get_values()
        
        if result:
            try:
                self.robo = Robot(
                    name=result['name'],
                    NL=result['num_links'],
                    NJ=result['num_joints'],
                    NF=result['num_frames'],
                    structure=result['structure'],
                    is_floating=result['is_floating'],
                    is_mobile=result['is_mobile']
                )
                
                self.robo.set_defaults(base=True, joint=True, geom=True)
                self.robo.directory = filemgr.get_folder_path(self.robo.name)
                
                self.joint_count.set(result['num_joints'])
                self.update_dh_table()
                
                messagebox.showinfo("Succès",
                    f"🤖 ROBOT CRÉÉ AVEC SUCCÈS !\n\n"
                    f"📝 Nom: {result['name']}\n"
                    f"🔗 Liens: {result['num_links']}\n"
                    f"🔄 Joints: {result['num_joints']}\n"
                    f"📐 Frames: {result['num_frames']}\n"
                    f"🏗️ Structure: {result['structure']}")
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur création robot:\n{e}")

    def load_robot(self):
        """Charge un robot depuis un fichier PAR"""
        try:
            default_dir = filemgr.get_base_path()
        except Exception:
            default_dir = None
        
        file_path = filedialog.askopenfilename(
            title="📂 Charger un robot SYMORO",
            initialdir=default_dir,
            filetypes=[("Fichiers SYMORO PAR", "*.par"), ("Tous les fichiers", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            robot_name = os.path.splitext(os.path.basename(file_path))[0]
            loaded_robot, flag = parfile.readpar(robot_name, file_path)
            
            if loaded_robot is None or flag == tools.FAIL:
                messagebox.showerror("Erreur",
                    f"Impossible de charger:\n{file_path}\n\n"
                    "Fichier corrompu ou incompatible.")
                return
            
            self.robo = loaded_robot
            self._refresh_after_load()
            
            messagebox.showinfo("Succès",
                f"✅ ROBOT CHARGÉ !\n\n"
                f"📝 Nom: {loaded_robot.name}\n"
                f"🔗 Liens: {loaded_robot.NL - 1}\n"
                f"🔄 Joints: {loaded_robot.NJ - 1}\n"
                f"📂 Fichier: {file_path}")
            
            try:
                configfile.set_last_robot(file_path)
            except Exception:
                pass
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur chargement:\n{e}")

    def _refresh_after_load(self):
        """Rafraîchit l'interface après chargement"""
        try:
            if hasattr(self, 'joint_count'):
                self.joint_count.set(self.robo.NJ - 1)
            if hasattr(self, 'update_dh_table'):
                self.update_dh_table()
            if hasattr(self, 'renderer_3d') and self.renderer_3d:
                self.renderer_3d.clear()
            if hasattr(self, 'joint_control_vars'):
                self.joint_control_vars = {}
        except Exception as e:
            print(f"⚠️ Erreur rafraîchissement: {e}")

    def save_robot(self):
        """Sauvegarde le robot dans un fichier PAR"""
        if not self.robo:
            messagebox.showerror("Erreur", "Aucun robot à sauvegarder.")
            return
        
        # Synchroniser DH si le tableau existe
        if hasattr(self, 'dh_entries') and self.dh_entries:
            try:
                self._sync_robot_from_dh()
            except Exception:
                pass
        
        default_filename = f"{filemgr.get_clean_name(self.robo.name)}.par"
        
        try:
            default_dir = self.robo.directory if hasattr(self.robo, 'directory') else filemgr.get_base_path()
        except Exception:
            default_dir = None
        
        file_path = filedialog.asksaveasfilename(
            title="💾 Sauvegarder le robot",
            initialdir=default_dir,
            initialfile=default_filename,
            defaultextension=".par",
            filetypes=[("Fichiers SYMORO PAR", "*.par"), ("Tous les fichiers", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            self.robo.par_file_path = file_path
            parfile.writepar(self.robo)
            
            messagebox.showinfo("Succès",
                f"✅ ROBOT SAUVEGARDÉ !\n\n"
                f"📝 Nom: {self.robo.name}\n"
                f"📂 Fichier: {file_path}")
            
            try:
                configfile.set_last_robot(file_path)
            except Exception:
                pass
                
        except PermissionError:
            messagebox.showerror("Erreur",
                f"Permission refusée:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur sauvegarde:\n{e}")

    def export_mgd_python(self):
        """Exporte le MGD en script Python"""
        if not self.robo:
            messagebox.showerror("Erreur", "Aucun robot chargé.")
            return
        
        # Synchroniser DH si le tableau existe
        if hasattr(self, 'dh_entries') and self.dh_entries:
            try:
                self._sync_robot_from_dh()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur synchronisation DH:\n{e}")
                return
        
        safe_name = self.robo.name.lower().replace(" ", "_")
        default_name = f"robot_{safe_name}.py"
        
        output_path = filedialog.asksaveasfilename(
            title="💾 Exporter le script Python",
            initialfile=default_name,
            defaultextension=".py",
            filetypes=[("Script Python", "*.py")]
        )
        
        if not output_path:
            return
        
        try:
            from exportation_python import generateur
            
            dh_table = [[self.robo.get_val(i, p) for p in ['theta', 'd', 'r', 'alpha']]
                       for i in range(1, self.robo.NJ)]
            
            sigmas = [self.robo.get_val(i, 'sigma') for i in range(1, self.robo.NJ)]
            
            constants = getattr(self.robo, 'constants', {})
            
            generator = generateur.RobotScriptGenerator(
                robot_name=self.robo.name,
                dh_table=dh_table,
                sigmas=sigmas,
                constants=constants
            )
            
            generator.generate(output_path)
            
            messagebox.showinfo("Succès",
                f"✅ Script généré !\n\n"
                f"📄 Fichier: {os.path.basename(output_path)}\n\n"
                f"Lancer avec:\n    python {os.path.basename(output_path)}")
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erreur", f"Échec export:\n{e}")

    def _show_help(self):
        """Affiche l'aide"""
        help_window = tk.Toplevel(self.root)
        help_window.title("📚 Documentation")
        help_window.geometry("600x500")
        help_window.configure(bg=COLORS['bg_white'])
        
        header = tk.Frame(help_window, bg=COLORS['primary'])
        header.pack(fill=tk.X)
        
        tk.Label(header, text="📚 Guide d'utilisation",
                font=('Arial', 16, 'bold'),
                bg=COLORS['primary'],
                fg=COLORS['secondary'],
                pady=15).pack()
        
        text_frame = tk.Frame(help_window, bg=COLORS['bg_white'])
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        help_text = """
🚀 DÉMARRAGE RAPIDE

1️⃣ Définir le nombre d'articulations
2️⃣ Remplir les paramètres DH
3️⃣ Valider les paramètres
4️⃣ Lancer les calculs via le menu ☰
        """
        
        text = tk.Text(text_frame, wrap=tk.WORD, font=('Arial', 10),
                      bg=COLORS['bg_light'], fg=COLORS['text_dark'],
                      relief=tk.FLAT, padx=15, pady=15)
        text.insert('1.0', help_text)
        text.configure(state='disabled')
        text.pack(fill=tk.BOTH, expand=True)

    def _show_about(self):
        """Affiche À propos"""
        about_window = tk.Toplevel(self.root)
        about_window.title("ℹ️ À propos")
        about_window.geometry("500x400")
        about_window.configure(bg=COLORS['bg_white'])
        
        header = tk.Frame(about_window, bg=COLORS['primary'])
        header.pack(fill=tk.X)
        
        tk.Label(header, text="🤖", font=('Arial', 40),
                bg=COLORS['primary'], fg=COLORS['secondary'],
                pady=20).pack()
        
        tk.Label(header, text="ROBOT MODELING", font=('Arial', 18, 'bold'),
                bg=COLORS['primary'], fg=COLORS['secondary']).pack()
        
        tk.Label(header, text="Version 1.0", font=('Arial', 10),
                bg=COLORS['primary'], fg=COLORS['text_light'],
                pady=10).pack()
        
        info_frame = tk.Frame(about_window, bg=COLORS['bg_white'])
        info_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        about_text = """
🎓 PROJET D'APPLICATION 2025

👨‍💻 Développeurs:
    • Safa Bouzidi
    • Mohamadou Dia

👨‍🏫 Encadrants:
    • M. Vincent Tourre
    • M. Abdelhamid Chriette

🏫 École Centrale de Nantes
    Option INFOSI
        """
        
        tk.Label(info_frame, text=about_text, font=('Arial', 10),
                bg=COLORS['bg_white'], fg=COLORS['text_dark'],
                justify=tk.LEFT).pack()
        
        ModernButton(about_window, "✅ Fermer", about_window.destroy,
                    bg_color=COLORS['secondary'],
                    width=120, height=35).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()