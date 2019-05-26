#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""g3_interface_karaoke

(C) Matthieu Durand, 2018-2019

Interface graphique pour lecture karaoke.

TO DO: a peu pres tout
"""
import pyanote.controleur as cont
import pyanote.son as son

nom_fichier = 'fichiersMidi/Madness - Baggy Trousers.kar'
sortie_midi = son.connecter_sortie()
controleur = cont.creer_controleur(nom_fichier, midi = sortie_midi, kar = "un objet qu'il faudrait modifier pour affichage")
### Analyse pour recuperer toutes les infos karaoke
### En les connaissant à l'avance on peut afficher un paragraphe
controleur['vitesse'] = float('inf')
cont.demarrer(controleur)
print(controleur['mod_paroles/chanson'][0])
### Fin analyse
cont.reinitialiser_controleur(controleur)
print("=====================================")
print("Affichage des paroles au fil du temps")
print("=====================================")
cont.demarrer(controleur, True)




