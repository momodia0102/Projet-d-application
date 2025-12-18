import pytest
from sympy import pi, zeros, eye, Symbol
from server.robot import Robot
from outils import tools
from outils import samplerobots


def test_creation_et_modification():
    """Test complet : créer + modifier + lire"""
    r = Robot('Test', NL=2, NJ=2, NF=2)
    
    # Modifier
    r.put_val(1, 'theta', pi/4)
    r.put_val(1, 'd', 0.5)
    r.put_val(1, 'sigma', 0)
    
    # Lire
    assert r.get_val(1, 'theta') == pi/4
    assert r.get_val(1, 'd') == 0.5
    assert r.get_val(1, 'sigma') == 0


def test_robot_complet_rx90():
    """Test complet sur RX90"""
    rx90 = samplerobots.rx90()
    
    # Vérifications multiples
    assert rx90.name == 'RX90'
    assert rx90.NJ == 7
    assert rx90.structure == tools.SIMPLE
    assert rx90.is_floating == False


def test_get_q_rotation():
    """Vérifie get_q pour joint rotatif"""
    r = Robot('Bot', NL=2, NJ=2, NF=2)
    r.sigma[1] = 0  # Rotation
    
    q = r.get_q(1)
    
    assert q == r.theta[1]


def test_get_q_prismatique():
    """Vérifie get_q pour joint prismatique"""
    r = Robot('Bot', NL=2, NJ=2, NF=2)
    r.sigma[1] = 1  # Prismatique
    
    q = r.get_q(1)
    
    assert q == r.r[1]


def test_get_q_fixe():
    """Vérifie get_q pour joint fixe"""
    r = Robot('Bot', NL=2, NJ=2, NF=2)
    r.sigma[1] = 2  # Fixe
    
    q = r.get_q(1)
    
    assert q == 0