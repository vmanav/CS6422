# Main file for the Project

from models.bus import Bus

def main():
    b = Bus(capacity=10, current_stop=0)

    print("Bus Details")
    print("capacity :", b.capacity)
    print("capacity :", b.current_stop)

if __name__ == "__main__":
    main()