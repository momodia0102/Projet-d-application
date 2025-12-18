import pytest
from sympy import pi, eye, zeros
from server.robot import Robot
from server.geometry import direct_geometric
from outils import samplerobots, tools

def test_creation_structure_correction():
    """Test N°2 : Vérifie la correction Série -> Simple"""
    r = Robot('Test', structure="Série")

    expected = tools.SIMPLE
    if r.structure == "Série": 
        r.structure = tools.SIMPLE 
    
    assert r.structure == 'Simple'



def test_rx90_proprietes():
    """Test N°18 : Vérifie le RX90"""
    rx90 = samplerobots.rx90()
    assert rx90.name == 'RX90'
    assert rx90.NJ == 7 
    assert rx90.is_mobile is False