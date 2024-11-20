import tkinter as tk
from models.passenger import Passenger
from models.bus import Bus
from route import (
    ROUTE_1_CONNECTIONS,
    ROUTE_2_CONNECTIONS,
    STOP_POSITIONS,
    STOP_TO_ROUTE,
)
import random

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

        # Initialize buses for each route
        self.buses = {
            1: Bus(capacity=10),
            2: Bus(capacity=10),
        }

        # Stops and passengers for each route
        self.stops = {i: [] for i in STOP_POSITIONS.keys()}
        self.passenger_list = []
        self.passenger_id = 1

        # Current indices for each route
        self.current_route_indices = {
            1: 0,  # Route 1
            2: 0,  # Route 2
        }

        # Canvas for drawing the routes and buses
        self.canvas = tk.Canvas(root, width=1000, height=700, bg="white")
        self.canvas.pack()

        # Status panel container
        self.status_panel = tk.Frame(root)
        self.status_panel.pack(fill=tk.X, pady=5)

        # Passenger Status panel
        self.status_frame = tk.Frame(self.status_panel, bg="light gray", relief=tk.RAISED, bd=2)
        self.status_frame.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        self.status_label = tk.Label(self.status_frame, text="Passenger Status", anchor="w",
                                     bg="light gray", font=("Arial", 14, "bold"))
        self.status_label.pack(fill=tk.X, padx=10, pady=5)

        self.status_text = tk.Text(self.status_frame, height=10, width=50, bg="black", fg="white",
                                   font=("Arial", 12))
        self.status_text.pack(fill=tk.BOTH, padx=10, pady=5)

        # Passenger Count box
        self.passenger_count_frame = tk.Frame(self.status_panel, bg="light gray", relief=tk.RAISED, bd=2)
        self.passenger_count_frame.pack(side=tk.RIGHT, padx=10)

        self.passenger_count_inner_frame = tk.Frame(self.passenger_count_frame, bg="black", relief=tk.FLAT)
        self.passenger_count_inner_frame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        self.passenger_count_label = tk.Label(
            self.passenger_count_inner_frame, text="Passengers on Bus: 0", font=("Arial", 12), bg="black", fg="white"
        )
        self.passenger_count_label.pack(padx=10, pady=10)

        # Start simulation
        self.root.after(1000, self.generate_passenger)
        self.root.after(1000, self.move_bus, 1)
        self.root.after(1000, self.move_bus, 2)

    def update_status(self):
        # Update passenger details in the text box
        self.status_text.delete(1.0, tk.END)

        # Show passengers at stops
        self.status_text.insert(tk.END, "Passengers at Stops:\n")
        for p in self.passenger_list:
            self.status_text.insert(
                tk.END, f"Passenger {p.id}: {p.status} | Start: {p.start}, End: {p.end}\n"
            )

        # Update passenger count for both buses
        passenger_counts = ", ".join(
            f"Route {route}: {len(bus.passengers)}" for route, bus in self.buses.items()
        )
        self.passenger_count_label.config(text=f"Passengers on Buses: {passenger_counts}")

    def generate_passenger(self):
        # Generate a passenger with random start and end stops
        start = random.choice(list(STOP_POSITIONS.keys())[:-1])
        end = random.choice([i for i in STOP_POSITIONS.keys() if i > start])
        passenger = Passenger(self.passenger_id, start, end)
        self.stops[start].append(passenger)
        self.passenger_list.append(passenger)
        self.passenger_id += 1
        self.update_status()
        self.draw_route()
        self.root.after(PASSENGER_GENERATION_INTERVAL * 1000, self.generate_passenger)

    def move_bus(self, route):
        # Get the current connections and indices for the route
        connections = ROUTE_1_CONNECTIONS if route == 1 else ROUTE_2_CONNECTIONS
        current_index = self.current_route_indices[route]
        current_stop, next_stop = connections[current_index]
        self.current_route_indices[route] = (current_index + 1) % len(connections)

        self.smooth_move_bus(route, current_stop, next_stop)

    def continue_movement(self, route):
        self.root.after(BUS_MOVE_DELAY * 1000, self.move_bus, route)

    def draw_route(self):
        # Draw the routes and stops
        self.canvas.delete("all")
        for route, connections in enumerate([ROUTE_1_CONNECTIONS, ROUTE_2_CONNECTIONS], start=1):
            color = "blue" if route == 1 else "green"
            for (stop1, stop2) in connections:
                x1, y1 = STOP_POSITIONS[stop1]
                x2, y2 = STOP_POSITIONS[stop2]
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)

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

    def smooth_move_bus(self, route, start_stop, end_stop):
        x1, y1 = STOP_POSITIONS[start_stop]
        x2, y2 = STOP_POSITIONS[end_stop]
        dx = (x2 - x1) / STEPS_PER_ROUTE
        dy = (y2 - y1) / STEPS_PER_ROUTE

        def step(i):
            if i <= STEPS_PER_ROUTE:
                new_x = x1 + i * dx
                new_y = y1 + i * dy
                self.draw_route()
                color = "red" if route == 1 else "orange"
                self.canvas.create_rectangle(
                    new_x - 15, new_y - 15, new_x + 15, new_y + 15, fill=color
                )
                self.root.after(SMOOTH_MOVE_INTERVAL, lambda: step(i + 1))
            else:
                self.handle_stop_actions(route, end_stop)

        step(0)

    def handle_stop_actions(self, route, stop):
        bus = self.buses[route]

        # Handle boarding
        for passenger in self.stops[stop][:]:
            if STOP_TO_ROUTE[passenger.end] != route and stop == 4:  # Intersection logic
                passenger.start = stop  # Update start for transfer
                passenger.status = "Waiting for transfer"
            elif STOP_TO_ROUTE[passenger.end] == route:
                if bus.board_passenger(passenger):
                    self.stops[stop].remove(passenger)

        # Handle deboarding
        bus.deboard_passengers()

        self.update_status()
        self.root.after(STOP_WAIT_TIME * 1000, self.continue_movement, route)