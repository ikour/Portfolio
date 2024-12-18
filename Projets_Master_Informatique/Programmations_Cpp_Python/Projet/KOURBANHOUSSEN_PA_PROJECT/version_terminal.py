# *****KOURBANHOUSSEN Idriss*****

# version terminal

import curses
from curses import wrapper
import threading
import time
from main import *

# tableau contenant les coordonées(x) des obstacles 
obstacles = []
# taille scène
longueur_scene_terminal = 100
largeur_scene_terminal = 15
stage = ""
#taille terminal
longueur_terminal = 120
largeur_terminal = 30
# variable pour arrèter le thread
stop = False
# variable pour dire quand il y a rafraichissement
verrou_refresh = threading.Lock() # pour éviter que tout les threads accède à la variable en meme temps
rafraichissement = False  

############################################################################################################################################################
############################################################################################################################################################

class frames_refresh_terminal (threading.Thread): # thread qui rafraichi la page
    def __init__(self, scene, score, number_refresh):
        threading.Thread.__init__(self)  # appel au constructeur de la classe mère
        self.number_refresh = number_refresh
        self.scene = scene
        self.score = score

    def run(self):
        global rafraichissement,verrou_refresh
        while (stop != True):   # continue le rafraichissement tant que la variable stop ne passe pas à True
            time.sleep(1/int(self.number_refresh))
            verrou_refresh.acquire()
            rafraichissement = True
            verrou_refresh.release()
            self.scene.refresh()
            self.score.refresh()
            verrou_refresh.acquire()
            rafraichissement = False
            verrou_refresh.release()
            

class thread_block_terminal (threading.Thread): # thread qui block pendant bloking_time
    def __init__(self, scene, joueur1, joueur2, joueur_appelant_thread):
        threading.Thread.__init__(self)  # appel au constructeur de la classe mère
        self.joueur_appelant_thread = joueur_appelant_thread
        self.scene = scene
        self.joueur1 = joueur1
        self.joueur2 = joueur2

    def run(self):
        global rafraichissement,verrou_refresh
        i = 0
        while (i != self.joueur_appelant_thread.blocking_time): # le block reste atif pendant bloking-time rafraichissements
            verrou_refresh.acquire()
            if rafraichissement == True:
                i += 1
            verrou_refresh.release()
        self.joueur_appelant_thread.state = "Rest" 
        affiche_scene_terminal(self.scene,self.joueur1,self.joueur2)


class thread_attack_terminal (threading.Thread): # thread qui attend attacking_speed frames avant d'attaquer
    def __init__(self, score, scene,joueur1,joueur2, joueur_appelant_thread, mouvement):
        threading.Thread.__init__(self)  # appel au constructeur de la classe mère
        self.score = score
        self.scene = scene
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.joueur_appelant_thread = joueur_appelant_thread # permet de savoir quel joueur appel le thread
        self.mouvement = mouvement # A1 ou A2

    def run(self):
        global rafraichissement,verrou_refresh
        i = 0
        while (i != self.joueur_appelant_thread.attacking_speed):   # on attend attacking_speed rafraichissements pour atteindre l'adverssaire (pendant ce temps l'dvesaire pourra l'exquiver)
            verrou_refresh.acquire()
            if rafraichissement == True:
                i += 1
            verrou_refresh.release()
        mouvement_joueur_terminal(self.score, self.scene, self.joueur1, self.joueur2, self.mouvement)
            
############################################################################################################################################################
############################################################################################################################################################
# la classe joueur avec ses attributs
class joueur_terminal:
    def __init__(self, mouvement_speed, attacking_speed, attacking_range, defending_range, blocking_time):
        self.mouvement_speed = mouvement_speed
        self.attacking_speed = attacking_speed
        self.attacking_range = attacking_range
        self.defending_range = defending_range
        self.blocking_time = blocking_time
        self.score = 0
        self.state = "Rest"
        self.coords_score = (0,0)
        self.coords_joueur = (7,0)

class joueur_1_terminal (joueur_terminal): # player 1
    def __init__(self, mouvement_speed, attacking_speed, attacking_range, defending_range, blocking_time):
        super().__init__(mouvement_speed, attacking_speed, attacking_range, defending_range, blocking_time)


class joueur_2_terminal (joueur_terminal): # player 2
    def __init__(self, mouvement_speed, attacking_speed, attacking_range, defending_range, blocking_time):
        super().__init__(mouvement_speed, attacking_speed, attacking_range, defending_range, blocking_time)

############################################################################################################################################################
############################################################################################################################################################
#fonction qui affiche le score
def affiche_score_terminal(score,joueur1,joueur2):
    _, num_cols = score.getmaxyx()

    score.clear()

    half_length_of_message = int(len("SCORE") / 2)
    middle_column = int(num_cols / 2)
    x_position = middle_column - half_length_of_message
    score.addstr( 0, x_position, "SCORE")

    half_length_of_message = int(len("JOUEUR 1 | JOUEUR 2") / 2)
    middle_column = int(num_cols / 2)
    x_position = middle_column - half_length_of_message
    score.addstr( 3, x_position, "JOUEUR 1 | JOUEUR 2")

    message = str(joueur1.score) + "    |    " + str(joueur2.score)
    half_length_of_message = int(len(message) / 2)
    middle_column = int(num_cols / 2)
    x_position = middle_column - half_length_of_message
    score.addstr( 4, x_position, message)

    joueur1.coords_score = (4,x_position)
    joueur2.coords_score = (4,x_position+len(message)-1)

############################################################################################################################################################
############################################################################################################################################################
#fonction qui affiche la scene
def affiche_scene_terminal(scene, joueur1, joueur2, stage = ""):

    scene.clear()

    for i in range (longueur_scene_terminal): # le tapis
        scene.addstr(12,i, "#")

    if(stage != ""): # pour le premier affichage
        for i in range (len(stage)):
            if (stage[i] == "1"):
                joueur1.coords_joueur = (joueur1.coords_joueur[0], i)
            elif(stage[i] == "2"):
                joueur2.coords_joueur = (joueur2.coords_joueur[0], i)
            elif(stage[i] == "x"):
                scene.addstr(11,i, "x")
                obstacles.append(i)
        joueur1.state = "Rest"
        joueur2.state = "Rest"
    else:
        for i in obstacles:
            scene.addstr(11,i, "x")

    y1 = joueur1.coords_joueur[0]
    x1 = joueur1.coords_joueur[1]
    scene.addstr(y1,x1, "O", curses.A_BOLD)
    scene.addstr(y1+1,x1, "|", curses.A_BOLD)
    scene.addstr(y1+2,x1-1, "_|_", curses.A_BOLD)
    scene.addstr(y1+3,x1, "|", curses.A_BOLD)
    scene.addstr(y1+4,x1-1, "|-|", curses.A_BOLD)
    if(joueur1.state == "Block"):
        scene.addstr(y1+2,x1+2, "/", curses.color_pair(1)) # épée du joueur
    elif(joueur1.state == "Rest"):
        scene.addstr(y1+3,x1+2, "\\", curses.color_pair(1)) # épée du joueur
    elif(joueur1.state == "Attack"):
        str = '_'*joueur1.attacking_range
        scene.addstr(y1+2,x1+2, str, curses.color_pair(1)) # épée du joueur

    y2 = joueur2.coords_joueur[0]
    x2 = joueur2.coords_joueur[1]
    scene.addstr(y2,x2, "O", curses.A_BOLD)
    scene.addstr(y2+1,x2, "|", curses.A_BOLD)
    scene.addstr(y2+2,x2-1, "_|_", curses.A_BOLD)
    scene.addstr(y2+3,x2, "|", curses.A_BOLD)
    scene.addstr(y2+4,x2-1, "|-|", curses.A_BOLD)
    if(joueur2.state == "Block"):
        scene.addstr(y2+2,x2-2, "\\", curses.color_pair(2)) # épée du joueur
    elif(joueur2.state == "Rest"):
        scene.addstr(y2+3,x2-2, "/", curses.color_pair(2)) # épée du joueur
    elif(joueur2.state == "Attack"):
        str = '_'*joueur2.attacking_range
        scene.addstr(y2+2,x2-2, str, curses.color_pair(2)) # épée du joueur

############################################################################################################################################################
############################################################################################################################################################
# fonction qui réalise les mouvements du joueur 
def mouvement_joueur_terminal(score, scene, joueur1, joueur2, mouvement): 
    global rafraichissement, verrou_refresh
    
    if (mouvement == "L1"):
        i=0##############################
        while (i!=joueur1.mouvement_speed): # attend le rafraichissement 
            verrou_refresh.acquire()#####
            if rafraichissement == True:#
                i+=1#####################
            verrou_refresh.release()#####
        #################################
        if(joueur1.coords_joueur[1]-1 > 0) & (joueur1.coords_joueur[1]-2 not in obstacles): # seulement si le joueur est dans la scène et pas d'obstacle sur le chemin
            joueur1.coords_joueur = (joueur1.coords_joueur[0], joueur1.coords_joueur[1]-1)
            affiche_scene_terminal(scene,joueur1, joueur2)
    elif (mouvement == "R1"):
        i=0##############################
        while (i!=joueur1.mouvement_speed): # attend le rafraichissement 
            verrou_refresh.acquire()#####
            if rafraichissement == True:#
                i+=1#####################
            verrou_refresh.release()#####
        #################################
        if(joueur1.coords_joueur[1]+1 < longueur_scene_terminal) & (joueur1.coords_joueur[1]+2 not in obstacles): 
            # seulement si le joueur est dans la scène et pas d'obstacle sur le chemin
            if(joueur1.coords_joueur[1]+2 != joueur2.coords_joueur[1]-2):
                joueur1.coords_joueur = (joueur1.coords_joueur[0], joueur1.coords_joueur[1]+1)
                affiche_scene_terminal(scene,joueur1,joueur2)
    elif (mouvement == "JL1"):
        if(joueur1.coords_joueur[1]-4 > 0): # seulement si le joueur est dans la scène 
            joueur1.coords_joueur = (joueur1.coords_joueur[0]-2, joueur1.coords_joueur[1])
            affiche_scene_terminal(scene,joueur1,joueur2)
            i=0##############################
            while (i!=joueur1.mouvement_speed): # attend le rafraichissement 
                verrou_refresh.acquire()#####
                if rafraichissement == True:#
                    i+=1#####################
                verrou_refresh.release()#####
            #################################
            joueur1.coords_joueur = (joueur1.coords_joueur[0], joueur1.coords_joueur[1]-2)
            affiche_scene_terminal(scene,joueur1,joueur2)
            i=0##############################
            while (i!=joueur1.mouvement_speed): # attend le rafraichissement 
                verrou_refresh.acquire()#####
                if rafraichissement == True:#
                    i+=1#####################
                verrou_refresh.release()#####
            #################################
            joueur1.coords_joueur = (joueur1.coords_joueur[0], joueur1.coords_joueur[1]-2)
            affiche_scene_terminal(scene,joueur1,joueur2)
            i=0##############################
            while (i!=joueur1.mouvement_speed): # attend le rafraichissement 
                verrou_refresh.acquire()#####
                if rafraichissement == True:#
                    i+=1#####################
                verrou_refresh.release()#####
            #################################
            joueur1.coords_joueur = (joueur1.coords_joueur[0]+2, joueur1.coords_joueur[1])
            affiche_scene_terminal(scene,joueur1,joueur2)
    elif (mouvement == "JR1"):
        if(joueur1.coords_joueur[1]+4 < longueur_scene_terminal): # seulement si le joueur est dans la scène 
            joueur1.coords_joueur = (joueur1.coords_joueur[0]-2, joueur1.coords_joueur[1])
            affiche_scene_terminal(scene,joueur1,joueur2)
            i=0##############################
            while (i!=joueur1.mouvement_speed): # attend le rafraichissement 
                verrou_refresh.acquire()#####
                if rafraichissement == True:#
                    i+=1#####################
                verrou_refresh.release()#####
            #################################
            joueur1.coords_joueur = (joueur1.coords_joueur[0], joueur1.coords_joueur[1]+2)
            affiche_scene_terminal(scene,joueur1,joueur2)
            i=0##############################
            while (i!=joueur1.mouvement_speed): # attend le rafraichissement 
                verrou_refresh.acquire()#####
                if rafraichissement == True:#
                    i+=1#####################
                verrou_refresh.release()#####
            #################################
            joueur1.coords_joueur = (joueur1.coords_joueur[0], joueur1.coords_joueur[1]+2)
            affiche_scene_terminal(scene,joueur1,joueur2)
            i=0##############################
            while (i!=joueur1.mouvement_speed): # attend le rafraichissement 
                verrou_refresh.acquire()#####
                if rafraichissement == True:#
                    i+=1#####################
                verrou_refresh.release()#####
            #################################
            joueur1.coords_joueur = (joueur1.coords_joueur[0]+2, joueur1.coords_joueur[1])
            affiche_scene_terminal(scene,joueur1,joueur2)
    elif (mouvement == "B1"):
        joueur1.state = "Block"
        affiche_scene_terminal(scene,joueur1,joueur2)
        th = thread_block_terminal(scene, joueur1, joueur2, joueur1)
        th.start()
    elif (mouvement == "A1"):
        if ((joueur1.coords_joueur[1]+1+joueur1.attacking_range) >= (joueur2.coords_joueur[1]-2)):
            if(joueur2.state == "Block"):
                if((joueur1.coords_joueur[1]+1)<(joueur2.coords_joueur[1]-1-joueur2.defending_range)):
                    joueur1.score = joueur1.score + 1
                    affiche_score_terminal(score,joueur1,joueur2)
                    affiche_scene_terminal(scene,joueur1,joueur2,stage)
            else:
                joueur1.score = joueur1.score + 1
                affiche_score_terminal(score,joueur1,joueur2)
                affiche_scene_terminal(scene,joueur1,joueur2,stage)
        joueur1.state = "Rest"
        affiche_scene_terminal(scene,joueur1,joueur2)

    ##################################################################################################################

    elif (mouvement == "L2"):
        i=0##############################
        while (i!=joueur2.mouvement_speed): # attend le rafraichissement 
            verrou_refresh.acquire()#####
            if rafraichissement == True:#
                i+=1#####################
            verrou_refresh.release()#####
        #################################
        if(joueur2.coords_joueur[1]-1 > 0) & (joueur2.coords_joueur[1]-2 not in obstacles): # seulement si le joueur est dans la scène et pas d'obstacle sur le chemin
            if(joueur1.coords_joueur[1]+2 != joueur2.coords_joueur[1]-2):
                joueur2.coords_joueur = (joueur2.coords_joueur[0], joueur2.coords_joueur[1]-1)
                affiche_scene_terminal(scene,joueur1,joueur2)
    elif (mouvement == "R2"):
        i=0##############################
        while (i!=joueur2.mouvement_speed): # attend le rafraichissement 
            verrou_refresh.acquire()#####
            if rafraichissement == True:#
                i+=1#####################
            verrou_refresh.release()#####
        #################################
        if(joueur2.coords_joueur[1]+1 <longueur_scene_terminal) & (joueur2.coords_joueur[1]+2 not in obstacles): # seulement si le joueur est dans la scène et pas d'obstacle sur le chemin
            joueur2.coords_joueur = (joueur2.coords_joueur[0], joueur2.coords_joueur[1]+1)
            affiche_scene_terminal(scene,joueur1,joueur2)
    elif (mouvement == "JL2"):
        if(joueur2.coords_joueur[1]-4 > 0): # seulement si le joueur est dans la scène 
            scene.clear()
            joueur2.coords_joueur = (joueur2.coords_joueur[0]-2, joueur2.coords_joueur[1])
            affiche_scene_terminal(scene,joueur1,joueur2)
            i=0##############################
            while (i!=joueur2.mouvement_speed): # attend le rafraichissement 
                verrou_refresh.acquire()#####
                if rafraichissement == True:#
                    i+=1#####################
                verrou_refresh.release()#####
            #################################
            joueur2.coords_joueur = (joueur2.coords_joueur[0], joueur2.coords_joueur[1]-2)
            affiche_scene_terminal(scene,joueur1,joueur2)
            i=0##############################
            while (i!=joueur2.mouvement_speed): # attend le rafraichissement 
                verrou_refresh.acquire()#####
                if rafraichissement == True:#
                    i+=1#####################
                verrou_refresh.release()#####
            #################################
            joueur2.coords_joueur = (joueur2.coords_joueur[0], joueur2.coords_joueur[1]-2)
            affiche_scene_terminal(scene,joueur1,joueur2)
            i=0##############################
            while (i!=joueur2.mouvement_speed): # attend le rafraichissement 
                verrou_refresh.acquire()#####
                if rafraichissement == True:#
                    i+=1#####################
                verrou_refresh.release()#####
            #################################
            joueur2.coords_joueur = (joueur2.coords_joueur[0]+2, joueur2.coords_joueur[1])
            affiche_scene_terminal(scene,joueur1,joueur2)
    elif (mouvement == "JR2"):
        if(joueur2.coords_joueur[1]-4 > 0): # seulement si le joueur est dans la scène 
            joueur2.coords_joueur = (joueur2.coords_joueur[0]-2, joueur2.coords_joueur[1])
            affiche_scene_terminal(scene,joueur1,joueur2)
            i=0##############################
            while (i!=joueur2.mouvement_speed): # attend le rafraichissement 
                verrou_refresh.acquire()#####
                if rafraichissement == True:#
                    i+=1#####################
                verrou_refresh.release()#####
            #################################
            joueur2.coords_joueur = (joueur2.coords_joueur[0], joueur2.coords_joueur[1]+2)
            affiche_scene_terminal(scene,joueur1,joueur2)
            i=0##############################
            while (i!=joueur2.mouvement_speed): # attend le rafraichissement 
                verrou_refresh.acquire()#####
                if rafraichissement == True:#
                    i+=1#####################
                verrou_refresh.release()#####
            #################################
            joueur2.coords_joueur = (joueur2.coords_joueur[0], joueur2.coords_joueur[1]+2)
            affiche_scene_terminal(scene,joueur1,joueur2)
            i=0##############################
            while (i!=joueur2.mouvement_speed): # attend le rafraichissement 
                verrou_refresh.acquire()#####
                if rafraichissement == True:#
                    i+=1#####################
                verrou_refresh.release()#####
            #################################
            joueur2.coords_joueur = (joueur2.coords_joueur[0]+2, joueur2.coords_joueur[1])
            affiche_scene_terminal(scene,joueur1,joueur2)
    elif (mouvement == "B2"):
        joueur2.state = "Block"
        affiche_scene_terminal(scene,joueur1,joueur2)
        th = thread_block_terminal(scene, joueur1, joueur2, joueur2)
        th.start()
    elif (mouvement == "A2"):
        if ((joueur2.coords_joueur[1]-1-joueur2.attacking_range) <= (joueur1.coords_joueur[1]+2)):
            if(joueur1.state == "Block"):
                if((joueur2.coords_joueur[1]-1)>(joueur1.coords_joueur[1]+1+joueur1.defending_range)):
                    joueur2.score = joueur2.score + 1
                    affiche_score_terminal(score,joueur1,joueur2)
                    affiche_scene_terminal(scene,joueur1,joueur2,stage)
            else:
                joueur2.score = joueur2.score + 1
                affiche_score_terminal(score,joueur1,joueur2)
                affiche_scene_terminal(scene,joueur1,joueur2,stage)
        joueur2.state = "Rest"
        affiche_scene_terminal(scene,joueur1,joueur2)

############################################################################################################################################################
############################################################################################################################################################
# fonction qui enregistre la partie dans un fichier
def enregistrer_partie_terminal(joueur1,joueur2):
    myFile = open("./parties_enregistrees/partie_save.txt", "w")
    temp = ""
    for i in range(1, 101):
        if i == joueur1.coords_joueur[1]:
            temp += "1"
        elif i == joueur2.coords_joueur[1]:
            temp += "2"
        elif i in obstacles:
            temp += "x"
        else:
            temp += "_"
    # ecriture de la scene
    myFile.write(temp)
    # ecriture des attributs du joueur1
    myFile.write(' '+str(joueur1.mouvement_speed)+' '+str(joueur1.attacking_speed)+' '+str(joueur1.attacking_range)+' '+str(joueur1.defending_range)+' '+str(joueur1.blocking_time))
    # ecriture des attributs du joueur1
    myFile.write(' '+str(joueur2.mouvement_speed)+' '+str(joueur2.attacking_speed)+' '+str(joueur2.attacking_range)+' '+str(joueur2.defending_range)+' '+str(joueur2.blocking_time))
    # ecriture du score du joueur1
    myFile.write(' '+str(joueur1.score))
    # ecriture du score du joueur2
    myFile.write(' '+str(joueur2.score))

    myFile.close()


############################################################################################################################################################
############################################################################################################################################################
# fonction qui affiche le menu
def affiche_menu_terminal(screen,menu, joueur1, joueur2):
    menu.clear()
    menu.resize(16,75)
    menu.border('|','|','-','-')
    num_rows, num_cols = menu.getmaxyx()

    str = "MENU"
    half_length_of_message = int(len(str) / 2)
    middle_column = int(num_cols / 2)
    x_position = middle_column - half_length_of_message
    menu.addstr( 1, x_position, str, curses.color_pair(3))

    str = "Commande joueur 1 | Commande joueur 2"
    half_length_of_message = int(len(str) / 2)
    middle_column = int(num_cols / 2)
    x_position = middle_column - half_length_of_message
    menu.addstr( 4, x_position, str)

    str = "        Déplacement droite: 'd' | Déplacement droite: 'Key_Right'"
    half_length_of_message = int(len(str) / 2)
    middle_column = int(num_cols / 2)
    x_position = middle_column - half_length_of_message
    menu.addstr( 6, x_position, str)

    str = "       Déplacement gauche: 'q' | Déplacement gauche: 'Key_Left'"
    half_length_of_message = int(len(str) / 2)
    middle_column = int(num_cols / 2)
    x_position = middle_column - half_length_of_message
    menu.addstr( 7, x_position, str)

    str = "Saut droite: 'e' | Saut droite: 'm'"
    half_length_of_message = int(len(str) / 2)
    middle_column = int(num_cols / 2)
    x_position = middle_column - half_length_of_message
    menu.addstr( 8, x_position, str)

    str = "Saut gauche: 'a' | Saut gauche: 'l'"
    half_length_of_message = int(len(str) / 2)
    middle_column = int(num_cols / 2)
    x_position = middle_column - half_length_of_message
    menu.addstr( 9, x_position, str)

    str = "Attaquer: 'z' | Attaquer: 'o'"
    half_length_of_message = int(len(str) / 2)
    middle_column = int(num_cols / 2)
    x_position = middle_column - half_length_of_message
    menu.addstr( 10, x_position, str)

    str = "Bloquer: 's' | Bloquer: 'p'"
    half_length_of_message = int(len(str) / 2)
    middle_column = int(num_cols / 2)
    x_position = middle_column - half_length_of_message
    menu.addstr( 11, x_position, str)

    str = "|Enregistrer|     |Quitter|     |Reprendre|"
    half_length_of_message = int(len(str) / 2)
    middle_column = int(num_cols / 2)
    x_position = middle_column - half_length_of_message
    menu.addstr( 13, x_position, str, curses.color_pair(3))

    menu.refresh()

    souris = 0 

    while True:
        souris = screen.getch()
        _, mx, my, _, _ = curses.getmouse()
        if (mx>=x_position)&(mx<=13+x_position):
            enregistrer_partie_terminal(joueur1,joueur2)
        if (mx>=18+x_position)&(mx<=27+x_position):
            if my == 14:
                return "Quitter"
        if (mx>=33+x_position)&(mx<=43+x_position):
            if my == 14:
                menu.clear()
                menu.refresh()
                menu.resize(3,10)
                menu.border('|','|','-','-')
                menu.addstr(1,3, "MENU", curses.A_BOLD)
                menu.refresh()
                return "Reprendre"



############################################################################################################################################################
############################################################################################################################################################
# fonction pricipale de la version terminale
def main_terminal(screen, scene, joueur1, joueur2, number_refresh):
    global stop, stage
    clavier = 0 

    stage = scene
    curses.resize_term(largeur_terminal,longueur_terminal)
    curses.curs_set(False) # rend le curseur clignotant invisible
    curses.mousemask(1)
    screen.refresh()

    # Start colors in curses
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)

    menu = curses.newwin(3, 10,1,1)
    menu.border('|','|','-','-')
    menu.addstr(1,3, "MENU", curses.A_BOLD)
    menu.refresh()

    # (lines, columns, start line, start column)
    score = curses.newwin(7, 30, 2,int((longueur_terminal/2)-15))
    affiche_score_terminal(score,joueur1,joueur2)

    scene = curses.newwin(largeur_scene_terminal, longueur_scene_terminal, 10, 10)
    affiche_scene_terminal(scene, joueur1, joueur2, stage)

    refresh_th = frames_refresh_terminal(scene, score, number_refresh)
    refresh_th.start()


    while (clavier != ord('w')):

        if clavier == ord('q'): # mouvement gauche joueur 1
            mouvement_joueur_terminal(score, scene,joueur1,joueur2, "L1")
        elif clavier == ord('d'): # mouvement droite joueur 1
            mouvement_joueur_terminal(score, scene,joueur1,joueur2, "R1")
        elif clavier == ord('a'): # mouvement saut gauche joueur 1
            mouvement_joueur_terminal(score, scene,joueur1,joueur2, "JL1")
        elif clavier == ord('e'): # mouvement saut droite joueur 1
            mouvement_joueur_terminal(score, scene,joueur1,joueur2, "JR1")
        elif clavier == ord('s'): # mouvement block joueur 1
            mouvement_joueur_terminal(score, scene,joueur1,joueur2, "B1")
        elif clavier == ord('z'): # mouvement attaque joueur 1
            joueur1.state = "Attack"
            affiche_scene_terminal(scene,joueur1,joueur2)
            th = thread_attack_terminal(score, scene,joueur1,joueur2, joueur1, "A1")
            th.start()
        elif clavier == curses.KEY_LEFT: # mouvement gauche joueur 2
            mouvement_joueur_terminal(score, scene,joueur1,joueur2, "L2")
        elif clavier == curses.KEY_RIGHT: # mouvement droite joueur 2
            mouvement_joueur_terminal(score, scene,joueur1,joueur2, "R2")
        elif clavier == ord('l'): # mouvement saut gauche joueur 2
            mouvement_joueur_terminal(score, scene,joueur1,joueur2, "JL2")
        elif clavier == ord('m'): # mouvement saut droite joueur 2
            mouvement_joueur_terminal(score, scene,joueur1,joueur2, "JR2")
        elif clavier == ord('p'): # mouvement block joueur 2
            mouvement_joueur_terminal(score, scene,joueur1,joueur2, "B2")
        elif clavier == ord('o'): # mouvement attaque joueur 2
            joueur2.state = "Attack"
            affiche_scene_terminal(scene,joueur1,joueur2)
            th = thread_attack_terminal(score, scene,joueur1,joueur2, joueur2, "A2")
            th.start()
        elif clavier == curses.KEY_MOUSE:
            _, mx, my, _, _ = curses.getmouse()
            num_rows, num_cols = menu.getmaxyx()
            if (mx>=0)&(mx<=num_cols):
                if(my>=0)&(my<=num_rows):
                    clavier = affiche_menu_terminal(screen, menu, joueur1, joueur2)
            if clavier == "Quitter":
                break
            else:
                affiche_score_terminal(score, joueur1, joueur2)

        if (joueur1.score == 5): # le jeu s'arrète quand l'un des 2 joueurs à un score de 5
            score.addstr( 6, 0, "Le joueur 1 a gagné !", curses.color_pair(1))
            curses.napms(1000)
            break
        elif(joueur2.score == 5):
            score.addstr( 6, 0, "Le joueur 2 a gagné !", curses.color_pair(2))
            curses.napms(1000)
            break
        
        clavier = screen.getch()

    stop = True # arrèt du thread de rafraichissement
    
    score.clear()
    scene.clear()
    menu.clear()
    screen.clear()
