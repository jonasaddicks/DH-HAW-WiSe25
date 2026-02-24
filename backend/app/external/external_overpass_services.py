import json

import httpx
import os

from shapely.geometry.polygon import Polygon


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
    return len(elements)
