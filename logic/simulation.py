import tkinter as tk
from models.passenger import Passenger
from models.bus import Bus
import random

from route import ROUTE1_CONNECTIONS, ROUTE2_CONNECTIONS, STOP_POSITIONS

PASSENGER_GENERATION_INTERVAL = 2  # seconds
BUS_MOVE_DELAY = 2  # seconds
STOP_WAIT_TIME = 2  # seconds
STOP_RADIUS = 25  # Radius for larger stops
SMOOTH_MOVE_INTERVAL = 50  # milliseconds
STEPS_PER_ROUTE = 20  # Number of steps between stops for smooth movement



class BusSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Bus Simulation")

        self.bus1 = Bus(capacity=10)  # Bus for Route 1
        self.bus2 = Bus(capacity=10)  # Bus for Route 2

        self.stops = {i: [] for i in STOP_POSITIONS.keys()}
        self.passenger_list = []
        self.passenger_id = 1

        # Track the routes
        self.route1_index = 0
        self.route2_index = 0

        # Canvas for drawing the routes and buses
        self.canvas = tk.Canvas(root, width=900, height=500, bg='white')
        self.canvas.pack()

        # Status panel container
        self.status_panel = tk.Frame(root)
        self.status_panel.pack(fill=tk.X, pady=5)

        # Passenger Status
        self.status_frame = tk.Frame(self.status_panel, bg="light gray", relief=tk.RAISED, bd=2)
        self.status_frame.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        self.status_label = tk.Label(self.status_frame, text="Passenger Status", anchor="w",
                                     bg="light gray", font=("Arial", 14, "bold"))
        self.status_label.pack(fill=tk.X, padx=10, pady=5)

        self.status_text = tk.Text(self.status_frame, height=10, width=50, bg="black", fg="white",
                                   font=("Arial", 12))
        self.status_text.pack(fill=tk.BOTH, padx=10, pady=5)

        # Passenger Count
        self.passenger_count_frame = tk.Frame(self.status_panel, bg="light gray", relief=tk.RAISED, bd=2)
        self.passenger_count_frame.pack(side=tk.RIGHT, padx=10)

        self.passenger_count_inner_frame = tk.Frame(self.passenger_count_frame, bg="black", relief=tk.FLAT)
        self.passenger_count_inner_frame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        self.passenger_count_label = tk.Label(
            self.passenger_count_inner_frame, text="Passengers on Bus 1: 0\nPassengers on Bus 2: 0",
            font=("Arial", 12), bg="black", fg="white"
        )
        self.passenger_count_label.pack(padx=10, pady=10)

        # Start simulation
        self.root.after(1000, self.generate_passenger)
        self.root.after(1000, self.move_bus1)
        self.root.after(1000, self.move_bus2)

    def update_status(self):
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(tk.END, "Passengers at Stops:\n")
        for p in self.passenger_list:
            self.status_text.insert(
                tk.END, f"Passenger {p.id}: {p.status} | Start: {p.start}, End: {p.end}\n"
            )
        self.passenger_count_label.config(
            text=f"Passengers on Bus 1: {len(self.bus1.passengers)}\nPassengers on Bus 2: {len(self.bus2.passengers)}"
        )

    def generate_passenger(self):
        route_choice = random.choice([1, 2])
        if route_choice == 1:
            active_stops = {stop for connection in ROUTE1_CONNECTIONS for stop in connection}
        else:
            active_stops = {stop for connection in ROUTE2_CONNECTIONS for stop in connection}

        start = random.choice(list(active_stops)[:-1])
        end = random.choice([s for s in active_stops if s > start])
        passenger = Passenger(self.passenger_id, start, end)
        self.stops[start].append(passenger)
        self.passenger_list.append(passenger)
        self.passenger_id += 1
        self.update_status()
        self.draw_routes()
        self.root.after(PASSENGER_GENERATION_INTERVAL * 1000, self.generate_passenger)

    def move_bus1(self):
        current_stop, next_stop = ROUTE1_CONNECTIONS[self.route1_index]
        self.route1_index = (self.route1_index + 1) % len(ROUTE1_CONNECTIONS)
        self.smooth_move_bus(self.bus1, current_stop, next_stop, "red")

    def move_bus2(self):
        current_stop, next_stop = ROUTE2_CONNECTIONS[self.route2_index]
        self.route2_index = (self.route2_index + 1) % len(ROUTE2_CONNECTIONS)
        self.smooth_move_bus(self.bus2, current_stop, next_stop, "blue")

    def draw_routes(self):
        self.canvas.delete("all")
        for (stop1, stop2) in ROUTE1_CONNECTIONS:
            x1, y1 = STOP_POSITIONS[stop1]
            x2, y2 = STOP_POSITIONS[stop2]
            self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

        for (stop1, stop2) in ROUTE2_CONNECTIONS:
            x1, y1 = STOP_POSITIONS[stop1]
            x2, y2 = STOP_POSITIONS[stop2]
            self.canvas.create_line(x1, y1, x2, y2, fill="gray", width=2)

        for stop, (x, y) in STOP_POSITIONS.items():
            self.canvas.create_oval(
                x - STOP_RADIUS, y - STOP_RADIUS, x + STOP_RADIUS, y + STOP_RADIUS,
                fill="light blue"
            )
            self.canvas.create_text(x, y, text=f"Stop {stop}")
            for i, passenger in enumerate(self.stops[stop]):
                self.canvas.create_oval(
                    x - 35 + i * 10, y - 40, x - 25 + i * 10, y - 30, fill="orange"
                )
    def smooth_move_bus(self, bus, start_stop, end_stop, color):
        x1, y1 = STOP_POSITIONS[start_stop]
        x2, y2 = STOP_POSITIONS[end_stop]
        dx = (x2 - x1) / STEPS_PER_ROUTE
        dy = (y2 - y1) / STEPS_PER_ROUTE

        def step(i):
            if i <= STEPS_PER_ROUTE:
                new_x = x1 + i * dx
                new_y = y1 + i * dy

                self.draw_routes()
                self.canvas.create_rectangle(
                    new_x - 15, new_y - 15, new_x + 15, new_y + 15, fill=color
                )

                self.root.after(SMOOTH_MOVE_INTERVAL, lambda: step(i + 1))
            else:
                bus.current_stop = end_stop

                for passenger in self.stops[end_stop][:]:
                    if bus.board_passenger(passenger):
                        self.stops[end_stop].remove(passenger)

                bus.deboard_passengers()
                self.update_status()
                if bus == self.bus1:
                    self.root.after(STOP_WAIT_TIME * 1000, self.move_bus1)
                else:
                    self.root.after(STOP_WAIT_TIME * 1000, self.move_bus2)

        step(0)


if __name__ == "__main__":
    root = tk.Tk()
    app = BusSimulation(root)
    root.mainloop()
