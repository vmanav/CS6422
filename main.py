from logic.simulation import BusSimulation
import tkinter as tk

def main():
    root = tk.Tk()
    simulation = BusSimulation(root)
    root.mainloop()

if __name__ == "__main__":
    main()
