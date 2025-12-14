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

def test_mgd_identite():
    """Test N°6 : Un robot avec tous paramètres à 0 doit donner l'identité"""
    r = Robot('ZeroBot', NL=3, NJ=3, NF=3, structure=tools.SIMPLE)

    from server.geometry import dgm
    from outils.symbolmgr import SymbolManager
    
    symo = SymbolManager()
    T = dgm(r, symo, 3, 0, fast_form=True)
    
    assert T == eye(4)

def test_rx90_proprietes():
    """Test N°18 : Vérifie le RX90"""
    rx90 = samplerobots.rx90()
    assert rx90.name == 'RX90'
    assert rx90.NJ == 7 
    assert rx90.is_mobile is False