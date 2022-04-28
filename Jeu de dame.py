class Pion():
    Dame=False
    def __init__(self,couleur:bool) -> None:
        self.couleur=couleur    #Noir:True Blanc=False



class Game():
    damier=[[False for j in range(10)]for i in range(10)]   #False: Pas de pion sur la case
    tourne = False  #tourne des joueurs. Noir:True Blanc=False
    def __init__(self) -> None:

        #Initialization de damier
        for i in range(4):
            for j in range(0+(not i%2),10,2):
                self.damier[i][j]=Pion(True)

        for i in range(6,10):
            for j in range(0+(not i%2),10,2):
                self.damier[i][j]=Pion(False)

        print('Welcome to jeu de dames!')

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
                elif case.Dame:
                    if case.couleur:
                        print("王",end='')
                    else:
                        print("玉",end='')
                else:
                    if case.couleur:
                        print("黑",end='')
                    else:
                        print("白",end='')
            print()

    def move(self,x:int,y:int,n_x:int,n_y:int):
        self.damier[n_x][n_y] = self.damier[x][y]
        self.damier[x][y]=False
        #Promotion
        if (self.tourne and n_x == 9) or (not self.tourne and n_x == 0):
            self.damier[n_x][n_y].Dame=True
    

    #x,y: position de la pion/dame
    #nx,ny: nouvelle potition de la pion/dame
    #return: -1: pas valide; 0: déplacer ; 1: manger
    def juger(self,x:int,y:int,n_x:int,n_y:int)->int:
        """il y a beaucoup de if les uns dans les autres, on pourra simplifier ça une fois que ça marche"""
        pion=self.damier[x][y]

        if not pion:
            print('Pas de pion ici')
            return -1
        if pion.couleur !=self.tourne:
            print("C'est pas votre pion!")
            return -1
        if not (0<=n_x<10 and 0<=n_y<10 and 0<=x<10 and 0<=y<10):
            print("En dehors de la damier!")
            return -1
        if self.damier[n_x][n_y]:# test si la case d'arrivé est occupée
            print("déjà un pion/une dame ici")
            return -1

        diff_x = n_x - x
        diff_y = n_y - y
        if abs(diff_y) != abs(diff_x):
            print("Diagonale svp!")
            return -1

        
        if not pion.Dame: #on traite le cas des pions
            if (pion.couleur and diff_x<0) or (not pion.couleur and diff_x>0):
                print("un pion ne peut pas aller en arrière")
                return -1
            if abs(n_y-y) == 1: #test si il est possible d'y aller en avançant
                return 0    #déplacer
            if abs(n_y-y)==2:   #test si il est possible d'y aller en mangeant
            #/!\ prise obligatoire, verifier si il y a une prise possible avant de regarder si on peut avancer
                à_manger=self.damier[x+diff_x//2][y+diff_y//2]
                if not à_manger or à_manger.couleur == self.tourne:
                    print("on peut pas manger!")
                    return -1
                self.damier[x+diff_x//2][y+diff_y//2] = False
                return 1 #manger
            
            #le cas dessous est donc quand abs(n_y-y)!=1, ni != 2
            print("un pion ne peut pas aller si loin")
            return -1
        
        else: #on traite le cas des dames
            #test si toutes les cases sur la diagonales sont libre (oui -> avancer, oui sauf l'avant dernière -> manger, non -> pas possible)
            free_diagonal = True #la diagonal entre x,y (non compris) et l'avant dernière(non compris)
            xd, yd = x, y
            i = 1
            while i < abs(diff_x)-1 and free_diagonal:
                xd = xd + 1 if diff_x>0 else xd-1
                yd = yd + 1 if diff_y > 0 else yd - 1
                if self.damier[xd][yd]:
                    free_diagonal = False
                i+=1

            avx = n_x -1 if diff_x>0 else n_x +1
            avy = n_y -1 if diff_y>0 else n_y +1

            if free_diagonal and not self.damier[avx][avy]:
                return 0
            if free_diagonal and self.damier[avx][avy].couleur!=self.tourne:
                self.damier[avx][avy]=False
                return 1
            
            #le cas dessous est donc soit diagonal n'est pas libre, soit on mange le faux pion
            print("vous mangez trop!")
            return -1

    def new_turn(self):
        print(f"Now is {'Black' if self.tourne else 'White'}'s turn")

        valide_input=False
        while not valide_input:
            x,y,n_x,n_y=map(lambda x:int(x),input("Please input the order(x y n_x n_y):\t"))
            juge=self.juger(x,y,n_x,n_y)
            if juge!=-1:valide_input=True
        self.move(x,y,n_x,n_y)

        self.tourne=not self.tourne

game=Game()

while True:
    game.affichage()
    game.new_turn()

#TODO: 目前皇后的移动还有问题,连跳也没做