from typing import Callable
from unittest.mock import MagicMock

import pytest

from sara_utilities.models.blob_storage_location import BlobStorageLocation
from sara_utilities.models.extras import CopyRawToVisualizedExtras
from sara_utilities.operations import copy_raw_to_visualized

BlobLocationFactory = Callable[..., BlobStorageLocation]


@pytest.fixture
def patched_io(monkeypatch: pytest.MonkeyPatch) -> dict[str, MagicMock]:
    mocks = {
        "validate_locations": MagicMock(),
        "build_blob_service_client": MagicMock(),
        "download_blob_to_bytes": MagicMock(return_value=b"raw-bytes"),
        "upload_bytes_to_blob": MagicMock(),
    }
    for name, mock in mocks.items():
        monkeypatch.setattr(copy_raw_to_visualized, name, mock)
    return mocks


def test_handler_raises_when_input_list_empty(
    make_blob_location: BlobLocationFactory,
    patched_io: dict[str, MagicMock],
) -> None:
    extras = CopyRawToVisualizedExtras(operation="copy-raw-to-visualized")

    with pytest.raises(ValueError, match="exactly one input blob"):
        copy_raw_to_visualized.handle([], make_blob_location(), extras)


def test_handler_raises_when_multiple_inputs(
    make_blob_location: BlobLocationFactory,
    patched_io: dict[str, MagicMock],
) -> None:
    extras = CopyRawToVisualizedExtras(operation="copy-raw-to-visualized")

    with pytest.raises(ValueError, match="exactly one input blob"):
        copy_raw_to_visualized.handle(
            [make_blob_location(), make_blob_location()],
            make_blob_location(),
            extras,
        )


def test_handler_uploads_with_video_mp4_content_type(
    make_blob_location: BlobLocationFactory,
    patched_io: dict[str, MagicMock],
) -> None:
    input_loc = make_blob_location(blob="raw/clip.mp4")
    output_loc = make_blob_location(blob="visualized/clip.mp4")
    extras = CopyRawToVisualizedExtras(operation="copy-raw-to-visualized")

    copy_raw_to_visualized.handle([input_loc], output_loc, extras)

    _, kwargs = patched_io["upload_bytes_to_blob"].call_args
    assert kwargs["content_type"] == "video/mp4"
    args, _ = patched_io["upload_bytes_to_blob"].call_args
    assert args[2] == b"raw-bytes"


def test_handler_falls_back_to_octet_stream_for_unknown_extension(
    make_blob_location: BlobLocationFactory,
    patched_io: dict[str, MagicMock],
) -> None:
    extras = CopyRawToVisualizedExtras(operation="copy-raw-to-visualized")

    copy_raw_to_visualized.handle(
        [make_blob_location(blob="raw/data.unknown-ext")],
        make_blob_location(blob="visualized/data.unknown-ext"),
        extras,
    )

    _, kwargs = patched_io["upload_bytes_to_blob"].call_args
    assert kwargs["content_type"] == "application/octet-stream"
