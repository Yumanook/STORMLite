from Tkinter import *
from picamera import PiCamera
from time import sleep
from time import localtime, strftime
import PIL.Image
from PIL import ImageTk
import numpy as np
import os
from StringIO import StringIO
from Image_Processingv8 import processed
from LED_display import detected
import threading
import tkSimpleDialog
from specimens import *
import random
from datetime import datetime, timedelta

#importing all libraries necessary to run program

class STORMLite(Frame): #mainframe to establish GUI

    global frames
    frames = 0
    global specimen
    global namePic
    specimen = [[],[],[]] #will include list of objects to be created after final screening to be picked from by user interface
    global output
    global triangle
    global rectangle
    global square
    initScreen = PIL.Image.new("RGB", (400,240))
    timeX = strftime("%m-%d-%Y_%H:%M:%S", localtime())
    output = "/home/pi/Desktop/Microscopy Control Files/Screenings/" + timeX + ".jpg" #saves image to screenings folder so that the image processing script can access previous files and collapse them
    initScreen.save(output)
    
    
    def __init__(self, master = None): #initializes screen
        Frame.__init__(self, master)

        self.master = master

        self.STORM()

    def STORM(self): #defines features of starting window
        self.master.title("BETA STORMLite")
        self.pack(fill = BOTH, expand = 1)

        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu)
        file.add_command(label = 'Exit', command = self.exit)
        file.add_command(label = 'Run', command = self.runIt)
        menu.add_cascade(label = 'File', menu = file)

        settings = Menu(menu)
        settings.add_command(label = 'Change Frame Count', command = self.setFrameCount)
        settings.add_command(label = 'Change Fluorophore Type')
        #make command for above statement
        settings.add_command(label = 'Change Specimen', command = self.setSpecimen)
        menu.add_cascade(label = 'Settings', menu = settings)
        
    def exit(self):
        exit()

    def setSpecimen(self):
        global specimen
        specimen = tkSimpleDialog.askstring("setSpecimen","Set Specimen (choose from \"triangle\", \"square\", or \"rectangle\")")
        
    def setFrameCount(self):
        global frames
        frames = tkSimpleDialog.askinteger("setFrame", "Set Frame Count", minvalue = 1, maxvalue = 30)
    
    def takePic(self, time):
        global frames
        global namePic
        global output
        self.timeX = strftime("%m-%d-%Y_%H:%M:%S", localtime())
        camera = PiCamera()
        namePic = "/home/pi/Desktop/Microscopy Control Files/Screenings/" + self.timeX + ".jpg"
        camera.start_preview(fullscreen = False, window = (400,240,400,240))
        sleep(1.5)
        camera.capture(namePic, resize = (400,240))
        camera.stop_preview()
        camera.close()
        #img = PIL.Image.open(namePic)
        #photo = ImageTk.PhotoImage(img)
        #label = Label(image=photo)
        #label.pack()
        processed(namePic,output)
        
    def showFrameCount(self, frames):
        global v
        if frames == 0:
            v.set("Finished")
        else:
            v.set("Number of Frames Left: " + str(frames))

    def runIt(self):
        global v
        global frames
        global namePic
        global specimen
        v = StringVar()
        
        stuff = Label(self, text = "Total number of Frames: " + str(frames))
        stuff.pack()
        Label(self, textvariable = v).pack()
        root.update_idletasks()
        if frames > 0:
            #threading.Thread(target = detected, args = ([[1,1],[2,2],[3,3],[4,4],[5,5]], int(random.random()*3 + 1))).start()
            threading.Thread(target = detected, args = (globals()[specimen], int(random.random()*3 + 1))).start()
            #fix above stuff to specimen file
            threading.Thread(target = self.takePic, args = (2.5,)).start()
            frames = frames - 1
        
root = Tk()

root.geometry("400x480")

app = STORMLite(root)

root.mainloop()
