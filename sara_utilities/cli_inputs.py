import json
from typing import List

from pydantic import ValidationError

from sara_utilities.models.blob_storage_location import BlobStorageLocation
from sara_utilities.models.extras import Extras, parse_extras_dict


def parse_input_blob_storage_locations(value: str) -> List[BlobStorageLocation]:
    try:
        raw = json.loads(value)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"--input-blob-storage-locations is not valid JSON: {exc}"
        ) from exc

    if not isinstance(raw, list):
        raise ValueError(
            "--input-blob-storage-locations must be a JSON array of blob "
            f"locations, got {type(raw).__name__}."
        )

    try:
        return [BlobStorageLocation.model_validate(item) for item in raw]
    except ValidationError as exc:
        raise ValueError(
            f"--input-blob-storage-locations entry is invalid: {exc}"
        ) from exc


def parse_output_blob_storage_location(value: str) -> BlobStorageLocation:
    try:
        raw = json.loads(value)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"--output-blob-storage-location is not valid JSON: {exc}"
        ) from exc

    if not isinstance(raw, dict):
        raise ValueError(
            "--output-blob-storage-location must be a JSON object, "
            f"got {type(raw).__name__}."
        )

    try:
        return BlobStorageLocation.model_validate(raw)
    except ValidationError as exc:
        raise ValueError(f"--output-blob-storage-location is invalid: {exc}") from exc


def parse_extras(value: str) -> Extras:
    try:
        raw = json.loads(value)
    except json.JSONDecodeError as exc:
        raise ValueError(f"--extras is not valid JSON: {exc}") from exc

    if not isinstance(raw, dict):
        raise ValueError(f"--extras must be a JSON object, got {type(raw).__name__}.")

    return parse_extras_dict(raw)
