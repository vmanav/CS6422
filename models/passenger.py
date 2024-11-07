class Passenger:
    def __init__(self, start_stop, end_stop):
        self.start_stop = start_stop
        self.end_stop = end_stop
        self.in_bus = False
        self.current_bus = None