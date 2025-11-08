from tkinter.ttk import Frame, Button, Label, Entry, Style
from tkinter import Menu, BOTH, END, messagebox, filedialog
import sys
from StudentIDDlg import StudentIDDlg
from LoanCalculator import LoanCalculator
from FeedBackDlg import FeedBackDlg


class MyFrame(Frame):
    
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.LCD = None
        self.FBD = None
        self.initUI()
    
    def initUI(self):
        self.parent.title("GUI Controls Test")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)
        
        # Create menus
        menuBar = Menu(self.parent)
        mnuFile = Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="File", menu=mnuFile)
        mnuFile.add_command(label="Open", command=self.mnuOpenFileClick)
        mnuFile.add_command(label="Save", command=self.mnuSaveFileClick)
        mnuFile.add_separator()
        mnuFile.add_command(label="Exit", command=self.exitButtonClick)
        
        mnuCustomers = Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="Loan Processing", menu=mnuCustomers)
        mnuCustomers.add_command(label="Loan Calculator", command=self.loanCalcButtonClick)
        mnuCustomers.add_separator()
        mnuCustomers.add_command(label="Provide Feedback", command=self.mnuShowFeedbackClick)
        
        self.parent.config(menu=menuBar)
        
        xpos = 30
        ypos = 40
        xpos2 = xpos + 120
        
        # Styling
        style = Style()
        style.configure("Exit.TButton", foreground="red", background="white")
        style.configure("MainButton.TButton", foreground="yellow", background="red")
        
        testButton = Button(self, text="Get StudentID", command=self.btnGetStudentIDClick)
        testButton.configure(style="MainButton.TButton")
        testButton.place(x=xpos, y=ypos)
        
        self.txtID = Entry(self, text="", foreground="#ff0000", background="light blue", font="Arial 9")
        self.txtID.place(x=xpos2, y=ypos)
        self.txtID.configure(state="readonly")
        
        ypos += 30
        btnLoanCalc = Button(self, text="Loan Calculator", command=self.loanCalcButtonClick)
        btnLoanCalc.configure(style="Exit.TButton")
        btnLoanCalc.place(x=xpos, y=ypos)
        
        ypos += 30
        exitButton = Button(self, text="Exit", command=self.exitButtonClick)
        exitButton.configure(style="Exit.TButton")
        exitButton.place(x=xpos, y=ypos)
    
    def exitButtonClick(self):
        if messagebox.askokcancel("OK to close?", "Close application?"):
            self.parent.destroy()
            exit()
    
    def btnGetStudentIDClick(self):
        dlg = StudentIDDlg("your ID", "Student ID?", "Please Enter your Student ID:")
        dlg.grab_set()
        self.wait_window(dlg)
        self.txtID.configure(state="normal")
        self.txtID.delete(0, END)
        self.txtID.insert(0, dlg.getID())
        self.txtID.configure(state="readonly")
        print(dlg.getID())
    
    def loanCalcButtonClick(self):
        if self.LCD is None:
            self.LCD = LoanCalculator()
        else:
            if self.LCD.winfo_exists():
                self.LCD.focus()
            else:
                self.LCD = LoanCalculator()
    
    def mnuOpenFileClick(self):
        options = {}
        options['initialdir'] = '.'
        options['filetypes'] = [('all files', '.*'), ('jpeg files', '.jpg'), ('png files', '.png')]
        fname = filedialog.askopenfilename(**options)
        if fname:
            try:
                from PIL import Image
                img = Image.open(fname)
                img.show()
            except ImportError:
                messagebox.showinfo("File Selected", f"Selected file: {fname}\n\nInstall Pillow to view images:\npip install Pillow")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {e}")
    
    def mnuSaveFileClick(self):
        messagebox.showinfo("Save", "Save functionality not implemented")
    
    def mnuShowFeedbackClick(self):
        if self.FBD is None:
            self.FBD = FeedBackDlg()
        else:
            if self.FBD.winfo_exists():
                self.FBD.focus()
            else:
                self.FBD = FeedBackDlg()