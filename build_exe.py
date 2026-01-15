#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de création d'un exécutable Windows pour Robot Modeler
Optimisé pour Python 3.11 + PyInstaller
"""

import PyInstaller.__main__
import sys
from pathlib import Path


# ================== CONFIGURATION ==================

APP_NAME = "RobotModeler"
DEBUG = True        # 🔁 False pour build final
ONEFILE = False     # 🔁 True pour .exe unique (final)

# ===================================================


def build_exe():
    base_dir = Path(__file__).resolve().parent
    src_dir = base_dir / "src"
    main_script = src_dir / "main.py"

    if not main_script.exists():
        print(f"❌ Erreur: {main_script} introuvable")
        sys.exit(1)

    pyinstaller_args = [
        str(main_script),

        f"--name={APP_NAME}",

        # === MODE ===
        "--onedir" if not ONEFILE else "--onefile",

        # === INTERFACE ===
        "--console" if DEBUG else "--windowed",

        # === DONNÉES ===
        # À utiliser seulement si tu as des fichiers non .py
        # f"--add-data={src_dir};src",

        # === IMPORTS DIFFICILES ===
        "--hidden-import=OpenGL",
        "--hidden-import=OpenGL.GL",
        "--hidden-import=OpenGL.GLU",
        "--hidden-import=pyopengltk",

        # === MATPLOTLIB BACKENDS ===
        "--hidden-import=matplotlib.backends.backend_tkagg",
        "--hidden-import=matplotlib.backends.backend_agg",

        # === NETTOYAGE ===
        "--clean",
        "--noconfirm",

        # === DOSSIERS ===
        "--distpath=dist",
        "--workpath=build",
        "--specpath=.",
    ]

    print("🚀 PyInstaller – Build RobotModeler")
    print(f"📦 Mode      : {'ONEFILE' if ONEFILE else 'ONEDIR'}")
    print(f"🐞 Debug     : {'ON' if DEBUG else 'OFF'}")
    print("-" * 60)

    PyInstaller.__main__.run(pyinstaller_args)

    print("\n✅ BUILD TERMINÉ")
    print(f"📁 Sortie : {base_dir / 'dist'}")


if __name__ == "__main__":
    build_exe()
