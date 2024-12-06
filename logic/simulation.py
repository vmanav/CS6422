import tkinter as tk
from models.passenger import Passenger
from models.bus import Bus
import random

from route import ROUTE1_CONNECTIONS, ROUTE2_CONNECTIONS, STOP_POSITIONS

PASSENGER_GENERATION_INTERVAL = 1  # seconds
BUS_MOVE_DELAY = 2  # seconds
STOP_WAIT_TIME = 2  # seconds
STOP_RADIUS = 25  # Radius for larger stops
SMOOTH_MOVE_INTERVAL = 50  # milliseconds
STEPS_PER_ROUTE = 20  # Number of steps between stops for smooth movement


class BusSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Bus Simulation")

        self.bus1 = Bus(capacity=15, name="B1")  # Bus for Route 1
        self.bus2 = Bus(capacity=30, name="B2")  # Bus for Route 2
        self.bus1_help = Bus(capacity=30, name="BH")  # Bus for Route 1

        self.stops = {i: [] for i in STOP_POSITIONS.keys()}
        self.passenger_list = []
        self.passenger_id = 1

        # Track the routes
        self.route1_index = 0
        self.route1_help_index = 0
        self.route2_index = 0
        self.helper_bus = False

        # Canvas for drawing the routes and buses
        self.canvas = tk.Canvas(root, width=900, height=500, bg="white")
        self.canvas.pack()

        # Status panel container
        self.status_panel = tk.Frame(root)
        self.status_panel.pack(fill=tk.X, pady=5)

        # Passenger Status
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
        self.root.after(1000, self.move_bus1)
        self.root.after(1000, self.move_bus2)

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

    def move_bus1(self):
        current_stop, next_stop = ROUTE1_CONNECTIONS[self.route1_index]
        self.route1_index = (self.route1_index + 1) % len(ROUTE1_CONNECTIONS)
        print("Bus 1 CS: ", current_stop, ", NS: ", next_stop, "Cap: ", len(self.bus1.passengers))
        self.smooth_move_bus(self.bus1, current_stop, next_stop, "red")

    def move_bus1_help(self):
        self.route1_help_index = self.route1_index-2
        current_stop, next_stop = ROUTE1_CONNECTIONS[self.route1_help_index]
        self.route1_help_index = (self.route1_help_index + 1) % len(ROUTE1_CONNECTIONS)
        print("Helper CS: ", current_stop, ", NS: ", next_stop, "Cap: ", len(self.bus1_help .passengers))
        self.smooth_move_bus(self.bus1_help, current_stop, next_stop, "red")

    def move_bus2(self):
        current_stop, next_stop = ROUTE2_CONNECTIONS[self.route2_index]
        self.route2_index = (self.route2_index + 1) % len(ROUTE2_CONNECTIONS)
        self.smooth_move_bus(self.bus2, current_stop, next_stop, "blue")

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

    def smooth_move_bus(self, bus, start_stop, end_stop, color):
        x1, y1 = STOP_POSITIONS[start_stop]
        x2, y2 = STOP_POSITIONS[end_stop]
        dx = (x2 - x1) / STEPS_PER_ROUTE
        dy = (y2 - y1) / STEPS_PER_ROUTE

        bus_tag = f"bus_{color}"

        def step(i):
            if i <= STEPS_PER_ROUTE:
                new_x = x1 + i * dx
                new_y = y1 + i * dy
                self.canvas.delete(bus_tag)
                self.canvas.create_rectangle(
                    new_x - 15, new_y - 15, new_x + 15, new_y + 15,
                    fill=color, outline="black", tags=bus_tag
                )
                self.root.after(SMOOTH_MOVE_INTERVAL, lambda: step(i + 1))
            else:
                bus.current_stop = end_stop

                # Handle boarding passengers
                for passenger in self.stops[end_stop][:]:
                    if bus.board_passenger(passenger):
                        self.stops[end_stop].remove(passenger)
                        print("Boarded passenger: ", passenger.id)
                    elif self.helper_bus == False and color =="red":
                        print("Adding new bus")
                        print(self.helper_bus)
                        self.root.after(1000, self.move_bus1_help)
                        self.helper_bus = True

                # Handle deboarding passengers
                [deboarding_passengers, transit_passengers] = bus.deboard_passengers()

                

                # Transfer logic for intersection stops
                for passenger in transit_passengers:
                    # if passenger.intermediate_stop == end_stop:
                        # Update start stop to intersection stop for next bus
                    passenger.start = end_stop
                    passenger.intermediate_stop = None
                    # self.stops[end_stop].append(passenger)
                        #Determine which route's bus the passenger should board
                    if passenger.end in {stop for conn in ROUTE2_CONNECTIONS for stop in conn}:
                        self.stops[end_stop].append(passenger)
                    elif passenger.end in {stop for conn in ROUTE1_CONNECTIONS for stop in conn}:
                        self.stops[end_stop].append(passenger) 

                self.update_status()

                if bus.name == "B1":
                    self.root.after(STOP_WAIT_TIME * 1000, self.move_bus1)
                elif bus.name == "BH":
                    self.root.after(STOP_WAIT_TIME * 1000, self.move_bus1_help)
                elif bus.name == "B2":
                    self.root.after(STOP_WAIT_TIME * 1000, self.move_bus2)


                # self.root.after(
                #     STOP_WAIT_TIME * 1000,
                #     self.move_bus1 if color == "red" else self.move_bus2
                # )

                # if self.helper_bus == True and color == "red":
                #     self.root.after(STOP_WAIT_TIME * 1000, self.move_bus1_help)

        step(0)


if __name__ == "__main__":
    root = tk.Tk()
    simulation = BusSimulation(root)
    root.mainloop()
