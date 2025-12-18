"""Tests sur les robots d'exemple"""
from outils import samplerobots
import pytest
from sympy import pi, zeros, eye, Symbol
from server.robot import Robot
from outils import tools


def test_rx90_creation():
    """Vérifie qu'on peut créer un RX90"""
    rx90 = samplerobots.rx90()
    
    assert rx90 is not None
    assert rx90.name == 'RX90'


def test_rx90_nombre_joints():
    """Vérifie le nombre de joints du RX90"""
    rx90 = samplerobots.rx90()
    
    assert rx90.NJ == 7  # 6 joints + base


def test_planar2r_creation():
    """Vérifie qu'on peut créer un Planar2R"""
    p2r = samplerobots.planar2r()
    
    assert p2r is not None
    assert p2r.name == 'Planar2R'


def test_planar2r_nombre_joints():
    """Vérifie le nombre de joints du Planar2R"""
    p2r = samplerobots.planar2r()
    
    assert p2r.NJ == 3  # 2 joints + base


def test_cart_pole_creation():
    """Vérifie qu'on peut créer un Cart-Pole"""
    cp = samplerobots.cart_pole()
    
    assert cp is not None
    assert cp.name == 'CartPole'


def test_cart_pole_joints_types():
    """Vérifie les types de joints du Cart-Pole"""
    cp = samplerobots.cart_pole()
    
    assert cp.sigma[1] == 1  # Chariot = Prismatique
    assert cp.sigma[2] == 0  # Pendule = Rotation
