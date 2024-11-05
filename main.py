# Main file for the Project

from models.bus import Bus

def main():
    b = Bus(c=10, stop=0)

    print("Bus Details")
    print("capacity :", b.c)
    print("capacity :", b.stop)

if __name__ == "__main__":
    main()