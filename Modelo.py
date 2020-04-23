# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 15:06:38 2020

@author: Carlos Jose Munoz
"""

import numpy as np
import matplotlib.pyplot as plt
from csv import reader as reader_csv
import scipy.signal as signal
import scipy.io as sio
import math
from chronux.mtspectrumc import mtspectrumc

class espectral:
    def __init__(self):
        self.field=""
        
        
    def  recibirruta(self,field): # Se carga la señal y se obtienen las llaves que contiene el diccionario de esta
        self.field=field
        self.math_contents=sio.loadmat(self.field)
        a=list(self.math_contents.keys())
        keys=[]
        for i in a:
            if (str(i)!= "__header__") and (str(i)!="__version__") and (str(i)!="__globals__"):
                keys.append(str(i))
        return keys
    
    def grafsenal(self, signnal,fs): # Permite graficr la señal cargada
        self.senial=np.squeeze(self.math_contents[str(signnal)]) #Comando squeeze reduce una dimension del vector de la senal
        self.senial=self.senial-np.mean(self.senial) # Se obtiene el promedio de la senal
        self.fs=int(fs) # Recibe el valor de la frecuencia de muestreo
        a=self.senial
        b=self.fs
        if len(a)%b!=0: # Rellena de ceros la senal cuando esta no contiene un numero de datos múltiplo de la frecuencia 
            z=int(len(a)/b)+1
            x=b*z-(b*(z-1))
            ceros=np.zeros(x-(len(a)%b))
            self.senial=np.append(a,ceros)
            
        d=int(len(self.senial)/self.fs)
        numbers=[]
        for i in range(d): # Permite obtener los numeros de segmentos en los que es posible partir la senal
            g=i+1
            c=d%g
            f=d/g
            if c==0:
                numbers.append(str(int(f)))
        
        self.time=np.arange(0,len(self.senial)/int(fs),1/int(fs))  # Se obtiene el vector de tiempo para la graficacion del analisis multitaper
        return self.senial, self.time, numbers
    
    def analice(self, w,t,p,smin,smax,num): #realiza el analisis de por multitaper, y devuelve las frecuencias y la potencia como vector 
        size=int(len(self.senial)/(self.fs*int(num)))
        params=dict(fs=self.fs,fpass=[int(smin),int(smax)], tapers= [int(w),int(t),int(p)], trialave=1) #se ingresan los parametros con los que se realiza el analisis multitaper 
        
        data=np.reshape(self.senial, (self.fs*size,int(num)), order='F')
        
        pxx,f=mtspectrumc(data,params) #genera el analisis de multitaper 
        return pxx,f
    
    def calcularwavelet(self,fmin,fmax): # Calculo        
        
        import pywt
        period=1/self.fs # Se calcula el periodo de la senal
        band=[fmin,fmax] # Banda de frecuencia que se desea analizar
        scales=np.arange(1,250) # numero de escalas 
        frequencies=pywt.scale2frequency('cmor', scales)/period 
        scales=scales[(frequencies >= band[0]) & (frequencies <= band[1])]  # Se extrae la escalas correspondientes a las frecuencias de interés
        
        
        N = self.senial.shape[0]        # numero de datos de la senal 
        time_epoch = period*N           # Tiempo correspondiente a una epoca de la señal (en segundos)
        time = np.arange(0, time_epoch, period)        
        [coef, freqs] = pywt.cwt(self.senial, scales, 'cmor', period) # Calculo de la transformada continua de Wavelet. Se implementa  Complex Morlet Wavelet
        
        power = (np.abs(coef))**2   # Calculo de potencia       
        
        return time, freqs, power
