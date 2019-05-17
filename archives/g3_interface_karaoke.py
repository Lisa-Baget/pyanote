#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""g3_interface_karaoke

(C) Matthieu Durand, 2018-2019

Interface graphique pour lecture karaoke.

TO DO: a peu pres tout
"""
import pyanote.controleur as cont
import pyanote.mod_temps_total as mtt
import pyanote.mod_karaoke as mkar


nom_fichier = 'fichiersMidi/Madness - Baggy Trousers.kar'
controleur = cont.creer_controleur(nom_fichier)
### Analyse pour recuperer toutes les infos karaoke
### En les connaissant à l'avance on peut afficher un paragraphe
mod1 = mtt.creer_modificateur_temps()
cont.ajouter_modificateur_controle(controleur, mod1)
mod2 = mkar.creer_modificateur_karaoke(None)
cont.ajouter_modificateur_controle(controleur, mod2)
controleur['vitesse'] = float('inf')
cont.demarrer(controleur)
print(controleur['paroles/chanson'][0])
### Fin analyse
cont.initialiser_valeurs_defaut(controleur)
# VERIFIER: pourquoi il faut enlever ces deux lignes?
#cont.ajouter_modificateur_controle(controleur, mod1)
#cont.ajouter_modificateur_controle(controleur, mod2)
print("=====================================")
print("Affichage des paroles au fil du temps")
print("=====================================")
cont.demarrer(controleur)



