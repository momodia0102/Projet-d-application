import pytest
from sympy import pi, zeros, eye, Symbol
from server.robot import Robot
from outils import tools


def test_creation_robot_simple():
    """Vérifie qu'on peut créer un robot basique"""
    r = Robot('TestBot', NL=3, NJ=3, NF=3)
    
    assert r.name == 'TestBot'
    assert r.NL == 4  # NL+1
    assert r.NJ == 4  # NJ+1
    assert r.NF == 4  # NF+1


def test_robot_defaut_structure():
    """Vérifie que la structure par défaut est TREE"""
    r = Robot('Bot')
    assert r.structure == tools.TREE


def test_robot_theta_init():
    """Vérifie que theta est initialisé correctement"""
    r = Robot('Bot', NL=2, NJ=2, NF=2)
    
    assert len(r.theta) == 3  # NF+1
    assert r.theta[0] == 0  # Base toujours 0


def test_robot_sigma_init():
    """Vérifie que sigma (type joint) est initialisé"""
    r = Robot('Bot', NL=2, NJ=2, NF=2)
    
    assert len(r.sigma) == 3  # NF+1
    assert all(s in [0, 1, 2] for s in r.sigma)  # 0=R, 1=P, 2=Fixe


def test_robot_ant_init():
    """Vérifie que ant (antécédents) est bien une chaîne"""
    r = Robot('Bot', NL=3, NJ=3, NF=3)
    
    assert r.ant[0] == -1  # Base n'a pas d'antécédent
    assert r.ant[1] == 0   # J1 rattaché à la base
    assert r.ant[2] == 1   # J2 rattaché à J1


def test_put_get_theta():
    """Vérifie qu'on peut écrire/lire theta"""
    r = Robot('Bot', NL=2, NJ=2, NF=2)
    
    r.put_val(1, 'theta', 1.5)
    
    assert r.get_val(1, 'theta') == 1.5


def test_put_get_d():
    """Vérifie qu'on peut écrire/lire d"""
    r = Robot('Bot', NL=2, NJ=2, NF=2)
    
    r.put_val(1, 'd', 0.75)
    
    assert r.get_val(1, 'd') == 0.75


def test_put_get_alpha():
    """Vérifie qu'on peut écrire/lire alpha"""
    r = Robot('Bot', NL=2, NJ=2, NF=2)
    
    r.put_val(1, 'alpha', pi/2)
    
    assert r.get_val(1, 'alpha') == pi/2


def test_put_get_r():
    """Vérifie qu'on peut écrire/lire r"""
    r = Robot('Bot', NL=2, NJ=2, NF=2)
    
    r.put_val(1, 'r', 0.5)
    
    assert r.get_val(1, 'r') == 0.5


def test_put_get_sigma():
    """Vérifie qu'on peut modifier le type de joint"""
    r = Robot('Bot', NL=2, NJ=2, NF=2)
    
    r.put_val(1, 'sigma', 1)  # Prismatique
    
    assert r.get_val(1, 'sigma') == 1


def test_robot_avec_symbole():
    """Vérifie qu'on peut stocker des symboles SymPy"""
    r = Robot('Bot', NL=2, NJ=2, NF=2)
    
    L1 = Symbol('L1')
    r.put_val(1, 'd', L1)
    
    val = r.get_val(1, 'd')
    assert isinstance(val, Symbol)
    assert str(val) == 'L1'


def test_chain_simple():
    """Vérifie que chain() retourne la chaîne cinématique"""
    r = Robot('Bot', NL=3, NJ=3, NF=3)
    
    chain = r.chain(3, 0)
    
    assert 3 in chain
    assert 2 in chain
    assert 1 in chain
    assert 0 not in chain  # k n'est pas inclus


def test_common_root():
    """Vérifie qu'on trouve la racine commune"""
    r = Robot('Bot', NL=3, NJ=3, NF=3)
    
    root = r.common_root(2, 3)
    
    assert root >= 0  # Doit retourner un indice valide


def test_q_vec():
    """Vérifie qu'on génère le vecteur des variables articulaires"""
    r = Robot('Bot', NL=2, NJ=2, NF=2)
    r.sigma[1] = 0  # Rotation
    r.sigma[2] = 1  # Prismatique
    
    q = r.q_vec
    
    assert len(q) == 2


def test_robot_is_floating_false():
    """Vérifie que is_floating est False par défaut"""
    r = Robot('Bot')
    assert r.is_floating == False


def test_robot_is_mobile_false():
    """Vérifie que is_mobile est False par défaut"""
    r = Robot('Bot')
    assert r.is_mobile == False


def test_robot_avec_floating():
    """Vérifie qu'on peut créer un robot à base flottante"""
    r = Robot('FloatBot', is_floating=True)
    assert r.is_floating == True


def test_robot_avec_mobile():
    """Vérifie qu'on peut créer un robot mobile"""
    r = Robot('MobileBot', is_mobile=True)
    assert r.is_mobile == True
