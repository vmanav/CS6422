class Passenger:
    def __init__(self, id, start, end):
        self.id = id
        self.start = start
        self.end = end
        self.intermediate_stop = None
        self.status = f"Waiting at Stop {start}"

    def __repr__(self):
        # Provide a meaningful representation of the object
        return (f"Passenger id={self.id}")
