# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 15:06:23 2020

@author: Carlos Jose Munoz
"""

from vista import ventana
from Modelo import espectral

import sys

from PyQt5.QtWidgets import QApplication 


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
    
    def calcularwavelet(self):
        return self._mi_modelo.calcularwavelet()
        
if __name__ == '__main__':
    app=QApplication(sys.argv)
    mi_vista=ventana()
    mi_modelo=espectral()
    mi_controlador=controlador(mi_vista,mi_modelo);
    
    mi_vista.asignarcontrolador(mi_controlador)
    
    mi_vista.show()
    
    sys.exit(app.exec_());