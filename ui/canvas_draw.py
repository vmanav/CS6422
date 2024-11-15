# ui/canvas_draw.py
import math
import tkinter as tk

def draw_stops(canvas, stops, stop_coords):
    canvas.delete("all")
    for i, (x, y) in enumerate(stop_coords):
        canvas.create_oval(x-15, y-15, x+15, y+15, fill="light blue")
        canvas.create_text(x, y, text=f"Stop {i}")
        
        for j, passenger in enumerate(stops[i]):
            canvas.create_oval(x - 25 + j * 10, y - 30, x - 15 + j * 10, y - 20, fill="orange")

def draw_route(canvas, stop_coords):
    for i in range(len(stop_coords)):
        x1, y1 = stop_coords[i]
        x2, y2 = stop_coords[(i + 1) % len(stop_coords)]
        canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

def draw_bus(canvas, stop_coords, current_stop):
    x, y = stop_coords[current_stop]
    canvas.create_rectangle(x-10, y-10, x+10, y+10, fill="red")