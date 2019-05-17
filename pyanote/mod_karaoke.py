#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pyanote.mod_comptage_temps

(C) Lisa Baget et et Matthieu Durand, 2018-2019 <li.baget@laposte.net> 

Ce module définit un modificateur de controleur permettant d'interagir
avec une interface de karaoke.
"""

def creer_modificateur_karaoke(widget):
    ''' Ce modificateur permet de calculer les canaux laissés disponibles par une chanson.
    '''
    return {'nom' : 'mod_karaoke',
            'init' : {'paroles': [], 'paroles/chanson': {}, 'karaoke_widget': widget},
            'prerequis' : ['mod_temps_total'],
            'fonctions' : {
                'mod_message_meta': gerer_karaoke,
                'mod_prochaine_chanson': sauvegarder_karaoke
                }}

def gerer_karaoke(controleur, num_piste, message):
    if message[0] == 1:
        if controleur['vitesse'] == float('inf'): # on est en mode analyse
            controleur['paroles'].append([controleur['temps_total'], message[1]]) ## sauvegarde
        else:
            ### C'est la qui faudra dire à l'interface ce qui'il faut faire
            ### message[1] contient le message courant
            ### controleur['karaoke_widget'] le widget qui doit gerer ce message
            ### pour tests on fait seulement un print
            print(controleur['temps_total'], message[1])

def sauvegarder_karaoke(controleur):
    controleur['paroles/chanson'][controleur['index_chanson']] = controleur['paroles']
    controleur['paroles'] = []