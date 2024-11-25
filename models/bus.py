from collections import deque

class Bus:
    def __init__(self, id, route, color, capacity=10):
        self.id = id
        self.route = deque(route)
        self.color = color
        self.capacity = capacity
        self.passengers = []
        self.current_stop = self.route[0]

    def move(self):
        """Move the bus to the next stop in its route."""
        self.route.rotate(-1)
        self.current_stop = self.route[0]

    def board_passenger(self, passenger):
        """Board a passenger if capacity allows."""
        if len(self.passengers) < self.capacity:
            self.passengers.append(passenger)
            passenger.status = f"On Bus {self.id}"
            return True
        return False

    def deboard_passengers(self):
        """Deboard passengers at the current stop."""
        deboarded = []  # Track all passengers deboarded at this stop

        for passenger in self.passengers[:]:  # Work on a copy of the passenger list
            # Direct passengers deboard at their final stop
            if not passenger.is_transit and passenger.end == self.current_stop:
                self.passengers.remove(passenger)  # Remove from bus
                passenger.status = f"Deboarded at Stop {self.current_stop}"  # Update status
                deboarded.append(passenger)  # Add to deboarded list
                print(f"Passenger {passenger.id} deboarded at Stop {self.current_stop} (Direct)")

            # Transit passengers deboard at intermediate or final stop
            elif passenger.is_transit:
                # Check if at intermediate stop (Leg 1)
                if passenger.current_leg == 1 and passenger.intermediate_stop == self.current_stop:
                    self.passengers.remove(passenger)  # Remove from bus
                    passenger.status = f"Deboarded at Stop {self.current_stop} (Transit - Leg 1)"
                    passenger.current_leg = 2  # Progress to the next leg
                    deboarded.append(passenger)  # Add to deboarded list
                    print(f"Passenger {passenger.id} deboarded at Stop {self.current_stop} (Intermediate Transit)")

                # Check if at final stop (Leg 2)
                elif passenger.current_leg == 2 and passenger.end == self.current_stop:
                    self.passengers.remove(passenger)  # Remove from bus
                    passenger.status = f"Deboarded at Stop {self.current_stop} (Final Transit Stop)"
                    deboarded.append(passenger)  # Add to deboarded list
                    print(f"Passenger {passenger.id} deboarded at Stop {self.current_stop} (Final Transit)")

        return deboarded  # Return the list of deboarded passengers
