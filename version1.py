from tkinter import *

# Version 1 : Dessin du décors

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

# On lis le décors. On garde les informations du décors dans une liste pour
# pouvoir tester si on tombe, si on peut monter, ....
Decors = lisDecors('niveaux/niv1.txt')
dessine()

fenetre.mainloop()
