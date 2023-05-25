import argparse
import json
import sys
from pathlib import Path

import jsonschema
from jsonschema import validate


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
    content: list[tuple[str, dict]] = []
    check_files: list[Path] = args.check_files
    for check_file in check_files:
        with check_file.open() as f:
            j = json.load(f)
            content.append((str(check_file), j))
        pass
    errors = validate_files(schema, content)
    if errors:
        # If any error happens
        for error_file, e in errors:
            print(error_file, str(e), file=sys.stderr)
        exit(1)
    return


def validate_files(
    schema: dict, check_contents: list[tuple[str, dict]]
) -> list[tuple[str, jsonschema.exceptions.ValidationError]]:
    """
    Validate all given files with the schema.
    :param schema: Assumed to be valid schema
    :param check_contents: tuple of file name and the json contents
    :return: list of validation errors
    """
    errors: list[tuple[str, jsonschema.exceptions.ValidationError]] = []
    for name, content in check_contents:
        try:
            validate(instance=content, schema=schema)
        except jsonschema.exceptions.ValidationError as e:
            errors.append((name, e))
    return errors


if __name__ == "__main__":
    main()
