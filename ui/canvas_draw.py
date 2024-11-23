# canvas_draw.py (inside the ui directory)

def draw_stops(canvas, stops, stop_positions, stop_radius):
    for stop, (x, y) in stop_positions.items():
        canvas.create_oval(
            x - stop_radius, y - stop_radius, x + stop_radius, y + stop_radius,
            fill="#ADD8E6", outline="black", width=2
        )
        canvas.create_text(x, y, text=f"Stop {stop}", font=("Arial", 10, "bold"))


def draw_routes(canvas, route_connections, stop_positions, color="black"):
    for stop1, stop2 in route_connections:
        x1, y1 = stop_positions[stop1]
        x2, y2 = stop_positions[stop2]
        canvas.create_line(x1, y1, x2, y2, fill=color, width=3)


def draw_passengers(canvas, stops, stop_positions):
    for stop, passengers in stops.items():
        x, y = stop_positions[stop]
        for i, passenger in enumerate(passengers):
            offset = i * 10
            if passenger.is_transit:
                canvas.create_polygon(
                    x - 25 + offset, y - 40, x - 20 + offset, y - 50, x - 15 + offset, y - 40,
                    fill="yellow", outline="black"
                )
            else:
                canvas.create_oval(
                    x - 25 + offset, y - 40, x - 15 + offset, y - 30,
                    fill="orange", outline="black"
                )


def draw_buses(canvas, buses, stop_positions):
    for bus in buses:
        x, y = stop_positions[bus.current_stop]
        canvas.create_rectangle(
            x - 20, y - 20, x + 20, y + 20, fill=bus.color, outline="black", width=2
        )
        canvas.create_text(x, y, text=f"Bus {bus.id}", font=("Arial", 10, "bold"), fill="white")
