import sys
from tkinter import Tk
from EnhancedMyFrame import EnhancedMyFrame

def main():
    root = Tk()
    root.geometry("520x650")
    app = EnhancedMyFrame(root)
    root.mainloop()

if __name__ == "__main__":
    sys.exit(int(main() or 0))