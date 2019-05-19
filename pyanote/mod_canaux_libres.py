#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pyanote.mod_midi

(C) Lisa Baget, 2018-2019

Ce module définit un modificateur de controleur permettant de calculer
les canaux libres dans une chanson. 
"""

def creer_modificateur_canaux_libres():
    ''' Ce modificateur permet de calculer les canaux laissés disponibles par une chanson.
    '''
    return {'nom' : 'mod_canaux_libres',
            'init' : {'canaux_libres': [True] * 16, 'canaux_libres/chanson': {}}, # au debut les 16 canaux sont libres
            'prerequis' : [],
            'fonctions' : {
                'mod_message_controle': maj_canaux_libres,
                'mod_prochaine_chanson' : enregistrement_canaux_libres
                }}

def maj_canaux_libres(controleur, num_piste, message):
    if message[0] // 16 == 9: # si c'est un note on
        canal = message[0] % 16
        if canal != 9: # le canal drums est toujours libre
            controleur['canaux_libres'][canal] = False

def enregistrement_canaux_libres(controleur):
    canaux_libres = []
    for i in range(16):
        if controleur['canaux_libres'][i]:
            canaux_libres.append(i)
    controleur['canaux_libres/chanson'][controleur['index_chanson']] = canaux_libres
    controleur['canaux_libres'] = [True] * 16

if __name__ == '__main__':
    import pyanote.controleur as cont
    nom_fichier = 'fichiersMidi/Dave Brubeck - Take Five.mid'
    controleur = cont.creer_controleur(nom_fichier)
    modificateur = creer_modificateur_canaux_libres()
    cont.ajouter_modificateur_controle(controleur, modificateur)
    controleur['vitesse'] = float('inf')
    cont.demarrer(controleur)
    print("Canaux libres", controleur['canaux_libres/chanson'])