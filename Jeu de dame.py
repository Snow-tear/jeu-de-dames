class Pion():
    Dame=False
    def __init__(self,couleur:bool) -> None:
        self.couleur=couleur    #Noir:True Blanc=False



class Game():
    damier=[[False for j in range(10)]for i in range(10)]
    tourne = False  #Noir:True Blanc=False
    def __init__(self) -> None:
        self.damier[0][1]=Pion(True)
        for i in range(4):
            for j in range(0+(not i%2),10,2):
                self.damier[i][j]=Pion(True)

        for i in range(6,10):
            for j in range(0+(not i%2),10,2):
                self.damier[i][j]=Pion(False)

    def affichage(self):
        print(' ',end='')
        for i in range(10):
            print('',i,end='')
        print()
        for i in range(len(self.damier)):
            print(i,'',end='')
            for case in self.damier[i]:
                if not case:
                    print("  ",end='')
                elif case.couleur:
                    print("黑",end='')
                else:
                    print("白",end='')
            print()

    def avance(self,ligne:int,colonne:int,sens:str):
        pion=self.damier[ligne][colonne]
        if pion:
            x=ligne+(1 if pion.couleur else -1) #x,y: nouvelles positions
            y=colonne+(1 if sens=='r' else -1)
            if not self.damier[x][y]:
                self.damier[x][y] = pion
                self.damier[ligne][colonne]=False
        else:
            print('Pas de pion ici')
    
    #x,y: position de la pion/dame
    #nx,ny: nouvelle potition de la pion
    #return: -1: pas valide; 0: pion avancer ; 1: pion manger; 2:dame déplacer 3: dame manger
    def juger(self,x,y,n_x,n_y)->int:
        """il y a beaucoup de if les uns dans les autres, on pourra simplifier ça une fois que ça marche"""
        #test si la pièce est un pion ou une dame
        pion=self.damier[x][y]
        print(pion.couleur)
        if not pion.Dame:
            # test si la case d'arrivé est libre
            if not self.damier[n_x][n_y]:
                #test si il est possible d'y aller en avançant
                if abs(n_y-y) == 1 and 0<=n_y<10:
                    if pion.couleur:
                        print(0 if n_x == x-1 and x>0 else "a")
                    else:
                        print(0 if n_x == x + 1 and x < 10 else -1)
                else: print(-1)
                #test si il est possible d'y aller en mangeant
                if n_y == y-2 and 0<=n_y<10: #à gauche
                    if pion.couleur:
                        print(1 if self.damier[x-1][y-1] else -1)
                    else:
                        print(1 if self.damier[x + 1][y - 1] else -1)
                elif n_y == y+2 and 0<=n_y<10: #à droite
                    if pion.couleur:
                        print(1 if self.damier[x-1][y+1] else -1)
                    else:
                        print(1 if self.damier[x + 1][y+1] else -1)
                else : print("b") #attention, ne pas verifier si l'on peut y aller en mangeant si on peut y aller en se déplaçant


            else:
                print(-1)

game=Game()
game.affichage()
game.juger(3,4,4,3)
game.avance(3,4,'l')

game.affichage()

#test
