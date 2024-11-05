# Main file for the Project

from models.bus import Bus
from models.busStop import BusStop

def main():
    b = Bus(capacity=10, current_stop=0)
    busStop = BusStop(1)

    print("Bus Details")
    print("capacity :", b.capacity)
    print("capacity :", b.current_stop)

    print("Bus Stop Details")
    print("Stop id:", busStop.stop_id)
    print("Passengers waiting on stop:", busStop.waiting_passengers)

if __name__ == "__main__":
    main()