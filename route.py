# Define two intersecting routes
ROUTE1_CONNECTIONS = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7,0)]
ROUTE2_CONNECTIONS = [(3, 8), (8, 9), (9, 10), (10, 4), (4,3)]

# Define stop positions for both routes (some shared)
STOP_POSITIONS = {
    0: (100, 250), 1: (200, 150), 2: (300, 150), 3: (400, 250), 4: (400, 350),
    5: (300, 450), 6: (200, 450), 7: (100, 350),  # Route 1 stops
    8: (500, 200), 9: (600, 300), 10: (500, 400)  # Route 2 stops
}
