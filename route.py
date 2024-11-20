# route.py

# Define stop positions for Route 1
ROUTE_1_STOP_POSITIONS = {
    0: (100, 100),
    1: (200, 100),
    2: (300, 100),
    3: (400, 100),
    4: (500, 100),  # Intersection stop
    5: (600, 100),
    6: (700, 100),
    7: (800, 100),
}

# Define stop positions for Route 2
ROUTE_2_STOP_POSITIONS = {
    4: (500, 100),  # Intersection stop
    8: (500, 10),
    9: (500, 50),
    10: (500, 150),
    11: (500, 200),
    12: (500, 250),
    13: (500, 300),
    14: (500, 350),
    15: (500, 400),
}

# Combined STOP_POSITIONS for both routes
STOP_POSITIONS = {**ROUTE_1_STOP_POSITIONS, **ROUTE_2_STOP_POSITIONS}

# Define connections for Route 1
ROUTE_1_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0)  # Loop back to the start
]

# Define connections for Route 2
ROUTE_2_CONNECTIONS = [
    (8, 9), (9, 10), (10, 11), (11, 12), (12, 13), (13, 14), (14, 15), (15, 8)  # Loop back to the start
]

# Combined ROUTE_CONNECTIONS for simulation
ROUTE_CONNECTIONS = ROUTE_1_CONNECTIONS + ROUTE_2_CONNECTIONS

# Map stops to their respective routes (optional for easier lookup)
STOP_TO_ROUTE = {stop: 1 for stop in ROUTE_1_STOP_POSITIONS.keys()}  # Route 1
STOP_TO_ROUTE.update({stop: 2 for stop in ROUTE_2_STOP_POSITIONS.keys()})  # Route 2