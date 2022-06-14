# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 09:12:08 2021

@author: bart.bozon
"""

import matplotlib.pyplot as plt
import numpy as np

maxarray=1000
x=np.zeros((maxarray),dtype=float)  # positie
xv=np.zeros((maxarray),dtype=float) # snelheid
setpoint=np.zeros((maxarray),dtype=float)
t=np.zeros((maxarray),dtype=float)
stuuractie=np.zeros((maxarray),dtype=float)

def voer_simulate_uit(kp,ki,kd):
    dt = 0.01           # [s] 
    massa = 0.1         # [kg]
    zwaartekracht_constante = 9.81 # [m.s-2]
    delay=0
    montage_offset=0
    x[0]=0
    prev_error=0    # nu nog niet gebruikt. Misschien handig voor d-actie?
    i_error=0       # nu nog niet gebruikt. Misschien handig voor i-actie?
    for i in range (maxarray-1-delay):
        totale_kracht = zwaartekracht_constante * massa *np.sin(stuuractie[i]+montage_offset)
        versnelling = totale_kracht / massa
        xv[i+1] = xv[i]+versnelling *dt
        x[i+1]=x[i]+xv[i+1]*dt
        t[i+1]=t[i]+dt
        #==============  HIER KOMT JOUW CODE ======================
        error=setpoint[i+1]-x[i+1]
        stuuractie[i+1+delay]=kp*error
        #==============  EINDE JOUW CODE ==========================
        if stuuractie[i+1]<-0.2 :
            stuuractie[i+1]=-0.2
        if stuuractie[i+1]>0.2 :
            stuuractie[i+1]=0.2
            
    fig,ax= plt.subplots()
    plt.plot(t[:maxarray-delay],x[:maxarray-delay],t[:maxarray-delay],setpoint[:maxarray-delay])
    plt.title ('uitslag en setpoint')
    plt.xlabel('Tijd (s)')
    plt.ylabel('Amplitude ()')
    plt.show()    
    plt.plot(t[:maxarray-delay],x[:maxarray-delay],t[:maxarray-delay],stuuractie[:maxarray-delay])
    plt.title ('uitslag en stuuractie')
    plt.xlabel('Tijd (s)')
    plt.ylabel('Amplitude ()')
    plt.show()    

setpoint[100:]=0.5   

voer_simulate_uit (1,0,0)

voer_simulate_uit (2,0,1)

        
    
    
    