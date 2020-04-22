# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 15:06:23 2020

@author: Carlos Jose Munoz
"""

from vista import ventana
from Modelo import espectral

import sys

from PyQt5.QtWidgets import QApplication 

class Principal(object):
    def __init__(self):        
        self.__app=QApplication(sys.argv)
        self.__mi_vista=ventana()
        self.__mi_biosenal=espectral()
        self.__mi_controlador=controlador(self.__mi_vista,self.__mi_biosenal)
        self.__mi_vista.asignarcontrolador(self.__mi_controlador)
    def main(self):
        self.__mi_vista.show()
        sys.exit(self.__app.exec_())

class controlador(object):
    def __init__(self, vista,modelo): 
        self._mi_vista=vista 
        self._mi_modelo= modelo
        
    def recibirruta (self, field):
        return self._mi_modelo.recibirruta(field)
        
    def grafsenal(self,signal,fs):
        return self._mi_modelo.grafsenal(signal,fs)
    
    def analice(self,w, t,p,smin,smax,num):
        return self._mi_modelo.analice(w,t,p,smin,smax,num)
    
    def calcularwavelet(self,fmin,fmax):
        return self._mi_modelo.calcularwavelet(fmin,fmax)
        
p=Principal()
p.main()