import pyforest
import tkinter as tk #GUI Package
from decimal import *
import numpy as np
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk) #Imported in order to allow matplotlib graphs to be interacted with

class Var:
	def __init__(self,name,num):
	    self.name = name
	    self.value = Decimal(num)
	    
	def print_value(self):
	    print(self.value)
        
def quit():
    window.destroy
    window.quit()#Air density --> sea level

def validate_input(entry, error_string, errPhrase):
    var = entry.get()
    if var:
        var = float(var)
    else:
        var = 1.0
        error_string += errPhrase
    return var, error_string
    
def get_values():
    global G, g_z, MoE, Mol_Air, R, T_z, P_z, Thrust_z, Cd_z, Radius, WetM, DryM, WetM, Isp, rho_z, A
    error_string = ''
    tUnit = str(tUnitSelection.get()).upper()
    G = Var('Gravitational Constant',6.67e-11)
    g_z = Var('Gravitational Acceleration', -9.81)
    MoE = Var('Mass of Earth (kg)', 5.972e24)
    Mol_Air = Var('Molar mass of dry air',289.64)
    R = Var('Molar gass constant', 8.3145)
    t0, error_string = validate_input(TempEntry,error_string,'\nTemperature at pad')
    if tUnit == 'K':
        t0 = t0
    elif tUnit == 'C':
        t0 += 273.15
    elif tUnit == 'F':
        t0 = ((t0 - 32) * 5/9) + 273.15
    else:
        error_string += '\nUnit of temperature (K,C,F)'
    T_z = Var('Temperature',t0)
    p0, error_string = validate_input(PressureEntry,error_string,'\nPressure at pad')
    P_z = Var('Pressure',p0)
    thrust0, error_string = validate_input(ThrustEntry,error_string,'\nThrust')
    Thrust_z = Var('Thrust',thrust0)
    Cd0, error_string = validate_input(DragCoEntry,error_string,'\nDrag Coefficient')
    Cd_z = Var('Cd', Cd0)
    r, error_string = validate_input(REntry,error_string,'\nRadius')
    Radius = Var('Radius', r)
    WetM0, error_string = validate_input(WetMassEntry,error_string,'\nWet mass')
    WetM = Var('Wet Mass', WetM0)
    dryM, error_string = validate_input(DryMassEntry,error_string,'\nDry mass')
    DryM = Var('Dry Mass', dryM)
    isp, error_string = validate_input(IspEntry,error_string,'\nIsp')
    Isp = Var('Isp', isp)
    rho = (Mol_Air.value*T_z.value) / (R.value * P_z.value) #Air density
    rho_z = Var('Air Density/Rho', rho)
    area = np.pi*(r**2)
    A = Var('Cross Sectional Area', area)
    if error_string != '':
        error_string = 'Please Enter:' + error_string
        errorLabel.config(text=error_string)
    else:
        errorLabel.config(text=error_string)
        plotButton.grid(row=1,column=5)
    '''
    #For example:
    T_z = Var('Temperature',300)
    P_z = Var('Pressure',101325)
    Thrust_z = Var('Thrust',560000)
    Cd_z = Var('Cd', 0.75)
    Radius = Var('Radius', 1.75/2)
    WetM = Var('Wet Mass', 46760)
    DryM = Var('Dry Mass', 3120)
    Isp = Var('Isp', 221)
    rho = (Mol_Air.value*T_z.value) / (R.value * P_z.value) #Air density
    rho_z = Var('Air Density/Rho', rho)
    area = np.pi*((1.75/2)**2)
    A = Var('Cross Sectional Area', area)
    plotButton.grid(row=1,column=5)
    '''
    
def density(T_z,z,P_z,g_z): #http://www.braeunig.us/space/atmmodel.htm#equations (Note: This is an approximation, will possibly get more exact in future updates)
    z_km = z / Decimal(1000) #altitude in km
    Lm = Decimal(279.65) * z_km #Lapse rate at altitude z
    T_z = T_z - Lm #Initial temp - lapse rate
    P_z = P_z*(T_z/T_z)**((g_z*Decimal(0.029))/(R.value*Lm))
    rho_z = (Decimal(0.029)*T_z)/(R.value*P_z)
    return rho_z, T_z, P_z

def drag_coefficient(v,T_z,Cd_z):
    n = Mol_Air.value*Decimal(1.4)
    if T_z > Decimal(0):
        speed_sound = Decimal(np.sqrt(n*T_z))
        Mach = v/speed_sound
        if Mach > Decimal(1):
            Cd_z /= Decimal(np.sqrt(Mach**2 - Decimal(1)))
        elif Mach == Decimal(1):
            Mach -= 1e-5
            Cd_z /= Decimal(np.sqrt(Mach**2 - Decimal(1)))
        else: 
            Cd_z /= Decimal(np.sqrt(Decimal(1)-Mach**2))
    else:
        Cd_z = 1
    return Cd_z

def g_getter(z,earth_grav,g_z):
    distance_from_earth = z+Decimal(6.371e6)
    distance_from_earth = Decimal(int(distance_from_earth))
    g_z = -earth_grav/(distance_from_earth**2) #Gravitational acceleration update as function of z
    return g_z

def euler_cromer():
    getcontext().prec = 32
    z = Var('Altitude', 1)
    v = Var('Velocity', 0)
    t = Var('Time', 0.1)
    dt = Var('dt', 0.1)
    z_values, t_values = [], []
    earth_grav =  Decimal(G.value*MoE.value)
    earth_grav = round(earth_grav,2)
    Fdrag = Var('Drag force', 1.0)
    mflowrate = Thrust_z.value/(g_z.value*Isp.value)
    Mass_flow_rate = Var('Mass flow rate', mflowrate)
    while t.value <= Isp.value:
        if z.value < Decimal(0): #Crash Condition
            print('Crashed!') #Change to a Tkinter output 
            break
        if WetM.value <= DryM.value: #If current mass is less than/equal to dry mass, no more propellant is available
            Thrust_z.value = 0
            Mass_flow_rate = 0
            print('No more fuel') #Change to a Tkinter output 
            break
        if int(g_z.value) == 0 or int(g_z.value) == 1:
            g_z.value = Decimal(1.0)
        else:
            g_z.value = g_getter(z.value,earth_grav,g_z.value)
        WetM.value += Mass_flow_rate.value #Mass update from fuel use
        rho_z.value, T_z.value, P_z.value = density(T_z.value,z.value,P_z.value,g_z.value) #Rho, temp, pressure update
        Cd_z.value = drag_coefficient(v.value, T_z.value, Cd_z.value) #Drag coefficient
        Thrust_z.value /= WetM.value
        v_sq = v.value**2
        Fdrag.value = (rho_z.value*v_sq*Cd_z.value*(A.value/WetM.value))/2
        if v.value < 0:
            Fdrag.value *= -1
        v.value += (Thrust_z.value - Fdrag.value - g_z.value)*dt.value
        z.value += v.value*dt.value
        t.value += dt.value
        z_values.append(z.value)
        t_values.append(t.value)
    plt.plot(t_values,z_values,'-o')
    plt.grid(True)
    ax = plt.gca()
    ax.spines['top'].set_color('none')
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    canvas.draw()
    window.update()
        
#Create tkinter window
window = tk.Tk()
window.columnconfigure(2,weight=2) #Tells frame to expand to fill extra space if window is resized and where to expand to.
window.rowconfigure(0, weight=1)
plotFrame = Frame(window) #Where the plot will stay
plotFrame.grid(column=1,row=0)
inputSection = Frame(window) #Where the user will input data
inputSection.grid(column=2,row=0)

#Integrate Matplotlib 
fig = plt.figure(figsize=(7,7))
canvas = FigureCanvasTkAgg(fig, master=plotFrame) #Create tkinter canvas that holds the matplotlib Figure
canvas.get_tk_widget().grid(row=0,column=0) #Places canvas on plotFrame
toolbarFrame = tk.Frame(master=plotFrame)
toolbarFrame.grid(row=1,column=0)
toolbar = NavigationToolbar2Tk(canvas,toolbarFrame)

#Basic Buttons
quitButton = Button(inputSection, text='Quit', command=quit).grid(row=2,column=5)
getVariables = Button(inputSection, text='Calculate', command=get_values).grid(row=0,column=5)
plotButton = Button(inputSection, text='Plot', command=euler_cromer)

#Error Thrower
errorLabel = Label(inputSection, text='')
errorLabel.grid(row=0, column=7)

#All entries
TempEntry = Entry(inputSection) #Enter temperature
TempEntry.grid(row=1,column=1)
Label(inputSection, text='Temp:').grid(row=1,column=0)
PressureEntry = Entry(inputSection) #Enter Pressure
PressureEntry.grid(row=2,column=1)
Label(inputSection, text='Pressure (Pa):').grid(row=2,column=0)
ThrustEntry = Entry(inputSection) #Enter Rocket Specs.
ThrustEntry.grid(row=3,column=1)
Label(inputSection, text='Thrust (N):').grid(row=3,column=0)
DragCoEntry = Entry(inputSection) #Enter Drag Coefficient
DragCoEntry.grid(row=4,column=1)
Label(inputSection, text='Drag Co:').grid(row=4,column=0)
REntry = Entry(inputSection) #Enter Radius
REntry.grid(row=5,column=1)
Label(inputSection, text='Radius (m):').grid(row=5,column=0)
WetMassEntry = Entry(inputSection) #Enter Wet Mass
WetMassEntry.grid(row=6,column=1)
Label(inputSection, text='Wet Mass (kg):').grid(row=6,column=0)
DryMassEntry = Entry(inputSection) #Enter Dry Mass
DryMassEntry.grid(row=7,column=1)
Label(inputSection, text='Dry Mass (kg):').grid(row=7,column=0)
IspEntry = Entry(inputSection) #Enter Isp
IspEntry.grid(row=8,column=1)
Label(inputSection, text='Isp (s):').grid(row=8,column=0)

#Select Unit of temperature
tUnits = ['K','C','F']
tUnitSelection = ttk.Combobox(inputSection,values=tUnits)
tUnitSelection.set('Temp. Unit')
tUnitSelection.grid(row=0,column=1)

window.mainloop()
#https://pages.vassar.edu/magnes/2019/05/12/computational-simulation-of-rocket-trajectories/
