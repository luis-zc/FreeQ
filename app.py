import tkinter as tk
from tkinter import *
from tkinter import messagebox
import pyautogui
import time
import discord
from dhooks import Webhook
import json
import os

if not os.path.exists("./data.json"):
    data = {'webHookUrl': 'no webhook found', 'userID': 'no userID found'}
    with open("data.json", "w") as f:
        json.dump(data,f)


# ----------------------------------------------------------------------
# Resource variables
# ----------------------------------------------------------------------
thumbURL = "https://cdn.discordapp.com/attachments/953990432218566676/953990574850068490/molangow.png"

# ----------------------------------------------------------------------
# Main Window setup
# ----------------------------------------------------------------------

root = tk.Tk()
root.title("Free-Q v1.0")
root.iconbitmap('molangow.ico')
#root.resizable(False, False) 
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry(f'{int(screen_width/6)}x{int(screen_height/6)}')
#root['bg'] = '#141414'

# ----------------------------------------------------------------------
# Generic Button def
# ----------------------------------------------------------------------

def bttn(text,cmd, window):
    mybutton=Button(window,text = text,command=cmd)
    mybutton.pack()




# ----------------------------------------------------------------------
# Settings
# ----------------------------------------------------------------------
global top
top = None


def initSettings(top):
    top.title("Free-Q v1.0 Settings")
    top.iconbitmap('molangow.ico')
    top.resizable(False, False)
    top.geometry(f'{int(screen_width/2.5)}x{int(screen_height/2.5)}')
    #top['bg'] = '#141414'
    def closeSettings():
        global top  
        top.destroy()
        top = None
    top.protocol('WM_DELETE_WINDOW', closeSettings)

    label1 = Label(top, text='Webhook url:', font=('Arial', 12))
    label1.grid(row=0,column=0,padx=5,pady=20)


    textbox1=Entry(top,width=50, font=('Arial', 12))
    textbox1.grid(row=0,column=1)

    label1 = Label(top, text='Webhook url:', font=('Arial', 12))
    label1.grid(row=0,column=0,padx=5,pady=20)

    label2 = Label(top, text='UserID:', font=('Arial', 12))
    label2.grid(row=1,column=0,padx=5,pady=20)

    textbox2=Entry(top,width=50, font=('Arial', 12))
    textbox2.grid(row=1,column=1)

    textbox = Text(top, width=70, height=10)
    textbox.place(relx=0.5, rely= 0.6, anchor = 'center')
    textbox.insert(INSERT, "Insert discord webhook url and userID\n(Enable developer setting in discord to access userIDs by\nrightclicking on profiles).\n")
    textbox.insert(INSERT, "The information is saved after closing the program.\n")
    for i in range(5):
        textbox.insert(INSERT,"\n")
    textbox.insert(INSERT, "v1.0 - https://github.com/luis-zc/FreeQ")

    def saveSettings():
        with open("data.json", "r") as f:
            data = json.load(f)
        if not textbox1.get() == "":
            data["webHookUrl"] = textbox1.get()
        if not textbox2.get() == "":
            data["userID"] = textbox2.get()
        with open("data.json", "w") as f:
            json.dump(data, f)
        
        if textbox1.get() == "" and textbox2.get() == "":
            messagebox.showerror(title="Error", message="Userdata was not overwritten.")
        else:
            messagebox.showinfo(title="Success", message="userdata was successfully updated")

    saveSettingsButton = Button(top, text="S A V E", command = saveSettings)
    saveSettingsButton.place(relx=0.5, rely= 0.9, anchor = 'center')
    


def openSettings():
    global top
    if top == None:
        top = Toplevel()
        initSettings(top)
    else:
        top.focus_set()

settingsButton = Button(root, text="Settings", command=openSettings)
settingsButton.place(relx=0.02, rely= 0.02, anchor = 'nw')


# ----------------------------------------------------------------------
# Global Variables
# ----------------------------------------------------------------------

# starting point of entering the queue
global startTime
startTime = 0

# Boolean if we are currently looking for a queue
global running
running = 0

# ----------------------------------------------------------------------
# Functions
# ----------------------------------------------------------------------

def sendNotification(mode):
    # 0 - Queue popped without confirming
    # 1 - Comp Game confirmation
    # 2 - QP Game confirmation
    endTime = time.time()
    seconds = int((endTime - startTime)) 
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    qTime = f'{h:d}:{m:02d}:{s:02d}'

    match mode:
        case 0:
            gamemode = "unspecified" 
        case 1:
           gamemode = "Competitive" 
        case 2:
            gamemode = "Quickplay" 
        case _:
            return

    with open("data.json", "r") as f:
        data = json.load(f)
    

    hook = Webhook(data["webHookUrl"])

    e = discord.Embed(title="G A M E   F O U N D", description=f"Hey <@!"+ data["userID"] + ">, you found a game!")
    e.add_field(name="Gamemode:", value=f"{gamemode}")
    e.add_field(name="Queue Time:", value=f"{qTime}")
    e.set_thumbnail(url=f"{thumbURL}")    
    hook.send(f"<@" + data["userID"] + ">")
    hook.send(embed = e)

def test():
    with open("data.json", "r") as f:
        data = json.load(f)
    print(data["userID"])

def stopButton():
    # Stops Tracking and additionally resets title to default
    stopTracking()
    title.config(text = "Free-Q v1.0")

def stopTracking():
    global running
    running = 0

def startTracking():
    global running
    running = 1
    track(0)

def checkPixelColors(x, y, threshold):
    InQColors = [ 95, 105, 130]
    CompColors = [ 196, 64, 255]
    QPColors = [ 84, 153, 208]

    rvalue = pyautogui.pixel(x,y)[0]
    gvalue = pyautogui.pixel(x,y)[1]
    bvalue = pyautogui.pixel(x,y)[2]
    # Debug
    # print("R:" + str(rvalue) + " G:" + str(gvalue) + " B:" + str(bvalue))

    if rvalue <= InQColors[0]+threshold and rvalue >= InQColors[0]-threshold and gvalue <= InQColors[1]+threshold and gvalue >= InQColors[1]-threshold and bvalue <= InQColors[2]+threshold and bvalue >= InQColors[2]-threshold:
        return 1
    elif rvalue <= CompColors[0]+threshold and rvalue >= CompColors[0]-threshold and gvalue <= CompColors[1]+threshold and gvalue >= CompColors[1]-threshold and bvalue <= CompColors[2]+threshold and bvalue >= CompColors[2]-threshold:
        return 2
    elif rvalue <= QPColors[0]+threshold and rvalue >= QPColors[0]-threshold and gvalue <= QPColors[1]+threshold and gvalue >= QPColors[1]-threshold and bvalue <= QPColors[2]+threshold and bvalue >= QPColors[2]-threshold:
        return 3
    else:
        return 0
    
    

def track(recVar):
    if not running:
        return     
    windowX = 1400
    windowY = 70
    isInQueue = recVar

    result = checkPixelColors(windowX,windowY,10)
    #print(str(result))
    match result:
        case 0:
            if not isInQueue:
                title.config(text = "No Queue detected")
            else: 
                sendNotification(0)
                title.config(text = "unspecified Game found!")
                stopTracking()
                title.after(5000, stopButton)

        case 1:
            title.config(text = "Currently in Queue")
            if isInQueue:
                pass
            else:
                isInQueue = 1
                global startTime
                startTime = time.time()
        case 2:
            sendNotification(1)
            title.config(text = "Comp Game found!")
            stopTracking()
            title.after(5000, stopButton)
        case 3:
            sendNotification(2)
            title.config(text = "QP Game found!")
            stopTracking()
            title.after(5000, stopButton)
            
    title.after(100, lambda: track(isInQueue))

 
# ----------------------------------------------------------------------
# Title
# ----------------------------------------------------------------------
title = Label(root, text="Free-Q v1.0")
font1 = ('Calibri (Body)', 18, 'bold')
title.config(font = font1)
#title.place(relx=0.5, rely= 0.2, anchor = 'center')
title.pack()

# ----------------------------------------------------------------------
# Place buttons
# ----------------------------------------------------------------------

bttn("S T A R T", startTracking, root)
bttn("C A N C E L", stopButton, root)


# ----------------------------------------------------------------------
# Mainloop
# ----------------------------------------------------------------------
root.mainloop()