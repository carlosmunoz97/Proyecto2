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
        self.__mi_vista=ventana() # objeto asociado a la ventana de inicio
        self.__mi_biosenal=espectral()
        self.__mi_controlador=controlador(self.__mi_vista,self.__mi_biosenal)
        self.__mi_vista.asignarcontrolador(self.__mi_controlador)
    def main(self):
        self.__mi_vista.show() # Se genera la ventana de visualizacion
        sys.exit(self.__app.exec_())

class controlador(object): # Este objeto recibe los comandos de la vista que son enviados al modelo para realizar la accion necesaria
    def __init__(self, vista,modelo): 
        self._mi_vista=vista # Atributo para la apertura de la ventana
        self._mi_modelo= modelo # Apertura del modelo
        
    def recibirruta (self, field): # Recibe el archivo de la senal
        return self._mi_modelo.recibirruta(field)
        
    def grafsenal(self,signal,fs): # Retorna la senal cargada
        return self._mi_modelo.grafsenal(signal,fs)
    
    def analice(self,w, t,p,smin,smax,num): # Retorna el analisis multitaper de la senal
        return self._mi_modelo.analice(w,t,p,smin,smax,num)
    
    def calcularwavelet(self,fmin,fmax): # Entrega el espectro tiempo-frecuencia
        return self._mi_modelo.calcularwavelet(fmin,fmax)
        
p=Principal() #se genera la interfaz 
p.main() #se inicial y muestra l ainterfaz
