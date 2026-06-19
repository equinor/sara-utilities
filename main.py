import argparse
import json
import logging
import sys
from pathlib import Path

from sara_utilities import operations  # noqa: F401  -- registers handlers
from sara_utilities import main_workflow
from sara_utilities.cli_inputs import (
    parse_extras,
    parse_input_blob_storage_locations,
    parse_output_blob_storage_location,
)
from sara_utilities.config.logger import setup_logger
from sara_utilities.config.open_telemetry import setup_open_telemetry

setup_logger()

logger = logging.getLogger(__name__)


def main() -> None:
    setup_open_telemetry()

    logger.info(f"Got command: {sys.argv}")
    parser = argparse.ArgumentParser(description="SARA utility analyzer")
    parser.add_argument("--input-blob-storage-locations", required=True)
    parser.add_argument("--output-blob-storage-location", required=True)
    parser.add_argument("--extras", required=True)
    parser.add_argument("--result-output-file", required=True)
    args = parser.parse_args()

    try:
        input_locations = parse_input_blob_storage_locations(
            args.input_blob_storage_locations
        )
        output_location = parse_output_blob_storage_location(
            args.output_blob_storage_location
        )
        extras = parse_extras(args.extras)
    except ValueError as e:
        logger.error(f"Failed to parse CLI arguments: {e}")
        raise

    logger.info(
        f"Parsed operation={extras.operation} "
        f"inputs={input_locations} output={output_location}"
    )

    main_workflow.run(input_locations, output_location, extras)

    result = {"outputBlobStorageLocation": output_location.model_dump(by_alias=True)}
    Path(args.result_output_file).write_text(json.dumps(result))


if __name__ == "__main__":
    main()
