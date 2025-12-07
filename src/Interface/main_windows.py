"""
Fenêtre principale de l'application Robot Modeler
Version améliorée - Design Centrale Nantes
"""
import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
from Interface.geometry import DialogDefinition
from server.robot import Robot
from server import geometry
from outils import filemgr, parfile, tools
from Interface.style import COLORS, ModernButton

from Interface.mixins.parametre_mixin import ParameterMixin
from Interface.mixins.resultat_mixin import ResultMixin
from Interface.mixins.visualization_mixin import VisualizationMixin

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))



class MainWindow(ParameterMixin, VisualizationMixin, ResultMixin):
    
    """Fenêtre principale de l'application - Version moderne"""
    
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_styles()
        self.create_header()
        self.create_main_layout()
        self.create_footer()

        self.robo = None
        self.sidebar_visible = False
        self.init_example_robot()
        

    def init_example_robot(self):
        """Initialiser ou charger un robot par défaut """
        try:
            from outils import configfile
            par_file_path = configfile.get_last_robot()

            if par_file_path and os.path.exists(par_file_path):
                robo_name = os.path.split(par_file_path)[1][:4]
                self.robo, flag = parfile.readpar(robo_name, par_file_path)
                if self.robo is None:
                    self.create_default_robot()
                else:
                    self.create_default_robot()

        except Exception as e:
            print(f"Erreur lors du chargement du robot: {e}")
            self.create_default_robot()

    def create_default_robot(self):
        """Créer un robot par défaut"""
        try:
            from outils import samplerobots
            self.robo = samplerobots.rx90()
            self.robo.set_defaults(base=True, joint = True ,geom=True)
        except Exception as e:
            print(f'Erreur création robot par défaut :{e}')
            self.robo = Robot( name ="MonRobot", NL=6, NJ=6, NF=6, structure="Série")
            self.robo.set_defaults(base=True, joint=True,geom=True)
    

    def calculate_mgd(self):
        """Calculer le modèle Géométrique Direct"""
        try:
            self.update_robo_from_dh()

            if not self.robo:
                messagebox.showerror("Erreur", "Aucun robot chargé")
                return
            
            nf = self.robo.NF
            frames = [(0, nf-1)]
            trig_subs = True

            # 1. Calculer le MGD (Pour affichage textuel)
            symo = geometry.direct_geometric(self.robo, frames, trig_subs)

            # 2. Afficher les résultats
            output_file = symo.file_out.name
            result_text = self.read_output(output_file)
            
            # 🆕 Utiliser la méthode du mixin ResultMixin
            self.display_mgd_result(result_text)

            # 🎯 3. VISUALISATION (Approche Directe SYMORO)
            if hasattr(self, 'renderer_3d') and self.renderer_3d:
                # A. Charger la hiérarchie du robot
                self.renderer_3d.load_robot(self.robo)
                
                # B. Initialiser les contrôles (Sliders)
                self.update_joint_controls()
            else:
                print("⚠️ Renderer 3D non disponible")

            messagebox.showinfo("Succès", f"✅ MGD calculé et robot visualisé !")

        except Exception as e:
            print(f"❌ Erreur calcul MGD: {e}")
            import traceback
            traceback.print_exc() 
            messagebox.showerror("Erreur", f"Erreur lors du calcul MGD: {e}")

    def read_output(self, file_path):
        """Lire le contenu du fichier de Sortie"""
        try:
            with open(file_path, 'r' , encoding='utf-8')as f :
                content = f.read()
            return content
        except Exception as e:
            return  f"❌ Erreur lecture fichier: {e}\n\nChemin: {file_path}"

    def display_mgd_result(self, result_text):
        """Affiche le résultat MGD"""
        formatted_result = (
            "🔍 Les  RÉSULTATS DU MODÈLE GÉOMÉTRIQUE DIRECT\n\n"
            f"{'='*60}\n\n"
            f"{result_text}"
        )
        self.update_result('mgd', formatted_result)
    
    def display_mgi_result(self, result_text):
        """Affiche le résultat MGI"""
        self.update_result('mgi', f"🔄 MGI\n\n{result_text}")
    
    def display_mcd_result(self, result_text):
        """Affiche le résultat MCD"""
        self.update_result('mcd', f"⚡ MCD\n\n{result_text}")
    
    def display_mci_result(self, result_text):
        """Affiche le résultat MCI"""
        self.update_result('mci', f"🎯 MCI\n\n{result_text}")


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
        
    def toggle_sidebar(self):
        """Affiche/masque la sidebar"""
        if self.sidebar_visible:
            self.sidebar_frame.pack_forget()
            self.sidebar_visible = False
        else:
            self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, before=self.sidebar_frame.master.winfo_children()[1])
            self.sidebar_visible = True

    def create_main_layout(self):
        """Crée la disposition principale avec sidebar coulissante"""
        
        # Conteneur principal
        main_container = tk.Frame(self.root, bg=COLORS['bg_light'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # === SIDEBAR COULISSANTE (masquée par défaut) ===
        self.sidebar_frame = tk.Frame(main_container, bg=COLORS['bg_white'], width=380)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar_frame.pack_forget()  # Masquer au départ
        
        # Contenu de la sidebar
        sidebar_content = tk.Frame(self.sidebar_frame, bg=COLORS['bg_white'])
        sidebar_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Bouton fermer en haut
        close_btn = ModernButton(
            sidebar_content,
            "✕ Fermer",
            self.toggle_sidebar,
            bg_color=COLORS['error'],
            width=100,
            height=30
        )
        close_btn.pack(anchor='ne', pady=(0, 10))
        
        # Titre sidebar
        tk.Label(
            sidebar_content,
            text="⚙️ Paramètres DH",
            font=('Arial', 14, 'bold'),
            bg=COLORS['bg_white'],
            fg=COLORS['primary']
        ).pack(pady=(0, 10))
        
        # Section DH compacte
        self.create_dh_parameters_section(sidebar_content)
        self.create_joint_control_section(sidebar_content)
        
        # === ZONE CENTRALE (toujours visible) ===
        center_container = tk.Frame(main_container, bg=COLORS['bg_light'])
        center_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Bouton pour ouvrir la sidebar
        btn_frame = tk.Frame(center_container, bg=COLORS['bg_light'])
        btn_frame.pack(fill=tk.X, pady=(0, 10))
        
        ModernButton(
            btn_frame,
            "📋 Voir paramètres robot",
            self.toggle_sidebar,
            bg_color=COLORS['secondary'],
            width=200,
            height=40
        ).pack(side=tk.LEFT)
        
        ModernButton(
            btn_frame,
            "🤖 Nouveau robot",
            self.new_robot,
            bg_color=COLORS['accent'],
            width=150,
            height=40
        ).pack(side=tk.LEFT, padx=10)
        
        # PanedWindow pour Visualisation et Résultats
        paned = tk.PanedWindow(
            center_container,
            orient=tk.HORIZONTAL,
            bg=COLORS['bg_light'],
            sashwidth=8,
            bd=0
        )
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Zone Visualisation (plus grande)
        viz_frame = ttk.LabelFrame(
            paned,
            text="👁️ Visualisation 3D du Robot",
            style='Modern.TLabelframe',
            padding=15
        )
        paned.add(viz_frame, minsize=500)
        self.create_visualization_section(viz_frame)
        
        # Zone Résultats (moyenne)
        result_frame = ttk.LabelFrame(
            paned,
            text="📊 Résultats",
            style='Modern.TLabelframe',
            padding=15
        )
        paned.add(result_frame, minsize=350)
        self.create_results_section(result_frame)

      
    
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
  
       
    def update_robo_from_dh(self):
            """Mettre à jour le robot avec les paramètres DH saisis"""
            if not self.robo or not self.dh_entries:
                return
            
            try:
                for i, joint in enumerate(self.dh_entries, 1):
                    frame_idx = i
                    
                    # Récupérer les valeurs (numériques ou symboliques)
                    theta_val = self.parse_dh_value(joint['theta'].get())
                    d_val = self.parse_dh_value(joint['d'].get())
                    a_val = self.parse_dh_value(joint['r'].get())
                    alpha_val = self.parse_dh_value(joint['alpha'].get())
                    joint_type = joint['type'].get()

                    self.robo.put_val(frame_idx, 'theta', theta_val)
                    self.robo.put_val(frame_idx, 'd', d_val)
                    self.robo.put_val(frame_idx, 'r', a_val)
                    self.robo.put_val(frame_idx, 'alpha', alpha_val)

                    sigma = 0 if 'R' in joint_type else 1
                    self.robo.put_val(frame_idx, 'sigma', sigma)

                print("✅ Paramètres DH synchronisés avec le robot ")
            except Exception as e:
                print(f"❌ Erreur synchronisation DH: {e}")
                messagebox.showerror("Erreur", f"Erreur lors de la synchronisation des paramètres: {e}")
        
    def parse_dh_value(self, value_str):
        """Parse une valeur DH : numérique ou symbolique"""
        if not value_str or value_str.strip() == "":
            return 0.0
        
        value_str = value_str.strip()
        
        # Essayer de convertir en nombre
        try:
            return float(value_str)
        except ValueError:
            # Si ce n'est pas un nombre, retourner la chaîne (variable symbolique)
            return value_str
        
  


  
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
        
    def new_robot(self):
        """Créer un nouveau robot avec formulaire détaillé"""
        # Ouvrir le dialog de création de robot
        current_name = self.robo.name if self.robo else "MonRobot"
        current_nl = self.robo.NL if self.robo else 6
        current_nj = self.robo.NJ if self.robo else 6
        current_structure = self.robo.structure if self.robo else "Série"
        current_floating = self.robo.is_floating if self.robo else False
        current_mobile = self.robo.is_mobile if self.robo else False
        
        dialog = DialogDefinition(
            self.root, 
            current_name=current_name,
            current_nl=current_nl,
            current_nj=current_nj,
            current_structure=current_structure,
            current_floating=current_floating,
            current_mobile=current_mobile
        )
        
        # Attendre la fermeture du dialog
        self.root.wait_window(dialog)
        
        # Récupérer les résultats
        result = dialog.get_values()
        
        if result:
            try:
                # Créer le nouveau robot SYMORO
                new_robo = Robot(
                    name=result['name'],
                    NL=result['num_links'],
                    NJ=result['num_joints'],
                    NF=result['num_frames'],
                    structure=result['structure'],
                    is_floating=result['is_floating'],
                    is_mobile=result['is_mobile']
                )
                
                # Appliquer les paramètres par défaut
                new_robo.set_defaults(base=True, joint=True, geom=True)
                
                # Copier les paramètres existants si demandé
                #if self.robo and result['keep_geo']:
                    #nf = min(self.robo.NF, new_robo.NF)
                    # Copier les paramètres géométriques...
                    #pass
                    
                self.robo = new_robo
                self.robo.directory = filemgr.get_folder_path(self.robo.name)
                
                # Mettre à jour l'interface
                self.joint_count.set(result['num_joints'])
                self.update_dh_table()
                
                # Message de succès
                success_msg = f"🤖 NOUVEAU ROBOT CRÉÉ AVEC SUCCÈS !\n\n"
                success_msg += f"📝 Nom: {result['name']}\n"
                success_msg += f"🔗 Liens: {result['num_links']}\n"
                success_msg += f"🔄 Joints: {result['num_joints']}\n"
                success_msg += f"📐 Frames: {result['num_frames']}\n"
                success_msg += f"🏗️ Structure: {result['structure']}\n"
                success_msg += f"🌊 Base flottante: {'Oui' if result['is_floating'] else 'Non'}\n"
                success_msg += f"🚗 Robot mobile: {'Oui' if result['is_mobile'] else 'Non'}\n\n"
                success_msg += "✅ Le robot a été configuré avec SYMORO."
                
                messagebox.showinfo("Succès", success_msg)
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la création du robot: {e}")

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
        """Calculer MGD """
        self.calculate_mgd()
        
    def calc_mgi(self):
        """Calculer MGI"""
        messagebox.showinfo("MGI",
            "🔄 Modèle Géométrique Inverse\n\n"
            "Calcul des coordonnées articulaires nécessaires\n"
            "pour atteindre une position donnée.\n\n"
            "Résultats disponibles dans l'onglet MGI(voir menu).")
        
    def calc_mcd(self):
        """Calculer MCD"""
        self.calculate_mcd()
        
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