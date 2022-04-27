# Jeu de dames ⋆ ⋆ ⋆

Le jeu de dame est un jeu de société combinatoire abstrait pour deux joueurs. Deux
joueurs s’affrontent en déplaçant des pions (20 par joueur) de couleur blanche ou
noire sur un damier carré de 10 par 10.

## Règles

Dans sa version la plus jouée, les pions doivent suivre les mouvements suivants :

— **Avancer** : un pion peut avancer d’une case en diagonale vers l’avant, si cette
case est libre. L’avant se définit de manière relative pour chaque joueur, i.e.
de sa propre position vers l’adversaire.

— **Capturer** : si la case est occupée par un pion adverse et que la case suivante
(dans la diagonale) est libre, le pion doit capturer ce pion en le “sautant”.
La capture d’un pion ne peut se faire qu’en avançant et est obligatoire. Si la
capture place le pion dans une situation de capture, la capture continue.
Quand un pion atteint la ligne de l’adversaire, la **promotion** intervient : le pion
devient une dame. La dame a alors plus de possibilités de mouvement :

— **Déplacement** : une dame peut avancer dans n’importe quelle diagonale,
d’autant de cases libres qu’elle souhaite.

— **Capture** : la capture peut se réaliser dans n’importe quelle diagonale, à n’importe
quelle distance du pion ou de la dame à capturer. Seule contrainte, la
dame doit arriver dans la case la plus proche du pion ou de la dame capturée.
1ère année PCC - ASINSA

## Projet

Proposez un programme permettant à deux humains de jouer à ce jeu. L’interface
pourra se limiter à un affichage sur le terminal.
