from tkinter import *
from tkinter import filedialog as fd
from tkinter import Toplevel as top, messagebox
import sys
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
import numpy as np
np.set_printoptions(threshold=sys.maxsize)

#Fonctions--------------------------------------------------------------

def Stegano():


    fen_stg = Toplevel(fenetre)
    fen_stg.title("Stéganographie")
    fen_stg.geometry('480x270')
    fen_stg.resizable(width=False, height=False)
    """! @brief Création de la fênêtre steganographie"""


    fond2 = PhotoImage(file=r'fd_Stg.png')
    img1 = Label(fen_stg, image=fond2)
    img1.pack()
    """! @brief Création du fond d'écran steganographie"""


    retour_btn = PhotoImage(file=r'Quitter.png')
    img_label2 = Label(image=retour_btn)
    my_button2 = Button(fen_stg, image=retour_btn, command=fen_stg.destroy, bd=0, bg="#1c1c1c", borderwidth=0)
    my_button2.place(x=155, y=195)
    """! @brief Creation bouton Quitter steganographie"""


    extraire_btn = PhotoImage(file=r'Decoder.png')
    img_label4 = Label(image=extraire_btn)
    my_button4 = Button(fen_stg, image=extraire_btn, bd=0, bg="#1c1c1c", borderwidth=0)
    my_button4.place(x=155, y=135)
    """! @brief Creation bouton Decoder steganographie"""


    encoder_btn = PhotoImage(file=r'Encoder.png')
    img_label1 = Label(image=encoder_btn)
    my_button1 = Button(fen_stg, image=encoder_btn, bd=0, bg="#1c1c1c", borderwidth=0)
    my_button1.place(x=155, y=75)
    """! @brief Creation bouton Encoder steganographie"""


    top.update(fen_stg)
    fenetre.mainloop()


def ouvr_img():

    def metadonnees(nom_doc):
        """!
        Cette fontion prend en argument un fihcier image (nom_doc)
        Elle d'extraire et d'afficher les principales métadonées à l'utilisateur
        """
        global cadre
        global fenetre
        image = nom_doc  # Le deuxième argument correspond à l'image; on créer une variable image
        parser = createParser(image)
        # parser est un module de python permettant de convertir des données dans un format exploitable en python.

        with parser:
            try:
                metadata = extractMetadata(
                    parser)  # On extrait les métadonnées et on les stocke dans la variable metadata
            except Exception as err:
                """! @error Gestion d'erreur: si l'extraction des métadonnées n'a pas abouti alors on affichera le message d'erreur associé"""
                metas = Label(cadre, text="Erreur dans l'extraction des métadonnées: %s" % err, bg="#373737", fg="#FFFFFF",
                              font=("Helvetica", 10))
                metas.pack()
                metadata = None

        if not metadata:
            # Si il n'ya pas de métadonnées dans l'image on affichera qu'il est impossible de les extraire
            metas = Label(cadre , text = "Impossible d'extraire les métadonnées", bg ="#373737", fg = "#FFFFFF",font = ("Helvetica",10))
            metas.pack()

        for line in metadata.exportPlaintext():  # Pour chaque ligne des métadonnées on affichera la ligne

            metas = Label(cadre , text = line, bg ="#373737", fg = "#FFFFFF",font = ("Helvetica",12))
            metas.pack()

    typesfichier = (('Images PNG', '*.png'),('Images JPG', '*.jpg'))
    nomfichier = fd.askopenfilename(title='Choisissez une image',initialdir='/Desktop',filetypes=typesfichier)
    global fenetre
    if not nomfichier:
        messagebox.showerror("Erreur", "Vous n'avez pas choisi d'image !")
    else:
        metadonnees(nomfichier)



fenetre = Tk()
fenetre.geometry('654x540')
fenetre.title("Projet POO")
fenetre.resizable(width=False, height=False)
"""! @brief Création de la fenêtre"""


Fond = PhotoImage(file=r'Background.png')
label1 = Label(fenetre, image=Fond)
label1.place(x=0,y=0, relwidth=1, relheight=1)
"""! @brief Fond d'écran de la fênetre"""


quit_btn = PhotoImage(file=r'Quitter.png')
img_label1 = Label(image=quit_btn)
my_button = Button(fenetre, image=quit_btn, command=fenetre.destroy, bd=0, bg="#1c1c1c", borderwidth=0)
my_button.place(x=246, y=4)
"""! @brief Création du bouton quitter"""

# Création du bouton Métadonnées
metas_btn = PhotoImage(file=r'Metas_btn.png')
img_label2 = Label(image=metas_btn)
my_button = Button(fenetre, image=metas_btn, command=ouvr_img, bd=0, bg="#1c1c1c", borderwidth=0)
my_button.place(x=40, y=10)

# Création du bouton Stéganographie
diss_btn = PhotoImage(file=r'Stg.png')
img_labe3 = Label(image=diss_btn)
my_button = Button(fenetre, image=diss_btn, command=Stegano, bd=0, bg="#1c1c1c", borderwidth=0)
my_button.place(x=425, y=10)


cadre = Frame(fenetre, width =210, height= 390, bg ="#373737" )
cadre.place(x=28, y=80)
"""! @brief Creation d'un cadre pour l'affichage des métadonnées"""

# Lancement du gestionnaire d’événements
fenetre.mainloop()
