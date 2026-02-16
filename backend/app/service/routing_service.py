from app.dtos import RoutingResponse, RouteSegment
import math


# Mock-Routen für POC
MOCK_ROUTES = [
    {
        "route_id": 1,
        "name": "Direkter Weg (Route 1)",
        "distance_m": 450,
        "duration_min": 6,
        "difficulty": "easy",
        "waypoints": [
            {"lat": 53.556090, "lng": 10.021469},
            {"lat": 53.556200, "lng": 10.021600},
            {"lat": 53.556350, "lng": 10.021900},
            {"lat": 53.556450, "lng": 10.022100},
        ]
    },
    {
        "route_id": 2,
        "name": "Barrierefreier Weg",
        "distance_m": 720,
        "duration_min": 10,
        "difficulty": "easy",
        "waypoints": [
            {"lat": 53.556090, "lng": 10.021469},
            {"lat": 53.555900, "lng": 10.021300},
            {"lat": 53.555700, "lng": 10.021400},
            {"lat": 53.555600, "lng": 10.021800},
            {"lat": 53.555700, "lng": 10.022200},
            {"lat": 53.556000, "lng": 10.022400},
            {"lat": 53.556450, "lng": 10.022100},
        ]
    },
    {
        "route_id": 3,
        "name": "Kürzeste Route",
        "distance_m": 380,
        "duration_min": 5,
        "difficulty": "medium",
        "waypoints": [
            {"lat": 53.556090, "lng": 10.021469},
            {"lat": 53.556250, "lng": 10.021750},
            {"lat": 53.556450, "lng": 10.022100},
        ]
    },
]


def calculate_routes(
        start: tuple[float, float],
        end: tuple[float, float]
) -> list[RoutingResponse]:
    """
    Berechnet mögliche Routen zwischen Start und Ziel (Mock-Daten).
    
    :param start: (latitude, longitude) des Startpunkts
    :param end: (latitude, longitude) des Zielpunkts
    :return: Liste von berechneten Routen
    """
    
    # Für den POC: Einfach die Mock-Routes zurückgeben
    # Mit angepassten Start-/Endpunkten
    
    routes_result = []
    for route in MOCK_ROUTES:
        # Anpassen der Waypoints (Mock bleiben gleich, aber mit echtenKoordinaten)
        adjusted_waypoints = []
        
        # Start-Punkt
        adjusted_waypoints.append(RouteSegment(lat=start[0], lng=start[1]))
        
        # Mittelpunkte
        for wp in route["waypoints"][1:-1]:
            adjusted_waypoints.append(RouteSegment(**wp))
        
        # End-Punkt
        adjusted_waypoints.append(RouteSegment(lat=end[0], lng=end[1]))
        
        route_response = RoutingResponse(
            route_id=route["route_id"],
            name=route["name"],
            distance_m=route["distance_m"],
            duration_min=route["duration_min"],
            difficulty=route["difficulty"],
            waypoints=adjusted_waypoints
        )
        routes_result.append(route_response)
    
    return routes_result