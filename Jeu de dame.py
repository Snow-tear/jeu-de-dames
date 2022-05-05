from turtle import color
import pygame

class Pion():
    Dame=False
    def __init__(self,couleur:bool) -> None:
        self.couleur=couleur    #Noir:True Blanc=False


class Game():
    damier=[[False for j in range(10)]for i in range(10)]   #False: Pas de pion sur la case
    tourne = False  #tourne des joueurs. Noir:True Blanc=False
    error_message=''
    colors={
            'black':(93, 45, 23),
            'white':(229, 177, 119)
        }

    def __init__(self) -> None:

        

        #Initialization de damier
        for i in range(4):
            for j in range(0+(not i%2),10,2):
                self.damier[i][j]=Pion(True)

        for i in range(6,10):
            for j in range(0+(not i%2),10,2):
                self.damier[i][j]=Pion(False)

        print('Welcome to jeu de dames!')

        #Initialization de GUI
        pygame.init()
        self.window = pygame.display.set_mode((500, 500))
        pawn = lambda image: pygame.transform.scale(pygame.image.load(image).convert_alpha(), (50, 50))
        self.white_pawn_icon = pawn("shrek.png")
        self.black_pawn_icon = pawn("risitas.png")

    def affichage(self):#affichage console

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
        print(f"Now is {'Black' if self.tourne else 'White'}'s turn")



    def move(self,x:int,y:int,n_x:int,n_y:int):
        self.damier[n_x][n_y] = self.damier[x][y]
        self.damier[x][y]=False
        #Promotion
        if (self.tourne and n_x == 9) or (not self.tourne and n_x == 0):
            self.damier[n_x][n_y].Dame=True
    

    #x,y: position de la pion/dame
    #nx,ny: nouvelle potition de la pion/dame
    #return: -1: pas valide; 0: déplacer ; 1: manger
    #metre la position du pion à manger
    def juger(self,x:int,y:int,n_x:int,n_y:int)->int:
        """il y a beaucoup de if les uns dans les autres, on pourra simplifier ça une fois que ça marche"""
        pion=self.damier[x][y]

        if not pion:
            self.error_message='Pas de pion ici'
            return -1
        if pion.couleur !=self.tourne:
            self.error_message="C'est pas votre pion!"
            return -1
        if not (0<=n_x<10 and 0<=n_y<10 and 0<=x<10 and 0<=y<10):
            self.error_message="En dehors de la damier!"
            return -1
        if self.damier[n_x][n_y]:# test si la case d'arrivé est occupée
            self.error_message="déjà un pion/une dame ici"
            return -1

        diff_x = n_x - x
        diff_y = n_y - y
        if abs(diff_y) != abs(diff_x):
            self.error_message="Diagonale svp!"
            return -1

        
        if not pion.Dame: #on traite le cas des pions
            if (pion.couleur and diff_x<0) or (not pion.couleur and diff_x>0):
                self.error_message="un pion ne peut pas aller en arrière"
                return -1
            if abs(n_y-y) == 1: #test si il est possible d'y aller en avançant
                return 0    #déplacer
            if abs(n_y-y)==2:   #test si il est possible d'y aller en mangeant
            #/!\ prise obligatoire, verifier si il y a une prise possible avant de regarder si on peut avancer
                pion_manger=self.damier[x+diff_x//2][y+diff_y//2]
                if not pion_manger or pion_manger.couleur == self.tourne:
                    self.error_message="on peut pas manger!"
                    return -1
                self.A_manger_x=x+diff_x//2
                self.A_manger_y=y+diff_y//2

                return 1 #manger
            
            #le cas dessous est donc quand abs(n_y-y)!=1, ni != 2
            self.error_message="un pion ne peut pas aller si loin"
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

            self.A_manger_x = n_x -1 if diff_x>0 else n_x +1
            self.A_manger_y = n_y -1 if diff_y>0 else n_y +1

            if free_diagonal and not self.damier[self.A_manger_x][self.A_manger_y]:
                return 0
            if free_diagonal and self.damier[self.A_manger_x][self.A_manger_y].couleur!=self.tourne:
                return 1
            
            #le cas dessous est donc soit diagonal n'est pas libre, soit on mange le faux pion
            self.error_message="vous mangez trop!"
            return -1

    #le pion doit obligatoiremant manger si c'est possible
    def detect_manger(self):
        for x in range(10):
            for y in range(10):
                if self.damier[x][y] and self.damier[x][y].couleur==self.tourne:
                    for n_x in range(10):
                        for n_y in range(10):
                            if self.juger(x,y,n_x,n_y)==1:
                                break

    def new_turn(self,positions=''):
        self.A_manger_x=False
        self.A_manger_y=False
        
        self.detect_manger()


        if positions=='': 

            valide_input=False
            while not valide_input:
                x,y,n_x,n_y=map(lambda x:int(x),input("Please input the order(x y n_x n_y):\t"))
                juge=self.juger(x,y,n_x,n_y)
                if juge==-1:
                    print(self.error_message)
                elif juge==0 and self.A_manger_x and not self.damier[x][y].Dame:
                    print('Il faut à un pion manger!!!!!')
                else:
                    valide_input=True
        else: #c'est pour débuggage
            x,y,n_x,n_y=map(lambda x:int(x),positions)

        #enlever le pion mangé!
        if self.A_manger_x:
            self.damier[self.A_manger_x][self.A_manger_y]=False

        self.move(x,y,n_x,n_y)

        self.tourne=not self.tourne

    def affichage_gui(self):
        #draw checkerboard
        for i in range(10):
            for j in range(10):
                square = pygame.Rect(i * 50, j * 50, 50, 50)
                pygame.draw.rect(self.window, self.colors['white'] if (i + j) % 2 == 0 else self.colors['black'], square)

        #draw pawns
        for x in range(10):
                for y in range(10):
                    if self.damier[x][y]:
                        pawn_display = self.window.blit(self.black_pawn_icon if game.damier[x][y].couleur else self.white_pawn_icon, (y * 50, x * 50))


game=Game()


"""
while True:
    game.affichage()
    game.new_turn()
"""

stop = False
while not stop:

    pygame.display.flip()
    for event in pygame.event.get():
        game.affichage()
        game.affichage_gui()


        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            stop = True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            print(event.pos)  # coordonnées du clique
