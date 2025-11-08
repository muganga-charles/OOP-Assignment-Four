from tkinter.ttk import Button, Label, Entry, Style
from tkinter import Toplevel


class StudentIDDlg(Toplevel):
    def __init__(self, initialText, title, labeltext=''):
        Toplevel.__init__(self)
        self.initUI(initialText, title, labeltext)
    
    def initUI(self, initialText, title, labeltext=''):
        self.STID = initialText
        self.geometry("250x120")
        if len(title) > 0:
            self.title(title)
        self.style = Style()
        self.style.theme_use("default")
        
        if len(labeltext) == 0:
            labeltext = 'Please enter your ID..'
        self.bind("<Return>", self.ok)
        
        xpos = 20
        ypos = 30
        xpos2 = xpos + 80
        
        l1 = Label(self, text=initialText, foreground="#ff0000", background="light blue", font="Arial 9")
        l1.place(x=xpos, y=ypos)
        
        self.txtID = Entry(self)
        self.txtID.place(x=xpos2, y=ypos, width=120)
        self.txtID.bind("<Return>", self.ok)
        self.txtID.bind("<Escape>", self.cancel)
        self.txtID.focus_set()
        
        ypos += 40
        
        okButton = Button(self, text="OK", background="light blue", command=self.ok)
        okButton.place(x=xpos2, y=ypos)
        
        cancelButton = Button(self, text="Cancel", command=self.cancel)
        cancelButton.place(x=xpos2 + 60, y=ypos)
    
    def getID(self):
        return self.STID
    
    def ok(self, event=None):
        self.STID = self.txtID.get()
        self.destroy()
    
    def cancel(self, event=None):
        self.destroy()