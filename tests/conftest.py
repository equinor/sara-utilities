from collections.abc import Generator
from dataclasses import dataclass
from typing import Callable

import pytest
from azure.storage.blob import BlobServiceClient
from testcontainers.azurite import AzuriteContainer

from sara_utilities.models.blob_storage_location import BlobStorageLocation

AZURITE_ACCOUNT: str = "devstoreaccount1"
BLOB_CONTAINER: str = "test"
SOURCE_BLOB_NAME: str = "input.mp4"
SOURCE_BLOB_BYTES: bytes = b"hello-mp4-bytes"


@dataclass
class AzuriteFixture:
    container: AzuriteContainer
    connection_string: str
    account_name: str


def _create_azurite() -> AzuriteContainer:
    container: AzuriteContainer = AzuriteContainer()
    container.with_command("azurite --blobHost 0.0.0.0 --skipApiVersionCheck")
    return container


@pytest.fixture
def make_blob_location() -> Callable[..., BlobStorageLocation]:
    def _make(
        account: str = "acct",
        container: str = "container",
        blob: str = "blob.mp4",
    ) -> BlobStorageLocation:
        return BlobStorageLocation(
            storageAccount=account, blobContainer=container, blobName=blob
        )

    return _make


@pytest.fixture()
def source_azurite() -> Generator[AzuriteFixture, None, None]:
    with _create_azurite() as container:
        connection_string: str = container.get_connection_string()
        client: BlobServiceClient = BlobServiceClient.from_connection_string(
            connection_string
        )
        client.create_container(BLOB_CONTAINER)
        client.get_blob_client(
            container=BLOB_CONTAINER, blob=SOURCE_BLOB_NAME
        ).upload_blob(SOURCE_BLOB_BYTES, overwrite=True)
        yield AzuriteFixture(
            container=container,
            connection_string=connection_string,
            account_name=AZURITE_ACCOUNT,
        )


@pytest.fixture()
def destination_azurite() -> Generator[AzuriteFixture, None, None]:
    with _create_azurite() as container:
        connection_string: str = container.get_connection_string()
        client: BlobServiceClient = BlobServiceClient.from_connection_string(
            connection_string
        )
        client.create_container(BLOB_CONTAINER)
        yield AzuriteFixture(
            container=container,
            connection_string=connection_string,
            account_name=AZURITE_ACCOUNT,
        )
