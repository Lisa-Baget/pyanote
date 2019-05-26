#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""l3_principe_utilisation_thread

(C) Phandaal <https://github.com/phandaal>, 2019

Principe d'utilisation du thread avec un controleur. On a une fonction foo très longue dont l'execution dépend
d'un controleur (qui doit etre un mutable, comme un dictionnaire ou une liste). Si on exécute juste
foo, on ne peut changer ses parametres d'exécution que quand l'exécution a fini, et ça ne sert plus à rien.

Le module Threading nous donne une solution. La fonction foo est exécutée dans un THREAD, et PYTHON partage
le temps entre le programme PRINCIPAL et le THREAD. Le programme PRINCIPAL n'aura donc pas à attendre la fin de l'exécution
de foo pour changer son comportement en modifiant le controleur. Il faudra adapter cette solution à ton projet:

La lecture d'un fichier Midi sera paramétrée par un controleur, qui dira par exemple si la lecture est en pause,
si il faut l'arreter, etc... Cette lecture sera lancée dans un THREAD, et le programme PRINCIPAL pourra par exemple mettre
en pause en changeant des valeurs dans le controleur.
"""
import threading
import time

def foo(controleur):
    while(not controleur['stop']):
        print(controleur['mot'])
        time.sleep(0.1)

controleur = {'mot': 'programmation', 'stop': False}
### Si on appelle juste foo(controleur), ça va afficher 'programmation' à l'infini, toutes les 0.1 secondes

thread = threading.Thread(None, foo, None, [controleur])
## On prépare un thread (un environnement) dédié à executer foo avec pour unique parametre controleur

print("Avant le start, thread vivant?:", thread.isAlive()) ## False, le thread ne va vivre que quand on le start

thread.start()
## Quand on démarre ce thread, il y a deux environnements d'exécution différents, le principal qui va continuer
## ce programme, et le thread qui va faire ce qu'on lui a dit, c'est à dire executer foo(controleur). 
## A partir de ce moment, python va répartir son temps d'execution entre l'environnement principal et le thread:
## on aura l'impression que les deux se deroulent en même temps.

print("Après le start, thread vivant?:", thread.isAlive()) #True

time.sleep(0.5) ## Au bout de 0.5 secondes du principal, et pendant ce temps le thread aura continué à afficher
controleur['mot'] = 'Python' ## le programme principal change le mot dans le controleur

### Comme l'environnement principal et le thread partagent la mémoire, cette modification sera vue dans le thread
### la prochaine fois que python va lui donner la main, et il commencera à afficher Python

time.sleep(1) ## Au bout d'une seconde du principal, et pendant ce temps le thread aura continué à afficher
controleur['stop'] = True ## le programme principal dit au thread de s'arreter en modifiant le controleur

## le thread "meurt" dès que foo(controleur) se termine, mais le resultat de ce print va dépendre de la façon
## dont python répartit le temps d'exécution, et donc notre test ne donnera pas toujours la même chose:
## PRINCIPAL: stop -> PRINCIPAL: print -> THREAD: test du while >> le print va faire False
## PRINCIPAL: stop -> THREAD: test du while -> THREAD: meurt -> PRINCIPAL: print >> le print va faire True
print("Avant le join, thread vivant?", thread.isAlive())

thread.join() ## le programme principal attend que le thread s'arrete
print("Après le join, thread vivant?", thread.isAlive()) ## La on est sur que ça répond False

