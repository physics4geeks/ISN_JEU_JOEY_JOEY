# Créé par VINNI, le 23/02/2013
from tkinter import *

# Version 1 : Dessin du décors
# Version 2 : On place la souris, que l'on autorise à se déplacer partout pour le moment
# Version 3 : On autorise ou non le déplacement de la souris selon le décors
# Version 4 : Animation de la souris

# Quand on appuie sur une touche, on l'ajoute à la liste
def enfoncee(evt) :
    if evt.keysym not in Touches :
        Touches.append(evt.keysym)

# Quand on relache la touche, on la retire
def relachee(evt) :
    if evt.keysym in Touches :
        Touches.remove(evt.keysym)

# Boucle principale :
def animation() :
    global XS, YS, AnimS
    XSavant, YSavant = XS, YS
    if "Up" in Touches :
        # On regarde si on se situe sur une échelle :
        if Decors[YS//40][XS//40] == 'H' :
            YS = YS - 8
            NomFichier = 'sourisFICHIERM'
    if "Down" in Touches :
        # On regarde si on a une échelle sous les pieds ( La souris mesure
        # 40 pixels de haut, on regarde donc à YS + 19 + 8
        if Decors[(YS+27)//40][XS//40] == 'H' :
            YS = YS + 8
            NomFichier = 'sourisFICHIERM'
    if "Left" in Touches :
        # On regarde ce qu'il y a au pied gauche de la souris : La souris fait
        # 30 pixels de large et 40 pixels de haut, on regarde donc la case qui
        # se situe à (XS - 15 - 8 , YS + 19)
        if Decors[(YS+19)//40][(XS-23)//40] in (' ','P','H') :
            XS = XS - 8
            NomFichier = 'sourisFICHIERG'
    if "Right" in Touches :
        # Idem à droite
        if Decors[(YS+19)//40][(XS+23)//40] in (' ','P','H') :
            XS = XS + 8
            NomFichier = 'sourisFICHIERD'
    # On regarde si on tombe :
    if Decors[(YS+20)//40][(XS)//40] in (' ','P') :
        YS = YS + 8
        NomFichier = 'sourisFICHIERT'
    # Animation de la souris
    if (XSavant, YSavant) != (XS, YS) :
        AnimS = 1 - AnimS   # Si Anims vallait 0, elle vaut 1 et inversement
        Fond.itemconfigure(souris, image=eval(NomFichier+str(AnimS))) # Magique cette fonction eval !
    Fond.coords(souris, XS, YS)
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
    global XS, YS
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
Fond=Canvas(fenetre,width=1200,height=680,bg="#5736A6")
Fond.place(x=0,y=0)
Fond.create_rectangle(1000,0,1200,680,fill="grey",width=5,outline="white")
Fond.create_image(1100,225,image=P)
Txt=Fond.create_text(1100,275,text="0 cupcake sur 5",font=("comic sans ms","15"),fill="#5736A6")

# Information sur la souris :
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

# On lis le décors. On garde les informations du décors dans une liste pour
# pouvoir tester si on tombe, si on peut monter, ....
Decors = lisDecors('niveaux/niv1.txt')
dessine()

souris=Fond.create_image(XS, YS, image=sourisFICHIERG0)

# Surveillance des touches
Touches = []
fenetre.bind_all("<KeyPress>",enfoncee)
fenetre.bind_all("<KeyRelease>",relachee)

animation()

fenetre.mainloop()
