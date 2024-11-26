class Passenger:
    def __init__(self, id, start, end, intermediate_stop):
        self.id = id
        self.start = start
        self.end = end
        self.status = f"Waiting at Stop {start}"
        self.intermediate_stop = intermediate_stop
