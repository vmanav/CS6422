import tkinter as tk
from models.passenger import Passenger
from models.bus import Bus
from route import ROUTE_CONNECTIONS, STOP_POSITIONS
import random

PASSENGER_GENERATION_INTERVAL = 2  # seconds
BUS_MOVE_DELAY = 2  # seconds
STOP_WAIT_TIME = 2  # seconds
STOP_RADIUS = 25  # Radius for larger stops
SMOOTH_MOVE_INTERVAL = 50  # milliseconds
STEPS_PER_ROUTE = 20       # Number of steps between stops for smooth movement

class BusSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Bus Simulation")

        self.bus = Bus(capacity=10)
        self.stops = {i: [] for i in STOP_POSITIONS.keys()}
        self.passenger_list = []
        self.passenger_id = 1
        self.current_route_index = 0

        # Canvas for drawing the route and bus
        self.canvas = tk.Canvas(root, width=900, height=500, bg='white')
        self.canvas.pack()

        # Status panel container (horizontal alignment)
        self.status_panel = tk.Frame(root)
        self.status_panel.pack(fill=tk.X, pady=5)  # Horizontal alignment with padding

        # Left: Passenger Status panel
        # Left: Passenger Status panel
        self.status_frame = tk.Frame(self.status_panel, bg="light gray", relief=tk.RAISED, bd=2)
        self.status_frame.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        # Increased font size for the Passenger Status label
        self.status_label = tk.Label(self.status_frame, text="Passenger Status", anchor="w", 
                                    bg="light gray", font=("Arial", 14, "bold"))
        self.status_label.pack(fill=tk.X, padx=10, pady=5)

        # Increased font size for the Passenger Status text
        self.status_text = tk.Text(self.status_frame, height=10, width=50, bg="black", fg="white", 
                                font=("Arial", 12))
        self.status_text.pack(fill=tk.BOTH, padx=10, pady=5)


        # Right: Passenger Count box
        self.passenger_count_frame = tk.Frame(self.status_panel, bg="light gray", relief=tk.RAISED, bd=2)
        self.passenger_count_frame.pack(side=tk.RIGHT, padx=10)

        # Inner rectangle for Passenger Count
        self.passenger_count_inner_frame = tk.Frame(self.passenger_count_frame, bg="black", relief=tk.FLAT)
        self.passenger_count_inner_frame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        self.passenger_count_label = tk.Label(
            self.passenger_count_inner_frame, text="Passengers on Bus: 0", font=("Arial", 12), bg="black", fg="white"
        )
        self.passenger_count_label.pack(padx=10, pady=10)

        # Start simulation
        self.root.after(1000, self.generate_passenger)
        self.root.after(1000, self.move_bus)

    def update_status(self):
        # Update passenger details in the text box
        self.status_text.delete(1.0, tk.END)

        # Show passengers at stops
        self.status_text.insert(tk.END, "Passengers at Stops:\n")
        for p in self.passenger_list:
            self.status_text.insert(
                tk.END, f"Passenger {p.id}: {p.status} | Start: {p.start}, End: {p.end}\n"
            )

        # Update passenger count on bus
        self.passenger_count_label.config(
            text=f"Passengers on Bus: {len(self.bus.passengers)}"
        )

    def generate_passenger(self):
        # Generate a passenger with random start and end stops
        start = random.choice(list(STOP_POSITIONS.keys())[:-1])  # Exclude the last stop
        end = random.choice([i for i in STOP_POSITIONS.keys() if i > start])  # Ensure end > start
        passenger = Passenger(self.passenger_id, start, end)
        self.stops[start].append(passenger)
        self.passenger_list.append(passenger)
        self.passenger_id += 1
        self.update_status()
        self.draw_route()
        self.root.after(PASSENGER_GENERATION_INTERVAL * 1000, self.generate_passenger)

    def move_bus(self):
        current_stop, next_stop = ROUTE_CONNECTIONS[self.current_route_index]
        self.current_route_index = (self.current_route_index + 1) % len(ROUTE_CONNECTIONS)  # Update route index
        
        self.smooth_move_bus(current_stop, next_stop)
     

    def continue_movement(self):
        self.root.after(BUS_MOVE_DELAY * 1000, self.move_bus)

    def draw_route(self):
        # Draw the route and stops
        self.canvas.delete("all")
        for (stop1, stop2) in ROUTE_CONNECTIONS:
            x1, y1 = STOP_POSITIONS[stop1]
            x2, y2 = STOP_POSITIONS[stop2]
            self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

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

    def smooth_move_bus(self, start_stop, end_stop):
    # If the route is resetting from Stop 7 to Stop 0, skip animation
        if start_stop == 7 and end_stop == 0:
            # Directly reset the bus position to Stop 0
            self.bus.current_stop = 0
            self.draw_route()
            self.canvas.create_rectangle(
                STOP_POSITIONS[0][0] - 15, STOP_POSITIONS[0][1] - 15,
                STOP_POSITIONS[0][0] + 15, STOP_POSITIONS[0][1] + 15,
                fill="red"
            )

            # Handle boarding and deboarding at Stop 0
            for passenger in self.stops[0][:]:
                if self.bus.board_passenger(passenger):
                    self.stops[0].remove(passenger)

            self.bus.deboard_passengers()
            self.update_status()

            print(f"Bus has reset to Stop 0. Number of passengers onboard: {len(self.bus.passengers)}/{self.bus.capacity}")

            # Wait before continuing to the next stop
            self.root.after(STOP_WAIT_TIME * 1000, self.move_bus)
            return

        # Regular animation for other stops
        x1, y1 = STOP_POSITIONS[start_stop]
        x2, y2 = STOP_POSITIONS[end_stop]
        dx = (x2 - x1) / STEPS_PER_ROUTE
        dy = (y2 - y1) / STEPS_PER_ROUTE

        def step(i):
            if i <= STEPS_PER_ROUTE:
                new_x = x1 + i * dx
                new_y = y1 + i * dy

                self.draw_route()
                self.canvas.create_rectangle(
                    new_x - 15, new_y - 15, new_x + 15, new_y + 15, fill="red"
                )

                self.root.after(SMOOTH_MOVE_INTERVAL, lambda: step(i + 1))
            else:
                self.bus.current_stop = end_stop

                for passenger in self.stops[end_stop][:]:
                    if self.bus.board_passenger(passenger):
                        self.stops[end_stop].remove(passenger)

                self.bus.deboard_passengers()

                self.update_status()
                print(f"Bus is at Stop {self.bus.current_stop}. Number of passengers onboard: {len(self.bus.passengers)}/{self.bus.capacity}")

                self.root.after(STOP_WAIT_TIME * 1000, self.move_bus)

        step(0)
