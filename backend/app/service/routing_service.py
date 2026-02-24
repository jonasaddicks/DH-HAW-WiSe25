import random
import pyproj

from sqlalchemy.orm import Session
from shapely.geometry import LineString
from shapely.ops import transform
from shapely.geometry.polygon import Polygon

from app.dtos import RoutingResponse, RouteSegment, RoutingRequest, Route
from app.external import RoutingServices, OverpassServices
from app.logging import log_error, Source, log_warning, log_debug
from app.repositories.route_repo import RoutingRepository


async def calculate_routes_service(
        dto: RoutingRequest,
        db: Session
) -> list[RoutingResponse]:
    """
    Calculate and evaluate routes from a specified start to a specified end.
    """

    routes = None
    try:
        routes = await RoutingServices.fetch_osrm_routes(
            (dto.start_lng, dto.start_lat),
            (dto.end_lng, dto.end_lat),
        )
    except Exception as e:
        log_error(Source.routing_service, f'Failed to fetch routes: {e}')

    if routes:
        log_debug(Source.routing_service, f'Evaluating {len(routes)} routes')
        route_response: list[RoutingResponse] = []
        for route in routes:

            route_meta: RouteMeta = await RouteMeta.create(route)
            evaluation_weights: EvaluationWeights = EvaluationWeights(user_id=dto.user_id, db=db)
            score: float = _calculate_score(
                route_meta=route_meta,
                evaluation_weights=evaluation_weights
            )
            route_response.append(
                RoutingResponse(
                    score=score,
                    route=route
                )
            )
        route_response.sort(key=lambda r: r.score, reverse=True)
        return route_response[:3]
    else:
        log_warning(Source.routing_service, f'Routes are empty')
        return []

class RouteMeta:
    k_stairs: float
    k_flat: float
    k_shadow: float
    k_seats: float
    k_weather: float

    def __init__(self, k_stairs, k_flat, k_shadow, k_seats, k_weather):
        self.k_stairs = k_stairs
        self.k_flat = k_flat
        self.k_shadow = k_shadow
        self.k_seats = k_seats
        self.k_weather = k_weather

    @classmethod
    async def create(cls, route: Route) -> "RouteMeta":
        route_polygon = _create_route_polygon(route.waypoints)

        k_stairs = random.random() # mock
        k_flat = random.random() # mock
        k_shadow = random.random() # mock

        number_seats: int = await OverpassServices.get_seats(route_polygon)
        seats_per_kilometer: float = number_seats / (route.distance_m / 1000)
        s_half: float = 2

        k_seats = seats_per_kilometer / (seats_per_kilometer + s_half)

        k_weather = random.random() # mock

        return cls(k_stairs, k_flat, k_shadow, k_seats, k_weather)

class EvaluationWeights:
    w_stairs: float = 1.5
    w_flat: float = 1.1
    w_shadow: float = 0.6
    w_seats: float = 1.3
    w_weather: float = 0.5

    def __init__(self, user_id: int, db: Session):
        if user_id == -1:
            return
        else:
            repo = RoutingRepository(db)
            user_prefs = repo.get_user_prefs(user_id=user_id)

            self.w_stairs = (self.w_stairs + user_prefs["w_stairs"]) / 2
            self.w_flat = (self.w_flat + user_prefs["w_flat"]) / 2
            self.w_shadow = (self.w_shadow + user_prefs["w_shadow"]) / 2
            self.w_seats = (self.w_seats + user_prefs["w_seats"]) / 2
            self.w_weather = (self.w_weather + user_prefs["w_weather"]) / 2

            w_sum: float = self.w_stairs + self.w_flat + self.w_shadow + self.w_seats + self.w_weather

            self.w_stairs /= w_sum
            self.w_flat /= w_sum
            self.w_shadow /= w_sum
            self.w_seats /= w_sum
            self.w_weather /= w_sum

def _calculate_score(
        route_meta: RouteMeta,
        evaluation_weights: EvaluationWeights
) -> float:
    score: float = 0
    score += route_meta.k_stairs * evaluation_weights.w_stairs
    score += route_meta.k_flat * evaluation_weights.w_flat
    score += route_meta.k_shadow * evaluation_weights.w_shadow
    score += route_meta.k_seats * evaluation_weights.w_seats
    score += route_meta.k_weather * evaluation_weights.w_weather
    return score

def _create_route_polygon(
        route_points: list[RouteSegment],
        buffer_m: float = 13
    )-> Polygon:
    line = LineString([(segment.lng, segment.lat) for segment in route_points])
    proj_wgs84 = pyproj.Proj('epsg:4326')
    proj_utm = pyproj.Proj(proj='utm', zone=32, ellps='WGS84')

    project_to_utm = pyproj.Transformer.from_proj(proj_wgs84, proj_utm, always_xy=True).transform
    project_to_wgs84 = pyproj.Transformer.from_proj(proj_utm, proj_wgs84, always_xy=True).transform

    line_utm = transform(project_to_utm, line)
    line_utm = line_utm.simplify(5, preserve_topology=False)

    polygon_utm = line_utm.buffer(buffer_m)

    polygon_wgs84 = transform(project_to_wgs84, polygon_utm)
    polygon_wgs84 = polygon_wgs84.simplify(0.0001, preserve_topology=True)

    return polygon_wgs84