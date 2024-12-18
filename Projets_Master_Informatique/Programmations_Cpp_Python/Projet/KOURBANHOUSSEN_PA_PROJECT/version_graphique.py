# *****KOURBANHOUSSEN Idriss*****

# version graphique

from tkinter import *
from PIL import Image, ImageTk
import sys
import threading
import time
import warnings

# pour ne pas mettre les warning de deperciation pour les resizes des images  
warnings.filterwarnings("ignore", category=DeprecationWarning) 

# tableau contenant les coordonées(x) des obstacles 
obstacles = []
# taille scène
longueur_scene_graphique = 1000
largeur_scene_graphique = 250
stage = ""
#tableau contenant les images 
images = []
init_coord_j1 = 0
init_coord_j2 = 0
# variable pour arrèter le thread
stop = False
# variable pour dire quand il y a rafraichissement
verrou_refresh = threading.Lock() # pour éviter que tout les threads accède à la variable en meme temps
rafraichissement = False  

############################################################################################################################################################
############################################################################################################################################################

class frames_refresh_graphique (threading.Thread): # thread qui rafraichi la page
    def __init__(self, scene, number_refresh):
        threading.Thread.__init__(self)  # appel au constructeur de la classe mère
        self.number_refresh = number_refresh
        self.scene = scene

    def run(self):
        global rafraichissement,verrou_refresh
        while (stop != True):   # continue le rafraichissement tant que la variable stop ne passe pas à True
            x = 1/int(self.number_refresh)
            time.sleep(1/int(self.number_refresh))
            verrou_refresh.acquire()
            rafraichissement = True
            verrou_refresh.release()
            time.sleep(0.00001)
            verrou_refresh.acquire()
            rafraichissement = False
            verrou_refresh.release()
    

class thread_attack_graphique (threading.Thread): # thread qui attend attacking_speed frames avant d'attaquer  
    def __init__(self, score, scene,joueur1,joueur2, joueur_appelant_thread):
        threading.Thread.__init__(self)  # appel au constructeur de la classe mère
        self.score = score
        self.scene = scene
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.joueur_appelant_thread = joueur_appelant_thread # permet de savoir quel joueur appel le thread

    def run(self):
        global stage
        global rafraichissement,verrou_refresh
        self.joueur_appelant_thread.state = "Attack"
        affiche_scene_graphique(self.scene,self.joueur1,self.joueur2)
        i = 0
        while (i != self.joueur_appelant_thread.attacking_speed):   # on attend attacking_speed rafraichissements pour atteindre l'adverssaire (pendant ce temps l'dvesaire pourra l'exquiver)
            verrou_refresh.acquire()
            if rafraichissement == True:
                i += 1
            verrou_refresh.release()

        if (self.joueur1 == self.joueur_appelant_thread): # attack du joueur 1
            if ((self.joueur1.coords_joueur[0]+70+(self.joueur1.attacking_range*10)) >= (self.joueur2.coords_joueur[0])):
                if(self.joueur2.state == "Block"):
                    if((self.joueur1.coords_joueur[0])<(self.joueur2.coords_joueur[0]-(self.joueur2.defending_range*10))):
                        self.joueur1.score = self.joueur1.score + 1
                        affiche_score_graphique(self.score,self.joueur1,self.joueur2)
                        self.joueur1.coords_joueur = (init_coord_j1, self.joueur1.coords_joueur[1])
                        affiche_scene_graphique(self.scene,self.joueur1,self.joueur2)
                else:
                    self.joueur1.score = self.joueur1.score + 1
                    affiche_score_graphique(self.score,self.joueur1,self.joueur2)
                    self.joueur1.coords_joueur = (init_coord_j1, self.joueur1.coords_joueur[1]) # remet le joueur à ses coordonées initiales
                    self.joueur2.coords_joueur = (init_coord_j2, self.joueur2.coords_joueur[1]) # remet le joueur à ses coordonées initiales
                    affiche_scene_graphique(self.scene,self.joueur1,self.joueur2)
        elif (self.joueur2 == self.joueur_appelant_thread):   # attack du joueur 2
            if ((self.joueur2.coords_joueur[0]-(self.joueur2.attacking_range*10)) <= (self.joueur1.coords_joueur[0]+70)):
                if(self.joueur1.state == "Block"):
                    if((self.joueur2.coords_joueur[0])>(self.joueur1.coords_joueur[0]+70+(self.joueur1.defending_range*10))):
                        self.joueur2.score = self.joueur2.score + 1
                        affiche_score_graphique(self.score,self.joueur1,self.joueur2)
                        self.joueur2.coords_joueur = (init_coord_j2, self.joueur2.coords_joueur[1])
                        affiche_scene_graphique(self.scene,self.joueur1,self.joueur2)
                else:
                    self.joueur2.score = self.joueur2.score + 1
                    affiche_score_graphique(self.score,self.joueur1,self.joueur2)
                    self.joueur1.coords_joueur = (init_coord_j1, self.joueur1.coords_joueur[1]) # remet le joueur à ses coordonées initiales
                    self.joueur2.coords_joueur = (init_coord_j2, self.joueur2.coords_joueur[1]) # remet le joueur à ses coordonées initiales
                    affiche_scene_graphique(self.scene,self.joueur1,self.joueur2)
        
        self.joueur_appelant_thread.state = "Rest"
        affiche_scene_graphique(self.scene,self.joueur1,self.joueur2)
        self.scene.update()


class thread_block_graphique (threading.Thread): # thread qui block pendant bloking_time
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
        affiche_scene_graphique(self.scene,self.joueur1,self.joueur2)
        

############################################################################################################################################################
############################################################################################################################################################
# la classe joueur avec ses attributs
class joueur_graphique:
    def __init__(self, mouvement_speed =1, attacking_speed=1, attacking_range=1, defending_range=1, blocking_time=1):
        self.mouvement_speed = mouvement_speed
        self.attacking_speed = attacking_speed
        self.attacking_range = attacking_range
        self.defending_range = defending_range
        self.blocking_time = blocking_time
        self.score = 0
        self.state = "Rest"
        self.coords_score = (0,0)
        self.coords_joueur = (0,9)
        self.image = None

class joueur_1_graphique (joueur_graphique): # player 1
    def __init__(self, mouvement_speed, attacking_speed, attacking_range, defending_range, blocking_time):
        super().__init__(mouvement_speed, attacking_speed, attacking_range, defending_range, blocking_time)


class joueur_2_graphique (joueur_graphique): # player 2
    def __init__(self, mouvement_speed, attacking_speed, attacking_range, defending_range, blocking_time):
        super().__init__(mouvement_speed, attacking_speed, attacking_range, defending_range, blocking_time)

############################################################################################################################################################
############################################################################################################################################################
#fonction qui affiche toutes les commandes
def affiche_commande_graphique(commande):

    str = "Commande joueur 1 | Commande joueur 2"
    half_length_of_message = int(len(str) / 2)
    middle_column = int(100 / 2)
    x_position = middle_column - half_length_of_message
    Label(commande, text=str, fg="blue").pack(padx=x_position, pady=1, side=TOP)

    str = "               Déplacement droite: 'd' | Déplacement droite: 'Key_Right'"
    half_length_of_message = int(len(str) / 2)
    middle_column = int(100 / 2)
    x_position = middle_column - half_length_of_message
    Label(commande, text=str).pack(padx=x_position, pady=1, side=TOP)

    str = "               Déplacement gauche: 'q' | Déplacement gauche: 'Key_Left'"
    half_length_of_message = int(len(str) / 2)
    middle_column = int(100 / 2)
    x_position = middle_column - half_length_of_message
    Label(commande, text=str).pack(padx=x_position, pady=1, side=TOP)

    str = "Saut droite: 'e' | Saut droite: 'm'"
    half_length_of_message = int(len(str) / 2)
    middle_column = int(100 / 2)
    x_position = middle_column - half_length_of_message
    Label(commande, text=str).pack(padx=x_position, pady=1, side=TOP)

    str = "Saut gauche: 'a' | Saut gauche: 'l'"
    half_length_of_message = int(len(str) / 2)
    middle_column = int(100 / 2)
    x_position = middle_column - half_length_of_message
    Label(commande, text=str).pack(padx=x_position, pady=1, side=TOP)

    str = "Attaquer: 'z' | Attaquer: 'o'"
    half_length_of_message = int(len(str) / 2)
    middle_column = int(100 / 2)
    x_position = middle_column - half_length_of_message
    Label(commande, text=str).pack(padx=x_position, pady=1, side=TOP)

    str = "Bloquer: 's' | Bloquer: 'p'"
    half_length_of_message = int(len(str) / 2)
    middle_column = int(100 / 2)
    x_position = middle_column - half_length_of_message
    Label(commande, text=str).pack(padx=x_position, pady=1, side=TOP)

############################################################################################################################################################
############################################################################################################################################################
#fonction qui affiche le score
def affiche_score_graphique(score,joueur1,joueur2):

    for widget in score.winfo_children():
        widget.destroy()

    Label(score, text="SCORE").pack(padx=10, pady=10, side=TOP)
    Label(score, text=joueur1.score).pack(padx=10, pady=5, side=LEFT)
    Label(score, text=" | ").pack(padx=10, pady=5, side=LEFT)
    Label(score, text=joueur2.score).pack(padx=10, pady=5, side=LEFT)

############################################################################################################################################################
############################################################################################################################################################
#fonction qui affiche la scene
def affiche_scene_graphique(scene, joueur1, joueur2, stage = ""):
    global images
    global init_coord_j1, init_coord_j2

    scene.delete('all') # supprime tout ce qu'il y a dans le canvas
    scene.delete(joueur1.image) 
    scene.delete(joueur2.image)
    
    for i in range (0,longueur_scene_graphique,10):
        scene.create_text(i, 200, text="#", font="bold")


    if(stage != ""): # pour le premier affichage
        for i in range (len(stage)):
            if (stage[i] == "1"):
                joueur1.coords_joueur = (i*10, joueur1.coords_joueur[1]*10)
                init_coord_j1 = i*10
            elif(stage[i] == "2"):
                joueur2.coords_joueur = (i*10, joueur2.coords_joueur[1]*10)
                init_coord_j2 = i*10
            elif(stage[i] == "x"):
                scene.create_text(i*10, 180, text="X", font="bold")
                obstacles.append(i*10)
        joueur1.state = "Rest"
        joueur2.state = "Rest"
    else:
        for i in obstacles:
            scene.create_text(i*10, 180, text="X", font="bold")

    x1 = joueur1.coords_joueur[0]
    y1 = joueur1.coords_joueur[1]

    for i in obstacles:
        scene.create_text(i, 180, text="X", font="bold")

    if joueur1.state == "Attack":
        joueur1.image = scene.create_image(x1, y1, anchor=NW, image=images[0])
    elif joueur1.state == "Block":
        joueur1.image = scene.create_image(x1, y1, anchor=NW, image=images[1])
    elif joueur1.state == "Rest":
        joueur1.image = scene.create_image(x1, y1, anchor=NW, image=images[2])
    elif joueur1.state == "Jump":
        joueur1.image = scene.create_image(x1, y1, anchor=NW, image=images[3])
    
    x2 = joueur2.coords_joueur[0]
    y2 = joueur2.coords_joueur[1]

    if joueur2.state == "Attack":
        joueur2.image = scene.create_image(x2, y2, anchor=NW, image=images[4])
    elif joueur2.state == "Block":
        joueur2.image = scene.create_image(x2, y2, anchor=NW, image=images[5])
    elif joueur2.state == "Rest":
        joueur2.image = scene.create_image(x2, y2, anchor=NW, image=images[6])
    elif joueur2.state == "Jump":
        joueur2.image = scene.create_image(x2, y2, anchor=NW, image=images[7])
    

############################################################################################################################################################
############################################################################################################################################################
# fonction qui réalise les mouvements du joueur 
def mouvement_joueur_graphique(event, scores, sc, j1, j2):
    global images
    global rafraichissement, verrou_refresh

    touche = event.keysym
    if touche == "q": # mouvement gauche joueur 1
        i=0##############################
        while (i!=j1.mouvement_speed): # attend le rafraichissement 
            verrou_refresh.acquire()#####
            if rafraichissement == True:#
                i+=1#####################
            verrou_refresh.release()#####
        ################################
        if (j1.coords_joueur[0]-10 < 0): # si le joueur se déplace hors de la scène
            return
        if(j1.coords_joueur[0]-10 in obstacles): # si il y a obstacle 
            return 
        j1.coords_joueur = (j1.coords_joueur[0]-10, j1.coords_joueur[1]) 
        sc.coords(j1.image, j1.coords_joueur[0], j1.coords_joueur[1])
    elif touche == "d": # mouvement droite joueur 1
        i=0##############################
        while (i!=j1.mouvement_speed): # attend le rafraichissement 
            verrou_refresh.acquire()#####
            if rafraichissement == True:#
                i+=1#####################
            verrou_refresh.release()#####
        #################################
        if (j1.coords_joueur[0]+10 > longueur_scene_graphique): # si le joueur se déplace hors de la scène
            return
        if(j1.coords_joueur[0]+80 == j2.coords_joueur[0]): # si l'aversaire est juste en face 
            return 
        if(j1.coords_joueur[0]+80 in obstacles): # si il y a obstacle 
            return 
        j1.coords_joueur = (j1.coords_joueur[0]+10, j1.coords_joueur[1]) 
        sc.coords(j1.image, j1.coords_joueur[0], j1.coords_joueur[1])
    elif touche == 'a': # saut gauche joueur 1
        if (j1.coords_joueur[0]-80 < 0): # si le joueur se déplace hors de la scène
            return
        j1.state = "Jump"
        affiche_scene_graphique(sc,j1,j2)
        i=0##############################
        while (i!=j1.mouvement_speed): # attend le rafraichissement 
            verrou_refresh.acquire()#####
            if rafraichissement == True:#
                i+=1#####################
            verrou_refresh.release()#####
        #################################
        j1.coords_joueur = (j1.coords_joueur[0], j1.coords_joueur[1]-10) 
        sc.update() 
        i=0##############################
        while (i!=j1.mouvement_speed): # attend le rafraichissement 
            verrou_refresh.acquire()#####
            if rafraichissement == True:#
                i+=1#####################
            verrou_refresh.release()#####
        #################################
        j1.coords_joueur = (j1.coords_joueur[0]-90, j1.coords_joueur[1]) 
        sc.update() 
        i=0##############################
        while (i!=j1.mouvement_speed): # attend le rafraichissement 
            verrou_refresh.acquire()#####
            if rafraichissement == True:#
                i+=1#####################
            verrou_refresh.release()#####
        #################################
        j1.coords_joueur = (j1.coords_joueur[0], j1.coords_joueur[1]+10) 
        j1.state = "Rest"
        affiche_scene_graphique(sc,j1,j2)
    elif touche == 'e': # saut droite joueur 1
        if (j1.coords_joueur[0]+80 > longueur_scene_graphique): # si le joueur se déplace hors de la scène
            return
        if(j1.coords_joueur[0]+80 == j2.coords_joueur[0]): # si l'aversaire est juste en face 
            return
        j1.state = "Jump"
        affiche_scene_graphique(sc,j1,j2)
        i=0##############################
        while (i!=j1.mouvement_speed): # attend le rafraichissement 
            verrou_refresh.acquire()#####
            if rafraichissement == True:#
                i+=1#####################
            verrou_refresh.release()#####
        #################################
        j1.coords_joueur = (j1.coords_joueur[0], j1.coords_joueur[1]-10) 
        sc.update() 
        i=0##############################
        while (i!=j1.mouvement_speed): # attend le rafraichissement 
            verrou_refresh.acquire()#####
            if rafraichissement == True:#
                i+=1#####################
            verrou_refresh.release()#####
        #################################
        j1.coords_joueur = (j1.coords_joueur[0]+90, j1.coords_joueur[1]) 
        sc.update() 
        i=0##############################
        while (i!=j1.mouvement_speed): # attend le rafraichissement 
            verrou_refresh.acquire()#####
            if rafraichissement == True:#
                i+=1#####################
            verrou_refresh.release()#####
        #################################
        j1.coords_joueur = (j1.coords_joueur[0], j1.coords_joueur[1]+10) 
        j1.state = "Rest"
        affiche_scene_graphique(sc,j1,j2)
    elif touche == "z": # mouvement attaque joueur 1 
        th = thread_attack_graphique(scores, sc,j1,j2, j1)
        th.start()
    elif touche == "s": # mouvement block joueur 1
        j1.state = "Block"
        affiche_scene_graphique(sc,j1,j2)
        th = thread_block_graphique(sc,j1,j2, j1)
        th.start()

    #######################################################################################################################
    
    elif touche == "Left": # mouvement gauche joueur 2
        i=0##############################
        while (i!=j2.mouvement_speed): # attend le rafraichissement 
            verrou_refresh.acquire()#####
            if rafraichissement == True:#
                i+=1#####################
            verrou_refresh.release()#####
        #################################
        if (j2.coords_joueur[0]-10 < 0): # si le joueur se déplace hors de la scène
            return
        if(j2.coords_joueur[0]-10 == j1.coords_joueur[0]+70): # si l'aversaire est juste en face 
            return 
        if(j2.coords_joueur[0]-10 in obstacles): # si il y a obstacle 
            return 
        j2.coords_joueur = (j2.coords_joueur[0]-10, j2.coords_joueur[1])  
        sc.coords(j2.image, j2.coords_joueur[0], j2.coords_joueur[1])
    elif touche == "Right": # mouvement droite joueur 2
        i=0##############################
        while (i!=j2.mouvement_speed): # attend le rafraichissement 
            verrou_refresh.acquire()#####
            if rafraichissement == True:#
                i+=1#####################
            verrou_refresh.release()#####
        #################################
        if (j2.coords_joueur[0]+80 > longueur_scene_graphique): # si le joueur se déplace hors de la scène
            return
        if(j2.coords_joueur[0]+10 in obstacles): # si il y a obstacle 
            return
        j2.coords_joueur = (j2.coords_joueur[0]+10, j2.coords_joueur[1]) 
        sc.coords(j2.image, j2.coords_joueur[0], j2.coords_joueur[1])
    elif touche == 'l': # saut gauche joueur 2
        if (j2.coords_joueur[0]-90 < 0): # si le joueur se déplace hors de la scène
            return
        if(j2.coords_joueur[0]-90 == j1.coords_joueur[0]): # si l'aversaire est juste en face 
            return
        j2.state = "Jump"
        affiche_scene_graphique(sc,j1,j2)
        i=0##############################
        while (i!=j2.mouvement_speed): # attend le rafraichissement 
            verrou_refresh.acquire()#####
            if rafraichissement == True:#
                i+=1#####################
            verrou_refresh.release()#####
        #################################
        j2.coords_joueur = (j2.coords_joueur[0], j2.coords_joueur[1]-10) 
        sc.update() 
        i=0##############################
        while (i!=j2.mouvement_speed): # attend le rafraichissement 
            verrou_refresh.acquire()#####
            if rafraichissement == True:#
                i+=1#####################
            verrou_refresh.release()#####
        #################################
        j2.coords_joueur = (j2.coords_joueur[0]-90, j2.coords_joueur[1]) 
        sc.update() 
        i=0##############################
        while (i!=j2.mouvement_speed): # attend le rafraichissement 
            verrou_refresh.acquire()#####
            if rafraichissement == True:#
                i+=1#####################
            verrou_refresh.release()#####
        #################################
        j2.coords_joueur = (j2.coords_joueur[0], j2.coords_joueur[1]+10) 
        j2.state = "Rest"
        affiche_scene_graphique(sc,j1,j2)
    elif touche == 'm': # saut droite joueur 2
        if (j2.coords_joueur[0]+90 > longueur_scene_graphique): # si le joueur se déplace hors de la scène
            return
        j2.state = "Jump"
        affiche_scene_graphique(sc,j1,j2)
        i=0##############################
        while (i!=j2.mouvement_speed): # attend le rafraichissement 
            verrou_refresh.acquire()#####
            if rafraichissement == True:#
                i+=1#####################
            verrou_refresh.release()#####
        #################################
        j2.coords_joueur = (j2.coords_joueur[0], j2.coords_joueur[1]-10) 
        sc.update() 
        i=0##############################
        while (i!=j2.mouvement_speed): # attend le rafraichissement 
            verrou_refresh.acquire()#####
            if rafraichissement == True:#
                i+=1#####################
            verrou_refresh.release()#####
        #################################
        j2.coords_joueur = (j2.coords_joueur[0]+90, j2.coords_joueur[1]) 
        sc.update() 
        i=0##############################
        while (i!=j2.mouvement_speed): # attend le rafraichissement 
            verrou_refresh.acquire()#####
            if rafraichissement == True:#
                i+=1#####################
            verrou_refresh.release()#####
        #################################
        j2.coords_joueur = (j2.coords_joueur[0], j2.coords_joueur[1]+10) 
        j2.state = "Rest"
        affiche_scene_graphique(sc,j1,j2)
    elif touche == "o": # mouvement attaque joueur 2
        th = thread_attack_graphique(scores, sc,j1,j2, j2)
        th.start()
    elif touche == "p": # mouvement block joueur 2
        j2.state = "Block"
        affiche_scene_graphique(sc,j1,j2)
        th = thread_block_graphique(sc,j1,j2, j1)
        th.start()

############################################################################################################################################################
############################################################################################################################################################
# fonction qui enregistre la partie dans un fichier
def enregistrer_partie_graphique(joueur1,joueur2):
    myFile = open("./parties_enregistrees/partie_save.txt", "w+")
    temp = ""
    list_obstacle = [i/10 for i in obstacles]
    for i in range(1, 101):
        if i == (joueur1.coords_joueur[0]/10):
            temp += "1"
        elif i == (joueur2.coords_joueur[0]/10):
            temp += "2"
        elif i in list_obstacle:
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
    myFile.write(' '+str(joueur1.score))
    myFile.close()

############################################################################################################################################################
############################################################################################################################################################

# fonction pricipale de la version graphique
def main_graphique(scene, joueur1, joueur2, number_refresh):
    global stop, stage, images

    stage = scene

    fenetre = Tk()
    fenetre.geometry('1050x500')
    fenetre.title("Fancy Fencing")    

    score = Frame(fenetre, borderwidth=4, relief=GROOVE)
    score.place(relx=0.6, rely=0.1)

    affiche_score_graphique(score,joueur1,joueur2)

    commande = Frame(fenetre, borderwidth=2, relief=GROOVE)
    commande.place(relx=0.15, rely=0.01)

    affiche_commande_graphique(commande)

    logo = Image.open("./images_graphique/logo.png")
    logo = logo.resize((200,200), Image.ANTIALIAS)
    logo = ImageTk.PhotoImage(logo)
    Label(fenetre, image=logo).place(relx=0.75, rely=0.0)


    img = Image.open("./images_graphique/joueur1_attack.png")
    img = img.resize((75,100), Image.ANTIALIAS)
    images.append(ImageTk.PhotoImage(img))
    img = Image.open("./images_graphique/joueur1_block.png")
    img = img.resize((75,100), Image.ANTIALIAS)
    images.append(ImageTk.PhotoImage(img))
    img = Image.open("./images_graphique/joueur1_rest.png")
    img = img.resize((75,100), Image.ANTIALIAS)
    images.append(ImageTk.PhotoImage(img))
    img = Image.open("./images_graphique/joueur1_jump.png")
    img = img.resize((75,100), Image.ANTIALIAS)
    images.append(ImageTk.PhotoImage(img))
    img = Image.open("./images_graphique/joueur2_attack.png")
    img = img.resize((75,100), Image.ANTIALIAS)
    images.append(ImageTk.PhotoImage(img))
    img = Image.open("./images_graphique/joueur2_block.png")
    img = img.resize((75,100), Image.ANTIALIAS)
    images.append(ImageTk.PhotoImage(img))
    img = Image.open("./images_graphique/joueur2_rest.png")
    img = img.resize((75,100), Image.ANTIALIAS)
    images.append(ImageTk.PhotoImage(img))
    img = Image.open("./images_graphique/joueur2_jump.png")
    img = img.resize((75,100), Image.ANTIALIAS)
    images.append(ImageTk.PhotoImage(img))

    scene = Canvas(fenetre, width=longueur_scene_graphique, height=largeur_scene_graphique, background='white')
    scene.place(relx=0.025, rely=0.4)
    
    affiche_scene_graphique(scene, joueur1,joueur2, stage)

    refresh_th = frames_refresh_graphique(scene, number_refresh)
    refresh_th.start()

    Button(fenetre, text="Quitter", command = fenetre.destroy).place(relx=0.02, rely=0.1) # boutton pour quitter
    Button(fenetre, text="Enregistrer", command = enregistrer_partie_graphique(joueur1,joueur2)).place(relx=0.02, rely=0.2) # boutton pour enregistrer la partie

    scene.focus_set()
    scene.bind("<Key>", lambda event, scores= score, sc=scene,j1=joueur1,j2=joueur2: mouvement_joueur_graphique(event,scores, sc,j1,j2))

    fenetre.mainloop()
    stop = True

