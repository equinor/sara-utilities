import pytest

from sara_utilities.models.extras import CopyRawToVisualizedExtras, parse_extras_dict


def test_parses_copy_raw_to_visualized_payload() -> None:
    result = parse_extras_dict({"operation": "copy-raw-to-visualized"})

    assert isinstance(result, CopyRawToVisualizedExtras)
    assert result.operation == "copy-raw-to-visualized"


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"operation": "unknown-op"},
        {"operation": "copy-raw-to-visualized", "extra": "field"},
    ],
    ids=[
        "missing-operation",
        "unknown-operation",
        "extra-field-forbidden",
    ],
)
def test_invalid_payload_rejected(payload: dict) -> None:
    with pytest.raises(ValueError, match="--extras is invalid"):
        parse_extras_dict(payload)
