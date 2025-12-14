from sympy import Symbol
from server.robot import Robot
from outils import tools

def test_symboles_mathematiques():
    """Test N°17 : Vérifie que le robot accepte des variables (L1, q1) et pas juste des nombres"""
    r = Robot('SymBot', NL=2, NJ=2, NF=2)
    
    symbole = Symbol('L1')
    r.put_val(1, 'd', symbole)
    
    valeur_stockee = r.get_val(1, 'd')
    assert isinstance(valeur_stockee, Symbol)
    assert str(valeur_stockee) == 'L1'

def test_limites_robot_minimal():
    """Test N°20 (Edge Case) : Un robot à 1 axe fonctionne-t-il ?"""
    r = Robot('MiniBot', NL=1, NJ=1, NF=1, structure=tools.SIMPLE)
    
    assert len(r.theta) >= 2 
    assert len(r.sigma) >= 2
    
    r.put_val(1, 'theta', 0.5)
    assert r.get_val(1, 'theta') == 0.5

def test_injection_valeur_incorrecte():
    """Test de robustesse : Que se passe-t-il si on met une clé invalide ?"""
    r = Robot('FailBot')
    
    resultat = r.put_val(1, 'parametre_imaginaire', 10)
    

    assert True