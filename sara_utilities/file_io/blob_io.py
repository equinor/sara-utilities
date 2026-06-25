import logging

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, ContentSettings

from sara_utilities.models.blob_storage_location import BlobStorageLocation

logger = logging.getLogger(__name__)


def build_blob_service_client(
    storage_account: str, connection_string: str
) -> BlobServiceClient:
    if connection_string:
        return BlobServiceClient.from_connection_string(connection_string)
    if storage_account:
        return BlobServiceClient(
            account_url=f"https://{storage_account}.blob.core.windows.net",
            credential=DefaultAzureCredential(),
        )
    raise ValueError(
        "Neither a storage account nor a connection string was configured."
    )


def download_blob_to_bytes(
    blob_service_client: BlobServiceClient,
    blob_storage_location: BlobStorageLocation,
) -> bytes:
    blob_client = blob_service_client.get_blob_client(
        container=blob_storage_location.blob_container,
        blob=blob_storage_location.blob_name,
    )
    return blob_client.download_blob().readall()


def upload_bytes_to_blob(
    blob_service_client: BlobServiceClient,
    blob_storage_location: BlobStorageLocation,
    data: bytes,
    content_type: str = "application/octet-stream",
) -> None:
    blob_client = blob_service_client.get_blob_client(
        container=blob_storage_location.blob_container,
        blob=blob_storage_location.blob_name,
    )
    settings = ContentSettings(content_type=content_type)
    logger.debug(f"Uploading {len(data)} bytes to {blob_storage_location}")
    blob_client.upload_blob(data, overwrite=True, content_settings=settings)


def _account_from_connection_string(connection_string: str) -> str:
    """Extract the AccountName field from an Azure Storage connection string."""
    for part in connection_string.split(";"):
        if part.startswith("AccountName="):
            return part[len("AccountName=") :]
    return ""


def resolve_expected_account(storage_account: str, connection_string: str) -> str:
    """Resolve which account name payload locations should be validated against.

    Prefers an explicitly configured account name; otherwise derives the
    account from the connection string so a single source of truth still
    pins which Azure Storage account the analyzer will talk to.
    """
    return storage_account or _account_from_connection_string(connection_string)


def validate_storage_account(
    storage_account: str, expected_storage_account: str
) -> None:
    if storage_account != expected_storage_account:
        raise ValueError(
            f"storageAccount '{storage_account}' does not match the expected "
            f"account '{expected_storage_account}'."
        )


def validate_locations(
    input_location: BlobStorageLocation,
    output_location: BlobStorageLocation,
    expected_source_account: str,
    expected_destination_account: str,
) -> None:
    validate_storage_account(input_location.storage_account, expected_source_account)
    validate_storage_account(
        output_location.storage_account, expected_destination_account
    )
    logger.info("Storage account validation successful.")
