from route import ROUTE1_CONNECTIONS, ROUTE2_CONNECTIONS, STOP_POSITIONS
from config.constants import  PASSENGER_GENERATION_INTERVAL, BUS_MOVE_DELAY, STOP_WAIT_TIME, STOP_RADIUS, SMOOTH_MOVE_INTERVAL, STEPS_PER_ROUTE

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
                    self.root.after(1000, move_bus1_help(self))
                    self.helper_bus = True

            # Handle deboarding passengers
            [deboarding_passengers, transit_passengers] = bus.deboard_passengers()

            # Transfer logic for intersection stops
            for passenger in transit_passengers:
            # Update start stop to intersection stop for next bus
                passenger.start = end_stop
                passenger.intermediate_stop = None
                if passenger.end in {stop for conn in ROUTE2_CONNECTIONS for stop in conn}:
                    self.stops[end_stop].append(passenger)
                elif passenger.end in {stop for conn in ROUTE1_CONNECTIONS for stop in conn}:
                    self.stops[end_stop].append(passenger) 

            self.update_status()

            if bus.name == "B1":
                self.root.after(STOP_WAIT_TIME * 1000, move_bus1(self))
            elif bus.name == "BH":
                self.root.after(STOP_WAIT_TIME * 1000, move_bus1_help(self))
            elif bus.name == "B2":
                self.root.after(STOP_WAIT_TIME * 1000, move_bus2(self))

    step(0)

def move_bus1(self):
    current_stop, next_stop = ROUTE1_CONNECTIONS[self.route1_index]
    self.route1_index = (self.route1_index + 1) % len(ROUTE1_CONNECTIONS)
    print("Bus 1 CS: ", current_stop, ", NS: ", next_stop, "Cap: ", len(self.bus1.passengers))
    smooth_move_bus(self, self.bus1, current_stop, next_stop, "red")

def move_bus1_help(self):
    self.route1_help_index = self.route1_index-2
    current_stop, next_stop = ROUTE1_CONNECTIONS[self.route1_help_index]
    self.route1_help_index = (self.route1_help_index + 1) % len(ROUTE1_CONNECTIONS)
    print("Helper CS: ", current_stop, ", NS: ", next_stop, "Cap: ", len(self.bus1_help .passengers))
    smooth_move_bus(self, self.bus1_help, current_stop, next_stop, "red")

def move_bus2(self):
    current_stop, next_stop = ROUTE2_CONNECTIONS[self.route2_index]
    self.route2_index = (self.route2_index + 1) % len(ROUTE2_CONNECTIONS)
    smooth_move_bus(self, self.bus2, current_stop, next_stop, "blue")

def move_bus(self):
    current_stop, next_stop = ROUTE2_CONNECTIONS[self.route2_index]
    self.route2_index = (self.route2_index + 1) % len(ROUTE2_CONNECTIONS)
    smooth_move_bus(self, self.bus2, current_stop, next_stop, "blue")

