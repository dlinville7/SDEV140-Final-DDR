#Title: Digital Dice Roller (DDR)
#Author: Dillon Linville
#Goal: To create a GUI program that allows for a user to roll dice to complete a Warhammer 40k combat sequence.


#Import Modules
from tkinter import *           #Provides base GUI functionality
from tkinter import messagebox  #Message boxes for error handling
from tkinter import ttk         #For Comboboxes
from random import *            #Used for dice rolls
import os                       #Allows for file pathing

#Create Window Frame
MainWindow = Tk()
MainWindow.geometry("410x410") #fixed size
MainWindow.title("Digital Dice Roller")
MainWindow.resizable(False,False) #no resize allowed

#Obtain PWD and create paths for DDR images.
pwd = os.path.dirname(os.path.abspath(__file__)) #pwd for file operations
Img1 = os.path.join(pwd,"DDR_Img1.png") #file path of Img1
Img2 = os.path.join(pwd,"DDR_Img2.png") #File path of Img2


#Create MainWindow Title Image 
try: #use try/except for instance with no picture
    TitleImg = PhotoImage(file=Img1) #use tk PhotoImage function
    TitleBox = Label(MainWindow,image= TitleImg) #attach the TitleImg to a label
    TitleBox.grid(row=0,column=0,columnspan=10) #specify grid parameters

except TclError: #Create Inner Window Title when TitleImg not found
    messagebox.showerror(title="Error",message="Error! Title image file not found. Using text instead. ")
    TopTitle = Label(MainWindow,text="Digital Dice Roller. ")
    TopTitle.grid(row=0,column=0,columnspan=6,pady=10)

#Create and Insert 2nd Image. 
try: #use try/except to error handle missing image. 
    SideImg2 = PhotoImage(file=Img2)
    Img2Box = Label(MainWindow,image= SideImg2)
    Img2Box.grid(row=1,column=2,rowspan=6)

except TclError: #Create Inner Window Title when img not found
    messagebox.showerror(title="Error",message="Error! Side image file not found. Using text instead. ")
    SideTitle = Label(MainWindow,text="*cool figure.*")
    SideTitle.grid(row=1,column=2,rowspan=6)


#Create Labels for Entry Boxes
ShotsLabel = Label(MainWindow, text="Number of Shots: ") #Define label
ShotsLabel.grid(row=1,column=0,pady=2) #Define Label grid values

BSLabel = Label(MainWindow, text="Ballistic Skill: ")
BSLabel.grid(row=2,column=0,pady=2) 

StrengthLabel = Label(MainWindow, text="Attack Strength: ")
StrengthLabel.grid(row=3,column=0,pady=2)

ToughnessLabel = Label(MainWindow, text="Target's Toughness: ")
ToughnessLabel.grid(row=4,column=0,pady=2)

APLabel = Label(MainWindow, text="Armor Penetration: ")
APLabel.grid(row=5,column=0,pady=2)

EnemySaveLabel = Label(MainWindow, text="Enemy's Save: ")
EnemySaveLabel.grid(row=6,column=0,pady=2)

DmgLabel = Label(MainWindow, text="Damage: ")
DmgLabel.grid(row=7,column=0,pady=2)

#Define Tuples for comboboxes
#Most options have a easily defined list of all possible values (Within the game logic.)
ShotsOption = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"]
BSOption = ["+2","+3","+4","+5","+6"]
StrengthOption = ["2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18"]
ToughnessOption = ["2","3","4","5","6","7","8","9"]
APOption = ["0","-1","-2","-3","-4","-5","-6","-7"]
EnemySaveOption = ["+2","+3","+4","+5","+6"] 
DamageOption = ["1","2","3","4","5","6","7","8","9","10","11","12"]

#Create Combo Boxes to allow user input
ShotsCombo = ttk.Combobox(MainWindow, values=ShotsOption) #allows for user input option
ShotsCombo.grid(row=1,column=1,pady=2) #Define combobox grid values
ShotsCombo.current(9) #default value

BSCombo = ttk.Combobox(MainWindow, values=BSOption,state="readonly")
BSCombo.grid(row=2,column=1,pady=2)
BSCombo.current(1)

StrengthCombo = ttk.Combobox(MainWindow,values=StrengthOption,state="readonly")
StrengthCombo.grid(row=3,column=1,pady=2)
StrengthCombo.current(4)

ToughnessCombo = ttk.Combobox(MainWindow,values=ToughnessOption,state="readonly")
ToughnessCombo.grid(row=4,column=1,pady=2)
ToughnessCombo.current(3)

APCombo = ttk.Combobox(MainWindow, values=APOption,state="readonly")
APCombo.grid(row=5,column=1,pady=2)
APCombo.current(1)

SaveCombo = ttk.Combobox(MainWindow, values=EnemySaveOption, state="readonly")
SaveCombo.grid(row=6,column=1,pady=2)
SaveCombo.current(2)

DmgCombo = ttk.Combobox(MainWindow, values=DamageOption) #allows for user input option
DmgCombo.grid(row=7,column=1,pady=2)
DmgCombo.current(1)


#Output Display
#Displays calculation results to GUI
LowerTitle = Label(MainWindow, text="Results: ")
LowerTitle.grid(row=9,column=0,columnspan=3)

HitsLabel = Label(MainWindow,text="Number of Hits: ")
HitsLabel.grid(row=10,column=0,columnspan=3)

WoundsLabel = Label(MainWindow, text="Number of Wounds: ")
WoundsLabel.grid(row=12,column=0,columnspan=3)

DmgDealtLabel = Label(MainWindow, text="Amount of Damage: ")
DmgDealtLabel.grid(row=14,column=0,columnspan=3) 


#Main Calculation Function 
def Calculate():

    #Define Function Variables
    Counter = 0 #Multi-use counter for while loops

    ShotList = [] #Shot rolls
    HitList = [] #Confirmed Hits
    WoundList = [] #Unconfirmed Wound rolls
    ConfWoundList = [] #Confirmed Wound Rolls
    SaveList = [] #Non-saved, Confirmed Wound Rolls

    NumWounds = 0 #Number of wounds / length of ConfWoundList
    NumHits = 0 #Number of hits / Length of HitList
    WoundChance = 0 #Calulated via Strength vs. Toughness matrix
    DmgDealt = 0 #Actual Dmg Dealt
    SaveCounter = 0 #Counter to determine number of sucessful save


    #Pull values from the entry boxes, w/ error handling
    try: #try to get int value from combobox
        Shots = int(ShotsCombo.get())
    except ValueError: #If ValueError, empty string or non-int, provide error message box   
        messagebox.showerror(title="Error",message="Error! For Number of Shots enter an Integer. ") 
    
    try:
        BalSkill = int(BSCombo.get()) 
    except ValueError:
        messagebox.showerror(title="Error",message="Error! For Ballistic Skill enter an Integer between 1 & 6. ") 
    
    try:
        Strength = int(StrengthCombo.get())
    except ValueError: 
        messagebox.showerror(title="Error",message="Error! For Strength enter an Integer. ")
    
    try:
        Toughness = int(ToughnessCombo.get())
    except ValueError:
        messagebox.showerror(title="Error",message="Error! For Toughness enter an Integer. ")

    try:
        Ap = int(APCombo.get())
    except ValueError:
        messagebox.showerror(title="Error",message="Error! For Armor Penetration enter an Integer. ")
    
    try:
        Dmg = int(DmgCombo.get())
    except ValueError:
        messagebox.showerror(title="Error",message="Error! For Damage enter an Integer. ")

    try: 
        EnemySave = int(SaveCombo.get())
    except ValueError:
        messagebox.showerror(title="Error",message="Error! For Enemy Save enter an Integer. ")
    
    #Create the rolls for ShotList
    while Counter < Shots:
        holder = randrange(1,7) #generate D6 roll
        ShotList.append(holder) #add to list
        Counter += 1 #increment counter
    Counter = 0 #reset Counter
    print("ShotList: ",ShotList) #tracing print statement
   
    print("Ballistic Skill: ",BalSkill) #tracing print statement

    #Based on BS determine if rolls in Shotlist are hits.
    for x in ShotList: #for each previously rolled die
        if x >= BalSkill: #test roll against Ballistic skill
            HitList.append(x) #Append rolls to new HitList if they hit
    print("HitList: ",HitList) #tracing print statement

    NumHits = len(HitList) #Determine total number of sucessful hits
    HitsLabel.config(text=f"Number of Hits: {NumHits} ") #Display number of hits
    print("Number of Hits: ",NumHits) #tracing print statement
    
    #Matrix to determine WoundChance, based on Toughness vs. Strength
    if (Strength / 2) >= Toughness: #if Strength Twice(or more) than Toughness
        WoundChance = 2 #Wound on 2+
    elif Strength > Toughness: #If Str is Greater than Tough
        WoundChance = 3 #Wound on 3+
    elif Strength == Toughness: #If Str equals Toughness
        WoundChance = 4 #Wound on 4+
    elif Strength < (Toughness / 2): #If Str is Half (or less) than Toughness
        WoundChance = 6 #Wound on 6+
    elif Strength < Toughness: #If Str is less (but not less than half) of Toughness
        WoundChance = 5 #Wound on 5+

    print("WoundChance: ",WoundChance) #tracing print statement
    
    #Generate the list of wound rolls
    while Counter < NumHits: 
        holder = randrange(1,7) #new die roll for wounds
        WoundList.append(holder)
        Counter += 1
    Counter = 0 #reset counter
    print("WoundList: ",WoundList) #tracing print statement

    #Generate the list of confirmed wound, test if they are >= to WoundChance
    for x in WoundList: 
        if x >= WoundChance: 
            ConfWoundList.append(x) 
    print("ConfWoundList: ",ConfWoundList) #tracing print statement

    #Determine number of confirmed Wounds
    NumWounds = len(ConfWoundList) 
    print("NumWound: ",NumWounds) #tracing print statement
    
    #Roll enemy saving throws, one for each Confirmed Wound
    while Counter < NumWounds:
        holder = randrange(1,7)
        SaveList.append(holder)
        Counter += 1
    Counter = 0 #Reset Counter
    print("SaveList: ",SaveList) #tracing print statement

    print("Enemy Save: ",EnemySave) #tracing print statement
    print("AP: ",Ap) #tracing print statement

    #Determine if Saving throws are succesful
    for x in SaveList:
        if (x + Ap) >= EnemySave: #Rolled save (x) plus (negative)Ap value, must be greater than/equal to EnemySave to pass
            SaveCounter += 1 #If pass, add 1 to the SaveCounter
    print("Save Counter: ",SaveCounter) #tracing print statement
    
    #Determine the number of confirmed, un-saved wounds 
    NumWounds -= SaveCounter 
    WoundsLabel.config(text=f"Number of Wounds: {NumWounds}") #Display this value to the user

    #Multply the number of confirmed, un-saved wounds by their Dmg value
    DmgDealt = NumWounds * Dmg #Calculate total Damage Dealt
    DmgDealtLabel.config(text=f"Amount of Damage: {DmgDealt}") #Display this value to the user

#Clear Combobox options and results output Function
def ClearCombos(): 
    #Set combobox entries to an empty string
    ShotsCombo.set('')
    BSCombo.set('')
    StrengthCombo.set('')
    ToughnessCombo.set('')
    APCombo.set('')
    SaveCombo.set('')
    DmgCombo.set('') 
    #reset results outputs
    HitsLabel.config(text=f"Number of Hits: ")
    WoundsLabel.config(text=f"Number of Wounds: ")
    DmgDealtLabel.config(text=f"Amount of Damage: ")

#Open Instructions Window Function
def OpenIns():
    InsTxtPath = os.path.join(pwd,"DDR_Instructions.txt") #create path to instructions txt file
    InsTxt = open(InsTxtPath, "r") #open the txt file in read mode

    InsWindow = Toplevel(MainWindow) #Create new window for instructions
    InsWindow.title("DDR Instructions") 
    InsWindow.geometry ("600x500")
    InsWindow.resizable(False,False)
    
    #Create a Label to hold the contents of the txt file
    InsTitle = Label(InsWindow, text="Instructions")
    InsTitle.grid(row=0,column=0) #set geometry 
    
    #Update InsTitle Label with the contents of the Txt file
    InsTitle.config(text=InsTxt.read())


#Buttons
CalcButton = Button(MainWindow, text="Calculate",command=Calculate) #Calculation button
CalcButton.grid(row=8,column=0,pady=5)

ClearButton = Button(MainWindow,text="Clear", command=ClearCombos) #Clear entries button
ClearButton.grid(row=8,column=1)

InsButton = Button(MainWindow,text="Instructions",command=OpenIns) #Open Instructions Window Button
InsButton.grid(row=8,column=2)

#Mainloop to run window
MainWindow.mainloop()

