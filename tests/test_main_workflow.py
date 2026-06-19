from typing import Callable
from unittest.mock import MagicMock, patch

import pytest

from sara_utilities import main_workflow
from sara_utilities.models.blob_storage_location import BlobStorageLocation
from sara_utilities.models.extras import CopyRawToVisualizedExtras

BlobLocationFactory = Callable[..., BlobStorageLocation]


def test_dispatches_to_registered_handler(
    make_blob_location: BlobLocationFactory,
) -> None:
    extras = CopyRawToVisualizedExtras(operation="copy-raw-to-visualized")
    handler = MagicMock()

    with patch.object(main_workflow, "_HANDLERS", {"copy-raw-to-visualized": handler}):
        main_workflow.run([make_blob_location()], make_blob_location(), extras)

    handler.assert_called_once()


def test_run_raises_when_no_handler_registered(
    make_blob_location: BlobLocationFactory,
) -> None:
    extras = CopyRawToVisualizedExtras(operation="copy-raw-to-visualized")

    with patch.object(main_workflow, "_HANDLERS", {}):
        with pytest.raises(ValueError, match="No handler registered"):
            main_workflow.run([make_blob_location()], make_blob_location(), extras)
