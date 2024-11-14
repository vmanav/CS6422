# logic/simulation.py

from models.bus import Bus
from models.busStop import BusStop
from random import randint

class Simulation:
    def __init__(self, bus_capacity, num_stops):
        self.bus_capacity = bus_capacity
        self.stops = [BusStop(i) for i in range(num_stops)]
        self.buses = [Bus(capacity=bus_capacity, current_stop=0)]  

    def generate_passenger(self):
        start_stop = randint(0, len(self.stops) - 1)
        end_stop = randint(0, len(self.stops) - 1)
        if start_stop != end_stop:
            self.stops[start_stop].add_passenger_request(end_stop)
            print(f"Generated passenger from Stop {start_stop} to Stop {end_stop}")

    def manage_buses(self):
        for bus in self.buses:
            current_stop = self.stops[bus.current_stop]
        
            departing_passengers = [p for p in bus.passengers if p.end_stop == bus.current_stop]
            for passenger in departing_passengers:
                bus.remove_passenger(passenger)
            print(f"Bus at Stop {bus.current_stop}: Dropped off {len(departing_passengers)} passengers")

            # Board waiting passengers, if there's space on the bus
            boarding_passengers = []
            while len(bus.passengers) < bus.capacity and current_stop.waiting_passengers:
                passenger = current_stop.waiting_passengers.pop(0)
                if bus.add_passenger(passenger):  # Attempt to board
                    boarding_passengers.append(passenger)
            print(f"Bus at Stop {bus.current_stop}: Boarded {len(boarding_passengers)} passengers")
            
            # Move bus to next stop (wrap around if it reaches the last stop)
            bus.current_stop = (bus.current_stop + 1) % len(self.stops)