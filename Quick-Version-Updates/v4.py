import pyforest
import tkinter as tk #GUI Package
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk) #Imported in order to allow matplotlib graphs to be interacted with

def set_window():
    window = tk.Tk()
    window.columnconfigure(2,weight=2) #Tells frame to expand to fill extra space if window is resized and where to expand to.
    window.rowconfigure(0, weight=1)
    plotFrame, inputSection = Frame(window), Frame(window)
    plotFrame.grid(column=1,row=0)
    inputSection.grid(column=2,row=0)
    return window, inputSection, plotFrame

def integrate_plot():
    global canvas
    fig = plt.figure(figsize=(7,9)) #Defines the matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master=plotFrame) #Create tkinter canvas holding the matplotlib Figure
    canvas.get_tk_widget().grid(row=0,column=0) #places canvas on plotFrame
    toolbarFrame = tk.Frame(master=plotFrame)
    toolbarFrame.grid(row=1,column=0)
    toolbar = NavigationToolbar2Tk(canvas,toolbarFrame)

def quit(): window.destroy, window.quit()
    
def add_plot_values():
    x = [i**2 for i in range(0,10)]
    plt.plot(x)
    plt.grid(True)
    ax = plt.gca()
    ax.spines['top'].set_color('none')
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    canvas.draw()

def test_input(entry,error_string,errPhrase): #Assures Entry boxes are filled
    entered = str(entry.get())
    if entered.isnumeric() is False:
        error_string += errPhrase
        var = 1.0
    else:
        var = float(entry.get())
    return var, error_string

def append_faster(ls, *to_append):
    for i in to_append:
        ls.append(float(i))
    return ls
    
def temp_get(T0, tUnit, error_string):
    if tUnit == 'K': 
        error_string += '\nThank you for using kelvin'
    elif tUnit == 'C': 
        T0 += 273.15 #Initial temperature in kelvin
    elif tUnit == 'F':
        T0 = ((T0 - 32) * 5/9) + 273.15 #Initial temperature in kelvin
        error_string += '\nPlease consider using celsius or kelvin next time'
    else:
        error_string += '\nA unit of temperature (K,C,F)'
    return T0, error_string
    
def values():
    global variables
    #Gravitational constant, Gravitational acceleration, Mass of earth, molar mass of dry air, molar gass constant
    variables = [6.67e-11, 9.81,5.972e24, 0.028964,8.3145]
    error_string = ''
    tUnit = str(tUnitSelection.get()).upper()
    T0, error_string = test_input(TempEntry,error_string,'\nThe temperature') #Returns T0 if it exists
    T0, error_string = temp_get(T0, tUnit, error_string) #Update T0 for the proper unit of temperature
    errors_to_throw = ['\nThe pressure at the pad','\nThe rocket\'s thrust','\nThe drag coefficient','\nThe rocket\'s radius','\nThe rocket\'s wet mass','\nThe rocket\'s dry mass','\nThe rocket\'s Isp']
    for i in range(len(entries) - 3):
        var, error_string = test_input(entries[i],error_string,errors_to_throw[i])
        variables.append(float(var))
    passableErrors = ['','\nPlease consider using celsius or kelvin next time','\nThank you for using kelvin']
    errorLabel.config(text=error_string)
    if error_string not in passableErrors:
       error_string = 'Please Enter:' + error_string
    else:
        rho0 = (variables[3]*variables[5])/(variables[4]*T0) #Air density --> sea level
        area = np.pi*(variables[3]**2)
        mflowrate = variables[6]/variables[1]*variables[11]
        append_faster(variables,T0,rho0,area,mflowrate)
        plotButton.grid(row=4,column=1)
        return variables

def drag(): #http://www.braeunig.us/space/atmmodel.htm#equations
    #T_z = variables[12] - 
    #P_z = P0(T0/T_z)**((g0*M)/(R*L))
    #rho_z = (variables[3]*T_z)/(variables[4]*P_z)
    #Fdrag = (rho_z*(v**2)*Cd*A)/2
    #return Fdrag
    pass
    
def euler_cromer():
    z, v, t = 1, 0, 0.1 #Initial altitude (m), Initial velocity (m/s), Initial time
    dt = 0.1
    total_mass = variables[9] + variables[10]
    while True: #t0 --> t max:
        m_t = m0 - (variables[15]*dt)
        g_z = (variables[0]*variables[2])/((z+6371000)**2)
        Fdrag = drag()
        
        #call: density func, wave drag func. Calculate: thrust, drag
        #If drag vector condition
        #euler-cromer: v = v + (thrust - drag - g)*dt
                       #z = z+ v*dt
        #save matrix values for v,z,m,g,thrust,drag,rho
        #save end time
        #If crash
        #If empty
    #Plot z vs. t, v vs. t
    #Plot thrust, drag force, and g vs. t (Optional)

window, inputSection, plotFrame = set_window()
integrate_plot()
quitButton = Button(inputSection, text='Quit', command=quit).grid(row=6,column=1)

def __prompts__(Prompted,r,c):
    self = Label(inputSection,text=Prompted)
    self.grid(row=r,column=c)
    
Prompted = ['Temp: ','Pressure (Pa): ','Thrust (N): ','Drag Coefficient: ','Radius (m): ','Dry Mass (kg):','Wet Mass (kg):','Isp (s):']
rows, cols = [1,2,0,1,2,3,4,5], [0,0,3,3,3,3,3,3]
for i in range(len(Prompted)):
    __prompts__(Prompted[i],rows[i],cols[i])

#Error Throwers
errorLabel = Label(inputSection, text='')

#Select Unit of temperature
tUnits = ['K','C','F']
tUnitSelection = ttk.Combobox(inputSection,values=tUnits)
tUnitSelection.set('Temp. Unit')

TempEntry = Entry(inputSection) #Enter temperature
PressureEntry = Entry(inputSection) #Enter Pressure
ThrustEntry = Entry(inputSection) #Enter Rocket Specs.
DragCoEntry = Entry(inputSection) #Enter Drag Coefficient
REntry = Entry(inputSection) #Enter Radius
WetMassEntry = Entry(inputSection) #Enter Wet Mass
DryMassEntry = Entry(inputSection) #Enter Dry Mass
IspEntry = Entry(inputSection) #Enter Isp

def __grid__(self,r,c):
    self.grid(row=r,column=c)
    
entries = [PressureEntry,ThrustEntry,DragCoEntry,REntry,WetMassEntry,DryMassEntry,IspEntry,errorLabel,tUnitSelection,TempEntry]
Rows, Cols = [2,0,1,2,3,4,5,3,0,1], [1,4,4,4,4,4,4,1,1,1]
for i in range(len(entries)):
    __grid__(entries[i], Rows[i], Cols[i])

getVariables = Button(inputSection, text='Calculate', command=values).grid(row=0,column=5)
plotButton = Button(inputSection, text='Plot', command=add_plot_values) #Adds values to the plot
window.mainloop()
#https://pages.vassar.edu/magnes/2019/05/12/computational-simulation-of-rocket-trajectories/
