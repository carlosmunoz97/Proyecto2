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
        
        
    def  recibirruta(self,field):
        self.field=field
        self.math_contents=sio.loadmat(self.field)
        a=list(self.math_contents.keys())
        keys=[]
        for i in a:
            if (str(i)!= "__header__") and (str(i)!="__version__") and (str(i)!="__globals__"):
                keys.append(str(i))
        return keys
    
    def grafsenal(self, signnal,fs):
        self.senial=np.squeeze(self.math_contents[str(signnal)])
        self.senial=self.senial-np.mean(self.senial)
        self.time=np.arange(0,len(self.senial)/int(fs),1/int(fs))
        self.fs=int(fs)
        d=int(len(self.senial)/self.fs)
        numbers=[]
        for i in range(d):
            g=i+1
            c=d%g
            f=d/g
            if c==0:
                numbers.append(str(int(f)))
        return self.senial, self.time, numbers
    
    def analice(self, w,t,p,smin,smax,num):
        size=int(len(self.senial)/(self.fs*int(num)))
        params=dict(fs=self.fs,fpass=[int(smin),int(smax)], tapers= [int(w),int(t),int(p)], trialave=1)
        
        data=np.reshape(self.senial, (self.fs*size,int(num)), order='F')
        
        pxx,f=mtspectrumc(data,params)
        return pxx,f
    
    def calcularwavelet(self):
        mat_contents = sio.loadmat('dataset_senales.mat')
        #the data is loaded as a Python dictionary
        print("the loaded keys are: " + str(mat_contents.keys()));
        #in the current case the signal is stored in the data field
        ojos_cerrados = np.squeeze(mat_contents['ojos_cerrados']); #to explain
        ojos_abiertos = np.squeeze(mat_contents['ojos_abiertos']);
        anestesia = np.squeeze(mat_contents['anestesia']);
        anestesia = anestesia - np.mean(anestesia)
        
        import pywt
        period=1/250
        band=[4,30]
        scales=np.arange(1,250)
        frequencies=pywt.scale2frequency('cmor', scales)/period
        scales=scales[(frequencies >= band[0]) & (frequencies <= band[1])] 
        
        N = anestesia.shape[0]
        
        time_epoch = period*N
        
        time = np.arange(0, time_epoch, period)
        
        [coef, freqs] = pywt.cwt(anestesia, scales, 'cmor', period)
        
        power = (np.abs(coef)) ** 2
        
        
        
        return time, freqs, power