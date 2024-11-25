import tkinter as tk
from tkinter import ttk
from models.route import STOP_POSITIONS, ROUTE_CONNECTIONS
from models.passenger import Passenger
from models.bus import Bus
from ui.canvas_draw import draw_stops, draw_routes, draw_passengers, draw_buses
import random

PASSENGER_GENERATION_INTERVAL = 3 # seconds
BUS_MOVE_DELAY = 5  # seconds
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

    def move_buses(self):
        """Move buses and handle passenger boarding/deboarding."""
        for bus in self.buses:
            # Move the bus to the next stop
            bus.move()
            print(f"Bus {bus.id} moved to Stop {bus.current_stop}")

            # Handle deboarding passengers
            deboarded = bus.deboard_passengers()
            for passenger in deboarded:
                # If the passenger has completed their journey, skip adding back to the stop
                if not passenger.is_transit or (passenger.is_transit and passenger.current_leg == 2):
                    continue  # Do nothing for passengers completing their journey

                # Transit passengers waiting for the next bus
                if passenger not in self.stops[bus.current_stop]:
                    self.stops[bus.current_stop].append(passenger)

            # Handle boarding passengers
            for passenger in self.stops[bus.current_stop][:]:  # Work on a copy of the stop list
                if bus.board_passenger(passenger):
                    self.stops[bus.current_stop].remove(passenger)
                    print(f"Passenger {passenger.id} boarded Bus {bus.id} at Stop {bus.current_stop}")

        # Update GUI and terminal
        self.update_status()
        self.draw_route()

        # Schedule the next iteration
        self.root.after(BUS_MOVE_DELAY * 1000, self.move_buses)


    def update_status(self):
            """Update the passenger table in the GUI and provide detailed simulation status in the terminal."""
            # Clear the current table
            for row in self.passenger_table.get_children():
                self.passenger_table.delete(row)

            # Update the passenger table in the GUI
            for passenger in self.passenger_list:
                self.passenger_table.insert(
                    "",
                    "end",
                    values=(
                        passenger.id,
                        passenger.status,
                        passenger.start,
                        passenger.end,
                        "Transit" if passenger.is_transit else "Direct",
                    ),
                )

            # Terminal log for bus and passenger statuses
            terminal_log = []

            for bus in self.buses:
                onboard = bus.passengers
                deboarding = [
                    p for p in bus.passengers
                    if (not p.is_transit and p.end == bus.current_stop)
                    or (p.is_transit and p.current_leg == 1 and p.intermediate_stop == bus.current_stop)
                    or (p.is_transit and p.current_leg == 2 and p.end == bus.current_stop)
                ]
                transit = [p for p in onboard if p.is_transit]

                # Add Bus status
                terminal_log.append(f"--- Bus {bus.id} ---")
                terminal_log.append(f"  Current Stop: {bus.current_stop}")
                terminal_log.append(f"  Passengers On Board: {len(bus.passengers)}/{bus.capacity}")
                
                # Onboard passengers
                for passenger in onboard:
                    terminal_log.append(
                        f"    Passenger {passenger.id}: On Bus {bus.id} | Start: {passenger.start} | End: {passenger.end} | {'Transit' if passenger.is_transit else 'Direct'}"
                    )
                
                # Deboarding passengers
                if deboarding:
                    terminal_log.append("  Deboarding Passengers:")
                    for passenger in deboarding:
                        terminal_log.append(
                            f"    Passenger {passenger.id}: Deboarding at Stop {bus.current_stop} | Final Stop: {passenger.end}"
                        )
                else:
                    terminal_log.append("  Deboarding Passengers: None")

                # Transit passengers
                if transit:
                    terminal_log.append("  Transit Passengers:")
                    for passenger in transit:
                        if passenger.current_leg == 1:
                            terminal_log.append(
                                f"    Passenger {passenger.id}: In Transit to Stop {passenger.intermediate_stop} | Final Stop: {passenger.end}"
                            )
                        elif passenger.current_leg == 2:
                            terminal_log.append(
                                f"    Passenger {passenger.id}: In Transit to Final Stop: {passenger.end}"
                            )
                else:
                    terminal_log.append("  Transit Passengers: None")
                
                terminal_log.append("")  # Add spacing between buses

            # Print the detailed log to the terminal
            print("\n=== Simulation Status ===")
            print("\n".join(terminal_log))
            print("=========================")


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
