# py@note



## Installation

### Récupération de pyanote

Si vous avez `git` installé sur votre ordinateur, vous pouvez récupérer tous les fichiers en tapant sous l'invite de commande:

```
git.clone "https://github.com/Lisa-Baget/pyanote"
```

Ceci va créer un répertoire pyanote qui contient tout notre projet. Pour avoir la version courante, après cette première installation allez dans le répertoire pyanote et tapez `git pull`dans l'invite de commande:

Si `git` n'est pas installé, un fichier compressé du projet existe (.zip) à l'addresse:

```
https://github.com/Lisa-Baget/pyanote/archive/master.zip
```

Vous devrez retélécharger le fichier et le redécompresser chaque fois que vous voudrez accéder à la nouvelle version courante.
Enfin vous irez à la racine du répertoire pyanote et taperez pour installer tous les modules:
python setup.py
utilisation de pyanote:
dans le répertoire racine pyanote, il y a 4 répertoires
- pyanote (le répertoire pyanote dans le répertoire pyanote) contient tous les modules que nous avons écrit pour notre projet
-fichiersMidi contient 4 exemples de fichiers midi récupérés sur le net que nous avons utilisé pour nos tests
- documentation n'est pas encore à jour (elle est destinée à tous les gens qui voudraient utiliser notre projets sur github) on essaiera de la finir quand on aura rédigé le rapport mais vous pourrez trouver dedans un cours que j'ai utilisé sur l'utilisation de github.
- archives contient des essais de codes que nous n'avons pas forcement retenus ou pas encore réussi à intégrer dans les modules de pyanote.
Vous pouvez tester depuis l'invit de commende:
python pyanote/piste.py (montre les listes python qu'on récupère en lisant  un  fichier binaire midi)
python archives/l1_lecteur_basique.py (joue un fichier midi qu'on a choisi)
python pyanote/piano.py (lance l'interface graphique du piano)
python archives/g1_interface_piano.py (autre inerface piano qu'on doit mélanger à la précédente)
python archives/g2_interface_lecteur.py (interface graphique de lecture de fichier midi)

```
python setup.py develop
```

## Utilisation


## Modules

### pyanote.fichier

