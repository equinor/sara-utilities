"""Byte-for-byte copy of the input blob to the output blob."""

import logging
import mimetypes

from azure.storage.blob import BlobServiceClient

from sara_utilities.config.settings import settings
from sara_utilities.file_io.blob_io import (
    build_blob_service_client,
    download_blob_to_bytes,
    resolve_expected_account,
    upload_bytes_to_blob,
    validate_locations,
)
from sara_utilities.main_workflow import register_handler
from sara_utilities.models.blob_storage_location import BlobStorageLocation
from sara_utilities.models.extras import CopyRawToVisualizedExtras

logger = logging.getLogger(__name__)


def _guess_content_type(blob_name: str) -> str:
    content_type, _ = mimetypes.guess_type(blob_name)
    return content_type or "application/octet-stream"


def handle(
    input_locations: list[BlobStorageLocation],
    output_location: BlobStorageLocation,
    extras: CopyRawToVisualizedExtras,
) -> None:
    if len(input_locations) != 1:
        raise ValueError(
            f"copy-raw-to-visualized requires exactly one input blob, "
            f"got {len(input_locations)}."
        )
    input_location: BlobStorageLocation = input_locations[0]

    expected_source: str = resolve_expected_account(
        settings.SOURCE_STORAGE_ACCOUNT,
        settings.SOURCE_STORAGE_CONNECTION_STRING,
    )
    expected_destination: str = resolve_expected_account(
        settings.DESTINATION_STORAGE_ACCOUNT,
        settings.DESTINATION_STORAGE_CONNECTION_STRING,
    )
    validate_locations(
        input_location,
        output_location,
        expected_source_account=expected_source,
        expected_destination_account=expected_destination,
    )

    src_client: BlobServiceClient = build_blob_service_client(
        settings.SOURCE_STORAGE_ACCOUNT,
        settings.SOURCE_STORAGE_CONNECTION_STRING,
    )
    dst_client: BlobServiceClient = build_blob_service_client(
        settings.DESTINATION_STORAGE_ACCOUNT,
        settings.DESTINATION_STORAGE_CONNECTION_STRING,
    )

    data: bytes = download_blob_to_bytes(src_client, input_location)
    content_type: str = _guess_content_type(output_location.blob_name)
    upload_bytes_to_blob(dst_client, output_location, data, content_type=content_type)
    logger.info(
        f"Copied {len(data)} bytes from {input_location} to {output_location} "
        f"(content_type={content_type})."
    )


register_handler("copy-raw-to-visualized", handle)
