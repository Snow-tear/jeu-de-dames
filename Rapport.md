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

## Structure du code

Le programme a trois partie: 

* La définition de la classe **Pion**, où on définit les propriétés d'un pion: son couleur et s'il est une dame ou pas.
* La définition de la classe **Game**. C'est le noyau du programme, elle contient toutes les variables importants et les fonctions qui interprètent le règle du jeu.
* **Une boucle while**. C'est le code 'principale' qui entraine le programme et fait les appels des fonction dans