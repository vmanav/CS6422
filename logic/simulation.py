# simulation/simulation.py
import tkinter as tk
import random
import math
from models.bus import Bus
from models.passenger import Passenger
from ui.canvas_draw import draw_stops, draw_route, draw_bus

class BusSimulation:
    def __init__(self, root, stop_count=6, bus_capacity=10, stop_wait_time=2):
        self.root = root
        self.stop_count = stop_count
        self.stop_wait_time = stop_wait_time
        self.bus = Bus(bus_capacity)
        self.stops = [[] for _ in range(stop_count)]
        self.passenger_list = []
        self.passenger_id = 1
        self.center_x, self.center_y, self.radius = 300, 200, 150
        self.angle_gap = 360 / stop_count
        self.stop_coords = [(self.center_x + self.radius * math.cos(math.radians(self.angle_gap * i)),
                             self.center_y + self.radius * math.sin(math.radians(self.angle_gap * i))) 
                            for i in range(stop_count)]
        
        # Canvas and UI elements
        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()
        
        # Passenger status display
        self.status_frame = tk.Frame(root)
        self.status_frame.pack()
        self.status_text = tk.Text(self.status_frame, height=10, width=70)
        self.status_text.pack()
        
        # Start simulation
        self.root.after(1000, self.generate_passenger)
        self.root.after(1000, self.move_bus)

    def generate_passenger(self):
        start = random.randint(0, self.stop_count - 1)
        end = random.choice([i for i in range(self.stop_count) if i != start])
        passenger = Passenger(self.passenger_id, start, end)
        self.stops[start].append(passenger)
        self.passenger_list.append(passenger)
        self.passenger_id += 1
        self.update_status()
        draw_stops(self.canvas, self.stops, self.stop_coords)
        draw_route(self.canvas, self.stop_coords)
        self.root.after(1000, self.generate_passenger)

    def move_bus(self):
        self.bus.current_stop = (self.bus.current_stop + 1) % self.stop_count
        draw_bus(self.canvas, self.stop_coords, self.bus.current_stop)

        # Board and deboard passengers
        for passenger in self.stops[self.bus.current_stop][:]:
            if self.bus.board_passenger(passenger):
                self.stops[self.bus.current_stop].remove(passenger)
        
        self.bus.deboard_passengers()
        self.update_status()
        
        # Wait before moving to the next stop
        self.root.after(self.stop_wait_time * 1000, self.move_bus)

    def update_status(self):
        self.status_text.delete(1.0, tk.END)
        for p in self.passenger_list:
            self.status_text.insert(tk.END, f"Passenger {p.id}: {p.status} | Start: {p.start}, End: {p.end}\n")