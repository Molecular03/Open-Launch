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
    window.columnconfigure(2,weight=2) #Tells frame to expand to fill extra space if window is resized and where to expand to.
    window.rowconfigure(0, weight=1)
    plotFrame = Frame(window)
    plotFrame.grid(column=1,row=0)
    inputSection = Frame(window)
    inputSection.grid(column=2,row=0)
    return window, inputSection, plotFrame

def integrate_plot():
    global canvas
    fig = plt.figure(figsize=(7,9)) #Defines the matplotlib figure
	#Create tkinter canvas holding the matplotlib Figure
    canvas = FigureCanvasTkAgg(fig, master=plotFrame)
    canvas.get_tk_widget().grid(row=0,column=0) #places canvas on plotFrame
    toolbarFrame = tk.Frame(master=plotFrame)
    toolbarFrame.grid(row=1,column=0)
    toolbar = NavigationToolbar2Tk(canvas,toolbarFrame)

def quit(): window.destroy, window.quit()

def add_plot_values():
    y = [i**2 for i in range(25)] #temporary variables
    z = [i**3 for i in range(25)]
    v = [i**4 for i in range(25)]
    plt.plot(y), plt.plot(z), plt.plot(v)
    canvas.draw()
	
def universal_constants():
    global constants
    constants = []
    tUnit = tUnitSelection.get()
    #Define G, Mass of earth (MoE), molar mass of dry air (MolAir), molar gass constant (R), P0, T0, rho0, g0
    G, g0 = 6.67e-11, 9.81 #Gravitational constant and Gravitational acceleration --> sea level
    MoE = 5.972e24
    molAir, R = 0.028964, 8.3145
    error_string = ''
    getTemp = str(TempEntry.get()) 
    if getTemp.isnumeric() is False: 
        error_string += '\nPlease enter a temperature'
        T0 = 0
    else: 
        T0 = float(getTemp)
    if tUnit == 'K':
        error_string += '\nThank you for using kelvin'
    elif tUnit == 'C':
        T0 += 273.15 #Initial temperature in kelvin
    elif tUnit == 'F':
        T0 = ((T0 - 32) * 5/9) + 273.15 #Initial temperature in kelvin
        error_string += '\nPlease consider using celsius or kelvin next time'
    else:
        error_string += '\nPlease select a Unit of temperature'
    if PressureEntry.get().isnumeric() is False:
        error_string += '\nPlease enter the pressure at the pad'
        P0 = 1.0
    else: 
        P0 = float(PressureEntry.get())
    errorLabel.config(text=error_string)
    inputSection.update()
    passableErrors = ['','\nPlease consider using celsius or kelvin next time','\nThank you for using kelvin']
    if error_string in passableErrors:
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

window, inputSection, plotFrame = set_window()
integrate_plot()
plotButton = Button(inputSection, text='Plot', command=add_plot_values).grid(row=4,column=1) #Adds values to the plot
quitButton = Button(inputSection, text='Quit', command=quit).grid(row=6,column=1)

#Select Unit of temperature
tUnits = ['K','C','F']
tUnitSelection = ttk.Combobox(inputSection,values=tUnits)
tUnitSelection.set('Temp. Unit')
tUnitSelection.grid(row=0,column=1)

#Enter temperature
TempPrompt = Label(inputSection,text='Temp: ').grid(row=1,column=0)
TempEntry = Entry(inputSection)
TempEntry.grid(row=1,column=1)

#Enter Pressure
PressurePrompt = Label(inputSection,text='Pressure (Pa): ').grid(row=2,column=0)
PressureEntry = Entry(inputSection)
PressureEntry.grid(row=2,column=1)

#Error Throwers
errorLabel = Label(inputSection, text='')
errorLabel.grid(row=3,column=1)

getConstants = Button(inputSection, text='Calculate', command=universal_constants).grid(row=0,column=2)

window.mainloop()
