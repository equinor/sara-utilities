# SARA Utilities

The **SARA Utilities** analyzer hosts small per-inspection utility
operations (currently: byte-for-byte blob copy from raw to
visualization storage) so that inspection records that have no
applicable analyzer still get a `sara/visualization_available` MQTT
publication. Part of the [SARA](https://github.com/equinor/sara)
ecosystem.

Operations are dispatched by the `extras.operation` field. The first
(and only) operation today is `copy-raw-to-visualized`. New operations
plug in as new sub-handlers without changes to the Argo manifests in
`equinor/analytics-infrastructure`.

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

```bash
uv run pytest
```
