import pytest
from pydantic import ValidationError

from sara_utilities.models.blob_storage_location import BlobStorageLocation


def test_round_trips_camel_case_aliases() -> None:
    payload = {
        "storageAccount": "acct",
        "blobContainer": "container",
        "blobName": "path/to/blob.mp4",
    }

    parsed = BlobStorageLocation.model_validate(payload)

    assert parsed.model_dump(by_alias=True) == payload


def test_str_joins_components_with_slashes() -> None:
    loc = BlobStorageLocation(
        storageAccount="acct", blobContainer="container", blobName="blob.mp4"
    )

    assert str(loc) == "acct/container/blob.mp4"


@pytest.mark.parametrize(
    "field_alias",
    ["storageAccount", "blobContainer", "blobName"],
)
def test_empty_string_rejected(field_alias: str) -> None:
    payload = {
        "storageAccount": "acct",
        "blobContainer": "container",
        "blobName": "blob.mp4",
        field_alias: "",
    }

    with pytest.raises(ValidationError, match=f"{field_alias} cannot be empty"):
        BlobStorageLocation.model_validate(payload)
