import os
import httpx
from app.dtos import RoutingResponse, RouteSegment
from app.logging.logger import log_error, log_info
from app.logging.module_source_enum import Source

OSRM_URL = os.environ.get("OSRM_URL", "https://routing.openstreetmap.de/routed-foot")


def _decode_polyline(polyline: str) -> list[dict]:
    """Dekodiert Google Encoded Polyline zu lat/lng-Liste."""
    coords = []
    index, lat, lng = 0, 0, 0
    while index < len(polyline):
        for is_lng in (False, True):
            shift, result = 0, 0
            while True:
                b = ord(polyline[index]) - 63
                index += 1
                result |= (b & 0x1F) << shift
                shift += 5
                if b < 0x20:
                    break
            value = ~(result >> 1) if result & 1 else result >> 1
            if is_lng:
                lng += value
                coords.append({"lat": lat / 1e5, "lng": lng / 1e5})
            else:
                lat += value
    return coords


async def fetch_osrm_routes(
    start: tuple[float, float],
    end: tuple[float, float]
) -> list[RoutingResponse] | None:
    """
    Ruft eine Route von der OSRM-API mit ab.
    :param start: (lat, lng)
    :param end: (lat, lng)
    """
    coords = f"{start[1]},{start[0]};{end[1]},{end[0]}"
    url = f"{OSRM_URL}/route/v1/foot/{coords}"
    params = {
        "overview": "full",
        "geometries": "polyline",
        "steps": "false",
        "alternatives": "3"
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

        if data.get("code") != "Ok" or not data.get("routes"):
            log_error(Source.external_routing_services, "OSRM returned no routes")
            return []

        names = ["Kürzeste Route", "Alternative Route", "Scenic Route"]
        result = []
        for i, route in enumerate(data["routes"][:3]):
            waypoints = _decode_polyline(route["geometry"])
            result.append(RoutingResponse(
                route_id=i + 1,
                name=names[i],
                distance_m=route["distance"],
                duration_min=int(route["duration"] / 60),
                difficulty="easy",
                start=RouteSegment(lat=start[0], lng=start[1]),
                end=RouteSegment(lat=end[0], lng=end[1]),
                waypoints=[RouteSegment(**wp) for wp in waypoints]
            ))

        log_info(Source.external_routing_services, f"OSRM returned {len(result)} routes")
        return result
    
    except Exception as e:
        log_error(Source.external_routing_services, f"OSRM request failed: {repr(e)}")
        return None