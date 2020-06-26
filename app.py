try:
    from Tkinter import *
except ModuleNotFoundError:
    from tkinter import *
    from tkinter import messagebox

import datetime
from time import sleep
import simpleaudio as sa
import os
import todoList

sound = "analog-watch-alarm_daniel-simion.wav"

path = os.path.dirname(os.path.realpath(__file__)) + "/"
# Credits to https://soundbible.com/2197-Analog-Watch-Alarm.html for the sound file 
alarm = sa.WaveObject.from_wave_file(path + sound)

class Timer:
    def __init__(self):

        self.root = Tk()
        self.root.title("Pomodoro Timer")

        try:
            with open(path + "data.txt") as file:
                print("GOT PREVIOUS SESSION DATA")
                self.work0 = int(file.readline())
                self.rest0 = int(file.readline())
        except (FileNotFoundError):
            self.work0 = 35
            self.rest0 = 10

        self.work = self.work0 * 60
        self.rest = self.rest0 * 60

        self.job = None
        self.sessions = 0

        title = Label(self.root, text = "Pomodoro Timer", font = ("Arial", 20))
        title.pack()

        input = Frame(self.root, bd = 15)
        input.pack()

        durationLabel = Label(input, text = "Enter Work Duration(mins):", font = ("Arial", 14))
        durationLabel.pack(side = LEFT)
        self.durationInput = Entry(input, font = ("Arial", 14))
        self.durationInput.pack(side = LEFT)

        breakDuration = Label(input, text = "Enter Break Duration(mins):", font = ("Arial", 14))
        breakDuration.pack(side = LEFT)
        self.breakInput = Entry(input, font = ("Arial", 14))
        self.breakInput.pack(side = LEFT)

        confirmBtn = Button(self.root, text = "Confirm", font = ("Arial", 12), width = 40, command = lambda: self.confirmInputs())
        confirmBtn.pack()

        timerFrame = Frame(self.root)
        timerFrame.pack()

        durationFrame = Frame(timerFrame, bd = 10)
        durationFrame.pack(side = LEFT)
        self.durationText = datetime.timedelta(seconds = self.work)
        self.durationTimer = Label(durationFrame, text = self.durationText, font = ("Arial", 35), fg = "red")
        self.durationTimer.pack()
        labelDuration = Label(durationFrame, text = "Work Remaining")
        labelDuration.pack()

        breakFrame = Frame(timerFrame, bd = 10)
        breakFrame.pack(side = LEFT)
        self.breakText = datetime.timedelta(seconds = self.rest)
        self.breakTimer = Label(breakFrame, text = self.breakText, font = ("Arial", 35), fg = "red")
        self.breakTimer.pack()
        labelBreak = Label(breakFrame, text = "Break Remaining")
        labelBreak.pack()

        sessionsFrame = Frame(timerFrame, bd = 10)
        sessionsFrame.pack(side = LEFT)
        self.sessionsCounter = Label(sessionsFrame, text = self.sessions, font = ("Arial", 35), fg = "red")
        self.sessionsCounter.pack()
        sessionsLabel = Label(sessionsFrame, text = "Sessions Worked")
        sessionsLabel.pack()

        btnsFrame = Frame(self.root, bd = 18)
        btnsFrame.pack()

        startBtn = Button(btnsFrame, command = lambda : self.startTimer(), 
                                    text = "Start", 
                                    font = ("Arial", 12),
                                    padx = 25,
                                    )
        startBtn.pack(side = LEFT, padx = 10)

        pauseBtn = Button(btnsFrame, 
                            command = lambda : self.pauseTimer(), 
                            text = "Pause", 
                            font = ("Arial", 12),
                            padx = 25
                            )
        pauseBtn.pack(side = LEFT, padx = 10)
        

        restartBtn = Button(btnsFrame,
                            command = lambda : self.restartTimer(), 
                            text = "Restart", 
                            font = ("Arial", 12),
                            padx = 25
                            )
        restartBtn.pack(side = LEFT, padx = 10)

        windowWidth = self.root.winfo_reqwidth()
        windowHeight = self.root.winfo_reqheight()
        positionRight = int(self.root.winfo_screenwidth()/2 - windowWidth * 2.2)
        positionDown = int(self.root.winfo_screenheight()/5 - windowHeight/2)
        self.root.geometry("+{}+{}".format(positionRight, positionDown))

        self.todoList = todoList.todoList(self.root)

        self.root.mainloop()

    def confirmInputs(self):
        if (self.validateInputs()):
            self.pauseTimer()
            with open(path + "data.txt", "w+") as file:
                file.write(str(self.work0))
                file.write("\n")
                file.write(str(self.rest0))
            self.work = self.work0 * 60
            self.rest = self.rest0 * 60

            self.durationText = datetime.timedelta(seconds = self.work)
            self.durationTimer.configure(text = self.durationText)

            self.breakText = datetime.timedelta(seconds = self.rest)
            self.breakTimer.configure(text = self.breakText)

    def validateInputs(self):
        try:
            work = int(self.durationInput.get())
            rest = int(self.breakInput.get())
            self.work0 = work
            self.rest0 = rest

            if (self.work0 >= 0 and self.rest0 >= 0):
                return True
            else:
                return False
        except ValueError:
            if (self.work == 35 and self.rest == 10):
                return True
            messagebox.showerror("Error", "Invalid Inputs")
            return False

    def startTimer(self):
        if (self.work >= 0):
            self.durationText = datetime.timedelta(seconds = self.work)
            self.durationTimer.configure(text = self.durationText)
            self.work -= 1
            self.job = self.durationTimer.after(1000, self.startTimer)
        else:
            self.playAlarm()
            self.startBreak()

    def startBreak(self):      
        if (self.rest >= 0):
            self.breakText = datetime.timedelta(seconds = self.rest)
            self.breakTimer.configure(text = self.breakText)
            self.rest -= 1
            self.job = self.breakTimer.after(1000, self.startBreak)
        else:
            self.sessions += 1
            self.sessionsCounter.configure(text = self.sessions)
            self.playAlarm()
            self.restartTimer()
    
    def playAlarm(self):
        print(self.job)
        player = alarm.play()
        sleep(1.5)
        player.stop()
        sleep(1)

    def pauseTimer(self):
        if (self.job is not None):
            self.durationTimer.after_cancel(self.job)
            self.breakTimer.after_cancel(self.job)
            self.job = None

    def restartTimer(self):
        self.pauseTimer()
        
        self.work = self.work0 * 60
        self.rest = self.rest0 * 60

        self.durationText = datetime.timedelta(seconds = self.work)
        self.durationTimer.configure(text = self.durationText)

        self.breakText = datetime.timedelta(seconds = self.rest)
        self.breakTimer.configure(text = self.breakText)


timer = Timer()