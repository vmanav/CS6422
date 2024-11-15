# models/passenger.py
class Passenger:
    def __init__(self, id: int, start: int, end: int):
        self.id = id
        self.start = start
        self.end = end
        self.status = f"Waiting at Stop {start}"