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
        self.route.rotate(-1)
        self.current_stop = self.route[0]

    def board_passenger(self, passenger):
        if len(self.passengers) < self.capacity:
            self.passengers.append(passenger)
            passenger.status = f"On Bus {self.id}"
            return True
        return False

    def deboard_passengers(self):
        deboarded = []
        for passenger in self.passengers[:]:
            if (passenger.is_transit and passenger.current_leg == 1 and passenger.intermediate_stop == self.current_stop) or \
               (not passenger.is_transit and passenger.end == self.current_stop) or \
               (passenger.is_transit and passenger.current_leg == 2 and passenger.end == self.current_stop):
                self.passengers.remove(passenger)
                passenger.status = f"Deboarded at Stop {self.current_stop}"
                if passenger.is_transit:
                    passenger.current_leg += 1
                deboarded.append(passenger)
        return deboarded
