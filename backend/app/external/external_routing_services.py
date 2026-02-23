import json
import os
import httpx

from app.dtos import RouteSegment, Route
from app.exceptions import UnexpectedRoutingResponseException
from app.logging import log_error, Source, log_warning, log_debug

OSRM_URL = os.environ.get("OSRM_URL", "https://routing.openstreetmap.de/routed-foot")

def _parse_osrm_route(route) -> list[RouteSegment]:
    waypoints: list[RouteSegment] = []
    coordinates = route["geometry"]["coordinates"]
    for lon, lat in coordinates:
        segment = RouteSegment(lat=lat, lng=lon)
        waypoints.append(segment)
    return waypoints

async def fetch_osrm_routes(
    start: tuple[float, float],
    end: tuple[float, float]
) -> list[Route] | None:

    coords = f"{start[0]},{start[1]};{end[0]},{end[1]}"
    url = f"{OSRM_URL}/route/v1/foot/{coords}"
    params = {
        "overview": "full",
        "geometries": "geojson",
        "steps": "false",
        "alternatives": "3"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=10)
            response.raise_for_status()
            data_raw = response.json()

        if data_raw.get("code") != "Ok":
            raise UnexpectedRoutingResponseException('OSRM responded with an unexpected response')

        if not data_raw.get("routes"):
            log_warning(Source.external_routing_services, f"OSRM returned no routes")
            return []

        result: list[Route] = []
        for route in data_raw["routes"]:
            result.append(
                Route(
                    distance_m=route["distance"],
                    duration_min=int(route["duration"] / 60),
                    start=RouteSegment(lat=start[0], lng=start[1]),
                    end=RouteSegment(lat=end[0], lng=end[1]),
                    waypoints=_parse_osrm_route(route)
                )
            )
        log_debug(Source.external_routing_services, f"OSRM returned {len(result)} routes")
        return result

    except Exception as e:
        log_error(Source.external_routing_services, f"OSRM failed: {repr(e)}")
        return None