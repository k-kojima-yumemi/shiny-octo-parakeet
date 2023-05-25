import argparse
import sys
from pathlib import Path

import yaml
from openapi_schema_validator import OAS30Validator, validate

from common import load_jsons, validate_contents


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--schema_file",
        type=Path,
        help="Path of OpenAPI specification",
        required=True,
    )
    parser.add_argument(
        "--target_schema",
        type=str,
        help="Definition name in schemas",
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
    target_schema: str = args.target_schema
    with schema_file.open() as f:
        schema = yaml.safe_load(f)["components"]["schemas"][target_schema]
        pass
    contents = load_jsons(args.check_files)
    errors = do_validation(schema, contents)
    if errors:
        # If any error happens
        for error_file, e in errors:
            print(error_file, str(e), file=sys.stderr)
        exit(1)
    return


def do_validation(schema: dict, contents: list[tuple[str, dict]]):
    return validate_contents(
        schema, contents, validate=validate, validator_class=OAS30Validator
    )


if __name__ == "__main__":
    main()
