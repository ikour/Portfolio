# *****KOURBANHOUSSEN Idriss*****

# fichier principale main 


from version_terminal import *
from version_graphique import *
import os
from curses import wrapper

joueur1 = 0
joueur2 = 0
number_refresh = 0
scene = ""

if __name__ == "__main__":
    
    print("\nBienvenue sur Jeux d'Escrime !\n")
    choix_version = input("Voulez-vous utiliser jouer sur la version Terminal ou Graphique (T/G)? ")
    number_refresh = input("Combiens d'images par secondes voulez-vous (20 conseillé)? ")
    choix_partie = input("Voulez-vous reprendre la Partie enregistrée (Y/N)? ")

    if (choix_partie == 'Y') | (choix_partie == 'y'): # si l'utilisateur veut continuer le jeu enregistré
        tab = ""
        with open("./parties_enregistrees/partie_save.txt") as my_file:
            for line in my_file:
                tab = line.split()
        
        scene = tab[0]
        mouvement_speed_1 = tab[1]
        attacking_speed_1 = tab[2]
        attacking_range_1 = tab[3]
        defending_range_1 = tab[4]
        blocking_time_1 = tab[5]
        mouvement_speed_2 = tab[6]
        attacking_speed_2 = tab[7]
        attacking_range_2 = tab[8]
        defending_range_2 = tab[9]
        blocking_time_2 = tab[10]
        score_1 = tab[11]
        score_2 = tab[12]
        
        if (choix_version == 'T')|(choix_version == 't'): # si le joueur choisi la version terminal
            joueur1 = joueur_1_terminal(int(mouvement_speed_1),int(attacking_speed_1),int(attacking_range_1),int(defending_range_1), int(blocking_time_1))
            joueur2 = joueur_2_terminal(int(mouvement_speed_2),int(attacking_speed_2),int(attacking_range_2),int(defending_range_2),int(blocking_time_2))
            joueur1.score = int(score_1)
            joueur2.score = int(score_2)
            wrapper(main_terminal, scene, joueur1, joueur2, number_refresh)
            os.system('cls||clear')

        else:   # si le joueur choisi la version graphique
            joueur1 = joueur_1_graphique(int(mouvement_speed_1),int(attacking_speed_1),int(attacking_range_1),int(defending_range_1), int(blocking_time_1))
            joueur2 = joueur_2_graphique(int(mouvement_speed_2),int(attacking_speed_2),int(attacking_range_2),int(defending_range_2),int(blocking_time_2))
            joueur1.score = int(score_1)
            joueur2.score = int(score_2)
            main_graphique(scene, joueur1, joueur2, number_refresh)
            


    else:   # si l'utilisateur veut commencer une nouvelle partie 

        list = os.listdir('./scenes/')
        for i in range(len(list)):
            temp = "./scenes/"+list[i]
            tab = ""
            with open(temp) as my_file:
                for line in my_file:
                    tab = line
            print(str(i)+" : "+tab)

        temp = [str(x) for x in range (len(list))]
        choix_scene = input("\nChoisissez le numéro de la scène : ")
        while (choix_scene not in temp):
            choix_scene = input("Choisissez à nouveaux : ")

        temp = "./scenes/"+list[int(choix_scene)]
        with open(temp) as my_file:
            for line in my_file:
                scene = line

        modfication = input("Voulez-vous modifier les attributs par défauts des joueurs (Y/N) ? ")
        print("\n")
        
        if (choix_version == 'T')|(choix_version == 't'): # si l'utilisateur choisi la version terminal
            if (modfication == 'Y')|(modfication == 'y'): # si l'utilisateur veut modifier les attributs des joueurs
                print("\nAttributs Joueur 1:\n")
                mouvement_speed_1 = input("mouvement_speed : ")
                attacking_speed_1 = input("attacking_speed (100000 conseillé): ")
                attacking_range_1 = input("attacking_range : ")
                defending_range_1 = input("defending_range : ")
                blocking_time_1 = input("blocking_time (100000 conseillé): ")
                print("\nAttributs Joueur 2:\n")
                mouvement_speed_2 = input("mouvement_speed : ")
                attacking_speed_2 = input("attacking_speed (100000 conseillé): ")
                attacking_range_2 = input("attacking_range : ")
                defending_range_2 = input("defending_range : ")
                blocking_time_2 = input("blocking_time (100000 conseillé): ")
                joueur1 = joueur_1_terminal(int(mouvement_speed_1),int(attacking_speed_1),int(attacking_range_1),int(defending_range_1), int(blocking_time_1))
                joueur2 = joueur_2_terminal(int(mouvement_speed_2),int(attacking_speed_2),int(attacking_range_2),int(defending_range_2),int(blocking_time_2))
            else:
                joueur1 = joueur_1_terminal(1,100000,1,1,100000)
                joueur2 = joueur_2_terminal(1,100000,1,1,100000)

            wrapper(main_terminal, scene, joueur1, joueur2, number_refresh)
            os.system('cls||clear')
        
        else:   # si le joueur choisi la version graphique

            if (modfication == 'Y')|(modfication == 'y'): # si l'utilisateur veut modifier les attributs des joueurs
                print("\nAttributs Joueur 1:\n")
                mouvement_speed_1 = input("mouvement_speed (100000 conseillé): ")
                attacking_speed_1 = input("attacking_speed : ")
                attacking_range_1 = input("attacking_range : ")
                defending_range_1 = input("defending_range : ")
                blocking_time_1 = input("blocking_time (100000 conseillé): ")
                print("\nAttributs Joueur 2:\n")
                mouvement_speed_2 = input("mouvement_speed (100000 conseillé): ")
                attacking_speed_2 = input("attacking_speed : ")
                attacking_range_2 = input("attacking_range : ")
                defending_range_2 = input("defending_range : ")
                blocking_time_2 = input("blocking_time (100000 conseillé): ")
                joueur1 = joueur_1_graphique(int(mouvement_speed_1),int(attacking_speed_1),int(attacking_range_1),int(defending_range_1), int(blocking_time_1))
                joueur2 = joueur_2_graphique(int(mouvement_speed_2),int(attacking_speed_2),int(attacking_range_2),int(defending_range_2),int(blocking_time_2))
            else:
                joueur1 = joueur_1_graphique(1,100000,1,1,100000)
                joueur2 = joueur_2_graphique(1,100000,1,1,100000)

            main_graphique(scene, joueur1, joueur2, number_refresh)
    
    os.system('cls||clear')
