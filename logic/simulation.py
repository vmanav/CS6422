import tkinter as tk
from models.passenger import Passenger
from models.bus import Bus
from route import ROUTE_CONNECTIONS, STOP_POSITIONS
import random

PASSENGER_GENERATION_INTERVAL = 2  # seconds
BUS_MOVE_DELAY = 2  # seconds
STOP_WAIT_TIME = 2  # seconds
STOP_RADIUS = 25  # Radius for larger stops

class BusSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Bus Simulation")

        self.bus = Bus(capacity=10)
        self.stops = {i: [] for i in STOP_POSITIONS.keys()}
        self.passenger_list = []
        self.passenger_id = 1
        self.current_route_index = 0

        self.canvas = tk.Canvas(root, width=900, height=500, bg='white')
        self.canvas.pack()

        self.status_frame = tk.Frame(root)
        self.status_frame.pack()
        self.status_label = tk.Label(self.status_frame, text="Passenger Status")
        self.status_label.pack()
        self.status_text = tk.Text(self.status_frame, height=10, width=70)
        self.status_text.pack()

        self.root.after(1000, self.generate_passenger)
        self.root.after(1000, self.move_bus)

    def update_status(self):
        self.status_text.delete(1.0, tk.END)
        for p in self.passenger_list:
            self.status_text.insert(tk.END, f"Passenger {p.id}: {p.status} | Start: {p.start}, End: {p.end}\n")

    def generate_passenger(self):
        start = random.choice(list(STOP_POSITIONS.keys()))
        end = random.choice([i for i in STOP_POSITIONS.keys() if i != start])
        passenger = Passenger(self.passenger_id, start, end)
        self.stops[start].append(passenger)
        self.passenger_list.append(passenger)
        self.passenger_id += 1
        self.update_status()
        self.draw_route()
        self.root.after(PASSENGER_GENERATION_INTERVAL * 1000, self.generate_passenger)

    def move_bus(self):
        # Move the bus along the route
        current_stop, next_stop = ROUTE_CONNECTIONS[self.current_route_index]
        self.bus.current_stop = next_stop
        self.current_route_index = (self.current_route_index + 1) % len(ROUTE_CONNECTIONS)

        self.draw_route()
        self.draw_bus()

        # Board and deboard passengers
        for passenger in self.stops[self.bus.current_stop][:]:
            if self.bus.board_passenger(passenger):
                self.stops[self.bus.current_stop].remove(passenger)

        self.bus.deboard_passengers()
        self.update_status()

        self.root.after(STOP_WAIT_TIME * 1000, self.continue_movement)

    def continue_movement(self):
        self.root.after(BUS_MOVE_DELAY * 1000, self.move_bus)

    def draw_route(self):
        self.canvas.delete("all")
        # Draw the route as lines connecting stops
        for (stop1, stop2) in ROUTE_CONNECTIONS:
            x1, y1 = STOP_POSITIONS[stop1]
            x2, y2 = STOP_POSITIONS[stop2]
            self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

        # Draw stops as larger circles and passengers as smaller circles
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

    def draw_bus(self):
        # Draw the bus at the current stop
        x, y = STOP_POSITIONS[self.bus.current_stop]
        self.canvas.create_rectangle(x - 15, y - 15, x + 15, y + 15, fill="red")
