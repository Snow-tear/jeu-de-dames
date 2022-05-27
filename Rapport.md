# Rapport du projet

Lien du développement du projet : [Jeu de dames · GitLab INSA Lyon](https://gitlab.insa-lyon.fr/kloumida/jeu-de-dames)

## Installation

Ce programme ne comporte qu'un fichier du code, mais la graphique dépend de la libraire `pygame`. Pour l'installer :

```bash
pip install pygame
```

Et pour jouer, il suffit d'exécuter :

```bash
python "Jeu de dame.py"
```

## Structure globale du code

Le programme a trois partie: 

* La définition de la classe **Pion**, où on définit les propriétés d'un pion: son couleur et s'il est une dame ou pas.
* La définition de la classe **Game**. C'est le noyau du programme, elle contient toutes les variables importantes et les fonctions qui interprètent le règle du jeu.
* **Une boucle while**. C'est le code 'principale' qui entraine le programme et fait les appels aux fonction dans la classe Game et aux fonction de la graphique.

## Fonctions et Variables

La majorité de fonctions sont dans la classe Game.

`Game.__init__(self)` : chaque fois un objet de Game créé, cette fonction fait l'initialisation: initialisation de GUI, de damier , de son......

`Game.affichage(self)` : L'affichage de la console utilisé au début du développement. A ce moment-là on a pas encore l'interface graphique. Elle affiche les pion dans la console. Ici on profite des charactères chinois qui sont carrées. "**黑 白 王 玉**" représentent respectivement le pion noir, blanc et la dame noire et blanche. On peut les voir aujourd'hui quand même dans la console.

`Game.move(self,x:int,y:int,n_x:int,n_y:int)` : Le but de cette fonction est simple : déplacer un pion. Les paramètres sont les coordonnées de pion à déplacer et les nouvelles coordonnées. Cette fonction doit être appelée après la fonction `Game.juger`.

`Game.test_pion_manger(self,x,y)` et `Game.mes_pions_peuvent_manger(self)`: On teste si **un** pion particulier peut manger, et s'il existe un pion parmi **tous** les pion d'un coté peut manger. Ces fonctions servent à la réalisation du règle: Si la case est occupée par un pion adverse et que la case suivante (dans la diagonale) est libre, le pion **doit** capturer ce pion en le “sautant”. 

`Game.juger(self,x:int,y:int,n_x:int,n_y:int)->int` : c'est la fonction la plus importante de ce programme. Elle prend aussi les coordonnées de pion à déplacer et les nouvelles coordonnées, et retourne un entier qui indique si une action est réalisable ou pas:

* -1: L'action n'est pas valide.
* 0: L'action est un déplacement et ce déplacement et possible.
* 1: L'action est une capture et cette capture et possible.

Il y a beaucoup de raisons pour lesquelles une action n'est pas valide. Comme le pion ne suit pas une diagonale ou le joueur essaie de déplacer un pion adverse. 

La fonction `Game.juger` est un peu compliquée. Elle traite d'abord les cas généraux, c'est à dire les règles qui appliquent sur tous les pions et dames(règle de diagonale par exemple). Et elle traite ensuite les cas plus particuliers(C'est un pion ou une dame? Le joueur veut déplacer ou capturer?).

`aller_possible(self,x,y)` : On teste si un pion/une dame a la possibilité de bouger. Cette fonction sert à la détermination de la victoire. Si aucun pion/ aucune dame sur place du joueur ne peut bouger, adversaire gagne.

`Game.new_action(self,x,y,n_x,n_y)` : Elle réalise une nouvelle action. Elle réagit selon de différents cas. Affichage un message en cas l'action impossible, prendre un pion en cas de capturer...... Elle est chargée aussi le control du '**mode repas**'. C'est réalisation du règle: Si la capture place le pion dans une situation de capture, la capture continue.

