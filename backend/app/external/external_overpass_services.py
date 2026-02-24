import json

import httpx
import os

from shapely.geometry.polygon import Polygon

from app.logging import log_debug, Source, log_warning

OVERPASS_URL = os.environ.get("OVERPASS_URL", "undefined")


def _polygon_to_overpass(polygon):
    """
    convert a Shapely Polygon to an Overpass poly string
    """
    coords = []
    for lon, lat in polygon.exterior.coords:
        coords.append(f"{lat} {lon}")
    return " ".join(coords)

async def get_seats(route_polygon: Polygon) -> int:
    """
    Get the number of seats inside a (route-)polygon.
    """
    poly_str = _polygon_to_overpass(route_polygon)

    log_debug(Source.external_overpass_services, f'Getting seats in polygon from {OVERPASS_URL}')
    try:
        query = f"""
            [out:json][timeout:60];
            (
              node["amenity"="bench"](poly:"{poly_str}");
              way["amenity"="bench"](poly:"{poly_str}");
            );
            out center;
            """

        async with httpx.AsyncClient() as client:
            resp = await client.post(OVERPASS_URL, content=query, timeout=60)
            resp.raise_for_status()
            data = resp.json()

        elements = data.get("elements") or []
        number_of_seats = len(elements)
        log_debug(Source.external_overpass_services, f'Found {number_of_seats} seats: {json.dumps(data, indent=2)}')
        return number_of_seats

    except Exception as e:
        log_warning(Source.external_overpass_services, f"Overpass getting seats failed: {repr(e)}")
        raise
