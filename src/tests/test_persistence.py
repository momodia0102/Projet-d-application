import pytest
import os
from server.robot import Robot
from outils import parfile, tools, samplerobots

def test_sauvegarde_nominale(tmp_path):
    """Test N°12 : Vérifie qu'un fichier .par est bien créé sur le disque"""
    dossier_temp = tmp_path / "test_robots"
    dossier_temp.mkdir()
    chemin_fichier = dossier_temp / "robot_test.par"

    r = Robot('RobotTest', NL=6, NJ=6, NF=6, structure=tools.SIMPLE)
    r.par_file_path = str(chemin_fichier) 
    
    parfile.writepar(r)

    assert chemin_fichier.exists(), "Le fichier .par n'a pas été créé !"
    assert chemin_fichier.stat().st_size > 0, "Le fichier est vide !"

def test_cycle_complet_sauvegarde_chargement(tmp_path):
    """Test N°13 : Sauvegarde un robot, le recharge et compare les données"""
    chemin_fichier = tmp_path / "cycle_test.par"
    
    original = Robot('CycleBot', NL=3, NJ=3, NF=3, structure=tools.SIMPLE)
    original.d[1] = 0.55  
    original.par_file_path = str(chemin_fichier)

    parfile.writepar(original)
    

    robot_charge, status = parfile.readpar('CycleBot', str(chemin_fichier))
    
    assert status == tools.OK
    assert robot_charge is not None
    assert robot_charge.name == 'CycleBot'
    assert robot_charge.nl == 3
    assert robot_charge.d[1] == 0.55 