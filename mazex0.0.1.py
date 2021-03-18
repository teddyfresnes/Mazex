#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 14:30:49 2021

@author: teddy
"""

"""
Mazex
"""

import tkinter as tk

class Mazex():

    def __init__(self,h,l):
        
        self.h = h # hauteur
        self.l = l # largeur
        self.grille = [[0] * h for i in range(l)]
        
        self.initTab()
        self.affiche()
        
        
    def initTab(self):
        
        for Colonne in range(self.h): # Mur gauche 
            self.grille[0][Colonne] = 1
    
        for Colonne in range(self.h): # Mur droit
            self.grille[self.l-1][Colonne] = 1
    
        for Ligne in range(self.l): # Mur haut
            self.grille[Ligne][0] = 1
    
        for Ligne in range(self.l): # Mur bas
            self.grille[Ligne][self.h-1] = 1
            
            
    def affiche(self):
        for j in range (self.h):
            for i in range(self.l):
                print(self.grille[i][j]," ", end=" ")
            print("")
 

class Graphique():
    
    def __init__(self,lab):
        
        super().__init__()
        
        self.initUI()
        

    def initUI(self):
        
        self.root = tk.Tk()
        self.root.title("Mazex")
        
        x = self.root.winfo_screenwidth() # récupère la largeur de l'écran
        y = self.root.winfo_screenheight() # récupère la hauteur de l'écran
        resolutions = str(int(x // 1.85))+'x'+str(int(y // 1.85)) # résolutions de la fenêtre divisé par 1.5 pour générer une petite fenêtre
        self.root.geometry(resolutions) # format 000x000 
        
        self.root.mainloop()    
        


def main():
    
    Mazex(20,5)
    Graphique(Mazex)


if __name__ == '__main__':
    main()
