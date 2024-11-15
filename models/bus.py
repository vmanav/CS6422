# models/bus.py
from models.passenger import Passenger

class Bus:
    def __init__(self, capacity):
        self.capacity = capacity
        self.passengers = []
        self.current_stop = 0
    
    def board_passenger(self, passenger: Passenger) -> bool:
        if len(self.passengers) < self.capacity:
            passenger.status = "In Bus"
            self.passengers.append(passenger)
            return True
        return False

    def deboard_passengers(self) -> list:
        deboarded = [p for p in self.passengers if p.end == self.current_stop]
        for p in deboarded:
            p.status = f"Deboarded at Stop {self.current_stop}"
            self.passengers.remove(p)
        return deboarded