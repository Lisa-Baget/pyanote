# Utilisation de GitHub

Tutoriel par [@phandaal](https://github.com/phandaal)

## Préparation 

1. S'inscrire sur [GitHub](https://github.com) (fournir `gitusername`, `email` et `password`). Attention, l'`email` est important: il sert à recevoir des instructions sur le projet, ou un nouveau mot de passe en cas de perte. Donnez donc un `email` que vous consultez régulièrement. Pour le `gitusername`, le format *Prénom-Nom* est préférable (je ne veux pas avoir à me demander qui est `Darkiller34`). 
2. Télécharger *git* sur https://git-scm.com/ et l'installer.
3. Choisir un répertoire pour installer ses projets GitHub (par exemple, `C:\Users\winusername\Documents\GitHub`)
4. Ouvrir un shell sur ce répertoire
   * Ouvrir ce répertoire `C:\Users\winusername\Documents\GitHub` dans le navigateur de fichiers
   * Lancer un shell depuis le navigateur de fichier ouvert sur ce répertoire (menu `Fichier`: `Ouvrir l'invite de commandes` ou `Fichier`: `Ouvrir Windows PowerShell`). L'invite de commande doit indiquer ce répertoire `C:\Users\winusername\Documents\GitHub`.
   * Si le shell n'est pas ouvert dans le bon répertoire, vous pouvez utiliser les commandes de ce shell pour naviguer dans l'arborescence de fichiers:
       * `dir` (*directory*) liste les fichiers et répertoires appartenant au répertoire courant
       * `cd` (`change directory`) change de répertoire courant. Par Exemple si le répertoire `foo`est dans le répertoire courant `C:\Users\winusername\Documents\GitHub`, la commande `cd foo` transforme le répertoire courant en `C:\Users\winusername\Documents\GitHub\foo` et la commande `cd ..` (`..` désigne le répertoire parent) transforme le répertoire courant en `C:\Users\winusername\Documents`
 5. Configurez *git* avec vos informations personnelles. Dans le shell, tapez:
    * `git config --global user.name gitusername` où `gituserame` est le nom d'utilisateur de votre inscription *GitHub*
    * `git config --global user.name gitusername` où `gituserame` est le nom d'utilisateur de votre inscription *GitHub*
 6. Préparez votre répertoire *git* à recevoir des commandes *git*. Dans ce répertoire (`C:\Users\winusername\Documents\GitHub`) tapez
    * `git init`
    
### Exemple 

```ShellSession
C:\Users\winusername\Documents@~$ dir
C:\Users\winusername\Documents@~$ mkdir GitHub

Répertoire : C:\Users\winusername\Documents

Mode              LastWriteTime     Length       Name
----              -------------     ------       ----
d----        29/09/2018   21:29                GitHub

C:\Users\winusername\Documents@~$ dir

Répertoire : C:\Users\winusername\Documents

Mode              LastWriteTime     Length       Name
----              -------------     ------       ----
d----        29/09/2018   21:29                GitHub

C:\Users\winusername\Documents@~$ cd GitHub
C:\Users\winusername\Documents\GitHub@~$ git config --global user.name "gitusername"
C:\Users\winusername\Documents\GitHub@~$ git config --global user.mail "email"
C:\Users\winusername\Documents\GitHub@~$ dir
C:\Users\winusername\Documents\GitHub@~$ dir -h
C:\Users\winusername\Documents\GitHub@~$ git init
Initialized empty Git repository in C:/Users/winusername/Documents/GitHub/.git/
C:\Users\winusername\Documents\GitHub@~$ dir
C:\Users\winusername\Documents\GitHub@~$ dir -h

Répertoire : C:\Users\winusername\Documents

Mode              LastWriteTime     Length       Name
----              -------------     ------       ----
d--h-        29/09/2018   21:32                  .git

C:\Users\winusername\Documents@~$
```

## Téléchargement et mises à jour d'un repository GitHub

  1. Maintenant, il va falloir lier un répertoire local (dans `C:\Users\winusername\Documents\GitHub`) au repository GitHub que vous souhaitez utilisez (dans ce cas https://github.com/Lisa-Baget/pyanote/). Ouvrez le shell dans ce répertoire `C:\Users\winusername\Documents\GitHub` et lancez la commande:
       * `git clone "https://github.com/Lisa-Baget/pyanote"`
  2. Le répertoire `C:\Users\winusername\Documents\GitHub` contient maintenant un répertoire `pyanote` qui contient tous les fichiers du repository. C'est ce répertoire `C:\Users\winusername\Documents\GitHub\pyanote` qui est lié au repository.
  3. Pour *mettre à jour* le répertoire `pyanote`, ouvrez un shell sur ce répertoire et exécutez la commande ``git pull``
  
 ### Exemple 

```ShellSession
C:\Users\winusername\Documents\GitHub@~$ dir
C:\Users\winusername\Documents\GitHub@~$ git clone "https://github.com/Lisa-Baget/pyanote"
Cloning into 'pyanote'...
remote: Counting objects: 12, done.
remote: Compressing objects: 100% (9/9), done.
remote: Total 12 (delta 1), reused 9 (delta 1), pack-reused 0
Unpacking objects: 100% (12/12), done.
C:\Users\winusername\Documents\GitHub@~$ dir

Répertoire : C:\Users\winusername\Documents\GitHub

Mode              LastWriteTime     Length       Name
----              -------------     ------       ----
d----        29/09/2018   21:41               pyanote

C:\Users\winusername\Documents\GitHub@~$ cd pyanote
C:\Users\winusername\Documents\GitHub\pyanote@~$ dir

Répertoire : C:\Users\winusername\Documents\GitHub\pyanote

Mode              LastWriteTime     Length         Name
----              -------------     ------         ----
-a---        29/09/2018   21:41         69    README.md
-a---        29/09/2018   21:41        212  testmidi.py

C:\Users\winusername\Documents\GitHub\pyanote@~$ dir -h

Répertoire : C:\Users\winusername\Documents\GitHub\pyanote

Mode              LastWriteTime     Length         Name
----              -------------     ------         ----
-d-h-        29/09/2018   21:41                    .git

C:\Users\winusername\Documents\GitHub\pyanote@~$ git pull
Already up to date.
```
Mais une petite heure plus tard...
```ShellSession
C:\Users\winusername\Documents\GitHub\pyanote@~$ git pull
remote: Counting objects: 3, done.
remote: Compressing objects: 100% (3/3), done.
remote: Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
Unpacking objects: 100% (3/3), done.
From https://github.com/Lisa-Baget/pyanote
   0a59be9..d07e6f4 master    -> origin/master
Updating 0a59be9..d07e6f4
Fast-forward
 GITHUB.md | 104 +++++++++++++++++++++++++++++++++++++++++++
 create mode 100644 GITHUB.md
C:\Users\winusername\Documents\GitHub\pyanote@~$ dir

Répertoire : C:\Users\winusername\Documents\GitHub\pyanote

Mode              LastWriteTime     Length         Name
----              -------------     ------         ----
-a---        29/09/2018   22:32       5830    GITHUB.md
-a---        29/09/2018   21:41         69    README.md
-a---        29/09/2018   21:41        212  testmidi.py

C:\Users\winusername\Documents\GitHub\pyanote@~$
```
## Obtention des droits d'édition sur le repository GitHub

1. Contactez [@Lisa-Baget](https://github.com/Lisa-Baget) et donnez-lui votre `gitusername` pour qu'elle vous donne une invitation. Cette invitation sera reçue sur votre `email` renseigné lors de l'inscription à GitHub. Ouvrez le mail envoyé par `Lisa Baget <noreply@github.com>` ayant pour titre *Lisa-Baget invited you to Lisa-Baget/pyanote*. Ce n'est pas la peine de répondre au mail (ça ne marchera pas), mais cliquez sur le lien `View Invitation`. Ceci vous enverra sur une page web où vous n'avez plus qu'à accepter l'invitation.
2. Félicitations, vous êtes maintenant un collaborateur officiel de pyanote! :+1:

## Modifier un fichier et mettre à jour le repository

1. Vous souhaitez par exemple modifier le fichier `README.md` (peut-être pour indiquer que vous êtes maintenant un participant à ce projet).
2. Commencez *toujours* par mettre à jour votre répertoire local (pour être aussi certain que possible que vous travaillez bien sur la dernière version du projet). 
 ```ShellSession
C:\Users\winusername\Documents\GitHub\pyanote@~$ git pull
```
3. Editez le fichier `README.md` avec votre editeur de texte préféré (attention, je parle d'editeur de texte et non de traitement de texte, MS Word est strictement interdit :angry:). Les fichiers `.md` contiennent du texte au format `markdown`. L'apprentissage est facile. Rajoutez par exemple dans la liste des collaborateurs: `[@gitusername](https://github.com/gitusername)`. Enregistrez puis indiquez à *git* que vous avez fait quelque chose sur ce fichier.
```ShellSession
C:\Users\winusername\Documents\GitHub\pyanote@~$ git add README.md
```
4. Lorsque vous avez fini la tâche que vous vous étiez fixée (et je vous conseille d'avancer à petit pas), dites à votre *git* local de préparer un paquet de mise à jour avec tous les fichiers tels qu'ils étaient au moment de votre dernier `add` (attention, si vous avez fait une modification depuis le dernier `add`, celle-ci ne sera pas prise en compte :cry:). Pour vérifier ce qui va être pris en compte dans ce paquet, on peut utiliser la commande `git status`:
```ShellSession
C:\Users\winusername\Documents\GitHub\pyanote@~$ git status
On branch master
Your branch is up to date with 'origin/master'

Changes to be commited:
  (use "git reset HEAD >file>..." to unstage)
  
      modified: README.md

C:\Users\winusername\Documents\GitHub\pyanote@~$
```
Mais si maintenant je fais une nouvelle modification du fichier `README.md`:
```ShellSession
C:\Users\winusername\Documents\GitHub\pyanote@~$ git status
On branch master
Your branch is up to date with 'origin/master'

Changes to be commited:
  (use "git reset HEAD >file>..." to unstage)
  
      modified: README.md

Changes not staged for commit:
   (use git add <file>..." to update what will be commited)
   (use "git checkout --<file>..." to discard changes in working directory)
      
      modified: README.md

C:\Users\winusername\Documents\GitHub\pyanote@~$ git add README.md
C:\Users\winusername\Documents\GitHub\pyanote@~$ git status
On branch master
Your branch is up to date with 'origin/master'

Changes to be commited:
  (use "git reset HEAD >file>..." to unstage)
  
      modified: README.md

C:\Users\winusername\Documents\GitHub\pyanote@~$
```
5. Maintenant vous êtes certain que tous les `add` des fichiers que vous avez modifié sont à jour. Il est maintenant temps de préparer votre paquet avec la commande `git commit`. Il est d'usage d'associer à ce paquet un message court (une ligne) indiquant la tâche réalisée dans ce paquet.
```ShellSession
C:\Users\winusername\Documents\GitHub\pyanote@~$ git commit -m "ajout participants dans README.md"
[master 7589046] ajout participants dans README.md
  1 file changed, 4 insertions(+)
C:\Users\winusername\Documents\GitHub\pyanote@~$ git status
On branch master
 Your branch is ahead of 'origin/master' by 1 commit.
    (use "git push" to publish your local commits)
    
nothing to commit, working tree clean
C:\Users\winusername\Documents\GitHub\pyanote@~$
 ```
6. Vous avez maintenant effectué un ou plusieurs `git commit` et vous souhaitez partager votre travail avec les autres collaborateurs du projet. Il ne reste plus qu'à utiliser la commande `git push`. Attention, un autre collaboratur peut avoir fait des modifications en même temps que vous, ce qui peut créer des problèmes...
```ShellSession
C:\Users\winusername\Documents\GitHub\pyanote@~$ git push
to https://github.com/Lisa-Baget/pyanote
 ! [rejected]    master -> master (fetch first)
error: failed to push some refs to 'https://github.com/Lisa-Baget/pyanote'
hint: Updates were rejected because the remote contains work that you do
hint: not have locally. This is usually caused by another repository pushing
hint: to the same ref. You may want to first integrate the remote changes
hint: (e.g. 'git pull...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
C:\Users\winusername\Documents\GitHub\pyanote@~$ git pull
remote: Counting objects: 6, done.
remote: Compressing objects: 100% (6/6), done.
remote: Total 6 (delta 1), reused 0 (delta 0), pack-reused 0
Unpacking objects: 100% (6/6), done.
From https://github.com/Lisa-Baget/pyanote
   0a59be9..45bb167 master    -> origin/master
Merge made by the 'recursive' strategy. 
 GITHUB.md | 132 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 132 insertions(+)
 create mode 100644 GITHUB.md
C:\Users\winusername\Documents\GitHub\pyanote@~$ git push
Counting objects: 5, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (5/5), done.
Writing objects: 100% (5/5), 774 bytes | 774.00 KiB/s, done.
Total 5 (delta 0), reused 0 (delta 0)
To https://github.com/Lisa-Baget/pyanote
   45bb167..77e3f70 master -> master
C:\Users\winusername\Documents\GitHub\pyanote@~$
```
7. Vous pouvez vérifier sur la page https://github.com/Lisa-Baget/pyanote que vos modifications ont bien été prises en compte. Félicitations, vous avez réalisé votre première contributions au projet `pyanote` sur *GitHub* ! :+1:

## A suivre ...

1. Que faire quand il y a un conflit d'édition (deux collaborateurs modifient le même fichier au même endroit au même moment). Dans ce cas, *git* ne va pas pouvoir arbitrer la fusion des modifications...
2. Utilisation des projets et problèmes dans *GitHub* pour pouvoir communiquer et organiser le projet...
