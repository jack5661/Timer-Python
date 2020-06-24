from tkinter import *

class todoList:

    def __init__(self, window):
        self.root = window
        fnt = ("Arial", 12)
        inputFrame = Frame(self.root, bd = 10)
        inputFrame.pack()
        inputLabel = Label(inputFrame, text = "Enter Your Thoughts:", font = fnt)
        inputLabel.pack(side = LEFT)
        self.inputEntry = Entry(inputFrame, font = fnt)
        self.inputEntry.pack(side = LEFT)
        self.inputEntry.bind("<Return>", lambda event : self.addToList(event))
        
        listFrame = Frame(self.root, bd = 10)
        listFrame.pack()

        self.listBoxLabel = Label(listFrame, text = "Things to do in Break:", font = fnt)
        self.listBoxLabel.pack()
        
        scroll = Scrollbar(listFrame)
        scroll.pack(side = RIGHT, fill = Y)

        self.listBox = Listbox(listFrame, width = 40, font = fnt, yscrollcommand = scroll.set, selectmode = SINGLE)
        scroll.config( command = self.listBox.yview)
        self.listBox.bind("<Double-1>", lambda event : self.removeSelected(event))
        self.listBox.bind('<FocusOut>', lambda e: self.listBox.selection_clear(0, END))
        self.listBox.bind('<Leave>', lambda e: self.listBox.selection_clear(0, END))
        self.listBox.pack()
        self.infoLabel = Label(listFrame, text = "*Delete Items by Clicking")
        self.infoLabel.pack()
        clear = Button(listFrame, text = "Clear Items", font = ("Arial", 11), command = lambda : self.listBox.delete(0, END))
        clear.pack(fill = X)

    def addToList(self, event):
        text = self.inputEntry.get()
        if (len(text) > 0):
            self.listBox.insert(END, text)
            self.inputEntry.delete(0, len(text))

    def removeSelected(self, event):
        if (self.listBox.size() > 0):
            w = event.widget
            index = int(w.curselection()[0])
            self.listBox.delete(index)
            self.listBox.selection_clear(0, self.listBox.size() - 1)

    


