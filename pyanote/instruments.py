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

INSTRUMENTS = {}

with open('pyanote/instruments.json') as json_file:  
    liste_instruments = json.load(json_file)
    for inst in liste_instruments:
        if inst['family'] not in list(INSTRUMENTS):
            INSTRUMENTS[inst['family']] = {}
        INSTRUMENTS[inst['family']][inst['instrument']] = int(inst['hexcode'], 16)
