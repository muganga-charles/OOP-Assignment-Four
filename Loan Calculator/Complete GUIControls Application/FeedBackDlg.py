from tkinter import Toplevel, BooleanVar, StringVar, Checkbutton, Radiobutton, Listbox, OptionMenu, EXTENDED, END, messagebox
from tkinter.ttk import Button, Label, Entry, Style


class FeedBackDlg(Toplevel):
    
    def __init__(self):
        Toplevel.__init__(self)
        self.initUI()
    
    def initUI(self):
        self.title("Feedback Form")
        self.geometry("600x450")
        self.style = Style()
        self.style.theme_use("default")
        
        xpos = 40
        ypos = 30
        xpos2 = xpos + 180
        
        # First Name
        l1 = Label(self, text="First Name:", foreground="#ff0000", background="light blue", font="Arial 9")
        l1.place(x=xpos, y=ypos)
        self.txtFirstName = Entry(self)
        self.txtFirstName.place(x=xpos2, y=ypos, width=150)
        
        ypos += 30
        # Email
        l2 = Label(self, text="Email:", foreground="#ff0000", background="light blue", font="Arial 9")
        l2.place(x=xpos, y=ypos)
        self.txtEmail = Entry(self)
        self.txtEmail.place(x=xpos2, y=ypos, width=200)
        
        ypos += 40
        # Checkboxes
        l3 = Label(self, text="Product Interests:", foreground="#ff0000", background="light blue", font="Arial 9 bold")
        l3.place(x=xpos, y=ypos)
        
        ypos += 25
        self.electronicsChoice = BooleanVar()
        self.electronicsChoice.set(True)
        self.chkElectronics = Checkbutton(self, text="Electronics", variable=self.electronicsChoice)
        self.chkElectronics.place(x=xpos2, y=ypos)
        
        self.sportsChoice = BooleanVar()
        self.chkSports = Checkbutton(self, text="Sports", variable=self.sportsChoice)
        self.chkSports.place(x=xpos2 + 100, y=ypos)
        
        self.gardeningChoice = StringVar()
        self.gardeningChoice.set("YES")
        self.chkGardening = Checkbutton(self, text="Gardening", variable=self.gardeningChoice, onvalue="YES", offvalue="NO")
        self.chkGardening.place(x=xpos2 + 200, y=ypos)
        
        ypos += 40
        # Radio buttons
        l4 = Label(self, text="Service Rating:", foreground="#ff0000", background="light blue", font="Arial 9 bold")
        l4.place(x=xpos, y=ypos)
        
        ypos += 25
        serviceChoices = [("Disappointed", "0"), ("Satisfied", "1"), ("Good", "2"), ("Excellent", "3")]
        self.serviceFeedback = StringVar()
        self.serviceFeedback.set("2")
        inc = 0
        for text, val in serviceChoices:
            radBtn = Radiobutton(self, text=text, variable=self.serviceFeedback, value=val)
            radBtn.place(x=xpos2 + inc, y=ypos)
            inc += 90
        
        ypos += 40
        # Listbox
        l5 = Label(self, text="Select State(s):", foreground="#ff0000", background="light blue", font="Arial 9 bold")
        l5.place(x=xpos, y=ypos)
        
        states = ["Connecticut", "New York", "New Jersey", "Massachusetts"]
        self.lb = Listbox(self, selectmode=EXTENDED, height=len(states))
        self.lb.place(x=xpos2, y=ypos, width=150)
        self.lb.delete(0, END)
        for state in states:
            self.lb.insert(END, state)
        
        ypos += 100
        # Dropdown
        l6 = Label(self, text="Department:", foreground="#ff0000", background="light blue", font="Arial 9 bold")
        l6.place(x=xpos, y=ypos)
        
        departments = ["Sales", "Marketing", "HR", "Technology"]
        self.dept = StringVar()
        self.dept.set("HR")
        self.ddlDept = OptionMenu(self, self.dept, *departments)
        self.ddlDept.place(x=xpos2, y=ypos, width=150)
        
        ypos += 50
        # Submit button
        style = Style()
        style.configure("MainButton.TButton", foreground="white", background="green")
        
        btnSubmit = Button(self, text="Submit Feedback", command=self.btnSubmitClick)
        btnSubmit.configure(style="MainButton.TButton")
        btnSubmit.place(x=xpos2, y=ypos, width=150)
    
    def btnSubmitClick(self):
        feedback_data = {
            'name': self.txtFirstName.get(),
            'email': self.txtEmail.get(),
            'electronics': self.electronicsChoice.get(),
            'sports': self.sportsChoice.get(),
            'gardening': self.gardeningChoice.get(),
            'service_rating': self.serviceFeedback.get(),
            'department': self.dept.get()
        }
        
        selected_states = [self.lb.get(i) for i in self.lb.curselection()]
        feedback_data['states'] = selected_states
        
        print("\n=== Feedback Submitted ===")
        print(f"Name: {feedback_data['name']}")
        print(f"Email: {feedback_data['email']}")
        print(f"Electronics: {feedback_data['electronics']}")
        print(f"Sports: {feedback_data['sports']}")
        print(f"Gardening: {feedback_data['gardening']}")
        print(f"Service Rating: {feedback_data['service_rating']}")
        print(f"States: {', '.join(selected_states)}")
        print(f"Department: {feedback_data['department']}")
        print("=========================\n")
        
        messagebox.showinfo("Feedback Submitted", "Thank you for your feedback!")