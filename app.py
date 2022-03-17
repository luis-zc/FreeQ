from cgi import test
from cgitb import text
from socket import setdefaulttimeout
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from turtle import width
from xml.dom import UserDataHandler
import pyautogui
import time
import random
import discord
from dhooks import Webhook
import data
from importlib import reload



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
root.resizable(False, False) 
root.geometry('300x200')
root['bg'] = '#141414'

# ----------------------------------------------------------------------
# Generic Button def
# ----------------------------------------------------------------------

def bttn(x,y,text,bcolor,fcolor, cmd, window, w, h):
    def on_enter(e):
        mybutton['background']=bcolor
        mybutton['foreground']=fcolor

    def on_leave(e):
        mybutton['background']=fcolor
        mybutton['foreground']=bcolor

    mybutton=Button(window,width=w,height = h, text = text,
                        fg=bcolor,
                        bg=fcolor,
                        border=0,
                        activeforeground=fcolor,
                        activebackground=bcolor,
                        command=cmd)
    mybutton.bind("<Enter>", on_enter)
    mybutton.bind("<Leave>", on_leave)

    mybutton.place(x=x,y=y)



# ----------------------------------------------------------------------
# Title
# ----------------------------------------------------------------------
title = Label(root, text="Free-Q v1.0", width = 100, height = 100, fg = "#c471ed", bg = "#141414")
font1 = ('Calibri (Body)', 18, 'bold')
title.config(font = font1)
title.place(relx=0.5, rely= 0.2, anchor = 'center')

# ----------------------------------------------------------------------
# Settings
# ----------------------------------------------------------------------
global top
top = None





def initSettings(top):
    top.title("Free-Q v1.0 Settings")
    top.iconbitmap('molangow.ico')
    top.resizable(False, False)
    top.geometry('600x400')
    top['bg'] = '#141414'
    def closeSettings():
        global top  
        top.destroy()
        top = None
    top.protocol('WM_DELETE_WINDOW', closeSettings)

    label1 = Label(top, text='Webhook url:', fg="#11998e", bg="#141414", font=('Arial', 12))
    label1.grid(row=0,column=0,padx=5,pady=20)


    textbox1=Entry(top,fg='white',bg="#141414",width=50, font=('Arial', 12),textvariable=data.hookUrl )
    textbox1.grid(row=0,column=1)

    label1 = Label(top, text='Webhook url:', fg="#11998e", bg="#141414", font=('Arial', 12))
    label1.grid(row=0,column=0,padx=5,pady=20)

    label2 = Label(top, text='UserID:', fg="#11998e", bg="#141414", font=('Arial', 12))
    label2.grid(row=1,column=0,padx=5,pady=20)

    textbox2=Entry(top,fg='white',bg="#141414",width=50, font=('Arial', 12), textvariable=data.userID)
    textbox2.grid(row=1,column=1)

    textbox = Text(top, width=70, height=10)
    textbox.place(relx=0.5, rely= 0.6, anchor = 'center')
    textbox.insert(INSERT, "Insert discord webhook url and userID (Enable developer setting in discord to access userIDs by rightclicking on profiles).\n")
    textbox.insert(INSERT, "The information is saved after closing the program.\n")
    textbox.insert(INSERT, "\n")
    textbox.insert(INSERT, "\n")
    textbox.insert(INSERT, "\n")
    textbox.insert(INSERT, "\n")
    textbox.insert(INSERT, "\n")
    textbox.insert(INSERT, "\n")
    textbox.insert(INSERT, "v1.0")

    def saveSettings():
        f = open("data.py", "w")
        f.write('hookUrl = "' + textbox1.get() + '"\n')
        f.write('userID = "' + textbox2.get() + '"\n')
        f.close()
        reload(data)
        messagebox.showinfo(title="Success", message="userdata was successfully updated")

    bttn(0,333,"S A V E", '#38ef7d', "#141414", saveSettings, top, 85,4)
    


def openSettings():
    global top
    if top == None:
        top = Toplevel()
        initSettings(top)
    else:
        top.focus_set()

settingsImage = PhotoImage(file='settings.gif')

settingsButton = Button(root, image=settingsImage, bg="#141414", border = 0, command=openSettings)
def on_enter(e):
    settingsButton['background']="#f64f59"
    settingsButton['foreground']="#141414"

def on_leave(e):
    settingsButton['background']="#141414"
    settingsButton['foreground']="#f64f59"

settingsButton.bind("<Enter>", on_enter)
settingsButton.bind("<Leave>", on_leave)
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

    hook = Webhook(f"{data.hookUrl}")

    e = discord.Embed(title="G A M E   F O U N D", description=f"Hey <@!{data.userID}>, you found a game!")
    e.add_field(name="Gamemode:", value=f"{gamemode}")
    e.add_field(name="Queue Time:", value=f"{qTime}")
    e.set_thumbnail(url=f"{thumbURL}")    
    hook.send(f"<@{data.userID}>")
    hook.send(embed = e)

def test():
    # Test function
    sendNotification(0)

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

    result = checkPixelColors(windowX,windowY,5)
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
# Place buttons
# ----------------------------------------------------------------------

bttn(0,80,"S T A R T", '#12c2e9', "#141414", startTracking, root, 42, 4)
bttn(0,140,"C A N C E L", '#f64f59', "#141414", stopButton, root, 42, 4)
#bttn(0,50,"T E S T", '#c471ed', "#141414", test)

# ----------------------------------------------------------------------
# Mainloop
# ----------------------------------------------------------------------
root.mainloop()