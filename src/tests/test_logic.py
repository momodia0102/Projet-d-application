from sympy import Symbol
from server.robot import Robot
from outils import tools

def test_symboles_mathematiques():
    """Test N°17 : Vérifie que le robot accepte des variables (L1, q1) et pas juste des nombres"""
    r = Robot('SymBot', NL=2, NJ=2, NF=2)
    
    # Simulation : L'utilisateur entre "L1" dans la case 'd'
    # Votre interface ou le code convertit souvent les strings en symboles
    symbole = Symbol('L1')
    r.put_val(1, 'd', symbole)
    
    # Vérification que c'est bien stocké comme symbole mathématique
    valeur_stockee = r.get_val(1, 'd')
    assert isinstance(valeur_stockee, Symbol)
    assert str(valeur_stockee) == 'L1'

def test_limites_robot_minimal():
    """Test N°20 (Edge Case) : Un robot à 1 axe fonctionne-t-il ?"""
    # Créer un robot avec le minimum possible (1 lien, 1 joint)
    r = Robot('MiniBot', NL=1, NJ=1, NF=1, structure=tools.SIMPLE)
    
    # Vérifier que les tableaux internes sont correctement initialisés
    # Rappel : les tableaux ont souvent une taille N+1 pour inclure la base
    assert len(r.theta) >= 2 
    assert len(r.sigma) >= 2
    
    # Vérifier qu'on peut écrire dedans sans crash "IndexError"
    r.put_val(1, 'theta', 0.5)
    assert r.get_val(1, 'theta') == 0.5

def test_injection_valeur_incorrecte():
    """Test de robustesse : Que se passe-t-il si on met une clé invalide ?"""
    r = Robot('FailBot')
    
    # Essayer de mettre une valeur dans une colonne qui n'existe pas
    resultat = r.put_val(1, 'parametre_imaginaire', 10)
    
    # Selon votre code (src/server/robot.py), put_val ne plante pas mais ne fait rien
    # ou retourne FAIL (si implémenté). Vérifions juste que ça ne crashe pas l'appli.
    # Ici, on vérifie simplement que l'exécution continue.
    assert True