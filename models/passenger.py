class Passenger:
    def __init__(self, id, start, end):
        self.id = id
        self.start = start
        self.end = end
        self.status = f"Waiting at Stop {start}"
