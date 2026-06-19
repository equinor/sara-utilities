from unittest.mock import MagicMock

import pytest

from sara_utilities.file_io.blob_io import (
    build_blob_service_client,
    download_blob_to_bytes,
    upload_bytes_to_blob,
    validate_locations,
)
from sara_utilities.models.blob_storage_location import BlobStorageLocation


def _loc(
    account: str = "acct", container: str = "c", blob: str = "b.mp4"
) -> BlobStorageLocation:
    return BlobStorageLocation(
        storageAccount=account, blobContainer=container, blobName=blob
    )


def test_download_returns_blob_bytes() -> None:
    service_client = MagicMock()
    service_client.get_blob_client.return_value.download_blob.return_value.readall.return_value = (
        b"payload"
    )

    result = download_blob_to_bytes(service_client, _loc())

    assert result == b"payload"
    service_client.get_blob_client.assert_called_once_with(container="c", blob="b.mp4")


def test_upload_calls_upload_blob_with_overwrite() -> None:
    service_client = MagicMock()
    blob_client = service_client.get_blob_client.return_value

    upload_bytes_to_blob(service_client, _loc(), b"payload", content_type="video/mp4")

    service_client.get_blob_client.assert_called_once_with(container="c", blob="b.mp4")
    args, kwargs = blob_client.upload_blob.call_args
    assert args[0] == b"payload"
    assert kwargs["overwrite"] is True
    assert kwargs["content_settings"].content_type == "video/mp4"


def test_validate_locations_passes_when_accounts_match() -> None:
    validate_locations(
        _loc(account="src"),
        _loc(account="dst"),
        expected_source_account="src",
        expected_destination_account="dst",
    )


@pytest.mark.parametrize(
    "src_account, dst_account, expected_src, expected_dst, bad_value",
    [
        ("wrong", "dst", "src", "dst", "wrong"),
        ("src", "wrong", "src", "dst", "wrong"),
    ],
    ids=["source-mismatch", "destination-mismatch"],
)
def test_validate_locations_raises_on_mismatch(
    src_account: str,
    dst_account: str,
    expected_src: str,
    expected_dst: str,
    bad_value: str,
) -> None:
    with pytest.raises(ValueError, match=f"'{bad_value}'"):
        validate_locations(
            _loc(account=src_account),
            _loc(account=dst_account),
            expected_source_account=expected_src,
            expected_destination_account=expected_dst,
        )


def test_build_client_raises_when_neither_account_nor_connection_string_provided() -> (
    None
):
    with pytest.raises(
        ValueError, match="Neither a storage account nor a connection string"
    ):
        build_blob_service_client(storage_account="", connection_string="")
