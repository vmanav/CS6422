# Define the route connections (linear route with direct connection from Stop 7 to Stop 0)
ROUTE_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7),  # Linear path
    (7, 0)  # Direct connection back to Stop 0
]

# Define stop positions (linear layout)
STOP_POSITIONS = {
    0: (100, 250),
    1: (200, 250),
    2: (300, 250),
    3: (400, 250),
    4: (500, 250),
    5: (600, 250),
    6: (700, 250),
    7: (800, 250),
}
