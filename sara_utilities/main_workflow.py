import logging
from typing import Callable

from sara_utilities.models.blob_storage_location import BlobStorageLocation
from sara_utilities.models.extras import Extras

logger = logging.getLogger(__name__)


OperationHandler = Callable[
    [list[BlobStorageLocation], BlobStorageLocation, Extras],
    None,
]


_HANDLERS: dict[str, OperationHandler] = {}


def register_handler(operation: str, handler: OperationHandler) -> None:
    _HANDLERS[operation] = handler


def run(
    input_locations: list[BlobStorageLocation],
    output_location: BlobStorageLocation,
    extras: Extras,
) -> None:
    handler = _HANDLERS.get(extras.operation)
    if handler is None:
        raise ValueError(f"No handler registered for operation '{extras.operation}'")
    logger.info(f"Dispatching to handler for operation '{extras.operation}'")
    handler(input_locations, output_location, extras)
