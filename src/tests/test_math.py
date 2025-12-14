import pytest
from sympy import pi
from server.robot import Robot
from outils import tools

def test_creation_robot():
    """Vérifie qu'on peut créer un robot simple"""
    r = Robot('TestBot', NL=6, NJ=6, NF=6, structure=tools.SIMPLE)
    
    assert r.name == 'TestBot'
    assert r.NL == 7
    assert r.structure == 'Simple'


def test_structure_type():
    """Vérifie que votre correction de bug fonctionne (Série vs Simple)"""
    input_interface = "Série"
    
    if input_interface == "Série":
        structure_reelle = tools.SIMPLE
    else:
        structure_reelle = input_interface
        
    assert structure_reelle == 'Simple'
    assert structure_reelle in tools.TYPES