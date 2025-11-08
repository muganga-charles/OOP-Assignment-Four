from tkinter.ttk import Frame, Button, Label, Entry, Style
from tkinter import BOTH, END, messagebox, filedialog, Text, Toplevel, Scrollbar, RIGHT, Y
import json
import csv
from datetime import datetime
import re


class EnhancedMyFrame(Frame):
    
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.calculation_history = []
        self.initUI()
    
    def initUI(self):
        self.parent.title("Enhanced Loan Calculator")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)
        
        xpos = 30
        ypos = 20
        xpos2 = xpos + 150
        
        # Title
        title = Label(self, text="Professional Loan Calculator", foreground="#0000ff", background="light gray", font="Arial 12 bold")
        title.place(x=xpos + 50, y=ypos)
        
        ypos += 40
        
        # Amount
        l1 = Label(self, text="Loan Amount ($):", foreground="#ff0000", background="light blue", font="Arial 9 bold")
        l1.place(x=xpos, y=ypos)
        self.txtAmount = Entry(self, font="Arial 10")
        self.txtAmount.place(x=xpos2, y=ypos, width=120)
        self.txtAmount.bind("<KeyRelease>", lambda e: self.validate_numeric(self.txtAmount))
        
        ypos += 35
        # Rate
        l2 = Label(self, text="Interest Rate (%):", foreground="#ff0000", background="light blue", font="Arial 9 bold")
        l2.place(x=xpos, y=ypos)
        self.txtRate = Entry(self, font="Arial 10")
        self.txtRate.place(x=xpos2, y=ypos, width=120)
        self.txtRate.bind("<KeyRelease>", lambda e: self.validate_numeric(self.txtRate))
        
        ypos += 35
        # Duration
        l3 = Label(self, text="Loan Duration (months):", foreground="#ff0000", background="light blue", font="Arial 9 bold")
        l3.place(x=xpos, y=ypos)
        self.txtDuration = Entry(self, font="Arial 10")
        self.txtDuration.place(x=xpos2, y=ypos, width=120)
        self.txtDuration.bind("<KeyRelease>", lambda e: self.validate_numeric(self.txtDuration))
        
        ypos += 40
        # Separator
        sep1 = Label(self, text="═" * 60, foreground="gray")
        sep1.place(x=xpos, y=ypos)
        
        ypos += 20
        # Monthly Payment
        l4 = Label(self, text="Monthly Payment:", foreground="#000080", background="yellow", font="Arial 9 bold")
        l4.place(x=xpos, y=ypos)
        self.txtMonthlyPayment = Entry(self, font="Arial 10 bold", background="#ffffcc")
        self.txtMonthlyPayment.configure(state="readonly")
        self.txtMonthlyPayment.place(x=xpos2, y=ypos, width=120)
        
        ypos += 30
        # Total Payment
        l5 = Label(self, text="Total Amount Paid:", foreground="#000080", background="yellow", font="Arial 9 bold")
        l5.place(x=xpos, y=ypos)
        self.txtTotalPayment = Entry(self, font="Arial 10 bold", background="#ffffcc")
        self.txtTotalPayment.configure(state="readonly")
        self.txtTotalPayment.place(x=xpos2, y=ypos, width=120)
        
        ypos += 30
        # Total Interest
        l6 = Label(self, text="Total Interest Paid:", foreground="#ff0000", background="orange", font="Arial 9 bold")
        l6.place(x=xpos, y=ypos)
        self.txtTotalInterest = Entry(self, font="Arial 10 bold", background="#ffcc99")
        self.txtTotalInterest.configure(state="readonly")
        self.txtTotalInterest.place(x=xpos2, y=ypos, width=120)
        
        ypos += 40
        # Buttons Row 1
        style = Style()
        style.configure("Calc.TButton", foreground="white", background="green", font="Arial 9 bold")
        style.configure("Clear.TButton", foreground="white", background="orange")
        style.configure("Save.TButton", foreground="white", background="blue")
        style.configure("Exit.TButton", foreground="white", background="red")
        
        calcButton = Button(self, text="Calculate", command=self.calcButtonClick, width=12)
        calcButton.configure(style="Calc.TButton")
        calcButton.place(x=xpos, y=ypos)
        
        clearButton = Button(self, text="Clear All", command=self.clearFields, width=12)
        clearButton.configure(style="Clear.TButton")
        clearButton.place(x=xpos + 110, y=ypos)
        
        exportButton = Button(self, text="Export CSV", command=self.exportToCSV, width=12)
        exportButton.configure(style="Save.TButton")
        exportButton.place(x=xpos + 220, y=ypos)
        
        ypos += 35
        # Buttons Row 2
        saveButton = Button(self, text="Save", command=self.saveCalculation, width=12)
        saveButton.configure(style="Save.TButton")
        saveButton.place(x=xpos, y=ypos)
        
        loadButton = Button(self, text="Load", command=self.loadCalculation, width=12)
        loadButton.configure(style="Save.TButton")
        loadButton.place(x=xpos + 110, y=ypos)
        
        scheduleButton = Button(self, text="Full Schedule", command=self.showAmortization, width=12)
        scheduleButton.configure(style="Calc.TButton")
        scheduleButton.place(x=xpos + 220, y=ypos)
        
        ypos += 40
        # Preview Label
        l7 = Label(self, text="Payment Schedule Preview (First 5 Months):", foreground="#000000", background="light gray", font="Arial 9 bold")
        l7.place(x=xpos, y=ypos)
        
        ypos += 25
        # Text widget for preview
        self.txtSchedule = Text(self, height=7, width=60, font="Courier 8", state="disabled")
        self.txtSchedule.place(x=xpos, y=ypos)
        
        scrollbar = Scrollbar(self, command=self.txtSchedule.yview)
        scrollbar.place(x=xpos + 455, y=ypos, height=115)
        self.txtSchedule.config(yscrollcommand=scrollbar.set)
        
        ypos += 125
        # Exit button
        exitButton = Button(self, text="Exit Application", command=self.exitButtonClick, width=15)
        exitButton.configure(style="Exit.TButton")
        exitButton.place(x=xpos, y=ypos)
        
        # Status label
        self.statusLabel = Label(self, text="Ready", foreground="green", font="Arial 8")
        self.statusLabel.place(x=xpos + 180, y=ypos + 5)
    
    def validate_numeric(self, entry_widget):
        """Real-time validation for numeric input"""
        value = entry_widget.get()
        if value and not re.match(r'^\d*\.?\d*$', value):
            entry_widget.delete(len(value) - 1, END)
            entry_widget.config(background="#ffcccc")
            self.statusLabel.config(text="Invalid input!", foreground="red")
        else:
            entry_widget.config(background="white")
            self.statusLabel.config(text="Ready", foreground="green")
    
    def validate_inputs(self):
        """Validate all inputs before calculation"""
        try:
            amt = float(self.txtAmount.get())
            rate = float(self.txtRate.get())
            dur = float(self.txtDuration.get())
            
            if amt <= 0:
                messagebox.showerror("Validation Error", "Loan amount must be greater than 0")
                return None
            if rate < 0 or rate > 100:
                messagebox.showerror("Validation Error", "Interest rate must be between 0 and 100")
                return None
            if dur <= 0 or dur > 600:
                messagebox.showerror("Validation Error", "Duration must be between 1 and 600 months")
                return None
            
            return amt, rate, dur
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values in all fields")
            return None
    
    def calcButtonClick(self):
        """Calculate loan with validation"""
        inputs = self.validate_inputs()
        if inputs is None:
            return
        
        amt, rate, dur = inputs
        
        # Calculate monthly payment
        monthly_rate = rate / 1200.0
        if monthly_rate == 0:
            monthlyPayment = amt / dur
        else:
            monthlyPayment = amt * monthly_rate * ((1 + monthly_rate) ** dur) / (((1 + monthly_rate) ** dur) - 1)
        
        totalPayment = monthlyPayment * dur
        totalInterest = totalPayment - amt
        
        # Display results
        self.txtMonthlyPayment.configure(state="normal")
        self.txtMonthlyPayment.delete(0, END)
        self.txtMonthlyPayment.insert(0, f"${monthlyPayment:,.2f}")
        self.txtMonthlyPayment.configure(state="readonly")
        
        self.txtTotalPayment.configure(state="normal")
        self.txtTotalPayment.delete(0, END)
        self.txtTotalPayment.insert(0, f"${totalPayment:,.2f}")
        self.txtTotalPayment.configure(state="readonly")
        
        self.txtTotalInterest.configure(state="normal")
        self.txtTotalInterest.delete(0, END)
        self.txtTotalInterest.insert(0, f"${totalInterest:,.2f}")
        self.txtTotalInterest.configure(state="readonly")
        
        # Store in history
        calculation = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'amount': amt,
            'rate': rate,
            'duration': dur,
            'monthly_payment': monthlyPayment,
            'total_payment': totalPayment,
            'total_interest': totalInterest
        }
        self.calculation_history.append(calculation)
        
        # Show preview
        self.displayAmortizationPreview(amt, rate, dur, monthlyPayment)
        self.statusLabel.config(text="Calculation complete!", foreground="green")
    
    def displayAmortizationPreview(self, principal, rate, months, payment):
        """Display first 5 months of amortization schedule"""
        self.txtSchedule.configure(state="normal")
        self.txtSchedule.delete(1.0, END)
        
        monthly_rate = rate / 1200.0
        balance = principal
        
        header = f"{'Mo':<5}{'Payment':<13}{'Principal':<13}{'Interest':<13}{'Balance':<13}\n"
        self.txtSchedule.insert(END, header)
        self.txtSchedule.insert(END, "=" * 57 + "\n")
        
        for month in range(1, min(6, int(months) + 1)):
            interest = balance * monthly_rate
            principal_payment = payment - interest
            balance -= principal_payment
            
            line = f"{month:<5}${payment:<12,.2f}${principal_payment:<12,.2f}${interest:<12,.2f}${balance:<12,.2f}\n"
            self.txtSchedule.insert(END, line)
        
        if months > 5:
            self.txtSchedule.insert(END, f"\n... {int(months) - 5} more months. Click 'Full Schedule' to see all.\n")
        
        self.txtSchedule.configure(state="disabled")
    
    def showAmortization(self):
        """Show full amortization schedule in new window"""
        inputs = self.validate_inputs()
        if inputs is None:
            return
        
        amt, rate, dur = inputs
        monthly_rate = rate / 1200.0
        
        if monthly_rate == 0:
            monthlyPayment = amt / dur
        else:
            monthlyPayment = amt * monthly_rate * ((1 + monthly_rate) ** dur) / (((1 + monthly_rate) ** dur) - 1)
        
        # Create new window
        schedule_window = Toplevel(self)
        schedule_window.title(f"Complete Amortization Schedule - {int(dur)} Months")
        schedule_window.geometry("700x500")
        
        # Text widget with scrollbar
        text_widget = Text(schedule_window, wrap="none", font="Courier 9")
        scrollbar_y = Scrollbar(schedule_window, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar_y.set)
        
        scrollbar_y.pack(side=RIGHT, fill=Y)
        text_widget.pack(side="left", fill=BOTH, expand=True)
        
        # Generate schedule
        balance = amt
        header = f"{'Month':<8}{'Payment':<15}{'Principal':<15}{'Interest':<15}{'Balance':<15}\n"
        text_widget.insert(END, header)
        text_widget.insert(END, "=" * 68 + "\n")
        
        for month in range(1, int(dur) + 1):
            interest = balance * monthly_rate
            principal_payment = monthlyPayment - interest
            balance -= principal_payment
            
            line = f"{month:<8}${monthlyPayment:<14,.2f}${principal_payment:<14,.2f}${interest:<14,.2f}${balance:<14,.2f}\n"
            text_widget.insert(END, line)
        
        text_widget.configure(state="disabled")
        self.statusLabel.config(text="Full schedule displayed", foreground="blue")
    
    def clearFields(self):
        """Clear all input and output fields"""
        self.txtAmount.delete(0, END)
        self.txtRate.delete(0, END)
        self.txtDuration.delete(0, END)
        
        self.txtMonthlyPayment.configure(state="normal")
        self.txtMonthlyPayment.delete(0, END)
        self.txtMonthlyPayment.configure(state="readonly")
        
        self.txtTotalPayment.configure(state="normal")
        self.txtTotalPayment.delete(0, END)
        self.txtTotalPayment.configure(state="readonly")
        
        self.txtTotalInterest.configure(state="normal")
        self.txtTotalInterest.delete(0, END)
        self.txtTotalInterest.configure(state="readonly")
        
        self.txtSchedule.configure(state="normal")
        self.txtSchedule.delete(1.0, END)
        self.txtSchedule.configure(state="disabled")
        
        self.statusLabel.config(text="Fields cleared", foreground="orange")
    
    def saveCalculation(self):
        """Save calculation history to JSON file"""
        if not self.calculation_history:
            messagebox.showwarning("No Data", "No calculations to save. Please calculate first.")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Calculation History"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.calculation_history, f, indent=4)
                messagebox.showinfo("Success", f"Saved {len(self.calculation_history)} calculation(s) to:\n{filename}")
                self.statusLabel.config(text="Saved successfully", foreground="green")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}")
    
    def loadCalculation(self):
        """Load calculation from JSON file"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Load Calculation History"
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    self.calculation_history = json.load(f)
                
                if self.calculation_history:
                    last_calc = self.calculation_history[-1]
                    self.txtAmount.delete(0, END)
                    self.txtAmount.insert(0, str(last_calc['amount']))
                    
                    self.txtRate.delete(0, END)
                    self.txtRate.insert(0, str(last_calc['rate']))
                    
                    self.txtDuration.delete(0, END)
                    self.txtDuration.insert(0, str(last_calc['duration']))
                    
                    self.calcButtonClick()
                    
                    messagebox.showinfo("Success", f"Loaded {len(self.calculation_history)} calculation(s) from:\n{filename}")
                    self.statusLabel.config(text="Loaded successfully", foreground="green")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file:\n{e}")
    
    def exportToCSV(self):
        """Export amortization schedule to CSV"""
        inputs = self.validate_inputs()
        if inputs is None:
            return
        
        amt, rate, dur = inputs
        monthly_rate = rate / 1200.0
        
        if monthly_rate == 0:
            monthlyPayment = amt / dur
        else:
            monthlyPayment = amt * monthly_rate * ((1 + monthly_rate) ** dur) / (((1 + monthly_rate) ** dur) - 1)
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Amortization Schedule"
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Month', 'Payment', 'Principal', 'Interest', 'Balance'])
                    
                    balance = amt
                    for month in range(1, int(dur) + 1):
                        interest = balance * monthly_rate
                        principal_payment = monthlyPayment - interest
                        balance -= principal_payment
                        
                        writer.writerow([
                            month,
                            f"${monthlyPayment:.2f}",
                            f"${principal_payment:.2f}",
                            f"${interest:.2f}",
                            f"${balance:.2f}"
                        ])
                
                messagebox.showinfo("Success", f"Exported {int(dur)} months to:\n{filename}")
                self.statusLabel.config(text="Exported to CSV", foreground="green")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export:\n{e}")
    
    def exitButtonClick(self):
        if messagebox.askokcancel("Confirm Exit", "Are you sure you want to exit?"):
            self.parent.destroy()
            exit()