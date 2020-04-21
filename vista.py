# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 18:46:09 2020

@author: Carlos Jose Munoz
"""

from PyQt5.QtWidgets import QMainWindow,QMessageBox,QFileDialog
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIntValidator

import numpy as np
import scipy.io as sio
import matplotlib as plt 

class ventana (QMainWindow):
    def __init__(self): #abre la ventana inicial 
        super(ventana, self).__init__();
        loadUi('interfaz.ui',self)
        self.setup();
        self.imin=0
        self.imax=2000
        self.band=0
        
    def setup(self):
        
        self.cargar.clicked.connect(self.carga)
        self.graficar.clicked.connect(self.grafica)
        
        self.tiempodisminuir.clicked.connect(self.disminuir)
        self.tiempoaumentar.clicked.connect(self.aumentar)
        
        
    def asignarcontrolador(self, c):# se crea el enlace entre esta ventana y el controlador 
        self.__mi_controlador = c
        
    def carga(self):
        self.senales.clear()
        archivo,_=QFileDialog.getOpenFileName(self, "Abrir senal","","Archivos mat (*.mat)*")
        keys= self.__mi_controlador.recibirruta(archivo)
        for i in keys:
            self.senales.addItem(i)
        
    def grafica(self): 
        self.campo_graficacion.clear()
        signal=self.senales.currentText()       
        self.senial= np.asarray(self.__mi_controlador.grafsenal(signal))
        if self.band==0:
            self.band=1
            self.imax=len(self.senial)-1
        x=np.asarray(list(range(self.imin,self.imax)))
        self.campo_graficacion.plot(x,self.senial[self.imin:self.imax],pen=('r'))
        self.campo_graficacion.repaint()
        
    def disminuir(self):
        if (self.imin==0 and self.imax==2000):
            self.imax=len(self.senial)-1        
        
        elif (self.imin==0 and self.imax==(len(self.senial)-1)):
            self.imin=int((len(self.senial)-1)/2000)*2000
        
        elif (self.imin==(int((len(self.senial)-1)/2000)*2000) and self.imax==(len(self.senial)-1)):
            self.imax=self.imin
            self.imin=self.imin-2000
        else:
            self.imax=self.imax-2000
            self.imin=self.imin-2000
        self.grafica()
        
    def aumentar(self):
        if (self.imin==0 and self.imax==(len(self.senial)-1)):
            self.imax=2000
        elif(self.imax==(int((len(self.senial)-1)/2000)*2000) and self.imin==((int((len(self.senial)-1)/2000)*2000)-2000)):
            self.imin=self.imax
            self.imax=len(self.senial)-1
        elif((self.imax==len(self.senial)-1) and (self.imin==(int((len(self.senial)-1)/2000)*2000))):
            self.imin=0
        else:
            self.imin=self.imin+2000
            self.imax=self.imax+2000
        self.grafica()