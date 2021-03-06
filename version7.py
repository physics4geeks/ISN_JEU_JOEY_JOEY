﻿from tkinter import *
import time

# Version 1 : Dessin du décors
# Version 2 : On place la souris, que l'on autorise à se déplacer partout pour le moment
# Version 3 : On autorise ou non le déplacement de la souris selon le décors
# Version 4 : Animation de la souris
# Version 5 : Même travail avec le chat
# Version 6 : On teste si la souris mange un cupcake et si elle se fait manger
# Version 7 : On gère les trous à l'appuie de la touche espace. Pour cela, on crée
#               une liste Trou vide au début. A chaque fois que l'on fait un trou
#               on ajoute 4 informations : le temps, la ligne, la colone (pour reboucher)
#               et l'adresse mémoire du rectangle bleu (pour l'effacer)

# Quand on appuie sur une touche, on l'ajoute à la liste
def enfoncee(evt) :
    T = evt.keysym.upper() # En majuscule pour confondre 'a' et 'A'
    if  T not in Touches :
        Touches.append(T)

# Quand on relache la touche, on la retire
def relachee(evt) :
    T = evt.keysym.upper()
    if T in Touches :
        Touches.remove(T)

# Boucle principale :
def animation() :
    global XS, YS, AnimS, XC, YC, AnimC, NBcup, direction

    Xavant, Yavant = XS, YS
    if "UP" in Touches :
        # On regarde si on se situe sur une échelle :
        if Decors[YS//40][XS//40] == 'H' :
            YS = YS - 8
            NomFichier = 'sourisFICHIERM'
    if "DOWN" in Touches :
        # On regarde si on a une échelle sous les pieds ( La souris mesure
        # 40 pixels de haut, on regarde donc à YS + 19 + 8
        if Decors[(YS+27)//40][XS//40] == 'H' :
            YS = YS + 8
            NomFichier = 'sourisFICHIERM'
    if "LEFT" in Touches :
        # On regarde ce qu'il y a au pied gauche de la souris : La souris fait
        # 30 pixels de large et 40 pixels de haut, on regarde donc la case qui
        # se situe à (XS - 15 - 8 , YS + 19)
        if Decors[(YS+19)//40][(XS-23)//40] in (' ','P','H') :
            XS = XS - 8
            NomFichier = 'sourisFICHIERG'
            direction = 1
    if "RIGHT" in Touches :
        # Idem à droite
        if Decors[(YS+19)//40][(XS+23)//40] in (' ','P','H') :
            XS = XS + 8
            NomFichier = 'sourisFICHIERD'
            direction = -1
    # On regarde si on tombe :
    if Decors[(YS+20)//40][(XS)//40] in (' ','P') :
        YS = YS + 8
        NomFichier = 'sourisFICHIERT'
    # Animation de la souris
    if (Xavant, Yavant) != (XS, YS) :
        AnimS = 1 - AnimS   # Si Anims vallait 0, elle vaut 1 et inversement
        Fond.itemconfigure(souris, image=eval(NomFichier+str(AnimS))) # Magique cette fonction eval !
    Fond.coords(souris, XS, YS)


    Xavant, Yavant = XC, YC
    if "A" in Touches :
        if Decors[YC//40][XC//40] == 'H' :
            YC = YC - 8
            NomFichier = 'chatFICHIERM'
    if "Q" in Touches :
        if Decors[(YC+27)//40][XC//40] == 'H' :
            YC = YC + 8
            NomFichier = 'chatFICHIERM'
    if "S" in Touches :
        if Decors[(YC+19)//40][(XC-23)//40] in (' ','P','H') :
            XC = XC - 8
            NomFichier = 'chatFICHIERG'
    if "D" in Touches :
        if Decors[(YC+19)//40][(XC+23)//40] in (' ','P','H') :
            XC = XC + 8
            NomFichier = 'chatFICHIERD'
    if Decors[(YC+20)//40][(XC)//40] in (' ','P') :
        YC = YC + 8
        NomFichier = 'chatFICHIERT'
    if (Xavant, Yavant) != (XC, YC) :
        AnimC = 1 - AnimC
        Fond.itemconfigure(chat, image=eval(NomFichier+str(AnimC)))
    Fond.coords(chat, XC, YC)

    # On mange un cupcake ?
    if Decors[YS//40][XS//40] == 'P' :
        Decors[YS//40][XS//40] = ' '
        # On efface le cupcake
        col, lig = (XS // 40) * 40, (YS // 40) * 40
        Fond.create_rectangle(col,lig,col + 39, lig + 39, fill="#BBBBF9", outline="#BBBBF9")
        Fond.tag_raise(souris)
        Fond.tag_raise(chat)
        NBcup = NBcup + 1
        texte = str(NBcup)+" cupcake"
        if NBcup > 1 : texte = texte + "s"
        texte = texte +" sur 5"
        Fond.itemconfig(Txt,text=texte)

    # On creue un trou ?
    if 'SPACE' in Touches and len(Trous) < 4 * 5 :
        l, c = YS // 40 + 1 , XS // 40 - direction
        if Decors[l][c] == 'T' :
            Decors[l][c] = ' '
            Trous.append(time.time())
            Trous.append(l)
            Trous.append(c)
            Trous.append(Fond.create_rectangle(c*40, l*40, c*40+39,l*40 + 39, fill="#BBBBF9", outline="#BBBBF9"))
            Fond.tag_raise(souris)
            Fond.tag_raise(chat)

    # Un trou à reboucher ?
    i = 0
    while i < len(Trous) :
        if time.time()-Trous[i] > 5 :
            Fond.delete(Trous[i+3])
            Decors[Trous[i+1]][Trous[i+2]] = 'T'
            for j in range(4) : Trous.pop(i)
        else :
            i = i + 4

    # Le chat mange la souris ? (On considère que se sont 2 boules de rayon 15)
    d = (XS - XC)**2 + (YS - YC)**2
    if d < 900 :
        Fond.create_text(600,340,text="PERDU", fill='black', font=("Arial",200))
    elif NBcup == 5 :
        Fond.create_text(600,340,text="GAGNE", fill='black', font=("Arial",200))
    else :
        fenetre.after(40,animation)

def lisDecors(fichier):
    """
    Fonction qui lis le contenu du fichier fichier et la place dans
    la liste 2D Decors
    """
    filin = open(fichier,'r')
    R = [list(line.replace('\n','')) for line in filin]
    filin.close()
    return R

def dessine():
    """
    Fonction qui dessine le plateau de jeu avec les données de la liste Decors
    """
    global XS, YS, XC, YC
    ligne, colonne = 0, 0
    while ligne < 17 :
      if Decors[ligne][colonne] == 'X' :
        Fond.create_image(colonne*40, ligne*40, image=X, anchor=NW)
      if Decors[ligne][colonne] == 'T' :
        Fond.create_image(colonne*40, ligne*40, image=T, anchor=NW)
      if Decors[ligne][colonne] == 'H' :
        Fond.create_image(colonne*40, ligne*40, image=H, anchor=NW)
      if Decors[ligne][colonne]=='P' :
        Fond.create_image(colonne*40, ligne*40, image=P, anchor=NW)
      if Decors[ligne][colonne] == 'S' :    # Si on a une souris dans le décors
        XS, YS = colonne*40+20, ligne*40+20 # On initialise les coordonnées
        Decors[ligne][colonne] = ' '        # On l'efface du décors
      if Decors[ligne][colonne] == 'C' :
        XC, YC = colonne*40+20, ligne*40+20
        Decors[ligne][colonne] = ' '
      colonne=colonne+1
      if colonne == 25 :
        colonne = 0
        ligne = ligne + 1


fenetre=Tk()
fenetre.resizable(width=False, height=False)

fenetre.title("Joe & Joey")
fenetre.geometry("1200x680")

# Chargement des fichiers :
T=PhotoImage(file="images/FondS.gif")
H=PhotoImage(file="images/FondH.gif")
X=PhotoImage(file="images/FondX.gif")
P=PhotoImage(file="images/pancake.gif")

# Dessin de l'interface
Fond=Canvas(fenetre,width=1200,height=680,bg="#C0C0FF")
Fond.place(x=0,y=0)
Fond.create_rectangle(1000,0,1200,680,fill="grey",width=5,outline="white")
Fond.create_image(1100,225,image=P)
Txt=Fond.create_text(1100,275,text="0 cupcake sur 5",font=("comic sans ms","15"),fill="#5736A6")

# Informations sur la souris :
sourisFICHIERG0=PhotoImage(file="images/sourisG0.gif") #fichier de la souris gauche position 0
sourisFICHIERD0=PhotoImage(file="images/sourisD0.gif") #fichier de la souris droite position 0
sourisFICHIERG1=PhotoImage(file="images/sourisG1.gif") #fichier de la souris gauche position 1
sourisFICHIERD1=PhotoImage(file="images/sourisD1.gif") #fichier de la souris droite position 1
sourisFICHIERM0=PhotoImage(file="images/sourisM0.gif") #fichier de la souris monte position 1
sourisFICHIERM1=PhotoImage(file="images/sourisM1.gif") #fichier de la souris monte position 1
sourisFICHIERT0=PhotoImage(file="images/sourisT0.gif") #fichier du souris qui tombe
sourisFICHIERT1=PhotoImage(file="images/sourisT1.gif") #fichier du souris qui tombe
XS, YS = 0, 0   # Position
AnimS = 0       # Animation de la souris (0 ou 1)

# Informations sur le chat :
chatFICHIERG0=PhotoImage(file="images/chatG0.gif") #fichier du chat gauche position 0
chatFICHIERD0=PhotoImage(file="images/chatD0.gif") #fichier du chat droite position 0
chatFICHIERG1=PhotoImage(file="images/chatG1.gif") #fichier du chat gauche position 1
chatFICHIERD1=PhotoImage(file="images/chatD1.gif") #fichier du chat droite position 1
chatFICHIERM0=PhotoImage(file="images/chatM0.gif") #fichier du chat monte position 1
chatFICHIERM1=PhotoImage(file="images/chatM1.gif") #fichier du chat monte position 1
chatFICHIERT0=PhotoImage(file="images/chatT0.gif") #fichier du chat qui tombe
chatFICHIERT1=PhotoImage(file="images/chatT1.gif") #fichier du chat qui tombe
XC, YC = 0, 0   # Position
AnimC = 0       # Animation de la souris (0 ou 1)

# On lis le décors. On garde les informations du décors dans une liste pour
# pouvoir tester si on tombe, si on peut monter, ....
Decors = lisDecors('niveaux/niv1.txt')
dessine()

souris=Fond.create_image(XS, YS, image=sourisFICHIERG0)
chat=Fond.create_image(XC, YC, image=chatFICHIERG0)
NBcup = 0
Trous = []
direction = 1 # Pour savoir où creuser le trou : 1=Gauche, -1=Droite)

# Surveillance des touches
Touches = []
fenetre.bind_all("<KeyPress>",enfoncee)
fenetre.bind_all("<KeyRelease>",relachee)

animation()

fenetre.mainloop()