"""
Point d'entrée principal de l'application Robot Modeler
"""
import tkinter as tk
from Interface.main_windows import MainWindow


def main():
    """Lance l'application"""
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()