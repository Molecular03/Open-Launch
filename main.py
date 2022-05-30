import pyforest
import tkinter as tk #GUI Package
from decimal import Decimal as d
import numpy as np
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk) #Imported in order to allow matplotlib graphs to be interacted with
import atmos_model

class Var:
#Assures all variables are set as decimals when passed through d(*variable name*)
	def __init__(self,name,num):
	    self.name = name
	    self.value = float(d(num))
	    
	def print_value(self):
	    print(self.value)
    
def quit():
#Destroys and quits tkinter window
    window.destroy
    window.quit()

def validate_input(entry, error_string, errPhrase):
#Assures variable is entered
    var = entry.get()
    if var:
        var = float(var)
    else:
        var = 1.0
        error_string += errPhrase
    return var, error_string
    
def get_values():
#Receives variables from the entries
    global T_z, P_z, Thrust_z, Cd_z, Radius, WetM, DryM, WetM, Isp, area, Thrust_0, Cd_0, error_string, Theta
    error_string = ''
    T_z = Var('Temperature',300)
    P_z = Var('Pressure',101325)
    thrust0, error_string = validate_input(ThrustEntry,error_string,'\nThrust')
    Thrust_z = Var('Thrust',thrust0)
    Thrust_0 = Var('Initial Thrust', thrust0)
    Cd0, error_string = validate_input(DragCoEntry,error_string,'\nDrag Coefficient')
    Cd_0 = Var('Initial Cd', Cd0)
    r, error_string = validate_input(REntry,error_string,'\nRadius')
    Radius = Var('Radius', r)
    WetM0, error_string = validate_input(WetMassEntry,error_string,'\nWet mass')
    WetM = Var('Wet Mass', WetM0)
    dryM, error_string = validate_input(DryMassEntry,error_string,'\nDry mass')
    DryM = Var('Dry Mass', dryM)
    isp, error_string = validate_input(IspEntry,error_string,'\nIsp')
    Isp = Var('Isp', isp)
    area = np.pi*(r**2)
    theta, error_string = validate_input(ThetaEntry,error_string,'\tTheta')
    Theta = Var('Theta', theta)
    if error_string != '':
        error_string = 'Please Enter:' + error_string
        errorLabel.config(text=error_string)
    else:
        errorLabel.config(text=error_string)
        plotButton.grid(row=1,column=5)
        
def euler_cromer():
    global z,v,t, status_string
    z = 0.0001
    t = 0.0
    m_dot = Thrust_z.value/(9.81*Isp.value)
    v = 0.0
    z_values, t_values, x_values, y_values = [],[],[],[]
    x_pos = 0.0
    y_pos = 0.0
    while True:
#Calls rust, returns rocket's values
        values = atmos_model.calc_sim(z,WetM.value,m_dot,v,Cd_0.value,Thrust_z.value,area,Theta.value,x_pos,y_pos,t)
        z = values[0]
        WetM.value = values[1]
        v = values[2]
        Thrust_z.value = values[3]
        x_pos, y_pos = values[4], values[5]
        x_values.append(x_pos)
        y_values.append(y_pos)
        z_values.append(z)
        t += 0.1
        t_values.append(t)
        if t >= Isp.value:
            #If the engine can no longer burn, the function stops.
            status_string = 'STATUS: \nENGINE BURN COMPLETE\nSUCCESS: TRUE'
            errorLabel.config(text=status_string)
            break
        elif z < d(0): #Crash Condition
            status_string = 'STATUS: CRASHED!\nSUCCESS: FALSE'
            errorLabel.config(text=status_string)
            break
        elif WetM.value <= DryM.value: #If current mass is less than/equal to dry mass, no more propellant is available
            status_string = 'STATUS: FUEL RESERVE DEPLETED!\nSUCCESS: FALSE' 
            errorLabel.config(text=status_string)
            break
    plt.plot(t_values,z_values,'-o')
    plt.plot(x_values,y_values,z_values,'-o')
    plt.grid(True)
    plt.title('3D Rocket Simulation')
    plt.ylabel('Y (KM)')
    plt.xlabel('X (KM)')
    ax = plt.gca()
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    canvas.draw()
    window.update()

def save_file():
#Saves current variables to a file:
    f = open('user_variables.txt','a')
    try:
        f.write(f'INITIAL THRUST (N): {Thrust_0.value} \nFINAL THRUST (N): {Thrust_z.value} \nINITIAL DRAG COEFFICIENT: {Cd_0.value} \nRADIUS (m): {Radius.value} \nWET MASS (Kg): {WetM.value} \nDRY MASS (Kg): {DryM.value} \nISP (s): {Isp.value} \nFINAL Z (m): {z} \nFINAL VELOCITY (m/s): {v} \nEND TIME: {t} \nMISSION: {status_string} \n\n')
        f.close
        saved_status = 'SAVED!'
        errorLabel.config(text=saved_status)
    except:
        saved_status = 'ERROR WHILE SAVING\nPLEASE TRY INPUTTING VARIABLES IF YOU HAVE NOT DONE SO'
        errorLabel.config(text=saved_status)

def help():
#Displays variable explanations:
    help_string = ('THRUST:\nEngine\'s force in Newtons\n\nDRAG CO:\nThe Drag Coefficient is used in the\ndrag equation, it is typically around 0.75 for rockets\n\nRADIUS:\nThe rocket\'s radius in meters\n\nWET MASS:\nTotal mass of the rocket, when fully fueled.\nMeasured in Kilograms.\n\nDRY MASS:\nMass of the rocket when fuel is completely expended\nEx. of leftover mass: Payload, Structural, etc.\nMeasured in Kilograms.\n\nISP (SPECIFIC IMPULSE):\nIn the most basic sense, the length of time that a \nrocket\'s engine can burn for or, it\'s efficiency.\nMeasured in seconds.')
    errorLabel.config(text=help_string)

#Create tkinter window
window = tk.Tk()
window.title('Open-Launch')
window.columnconfigure(2,weight=2) #Tells frame to np.expand to fill extra space if window is resized and where to np.expand to.
window.rowconfigure(0, weight=1)
plotFrame = Frame(window) #Where the plot will stay
plotFrame.grid(column=1,row=0)
inputSection = Frame(window) #Where the user will input data
inputSection.grid(column=2,row=0)

#Integrate Matplotlib 
fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(projection='3d')
canvas = FigureCanvasTkAgg(fig, master=plotFrame) #Create tkinter canvas that holds the matplotlib Figure
canvas.get_tk_widget().grid(row=0,column=0) #Places canvas on plotFrame
toolbarFrame = tk.Frame(master=plotFrame)
toolbarFrame.grid(row=1,column=0)
toolbar = NavigationToolbar2Tk(canvas,toolbarFrame)

#Basic Buttons
quitButton = Button(inputSection, text='Quit', command=quit).grid(row=4,column=5)
getVariables = Button(inputSection, text='Calculate', command=get_values).grid(row=0,column=5)
plotButton = Button(inputSection, text='Plot', command=euler_cromer)
saveButton = Button(inputSection, text='Save Your Variables', command=save_file).grid(row=2,column=5)
helpButton = Button(inputSection, text='What are these variables?', command=help).grid(row=3,column=5)

#Error Thrower
errorLabel = Label(inputSection, text='')
errorLabel.grid(row=0, column=7)

#All entries
ThrustEntry = Entry(inputSection) #Enter Rocket Specs.
ThrustEntry.grid(row=0,column=1)
Label(inputSection, text='Thrust (N):').grid(row=0,column=0)
DragCoEntry = Entry(inputSection) #Enter Drag Coefficient
DragCoEntry.grid(row=1,column=1)
Label(inputSection, text='Drag Co:').grid(row=1,column=0)
REntry = Entry(inputSection) #Enter Radius
REntry.grid(row=2,column=1)
Label(inputSection, text='Radius (m):').grid(row=2,column=0)
WetMassEntry = Entry(inputSection) #Enter Wet Mass
WetMassEntry.grid(row=3,column=1)
Label(inputSection, text='Wet Mass (kg):').grid(row=3,column=0)
DryMassEntry = Entry(inputSection) #Enter Dry Mass
DryMassEntry.grid(row=4,column=1)
Label(inputSection, text='Dry Mass (kg):').grid(row=4,column=0)
IspEntry = Entry(inputSection) #Enter Isp
IspEntry.grid(row=5,column=1)
Label(inputSection, text='Isp (s):').grid(row=5,column=0)
Label(inputSection, text='Theta (DEG):').grid(row=6,column=0)
ThetaEntry = Entry(inputSection)
ThetaEntry.grid(row=6,column=1)
window.mainloop()
#Physics Ressource: https://pages.vassar.edu/magnes/2019/05/12/computational-simulation-of-rocket-trajectories/





