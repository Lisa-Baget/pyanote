#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pyanote.instruments

(C) Lisa Baget, 2018-2019

Ce module construit un dictionnaire de tous les instruments
Midi à partir d'un fichier json créé par Maximillian von Briesen
https://github.com/mobyvb/midi-converter/blob/master/lib/instruments.json

Voir https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
pour savoir comment lire un fichier json.
"""
import json

### On construit un dictionnaire INSTRUMENTS qui donne la liste de tous les instruments
### standards MIDI.
### Instrument[nom_famille][nom_instrument] donne le numéro MIDI de l'instrument.
INSTRUMENTS = {}
with open('pyanote/instruments.json') as json_file:
    ## instrumenst.json est une liste de dictionnaires représentant chacun un instrument comme
    ### {"hexcode":"0x00", "family":"Piano", "instrument":"Acoustic Grand Piano"}
    ### on veut mettre ça sous la forme
    ### {"Piano" : {"Acoustic Grand Piano" : 0x00}}
    ### pour pouvoir être utilisé facilement par piano.py
    liste_instruments = json.load(json_file)
    for inst in liste_instruments:
        if inst['family'] not in list(INSTRUMENTS): ## si la famille n'existe pas encore
            INSTRUMENTS[inst['family']] = {} ## on la crée
        INSTRUMENTS[inst['family']][inst['instrument']] = int(inst['hexcode'], 16) # et on rajoute l'instrument
