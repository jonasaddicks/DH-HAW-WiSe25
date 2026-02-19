from sqlalchemy.orm import Session
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

from app.dtos import CommentResponseDTO, CommentCreateDTO
from app.logging import log_error, Source
from app.model import CommentModel
from app.repositories import CommentRepository

# Mock-Daten für POC
MOCK_COMMENTS = [
    {
        "id": 1,
        "text": "Hervorragende Zugänglichkeit und hilfreiche Mitarbeiter!",
        "lat": 53.556458,
        "lng": 10.022068,
        "user": "Sarah_B",
        "created_at": "2025-02-10 14:30:00"
    },
    {
        "id": 2,
        "text": "Rampe ist zu steil, schwer zu erklimmen.",
        "lat": 53.556073,
        "lng": 10.021971,
        "user": "Thomas_K",
        "created_at": "2025-02-08 09:15:00"
    },
    {
        "id": 3,
        "text": "Kostenlose Parkplätze für Menschen mit Behinderung",
        "lat": 53.555697,
        "lng": 10.020262,
        "user": "Anna_M",
        "created_at": "2025-02-05 16:45:00"
    },
    {
        "id": 4,
        "text": "Aufzug funktioniert, sehr sauber",
        "lat": 53.556700,
        "lng": 10.021500,
        "user": "Michael_S",
        "created_at": "2025-02-01 11:20:00"
    },
]


def get_comments_at_service(
        lat: float,
        lng: float,
        radius: float = 1000.0
) -> list[CommentResponseDTO]:
    """
    Gibt alle Kommentare in der Nähe eines Punktes zurück (Mock-Daten).
    
    :param lat: Latitude des Suchpunkts
    :param lng: Longitude des Suchpunkts
    :param radius: Radius in Metern (ungefähr)
    :return: Liste von Kommentaren
    """
    
    # Sehr vereinfachte Distanzberechnung (nicht exakt, für POC OK)
    # 1 Grad ≈ 111 km
    lat_diff = abs(lat - 53.556300)
    lng_diff = abs(lng - 10.021300)
    max_diff = radius / 111000  # Ungefähre Umrechnung
    
    nearby_comments = []
    for comment in MOCK_COMMENTS:
        lat_dist = abs(comment["lat"] - lat)
        lng_dist = abs(comment["lng"] - lng)
        
        if lat_dist <= max_diff and lng_dist <= max_diff:
            nearby_comments.append(CommentResponseDTO(**comment))
    
    return nearby_comments


def post_comment_service(
    db: Session,
    dto: CommentCreateDTO
) -> bool:
    """
    Creates and saves a comment in the database
    """
    try:
        geom_point = from_shape(Point(dto.lng, dto.lat), srid=4326)  # PostGIS: POINT(lon lat)
        comment = CommentModel(
            text=dto.text,
            user_id=dto.user_id,
            geom=geom_point
        )
    except Exception as e:
        log_error(Source.comment_service, f'Could not create CommentModel: {repr(e)}')
        return False

    repo = CommentRepository(db)
    try:
        repo.create(comment)
        db.commit()
        db.refresh(comment)
        return True

    except Exception as e:
        db.rollback()
        log_error(Source.comment_service, repr(e))
        raise