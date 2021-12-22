
import sys
from os import listdir
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
import numpy as np
from PIL import Image
np.set_printoptions(threshold=sys.maxsize)

def aide() -> None:
    """Cette fonction ne prend pas d'argument
        Elle permet d'afficher les aides possibles pour executer le programme
    """
    print("Voici ce que vous pouvez faire:\n "
            " -d '.' affichier les fichiers du repetoire courant\n "
            " -f [image.ext] pour afficher les métadonées d'une image. \n "
            " -f [image.ext] -e pour afficher un message dissimulé.\n "
            " -f [image.ext] -s ['message'] [image2.png] pour creer une nouvelle image avec un msg caché.\n ")

def metadonnees(nom_doc):
    """Cette fontion prend en argument un fihcier image (nom_doc)
        Elle d'extraire et d'afficher les principales métadonées à l'utilisateur
    """
    image = nom_doc  # Le deuxième argument correspond à l'image; on créer une variable image
    parser = createParser(image)
    # parser est un module de python permettant de convertir des données dans un format exploitable en python.

    with parser:
        try:
            metadonnees = extractMetadata(parser)  # On extrait les métadonnées et on les stocke dans la variable metadonnees
        except Exception as err:
            """Gestion d'erreur: si l'extraction des métadonnées n'a pas abouti alors on affichera le message d'erreur associé"""
            print("Erreur dans l'extraction des métadonnées: %s" % err)
            metadonnees = None
    if not metadonnees:
        #si il n'ya pas de métadonnées dans l'image on affichera qu'il est impossible de les extraire
        print("Impossible d'extraire les métadonnées")

    for line in metadonnees.exportPlaintext():  # Pour chaque ligne des métadonnées on affichera la ligne
        print(line)

#-----------------------------------------------------------------------------------------------------------

#encoding function
def Encode(image, message, dest):
    """ Cette fonction prend en argument une image, une chaîne de caractères (message en ASCII), un nouveau d'image (dest) et n le nombre de dimensions d'un pixel (RGBA)
        ELle permet de dissimuler un message dans une image
     """
    img = Image.open(image, 'r') #On ouvre l'image "image" avec l'option de lecture read 'r'
    width, height = img.size #La largeur et la hauteur forment les dimmensions de l'image
    array = np.array(list(img.getdata())) #array=tableau on créer donc un tableau de pixel à partir des données de l'image qui sont à l'origine sous forme de liste

    if img.mode == 'RGB': #Ici on cherche à savoir combien de dimensions possède l'image soit elle n'a que les 3 couleurs dans ce cas le nombre de dimensions est 3
        n = 3
    elif img.mode == 'RGBA': # soit elle a la dimension A (transparence) et là le nombre est 4
        n = 4

    total_pixels = array.size//n  #Ici on veut le nombre total de pixels

    message += "$top" #message est la variable étiquette associé à notre message pour pouvoir retrouver le message en entier lorsqu'il faudra le décoder
    b_message = ''.join([format(ord(i), "08b") for i in message]) #b_message est la variable ù on stocke le message (avec l'étiquette) convertit en binaire avec 08b
    req_pixels = len(b_message) #On calcule le nombre de pixel dont on va avoir besoin pour dissimuler le message, donc ca correspond à la longueur du message en binaire

    if req_pixels > total_pixels:
        """Gestion d'erreur: dans le cas ou le message nécessite plus de pixels que l'image en comporte"""
        print("Erreur: L'image est trop petite pour contenir le message")

    else: #si la taille de l'image le permet alors on va pouvoir dissimuler le message
        index=0 #On créer un compteur pour la boucle suivante
        for p in range(total_pixels): #Pour chaque pixel de l'image
            for q in range(0, 3): #Pour chaque dimension du pixel
                if index < req_pixels: #Si l'index est inférieur à la taille requise pour le message c'est que nous n'avons pas fini de le dissimulé
                    array[p][q] = int(bin(array[p][q])[2:9] + b_message[index], 2) #On prend le pixel de coordonnées p et q dans notre tableau, la fonction bin() va nous donner le pixel en binaire. On prends les 8 bits entre le 2eme et le 9eme (les deux premieres étant 0b)
                    index += 1 #On ajoute 1 au compteur index

        array=array.reshape(height, width, n) #Ici on donne au tableau initial les valeurs du tableau après nos modification (une mise à jour)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode) #on recrée l'image à partir de notre tableau actualisé astype('uint8) signifie qu'une donnée est un octet (8 bits)
        enc_img.save(dest) #On sauvegarde l'image sous le nom que l'on aura entré (correspondant à la variable dest)
        print("Votre message a été dissimulé") #On affiche un message pour indiqué le bon déroulement de la fonction


#decoding function
def Decode(image):
    """Cette fonction prend une image en argument et n le nombre de dimensions d'un pixel
        Elle a pour but d'extraire le message qui a été dissimulé dans cette dernière
     """
    img = Image.open(image, 'r')
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4

    total_pixels = array.size//n

    bits = "" #On cherche à extrait les bits de les moins significatifs des pixels
    for p in range(total_pixels): #Pour chaque pixel dans l'image
        for q in range(0, 3): #Pour chaque dimensions (RGB) du pixel
            bits += (bin(array[p][q])[2:][-1]) #On récupère les 2 derniers bits du pixel précédent(-1)

    bits = [bits[i:i+8] for i in range(0, len(bits), 8)] #On groupes par 8 les bits obtenus

    message = "" #On créer une variable message
    for i in range(len(bits)):
        if message[-4:] == "$top": #On cherche notre délimiteur
            break #On sort du for
        else:
            message += chr(int(bits[i], 2)) #Si l'utilisateur à mis du texte unicode on doit le convertir d'héxadecimal en binaire
    if "$top" in message:
        print("Voici le message caché:", message[:-4]) #On lit le message sans le délimiteur
    else:
        print("Aucun message n'a été trouvé")
#-----------------------------------------------------------------------------------------------------------
def main():
    """Cette fonction a pour but de réaliser une action en fonction du nombre d'argument et de l'argument renseigné:
    Les actions possibles sont:
    -Demander de l'aide: -h
    -Explorer le répertoire courant: -d
    -Extraire les métadonnées d'un fichier image: -f
    -Dissimuler un message dans une image : -f [image] -s [message]
    -Extraire le message: -f [image) -e
    Si aucun argument est renseigné alors on incite l'utilisateur a utilser l'option d'aide -h
    """
    if len(sys.argv) < 2:
        print("Tapez : python CLI_POO.py -h ,pour avoir de l'aide") #On affiche comment obtenir de l'aide
        exit() #On stop le programme

    else :
        type_fichier = str(sys.argv[1])

        if type_fichier == '-h':
            aide()

        elif type_fichier == '-d':
            nom_doc = sys.argv[2]
            print(listdir(nom_doc))

        elif type_fichier == '-f':
            nom_file = sys.argv[2]

            if len(sys.argv) < 4:
                metadonnees(nom_file)

            else:
                options = sys.argv[3]

                if options == '-e':
                    Decode(nom_file)

                elif options == '-s':
                    print("Je dissimule un message caché...")
                    message = sys.argv[4]
                    dest = sys.argv[5]
                    Encode(nom_file,message,dest)
                    ...

if __name__ == '__main__':
    main()
