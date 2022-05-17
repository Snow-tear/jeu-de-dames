from re import L
import pygame

class Pion():
    Dame=False
    def __init__(self,couleur:bool) -> None:
        self.couleur=couleur    #Noir:True Blanc=False


class Game():
    message = ""
    mode_repas = {'activé':False} #s'il faut à un pion condinuellement manger
    damier=[[False for j in range(10)]for i in range(10)]   #False: Pas de pion sur la case
    tourne = False  #tourne des joueurs. Noir:True Blanc=False
    error_message=''
    colors={
            'black':(93, 45, 23),
            'white':(229, 177, 119),
            'txt_white':(255, 255, 255),
            'bg_color':(29, 142, 48)
        }
    window_size=720 #window's size in pixel 实际上是屏幕高, 推荐值720或1080    
    margin = int(window_size*0.02) #让屏幕尺寸为16:9

    def __init__(self) -> None:      

        #Initialization de GUI
        pygame.init()
        self.case_size=self.window_size//10
        self.window_size=self.case_size*10
        self.window = pygame.display.set_mode((self.window_size*1.75, self.window_size))
        self.text_font = pygame.font.SysFont('arial', int(self.case_size*0.71))
        pawn = lambda image: pygame.transform.scale(pygame.image.load(image).convert_alpha(), (self.case_size, self.case_size))
        self.icon=dict(zip(
            ('white pawn','black pawn', 'white king', 'black king'),
            map(pawn,("shrek.png","risitas.png", "fiona.png", "stonks.png"))
        ))

        #Initialization de damier
        for i in range(4):
            for j in range(0+(not i%2),10,2):
                self.damier[i][j]=Pion(True)

        for i in range(6,10):
            for j in range(0+(not i%2),10,2):
                self.damier[i][j]=Pion(False)

        self.message = 'Welcome to jeu de dames!'
        self.affichage()

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
        
        turn_print=f"Now is {'Black' if self.tourne else 'White'}'s turn"
        print(turn_print)
        turn_print = self.text_font.render(turn_print, True, (255, 255, 255))
        self.window.blit(turn_print, (self.window_size + self.margin, self.margin))

    #cette fonction charge le mouvement et la promotion d'un pion/une dame
    def move(self,x:int,y:int,n_x:int,n_y:int):
        self.damier[n_x][n_y] = self.damier[x][y]
        self.damier[x][y]=False
        #Promotion
        if (self.tourne and n_x == 9) or (not self.tourne and n_x == 0):
            self.damier[n_x][n_y].Dame=True
    
    def test_pion_manger(self,x,y):
        return 1 in [self.juger(x,y,x+dx,y+dy) for dx in (-2,2) for dy in (-2,2)]

    #x,y: position de la pion/dame
    #nx,ny: nouvelle potition de la pion/dame
    #return: -1: pas valide; 0: déplacer ; 1: manger
    #metre la position du pion à manger
    def juger(self,x:int,y:int,n_x:int,n_y:int)->int:
        """il y a beaucoup de if les uns dans les autres, on pourra simplifier ça une fois que ça marche"""
        
        #les cassgénérals, quelque soit pion ou dame
        if not (0<=n_x<10 and 0<=n_y<10 and 0<=x<10 and 0<=y<10):
            self.error_message="En dehors de la damier!"
            return -1
        pion=self.damier[x][y]
        if not pion:
            self.error_message='Pas de pion ici'
            return -1
        if pion.couleur !=self.tourne:
            self.error_message="C'est pas votre pion!"
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
                if self.mode_repas['activé']:
                    self.error_message='continuer à manger!'
                #le pion doit obligatoiremant manger si c'est possible
                elif self.mes_pions_peuvent_manger():
                    self.error_message='Il faut à un pion manger!!!!!'
                    return -1
                else:
                    return 0    #déplacer
            if abs(n_y-y)==2:   #test si il est possible d'y aller en mangeant
                if self.mode_repas['activé']:
                    if self.mode_repas['x']!=x or self.mode_repas['y']!=y:
                        self.error_message='il faut à un MÊME pion continuer à manger!'
                        return -1
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
            if self.mes_pions_peuvent_manger():
                self.error_message='Il faut à un pion manger!!!!!'
                return -1
            if abs(diff_x)==1:return 0
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

    def mes_pions_peuvent_manger(self):
        for x in range(10):
            for y in range(10):
                if self.damier[x][y]:
                    if not self.damier[x][y].Dame and self.test_pion_manger(x,y):
                        return True
        return False

    def new_action(self,x,y,n_x,n_y):
        self.A_manger_x=False
        self.A_manger_y=False
 
        juge=self.juger(x,y,n_x,n_y)
        if juge==-1:
            print(self.error_message)
        else:
            self.move(x,y,n_x,n_y)
            if juge==1: #cas de manger
                self.damier[self.A_manger_x][self.A_manger_y]=False #enlever le pion mangé!
                if not self.damier[n_x][n_y].Dame and self.test_pion_manger(n_x,n_y):
                    self.mode_repas['activé']=True
                    self.mode_repas['x']=n_x
                    self.mode_repas['y']=n_y
          
                else:
                    self.mode_repas['activé']=False
                    self.tourne=not self.tourne
            else:   #cas de déplacement
                self.tourne=not self.tourne
            

            

    def affichage_gui(self):
        #draw checkerboard
        for i in range(10):
            for j in range(10):
                square = pygame.Rect(i * self.case_size, j * self.case_size, self.case_size, self.case_size)
                pygame.draw.rect(self.window, self.colors['white'] if (i + j) % 2 == 0 else self.colors['black'], square)


        #draw pawns
        for x in range(10):
                for y in range(10):
                    if self.damier[x][y]:
                        if game.damier[x][y].couleur:
                            if game.damier[x][y].Dame:
                                pawn_shape = self.icon['black king']
                            else:
                                pawn_shape = self.icon['black pawn']
                        else:
                            if game.damier[x][y].Dame:
                                pawn_shape = self.icon['white king']
                            else:
                                pawn_shape = self.icon['white pawn']

                        self.pawn_display = self.window.blit(pawn_shape, (y * self.case_size, x * self.case_size))
        #message display
        bg = pygame.Rect(self.window_size, 0, 0.75*self.window_size,self.window_size)
        pygame.draw.rect(self.window, self.colors['bg_color'], bg)


game=Game()


"""
while True:
    game.affichage()
    x,y,n_x,n_y=map(lambda x:int(x),input("Please input the order(x y n_x n_y):\t"))
    game.new_turn(x,y,n_x,n_y)
"""

stop = False
selected=False

while not stop:

    pygame.display.flip()
    for event in pygame.event.get():
        #game.affichage()
        game.affichage_gui()
        message_print = game.text_font.render(game.error_message, True, (255, 255, 255))
        game.window.blit(message_print, (game.window_size + game.margin,game.margin*5.33))


        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            stop = True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #print(event.pos)  # coordonnées du clique
            if not selected:
                x,y=event.pos[1]//game.case_size,event.pos[0]//game.case_size
                selected=True
            else:
                x_n,y_n=event.pos[1]//game.case_size,event.pos[0]//game.case_size
                print(x,y,x_n,y_n)
                game.new_action(x,y,x_n,y_n)
                game.affichage()
                selected=False
        coordonnes_souris = pygame.mouse.get_pos()
        x_mouse, y_mouse = coordonnes_souris[1] // game.case_size,coordonnes_souris[0] // game.case_size
        if x_mouse < 10 and y_mouse < 10:
            if game.damier[x_mouse][y_mouse]:
                if game.tourne == game.damier[x_mouse][y_mouse].couleur:
                    image = game.icon['white king']
                    image.fill((255, 255, 255, 128))
                    game.pawn_display = game.window.blit(image, (y_mouse*game.case_size, x_mouse*game.case_size))