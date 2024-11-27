class Bus:
    def __init__(self, capacity, name):
        self.capacity = capacity
        self.passengers = []  # List of passengers on the bus
        self.current_stop = None  # Current stop of the bus
        self.name = name

    def board_passenger(self, passenger):
        """
        Boards a passenger onto the bus if there's space available.
        Returns True if the passenger was successfully boarded.
        """
        if len(self.passengers) < self.capacity:
            passenger.status = f"On Bus and Intermediate Stop = {passenger.intermediate_stop}" 
            self.passengers.append(passenger)
            return True
        return False

    def deboard_passengers(self):
        """
        Deboards all passengers whose destination matches the current stop.
        Returns a list of deboarded passengers.
        """
        deboarded_passengers = [
            p for p in self.passengers if p.end == self.current_stop
        ]

        transit_passengers = [
            p for p in self.passengers if p.intermediate_stop == self.current_stop
        ]
        # transit_passengers = []
        # for passenger in self.passengers:
        #     if(passenger.intermediate_stop):
        #         transit_passengers = [
        #             p for p in self.passengers if p.intermediate_stop == self.current_stop
        #         ]
        # Remove these passengers from the bus
        self.passengers = [
            p for p in self.passengers if p.end != self.current_stop and p.intermediate_stop != self.current_stop
        ]
        # print("Passengers on bus: ", str(self.passengers))

        for passenger in deboarded_passengers:
            passenger.status = "Deboarded"
            print("Deboarded passenger - ", passenger.id)

        for passenger in transit_passengers:
            passenger.status = "Debaorded at Intersection stop"
            print("Deboarded passenger at intersection - ", passenger.id)
            
        return [deboarded_passengers, transit_passengers]
