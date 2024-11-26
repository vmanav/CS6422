class Bus:
    def __init__(self, capacity):
        self.capacity = capacity
        self.passengers = []  # List of passengers on the bus
        self.current_stop = None  # Current stop of the bus

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
            p for p in self.passengers if p.end != self.current_stop
        ]
        for passenger in deboarded_passengers:
            passenger.status = "Deboarded"

        for passenger in transit_passengers:
            passenger.status = "Debaorded at Intersection stop"
            
        return [deboarded_passengers, transit_passengers];
