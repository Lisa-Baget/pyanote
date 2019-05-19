#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pyanote.mod_temps_total

(C) Lisa Baget, 2018-2019

Ce module définit un modificateur de controleur permettant de calculer
le temps écoulé depuis le début de la chanson.
"""

def creer_modificateur_temps():
    ''' Ce modificateur permet de calculer le temps écoulé depuis le début de la chanson.
    '''
    return {'nom' : 'mod_temps_total',
            'init' : {'temps_total': 0, 'temps/chanson': {}},
            'prerequis' : [],
            'fonctions' : {
                'mod_delta_temps': ajouter_temps,
                'mod_prochaine_chanson' : enregistrement_temps}}

def ajouter_temps(controleur, ticks, micros):
    controleur['temps_total'] = controleur['temps_total'] + micros

def enregistrement_temps(controleur):
    controleur['temps/chanson'][controleur['index_chanson']] = controleur['temps_total']
    controleur['temps_total'] = 0
    
if __name__ == '__main__':
    import pyanote.controleur as cont
    nom_fichier = 'fichiersMidi/Dave Brubeck - Take Five.mid'
    controleur = cont.creer_controleur(nom_fichier)
    modificateur = creer_modificateur_temps()
    cont.ajouter_modificateur_controle(controleur, modificateur)
    controleur['vitesse'] = float('inf')
    cont.demarrer(controleur)
    print("Durées en micros", controleur['temps/chanson'])