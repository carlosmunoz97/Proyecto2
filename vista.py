# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 18:46:09 2020

@author: Carlos Jose Munoz
"""
import sys
#Qfiledialog es una ventana para abrir yu gfuardar archivos
#Qvbox es un organizador de widget en la ventana, este en particular los apila en vertcal
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFileDialog,QMessageBox
from PyQt5 import QtCore, QtWidgets

from PyQt5.QtGui import QIntValidator

from matplotlib.figure import Figure

from PyQt5.uic import loadUi

from numpy import arange, sin, pi
#contenido para graficos de matplotlib
from matplotlib.backends. backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import scipy.io as sio
import numpy as np
from Modelo import espectral

import pyqtgraph as pg

class MyGraphCanvas(FigureCanvas):
    #constructor
    def __init__(self, parent= None,width=5, height=4, dpi=100):
        
        #se crea un objeto figura
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        #el axes en donde va a estar mi grafico debe estar en mi figura
        self.axes = self.fig.add_subplot(111)        
        
        #se inicializa la clase FigureCanvas con el objeto fig
        FigureCanvas.__init__(self,self.fig)
        
    def limpiar(self):
        self.axes.clear()
        self.axes.figure.canvas.draw()
        
    def graficar_espectros(self, time, freqs, power,fmin,fmax):        
        self.axes.clear()        
        self.axes.contour(time, 
                          freqs[(freqs >= fmin) & (freqs <= fmax)],
                          power[(freqs >= fmin) & (freqs <= fmax),:],
                          1000,
                          extend='both')
        print("datos")
        self.axes.figure.canvas.draw()


class ventana (QMainWindow):
    def __init__(self): #abre la ventana inicial 
        super(ventana, self).__init__();
        loadUi('interfaz.ui',self)
        self.setup();
        self.show()
        self.imin=0
        self.imax=2000
        self.band=0
        self.index=0
        
    def setup(self):
        
        #los layout permiten organizar widgets en un contenedor
        #esta clase permite aÃ±adir widget uno encima del otro (vertical)
        layout = QVBoxLayout()
        #se aÃ±ade el organizador al campo grafico
        self.campo_grafica.setLayout(layout)
        #se crea un objeto para manejo de graficos
        self.__sc = MyGraphCanvas(self.campo_grafica, width=5, height=4, dpi=100)
        #se aÃ±ade el campo de graficos
        layout.addWidget(self.__sc)
        
        self.cargar.clicked.connect(self.carga)
        self.graficar.clicked.connect(self.grafica)
        self.frecmuestreo.setValidator(QIntValidator(1,1999))
        self.w.setValidator(QIntValidator(1,9))
        self.t.setValidator(QIntValidator(1,20))
        self.p.setValidator(QIntValidator(1,5))
        self.tiempodisminuir.clicked.connect(self.disminuir)
        self.tiempoaumentar.clicked.connect(self.aumentar)
        self.analyze.clicked.connect(self.analizar)
        self.graphspec.clicked.connect(self.graficar_espectro)
        self.grafica_espectro.clicked.connect(self.grafica_tf)
        
        self.grafica_espectro.setEnabled(False)
        
    def asignarcontrolador(self, c):# se crea el enlace entre esta ventana y el controlador 
        self.__mi_controlador = c
       
    def limpiar_campos(self):
            self.num.clear()
            self.t.setText("")
            self.w.setText("")
            self.p.setText("")
            self.sfmin.setText("")
            self.sfmax.setText("")
            self.gfmin.setText("")
            self.gfmax.setText("")
            
            
    def carga(self):
        self.limpiar_campos()
        self.campo_graficacion_2.clear()
        self.__sc.limpiar()
        self.num.clear()
        self.senales.clear()
        self.frecmuestreo.setText("")
        archivo,_=QFileDialog.getOpenFileName(self, "Abrir senal","","Archivos mat (*.mat)*")
        keys= self.__mi_controlador.recibirruta(archivo)
        for i in keys:
            self.senales.addItem(i)
        self.band=0
        self.index=0
        self.campo_graficacion.clear()
        
    def grafica(self):
        if self.frecmuestreo.text()=="":
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setText('Message Error')
            msg.setWindowTitle('Message Box')
            msg.setInformativeText('Please, write the sampling rate')
            msg.show()
        else:
            self.campo_graficacion.clear()
            self.campo_graficacion_2.clear()
            self.__sc.limpiar()
            signal=self.senales.currentText() 
            if (self.index != self.senales.currentIndex()):
                self.num.clear()
                self.band=0                
                self.index=self.senales.currentIndex()
            self.senial,self.time,self.numbers= np.asarray(self.__mi_controlador.grafsenal(signal,self.frecmuestreo.text()))
            if self.band==0:
                self.limpiar_campos()
                self.band=1
                self.imin=0
                self.imax=(len(self.senial)-1)
                self.sfmin.setValidator(QIntValidator(0,int(self.frecmuestreo.text())/2-1))
                self.sfmax.setValidator(QIntValidator(1,int(self.frecmuestreo.text())/2))
                for i in self.numbers:
                    self.num.addItem(str(i))
            x=np.asarray(self.time*1000)
                
            self.campo_graficacion.plot(x[self.imin:self.imax],self.senial[self.imin:self.imax],pen=('r'))
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
    
    def analizar(self):
        if (self.w.text()=="" or self.t.text()=="" or self.p.text()=="" or self.sfmin.text()=="" or self.sfmax.text()==""):
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setText('Message Error')
            msg.setWindowTitle('Message Box')
            msg.setInformativeText('Please, complete the requirements')
            msg.show()
        else:
            self.pxx,self.f=self.__mi_controlador.analice(self.w.text(), self.t.text(),self.p.text(),self.sfmin.text(),self.sfmax.text(),self.num.currentText())
            self.gfmin.setValidator(QIntValidator(int(self.sfmin.text()),int(self.sfmax.text())))
            self.gfmax.setValidator(QIntValidator(int(self.sfmin.text()),int(self.sfmax.text())))
            self.gfmin.setText(self.sfmin.text())
            self.gfmax.setText(self.sfmax.text())
            
            
    def graficar_espectro(self):
        self.campo_graficacion_2.clear()
        f=[]
        j=0
        for i in self.f:
            if (i>=int(self.gfmin.text()) and i<=int(self.gfmax.text())):
                f.append(i)
                j=i
        inicial=np.where(self.f==f[0])
        final=np.where(self.f==j)
        self.grafica_espectro.setEnabled(True)
        self.campo_graficacion_2.plot(f,self.pxx[inicial[0][0]:final[0][0]+1])
        self.campo_graficacion_2.repaint()
        
        
    def grafica_tf(self):
        [tiempo,freq,power]= self.__mi_controlador.calcularwavelet(int(self.sfmin.text()), int(self.sfmax.text()))
        self.__sc.graficar_espectros(tiempo, freq, power, int(self.gfmin.text()), int(self.gfmax.text()))