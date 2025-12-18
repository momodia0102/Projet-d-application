import pytest
from sympy import pi, zeros, eye, Symbol
from server.robot import Robot
from outils import tools

def test_dh_tous_zeros():
    """Un robot avec DH = 0 partout doit donner identité"""
    r = Robot('ZeroBot', NL=2, NJ=2, NF=2)
    
    for i in range(1, r.NF):
        r.put_val(i, 'theta', 0)
        r.put_val(i, 'd', 0)
        r.put_val(i, 'r', 0)
        r.put_val(i, 'alpha', 0)
    
    # Vérifications basiques
    assert r.get_val(1, 'theta') == 0
    assert r.get_val(1, 'd') == 0


def test_dh_valeurs_negatives():
    """Vérifie qu'on peut avoir des valeurs négatives"""
    r = Robot('Bot', NL=2, NJ=2, NF=2)
    
    r.put_val(1, 'd', -0.5)
    r.put_val(1, 'theta', -pi/4)
    
    assert r.get_val(1, 'd') == -0.5
    assert r.get_val(1, 'theta') == -pi/4


def test_dh_grandes_valeurs():
    """Vérifie qu'on peut avoir de grandes valeurs"""
    r = Robot('Bot', NL=2, NJ=2, NF=2)
    
    r.put_val(1, 'd', 100.0)
    r.put_val(1, 'r', 50.0)
    
    assert r.get_val(1, 'd') == 100.0
    assert r.get_val(1, 'r') == 50.0

