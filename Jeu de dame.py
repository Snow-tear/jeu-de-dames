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
    def juger(self,x,y,nx,n_y)->int:
        pass


game=Game()
game.affichage()
game.avance(3,2,'l')
game.affichage()
