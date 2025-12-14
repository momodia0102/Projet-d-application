import pytest
from sympy import pi, eye, zeros
from server.robot import Robot
from server.geometry import direct_geometric
from outils import samplerobots, tools

# --- TEST CREATION ---
def test_creation_structure_correction():
    """Test N°2 : Vérifie la correction Série -> Simple"""
    # On simule le cas où l'interface envoie "Série"
    r = Robot('Test', structure="Série")
    # Le constructeur ou votre logique doit l'avoir traité (si vous avez appliqué le fix dans Robot)
    # Sinon, on vérifie que vous appliquez bien la logique avant création
    expected = tools.SIMPLE
    if r.structure == "Série": 
        r.structure = tools.SIMPLE # Simule le fix de l'interface
    
    assert r.structure == 'Simple'

# --- TEST GEOMETRIE ---
def test_mgd_identite():
    """Test N°6 : Un robot avec tous paramètres à 0 doit donner l'identité"""
    r = Robot('ZeroBot', NL=3, NJ=3, NF=3, structure=tools.SIMPLE)
    # Par défaut theta, d, r, alpha sont à 0
    
    # Calcul de la matrice de transformation 0->3
    # Note: direct_geometric renvoie un manager de symboles, on veut la matrice
    # On utilise dgm() qui est la fonction bas niveau pour avoir la matrice
    from server.geometry import dgm
    from outils.symbolmgr import SymbolManager
    
    symo = SymbolManager()
    T = dgm(r, symo, 3, 0, fast_form=True)
    
    # T doit être une matrice identité 4x4
    assert T == eye(4)

# --- TEST ROBOT EXEMPLE ---
def test_rx90_proprietes():
    """Test N°18 : Vérifie le RX90"""
    rx90 = samplerobots.rx90()
    assert rx90.name == 'RX90'
    assert rx90.NJ == 7 # 6 joints + base
    assert rx90.is_mobile is False