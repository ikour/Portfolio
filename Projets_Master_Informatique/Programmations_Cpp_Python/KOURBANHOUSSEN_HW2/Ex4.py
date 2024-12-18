
def make_histo(name_file, nbin=20, height=20):
    tab_valeurs = [] # table avec toutes les valeurs contenue dans le fichier passé en paramètre
    dico_histogram = {} # dictionnaire => exemple : {bin : nombre d'étoiles}

    #ajoute tout les float du fichier dans le tableau tab_valeur
    with open(name_file) as my_file:
        for line in my_file:
            x = line.split()
            for i in x:
                if i == x:
                    tab_valeurs.append(float(i)) # car pas de virgule a^rès le dernier float
                    break
                i = i[:-1]
                tab_valeurs.append(float(i))

    valeur_min = min(tab_valeurs)
    valeur_max = max(tab_valeurs)

    distance_entre_nbin = (valeur_max-valeur_min)/nbin

    # mets toutes les nbin de l'histogramme espacé d'une valeur (calculé en fonction du nbin passé en paramètre)
    temp = valeur_min
    for i in range (nbin): 
        dico_histogram[temp] = 0
        temp += distance_entre_nbin

    #on calcule le nombres de valeurs qui ont la mème limite (le meme bin)
    #on calcule qu'elle nbin est le plus proche parmis les nbin présents dans le dictionnaire
    #dico_histogram = {bin x : nombre de valeurs qui ont leurs limites à x}
    for valeur in tab_valeurs:
        dist_nbin_proche = valeur_max
        nbin_proche = valeur_max
        for key in dico_histogram:
            if (valeur-key)<dist_nbin_proche:
                if (valeur-key)>=0:
                    dist_nbin_proche = valeur-key
                    nbin_proche = key
                else:
                    break
        if dico_histogram.get(nbin_proche) != None:
            dico_histogram[nbin_proche] = dico_histogram.get(nbin_proche)+1
        else:
            dico_histogram[nbin_proche] = 1
        
    #on ré-adapte le nombres d'étoiles en fonction de la valeur du height passé en paramètre 
    nbin_max = max(dico_histogram.values())
    for key in dico_histogram:
        dico_histogram[key] = int((dico_histogram[key]*height)/nbin_max)

    #Affichage de l'histigramme
    for y in range (height, 0, -1):
        for x in dico_histogram:
            if dico_histogram[x] >= y:
                print(" * ", end='')
            else:
                print("   ", end='')
        print("")

    #Affichage de la dernière ligne de l'histogramme avec l'ensemble des bins
    for x in dico_histogram:
        if int(x)<10:
            print(int(x), " ", end='')
        else:
            print(int(x), "", end='')
    print(int(valeur_max)) # nbin+1 valeur sur la dernière ligne

    return 0

