from app.dtos import RoutingResponse, RouteSegment
import math


# Mock-Routen für POC
MOCK_ROUTES = [
    {
        "route_id": 1,
        "name": "Schattiger Weg",
        "distance_m": 450,
        "duration_min": 6,
        "difficulty": "easy",
        "waypoints": [
            {"lat": 53.556301, "lng": 10.021649},
            {"lat": 53.556305, "lng": 10.021653},
            {"lat": 53.556008, "lng": 10.021997},
            {"lat": 53.555751,"lng": 10.022365},
            {"lat": 53.555418, "lng": 10.021952},
            {"lat": 53.555416, "lng":10.021726},
            {"lat": 53.554817, "lng": 10.020319},

        ]
    },
    {
        "route_id": 2,
        "name": "Rollstuhl-freundlicher Weg",
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