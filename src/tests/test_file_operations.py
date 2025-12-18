from outils import filemgr
import os


def test_get_clean_name():
    """Vérifie le nettoyage des noms"""
    assert filemgr.get_clean_name("Mon Robot") == "mon-robot"
    assert filemgr.get_clean_name("RX90") == "rx90"
    assert filemgr.get_clean_name("ROBOT_TEST") == "robot_test"


def test_get_clean_name_avec_espaces():
    """Vérifie le remplacement des espaces"""
    name = filemgr.get_clean_name("Test Robot 2025")
    assert " " not in name
    assert name == "test-robot-2025"


def test_get_clean_name_underscore():
    """Vérifie qu'on peut remplacer par underscore"""
    name = filemgr.get_clean_name("Test Robot", char='_')
    assert name == "test_robot"


def test_base_path_existe():
    """Vérifie que get_base_path retourne un Path"""
    from pathlib import Path
    path = filemgr.get_base_path()
    assert isinstance(path, Path)