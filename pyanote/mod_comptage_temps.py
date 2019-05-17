#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pyanote.mod_comptage_temps

(C) Lisa Baget, 2018-2019 <li.baget@laposte.net>

Ce module définit un modificateur de controleur permettant de jouer les
notes dans une sortie Midi.
"""
from math import floor

def creer_modificateur_comptage(horloge, defilement):
    ''' Ce modificateur sert à  lier les messages controle et les messages systeme à une sortie MIDI.
    '''
    return {'nom' : 'mod_midi',
            'init' : {'derniere_seconde' : 0, 'interf_horloge': horloge, 'interf_defilement': defilement},
            'prerequis' : ['mod_temps_total'],
            'fonctions' : {
                'mod_delta_temps' : traiter_changement_temps}}

def traiter_changement_temps(controleur, ticks, micros):
    nouveau_secondes = floor(controleur['temps_total'] // 10**6)
    if nouveau_secondes > controleur['derniere_seconde']:
        controleur['derniere_seconde'] = nouveau_secondes
        chaine = '{:02}:{:02}'.format(nouveau_secondes // 60, nouveau_secondes % 60)
        controleur['interf_horloge'].configure(text = chaine)
        controleur['interf_defilement'].set(nouveau_secondes)

## ici pas de test, il se fait dans l'interface lecteur