import os
import sys

# Configuration du path une seule fois
_current_dir = os.path.dirname(__file__)
_parent_dir = os.path.join(_current_dir, '..')
if _parent_dir not in sys.path:
    sys.path.append(_parent_dir)

# Imports communs
import tkinter as tk
from tkinter import ttk, messagebox

# Exports pour faciliter les imports
from Interface.style import COLORS, ModernButton
from Interface.geometry import DialogDefinition

__all__ = ['COLORS', 'ModernButton', 'DialogDefinition', 'tk', 'ttk', 'messagebox']

