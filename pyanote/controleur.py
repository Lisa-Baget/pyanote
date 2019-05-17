import pyanote.album as alb
import threading
import time

CONTROLEUR_STANDARD = {
    'index_chanson' : 0, ## le numero de la chanson qu'on est en train de jouer
    'index_evenement' : 0, ## Le numero de l'evenement dans la chanson qu'on est en train de jouer
    'vitesse' : 1, # 1 standard (vitesse normale), float('inf') pour ne plus faire de sleep
    'fin' : False, ## le mettre à True pour finir la lecture
    'pause' : False, ## le mettre à True pour mettre la lecture en pause
    'evenements_urgents': [], ## pour mettre les evenements a faire en urgence
    'thread': False,
    ### ici les champs qui servent à gérer les controles ajoutés
    'modificateurs': [],
    'mod_message': [],
    'mod_message_controle':  [],
    'mod_message_systeme': [],
    'mod_message_meta' : [],
    'mod_delta_temps': [],
    'mod_prochaine_chanson': [],
    'mod_pause': [],
    'mod_arret': []
}

def creer_controleur(nom_fichier, thread=False):
    controleur = alb.creer_album(nom_fichier) ## le controleur est d'abord un album 
    initialiser_valeurs_defaut(controleur) ## rajoute toutes les valeurs initiales du controleur standard
    controleur['thread'] = thread
    return controleur

def initialiser_valeurs_defaut(controleur):
    controleur.update(CONTROLEUR_STANDARD) ## on lui rajoute toutes les clés/valeurs du controleur standard et on remplace si deja la
    controleur["micros/tick"] = maj_tempo(controleur, 500000) # valeur par defaut, 120BPM -> (60/120) * 10**6 =  500000 microsecondes/beat
    
def maj_tempo(controleur, tempo):
    ### le ticks/beat dans le controleur est ce qui a été lu dans le header
    ### le tempo envoyé par les messages meta est en microsecondes/beat
    return tempo / controleur["ticks/noire"] # Le retour est en microsecondes / tick

def demarrer(controleur):
    if controleur['thread']:
        controleur['thread'] = threading.Thread(None, boucle_lecture, None, [controleur])
        controleur['thread'].start()
    else:
        boucle_lecture(controleur)

def boucle_lecture(controleur):
    while not controleur['fin']: # tant que le controleur ne dit pas que c'est fini
        for evenement in controleur['evenements_urgents']:
            traiter_message(controleur, evenement[1], evenement[2])
        if controleur['pause']: # si le controleur est en pause
            executer_modificateurs_controles('mod_pause', controleur)
            time.sleep(0.1) # durée à verifier dans tests, on fait un sleep pour pas retester la pause immediatement
        else: # traiter le prochain evenement
            evenement = evenement_courant(controleur)
            traiter_evenement(controleur, evenement)
            prochain_evenement(controleur)
    executer_modificateurs_controles('mod_arret', controleur)
    for evenement in controleur['evenements_urgents']:
            traiter_message(controleur, evenement[1], evenement[2])

def evenement_courant(controleur):
    ''' Retourne l'evenement qui doit etre joué par le controleur.
    '''
    album = controleur['chansons']
    return album[controleur["index_chanson"]][controleur["index_evenement"]]

def prochain_evenement(controleur):
    ''' Mise a jour du controleur pour qu'il indique le prochain evenement courant.
    '''
    album = controleur['chansons']
    chanson = album[controleur["index_chanson"]]
    if controleur["index_evenement"] + 1 == len(chanson): # on a traité le dernier evenement de la chanson
        prochaine_chanson(controleur)
    else: # continuer sur la même piste
        controleur["index_evenement"] += 1

def prochaine_chanson(controleur):
    executer_modificateurs_controles('mod_prochaine_chanson', controleur)
    album = controleur['chansons']
    if controleur["index_chanson"] + 1 == len(album): # on a traité la dernière chanson
        controleur["fin"] = True ## c'est la fin
    else: # on  doit passer à la chanson suivante
        controleur["index_chanson"] += 1 # chanson suivante
        controleur["index_evenement"] = 0
        ## la il faudra aussi gerer les temps et signaler à l'interface....

def traiter_evenement(controleur, evenement):
    traiter_delta_temps(controleur, evenement[0])
    traiter_message(controleur, evenement[1], evenement[2])

def traiter_delta_temps(controleur, ticks):
    micros = ticks * controleur["micros/tick"]
    executer_modificateurs_controles('mod_delta_temps', controleur, ticks, micros)
    time.sleep(micros / (10**6 * controleur["vitesse"]))

def traiter_message(controleur, num_piste, message):
    executer_modificateurs_controles('mod_message', controleur, num_piste, message)
    if len(message) == 1: # systeme
        executer_modificateurs_controles('mod_message_systeme', controleur, num_piste, message)
    elif len(message) == 3: # controle
        executer_modificateurs_controles('mod_message_controle', controleur, num_piste, message)
    else: # meta
        executer_modificateurs_controles('mod_message_meta', controleur, num_piste, message)
        if message[0] == 0x51: # changement tempo
            controleur["micros/tick"] = maj_tempo(controleur, message[1])

def ajouter_modificateur_controle(controleur, modificateur):
    controleur['modificateurs'].append(modificateur['nom'])
    controleur.update(modificateur['init'])
    for prerequis in modificateur['prerequis']:
        if prerequis not in controleur['modificateurs']:
            raise ValueError('Un modificateur prerequis est absent.')
    for cle, valeur in modificateur['fonctions'].items():
        controleur[cle].append(valeur)

def executer_modificateurs_controles(cle, *args):
    for fonction in args[0][cle]: ## args[0] c'est toujours le controleur
        fonction(*args)


if __name__ == "__main__":
    import tkinter
    from tkinter.filedialog import askopenfilename
    import pyanote.son as son
    nom_fichier = 'fichiersMidi/Dave Brubeck - Take Five.mid'
    controleur = creer_controleur(nom_fichier)
    modificateur = {
        'nom' : 'Afficheur de messages Meta',
        'init' : {},
        'prerequis' : [],
        'fonctions' : {
            'mod_message_meta' : lambda controleur, num_piste, message: print(num_piste, message)
        }
    }
    controleur['vitesse'] = 10
    ajouter_modificateur_controle(controleur, modificateur)
    ## on voit ici que plein de pistes ce sont arretees tres vite
    demarrer(controleur)
