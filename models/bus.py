# Represents a Bus in the System
class Bus:
    def __init__(self, capacity, current_stop=0):
        self.capacity = capacity
        self.current_stop = current_stop
        self.passengers = []

    def add_passenger(self, passenger):
        if len(self.passengers) < self.capacity:
            passenger.in_bus = True
            passenger.current_bus = self
            self.passengers.append(passenger)
            return True
        return False

    def remove_passenger(self, passenger):
        if passenger in self.passengers:
            self.passengers.remove(passenger)
            passenger.in_bus = False
            passenger.current_bus = None
