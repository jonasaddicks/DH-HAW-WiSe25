from sqlalchemy.orm import Session
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

from app.dtos import CommentResponseDTO, CommentCreateDTO, CommentRequestDTO
from app.exceptions import CommentConversionException
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
        db: Session,
        dto: CommentRequestDTO
) -> list[CommentResponseDTO]:
    """
    Returns a list of all comments in a specified area
    """
    repo = CommentRepository(db)
    rows = repo.get_comments_in_radius(dto.lng, dto.lat, dto.radius)

    result: list[CommentResponseDTO] = []
    for r in rows:
        created = r.created_at
        created_iso = created.isoformat() if hasattr(created, "isoformat") else str(created)

        dto_out = CommentResponseDTO(
            id=int(r.id),
            text=r.text,
            lat=float(r.lat),
            lng=float(r.lng),
            user=r.user,
            created_at=created_iso,
        )
        result.append(dto_out)

    return result


def post_comment_service(
    db: Session,
    dto: CommentCreateDTO
):
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
        log_error(Source.comment_service, f'Could not translate from CommentCreateDTO to CommentModel: {repr(e)}')
        raise CommentConversionException

    repo = CommentRepository(db)
    try:
        repo.create(comment)
        db.commit()
        db.refresh(comment)

    except Exception as e:
        db.rollback()
        log_error(Source.comment_service, f'Exception writing to database: {repr(e)}')
        raise