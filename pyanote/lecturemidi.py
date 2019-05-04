#on selectionne un  fichier
#retourne un dico avec les pistes le format 0,1...

def preparer_midi(nom_fichier):
    ''' Retourne un dictionnaire contenant les informations nécessaires à l'utilisation d'un fichier MIDI.
    '''
    fichier = open(nom_fichier, "rb") # r = read b = binaire
    description_midi = lire_header(fichier) # creation du dico
    description_midi["nom fichier"] = nom_fichier
    description_midi["pistes"] = []
    for i in range(description_midi['nb_pistes']):# je demande quelle est la valeur dans le dico
        description_midi["pistes"].append(preparer_piste(fichier, i))
    fichier.close()
    return description_midi

def lire_header(fichier):
    verifier(fichier, b'MThd', "Ce n'est pas un fichier Midi")
    taille_header = lire_entier(fichier, 4) #lire le nombre qui donne la taille du header
    midi_format, nb_pistes = lire_nb_pistes(fichier) 
    tempo = lire_tempo(fichier)
    avancer(fichier, taille_header - 6) #6 ce qui nous interesse dans header         
    return {'format' : midi_format, 'nb_pistes' : nb_pistes, 'tempo' : tempo} 

def verifier(fichier, mot_clé, msg_erreur):
    if fichier.read(len(mot_clé)) != mot_clé:
        raise TypeError(msg_erreur)

def lire_entier(fichier, nb_octets):
    entier = 0
    for i in range(nb_octets): #commence par poid fort
        entier = entier + ord(fichier.read(1))*256**(nb_octets-i-1) #ord transforme 1 octet binaire en entier (
    return entier

def lire_entier_variable(fichier):
    entier = 0
    octet = ord(fichier.read(1))
    while octet >= 128:
        entier = entier*128 + octet-128
        octet = ord(fichier.read(1))
    return entier*128 + octet
    
def lire_nb_pistes(fichier):
    midi_format = lire_entier(fichier, 2) #ne pas changer l'ordre de ces deux car le curseur a
    nb_pistes = lire_entier(fichier, 2)
    if midi_format == 0 and nb_pistes != 1:
        raise ValueError("Le nombre de piste ne correspond pas au format Midi0")
    return midi_format, nb_pistes

def lire_tempo(fichier):
    octet1 = ord(fichier.read(1))
    octet2 = ord(fichier.read(1))
    if octet1 < 128: # bit de poids fort = 0
        return {"metrique" : True, "valeur" : 256 * octet1 + octet2}
    else:
        return {"metrique" : False, "smpte" : octet1 - 128, "tpf" : octet2}

def avancer(fichier, nb_octets):
    fichier.seek(nb_octets, 1) #1 a partir de la position ou l'on est / 0 debut fichier

def preparer_piste(fichier, num_piste):
    verifier(fichier, b'MTrk', "Ce n'est pas le début d'une piste")
    taille_piste = lire_entier(fichier, 4)
    position = fichier.tell() #retourne le nombre d'octets passé depuis le début
    avancer(fichier, taille_piste)
    return {'ID' : num_piste, 'début' : position, 'fin' : position + taille_piste}

def enumerer_piste(description, num_piste):
    fichier = open(description["nom fichier"], 'rb')
    description_piste = description['pistes'][num_piste]
    avancer(fichier, description_piste['début'])
    sauvegarde = [False, None, None] # initialisation de la sauvegarde. liste car mutable
    while fichier.tell() < description_piste['fin']:
        delta_temps = lire_entier_variable(fichier) # ordre a pas changer!!
        evenement = lire_evenement(fichier, sauvegarde)
        yield delta_temps, evenement  # enumere 

def lire_evenement(fichier,sauvegarde):
    octet = ord(fichier.read(1))
    if octet == 255:
        sauvegarde[0]= False
        return lire_meta_evenement(fichier)
    elif octet == 240 or octet == 247:
        sauvegarde[0]= False
        return lire_evenement_systeme(fichier)
    else:
        return lire_message(fichier, octet,sauvegarde)

def lire_meta_evenement(fichier):
    sorte = ord(fichier.read(1))
    taille = lire_entier_variable(fichier)
    valeur = fichier.read(taille)
    return ["meta", sorte, valeur]

def lire_evenement_systeme(fichier):
    taille = lire_entier_variable(fichier)
    valeur = fichier.read(taille)
    return ["systeme", valeur]
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
def lire_message(fichier, octet, sauvegarde):
    instruction = octet // 16 # 4 1ers bits
    if instruction < 8 or instruction > 14: # pas une instruction
        if sauvegarde[0]: # il y a une sauvegarde
            instruction = sauvegarde[1]
            canal = sauvegarde[2]
            arg1 = octet # l'octet code le premier argument
        else: # on aurait du trouver la sauvegarde
            raise SyntaxError("Sauvegarde introuvable")
    else:
        canal = octet % 16 # 4 derniers bits
        sauvegarde[0] = True # mise a jour de la sauvegarde
        sauvegarde[1] = instruction
        sauvegarde[2] = canal
        arg1 = ord(fichier.read(1))
    if instruction == 12 or instruction ==13: # instructions à 1 argument
        arg2 = 0
    else:
        arg2 = ord(fichier.read(1))
    return ['message', instruction, canal, arg1, arg2]
    
    
if __name__ == "__main__":
    nom ="../exemples/Dave Brubeck - Take Five 1.mid"
    descrip = preparer_midi(nom)
    for element in enumerer_piste(descrip, 0):
        print(element)
