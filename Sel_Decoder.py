from tkinter import *
from tkinter import filedialog as fd, messagebox
from PIL import ImageTk, Image
import sys
import numpy as np
np.set_printoptions(threshold=sys.maxsize)

def Decode(src):
      global d_text

      img = Image.open(src, 'r')
      array = np.array(list(img.getdata()))

      if img.mode == 'RGB':
            n = 3
      elif img.mode == 'RGBA':
            n = 4

      total_pixels = array.size // n

      hidden_bits = ""
      for p in range(total_pixels):
            for q in range(0, 3):
                  hidden_bits += (bin(array[p][q])[2:][-1])

      hidden_bits = [hidden_bits[i:i + 8] for i in range(0, len(hidden_bits), 8)]

      message = ""
      for i in range(len(hidden_bits)):
            if message[-5:] == "$t3g0":
                  break
            else:
                  message += chr(int(hidden_bits[i], 2))
      if "$t3g0" in message:
            return (message[:-5])
      else:
            return ("Il n'y a pas de message caché.")


def Decoder():

      """Ouvrir l'image qui va ensuite etre envoyer dans la commande."""
      typesfichier = (('Images PNG', '*.png'), ('Images JPG', '*.jpg'), ('Images JPEG', '*.jpeg'))
      f_img = fd.askopenfilename(title='Choisissez une image', initialdir='/Desktop', filetypes=typesfichier)
      if not f_img:
            messagebox.showerror("Erreur", "Vous n'avez pas choisi d'image !")
      else:
            e_select.destroy()
            global quit_btn
            #global cacher_btn


            """Paramètres de la page Decode"""
            f_decoder = Tk()
            f_decoder.title("Encoder un message")
            f_decoder.geometry('480x450')
            f_decoder.resizable(width=False, height=False)

            """Fond d'écran de la page Decode"""
            bg_decoder = PhotoImage(file=r'fd2_decoder.png')
            bg_decoder.image = bg_decoder
            img_extraite = Label(f_decoder, image=bg_decoder)
            img_extraite.place(x=0, y=0, relwidth=1, relheight=1)

            """Creation d'un cadre pour l'affichage de l'image Decode"""
            myimg = Image.open(f_img)
            myimage = myimg.resize((300, 200))
            img = ImageTk.PhotoImage(myimage)
            panel = Label(f_decoder, image=img)
            panel.image = img
            panel.place(x=87,y=12)

            """Entry widget : message Decode"""
            d_text = Text(f_decoder)
            d_text.place(x=15, y=254, width=450, height=110)
            d_message = Decode(f_img)
            d_text.insert(INSERT, d_message)
            d_text.configure(state='disabled')

            """Creation bouton Quitter Decode"""
            quit_btn = PhotoImage(file=r'Quitter.png')
            img_label1 = Label(image=quit_btn)
            my_button = Button(f_decoder, image=quit_btn, command=f_decoder.destroy, bd=0, bg="#1C1C1C", borderwidth=0)
            my_button.place(x=155, y=370)




# fen_stg.destroy
"""Paramètres de la page"""
e_select = Tk()
e_select.title("Selectionner une image")
e_select.geometry('480x405')
e_select.resizable(width=False, height=False)

"""Fond d'écran de la page"""
bg_eselect = PhotoImage(file=r'd_selection.png')
img_eselect = Label(e_select, image=bg_eselect)
img_eselect.pack()

"""Creation du bouton Ouvrir"""
ouvrir_btn = PhotoImage(file=r'Ouvrir.png')
img_label2 = Label(image=ouvrir_btn)
my_button = Button(e_select, image=ouvrir_btn,command = Decoder ,bd=0, bg="#1c1c1c", borderwidth=0)
my_button.place(x=155, y=155)

"""Création du bouton quitter"""
quit_btn = PhotoImage(file=r'Quitter.png')
img_label1 = Label(image=quit_btn)
my_button = Button(e_select, image=quit_btn, command=e_select.destroy, bd=0, bg="#1c1c1c", borderwidth=0)
my_button.place(x=155, y=215)


e_select.mainloop()
