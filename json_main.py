import argparse
import json
import sys
from pathlib import Path

import jsonschema
from jsonschema import validate

from common import load_jsons, validate_contents

__all__ = ["do_validation"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--schema_file",
        type=Path,
        help="Path of schema JSON",
        required=True,
    )
    parser.add_argument(
        "--check_files",
        type=Path,
        nargs="*",
        help="Paths of JSON to be checked",
        required=True,
    )
    args = parser.parse_args()

    schema_file: Path = args.schema_file
    with schema_file.open() as f:
        schema = json.load(f)
        pass
    content = load_jsons(args.check_files)
    errors = do_validation(schema, content)
    if errors:
        # If any error happens
        for error_file, e in errors:
            print(error_file, str(e), file=sys.stderr)
        exit(1)
    return


def do_validation(
        schema: dict,
        contents: list[tuple[str, dict]],
) -> list[tuple[str, jsonschema.exceptions.ValidationError]]:
    return validate_contents(schema, contents, validate=validate)


if __name__ == "__main__":
    main()
