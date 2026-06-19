import json

import pytest

from sara_utilities.cli_inputs import (
    parse_extras,
    parse_input_blob_storage_locations,
    parse_output_blob_storage_location,
)
from sara_utilities.models.blob_storage_location import BlobStorageLocation
from sara_utilities.models.extras import CopyRawToVisualizedExtras


def _loc(account: str = "a", container: str = "b", blob: str = "c.mp4") -> dict:
    return {
        "storageAccount": account,
        "blobContainer": container,
        "blobName": blob,
    }


def test_parse_input_returns_list_of_locations() -> None:
    result = parse_input_blob_storage_locations(
        json.dumps([_loc(), _loc(blob="d.mp4")])
    )

    assert [loc.blob_name for loc in result] == ["c.mp4", "d.mp4"]
    assert all(isinstance(loc, BlobStorageLocation) for loc in result)


@pytest.mark.parametrize(
    "payload, message_fragment",
    [
        ("not json{", "valid JSON"),
        (json.dumps({"storageAccount": "a"}), "JSON array"),
        (json.dumps([{"storageAccount": "a"}]), "invalid"),
    ],
    ids=["malformed-json", "object-instead-of-array", "missing-required-field"],
)
def test_parse_input_rejects_invalid_payloads(
    payload: str, message_fragment: str
) -> None:
    with pytest.raises(ValueError, match=message_fragment):
        parse_input_blob_storage_locations(payload)


def test_parse_output_returns_single_location() -> None:
    result = parse_output_blob_storage_location(json.dumps(_loc(blob="out.mp4")))

    assert result.blob_name == "out.mp4"


@pytest.mark.parametrize(
    "payload, message_fragment",
    [
        ("not json{", "valid JSON"),
        (json.dumps([_loc()]), "JSON object"),
        (json.dumps({"storageAccount": "a"}), "invalid"),
    ],
    ids=["malformed-json", "array-instead-of-object", "missing-required-field"],
)
def test_parse_output_rejects_invalid_payloads(
    payload: str, message_fragment: str
) -> None:
    with pytest.raises(ValueError, match=message_fragment):
        parse_output_blob_storage_location(payload)


def test_parse_extras_returns_matching_variant() -> None:
    result = parse_extras(json.dumps({"operation": "copy-raw-to-visualized"}))

    assert isinstance(result, CopyRawToVisualizedExtras)


@pytest.mark.parametrize(
    "payload, message_fragment",
    [
        ("not json{", "valid JSON"),
        (json.dumps([]), "JSON object"),
        (json.dumps({"operation": "unknown-op"}), "invalid"),
    ],
    ids=["malformed-json", "array-instead-of-object", "unknown-operation"],
)
def test_parse_extras_rejects_invalid_payloads(
    payload: str, message_fragment: str
) -> None:
    with pytest.raises(ValueError, match=message_fragment):
        parse_extras(payload)
