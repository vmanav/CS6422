# main.py

from logic.simulation import BusSimulation
import tkinter as tk

def main():
    root = tk.Tk()
    root.geometry("1000x700")  # Set initial size
    simulation = BusSimulation(root)
    root.mainloop()

if __name__ == "__main__":
    main()
