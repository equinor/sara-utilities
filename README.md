# SARA Utilities

The **SARA Utilities** analyzer hosts small per-inspection utility
operations so that inspection records that have no applicable analyzer
still get a `sara/visualization_available` MQTT publication. Part of
the [SARA](https://github.com/equinor/sara) ecosystem.

Operations are dispatched by the `extras.operation` field. New
operations plug in as new sub-handlers.

## Required Environment Variables

| Env var                                              | Description                                            |
| ---------------------------------------------------- | ------------------------------------------------------ |
| `SARA_UTILITIES_SOURCE_STORAGE_ACCOUNT`              | Source storage account name.                           |
| `SARA_UTILITIES_SOURCE_STORAGE_CONNECTION_STRING`    | Connection string for the source storage account.      |
| `SARA_UTILITIES_DESTINATION_STORAGE_ACCOUNT`         | Destination storage account name.                      |
| `SARA_UTILITIES_DESTINATION_STORAGE_CONNECTION_STRING` | Connection string for the destination storage account. |

`*_STORAGE_ACCOUNT` triggers Azure AD auth (`DefaultAzureCredential`);
`*_STORAGE_CONNECTION_STRING` is used as a fallback when the account
name is empty.

## Dependencies

The dependencies used for this package are listed in `pyproject.toml`
and pinned in `uv.lock`. This project uses
[uv](https://docs.astral.sh/uv/) for dependency management:

```bash
uv lock
```

To update the dependencies to the latest versions, run:

```bash
uv lock --upgrade
```

## Running tests

The integration test in `tests/test_integration_copy_raw_to_visualized.py`
spins up an [Azurite](https://github.com/Azure/Azurite) container via
`testcontainers` and requires a running Docker daemon.

```bash
uv run pytest
```

## Build and run with Docker

```bash
docker build -t sara-utilities:test .
```

Run the `copy-raw-to-visualized` operation against a real blob (make
sure the signed-in identity has Storage Blob Data Contributor on both
accounts, or pass connection strings instead):

```bash
docker run --rm \
    -e SARA_UTILITIES_SOURCE_STORAGE_ACCOUNT="$SOURCE_ACCOUNT" \
    -e SARA_UTILITIES_DESTINATION_STORAGE_ACCOUNT="$DEST_ACCOUNT" \
    sara-utilities:test \
    python main.py \
      --input-blob-storage-locations "[{\"storageAccount\": \"$SOURCE_ACCOUNT\", \"blobContainer\": \"$BLOB_CONTAINER\", \"blobName\": \"clip.mp4\"}]" \
      --output-blob-storage-location "{\"storageAccount\": \"$DEST_ACCOUNT\", \"blobContainer\": \"$BLOB_CONTAINER\", \"blobName\": \"clip.mp4\"}" \
      --extras "{\"operation\": \"copy-raw-to-visualized\"}" \
      --result-output-file /tmp/result.json
```
