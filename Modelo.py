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
    
    def grafsenal(self, signnal):
        self.senial=np.squeeze(self.math_contents[str(signnal)])
        return self.senial