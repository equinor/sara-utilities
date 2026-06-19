import json
from pathlib import Path
from typing import Any

import pytest
from azure.storage.blob import BlobClient, BlobServiceClient

import main
from sara_utilities.config.settings import settings
from sara_utilities.models.blob_storage_location import BlobStorageLocation
from tests.conftest import (
    AZURITE_ACCOUNT,
    BLOB_CONTAINER,
    SOURCE_BLOB_BYTES,
    SOURCE_BLOB_NAME,
    AzuriteFixture,
)


def test_main_copies_blob_byte_for_byte(
    source_azurite: AzuriteFixture,
    destination_azurite: AzuriteFixture,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(settings, "SOURCE_STORAGE_ACCOUNT", "")
    monkeypatch.setattr(
        settings,
        "SOURCE_STORAGE_CONNECTION_STRING",
        source_azurite.connection_string,
    )
    monkeypatch.setattr(settings, "DESTINATION_STORAGE_ACCOUNT", "")
    monkeypatch.setattr(
        settings,
        "DESTINATION_STORAGE_CONNECTION_STRING",
        destination_azurite.connection_string,
    )

    input_loc = BlobStorageLocation(
        storageAccount=AZURITE_ACCOUNT,
        blobContainer=BLOB_CONTAINER,
        blobName=SOURCE_BLOB_NAME,
    )
    output_loc = BlobStorageLocation(
        storageAccount=AZURITE_ACCOUNT,
        blobContainer=BLOB_CONTAINER,
        blobName="visualized/output.mp4",
    )
    result_file: Path = tmp_path / "result.json"

    monkeypatch.setattr(
        "sys.argv",
        [
            "main.py",
            "--input-blob-storage-locations",
            json.dumps([input_loc.model_dump(by_alias=True)]),
            "--output-blob-storage-location",
            output_loc.model_dump_json(by_alias=True),
            "--extras",
            json.dumps({"operation": "copy-raw-to-visualized"}),
            "--result-output-file",
            str(result_file),
        ],
    )

    main.main()

    dst_client: BlobServiceClient = BlobServiceClient.from_connection_string(
        destination_azurite.connection_string
    )
    dst_blob: BlobClient = dst_client.get_blob_client(
        container=BLOB_CONTAINER, blob="visualized/output.mp4"
    )
    downloaded = dst_blob.download_blob()
    downloaded_bytes: bytes = downloaded.readall()

    payload: dict[str, Any] = json.loads(result_file.read_text())
    assert payload == {
        "outputBlobStorageLocation": output_loc.model_dump(by_alias=True)
    }
    assert downloaded_bytes == SOURCE_BLOB_BYTES
    assert downloaded.properties.content_settings.content_type == "video/mp4"
