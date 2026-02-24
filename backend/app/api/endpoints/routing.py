from fastapi import APIRouter, Query, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session

from fastapi.params import Depends

from app.db import get_db
from app.dtos import RoutingResponse, RoutingRequest
from app.logging import log_info, Source, log_error
from app.service import RoutingService

router = APIRouter()

@router.get("/route", response_model=list[RoutingResponse])
async def calculate_routes(
    dto: Annotated[RoutingRequest, Query()],
    db: Session = Depends(get_db)
) -> list[RoutingResponse]:
    """
    Calculates possible routes from given start to given end coordinates.
    """

    log_info(Source.endpoint_routing, f'/route: {dto}')

    try:
        result: list[RoutingResponse] = await RoutingService.calculate_routes_service(dto, db)
        return result

    except Exception as e:
        log_error(Source.endpoint_comment, f'/route: internal failure: {repr(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error."
        )
