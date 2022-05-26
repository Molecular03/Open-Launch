import pyforest
import tkinter as tk #GUI Package
from decimal import Decimal as d
import numpy as np
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk) #Imported in order to allow matplotlib graphs to be interacted with

class Var:
	def __init__(self,name,num):
	    self.name = name
	    self.value = d(num)
	    
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
    global G, g_z, MoE, Mol_Air, R, T_z, P_z, P_0, Thrust_z, Cd_z, Radius, WetM, DryM, WetM, Isp, rho_z, A, Thrust_0, Cd_0
    error_string = ''
    G = Var('Gravitational Constant',6.67e-11)
    g_z = Var('Gravitational Acceleration', -9.81)
    MoE = Var('Mass of Earth (kg)', 5.972e24)
    Mol_Air = Var('Molar mass of dry air',0.029)
    R = Var('Molar gass constant', 8.3145)
    t0, error_string = validate_input(TempEntry,error_string,'\nTemperature at pad')
    T_z = Var('Temperature',t0)
    p0, error_string = validate_input(PressureEntry,error_string,'\nPressure at pad')
    P_z = Var('Pressure',p0)
    P_0 = Var('Initial Pressure', p0)
    thrust0, error_string = validate_input(ThrustEntry,error_string,'\nThrust')
    Thrust_z = Var('Thrust',thrust0)
    Thrust_0 = Var('Initial Thrust', thrust0)
    Cd0, error_string = validate_input(DragCoEntry,error_string,'\nDrag Coefficient')
    Cd_0 = Var('Initial Cd', Cd0)
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

def temp_pressure_get(z):
    b = d(216.65)
    c = d(34.1632)
    e = d(270.65)
    h = c/d(2.8)
    if z >= d(86):
        B = round(z**3,2)
        C = round(z**2,2)
    if z >= d(0) and z < d(11):
        a = d(6.5) * z
        T_m = d(288.15) - a
        f = d(288.15)
        ff = (f/(f-a)) ** (c/d(-6.5)) 
        P = P_0.value * ff
    elif z >= d(11) and z < d(20):
        T_m = d(216.63)
        f = d(22632.06)
        ff = (-c * (z - d(11))) / b
        P = f * np.exp(ff)
    elif z >= d(20) and z < d(32):
        T_m = d(196.65) + z 
        f = d(5474.889)
        ff = b / (b + (z - 20))
        P = f * (ff**c)
    elif z >= d(32) and z < d(47):
        a = d(2.8) * z
        T_m = d(139.05) + a
        f = d(228.65)
        g = f + (d(2.8) * (z-d(32)))
        ff = (f/g) ** h
        P = d(868.0187) * ff
    elif z >= d(47) and z < d(51):
        T_m = e
        f = -c * (z-d(47))
        ff = f / e
        P = d(110.9063) * np.exp(ff)
    elif z >= d(51) and z < d(71):
        a = d(2.8) * z
        T_m = d(413.45) - a
        f = d(2.8) * (z - d(51))
        ff = e/(e-f)
        P = d(66.93887) * (ff) ** -h
    elif z >= d(71) and z < d(86):
        a = d(2.0) * z
        T_m = d(356.65) - a
        f = d(214.65)
        g = d(2) * (z-d(71))
        ff = f / (f-g)
        gg = c / d(-2)
        P = d(3.956420) * (ff**gg)
    elif z >= d(86) and z < d(91):
        T_m = d(186.8673)
        BB = round(d(2.159582E-06) * B, 3)
        CC = round(d(-4.836957E-04) * C, 3)
        DD = round(d(-0.1425192) * z, 3)
        P = BB + CC + D + d(13.48)
    elif z >= d(91) and z < d(110):
        a = (z-d(91)) / d(-19.9429)
        b = d(1)-(a**2)
        T_m = d(186.8673) * np.sqrt(b)
        BB = round(d(3.304895E-05) * B, 3)
        CC = round(d(-0.019) * C, 3)
        DD = round(d(1.72) * z, 3)
        P = BB + CC + D + d(-47.75)
    elif z >= d(110) and z < d(120):
        a = z - d(110)
        T_m = d(252) * a
        BB = round(d(-6.539316E-05) * B, 3)
        CC = round(d(0.025) * C, 3)
        DD = round(d(-3.22) * z, 3)
        P = BB + CC + D + d(135.94)
    elif z >= d(120.0) and z < d(1000):
        a = d(6473.77) / (d(6356.77)+z)
        epsilon = (z - d(120)) * a
        T_m = d(360) * np.exp(epsilon)
        A = round(z**4,2)
        AA = round(d(2.283506E-07) * A, 3)
        BB = round(d(-1.343221E-04) * B, 3)
        CC = round(d(0.03) * C, 3)
        DD = round(d(-3.055) * z, 3)
        P = BB + CC + D + d(113.58)
    return T_m, P
    
def density(z): #http://www.braeunig.us/space/atmmodel.htm#equations (Note: This is an approximation, will possibly get more exact in future updates)
    R = d(287.053)
    z = round(z,2)
    z /= 1000 #Altitude in km
    T_m, P = temp_pressure_get(z)
    T_m = round(T_m, 3)
    P = round(P,3)
    rho = P / (R * T_m)
    return rho, T_m, P

def drag_coefficient(v,T_z,Cd_z,Cd_0):
    n = Mol_Air.value*d(1.4)
    if T_z > d(0):
        speed_sound = d(np.sqrt(n*T_z))
        Mach = v/speed_sound
        if Mach > d(1):
            Prandtl_Glauert = d(np.sqrt(Mach**2-d(1)))
            Cd_z = Cd_0/Prandtl_Glauert
        elif Mach == d(1):
            Mach -= 1e-5
            Prandtl_Glauert = d(np.sqrt(Mach**2-d(1)))
            Cd_z = Cd_0/Prandtl_Glauert
        elif Mach < d(1): 
            l = d(1)-Mach**2
            if l < 0:
                l *= -1
            Prandtl_Glauert = d(np.sqrt(l))
            Cd_z = Cd_0/Prandtl_Glauert
    else:
        Cd_z = 1
    return Cd_z

def g_getter(z,earth_grav,g_z):
    distance_from_earth = z+d(6.371e6)
    distance_from_earth = d(int(distance_from_earth))
    g_z = -earth_grav/(distance_from_earth**2) #Gravitational acceleration update as function of z
    return g_z

def euler_cromer():
    z = Var('Altitude', 1)
    v = Var('Velocity', 0)
    t = Var('Time', 0.1)
    dt = Var('dt', 0.1)
    z_values, t_values = [], []
    T_z = Var('Temperature',300)
    P_z = Var('Pressure',101325)
    earth_grav =  d(G.value*MoE.value)
    earth_grav = round(earth_grav,2)
    fdrag0 = Cd_z.value * rho_z.value * v.value**2 * A.value * d(0.5)
    Fdrag = Var('Drag force', fdrag0)
    mflowrate = Thrust_z.value/(g_z.value*Isp.value)
    Mass_flow_rate = Var('Mass flow rate', mflowrate)
    while t.value <= Isp.value:
        if z.value < d(0): #Crash Condition
            print('Crashed!') #Change to a Tkinter output 
            break
        if WetM.value <= DryM.value: #If current mass is less than/equal to dry mass, no more propellant is available
            print('No more fuel') #Change to a Tkinter output 
            break
        if int(g_z.value) == 0 or int(g_z.value) == 1:
            g_z.value = d(1.0)
        else:
            g_z.value = g_getter(z.value,earth_grav,g_z.value)
        WetM.value += Mass_flow_rate.value #Mass update from fuel use
        WetM.value = round(WetM.value,3)
        rho_z.value, T_z.value, P_z.value = density(z.value) #Rho, temp, pressure update
        Cd_z.value = drag_coefficient(v.value, T_z.value, Cd_z.value, Cd_0.value) #Drag coefficient
        Thrust_z.value = Thrust_0.value/WetM.value
        v_sq = v.value**2
        A.value = round(A.value,2)
        Fdrag.value = rho_z.value*v_sq*Cd_z.value*A.value*d(0.5)
        if v.value < 0:
            Fdrag.value *= -1
        v.value += (Thrust_z.value - Fdrag.value - g_z.value)
        z.value += v.value*dt.value
        t.value += dt.value
        z_km = z.value / d(1000)
        z_values.append(z_km)
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

def example():
    pass

def save_file():
    pass
    
#Create tkinter window
window = tk.Tk()
window.columnconfigure(2,weight=2) #Tells frame to np.expand to fill extra space if window is resized and where to np.expand to.
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
quitButton = Button(inputSection, text='Quit', command=quit).grid(row=4,column=5)
getVariables = Button(inputSection, text='Calculate', command=get_values).grid(row=0,column=5)
plotButton = Button(inputSection, text='Plot', command=euler_cromer)
presetButton = Button(inputSection, text='Example Plot', command=example).grid(row=2,column=5)
saveButton = Button(inputSection, text='Save Your Variables', command=save_file).grid(row=3,column=5)

#Error Thrower
errorLabel = Label(inputSection, text='')
errorLabel.grid(row=0, column=7)

#All entries
TempEntry = Entry(inputSection) #Enter temperature
TempEntry.grid(row=0,column=1)
Label(inputSection, text='Temp:').grid(row=0,column=0)
PressureEntry = Entry(inputSection) #Enter Pressure
PressureEntry.grid(row=1,column=1)
Label(inputSection, text='Pressure (Pa):').grid(row=1,column=0)
ThrustEntry = Entry(inputSection) #Enter Rocket Specs.
ThrustEntry.grid(row=2,column=1)
Label(inputSection, text='Thrust (N):').grid(row=2,column=0)
DragCoEntry = Entry(inputSection) #Enter Drag Coefficient
DragCoEntry.grid(row=3,column=1)
Label(inputSection, text='Drag Co:').grid(row=3,column=0)
REntry = Entry(inputSection) #Enter Radius
REntry.grid(row=4,column=1)
Label(inputSection, text='Radius (m):').grid(row=4,column=0)
WetMassEntry = Entry(inputSection) #Enter Wet Mass
WetMassEntry.grid(row=5,column=1)
Label(inputSection, text='Wet Mass (kg):').grid(row=5,column=0)
DryMassEntry = Entry(inputSection) #Enter Dry Mass
DryMassEntry.grid(row=6,column=1)
Label(inputSection, text='Dry Mass (kg):').grid(row=6,column=0)
IspEntry = Entry(inputSection) #Enter Isp
IspEntry.grid(row=7,column=1)
Label(inputSection, text='Isp (s):').grid(row=7,column=0)

window.mainloop()
#https://pages.vassar.edu/magnes/2019/05/12/computational-simulation-of-rocket-trajectories/