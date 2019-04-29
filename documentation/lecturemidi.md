# Utilisation du module lecturemidi

### Importation du module

```python
from pyanote.lecturemidi import preparer_midi, enumerer_piste
```

### Création d'une description de fichier

Supposons qu'on ait un répertoire ```rep``` contenant un fichier ```test.mid```. 

```python
description = preparer_midi('./test/test.mid')
```
La variable ```description``` contient maintenant un dictionnaire permettant de récupérer toutes les informations utiles
pour lire le fichier MIDI.

```python
{
  'format': 1,
  'nb_pistes': 2,
  'tempo': {'metrique': True, 'valeur': 384},
  'nom fichier': 'rep/test.mid',
  'pistes': [
    {'ID': 0, 'début': 22, 'fin': 56},
    {'ID': 1, 'début': 64, 'fin': 1384}
  ]
}
```
