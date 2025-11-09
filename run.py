"""Script de lancement """
import sys
from pathlib import Path

# Ajouter src au path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

from src.main import main

if __name__ == "__main__":
    main()