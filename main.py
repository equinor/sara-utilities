import argparse
import logging
import sys

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
    raise NotImplementedError("Operation dispatch not yet implemented")


if __name__ == "__main__":
    main()
