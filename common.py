import json
from pathlib import Path
from typing import Callable

import jsonschema

__all__ = [
    "load_jsons",
    "validate_contents",
]


def load_jsons(paths: list[Path]) -> list[tuple[str, dict]]:
    contents: list[tuple[str, dict]] = []
    for check_file in paths:
        with check_file.open() as f:
            j = json.load(f)
            contents.append((str(check_file), j))
        pass
    return contents


def validate_contents(
    schema: dict,
    check_contents: list[tuple[str, dict]],
    validate: Callable,
    validator_class=None,
) -> list[tuple[str, jsonschema.exceptions.ValidationError]]:
    """
    Validate all given files with the schema.
    :param schema: Assumed to be valid schema
    :param check_contents: tuple of file name and the json contents
    :param validate: validate function. maybe jsonschema#validate or openapi_schema_validator#validate
    :param validator_class: cls parameter for validate function
    :return: list of validation errors
    """
    errors: list[tuple[str, jsonschema.exceptions.ValidationError]] = []
    for name, content in check_contents:
        try:
            validate(instance=content, schema=schema, cls=validator_class)
        except jsonschema.exceptions.ValidationError as e:
            errors.append((name, e))
    return errors
