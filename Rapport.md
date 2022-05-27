# Rapport du projet

Lien du développement du projet : [Jeu de dames · GitLab INSA Lyon](https://gitlab.insa-lyon.fr/kloumida/jeu-de-dames)
<br/>Lien du design : [Jeu de dames - Figma](https://www.figma.com/file/m8VwZRUorLVr325wRjFDpI/Jeu-de-dame?node-id=0%3A1)

## Installation

Ce programme ne comporte qu'un fichier du code, mais l'interface graphique dépend de la libraire `pygame`. Pour l'installer :

```bash
pip install pygame
```

Et pour jouer, il suffit d'exécuter :

```bash
python "Jeu de dame.py"
```

## Structure globale du code

Le programme a trois partie: 

* La définition de la classe **Pion**, où on définit les propriétés d'un pion: sa couleur et s'il est une dame ou pas.
* La définition de la classe **Game**. C'est le noyau du programme, elle contient toutes les variables importantes et les fonctions qui interprètent le règle du jeu.
* **Une boucle while**. C'est le code 'principale' qui entraine le programme et fait les appels aux fonction dans la classe Game et aux fonction de l'interface graphique.

## Fonctions et Variables

La majorité de fonctions sont dans la classe Game.

* `Game.__init__(self)` : chaque fois un objet de Game créé, 
* `affichage_gui(self)` : pemet d'afficher la partie : des boucles créent le damier et y placent les pions
* `main_menu_gui(self, click)` : affiche le menu principal en affichant les différents boutons et élément de design. Pour les clics, on utilise des collisions avec les différents boutons, ce qui permet d'accéder au reste du programme.
* `setting_gui(self, click, event)` : affiche les paramètre du jeu : activer ou desactiver le son, la musique ou l'écran de presentation (ce dernier paramètre necessite un redemarage de l'application). Les changements sont incrits dans un fichier externe (Settings.txt) afin d'être conservé au redemarrage.
* `lang_gui(self, click, event)` : permet de changer la langue du programme. Pour cela, on stock toute le texte affiché dans 2 fichier de langue que l'on importe sous forme de liste. Le paramètre change un autre fichier, lang.txt, qui stock la langue à importer au démarrage.

Fonctionnement de la boucle principale:

On a d'abord la fonction `pygame.display.flip()` qui permet de raffraichir l'affichage.
Ensuite, la boucle `for event in pygame.event.get():` est parcouru chaque fois qu'un évenement est détécté par pygame, et cette évenement sera nommé `event`.
Cela permet ainsi de définir la fermeture du jeu quand on ferme la fenetre, ainsi que le role de la touche echap (retour au menu principal ou quitter).
La boucle est ensuite découpé en différentes `user_view`, correspondant à la partie du programme dans laquelle nous nous trouvons.
Chacune d'entre elle renvoie aux fonctions d'affichage associés. Dans la `user_view` 1, correspondant à la phase de jeu, on doit également afficher les messages. On utilise un algorithme qui permet un retour à la ligne si un message est trop long. Si il n'y a pas victoire, on détecte les clics et la position de la souris pour permettre la selection/déselection des pions, et on met un effet blanc quand la souris passe au dessus d'un pion que l'on a la droit de jouer, ainsi que sur le pion selectionné.