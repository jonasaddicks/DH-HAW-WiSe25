from sqlalchemy.orm import Session
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

from app.dtos import CommentResponseDTO, CommentCreateDTO, CommentRequestDTO
from app.exceptions import CommentConversionException
from app.logging import log_error, Source, log_debug
from app.model import CommentModel
from app.repositories import CommentRepository


def get_comments_at_service(
        db: Session,
        dto: CommentRequestDTO
) -> list[CommentResponseDTO]:
    """
    Returns a list of all comments in a specified area
    """

    repo = CommentRepository(db)
    rows = repo.get_comments_in_radius(dto.lng, dto.lat, dto.radius)
    log_debug(Source.comment_service, f'Found {len(rows)} comments')

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

    log_debug(Source.external_overpass_services, f'Creating new comment "{dto.text}" at (lng;lat): {dto.lng};{dto.lat} from {dto.user_id}')
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
        log_error(Source.comment_service, f'Exception writing to database: {repr(e)} - rollback')
        db.rollback()
        raise