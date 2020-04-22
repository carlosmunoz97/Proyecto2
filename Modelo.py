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
        self.fs=int(fs)
        a=self.senial
        b=self.fs
        if len(a)%b!=0:
            z=int(len(a)/b)+1
            x=b*z-(b*(z-1))
            ceros=np.zeros(x-(len(a)%b))
            self.senial=np.append(a,ceros)
            
        d=int(len(self.senial)/self.fs)
        numbers=[]
        for i in range(d):
            g=i+1
            c=d%g
            f=d/g
            if c==0:
                numbers.append(str(int(f)))
        
        self.time=np.arange(0,len(self.senial)/int(fs),1/int(fs))
        return self.senial, self.time, numbers
    
    def analice(self, w,t,p,smin,smax,num):
        size=int(len(self.senial)/(self.fs*int(num)))
        params=dict(fs=self.fs,fpass=[int(smin),int(smax)], tapers= [int(w),int(t),int(p)], trialave=1)
        
        data=np.reshape(self.senial, (self.fs*size,int(num)), order='F')
        
        pxx,f=mtspectrumc(data,params)
        return pxx,f
    
    def calcularwavelet(self,fmin,fmax):        
        
        import pywt
        period=1/self.fs
        band=[fmin,fmax]
        scales=np.arange(1,250)
        frequencies=pywt.scale2frequency('cmor', scales)/period
        scales=scales[(frequencies >= band[0]) & (frequencies <= band[1])] 
        
        N = self.senial.shape[0]        
        time_epoch = period*N        
        time = np.arange(0, time_epoch, period)        
        [coef, freqs] = pywt.cwt(self.senial, scales, 'cmor', period)
        
        power = (np.abs(coef))**2         
        
        return time, freqs, power