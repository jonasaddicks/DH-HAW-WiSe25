from app.dtos import RoutingResponse, RouteSegment
import math


# Mock-Routen für POC
# Struktur: start, end, waypoints (all points vom start bis end)
# Dadurch kompatibel für externe APIs
MOCK_ROUTES = [
    {
        "route_id": 1,
        "name": "Schattiger Weg",
        "distance_m": 450,
        "duration_min": 6,
        "difficulty": "easy",
        "start": {"lat": 53.556710, "lng": 10.022605},
        "end": {"lat": 53.554730, "lng": 10.020165},
        "waypoints": [
            {"lat": 53.556305, "lng": 10.021653},
            {"lat": 53.556008, "lng": 10.021997},
            {"lat": 53.555751, "lng": 10.022365},
            {"lat": 53.555418, "lng": 10.021952},
            {"lat": 53.555443, "lng": 10.021634},
        ]
    },
    {
        "route_id": 2,
        "name": "Rollstuhl-freundlicher Weg",
        "distance_m": 720,
        "duration_min": 10,
        "difficulty": "easy",
        "start": {"lat": 53.556710, "lng": 10.022605},
        "end": {"lat": 53.554730, "lng": 10.020165},
        "waypoints": [
            {"lat": 53.556305, "lng": 10.021653},
            {"lat": 53.556955, "lng": 10.020757},
            {"lat": 53.557060, "lng": 10.020520},
            {"lat": 53.556089, "lng": 10.018341},
            {"lat": 53.555387, "lng": 10.019418},
            {"lat": 53.555295, "lng": 10.019554},
            {"lat": 53.554978, "lng": 10.020061},
            {"lat": 53.554905, "lng": 10.019908},
        ]
    },
    {
        "route_id": 3,
        "name": "Kürzeste Route",
        "distance_m": 380,
        "duration_min": 5,
        "difficulty": "medium",
        "start": {"lat": 53.556710, "lng": 10.022605},
        "end": {"lat": 53.554730, "lng": 10.020165},
        "waypoints": [
            {"lat": 53.556084, "lng": 10.021164},
            {"lat": 53.555939, "lng": 10.020992},
            {"lat": 53.555295, "lng": 10.019554},
            {"lat": 53.554978, "lng": 10.020061},
            {"lat": 53.554905, "lng": 10.019908},
            
        ]
    },
]


def calculate_routes_service(
        start: tuple[float, float],
        end: tuple[float, float]
) -> list[RoutingResponse]:
    """
    Berechnet mögliche Routen zwischen Start und Ziel.
    Für POC: Gibt Mock-Routes zurück.
    Später: Kann externe API (OpenRouteService, OSRM) aufgerufen werden.
    
    :param start: (latitude, longitude) des Startpunkts
    :param end: (latitude, longitude) des Zielpunkts
    :return: Liste von berechneten RoutingResponse-Objekten
    """
    
    # POC: Einfach die Mock-Routes zurückgeben
    # Kombiniere Start + Waypoints + End zu vollständiger Route
    routes_result = []
    for route in MOCK_ROUTES:
        # Starte mit Start-Punkt, dann Waypoints, dann End-Punkt
        full_waypoints = [
            RouteSegment(**route["start"]),
            *[RouteSegment(**wp) for wp in route["waypoints"]],
            RouteSegment(**route["end"])
        ]
        
        route_response = RoutingResponse(
            route_id=route["route_id"],
            name=route["name"],
            distance_m=route["distance_m"],
            duration_min=route["duration_min"],
            difficulty=route["difficulty"],
            start=RouteSegment(**route["start"]),
            end=RouteSegment(**route["end"]),
            waypoints=full_waypoints
        )
        routes_result.append(route_response)
    
    return routes_result
    
    # Später: z.B. externe API aufrufen
    # response = requests.get(f"https://api.openrouteservice.org/v2/directions/foot", params={
    #     "start": f"{start[1]},{start[0]}",  # lng,lat (ORS Format)
    #     "end": f"{end[1]},{end[0]}",
    # })
    # return parse_ors_response(response)