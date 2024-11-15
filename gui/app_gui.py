# # gui/app_gui.py

# import tkinter as tk
# from logic.simulation import Simulation
# from config.settings import SIMULATION_SPEED

# class BusSimulationApp:
#     def __init__(self, bus_capacity, num_stops):
#         self.simulation = Simulation(bus_capacity, num_stops)
#         self.root = tk.Tk()
#         self.root.title("Bus Simulation")
#         self.canvas = tk.Canvas(self.root, width=1500, height=1000)  # Further increased canvas size
#         self.canvas.pack()

#         # Store the positions of each stop
#         self.stop_positions = []
#         self.stop_labels = []  # Labels for displaying waiting passengers
#         self.buses = []  # References to bus icons on canvas
        
#         self.setup_route(num_stops)
        
#     def setup_route(self, num_stops):
#         # Draw bus stops as blue circles on the route with greater spacing
#         for i in range(num_stops):
#             x, y = i * 150 + 100, 300  # Significantly increased horizontal spacing
#             self.stop_positions.append((x, y))
#             self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="blue")
#             self.canvas.create_text(x, y + 35, text=f"Stop {i}")  # Position text below the stop

#             # Initialize a label for waiting passenger count at each stop, placed higher
#             label = self.canvas.create_text(x, y - 40, text="Waiting: 0")  # Higher above the stop
#             self.stop_labels.append(label)

#     def draw_buses(self):
#         # Remove existing bus icons
#         for bus_icon in self.buses:
#             self.canvas.delete(bus_icon)
#         self.buses.clear()

#         # Draw each bus at its current position with passenger count
#         for bus in self.simulation.buses:
#             stop_x, stop_y = self.stop_positions[bus.current_stop]
#             # Place the bus rectangle further below the stop
#             bus_icon = self.canvas.create_rectangle(stop_x - 25, stop_y + 20, stop_x + 25, stop_y + 50, fill="red")
#             passenger_text = f"Bus\nPassengers: {len(bus.passengers)}"
#             # Position bus info well below the bus icon
#             self.canvas.create_text(stop_x, stop_y + 70, text=passenger_text, fill="black")
#             self.buses.append(bus_icon)

#     def update(self):
#         # Update the simulation state
#         self.simulation.generate_passenger()
#         self.simulation.manage_buses()

#         # Update waiting passenger counts at each stop
#         for i, stop in enumerate(self.simulation.stops):
#             waiting_count = len(stop.waiting_passengers)
#             self.canvas.itemconfigure(self.stop_labels[i], text=f"Waiting: {waiting_count}")

#         # Update the buses on the GUI
#         self.draw_buses()

#         # Schedule the next update
#         self.root.after(1000 // SIMULATION_SPEED, self.update)

#     def run(self):
#         # Start the simulation update loop
#         self.root.after(1000 // SIMULATION_SPEED, self.update)
#         self.root.mainloop()