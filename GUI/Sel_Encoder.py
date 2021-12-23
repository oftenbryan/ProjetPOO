from tkinter import *
from tkinter import filedialog as fd, messagebox
from PIL import ImageTk, Image
import sys
import numpy as np
np.set_printoptions(threshold=sys.maxsize)

def Encoder():
      """!
      @brief Affiche une fenêtre à l'utilisateur et permet l'action de dissimuler un message dans une image.
      """
      def Encode(src, message, dest):
            img = Image.open(src, 'r')
            width, height = img.size
            array = np.array(list(img.getdata()))

            if img.mode == 'RGB':
                  n = 3
            elif img.mode == 'RGBA':
                  n = 4

            total_pixels = array.size // n

            message += "$top"
            b_message = ''.join([format(ord(i), "08b") for i in message])
            req_pixels = len(b_message)

            if req_pixels > total_pixels:
                  messagebox.showerror("ERREUR", "Nous avons besoin d'un fichier plus volumineux")

            else:
                  index = 0
                  for p in range(total_pixels):
                        for q in range(0, 3):
                              if index < req_pixels:
                                    array[p][q] = int(bin(array[p][q])[2:9] + b_message[index], 2)
                                    index += 1

                  array = array.reshape(height, width, n)
                  enc_img = Image.fromarray(array.astype('uint8'), img.mode)
                  enc_img.save(dest)
                  messagebox.showinfo("Success", "Votre image a bien été encodée")


      typesfichier = (('Images PNG', '*.png'), ('Images JPG', '*.jpg'), ('Images JPEG', '*.jpeg'))
      f_img = fd.askopenfilename(title='Choisissez une image', initialdir='/Desktop', filetypes=typesfichier)
      if not f_img:
            messagebox.showerror("Erreur", "Vous n'avez pas choisi d'image !")
      else:
            e_select.destroy()
            global quit_btn
      """! @brief Ouvrir l'image qui va ensuite etre envoyer dans la commande."""

            f_encoder = Tk()
            f_encoder.title("Encoder un message")
            f_encoder.geometry('480x450')
            f_encoder.resizable(width=False, height=False)
            """! @brief Paramètres de la page"""

            bg_encoder = PhotoImage(file=r'fd2_encoder.png')
            bg_encoder.image = bg_encoder
            img_cacher = Label(f_encoder, image=bg_encoder)
            img_cacher.place(x=0, y=0, relwidth=1, relheight=1)
            """! @brief Fond d'écran de la page"""

            myimg = Image.open(f_img)
            myimage = myimg.resize((300, 200))
            img = ImageTk.PhotoImage(myimage)
            panel = Label(f_encoder, image=img)
            panel.image = img
            panel.place(x=87,y=12)
            """! @brief Creation d'un cadre pour l'affichage de l'image"""

            msg = StringVar()
            message = Entry(f_encoder, textvariable = msg)
            message.place(x=15, y=254, width=450, height=35)
            """! @brief Entry widget : message"""

            desti = StringVar()
            destination = Entry(f_encoder, textvariable = desti)
            destination.place(x=15, y=327, width=450, height=35)
            """! @brief Entry widget : nouveau nom"""

            my_button1 = Button(f_encoder, text="Encoder", command=lambda: Encode(f_img, msg.get(), desti.get()), bd=0,
                                bg="#282828", borderwidth=0, font=("Montserrat", 12, 'bold'), fg="#FFFFFF")
            my_button1.place(x=95, y=388)
            """! @brief Creation bouton Encoder"""

            quit_btn = PhotoImage(file=r'Quitter.png')
            img_label1 = Label(image=quit_btn)
            my_button = Button(f_encoder, image=quit_btn, command=f_encoder.destroy, bd=0, bg="#1C1C1C", borderwidth=0)
            my_button.place(x=250, y=375)
            """! @brief Creation bouton Quitter"""



e_select = Tk()
e_select.title("Selectionner une image")
e_select.geometry('480x405')
e_select.resizable(width=False, height=False)
"""! @brief Paramètres de la page"""


bg_eselect = PhotoImage(file=r'e_selection.png')
img_eselect = Label(e_select, image=bg_eselect)
img_eselect.pack()
"""! @brief Fond d'écran de la page"""


ouvrir_btn = PhotoImage(file=r'Ouvrir.png')
img_label2 = Label(image=ouvrir_btn)
my_button = Button(e_select, image=ouvrir_btn,command = Encoder ,bd=0, bg="#1c1c1c", borderwidth=0)
my_button.place(x=155, y=155)
"""! @brief Creation du bouton Ouvrir"""


quit_btn = PhotoImage(file=r'Quitter.png')
img_label1 = Label(image=quit_btn)
my_button = Button(e_select, image=quit_btn, command=e_select.destroy, bd=0, bg="#1c1c1c", borderwidth=0)
my_button.place(x=155, y=215)
"""! @brief Création du bouton quitter"""

e_select.mainloop()
