import tkinter as tk
from models.passenger import Passenger
from models.bus import Bus
import random

from config.constants import PASSENGER_GENERATION_INTERVAL, STOP_RADIUS
from route import ROUTE1_CONNECTIONS, ROUTE2_CONNECTIONS, STOP_POSITIONS
from logic.traversal import smooth_move_bus, move_bus1, move_bus1_help, move_bus2

class BusSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Bus Simulation")

        self.bus1 = Bus(capacity=15, name="B1")  # Route 1 bus
        self.bus2 = Bus(capacity=30, name="B2")  # Route 2 bus
        self.bus1_help = Bus(capacity=30, name="BH")  # HelperBus

        self.stops = {i: [] for i in STOP_POSITIONS.keys()}
        self.passenger_list = []
        self.passenger_id = 1

        self.route1_index = 0
        self.route1_help_index = 0
        self.route2_index = 0
        self.helper_bus = False

        # Canvas for routes and buses
        self.canvas = tk.Canvas(root, width=900, height=500, bg="white")
        self.canvas.pack()

        self.status_panel = tk.Frame(root)
        self.status_panel.pack(fill=tk.X, pady=5)

        # Passenger statuses
        self.status_frame = tk.Frame(self.status_panel, bg="light gray", relief=tk.RAISED, bd=2)
        self.status_frame.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        self.status_label = tk.Label(
            self.status_frame, text="Passenger Status", anchor="w",
            bg="light gray", font=("Arial", 14, "bold")
        )
        self.status_label.pack(fill=tk.X, padx=10, pady=5)

        self.status_text = tk.Text(self.status_frame, height=10, width=50, bg="black", fg="white", font=("Arial", 12))
        self.status_text.pack(fill=tk.BOTH, padx=10, pady=5)

        # Passenger Count
        self.passenger_count_frame = tk.Frame(self.status_panel, bg="light gray", relief=tk.RAISED, bd=2)
        self.passenger_count_frame.pack(side=tk.RIGHT, padx=10)

        self.passenger_count_inner_frame = tk.Frame(self.passenger_count_frame, bg="black", relief=tk.FLAT)
        self.passenger_count_inner_frame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        self.passenger_count_label = tk.Label(
            self.passenger_count_inner_frame,
            text="Passengers on Bus 1: 0\nPassengers on Bus 2: 0\nPassengers on Helper Bus: 0",
            font=("Arial", 12), bg="black", fg="white"
        )
        self.passenger_count_label.pack(padx=10, pady=10)

        # Start simulation
        self.root.after(1000, self.generate_passenger)
        self.root.after(1000, move_bus1(self))
        self.root.after(1000, move_bus2(self))

    def update_status(self):
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(tk.END, "Passengers at Stops:\n")
        for p in self.passenger_list:
            self.status_text.insert(
                tk.END, f"Passenger {p.id}: {p.status} | Start: {p.start}, End: {p.end}, Intermediate: {p.intermediate_stop}\n"
            )
        self.passenger_count_label.config(
            text=f"Passengers on Bus 1: {len(self.bus1.passengers)}\nPassengers on Bus 2: {len(self.bus2.passengers)}\nPassengers on Helper Bus: {len(self.bus1_help.passengers)}"
        )

    def generate_passenger(self):
        start = random.choice(list(STOP_POSITIONS.keys())[:-1])
        end = random.choice([s for s in STOP_POSITIONS.keys() if s > start])

        # Determine if start and end are on the same route
        route1_stops = {stop for conn in ROUTE1_CONNECTIONS for stop in conn}
        route2_stops = {stop for conn in ROUTE2_CONNECTIONS for stop in conn}

        if start in route1_stops and end in route2_stops:
            intermediate_stop = 3  # Intersection Stop
        elif start in route2_stops and end in route1_stops:
            intermediate_stop = 4  # Intersection Stop
        else:
            intermediate_stop = None

        passenger = Passenger(self.passenger_id, start, end)
        passenger.intermediate_stop = intermediate_stop  # Track transfer stop if needed
        self.stops[start].append(passenger)
        self.passenger_list.append(passenger)
        self.passenger_id += 1
        self.update_status()
        self.draw_routes()
        self.root.after(PASSENGER_GENERATION_INTERVAL * 1000, self.generate_passenger)


    def draw_routes(self):
        self.canvas.delete("all")
        for (stop1, stop2) in ROUTE1_CONNECTIONS:
            x1, y1 = STOP_POSITIONS[stop1]
            x2, y2 = STOP_POSITIONS[stop2]
            self.canvas.create_line(x1, y1, x2, y2, fill="red", width=10)

        for (stop1, stop2) in ROUTE2_CONNECTIONS:
            x1, y1 = STOP_POSITIONS[stop1]
            x2, y2 = STOP_POSITIONS[stop2]
            self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=10)

        for stop, (x, y) in STOP_POSITIONS.items():
            self.canvas.create_oval(
                x - STOP_RADIUS, y - STOP_RADIUS, x + STOP_RADIUS, y + STOP_RADIUS,
                fill="light blue"
            )
            self.canvas.create_text(x, y, text=f"Stop {stop}")

            for i, passenger in enumerate(self.stops[stop]):
                if(passenger.intermediate_stop):
                    self.canvas.create_polygon(x - 30 + i * 10, y - 40, x - 40 + i * 10, y - 20, x - 20 + i * 10, y - 20, fill="orange")
                else:
                    self.canvas.create_oval(
                        x - 35 + i * 10, y - 40, x - 25 + i * 10, y - 30, fill="orange"
                    )


if __name__ == "__main__":
    root = tk.Tk()
    simulation = BusSimulation(root)
    root.mainloop()
