# main.py
import tkinter as tk
from logic.simulation import BusSimulation

def main():
    root = tk.Tk()
    root.title("Bus Simulation")
    simulation = BusSimulation(root)
    root.mainloop()

if __name__ == "__main__":
    main()