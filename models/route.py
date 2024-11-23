# Define stop positions
STOP_POSITIONS = {
    0: (100, 200), 1: (200, 100), 2: (300, 50), 3: (400, 200),  # Intersection at Stop 3
    4: (500, 300), 5: (500, 400), 6: (400, 450), 7: (300, 400),
    8: (100, 300), 9: (200, 400), 10: (400, 50)  # Blue route stops
}

ROUTE_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0),  # Main route (Red)
    (3, 8), (8, 9), (9, 10), (10, 3)  # Secondary route (Blue)
]

INTERSECTION_STOP = 3  # Stop where buses intersect
