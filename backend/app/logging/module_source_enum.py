from enum import Enum


class Source(Enum):
    """
    Enumeration of logging sources used for categorizing log messages.

    Each member represents a distinct component or subsystem within the application,
    enabling structured and consistent logging across modules.
    """
    logger = 'LOGGER'
    endpoint_comment = 'ENDPOINT_COMMENT'
    endpoint_routing = 'ENDPOINT_ROUTING'
    db_session = 'DB_SESSION'
    comment_dto = 'COMMENT_DTO'
    routing_dto = 'ROUTING_DTO'
    external_overpass_services = 'EXTERNAL_OVERPASS_SERVICES'
    external_routing_services = 'EXTERNAL_ROUTING_SERVICES'
    comment_model = 'COMMENT_MODEL'
    user_model = 'USER_MODEL'
    user_prefs_model = 'USER_PREFS_MODEL'
    comment_repo = 'COMMENT_REPO'
    route_repo = 'ROUTE_REPO'
    comment_service = 'COMMENT_SERVICE'
    routing_service = 'ROUTING_SERVICE'

    def __str__(self):
        return self.value