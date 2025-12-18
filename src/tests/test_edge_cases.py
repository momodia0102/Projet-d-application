import pytest
from sympy import pi, zeros, eye, Symbol
from server.robot import Robot
from outils import tools


def test_robot_1_joint():
    """Vérifie qu'un robot à 1 joint fonctionne"""
    r = Robot('Mini', NL=1, NJ=1, NF=1)
    
    assert r.NL == 2
    assert r.NJ == 2


def test_robot_max_joints():
    """Vérifie qu'on peut créer un robot avec beaucoup de joints"""
    r = Robot('BigBot', NL=10, NJ=10, NF=10)
    
    assert r.NL == 11
    assert len(r.theta) == 11


def test_put_val_index_zero():
    """Vérifie qu'on peut écrire à l'index 0 (base)"""
    r = Robot('Bot', NL=2, NJ=2, NF=2)
    
    result = r.put_val(0, 'theta', 0)
    
    # Doit réussir sans erreur
    assert result != tools.FAIL


def test_chain_meme_index():
    """Vérifie chain(i, i) retourne liste vide"""
    r = Robot('Bot', NL=3, NJ=3, NF=3)
    
    chain = r.chain(2, 2)
    
    assert chain == []


def test_robot_nom_vide():
    """Vérifie qu'on peut créer un robot sans nom"""
    r = Robot('', NL=2, NJ=2, NF=2)
    
    assert r.name == ''


def test_robot_nom_avec_espaces():
    """Vérifie qu'on peut avoir des espaces dans le nom"""
    r = Robot('Mon Super Robot', NL=2, NJ=2, NF=2)
    
    assert r.name == 'Mon Super Robot'

