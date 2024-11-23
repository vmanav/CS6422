from models.route import INTERSECTION_STOP

class Passenger:
    def __init__(self, id, start, end, is_transit=False):
        self.id = id
        self.start = start
        self.end = end
        self.status = "Waiting at Stop"
        self.is_transit = is_transit  # Flag for transit passengers
        self.current_leg = 1  # Track which leg of the journey (1 or 2)
        self.intermediate_stop = INTERSECTION_STOP if is_transit else None
