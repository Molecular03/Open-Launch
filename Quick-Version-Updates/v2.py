import sys
import tkinter as tk #GUI Package
from tkinter import *
from tkinter import ttk
#import numpy as np
import matplotlib.pyplot as plt
#Imported in order to allow matplotlib graphs to be interacted with --> 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk) 

def set_window():
    window = tk.Tk()
    window.title("Rocket Simulation")
    mainframe = ttk.Frame(window, padding='5 5 5 5')
    mainframe.grid(sticky=(N,W,E,S)) #Creates the grid for all frames to be placed in
    window.columnconfigure(1,weight=1) #Tells frame to expand to fill extra space if window is resized and where to expand to.
    window.rowconfigure(0, weight=1)
    return window, mainframe

def integrate_plot(window,mainframe):
    global canvas
    fig = plt.figure(figsize=(9,9)) #Defines the matplotlib figure
	#Create tkinter canvas holding the matplotlib Figure
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().grid(row=0,column=0) #places canvas on window
    toolbarFrame = tk.Frame(master=window)
    toolbarFrame.grid(row=1,column=0)
    toolbar = NavigationToolbar2Tk(canvas,toolbarFrame)

def quit():
	window.destroy
	window.quit()

def add_plot_values():
    y = [i**2 for i in range(25)] #temporary variables
    z = [i**3 for i in range(25)]
    plt.plot(y), plt.plot(z)
    canvas.draw()

def temperature_choice_button(window):
    units = ['K','C','F'] #Add degree symbol
    unitvar = StringVar(window)
    unitvar.set(units[0])
    menu = OptionMenu(window,unitvar,*units)
    menu.grid(row=1,column=1)
    
def universal_constants():
    #Define G, Mass of earth (MoE), molar mass of dry air (MolAir), molar gass constant (R), P0, T0, rho0, g0
    G, g0 = 6.67e-11, 9.81 #Gravitational constant and Gravitational acceleration --> sea level
    MoE = 5.972e24 
    molAir, R = 0.028964, 8.3145
    P0 = float(input('Air pressure in launch area (Pa): ')) #Possible addition --> Add in averages for certain regions of the world by time of year
    temp_unit = input('Unit of temperature used (K, F or C): ') #Convert to button to choose F, K or C
    if temp_unit.upper() == 'K':
        T0 = float(input('Temperature in K: ')) #Initial temperature in kelvin
    elif temp_unit.upper() == 'C':
        T0 = float(input('Temperature in C: ')) + 273.15 #Initial temperature in kelvin
    else:
        T0 = ((float(input('Temperature in F: ')) - 32) * 5/9) + 273.15 #Initial temperature in kelvin
    rho0 = (molAir*P0)/(R*T0)  #Air density --> sea level
    constants = [G, MoE, molAir, R, P0, T0, rho0, g0]
    return constants

def rocket_specs():
    #Get rockets specs: thrust, drag coef., diameter, area, wet + dry mass, Isp, mass flow rate
    pass
    
def euler_cromer():
    #Initialize altitude (1m), velocity(0 m/s), mass (m0), air density (rho0), g0
    #t0 --> t max: 
        #update g and m, call: density func, wave drag func. Calculate: thrust, drag
        #If drag vector condition 
        #euler-cromer: v = v + (thrust - drag - g)*dt
                       #z = z+ v*dt
        #save matrix values for v,z,m,g,thrust,drag,rho
        #save end time
        #If crash
        #If empty
    #Plot z vs. t, v vs. t
    #Plot thrust, drag force, and g vs. t (Optional)
    pass
    
    
window, mainframe = set_window()
integrate_plot(window,mainframe)
Button(window, text='Plot', command=add_plot_values).grid(row=0,column=1) #Adds values to the plot
Button(window, text='Quit', command=quit).grid(row=2,column=1)
temperature_choice_button(window)
window.mainloop()
