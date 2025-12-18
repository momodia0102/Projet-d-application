"""Tests sur les utilitaires"""
import pytest
from sympy import pi, zeros, eye, Symbol
from server.robot import Robot
from outils import tools
from outils import tools
from sympy import Matrix


def test_skew_matrix():
    """Vérifie la matrice antisymétrique"""
    v = Matrix([1, 2, 3])
    S = tools.skew(v)
    
    assert S.shape == (3, 3)
    assert S[0, 0] == 0
    assert S[0, 1] == -3
    assert S[0, 2] == 2


def test_skew_zeros():
    """Vérifie skew du vecteur nul"""
    v = Matrix([0, 0, 0])
    S = tools.skew(v)
    
    assert S == Matrix([[0, 0, 0], [0, 0, 0], [0, 0, 0]])


def test_constants():
    """Vérifie les constantes de base"""
    assert tools.ZERO == 0
    assert tools.ONE == 1
    assert tools.FAIL == 1
    assert tools.OK == 0


def test_structure_types():
    """Vérifie les types de structure"""
    assert tools.SIMPLE in tools.TYPES
    assert tools.TREE in tools.TYPES
    assert tools.CLOSED_LOOP in tools.TYPES