"""Pydantic models for the ``--extras`` CLI payload, discriminated on ``operation``."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, TypeAdapter, ValidationError


class CopyRawToVisualizedExtras(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    operation: Literal["copy-raw-to-visualized"]


# Grow into a tagged union once a second operation lands:
#     Extras = Annotated[
#         Union[CopyRawToVisualizedExtras, NewExtras],
#         Field(discriminator="operation"),
#     ]
Extras = CopyRawToVisualizedExtras

_extras_adapter: TypeAdapter[Extras] = TypeAdapter(Extras)


def parse_extras_dict(data: dict) -> Extras:
    try:
        return _extras_adapter.validate_python(data)
    except ValidationError as exc:
        raise ValueError(f"--extras is invalid: {exc}") from exc
