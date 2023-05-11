#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 14:30:49 2021

@author: teddy, thomas, damien
"""

"""
Mazex
"""

import pyglet # /!\ import manuel
import pygame # /!\ import manuel
import tkinter as tk
import time
import threading
import os
from datetime import datetime




class Mazex():

    def __init__(self,h,l):
        
        self.h = h # hauteur
        self.l = l # largeur
        self.grille = [[0] * h for i in range(l)]
        
        self.initTab()
        self.affiche()
        
        
    def initTab(self): # Crée une matrice, un tableau de 0 pour les cases vides et de 1 pour les murs
        
        for Colonne in range(self.h): # Mur gauche 
            self.grille[0][Colonne] = 1
    
        for Colonne in range(self.h): # Mur droit
            self.grille[self.l-1][Colonne] = 1
    
        for Ligne in range(self.l): # Mur haut
            self.grille[Ligne][0] = 1
    
        for Ligne in range(self.l): # Mur bas
            self.grille[Ligne][self.h-1] = 1
         
            
    """fonction temp"""       
    def affiche(self):
        for j in range (self.h):
            for i in range(self.l):
                print(self.grille[i][j]," ", end=" ")
            print("")




class Cd:
    
    """Gestion des fichiers externes sauvegardes/options"""
    
    def __init__(self):
        
        self.options = {}
        self.saves = {}
        
    
    def get_options(self):
        
        try:
            fichier = open("options.txt","r")
        except:
            fichier = open("options.txt","a")
            fichier.write("screenmode = 0 \nskipintro = 0 ")
        
        for ligne in fichier:
            
            ligne = ligne.replace(' ','') # supprime espaces entre les symboles égales      
            x = ligne.find('=')        
            self.options[ligne[:x]] = int(ligne[x+1:x+2])
                
        fichier.close() 
        
        return self.options
    
    
    def edit_option(self, iD, value):
        
        fichier = open("options.txt","r")
        
        contenu = fichier.read()
         
        lignes_contenu = contenu.split("\n")
        
        ligne = lignes_contenu[iD]
        
        ligne = ligne.replace(' ','') # supprime espaces entre les symboles égales      
        x = ligne.find('=')
        
        ligne = ligne[:x]+' '+ligne[x:x+1]+' '+str(value)+' '+ligne[x+2:]
        
        lignes_contenu[iD] = ligne
        
        contenu = "\n".join(lignes_contenu)
    
        fichier.close()
        
        with open("options.txt", "w", encoding = "utf-8") as fichier:
            fichier.write(contenu)
    
    
class Mixer:
    
    def __init__(self, sound, number=0):
        
        self.path = sound
        self.channel = number
        
    
    def play(self):

        pygame.mixer.Channel(self.channel).play(pygame.mixer.Sound(self.path))
        
        
    def stop(self):

        pygame.mixer.Channel(self.channel).stop(pygame.mixer.Sound(self.path))
        
    
    def check_channel(self):
      
        if pygame.mixer.Channel(self.channel).get_busy() == False:
            
            self.play()


        
        
class HoverButton(tk.Button):
    
    def __init__(self, master, **kw):
        tk.Button.__init__(self,master=master,**kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        

    def on_enter(self, e):
        self['background'] = self['activebackground']
        

    def on_leave(self, e):
        self['background'] = self.defaultBackground




class Graphique():
    
    def __init__(self,lab):
        
        self.external = Cd()
        self.options = self.external.get_options()
        self.firstboot = True
        
        self.root = tk.Tk()
        
        self.screenWidth = self.root.winfo_screenwidth() # largeur de l'écran
        self.screenHeight = self.root.winfo_screenheight() # hauteur de l'écran     
        self.rootWidth = int(self.screenWidth/1.5) # largeur de la demi fenêtre
        self.rootHeight = int(self.screenHeight/1.5) # hauteur de la demi fenêtre

        self.ratioWidth = 0 # utilisé pour la taille des widgets
        self.ratioHeight = 0 # utilisé pour la taille des widgets
        self.ratioSize = 0 # ratio de la taille hauteur/largeur
        self.policeSize = 0 # taille de police
        self.coo = tuple
    
        self.img_bg_credit = tk.PhotoImage(file="assets/textures/credit.gif") # import images
        self.img_canvas_credit = tk.PhotoImage(file="assets/textures/wallpaper.gif")
        
        self.desc1Canvas = tk.Canvas()
        self.title = tk.Canvas()

        self.buttons_frame = tk.Frame() 
        self.buttons_frame_background = tk.Canvas()
        self.menu_buttons = []
        self.button = HoverButton(self.root)
                
        self.initUI()
        

    def initUI(self):
        
        self.root.title("Mazex") # Nom de fenêtre
        
        pyglet.font.add_file('assets/font/Debrosee.ttf') # import des polices
        pyglet.font.add_file('assets/font/ReggaeOne.ttf')
        pyglet.font.add_file('assets/font/Pacifico.ttf')
        
        logo = tk.PhotoImage(file='assets/textures/logo.gif') # icone de la fenêtre
        self.root.tk.call('wm', 'iconphoto', self.root._w, logo)
        
        pygame.mixer.init() # démarre le module musique de pygame
        
        """définit taille variables et fenêtre en fonction du screenmode choisie dans options.txt"""

        if self.options['screenmode'] == 0: # semi fenêtré          
            self.root.geometry("%dx%d%+d%+d" % (self.rootWidth,self.rootHeight,(self.screenWidth-self.rootWidth) // 2, (self.screenHeight-self.rootHeight)//2)) # divise la fenêtre par 2 et la centre au milieu de l'écran
            self.ratioWidth = self.rootWidth # utilisé pour la taille des widgets
            self.ratioHeight = self.rootHeight # utilisé pour la taille des widgets
            self.coo = (4.3,2,1.15)

        elif self.options['screenmode'] == 1: # grande fenêtre         
            self.root.geometry(str(self.screenWidth)+'x'+str(self.screenHeight))
            if os.name == 'nt': # pour windows          
                self.root.wm_state('zoomed') # grande fenêtre avec titlebar
            else: # linux et autres
                self.root.attributes('-zoomed', True)  # grande fenêtre avec titlebar
            self.ratioWidth = self.screenWidth # utilisé pour la taille des widgets
            self.ratioHeight = self.screenHeight # utilisé pour la taille des widgets
            self.coo = (8,1.938,1.2)
            
        elif self.options['screenmode'] == 2: # fullscreen
            self.root.geometry(str(self.screenWidth)+'x'+str(self.screenHeight))
            self.root.attributes('-fullscreen', True)
            self.ratioWidth = self.screenWidth # utilisé pour la taille des widgets
            self.ratioHeight = self.screenHeight # utilisé pour la taille des widgets
            self.coo = (8,1.938,1.2)

        self.ratioSize = (int((self.ratioWidth+self.ratioHeight))) # ratio de la taille hauteur/largeur          
        self.policeSize = self.ratioSize // 100 # taille de police

        self.root.attributes("-topmost", True) # fenêtre au premier plan

        if self.options['skipintro'] == 0:
            t1 = threading.Thread(target=self.loadingUI) # démarre la fonction dans un thread pour pouvoir maintenir le mainloop
            t1.start()
            
        else:
            t1 = threading.Thread(target=self.menuUI)
            t1.start()

        self.root.mainloop()


    def loadingUI(self):
        
        frame_background = tk.Frame(self.root, width=self.ratioWidth, height=self.ratioHeight, background="black")
        frame_background.place(x=0, y=0)
        
        voice_loading = Mixer('assets/sounds/voice.wav',1)
        voice_loading.play()
        
        time.sleep(2)
        
        music_loading = Mixer('assets/sounds/intro.wav',0)
        music_loading.play()

        sequence = ['black', '#090909', '#181715', '#201f1b', '#2e2c23', '#525430', '#737637', '#959936', '#acb130', '#c4cb21']
        
        index = -1
        for i in range(len(sequence)):
            time.sleep(0.05)
            index = (index + 1) % len(sequence)
            frame_background.configure(background=sequence[index])
                
        self.root.configure(background='#c4cb21')
        
        time.sleep(0.07)
                   
        desc1Label = tk.Label(text='Not a simple Maze game...', font=('Snell Roundhand',self.policeSize,'bold'), background='#c4cb21')
        desc1Label.place(x=self.ratioWidth//12, y=self.ratioHeight//12, anchor='nw')
        
        time.sleep(1.35)
        
        desc2Label = tk.Label(text="It's the BEST Maze game...", font=('Snell Roundhand',self.policeSize,'bold'), background='#c4cb21') 
        desc2Label.place(x=-(self.ratioWidth//12), y=-(self.ratioHeight//12), rely=1.0, relx=1.0, anchor='se')
        
        time.sleep(1.3)
        
        frame_background = tk.Frame(self.root, width=self.ratioWidth, height=self.ratioHeight, background='#c4cb21')
        frame_background.place(x=0, y=0)
        
        sequence = ['#c4cb21', '#afb528', '#8d912c', '#6d702c', '#41421b', '#141430', '#131347']
        
        index = -1
        for i in range(len(sequence)):
            time.sleep(0.06)
            index = (index + 1) % len(sequence)
            frame_background.configure(background=sequence[index])
            
        time.sleep(0.45)

        desc1Label.destroy()
        desc2Label.destroy()
            
        desc1Label = tk.Label(frame_background, text='Mazex',font=('Debrosee',self.policeSize*11), bg='#131347', fg='#ede168')
        desc1Label.place(x=self.ratioWidth//6, y=self.ratioHeight//4)
        
        desc2Label = tk.Label(frame_background, text='=====================================================================',font=('Debrosee',self.policeSize*4), bg='#131347', fg='#7d7529')
        desc2Label.place(x=0, y=self.ratioHeight//1.5)
        
        time.sleep(2.1)
        
        desc1Label.destroy()
        desc2Label.destroy()
        frame_background.destroy()
        
        self.menuUI()

        
    def menuUI(self):
        
        if self.firstboot == False:        
            music_click = Mixer('assets/sounds/click.wav',1)
            music_click.play()
        else:
            self.firstboot == False
        
        """Disparition des widgets du jeu"""
        try:
            self.label_background.destroy()
            self.title.place_forget()
            self.desc1Canvas.place_forget()
            self.button.place_forget()
        except:
            pass

        music_menu = Mixer('assets/sounds/menu.wav',0)
        music_menu.play()
        
        self.img_bg_menu = tk.PhotoImage(file="assets/textures/background.gif")
        self.label_background = tk.Label(self.root, image = self.img_bg_menu)
        self.label_background.photo = self.img_bg_menu
        self.label_background.grid(row=0, column=0)

        self.title = tk.Canvas(self.root, width=self.ratioWidth, height=self.ratioHeight//3.3, highlightthickness=0)
        self.title.create_image(0, 0, image=self.img_bg_menu, anchor='nw')
        self.title.create_text(self.ratioWidth//2.05, self.ratioHeight//6.65, fill="black", font=('Debrosee',str(self.policeSize*10)), text="Mazex")
        self.title.create_text(self.ratioWidth//2, self.ratioHeight//6.6, fill="#a6a633", font=('Debrosee',str(self.policeSize*10)), text="Mazex")
        self.title.place(x=0, y=int(self.ratioHeight*0.03))
        
        self.menu_buttons = []
        
        self.menu_buttons.append(HoverButton(self.root, width=self.ratioWidth//25,
                            text="Play", font=('ReggaeOne bold', self.policeSize, "bold"),
                            bg='#d9d0a7', activebackground='#d9b304', foreground='black', activeforeground='red',
                            command= lambda: self.checkpointmenu(0)))
        self.menu_buttons.append(HoverButton(self.root, width=int(self.ratioWidth*0.04),
                            text="Credit", font=('ReggaeOne bold', self.policeSize, "bold"),
                            bg='#d9d0a7', activebackground='#d9b304', foreground='black', activeforeground='red',
                            command= lambda: self.checkpointmenu(1)))
        self.menu_buttons.append(HoverButton(self.root, width=int(self.ratioWidth*0.0189),
                            text="Settings", font=('ReggaeOne bold', self.policeSize, "bold"),
                            bg='#d9d0a7', activebackground='#d9b304', foreground='black', activeforeground='red',
                            command= lambda: self.checkpointmenu(2)))
        self.menu_buttons.append(HoverButton(self.root, width=int(self.ratioWidth*0.0189),
                            text="Close", font=('ReggaeOne bold', self.policeSize, "bold"),
                            bg='#d9d0a7', activebackground='#d9b304', foreground='black', activeforeground='red',
                            command= lambda: self.checkpointmenu(3)))

        self.menu_buttons[0].place(x=self.ratioWidth//self.coo[0], y=self.ratioHeight//2.5)
        self.menu_buttons[1].place(x=self.ratioWidth//self.coo[0], y=self.ratioHeight//1.85)
        self.menu_buttons[2].place(x=self.ratioWidth//self.coo[0], y=self.ratioHeight//1.45)
        self.menu_buttons[3].place(x=self.ratioWidth//self.coo[1], y=self.ratioHeight//1.45)
        
        
    def checkpointmenu(self,buttonId):
        
        self.menu_buttons[buttonId].configure(state="disable", background='#ff9d00', fg="white")
         
        music_click = Mixer('assets/sounds/click.wav',1)
        music_click.play()
         
        time.sleep(0.005)
        
        """Disparition des widgets du menu"""
        try:
            for button in self.menu_buttons:
                button.place_forget()
            self.title.place_forget()
        except:
            pass
         
        if buttonId == 0: # Play
            
            self.label_background.destroy()
            self.root.destroy()
            mainLab()
        
        elif buttonId == 1: # Credit
            
            self.label_background.destroy()
            self.credit()
        
        elif buttonId == 2: # Settings
            
            self.settingsUI()
        
        elif buttonId == 3: # Close
            
            pygame.mixer.pause()
            self.root.destroy()

             
    def credit(self):
  
        music_credit = Mixer('assets/sounds/credit.wav',0)
        music_credit.play()
        
        self.label_background = tk.Label(self.root, image = self.img_bg_credit)
        self.label_background.photo = self.img_bg_credit
        self.label_background.grid(row=0, column=0)
        
        self.title = tk.Canvas(self.root, width=self.ratioWidth, height=self.ratioHeight//7.5, highlightthickness=0)
        self.title.create_image(0, 0, image=self.img_bg_credit, anchor='nw')
        self.title.create_text(self.ratioWidth//2.05, self.ratioHeight//15, fill="black", font=('Debrosee',str(self.policeSize*5)), text="Mazex")
        self.title.create_text(self.ratioWidth//2, self.ratioHeight//15, fill="#a6a633", font=('Debrosee',str(self.policeSize*5)), text="Mazex")
        self.title.place(x=0, y=int(self.ratioHeight*0.04))
        
        self.desc1Canvas = tk.Canvas(self.root, width=self.ratioWidth, height=self.ratioHeight//2, highlightthickness=self.policeSize)
        self.desc1Canvas.create_image(0, 0, image=self.img_canvas_credit, anchor='nw')
        self.desc1Canvas.create_text(self.ratioWidth//4, self.ratioHeight//9.9, fill="#009183", font=('Orbitron',str(int(self.policeSize*1.6))), text="Teddy Koehren :")
        self.desc1Canvas.create_text(self.ratioWidth//4, self.ratioHeight//5.2, fill="#009183", font=('Orbitron',str(int(self.policeSize*1.6))), text="Thomas Amiotte :")
        self.desc1Canvas.create_text(self.ratioWidth//4, self.ratioHeight//3.5, fill="#009183", font=('Orbitron',str(int(self.policeSize*1.6))), text="Damien Balasse :")
        self.desc1Canvas.create_text(self.ratioWidth//4, self.ratioHeight//2.6, fill="#009183", font=('Orbitron',str(int(self.policeSize*1.6))), text="Mohammed Chenning :")
        self.desc1Canvas.create_text(self.ratioWidth//2.7, self.ratioHeight//2.05, fill="black", font=('Orbitron',str(int(self.policeSize*0.8))), text="Martin Gadet :")
        self.desc1Canvas.create_text(self.ratioWidth//1.45, self.ratioHeight//9.9, fill="red", font=('Courgette',str(int(self.policeSize*1.3))), text="Égal de Chuck Norris")
        self.desc1Canvas.create_text(self.ratioWidth//1.45, self.ratioHeight//5.2, fill="red", font=('Courgette',str(int(self.policeSize*1.3))), text="Le 7ème jour, il créa Mazex")
        self.desc1Canvas.create_text(self.ratioWidth//1.45, self.ratioHeight//3.5, fill="red", font=('Courgette',str(int(self.policeSize*1.3))), text="MacGyver du codage")
        self.desc1Canvas.create_text(self.ratioWidth//1.45, self.ratioHeight//2.6, fill="red", font=('Courgette',str(int(self.policeSize*1.3))), text="Neil Armstrong de la progammation")
        self.desc1Canvas.create_text(self.ratioWidth//1.65, self.ratioHeight//2.05, fill="black", font=('Courgette',str(int(self.policeSize*0.6))), text="ASMR introductif")
        self.desc1Canvas.place(x=0, y=int(self.ratioHeight*0.25))
               
        self.button1 = HoverButton(self.root, width=int(self.ratioWidth*0.04),
                            text="Back", font=('Pacifico bold', self.policeSize, "bold"),
                            bg='#162947', activebackground='#1a53ad', foreground='white', activeforeground='red',
                            command= self.menuUI)
        self.button1.place(x=self.ratioWidth//self.coo[0], y=self.ratioHeight//self.coo[2])
            
        
    def settingsUI(self):
        
        print(self.options,type(self.options))
        self.button1 = HoverButton(self.root, width=int(self.ratioWidth*0.04),
                            text="Back", font=('Pacifico bold', self.policeSize, "bold"),
                            bg='#162947', activebackground='#1a53ad', foreground='white', activeforeground='red',
                            command= self.menuUI)
        self.button1.place(x=self.ratioWidth//self.coo[0], y=self.ratioHeight//self.coo[2])

        
        #option0
        if self.options['screenmode'] == 0:
            
            self.button_option0 = HoverButton(self.root, width=int(self.ratioWidth*0.04),
                                text="Screenmode : Small windowed", font=('Pacifico bold', self.policeSize, "bold"),
                                bg='#dbe0a8', activebackground='#f5ff8f', foreground='black', activeforeground='red',
                                command= lambda: self.settings(0,1))
            self.button_option0.place(x=self.ratioWidth//self.coo[0], y=self.ratioHeight//10)
            
        elif self.options['screenmode'] == 1:
            
            self.button_option0 = HoverButton(self.root, width=int(self.ratioWidth*0.04),
                                text="Screenmode : Windowed", font=('Pacifico bold', self.policeSize, "bold"),
                                bg='#dbe0a8', activebackground='#f5ff8f', foreground='black', activeforeground='red',
                                command= lambda: self.settings(0,2))
            self.button_option0.place(x=self.ratioWidth//self.coo[0], y=self.ratioHeight//10)
            
        else:
            
            self.button_option0 = HoverButton(self.root, width=int(self.ratioWidth*0.04),
                                text="Screenmode : Fullscreen", font=('Pacifico bold', self.policeSize, "bold"),
                                bg='#dbe0a8', activebackground='#f5ff8f', foreground='black', activeforeground='red',
                                command= lambda: self.settings(0,0))
            self.button_option0.place(x=self.ratioWidth//self.coo[0], y=self.ratioHeight//10)
            
        #option1
        if self.options['skipintro'] == 0:
            
            self.button_option1 = HoverButton(self.root, width=int(self.ratioWidth*0.04),
                                text="Skip Intro : No", font=('Pacifico bold', self.policeSize, "bold"),
                                bg='#dbe0a8', activebackground='#f5ff8f', foreground='black', activeforeground='red',
                                command= lambda: self.settings(1,1))
            self.button_option1.place(x=self.ratioWidth//self.coo[0], y=self.ratioHeight//5.5)
            
        else:
            
            self.button_option1 = HoverButton(self.root, width=int(self.ratioWidth*0.04),
                                text="Skip Intro : Yes", font=('Pacifico bold', self.policeSize, "bold"),
                                bg='#dbe0a8', activebackground='#f5ff8f', foreground='black', activeforeground='red',
                                command= lambda: self.settings(1,0))
            self.button_option1.place(x=self.ratioWidth//self.coo[0], y=self.ratioHeight//5.5)       
            
            
    def settings(self, option, value):
        
        music_click = Mixer('assets/sounds/click.wav',1)
        music_click.play()
        
        self.external.edit_option(option,value)
        self.options = self.external.get_options()
        
        self.settingsUI()

"""partie damien thomas"""

def indexx(e,l):
    for y in range (len(l)):
        for x in range (len(l[0])):
            if l[y][x][0] == e:
                return (y,x)
            
def parcours_largeur(g, source):
    """parcours en largeur depuis le sommet source"""
    dist = {source: 0}
    courant = {source}
    suivant = set()
    while len(courant) > 0:
        s = courant.pop()
        for v in g.voisins(s):
            if v not in dist:
                suivant.add(v)
                dist[v] = dist[s] + 1
        if len(courant) == 0:
            courant, suivant = suivant, set()
    return dist

def distance(g, u, v):
    """distance de u à v (et None si pas de chemin)"""
    dist = parcours_largeur(g, u)
    return dist[v] if v in dist else None

    
class Control():
    
    def __init__(self):
        self.graph=None
        self.lab=None
        self.A=bool
    
    def sauvegarder(self):
        dates = str(datetime.now().date())
        #print(dates)
        temps = str(datetime.now().time())
        #print(temps)
        date =str(dates[8:]+"_"+dates[5:7]+"_"+dates[0:4]+"_"+temps[0:2]) + "h" + str(temps[3:5]) + "m" + str(temps[6:8])+"s"
        list_temp = []
        #print(date)
        f = open('save_laby_'+date+'.csv', 'w')
        for y in range (len (self.lab.grille)):
            for x in range (len (self.lab.grille[0])):
                list_temp.append(str(self.lab.grille[y][x]))
            ligne = ";".join(list_temp) + "\n"
            f.write(ligne)
            #print(list_temp)
            list_temp=[]
        f.close()
    
    def import_laby(self):
        
        from tkinter import filedialog
        name = filedialog.askopenfilename(title = "Selecteur de fichiers",filetypes = (("CSV Files","*.csv"),))
        print (name)
        with open(name, newline='') as csvfile:
            a =csvfile.read()
            #print(a)
        list_temp = []
        liste = []
        for i in a:
            if i == "1" or i =="0" or i =="2" or i=="3":
            
                list_temp.append(int(i))
            elif i == ";":
                pass
            elif i == chr(13) and len(list_temp)!=0: #si le champs est vide (chr(13)) et que la liste est vide  alors :

                liste.append(list_temp)
                list_temp = [] #reset la list

        self.lab.grille = liste        
        self.graph.Labyrinthe(self.graph.taille) # actualise avec 50 la taille des carrés
        self.graph.Labyrinthe_binaire()
        self.graph.Graphe()
        
    def calculer(self): #calculer le graphe en fonction des valeur entry largeur et hauteur
        if ((int(self.graph.largeurgraphe.get()) or int(self.graph.longueurgraphe.get())) < 4 )or ((int(self.graph.largeurgraphe.get()) or int(self.graph.longueurgraphe.get())) > 34): # limite la taille du labyrinthe
            self.A=False
            self.graph.verif_taille()
            
        else:
            self.A=True
            self.graph.verif_taille()
            self.lab.h = int(self.graph.largeurgraphe.get())
            self.lab.l = int(self.graph.longueurgraphe.get()) 
            self.lab.grille = [[0] * self.lab.h for i in range(self.lab.l)]

        self.lab.initTab() #actualise
        self.graph.taille = (max(self.graph.x,self.graph.y )//4)//max(len(self.lab.grille),len(self.lab.grille[0]))

        self.graph.Labyrinthe(self.graph.taille)
        self.graph.Labyrinthe_binaire()
        self.graph.Graphe()
        
    def set_graphique(self,graphique):
        self.graph=graphique
        
    def set_labyrinthe(self,labyrinthe):
        self.lab=labyrinthe
    
    def clique(self,event):
        print(event.y//self.graph.taille,event.x//self.graph.taille)
        if event.y//self.graph.taille == 0 or event.y//self.graph.taille == len(self.lab.grille)-1 or event.x//self.graph.taille == 0 or event.x//self.graph.taille==len(self.lab.grille[0])-1 : #si on clique sur un mur d'un bord
          print("pas possible")
        elif self.lab.grille[event.y//self.graph.taille][event.x//self.graph.taille] == 0: # si le carré est blanc il devient noir
            self.lab.grille[event.y//self.graph.taille][event.x//self.graph.taille] = 1
        elif self.lab.grille[event.y//self.graph.taille][event.x//self.graph.taille] == 1: # si le carré est noir il devient blanc
            self.lab.grille[event.y//self.graph.taille][event.x//self.graph.taille] = 0
           
        self.graph.Labyrinthe(self.graph.taille) # actualise avec 50 la taille des carré
        self.graph.Labyrinthe_binaire()
        self.graph.Graphe()
        
        
    def clique2(self,event):
        print(event.y//self.graph.taille,event.x//self.graph.taille)
        if event.y//self.graph.taille == 0 or event.y//self.graph.taille == len(self.lab.grille)-1 or event.x//self.graph.taille == 0 or event.x//self.graph.taille==len(self.lab.grille[0])-1 : #si on clique sur un mur d'un bord
          print("pas possible")
        
        elif self.test_case_entree(self.lab.grille)==False:
            if self.lab.grille[event.y//self.graph.taille][event.x//self.graph.taille] == 0: # si le carré est blanc il devient vert
                self.lab.grille[event.y//self.graph.taille][event.x//self.graph.taille] = 2
                
        elif self.test_case_entree(self.lab.grille)==True:
            if self.lab.grille[event.y//self.graph.taille][event.x//self.graph.taille] == 2: # si le carré est vert il devient blanc
                self.lab.grille[event.y//self.graph.taille][event.x//self.graph.taille] = 0
                
        self.graph.Labyrinthe(self.graph.taille) # actualise avec 50 la taille des carré
        self.graph.Labyrinthe_binaire()
        self.graph.Graphe()
        
    def clique3(self,event):
        print(event.y//self.graph.taille,event.x//self.graph.taille)
        if event.y//self.graph.taille == 0 or event.y//self.graph.taille == len(self.lab.grille)-1 or event.x//self.graph.taille == 0 or event.x//self.graph.taille==len(self.lab.grille[0])-1 : #si on clique sur un mur d'un bord
          print("pas possible")
          
        elif self.test_case_sortie(self.lab.grille)==True:
            if self.lab.grille[event.y//self.graph.taille][event.x//self.graph.taille] == 3: # si le carré est rouge il devient blanc
                self.lab.grille[event.y//self.graph.taille][event.x//self.graph.taille] = 0
        
        elif self.test_case_sortie(self.lab.grille)==False:
            if self.lab.grille[event.y//self.graph.taille][event.x//self.graph.taille] == 0: # si le carré est blanc il devient rouge
                self.lab.grille[event.y//self.graph.taille][event.x//self.graph.taille] = 3
                
        self.graph.Labyrinthe(self.graph.taille) # actualise avec 50 la taille des carré
        self.graph.Labyrinthe_binaire()
        self.graph.Graphe()
        
    def test_case_entree(self,l):
        """vérifie si dans le laby il y a une entrée pour créer une case entrée"""
        for i in range (len(l)):
            for j in range(len(l[0])):
                if l[i][j]==2: #verif si une entrée existe
                    return True
        return False
        
                
    def test_case_sortie(self,l):
        """vérifie si dans le laby il y a une sortie pour créer une case sortie"""
        for i in range (len(l)):
            for j in range(len(l[0])):
                if l[i][j]==3: #verif si une sortie existe
                    return True
        return False
    
class GraphiqueLab():
    
    def __init__(self,lab):
        
        self.my_canvas = 0
        self.lab=lab
        self.control=None
        
        self.initUI()

    def set_control(self,control):
        self.control=control
        
    def initUI(self):
        
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.bind('<Escape>',lambda e: self.root.destroy())
        self.root.title("Mazex")
        self.boutongroupe = tk.Frame(self.root)
        self.x = self.root.winfo_screenwidth() # récupère la largeur de l'écran
        self.y = self.root.winfo_screenheight() # récupère la hauteur de l'écran
        
        resolutions = str(int(self.x // 1.85))+'x'+str(int(self.y // 1.85)) # résolutions de la fenêtre divisé par 1.5 pour générer une petite fenêtre
        self.root.geometry(resolutions) # format 000x000 
        
        self.my_canvas1 = tk.Canvas(self.root, width=self.x//2, height=self.y//2,bg = "white")  #labyrinthe
        self.my_canvas2 = tk.Canvas(self.root, width=self.x//2, height=self.y//2,bg = "white")  #binaire
        self.my_canvas3 = tk.Canvas(self.root, width=self.x//2, height=self.y//1,bg = "white")  #graphe
        
        self.save = tk.Button(self.boutongroupe, text="sauvegarder", bg="red", fg="white", command = self.sauvegarder ) # bouton sauvegarder
        self.calcule = tk.Button(self.boutongroupe, text="calculer", bg="red", fg="white",command = self.calculer) # bouton calculer
        self.importe = tk.Button(self.boutongroupe, text="importer", bg="red", fg="white", command = self.import_laby) #bouton importer 
        self.quitter = tk.Button(self.boutongroupe, text ="quitter", bg = "red" , fg = "white", command = self.root.destroy)
        self.largeurgraphe = tk.Entry(self.boutongroupe,bg = "red")
        self.resolution = tk.Button(self.boutongroupe, text ="resolution", bg = "red" , fg = "white", command = self.graph)
        self.text = tk.Label(self.boutongroupe, text="")
        self.text2 = tk.Label(self.boutongroupe, text="Taille labyrinthe \n entre 4 et 34", background="pink")
        self.largeurgraphe.insert(0,"largeur") #place holder (text qui apparait deja de base dans le saisi de texte)
        self.largeurgraphe.bind("<Button-1>", lambda args: self.largeurgraphe.delete('0', 'end')) #enleve le texte lorsque l'on clique dessus
        
        self.longueurgraphe = tk.Entry(self.boutongroupe,bg = "red")
        self.longueurgraphe.bind("<FocusIn>", lambda args: self.longueurgraphe.delete('0', 'end'))
        self.longueurgraphe.insert(0,"longeur")
        self.boutongroupe.grid(row=0,rowspan = 2)
        self.text2.grid(row = 0 , column = 0)
        self.save.grid(row=1, column=0) #bouton sauvegarder
        self.importe.grid(row=2 , column = 0)
        self.largeurgraphe.grid(row=3,column=0)
        self.longueurgraphe.grid(row=4,column=0)
        self.calcule.grid(row=5, column =0)
        self.quitter.grid(row = 6 , column = 0)
        self.resolution.grid( row = 7 , column = 0)
        self.text.grid(row = 8 , column = 0)
        
        self.my_canvas1.grid(row=0, column=1)   #labyrinthe
        self.my_canvas1.bind('<Button-1>',self.clique_murs) #fonction clique mur 
        self.my_canvas1.bind('<Button-3>',self.clique_e) #fonction depart 
        self.my_canvas1.bind('<Double-Button-3>',self.clique_s) #fonction arriver
        
        self.my_canvas2.grid(row=1, column=1)  #binaire
        self.my_canvas3.grid(row=0, column=2,rowspan = 2) #graphe
        self.taille = (max(self.x,self.y )//4)//max(len(self.lab.grille),len(self.lab.grille[0]))
        
        
        self.Labyrinthe(self.taille)

        self.Labyrinthe_binaire()
        self.Graphe()

    def carrer(self,x,y,c,taille): #avec x et y du coin en haut a gauche d'un carrer et c couleur
        self.my_canvas1.create_rectangle(x,y,x+taille,y+taille,fill=c)
        
    def sauvegarder(self):
        self.control.sauvegarder()
    
    def calculer(self): #calculer le graphe en fonction des valeur entry largeur et hauteur
        self.control.calculer()
    
    def import_laby(self):
        self.control.import_laby()
    
    def clique_murs(self,event):
        self.control.clique(event)
        
    def clique_e(self,event):
        self.control.clique2(event)
    
    def clique_s(self,event):
        self.control.clique3(event)
        
    def verif_taille(self):
        """vérifie la taille et affiche le message d'erreur ou non"""
        if self.control.A==False:
            self.text.configure(text="Erreur \n taille trop grande \n 3< taille <35", background="pink")
            self.root.update()
            
        elif self.control.A==True:
            self.text.configure(text="", background="white")
            self.root.update()
        
    
    def Labyrinthe(self,taille):#avec comme largueur de carrer de taille "taille
        self.my_canvas1.delete("all")
        self.taille = taille
        for i in range(len(self.lab.grille)+1): #ligne
            self.my_canvas1.create_line((0,i*taille), (len(self.lab.grille[0]) * taille) ,(i*taille),fill="black")
        for i in range(len(self.lab.grille[0])+1): #colonne
            self.my_canvas1.create_line((i*taille), 0 , (i*taille), (len(self.lab.grille)*taille) ,fill="black")

        for i in range(len(self.lab.grille)): #remplies les cases en carrer noir ou blanc
            x = 0
            for j in self.lab.grille[i]:
                if j == 1:
                    self.carrer(x*taille,i*taille ,"black",taille )
                elif j == 0:
                    self.carrer(x*taille,i*taille ,"white",taille)
                elif j == 2:
                    self.carrer(x*taille,i*taille ,"green",taille) #soit 2 le depart
                elif j == 3:
                    self.carrer(x*taille,i*taille ,"red",taille)
                x+=1
                
                
    def Labyrinthe_binaire(self):
        self.my_canvas2.delete("all")
        largeur = (self.x//4)/max(len(self.lab.grille[0]),len(self.lab.grille)) #IL FAUT REMPLACER LE 500 PAR X
        for i in range(len(self.lab.grille)+1): #ligne
            self.my_canvas2.create_line((0,i*largeur), (len(self.lab.grille[0]) * largeur) ,(i*largeur),fill="black")
        for i in range(len(self.lab.grille[0])+1):
            self.my_canvas2.create_line((i*largeur), 0 , (i*largeur), (len(self.lab.grille)*largeur) ,fill="black")

        for i in range (len(self.lab.grille)):
            for j in range (len(self.lab.grille[0])): 
                self.my_canvas2.create_text(10+j*largeur,10+i*largeur,text=self.lab.grille[i][j])
      
    def Graphe(self):
        self.my_canvas3.delete("all")
        d = 75 #largeur
        t = 50 # taille
        self.rejoingnable = [0,2,3]
        for i in range (len(self.lab.grille)):
            for j in range(len (self.lab.grille[0])):
                self.my_canvas3.create_oval(j*d+t , i*d + t , j*d + 2*t , i*d+2*t, outline='green', width=1.5)
                self.my_canvas3.create_text((j*d)+3*t/2 , (i*d)+3*t/2 , text=(i,";",j),)
                if j != len (self.lab.grille[0])-1 :
                    
                    if self.lab.grille[i][j]in self.rejoingnable and self.lab.grille[i][j+1]in self.rejoingnable: # si les deux cases adjacente sont rejoinglable
                        self.my_canvas3.create_line(j*d + 2*t,(i*d)+3*t/2,j*d+2.5*t,(i*d)+3*t/2)
                if i !=len(self.lab.grille)-1:
                    if self.lab.grille[i][j] in self.rejoingnable and self.lab.grille[i+1][j] in self.rejoingnable:
                        self.my_canvas3.create_line((j*d)+3*t/2,i*d+2*t,j*d+3*t/2,i*d+2*t+t/2)
      
    
        
    def listtocord(l):
        listcord = []
        listcord_temp = []
        for y in range (len(l)):
            for x in range (len(l[0])):
                listcord_temp.append([str(x)+","+str(y),l[x][y]]) # list qui comprend x y et ca valeur
            listcord.append(listcord_temp)
            listcord_temp = []
    
        for i in range (len(listcord)):
            print (listcord[i])
        return listcord    
    
 
    
 
   
 
    def graph(self):
        self.cord = GraphiqueLab.listtocord(self.lab.grille)
        self.g = Graphe()
        for y in range (len(self.cord)):
            for x in range (len(self.cord[0])-1):
                if int(self.cord[y][x][1]) in self.rejoingnable and int(self.cord[y][x+1][1]) in self.rejoingnable:
                    self.g.ajouter_arc(self.cord[y][x][0],self.cord[y][x+1][0])
                    self.g.ajouter_arc(self.cord[y][x+1][0],self.cord[y][x][0])

                if int(self.cord[y][x][1]) in self.rejoingnable and int(self.cord[y+1][x][1]) in self.rejoingnable:
                    self.g.ajouter_arc(self.cord[y][x][0],self.cord[y+1][x][0])
                    self.g.ajouter_arc(self.cord[y+1][x][0],self.cord[y][x][0])

        occurance_d = 0 #occurence départ
        occurance_a = 0 #occurence arrivé
        
        for x in range(len(self.cord)-1): #cherche le point départ et arrivé
            for y in range((len(self.cord[0])-1)):
                if self.cord[y][x][1] == 2 and occurance_d < 1:
                    self.depart = self.cord[y][x][0]
                    occurance_d += 1
                elif self.cord[y][x][1] == 2:
                    print("probleme mon pote")
                if self.cord[y][x][1] == 3 and occurance_a < 1:
                    self.arrive = self.cord[y][x][0]
                    occurance_a += 1
                elif self.cord[y][x][1] == 3:
                    print("probleme mon pote")
                    
            
        
        
        
        self.dist = distance(self.g,self.arrive,self.depart)
               
        while self.dist != 0 :
           for i in (self.g.voisins(self.depart)):
               #print("i=",i)
               #print("distance(self.g,self.arrive,i) =",distance(self.g,self.arrive,str(i)))
               if self.dist > distance(self.g,self.arrive,str(i)):
                   #print(i,"i est plus cour que ",self.depart)
                   self.my_canvas1.create_line(int(self.depart[2])*self.taille + self.taille/2,int(self.depart[0])*self.taille + self.taille/2,int(i[2])*self.taille + self.taille/2,int(i[0])*self.taille + self.taille/2, fill ='orange', width=3)       
                   time.sleep(0.2)
                   self.my_canvas1.update_idletasks()
                   self.depart = str(i)
                   self.dist = distance(self.g,self.arrive,self.depart)


class Graphe:
    def __init__(self):
        self.adj = {}
    def ajouter_sommet(self, s):
        if s not in self.adj:
            self.adj[s] = set()
    def ajouter_arc(self, s1, s2):
        self.ajouter_sommet(s1)
        self.ajouter_sommet(s2)
        self.adj[s1].add(s2)
    def arc(self, s1, s2):
        return s2 in self.adj[s1]
    def sommets(self):
        return list (self.adj)
    def voisins(self, s):
        return self.adj[s]

def mainLab():
    a = Mazex(10,10)
    pygame.mixer.Channel(0).play(pygame.mixer.Sound('assets/sounds/ingame.wav'))
    graph = GraphiqueLab(a)
    control=Control()
    control.set_graphique(graph)
    graph.set_control(control)
    control.set_labyrinthe(a)
    graph.root.mainloop()

    """partie damien thomas ^^^ """






def main():
    
    Mazex(20,5)
    Graphique(Mazex)
    
    
    

if __name__ == '__main__':
    main()