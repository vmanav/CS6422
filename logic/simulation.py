import tkinter as tk
from tkinter import ttk
from models.route import STOP_POSITIONS, ROUTE_CONNECTIONS
from models.passenger import Passenger
from models.bus import Bus
from ui.canvas_draw import draw_stops, draw_routes, draw_passengers, draw_buses
import random

PASSENGER_GENERATION_INTERVAL = 3 # seconds
BUS_MOVE_DELAY = 2  # seconds
STOP_RADIUS = 25  # Radius for stops


class BusSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Bus Simulation")

        # Main layout frames
        self.main_frame = tk.Frame(root, bg="#F5F5F5")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas for visualization (fully centered and resizable)
        self.canvas_frame = tk.Frame(self.main_frame, bg="#F5F5F5")
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=5)
        self.canvas = tk.Canvas(self.canvas_frame, bg="#FFFFFF")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Status frame for passenger and bus information
        self.status_frame = tk.Frame(self.main_frame, bg="#E0E0E0", height=150)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        # Passenger table using ttk.Treeview
        self.passenger_table = ttk.Treeview(
            self.status_frame,
            columns=("ID", "Status", "Start", "End", "Type"),
            show="headings",
            height=6,
        )
        self.passenger_table.heading("ID", text="Passenger ID")
        self.passenger_table.heading("Status", text="Status")
        self.passenger_table.heading("Start", text="Start Stop")
        self.passenger_table.heading("End", text="End Stop")
        self.passenger_table.heading("Type", text="Type")

        # Dynamically adjust column widths and center align text
        for col in ("ID", "Status", "Start", "End", "Type"):
            self.passenger_table.column(col, anchor="center", stretch=True)

        self.passenger_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Passenger count display
        self.passenger_count_label = tk.Label(
            self.status_frame,
            text="Passengers on Buses: ",
            bg="#E0E0E0",
            font=("Arial", 12, "bold"),
        )
        self.passenger_count_label.pack(pady=5)

        # Simulation data
        self.stops = {i: [] for i in STOP_POSITIONS.keys()}
        self.passenger_list = []
        self.passenger_id = 1

        # Initialize buses
        self.buses = [
            Bus(id=1, route=[0, 1, 2, 3, 4, 5, 6, 7], color="#FF6347", capacity=25),
            Bus(id=2, route=[3, 8, 9, 10], color="#4682B4", capacity=25),
        ]

        # Start simulation
        self.root.after(1000, self.generate_passenger)
        self.root.after(1000, self.move_buses)

    def update_status(self):
        """Update the passenger table and bus status."""
        # Clear the current table
        for row in self.passenger_table.get_children():
            self.passenger_table.delete(row)

        # Add passenger information to the table
        for p in self.passenger_list:
            self.passenger_table.insert(
                "",
                "end",
                values=(
                    p.id,
                    p.status,
                    p.start,
                    p.end,
                    "Transit" if p.is_transit else "Direct",
                ),
            )

        # Update the bus passenger counts
        passenger_counts = [len(bus.passengers) for bus in self.buses]
        counts_text = " | ".join(
            [f"Bus {bus.id}: {len(bus.passengers)} passengers" for bus in self.buses]
        )
        self.passenger_count_label.config(text=f"Passengers on Buses: {counts_text}")

    def generate_passenger(self):
        """Generate a new passenger."""
        start = random.choice(list(STOP_POSITIONS.keys()))
        end = random.choice([i for i in STOP_POSITIONS.keys() if i != start])

        # Determine if the passenger is a transit passenger
        is_transit = (
            (start in self.buses[0].route and end not in self.buses[0].route)
            or (start in self.buses[1].route and end not in self.buses[1].route)
        )

        passenger = Passenger(self.passenger_id, start, end, is_transit=is_transit)
        self.stops[start].append(passenger)
        self.passenger_list.append(passenger)
        self.passenger_id += 1
        self.update_status()
        self.draw_route()
        self.root.after(PASSENGER_GENERATION_INTERVAL * 1000, self.generate_passenger)

    def move_buses(self):
        """Move buses and handle passenger boarding/deboarding."""
        for bus in self.buses:
            bus.move()
            deboarded = bus.deboard_passengers()

            # Handle deboarded passengers
            for passenger in deboarded:
                if passenger.is_transit and passenger.current_leg == 2:
                    continue  # No re-adding, they've completed the trip
                if passenger.is_transit and passenger.current_leg == 1:
                    self.stops[passenger.intermediate_stop].append(passenger)
                else:
                    self.stops[passenger.end].append(passenger)

            # Handle boarding passengers
            for passenger in self.stops[bus.current_stop][:]:
                if bus.board_passenger(passenger):
                    self.stops[bus.current_stop].remove(passenger)

        self.update_status()
        self.draw_route()
        self.root.after(BUS_MOVE_DELAY * 1000, self.move_buses)

    def draw_route(self):
        """Draw the routes, stops, buses, and passengers."""
        self.canvas.delete("all")

        # Draw routes
        draw_routes(self.canvas, ROUTE_CONNECTIONS, STOP_POSITIONS, color="#FF6347")
        draw_routes(
            self.canvas, [(3, 8), (8, 9), (9, 10), (10, 3)], STOP_POSITIONS, color="#4682B4"
        )

        # Draw stops, passengers, and buses
        draw_stops(self.canvas, self.stops, STOP_POSITIONS, STOP_RADIUS)
        draw_passengers(self.canvas, self.stops, STOP_POSITIONS)
        draw_buses(self.canvas, self.buses, STOP_POSITIONS)
