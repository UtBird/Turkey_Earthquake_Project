import tkinter as tk
try:
    import customtkinter as ctk
except ImportError:
    ctk = None

from gui_app import App

def main():
    if ctk:
        # CustomTkinter ana penceresi
        root = ctk.CTk()
    else:
        root = tk.Tk()
        
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
