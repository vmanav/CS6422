import tkinter as tk
from models.passenger import Passenger
from models.bus import Bus
from route import ROUTE_1_CONNECTIONS, ROUTE_2_CONNECTIONS, ROUTE_1_STOP_POSITIONS, ROUTE_2_STOP_POSITIONS
import random

PASSENGER_GENERATION_INTERVAL = 2  # seconds
BUS_MOVE_DELAY = 2  # seconds
STOP_WAIT_TIME = 2  # seconds
STOP_RADIUS = 25  # Radius for larger stops

class BusSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Bus Simulation")

        # Create buses for both routes
        self.bus1 = Bus(capacity=10)
        self.bus2 = Bus(capacity=10)
        
        # Track stops for both routes
        self.stops_route_1 = {i: [] for i in ROUTE_1_STOP_POSITIONS.keys()}
        self.stops_route_2 = {i: [] for i in ROUTE_2_STOP_POSITIONS.keys()}
        self.passenger_list = []
        self.passenger_id = 1

        self.current_route_1_index = 0
        self.current_route_2_index = 0

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
        start = random.choice(list(ROUTE_1_STOP_POSITIONS.keys()) + list(ROUTE_2_STOP_POSITIONS.keys()))
        end = random.choice([i for i in list(ROUTE_1_STOP_POSITIONS.keys()) + list(ROUTE_2_STOP_POSITIONS.keys()) if i != start])
        passenger = Passenger(self.passenger_id, start, end)

        if start in ROUTE_1_STOP_POSITIONS:
            self.stops_route_1[start].append(passenger)
        else:
            self.stops_route_2[start].append(passenger)

        self.passenger_list.append(passenger)
        self.passenger_id += 1
        self.update_status()
        self.draw_route()
        self.root.after(PASSENGER_GENERATION_INTERVAL * 1000, self.generate_passenger)

    def move_bus(self):
        # Move bus 1 along Route 1
        if self.current_route_1_index < len(ROUTE_1_CONNECTIONS):
            current_stop, next_stop = ROUTE_1_CONNECTIONS[self.current_route_1_index]
            self.bus1.current_stop = next_stop
            self.current_route_1_index += 1
            if self.current_route_1_index == len(ROUTE_1_CONNECTIONS):
                self.current_route_1_index = 0

            self.handle_passengers(self.bus1, self.stops_route_1, ROUTE_1_STOP_POSITIONS)

        # Move bus 2 along Route 2
        if self.current_route_2_index < len(ROUTE_2_CONNECTIONS):
            current_stop, next_stop = ROUTE_2_CONNECTIONS[self.current_route_2_index]
            self.bus2.current_stop = next_stop
            self.current_route_2_index += 1
            if self.current_route_2_index == len(ROUTE_2_CONNECTIONS):
                self.current_route_2_index = 0

            self.handle_passengers(self.bus2, self.stops_route_2, ROUTE_2_STOP_POSITIONS)

        self.draw_route()
        self.draw_bus()
        self.update_status()

        self.root.after(STOP_WAIT_TIME * 1000, self.continue_movement)

    def handle_passengers(self, bus, stops, stop_positions):
        for passenger in stops[bus.current_stop][:]:
            if bus.board_passenger(passenger):
                stops[bus.current_stop].remove(passenger)

        bus.deboard_passengers()

        # Handle passenger intersection logic (route 1 -> route 2 at stop 4)
        if bus == self.bus1:  # Route 1 bus
            for passenger in self.stops_route_1[4]:  # Intersection stop
                if passenger.end in ROUTE_2_STOP_POSITIONS:
                    # Passenger moves to Route 2
                    passenger.start = 4  # Re-update the start stop to the intersection
                    self.stops_route_2[4].append(passenger)  # Add to Route 2 at the intersection

                    # Remove from Route 1
                    self.stops_route_1[4].remove(passenger)

        elif bus == self.bus2:  # Route 2 bus
            for passenger in self.stops_route_2[4]:  # Intersection stop
                if passenger.end in ROUTE_1_STOP_POSITIONS:
                    # Passenger moves to Route 1
                    passenger.start = 4  # Re-update the start stop to the intersection
                    self.stops_route_1[4].append(passenger)  # Add to Route 1 at the intersection

                    # Remove from Route 2
                    self.stops_route_2[4].remove(passenger)

    def continue_movement(self):
        self.root.after(BUS_MOVE_DELAY * 1000, self.move_bus)

    def draw_route(self):
        self.canvas.delete("all")

        # Draw Route 1
        for (stop1, stop2) in ROUTE_1_CONNECTIONS:
            x1, y1 = ROUTE_1_STOP_POSITIONS[stop1]
            x2, y2 = ROUTE_1_STOP_POSITIONS[stop2]
            self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=2)

        # Draw Route 2
        for (stop1, stop2) in ROUTE_2_CONNECTIONS:
            x1, y1 = ROUTE_2_STOP_POSITIONS[stop1]
            x2, y2 = ROUTE_2_STOP_POSITIONS[stop2]
            self.canvas.create_line(x1, y1, x2, y2, fill="green", width=2)

        # Draw stops for Route 1
        for stop, (x, y) in ROUTE_1_STOP_POSITIONS.items():
            self.canvas.create_oval(x - STOP_RADIUS, y - STOP_RADIUS, x + STOP_RADIUS, y + STOP_RADIUS, fill="light blue")
            self.canvas.create_text(x, y, text=f"Stop {stop}")

        # Draw stops for Route 2
        for stop, (x, y) in ROUTE_2_STOP_POSITIONS.items():
            self.canvas.create_oval(x - STOP_RADIUS, y - STOP_RADIUS, x + STOP_RADIUS, y + STOP_RADIUS, fill="light green")
            self.canvas.create_text(x, y, text=f"Stop {stop}")

    def draw_bus(self):
        # Draw bus 1
        x, y = ROUTE_1_STOP_POSITIONS[self.bus1.current_stop]
        self.canvas.create_rectangle(x - 15, y - 15, x + 15, y + 15, fill="red")

        # Draw bus 2
        x, y = ROUTE_2_STOP_POSITIONS[self.bus2.current_stop]
        self.canvas.create_rectangle(x - 15, y - 15, x + 15, y + 15, fill="yellow")