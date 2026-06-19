from typing import Callable

import pytest

from sara_utilities.models.blob_storage_location import BlobStorageLocation


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
